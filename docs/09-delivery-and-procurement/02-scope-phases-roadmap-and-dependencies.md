# DEL-02 — Phases and dependency roadmap

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Delivery Manager · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Delivery Manager  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-IAM-001–002, FR-DOC-001–003, FR-IMP-001, FR-EXP-001, FR-PUB-001–002, FR-RGT-001, FR-FMT-001, FR-CAT-001, FR-COM-001, FR-FIN-001, FR-OPS-001.

## Scope options

| Option | Deliverable | Dependency and tradeoff | Decision |
|---|---|---|---|
| Lean author-studio-led | Private identity, structured text, durable saves/recovery, snapshots and portable import/export; manual editorial bridge | Lowest scope; no paid publication until rights, production, commerce and finance gates are delivered | Candidate for earliest author pilot |
| Balanced publishing MVP | Lean scope plus editorial, rights, approved renditions, 2D catalog, limited purchase/entitlement and auditable royalty controls | Cross-functional legal, finance, conversion, recovery and provider readiness; marketplace may lag studio | Proposed target, contingent on evidence |
| Broader all-in-one | Adds real-time collaboration, POD/distribution, extensive reader/marketing and optional AI/3D | Higher integration and verification burden; not an unbounded first-release commitment | Later investment decision |

Sequence: (1) research, legal/market and durability design; (2) authoring and recovery, semantic import/export, access and telemetry; (3) controlled editorial/rights, conversion and proof; (4) commerce/ledger, catalog, reconciliation and support; (5) pilot and independent security/accessibility reviews; (6) expansion based on observed outcomes. Rights and provider selection precede live sales; physical print requires vendor-specific proof; 3D remains optional with accessible 2D baseline. Real-time/offline merge and AI are separately validated. Each stage can stop or defer without treating partial payment or unproven backups as production-ready.

## Open questions and references

Which option, team capacity, launch market, pilot thresholds and milestone dates will the Sponsor approve? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Delivery Manager | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
