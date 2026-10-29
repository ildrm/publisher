# OPS-04 — Backup, restore and continuity

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: SRE Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: SRE Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002, FR-OPS-001, FR-FIN-001; NFR-REL-001–004.

## Backup and durability are different

Capture encrypted, access-controlled, versioned database backups and private object versions with integrity checks; include metadata, artifacts, audit, ledger and required encryption keys/configuration in a separately protected recovery plan. Test restore into an isolated environment with synthetic accounts, verify hashes, document version links and financial reconciliation, and record elapsed time and data discrepancies. Protect backups from routine deletion and test retention and key recovery; legal hold and retention are pending jurisdictional decisions.

A proposed 15-minute backup interval is not an allowed loss window for acknowledged edits. The journal/replication and disaster recovery design capable of recovering every acknowledged edit remains unresolved; a successful isolated backup restore alone does not prove this invariant. Before pilot, fault-inject loss immediately after acknowledged commits and demonstrate recovery of each acknowledged revision. Proposed authoring RTO ≤ 4 hours remains unmeasured. If recovery fails, retain read-only mode, escalate as critical and notify under approved policy. Reconcile external payment state before enabling new settlement. Run drills regularly once cadence is approved.

## Open questions and references

What architecture proves no acknowledged loss across declared failures, and who owns backup frequency, retention, key escrow and RTO sign-off? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| SRE Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
