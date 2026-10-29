# ENG-06 — Git, review and delivery definition

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Engineering Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Engineering Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-OPS-001; NFR-SEC-004, NFR-REL-001–004.

## Change workflow

Use small topic branches, protected mainline, peer-reviewed pull requests and explicit ownership. A change description states behavior, risk, migration, rollback, evidence and changed contracts; reviewers independently examine permissions, data handling, invariants and failure paths. Require automated build, unit/contract and security checks plus appropriate integration, browser, accessibility, print, provider and restore evidence before a release. Never merge secrets, customer data or unreviewed generated code. Documentation and traceability update with behavior.

Definition of Ready: agreed owner, testable requirements, dependencies, risk, privacy classification, accessibility and operational impact. Definition of Done: reviewed implementation, reproducible tests, failure/rollback handling, versioned migrations and contracts, privacy-safe telemetry, runbook, release evidence and accepted residual risk. Feature flags default off for risky integrations; irreversible schema changes follow expand/migrate/contract and never remove a column while an older version still needs it. Unexplained acknowledged text loss, ledger imbalance or private exposure blocks release irrespective of schedule.

## Open questions and references

Who are branch owners and independent approvers, and what required checks does the selected CI provide? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Engineering Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
