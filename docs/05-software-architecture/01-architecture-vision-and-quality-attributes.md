# ARC-01 — Architecture vision and quality attributes

Version 0.2 · 2026-10-29 · **Draft — simulated review; human approval pending**

Author/accountable: Solution Architect. Consulted: Document Engineer, Backend, Frontend, Conversion, Security, Accessibility, SRE, Editorial and Finance. Reviewer: Engineering Lead. Approver: Product Owner and Security/Finance/Editorial owners for their gates. Decision owner: Solution Architect. Assumptions: ASM-001–012 and proposed DEC-001–010; a text-centric single-imprint pilot, not approved market or capacity. Related requirements: FR-IAM-002, FR-DOC-002, FR-PUB-002, FR-COM-001, FR-FIN-001. References: [governance](../00-governance/02-decisions-and-open-questions.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md), [standards register](../01-discovery-strategy/07-standards-and-source-register.md).

## Direction and alternatives

| Candidate | Transaction/save reliability | Deployment/team cost | Isolation and extraction | Decision |
|---|---|---|---|---|
| Modular monolith plus isolated workers | One database transaction can commit revision, idempotency receipt and outbox; no distributed commit in save | One API deployment; clear module interfaces still mandatory | Converter processes have separate credentials/network; modules can later extract | Proposed pilot baseline DEC-002 |
| Service-oriented modular application | Authoring, commerce and production can deploy separately; cross-boundary invariants need sagas/reconciliation | More contracts, tracing and staging environments | Useful for dedicated teams or distinct regulatory residency | Reconsider if team/operational ownership warrants |
| Microservices per bounded context | Highest risk of partial writes, stale rights/entitlements and coordination | Highest on-call, schema, networking and test burden | Fine-grained scaling but large fixed cost | Defer absent measured need |

A modular monolith is not one god service or permissionless shared database. Application modules own tables and expose commands/queries. One deployment may share a transaction coordinator but must not bypass another module's business rules. Conversion must run outside the trusted API process because imported files are untrusted and conversions are expensive.

## Quality scenarios and release consequences

| Scenario | Design response | Evidence before enabling |
|---|---|---|
| Connection drops after committed save, before response | After current authorization, retry with the same actor/resource/key returns the committed revision before evaluating base-version conflict | Failure-injection and revoke-before-retry tests; persistent receipts |
| Worker is killed half-way | Staging output remains private; no success pointer until atomic artifact registration | Process kill + lease expiry test |
| Rights expire between scheduling and release | Recheck under transactional release lock at actual release time and again before new sale | Clock/expiry race test |
| Membership is revoked during save | Permission mutation and content mutation serialize on project access epoch; permission wins according to transaction order | Two-session revoke/write race test |
| Processor callback arrives twice or out of order | Signed provider events are deduplicated, verified against provider state and reconciled | Replay/out-of-order fixture suite |

Primary SLOs and workload assumptions are authoritative in [REQ-06](../02-requirements/06-nonfunctional-requirements-and-slos.md). A backup interval does not excuse acknowledged-write loss. Architecture baseline must define the tolerated regional failure and confirm synchronous replica/write-ahead durability and recovery testing before making that promise. Complete-region destruction outside the declared model remains a documented risk, not hidden behind an uptime number.

## Extraction triggers and escape hatches

Extract conversion first if resource contention affects save p95 or untrusted input isolation requires it. Extract commerce if independent regulatory/ownership boundaries demand it; first make outbox/inbox reconciliation observable. Use measured CPU/queue delay, deployment contention and incident ownership rather than guessed user counts. Keep canonical AST export, relational dumps, object manifests and documented events to preserve provider exit. Tenant is an organization/workspace boundary; publisher's imprint is not automatically the owner of an author's workspace.

## Open decisions and cross-role review

Jurisdiction, partner eligibility, operational capacity and product targets remain decisions for their owners at market/vendor/architecture baseline milestones in the governance register. This design must be validated in a prototype and does not assert implemented security, compliance or performance. Architecture review: boundaries and invariants are explicit; Security review: deny-by-default and private data require adversarial testing; QA review: contracts and tests require integration evidence; Editorial/Finance review: release and posting rules require qualified human review. Approvals remain pending.
