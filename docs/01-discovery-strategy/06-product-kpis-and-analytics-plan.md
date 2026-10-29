# DISC-06 — Product KPIs and analytics plan

Version 0.2 · 2026-10-29 · **Draft** · Author: Product Owner · Accountable/decision owner: Product Owner · Consulted: Analytics, Privacy, Editorial, Finance, SRE · Reviewer: Privacy lead · Approver required: Product Owner and privacy lead

**Assumptions:** events are proposed, not collected; consent and retention vary by launch jurisdiction. **Related:** DISC-01, DISC-04, DISC-05; requirements and QA traceability to be completed. **Unresolved:** launch market, consent basis, operational baseline, denominators and target thresholds; owner Product Owner and Privacy lead, before pilot instrumentation.

## Measures and guardrails

| Outcome / owner | Definition and denominator | Interpretation / safeguard |
|---|---|---|
| Author activation / Product | Distinct newly verified eligible authors with a first server-acknowledged chapter within a chosen window / eligible newly verified authors in cohort | Show time-to-first acknowledgement distribution; exclude test accounts; choose window before baseline |
| Author retention / Product | Activated cohort with an acknowledged edit in a later defined period / activated cohort | Cohort by signup month and report churn; activity is not manuscript quality |
| Portability / Product | Successful user-initiated export jobs / eligible export attempts | Include failures and unsupported-structure warnings; success is not proof of fidelity |
| Submission quality / Editorial | Submissions meeting a separately approved structural and eligibility checklist / submitted revisions | Human criteria and sample audit; not a proxy for literary quality |
| Acceptance / Editorial | Distinct submissions accepted / eligible submissions with a final decision in period | Track awaiting decisions separately and median decision time; acceptance is not an edition |
| Publishable output / Production | Rights-cleared editions with required proofs and approvals / accepted projects entering production | Count only complete evidence; report held and failed projects |
| Purchase completion / Commerce | Completed, verified orders / initiated eligible checkouts | Monitor payment failure and abandonment; account for retries and test orders |
| Royalty reconciliation / Finance | Closed period sales/refunds with matched ledger and provider settlement / eligible settlement events | Also report monetary unmatched balance; zero duplicates and reconciled clearing are release controls |
| Data durability / SRE | Confirmed acknowledged-edit losses per incident and affected acknowledgements | Treat any suspected loss as an incident; monitor save failures separately, test restore and acknowledge semantics |
| Trust and quality / Operations | Support tickets per active author; proof rejection rate; rights holds, accessibility defects, fraud and refund rates | Each has separately documented definitions and severity; compare alongside growth, not as a single score |

No measured baselines, conversion forecasts or numerical targets are claimed. Product and owners must set proposed thresholds with pilot capacity and revisit after a baseline is observed. Operational reliability targets and RPO must be defined separately from business metrics; a backup RPO does not authorize loss of acknowledged edits.

### Units, periods and safeguards

Report rates as percentages (`100 × numerator / denominator`), with both raw counts and the selected reporting period. Default operational reporting is a calendar month in UTC; author cohorts use the verification month and an explicitly selected observation window. A zero denominator is **not applicable**, never zero percent. Time-to-event uses elapsed minutes from account verification to first acknowledged chapter and reports median and p95 plus sample count; calendar decision time uses elapsed days from valid submission to final decision. Pending decisions are excluded from the acceptance denominator but reported as a separate count and age distribution. If an author has multiple projects, activation counts the author once, while export attempts count distinct job IDs and retries are reported separately.

Support load is eligible author-support tickets / distinct active authors in the period, expressed as tickets per 100 active authors; active means at least one server-acknowledged authoring action. Proof rejection is distinct rejected proof cycles / distinct proof cycles reviewed, as a percentage. Refund rate is refunded orders / paid orders in an explicitly matched sale cohort, with amount refunded separately in settlement currency; a refund event may be partial. Rights holds, confirmed lost-edit incidents, privacy exposures and accessibility defects are counts by severity, not percentages without an appropriate exposure denominator. Reconciliation exceptions are an event count and an unmatched signed monetary balance grouped by currency; currencies are never summed without a documented conversion basis and date. Small cohorts should be suppressed or aggregated under privacy policy.

## Event contract and privacy

Proposed versioned names: `project.created`, `chapter.save_acknowledged`, `export.requested`, `export.completed`, `export.failed`, `submission.created`, `submission.decision_recorded`, `edition.approved`, `listing.published`, `checkout.started`, `payment.confirmed`, `refund.recorded`, `royalty.posted`, `payout.settled`. Every event has event ID, schema version, occurred-at UTC timestamp, pseudonymous subject/project identifier where necessary, tenant scope, outcome and correlation ID; financial events link to ledger source records. Never emit manuscript body, sensitive notes, payment credentials or AI prompts. Reject or quarantine malformed schemas; deduplicate IDs, document late delivery and reconcile authoritative domain records.

Operational security and audit records have a separately justified purpose, access, retention and deletion policy from optional product analytics. Consent, opt-out and lawful basis require local review. Restrict raw access, aggregate small cohorts, use minimum retention, and do not join to private content. Document collection in a data inventory, test deletion/export behavior, and record all exceptions or legal holds. Metrics derived from events require documented time zone, inclusion/exclusion, late-arrival and correction rules.

## Review checkpoint

| Role | Concern / response | Residual risk | Approver required |
|---|---|---|---|
| Analytics | Event delivery can duplicate or arrive late; IDs and reconciliation specified | Pipeline not built | Analytics lead |
| Privacy | Behavioral instrumentation can expose writing habits; minimize and separate purposes | Legal basis and retention unknown | Privacy lead |
| Finance | Event totals are not accounting authority | Settlement and ledger controls untested | Finance lead |

References: [journeys](05-service-blueprints-and-user-journeys.md); [business model](04-business-model-and-unit-economics.md). No observed KPI values are available.
