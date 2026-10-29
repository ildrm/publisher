# SAMPLE-REF-001 — Executable Python reference illustrations

Version 0.2 · 2026-10-29 · Draft, educational reference only; no production or approval claim.  
Authoring/accountable: Engineering Lead · Consulted: Document Engineering, Security, Finance and QA · Reviewer: Solution Architect · Approver/decision owner: Engineering Lead.  
Assumptions: ASM-001–012, DEC-001–010; related requirements: FR-DOC-001–003, FR-IMP-001, FR-EXP-001, FR-COM-001, FR-FIN-001 and FR-OPS-001. References: [SRS](../../02-requirements/02-system-requirements-specification-srs.md), [patterns](../../06-engineering-handbook/04-coding-patterns-and-anti-patterns.md), [QA catalog](../../07-assurance/02-functional-integration-e2e-test-catalog.md).

Run from repository root using Python 3.14 standard library:

```sh
python3 -m unittest discover -s docs/samples/tests -t docs/samples -v
```

| File / responsibility | Input → output and failures | Security and production limits / tests |
|---|---|---|
| `domain.py`: immutable project/chapter/node and save semantics | Typed project, actor, expected revision and operation key → revision; invalid structure, unauthorized access, stale version and key collision raise errors. | In-memory lock simulates atomic compare-and-save; no durable commit, distributed transaction, storage recovery or real auth. Test immutable nesting, duplicate IDs, stale races, replay after lost response and revocation. |
| `export.py`: job dedupe and promotion | Actor, job key, target, profile, bytes and converter → checksummed artifact; current grant is checked on each request, including replay. Failures preserve the prior good artifact and allow retry with the same work key. | Lock and memory are a simulation; lacks process isolation, malware scan, persisted job state, authorization, crash recovery, validated formats and external storage. Test retries, changed keys and failure. |
| `finance.py`: raw-body HMAC example and balanced entries | Raw bytes, timestamp, signature and account → accepted/duplicate or rejection; integer-unit entries and approved cleared amount → balanced posting or refusal. | HMAC format is illustrative, not any provider's protocol; uses an illustrative timestamp window and account check, but lacks provider-specific canonicalization, order/amount verification, persistent transaction/outbox, real authorization, cash-clearing proof or accounting policy. Caller must reconcile cleared funds independently. Test signature, body changes, duplicate IDs, balances and payout bounds. |
| `upload.py`: limited upload preflight | Filename/bytes/policy → markdown or DOCX label; invalid type, archive path, member count/size/ratio or selected active/XML features are rejected. | Illustrates limits only; not a malware scanner, complete parser or sanitizer. Do not rely on string checks for XML security; production must independently scan, safely parse, sanitize and process under resource-limited isolation. No files are extracted here. Test spoofing, traversal, expansion and active content. |
| `../tests/test_reference.py`: executable checks | Synthetic inputs → `unittest` assertions; fixtures contain no real manuscripts, payment details or keys. | Tests cover bounded examples only; no end-to-end system, independent audit, provider, printer, accessibility or disaster recovery proof. |

All mutable state belongs to an explicit instance rather than global shared state. Production requires database transactions and unique constraints, secure key management, schema validation, tenant-scoped authorization, durable event delivery, provider-specific cryptographic verification, resource isolation, audit and fault injection. In particular no-loss acknowledgement depends on an unresolved recovery architecture, not these examples. The test secret is a synthetic fixture only. Output exceptions are deliberately simple; real APIs should translate them into privacy-safe error contracts.

## Unresolved questions and review

Engineering and Security must select a production language, authentication model, persistence, job and recovery architecture before implementation; Finance must approve accounting and settlement rules. Existing examples are not evidence of those decisions.

| Role | Concern / response | Residual risk | Approval required |
|---|---|---|---|
| Engineering / SRE | Examples illustrate concurrency but not durable storage | Zero acknowledged-loss proof remains open | Engineering / SRE |
| Security | Intake is deliberately limited | No malware or provider integration assurance | Security lead |
| Finance | Balanced example is not real settlement | Jurisdiction and accounting treatment unknown | Finance lead |

## Browser autosave integration example

[frontend-autosave.mjs](../frontend-autosave.mjs) is a browser-neutral JavaScript controller, not a rendered editor. It takes canonical AST snapshots plus a transport adapter and exposes saved/unsaved/saving/failure states. The adapter must send current access epoch, If-Match and Idempotency-Key and translate HTTP errors; no transport, browser persistence or editor library is implemented. The Python `Node` model is an intentionally smaller teaching schema with integer revisions; it is not the wire-format AST or UUID/ETag API adapter. These examples illustrate the same invariants, not a ready-to-connect cross-language application.

Run `node --test docs/samples/tests/autosave.test.mjs`. Three local tests passed on 2026-10-29: identical lost-response retry, in-flight edit acknowledgement ordering, and stale-version manual recovery. Never claim a local recovery copy unless a separate persistence operation confirms one exists. The controller retains memory only; tab/device loss can lose unacknowledged changes.
