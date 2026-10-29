# OPS-01 — Environments and deployment

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: SRE Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: SRE Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-OPS-001; NFR-SEC-001–004, NFR-REL-001–004.

## Environment boundaries

Local development uses synthetic fixtures and no production credentials. Development is isolated for integration; test runs destructive and security exercises against synthetic data; staging mirrors relevant production versions and network controls with provider sandboxes; production is separately secured with scoped access and audit. IaC defines network boundaries, identities, private storage, database, secret references, conversion-worker sandbox, queue, monitoring and backups. Provider, region and topology remain open pending residency, reliability, cost and contract decisions.

A release builds an immutable artifact, verifies provenance and scans, deploys a backward-compatible schema expansion, rolls out behind flags, performs health and synthetic smoke checks, then shifts traffic. Roll back the application if checks fail, but use forward repair or approved restore for destructive migrations and never erase financial history. No production cutover until restore, acknowledged-save durability, legal/finance and security gates are proven. See [backup](04-backup-restore-and-business-continuity.md) and [CI/CD](02-cicd-and-supply-chain-security.md).

## Open questions and references

Which provider, regions, residency controls, environments and deployment topology are approved? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| SRE Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
