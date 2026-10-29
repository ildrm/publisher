# ENG-02 — Repository and module boundaries

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Engineering Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Engineering Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-001–003, FR-RGT-001, FR-PUB-002, FR-COM-001, FR-FIN-001.

## Suggested layout and dependency rule

A future repository may place domain modules under `identity`, `projects`, `documents`, `assets`, `conversion`, `editorial`, `rights`, `catalog`, `commerce`, `ledger`, `notifications` and `operations`; adapters implement ports for storage, queue, provider and time. Public contracts, migration scripts, tests and infrastructure receive separately versioned paths. These are proposals, not a claim the application exists. The domain owns invariants and is independent of HTTP, database and UI; application services orchestrate repositories and external ports; adapters translate protocol and storage. Imports flow inward and are checked in CI.

Within a database transaction, mutate one consistent boundary and write an outbox event; consumers are idempotent and reconcile eventual consistency. The document, edition, order and ledger aggregates have distinct identities and lifecycles. Reject shared-table writes from another domain; expose an explicit interface or event. Extract a service only after measured independent scale or ownership justifies network and operational costs, while maintaining versioned contracts and ownership.

## Open questions and references

Where will actual application source, ownership and transaction boundaries reside after stack selection? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Engineering Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
