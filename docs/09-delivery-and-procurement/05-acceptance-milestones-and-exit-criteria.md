# DEL-05 — Acceptance and exit criteria

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Product Owner · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Product Owner  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002–003, FR-EXP-001, FR-PUB-002, FR-RGT-001, FR-FMT-001, FR-COM-001, FR-FIN-001; NFR-REL-001–004.

## Proposed milestones

| Milestone | Observable evidence | Required accountable sign-off |
|---|---|---|
| Discovery baseline | Market, segment and manuscript corpus selected; assumptions and scope documented | Sponsor / Product |
| Authoring pilot entry | P0 authoring positive, negative and race cases passed; no acknowledged loss under documented injected failures; isolated restore; accessibility and export review | Document Engineering / SRE / Security / Accessibility |
| Publishing pilot entry | Version-matched rights, editorial, metadata, validated renditions and human/physical proof on representative titles | Editorial / Legal / Production / Author as applicable |
| Commerce activation | Verified provider and market; purchase, replay, refund, ledger and payout reconciliation evidence with qualified finance review | Finance / Legal / Commerce |
| General release | S1/S2 closed, support/incident/rollback exercised, risk exceptions time-bounded and signed; human stakeholder approvals | Sponsor and domain owners |

Acceptance artifacts identify build, environment, fixture, requirements, test case, actual result, defects, reviewer and timestamp. Pilot exit requires measured activation, recovery and support outcomes against thresholds chosen before pilot; no metrics are invented here. Rollback uses feature flags/read-only mode, preserves immutable transactions and customer entitlements, and reconciles external provider state. A failed gate blocks the affected release rather than being recategorized as a pass.

## Open questions and references

What quantitative pilot thresholds, acceptance windows, support model and actual signatories will be agreed? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Product Owner | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
