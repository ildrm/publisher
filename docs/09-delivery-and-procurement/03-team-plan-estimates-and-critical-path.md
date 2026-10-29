# DEL-03 — Team, estimates and critical path

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Delivery Manager · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Delivery Manager  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002, FR-FMT-001, FR-RGT-001, FR-FIN-001; NFR-REL-003.

## Team and estimating method

Suggested role mix: Product/BA and delivery; UX research, content, accessibility/i18n; document/editor and frontend; backend/domain and integration; conversion/print; security/privacy; SRE; QA; editorial/rights; finance/royalty; customer support and procurement. Individuals may cover multiple roles only where adequate capacity and segregation of financial approval are demonstrated. Legal, tax, physical proof and independent security/accessibility reviews require qualified external or internal specialists.

Do not present a date or budget as fact. Estimate workstream effort in person-weeks as `base effort × uncertainty factor`; estimate elapsed weeks separately as `effort / productive full-time equivalents`, respecting the dependency graph rather than summing parallel durations; include discovery, implementation, cross-team integration, independent verification, operational readiness and rework. Sum dependency-aware effort, reserve for unknowns, model provider lead time separately, and show low/base/high ranges after team workshops. Include infrastructure as fixed and usage-driven cost plus vendor minimums, proof samples and support; all rates remain unknown.

Illustrative sizing envelopes for an initial planning workshop, not forecasts or procurement quotes: lean Studio-led option **40–100 person-weeks**, balanced publishing MVP **120–300 person-weeks**, broader all-in-one option **300–700 person-weeks**. These are deliberately wide scenario assumptions, not estimates grounded in a staffed backlog or supplier bids. They exclude unforeseen vendor minimums and external-review calendar delays. Workshop owners must replace them with component-level estimates, confidence, staffing availability and critical-path lead times before investment; no duration follows without capacity and dependency assumptions.

Critical path hypothesis: choose market/rights and durability architecture → prove save/recovery and structured schema → import/export and editorial flow → approved format/proof → provider/ledger/reconciliation → integrated security/a11y and restore evidence → pilot exit. Provider procurement and legal decisions run in parallel but can block the paid launch. Track evidence and queue delays weekly; replan if assumptions or staffing change.

## Open questions and references

What actual team availability, rate assumptions, delivery target and procurement lead times are approved? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Delivery Manager | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
