# ENG-07 — Data schema and migration standards

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Data Engineering Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Data Engineering Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002–003, FR-PUB-002, FR-COM-001, FR-FIN-001; NFR-REL-003.

## Data invariants and migrations

Every tenant-owned row includes tenant identity and enforceable access checks; tenant-scoped unique keys include tenant ID where appropriate. Use immutable identifiers, foreign keys, constraints, auditable timestamps and version columns. Document AST schema versions migrate through explicit, tested transforms; reject unknown versions safely and retain original snapshots. Accepted edition artifacts reference immutable source revision, configuration and content hashes. Financial entries are append-only and balanced, carry source idempotency keys and currency, and corrections are linked postings, not destructive updates.

Migrations are versioned, reviewed, reproducible and tested against realistic synthetic data and both old/new application versions. Expand, backfill in resumable chunks, verify counts and checksums, switch reads, then contract after rollback window. Document lock duration, capacity, feature flag and forward-fix/rollback plan; never assume destructive rollback can undo customer writes. Backups and logs cannot by themselves guarantee acknowledged edit durability; a proven journal/replication design remains a release blocker.

## Open questions and references

What database vendor, version, migration tooling, retention and tenancy enforcement approach are chosen? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Data Engineering Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
