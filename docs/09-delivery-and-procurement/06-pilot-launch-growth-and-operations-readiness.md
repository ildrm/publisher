# DEL-06 — Pilot, launch and readiness

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Product Owner · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Product Owner  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-001–003, FR-EXP-001, FR-PUB-001–002, FR-CAT-001, FR-COM-001, FR-OPS-001.

## Pilot plan

Recruit a consented mix of fiction/nonfiction authors and editorial, finance and accessibility participants using synthetic or appropriately licensed manuscripts. Offer trustworthy free drafting and portable export without coercing submission; observe onboarding, first acknowledged chapter, recovery, import and export, and reasons for submission or abandonment. Confirm written consent and data handling, measure outcomes using [KPI definitions](../01-discovery-strategy/06-product-kpis-and-analytics-plan.md), and review feedback without implying interviews occurred. A small curated pilot expands only after quality, rights and support gates pass.

## Launch and operations readiness

- Acquisition hypotheses: author education and templates, creator partnerships, accessible landing pages and a consent-based newsletter; test reach and cost before scaling. Migrating-author import is valuable only if loss reports and user review work.
- Marketplace readiness: vetted listings, sample rights, accurate prices, serviceable customer support, moderated reviews and verified checkout/entitlement. Community and editorial marketplace await moderation and capacity decisions.
- Operations: named on-call and support escalation, rehearsed incident/restore, production secrets and provider readiness, support scripts for failed save/import/rights/refund, documented takedown and appeals, dashboard and rollback owners.
- Expansion: select territories only after legal, payment, tax, localization and print availability reviews; measure retention, published quality, refund and incident rates against predeclared thresholds.

The team should simulate an author recovery, a release hold and ambiguous payout prior to activation, retain evidence and assign unresolved defects. No production readiness or forecast is claimed by this plan.

## Open questions and references

Who will recruit the cohort, fund support/on-call, set success thresholds and approve each launch market? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Product Owner | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
