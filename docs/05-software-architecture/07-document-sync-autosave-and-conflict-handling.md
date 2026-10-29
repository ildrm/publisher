# ARC-07 — Document sync, autosave and conflict handling

Version 0.2 · 2026-10-29 · **Draft — simulated review; human approval pending**

Author/accountable: Solution Architect. Consulted: Document Engineer, Backend, Frontend, Conversion, Security, Accessibility, SRE, Editorial and Finance. Reviewer: Engineering Lead. Approver: Product Owner and Security/Finance/Editorial owners for their gates. Decision owner: Solution Architect. Assumptions: ASM-001–012 and proposed DEC-001–010; a text-centric single-imprint pilot, not approved market or capacity. Related requirements: FR-DOC-001, FR-DOC-002, FR-DOC-003, FR-IAM-002. References: [governance](../00-governance/02-decisions-and-open-questions.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md), [standards register](../01-discovery-strategy/07-standards-and-source-register.md).

## Canonical state and editing engine evaluation

Store versioned structured AST nodes with stable IDs and semantic roles, not arbitrary editor HTML. Arbitrary HTML carries XSS, inconsistent copy/paste and lossy format assumptions. Render to sanitized HTML/EPUB/PDF as a projection; never feed rendered page markup back as source. AST schema migration is explicit with original preservation, warnings and fixture comparisons. Direction is per-document/per-block; Unicode normalization must not alter author-intended text or split grapheme clusters.

| Engine candidate | Decision evidence needed | Exit path |
|---|---|---|
| ProseMirror/Tiptap | Schema and transaction model, IME/accessibility fidelity, extension licensing and collaboration pricing | Canonical AST adapter, editor-neutral test fixtures |
| Lexical | Node model, composition/selection/RTL behavior and conversion extension costs | Versioned JSON adapter and portable snapshots |
| Slate | Normalization/selection complexity for long manuscripts and plugin maintenance | Canonical tree boundary; avoid plugin-specific persistence |

### Primary-source evidence and licensing boundaries

Sources below were checked 2026-10-29. Repository-level licenses describe those source trees only; they do not establish terms for every extension, hosted service, dependency or selected version. Document Engineering owns a pinned dependency inventory and legal review before selection; no editor or commercial service has been selected.

| Candidate | Official-source observation | Unresolved evaluation |
|---|---|---|
| ProseMirror / Tiptap | [ProseMirror state package license](https://github.com/ProseMirror/prosemirror-state/blob/master/LICENSE) and [Tiptap repository license](https://github.com/ueberdosis/tiptap/blob/main/LICENSE.md) identify MIT terms for those sources. [Tiptap documentation](https://tiptap.dev/docs) describes an open-source ProseMirror-based editor alongside separately offered cloud and on-premises capabilities. | Inventory exact packages and extensions, hosted terms, data residency and total costs; validate schema migration and keyboard/IME/RTL behavior. |
| Lexical | [Official repository](https://github.com/meta/lexical) describes an extensible editor framework and identifies an MIT license. | Test its node/selection model, production browser matrix and conversion adapters; vendor claims of accessibility are not a project conformance assessment. |
| Slate | [Official repository and license](https://github.com/ianstormtaylor/slate) identify MIT terms and describe the framework as beta with API stability caveats. | Evaluate API churn, normalization cost, long-document performance and plugin dependencies on a pinned release. |
| Yjs, optional collaboration | [Official Yjs license documentation](https://docs.yjs.dev/license) identifies MIT licensing; [Yjs introduction](https://docs.yjs.dev/) describes CRDT building blocks. | Separately evaluate transport, persistence, authorization, presence, operational cost and provider terms; CRDT use is not a commitment to realtime or offline support. |

Capture package version, license text and notices, dependency SBOM, release maintenance and actual commercial terms in procurement evidence. The sources are descriptive and do not replace legal advice, security review or compatibility tests.

## Pilot save protocol

1. Client applies semantic edits locally and shows `Unsaved`; active IME composition is not split or submitted as final content prematurely.
2. Client validates current schema and queues a bounded full-chapter snapshot with base revision, access epoch and idempotency key; `Saving` is not `Saved`.
3. API authenticates, checks body size/structure, locks project authorization epoch and chapter current pointer, and verifies current permission. Only then may a receipt for the same actor/request be disclosed; lookup precedes stale-base rejection. A changed key payload fails. Revocation wins if its transaction committed first.
4. Under the same transaction and access lock, check base version, write immutable revision, current pointer, receipt and outbox. Acknowledge only after declared durable commit/replica policy succeeds.
5. Client adopts returned revision and shows `Saved`; if further edits exist, it immediately remains `Unsaved` for those edits. Lost response retries reuse the identical key/body. Errors never overwrite local pending text.
6. A 412 stale base offers comparison, recoverable export and an explicitly confirmed new save. Pilot does not silently auto-merge. Restore creates a new revision under the same concurrency protocol.

Revocation serializes with fresh reads/writes under project access epoch. Workers reauthorize before fetching and before publishing results. If a transaction completed before revocation, its acknowledgement may arrive after revocation; audit order explains the race. Existing local copies cannot be remotely guaranteed erased. Offline browser storage is optional, encrypted where platform permits and visibly identified; failure to persist locally must say “Not saved. Keep this tab open or copy your changes.” Do not claim “on this device” unless storage succeeded.

## Collaboration alternatives and deferred behavior

OT needs an ordering/transform authority and transform correctness for every operation. CRDT (e.g. Yjs) supports concurrent merge but adds tombstone/compaction, storage/permission epochs and semantics; it does not solve access revocation or produce finance-grade audit history. Pilot uses server-versioned saves and review comments. Before realtime launch, evaluate concurrent same-paragraph edits, IME/RTL, undo ownership, stale-client resync, snapshot compaction, message/size abuse and revocation mid-session. Presence/cursors are ephemeral and cannot acknowledge saves. Reconnect must fetch fresh permissions and canonical state; preserve unauthorized pending changes only under the approved recovery policy. Neither OT nor CRDT is guaranteed offline support until tested.

## Open decisions and cross-role review

Jurisdiction, partner eligibility, operational capacity and product targets remain decisions for their owners at market/vendor/architecture baseline milestones in the governance register. This design must be validated in a prototype and does not assert implemented security, compliance or performance. Architecture review: boundaries and invariants are explicit; Security review: deny-by-default and private data require adversarial testing; QA review: contracts and tests require integration evidence; Editorial/Finance review: release and posting rules require qualified human review. Approvals remain pending.
