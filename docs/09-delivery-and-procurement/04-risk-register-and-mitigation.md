# DEL-04 — Delivery risk management

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Delivery Manager · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Delivery Manager  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002, FR-RGT-001, FR-PUB-002, FR-COM-001, FR-FIN-001; NFR-REL-003.

## Operating the risk register

The canonical risks and owners are [RSK-001–012](../00-governance/02-decisions-and-open-questions.md). Review likelihood, impact, trigger, mitigation, owner and due milestone at each steering checkpoint; changes to baseline scope or cost require sponsor decision. No probability is asserted without data.

| Priority | Risk and trigger | Required response / evidence |
|---|---|---|
| Critical | RSK-001/010: acknowledgement durability or recovery unproven | Block pilot; prove recovery across failure modes, record independent restore evidence. |
| Critical | RSK-002: private content leakage | Isolate indexes/storage, review access, test canaries and incident response. |
| Critical | RSK-003: missing or expired rights | Hold release; validate scope and obtain qualified review. |
| Critical | RSK-004: duplicate or unbalanced financial posting | Block live settlement; replay and reconciliation tests with finance sign-off. |
| High | RSK-005/006/012: inaccessible or inaccurate rendition/proof | Validate with corpus, assistive technology and physical printer proof. |
| High | RSK-007/009: jurisdiction or vendor unavailable | Keep paid flow disabled, choose supported market/partner based on dated evidence. |
| High | RSK-008: scope/capacity exceeds plan | Defer features and rebaseline milestones; never waive critical invariants. |

Escalation records decision, alternatives, owner, compensating control and expiry. Sponsor accepts residual business risks; designated security, legal, finance and accessibility owners must accept their own domain risks. Simulated review does not constitute acceptance.

## Open questions and references

Who holds each risk, what capacity and due dates are available, and what escalation threshold is approved? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Delivery Manager | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
