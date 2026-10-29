# OPS-03 — Observability, SLO and incidents

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: SRE Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: SRE Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002, FR-FMT-001, FR-COM-001, FR-FIN-001, FR-OPS-001; NFR-REL-001–004.

## Indicators and alert routing

Instrument save commit and acknowledgement, unsaved/conflict rate, queue age and conversion failures, public index lag, payment confirmation and entitlement lag, refund/payout reconciliation, ledger imbalance and optional 3D fallback. Report latency and availability by eligible request denominator, plus low-volume raw counts; proposed targets and exclusions are in [NFRs](../02-requirements/06-nonfunctional-requirements-and-slos.md). Logs contain correlation, tenant-safe identifiers and failure class, not content, credentials or financial secrets. SRE owns routing; document, conversion, commerce and finance owners receive their respective actionable alerts.

## Incident runbook

1. Triage symptom, scope, time and severity; assign incident commander, scribe and channel. Treat acknowledged text loss, private exposure, duplicate payouts or unauthorized release as critical.
2. Contain via safe feature flags or read-only mode; preserve audit evidence, do not delete data or blindly retry payments. Engage domain owners and Legal/Privacy when indicated.
3. Diagnose using correlation IDs and versioned events. Communicate status and known impact to authorized affected users without exposing content; counsel decides notification obligations.
4. Restore/reconcile, verify data and ledger, return service gradually, monitor recurrence and record timeline. Assign root-cause actions and deadlines; do not assert recovery without evidence.

Exercise paging, status communications and escalation before launch; on-call rotation and incident SLAs are not yet established.

## Open questions and references

Who is on call, what alert thresholds apply to actual workload, and who decides external notifications? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| SRE Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
