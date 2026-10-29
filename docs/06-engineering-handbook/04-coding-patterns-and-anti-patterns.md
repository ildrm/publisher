# ENG-04 — Patterns and anti-patterns

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Principal Architect · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Principal Architect  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002–003, FR-FMT-001, FR-COM-001, FR-FIN-001.

## Decision patterns

| Problem | Preferred pattern | Failure to avoid |
|---|---|---|
| Save concurrent edits | Version precondition; commit then acknowledge; offer manual recovery from a verified client copy where available, otherwise warn and offer immediate copy/export where possible | Last-write-wins silent overwrite or marking a queued request saved |
| Publish approved revision | Version-bound approval and rights check in transaction; immutable artifact | Editing rendered HTML as source, releasing changed artifact under stale approval |
| Export or webhook | Resource-limited job, idempotency key, checksum, outbox and reconciliation | Blind retries, duplicate charge, overwriting a known-good rendition, swallowing failure |
| Cross-context change | Transactional outbox and versioned events with retry/dead-letter and reconciliation | Shared DB coupling or synchronous distributed transaction |
| Authority | Current server-side RBAC/ABAC checks at resource boundary | Frontend-only checks or unrestricted admin impersonation |
| Design evolution | Cohesive domain aggregates and narrow ports | God service, anemic domain with rules in controllers, distributed monolith, shared mutable singleton |

Events are at-least-once unless a provider proves otherwise; duplicate and out-of-order handling are explicit. An idempotency key must bind to request parameters and result, reject conflicting reuse, and be stored atomically with the action. Externally visible money movement requires reconciliation before retries when outcome is uncertain.

## Open questions and references

What storage/queue capabilities support these patterns, and what measured triggers justify extraction? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Principal Architect | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
