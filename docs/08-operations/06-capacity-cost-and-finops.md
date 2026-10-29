# OPS-06 — Capacity and cost model

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: FinOps Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: FinOps Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002, FR-FMT-001, FR-COM-001; NFR-PERF-001–002.

## Cost model and capacity decisions

Estimate monthly cost as fixed platform and staffing + active authors × usage per author × unit rates + retained GB × storage rate + export jobs × worker cost + egress + payments, tax services, monitoring and support. AI, 3D, print and distribution are separate optional drivers; do not insert unverified prices. A scenario table should show low/base/high active authors, manuscripts per author, mean and tail manuscript size, saves/day, export jobs/title, CPU seconds, retained versions, peak concurrency and provider fees, with sensitivity and uncertainty per input.

Measure cost per active author, saved GB, successfully delivered export and reconciled purchase; tag by environment and service without manuscript text. Autoscale worker queues with budgets and backpressure while protecting save traffic; set alerts on storage growth, queue age and unusual spend. Stress-test peaks and backup/recovery overhead before committing capacity. Avoid optimizing away redundancy needed for acknowledged-save durability or audit retention.

## Scenario worksheet and decisions

| Driver | Low / base / high input (owner supplies values) | Sensitivity and monitoring |
|---|---|---|
| Active authors, saves/day, peak concurrent editors | Product and SRE select cohort and concurrency before load test. | Scale application and durable write capacity; alert on latency and failed acknowledgements. |
| Manuscript size, revisions, backups, retained GB | Document Engineering and Privacy choose fixture distribution and retention policy. | Storage, replication, backup and restore egress drive cost; never remove recovery guarantees to meet budget. |
| Exports/title, pages, CPU seconds, queue peak | Conversion and SRE measure worker duration and failures. | Set queue backpressure and per-tenant limits; keep authoring capacity isolated. |
| Purchases/refunds, provider fixed and per-event charges | Finance obtains territory-specific written rates and tax assumptions. | Reconcile per-transaction fees separately from royalties and report uncertainty. |
| Support hours, security review, physical proofs and optional AI/3D | Delivery and domain owners estimate effort and obtain quotes. | Track fixed commitments, usage costs and one-time launch costs independently. |

Model total monthly cost using the prior formula for each input set, show currency and rate date, and perform one-at-a-time sensitivity on the largest unknowns. No input figures, supplier rates or measured cost are asserted. FinOps owner updates this worksheet after vendor selection and pilot telemetry.

## Open questions and references

What observed workload, unit rates, vendor minimums, cost allocation tags and authorized budget apply? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| FinOps Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
