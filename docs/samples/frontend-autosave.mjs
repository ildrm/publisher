/** Browser-neutral editor integration illustration. No editor library, durable storage or UI is implemented.
 * transport receives canonical AST, If-Match etag and stable Idempotency-Key; production adapter
 * must include current access epoch and map 401/403/412 to typed errors. Never log draft content.
 */
export class AutosaveController {
  constructor({ transport, etag, keyFactory = () => crypto.randomUUID(), onState = () => {} }) {
    this.transport = transport;
    this.etag = etag;
    this.keyFactory = keyFactory;
    this.onState = onState;
    this.generation = 0;
    this.savedGeneration = 0;
    this.draft = null;
    this.pending = null;
    this.flight = null;
    this.blocked = false;
    this.state = 'saved';
  }
  notify(state) { this.state = state; this.onState(state); }
  edit(ast) {
    this.draft = structuredClone(ast);
    this.generation += 1;
    if (!this.blocked) this.notify('unsaved');
  }
  flush() {
    if (this.blocked) return Promise.reject(new Error('Manual recovery or renewed permission required'));
    if (this.flight) return this.flight;
    // Reserve a shared promise before callbacks run; concurrent flushes cannot create duplicate requests.
    this.flight = Promise.resolve().then(() => this.run()).finally(() => { this.flight = null; });
    return this.flight;
  }
  async run() {
    while (this.savedGeneration < this.generation) {
      // Retain identical request and key across lost-response/network retries, even if a newer draft exists.
      this.pending ??= {
        generation: this.generation, ast: structuredClone(this.draft), etag: this.etag, key: this.keyFactory()
      };
      this.notify('saving');
      let result;
      try {
        result = await this.transport(this.pending.ast, {
          etag: this.pending.etag, idempotencyKey: this.pending.key
        });
        if (!result || typeof result.etag !== 'string' || typeof result.revisionId !== 'string') {
          throw new Error('Invalid save acknowledgement');
        }
      } catch (error) {
        if ([401, 403, 404, 409, 412, 422].includes(error.status)) this.blocked = true;
        this.notify(this.blocked ? 'recovery-required' : 'not-saved');
        throw error;
      }
      this.etag = result.etag;
      this.savedGeneration = this.pending.generation;
      this.pending = null;
      this.notify(this.savedGeneration === this.generation ? 'saved' : 'unsaved');
    }
    return this.etag;
  }
}
// Editor adapter: call edit only after committed semantic transactions (respect IME composition).
// Debounce flush outside this class; render state in an aria-live polite status region.
// On 'not-saved', say: 'Not saved. Keep this tab open or copy your changes.'
// Only claim a local recovery copy after a separate storage write succeeds and is verified.
// On 'recovery-required', offer compare/export and fresh permissions; do not silently overwrite.
