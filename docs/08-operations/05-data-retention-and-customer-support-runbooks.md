# OPS-05 — Retention and support runbooks

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Support Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Support Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-IAM-002, FR-EXP-001, FR-OPS-001; NFR-PRIV-001–002.

## Retention and deletion policy design

Classify manuscript content, assets, account PII, logs, entitlements, financial records, audit and backups separately. Retention duration, deletion exceptions, residency and legal holds require qualified counsel in each launch market; do not invent dates. Maintain a scheduled policy engine with deletion evidence, scoped holds, review deadlines and backup expiry behavior. Export must remain accessible to authorized authors who never publish, subject to documented lawful exceptions. Public removal and legal hold do not imply immediate destruction of required financial evidence.

## Support flow

Verify identity and project scope; capture operation ID and symptom without asking for manuscript or card data. Explain save state and offer user-directed recovery or export. Support access requires specific time-limited purpose, authorization and audit; no silent impersonation. For rights/takedown, preserve evidence, temporarily hold if authorized, assign human reviewer, notify and provide appeal/reinstatement route. For payment or payout uncertainty, route to Finance for provider reconciliation before retry or adjustment. Escalate suspected privacy exposure to incident command and Legal. Record outcome without copying content into tickets.

## Open questions and references

What user support hours, access approval mechanism, deletion schedule, legal holds and notification timelines apply? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Support Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
