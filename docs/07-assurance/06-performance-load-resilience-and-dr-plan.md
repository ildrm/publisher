# QA-06 — Performance, load, resilience and disaster recovery

Version 0.3 · 2026-10-29 · Status: Draft assurance plan; bounded local implementation evidence is recorded separately, not full target acceptance  
Authoring/accountable: SRE Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: SRE Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002, FR-EXP-001, FR-FMT-001, FR-COM-001, FR-FIN-001, FR-OPS-001; NFR-REL-001–004, NFR-PERF-001–002.

## Method and proposed tests

Baseline an agreed device, manuscript corpus, region, users, payload sizes, throughput and network profile before making claims. Measure p50/p95/p99 editor interaction and save acknowledgement, server error rate, memory growth for 100k-word manuscripts, conversion queue age, job duration and throughput, catalog search and checkout. Exercise normal, peak and burst loads, worker saturation and recovery; isolate dependencies and report denominators, warm-up and rejected traffic. Alert when budget burn or queue age threatens operations; cost is measured per active author, retained GB and export after prices are selected.

Fault-inject connection drop before commit, commit before response, stale writes, primary loss after acknowledged commit, worker kill, queue redelivery, provider timeout, lost webhook, corrupted backup and region outage. Test both confirmed local recovery and denied, full, cleared or unavailable device storage; never claim an unverified copy exists. In the latter case preserve the unsaved warning and offer immediate copy/export where possible; stale writes require manual resolution. NFR-REL-003 requires **no loss of acknowledged edits**; a 15-minute backup interval is not a permitted loss window. The replication/journal/recovery design remains unresolved and must be proven by failure-injection and isolated restore before pilot. Proposed RTO ≤ 4 hours is a target, not measured performance. Restore docs, metadata, audit and ledger to a consistent point, verify checksums and reconciliation, record start/end, lost/unrecoverable operations and evidence, and involve SRE, Finance and document owners.

3D is optional: profile frame time and memory against a selected device, honor reduced motion, and demonstrate the accessible 2D baseline whenever WebGL fails. Exercise rollback and feature flags without rolling back immutable financial history or destroying newer database data.


## Planned NFR test IDs

The following cases define the broader target coverage, not a claim that every case has run or passed. Bounded local authoring checks and the current multilingual run status are recorded in [implementation evidence](../../implementation/test-evidence.md); production, manual and later-feature acceptance remain open. Each owner records inputs, environment, observed result, source evidence and defects against the approved target. See security and accessibility plans for execution methods.

| Case | Setup and expected evidence / owner |
|---|---|
| TC-NFR-SEC-001 | Cross-tenant and revoked-role requests denied at every endpoint and job; Security. |
| TC-NFR-SEC-002 | Inspect transit/rest encryption and key rotation with controlled test keys; Security. |
| TC-NFR-SEC-003 | Hostile files and archive bombs rejected within sandbox limits; Security/Conversion. |
| TC-NFR-SEC-004 | Privileged login requires MFA and protected audit records identify actor and outcome; Security. |
| TC-NFR-PRIV-001 | Seeded private canaries absent from public index, CDN, logs and telemetry; Privacy. |
| TC-NFR-PRIV-002 | AI request without specific opt-in is denied; revocation and provider terms reviewed before enablement; Privacy. |
| TC-NFR-REL-001 | Kill process before/after commit and verify no false save acknowledgement; Document Engineering. |
| TC-NFR-REL-002 | Measure eligible authoring successes / total over declared window and compare with proposed objective; SRE. |
| TC-NFR-REL-003 | Simulate failure just after acknowledgement and recover every acknowledged revision; time isolated restore and reconcile data; SRE. |
| TC-NFR-REL-004 | Fail/retry imports, exports and stale writes; source intact and no duplicate final artifact; Conversion. |
| TC-NFR-A11Y-001 | Manual keyboard and assistive-technology assessment plus automated checks against scoped target; Accessibility. |
| TC-NFR-A11Y-002 | Validate export semantic structure, reading order and unresolved warnings with manual review; Accessibility. |
| TC-NFR-I18N-001 | Edit, save, reload, restore and portable export mixed RTL/LTR, CJK and combining marks without corruption. Switch interface languages while unsaved without remount, selection/undo loss, metadata mutation or extra revision. Real IME/device review is separate from synthetic input; Localization/Document Engineering. |
| TC-NFR-I18N-002 | Check all 15 catalogs for key/placeholder parity, nonempty values and count forms; switch every interface independently of manuscript direction; verify Intl formatting, RTL/reflow, message descriptors, device/browser/account preferences, restricted storage, synchronization failures and schema-1 migration. Obtain actual language review before pilot; Localization/QA. |
| TC-NFR-PERF-001 | Measure p95 interaction on agreed device with 100k-word fixture against provisional target; Performance QA. |
| TC-NFR-PERF-002 | Measure p95 end-to-end acknowledgement with declared connection and denominator; Performance QA. |
| TC-NFR-PERF-003 | Measure p95 public-only catalog search under the stated pilot dataset and load profile; Search/Performance QA. |
| TC-NFR-PERF-004 | Measure queue plus processing duration and success/failure denominator for the 100k-word EPUB fixture; separately document pending print-PDF target; Conversion/Performance QA. |
| TC-NFR-PERF-005 | On selected low-power device, measure 3D frame time or verify accessible 2D fallback and reduced-motion behavior; Frontend/Accessibility. |
| TC-NFR-PERF-006 | Measure peak editor heap and initial payload bytes on named devices with the 100k-word fixture; Document Engineering. |
| TC-NFR-SCALE-001 | Run declared low/base/high workloads, batch imports and sales; record saturation, queue age and error rates; SRE. |
| TC-NFR-COST-001 | Reconcile modeled monthly cost allocations against infrastructure invoices and declared active-author, stored-project and export denominators; FinOps. |
| TC-NFR-OPS-001 | Inject backup, queue and reconciliation failures and exercise alert routing; SRE. |
| TC-NFR-OPS-002 | Inspect structured logs for correlation IDs and absence of private canaries and secrets; Security/SRE. |
| TC-NFR-FIN-001 | Replay sale/refund events and assert balanced postings, unique keys and reconciliation; Finance/QA. |

## Open questions and references

What workload distribution, device profile, durability architecture, capacity budget and disaster recovery topology are approved? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| SRE Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
