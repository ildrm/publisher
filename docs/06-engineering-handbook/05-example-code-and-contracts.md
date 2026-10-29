# ENG-05 — Reference example index

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Engineering Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Engineering Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-001–003, FR-EXP-001, FR-COM-001, FR-FIN-001, FR-OPS-001.

## Reference sources and verification

These files are Python 3.14 standard-library educational artifacts; they are not production components, deployable services, provider integration or proof of durable recovery. See the [sample README](../samples/reference/README.md) for inputs, outputs, failure modes, security boundaries and test coverage.

| Source | Illustrates | Principal limitation |
|---|---|---|
| [domain.py](../samples/reference/domain.py) | Immutable manuscript structure; current authorization before idempotent receipt, then stale revision check. | Process-local lock and memory; no durable database, distributed locking or real identity. |
| [export.py](../samples/reference/export.py) | Per-request authorization, deduplication, same-key retry after failure and preservation of prior artifact. | No real worker isolation, persistence, permission service, validator or storage. |
| [finance.py](../samples/reference/finance.py) | Timestamped raw-body HMAC/account check, idempotency, balanced entries and bounded payout. | Illustrative signature scheme, not a verified provider implementation; no real settlement or approved accounting. |
| [upload.py](../samples/reference/upload.py) | Basic type and archive limits, traversal and selected unsafe-content rejection. | Neither malware scanner nor complete secure DOCX/XML parser; isolation and scanning remain required. |
| [test_reference.py](../samples/tests/test_reference.py) | Synthetic unit checks, including concurrency, reauthorization and retry. | Does not test a distributed service, restore, provider or accessible UI. |

On 2026-10-29, `python3 -m unittest discover -s docs/samples/tests -t docs/samples -v` passed **16 tests** on Python 3.14.5 in the local workspace. That result applies only to these bounded examples; it is not conformance, safety or delivery acceptance evidence. Production stack selection, schema and contract alignment, real authorization, provider-specific verification, persistence, isolation and disaster recovery remain open. No fictional implementation is implied.

## Open questions and references

Which contract schemas, selected stack and production integrations will be independently verified? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Engineering Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |

## Frontend and contract examples

The [browser-neutral autosave controller](../samples/frontend-autosave.mjs) and [three Node tests](../samples/tests/autosave.test.mjs) exercise lost-response retry, subsequent edits while saving, and stale-version recovery. The controller consumes canonical JSON through an adapter; the Python sample uses a reduced teaching AST and integer revisions, so neither is falsely presented as a complete API client. [OpenAPI](../contracts/openapi.yaml), [AsyncAPI](../contracts/asyncapi.yaml) and [canonical AST schema](../contracts/schemas/manuscript-ast.v1.schema.json) are documentation contracts. Structural checks and event fixtures do not replace full standards validators or implemented contract tests.

## Subsequent local implementation

The bounded examples above remain teaching code. The actual local Author Studio is separate under apps/api, apps/web and packages/editor; see [implementation evidence](../../implementation/README.md). Its canonical v2/cookie runtime has explicit deltas from the representative v1 design contract. No later publishing, finance or production readiness is implied.
