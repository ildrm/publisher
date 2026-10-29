# ENG-01 — Candidate stack and tradeoffs

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Engineering Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Engineering Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002, FR-FMT-001, FR-COM-001; NFR-REL-001–004.

## Selection is provisional

Reference snippets use Python standard-library type-annotated examples only; they demonstrate contracts, not a deployed platform. The production stack remains undecided. Compare TypeScript/React/Next.js with alternatives on editor accessibility and deployment; Python, TypeScript and JVM frameworks on team skill, transactions and operability; PostgreSQL and comparable relational stores on transactional constraints and recovery; object storage on versioning and private access; durable queues on redelivery and visibility; and WebGL/Three.js on optional 3D performance and licensing. Verify current version, license, security maintenance, data residency, portability, cost and support before selection. No package capability or provider availability is assumed.

Favor modular boundaries and isolated conversion workers as the DEC-002 proposal; neither a microservice fleet nor one undifferentiated service is required. A separate search service only becomes justified by measured needs; public indexing and private search must remain isolated. Use independent interfaces for payments, storage, search and conversions, with exports and migration tests as exit mechanisms. CRDT/OT selection is deferred until collaboration is a funded scope and threat/merge experiments support the choice.

## Open questions and references

Which team skills, vendor contracts, editor license, production language and recovery topology are accepted? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Engineering Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
