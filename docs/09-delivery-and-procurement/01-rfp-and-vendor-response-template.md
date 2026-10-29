# DEL-01 — RFP and vendor scorecard

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Procurement Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Procurement Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002, FR-EXP-001, FR-RGT-001, FR-FMT-001, FR-COM-001, FR-FIN-001; NFR-SEC-001–004.

## Bidder response template

Request bidder identity, ownership, references and publishing experience; proposed architecture with trust boundaries, transaction and recovery design; delivery team and role commitments; evidence of secure SDLC and accessibility practices; named licensed components, versions, restrictions and sub-processors; import/export and printer capability; provider/market availability with dated evidence; implementation plan by module and dependency; assumptions, exclusions, acceptance and change control; milestone and support costs broken into one-time/recurring/variable; IP and source repository access; operational support/SLA; migration, portability and exit assistance. Require clear distinctions between existing capability, planned work and third-party dependencies. No submission may assert compliance without evidence.

Require sandbox demonstrations: recover an acknowledged edit after an injected failure; reject a stale save; export an unpublished manuscript with mixed RTL content; block release without valid rights; validate an EPUB and printer-specific proof; replay a payment callback and reconcile a refund/royalty; demonstrate accessible 2D preview and optional labeled 3D. Specify data set, expected result, reviewer and evidence for each. Define acceptance as jointly reviewed test results rather than slideware.

## Proposed scorecard

| Criterion | Weight | Evaluation anchor |
|---|---:|---|
| Document durability, portability and recovery | 25 | Demonstrated fault cases and export fidelity |
| Security, privacy and accessibility | 20 | Evidence, threat response and accessible tasks |
| Publishing, rights and format fidelity | 20 | Exact proof/rights workflows and references |
| Finance, integrations and reconciliation | 15 | Idempotency, audit and market/provider evidence |
| Delivery team, governance and support | 10 | Named role capacity, quality and continuity |
| Total cost, IP and exit | 10 | Transparent lifecycle costs and portable source/data |

Score each 0–5 with evidence and weighted normalization; a zero or unacceptable gap in durability, privacy, rights or finance is a disqualifying gate, not something price can offset. Confirm weights and conflicts of interest before procurement. Draft contract must specify deliverables, acceptance window, defect remedy, confidentiality, processor obligations, audit rights, escrow/exit, change-order approval, payment milestones and termination obligations, subject to qualified legal review.

## Open questions and references

What budget, markets, procurement terms, bidder shortlist and acceptance signatories apply? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Procurement Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
