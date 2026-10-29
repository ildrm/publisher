# SRS-001 — System requirements specification

Version 0.2 · 2026-10-29 · Status: Draft, not approved  
Authoring/accountable: Requirements Engineer · Consulted: Product, Document Engineering, Editorial, Security, Finance, Accessibility · Reviewer: Solution Architect · Approver and decision owner: Product Owner  
Assumptions: ASM-001–012; decisions DEC-001–010. Related requirements: FR-IAM-001–002, FR-DOC-001–003, FR-IMP-001, FR-EXP-001, FR-PUB-001–002, FR-RGT-001, FR-FMT-001, FR-3D-001, FR-CAT-001, FR-COM-001, FR-FIN-001, FR-OPS-001 and NFR-SEC/REL/A11Y/I18N/PERF/OPS/PRIV/FIN. Requirements are proposed unless explicitly derived from the supplied brief. See [feature catalog](03-feature-catalog-and-prioritization.md), [rules](05-business-rules-and-permissions.md), [SLOs](06-nonfunctional-requirements-and-slos.md), and planned test traceability (`../07-assurance/07-requirements-to-test-traceability.md`). The structure borrows requirements discipline from ISO/IEC/IEEE 29148; it does not assert certification.

## Scope and requirement interpretation

The system comprises browser interfaces, application services, durable stores and isolated asynchronous workers, with payment, communication and production partners outside its trust boundary. IDs below are capability-level parents; numbered clauses are individually verifiable child requirements, each inheriting the parent's release and ownership. P0 means proposed launch foundation; availability of an external partner is a prerequisite, not a promise. Verification methods: T = automated or manual test, I = inspection, D = demonstration. All P0 clauses require recorded passing evidence and owner sign-off before their capability is enabled.

| ID | Requirement: the system shall… | Priority / verification | Rationale / dependency |
|---|---|---|---|
| FR-IAM-001.1 | authenticate a user before granting private workspace access. | P0 / T | Private content boundary; identity service |
| FR-IAM-001.2 | require step-up MFA for privileged publisher, finance and platform administration sessions. | P0 / T | Reduce privilege abuse |
| FR-IAM-002.1 | authorize each private resource operation on the server against current membership and role, including tenant and project scope. | P0 / T | Revocation and isolation |
| FR-IAM-002.2 | reject an expired, revoked or insufficient grant without disclosing private content. | P0 / T | Access control |
| FR-DOC-001.1 | create a project with an ordered collection of semantically structured chapters in a private workspace. | P0 / T | Manuscript structure |
| FR-DOC-002.1 | distinguish local unsaved changes, in-flight changes, acknowledged durable saves and failed saves in the editor. | P0 / T | Trust; persistence contract |
| FR-DOC-002.2 | acknowledge a save only after its accepted document version is committed to durable storage. | P0 / T | Recovery; optimistic version check |
| FR-DOC-002.3 | reject stale writes without silently overwriting a newer accepted version; preserve unsynced content where local recovery succeeds and show an immediate copy/export option when it does not. | P0 / T | Race safety; local device persistence cannot be guaranteed |
| FR-DOC-003.1 | restore a selected authorized snapshot as a new revision without deleting the current revision. | P0 / T | Reversible recovery |
| FR-IMP-001.1 | validate and scan an uploaded supported DOCX or Markdown file before isolated conversion. | P0 / T | Safe ingest |
| FR-IMP-001.2 | provide a reviewable import report identifying unsupported or changed structures before an author confirms import. | P0 / T | Prevent silent loss |
| FR-EXP-001.1 | let an authorized author export manuscript content and relevant metadata without submission or publication. | P0 / T | Portability |
| FR-EXP-001.2 | provide export status and actionable failure detail, and retain the source revision on failure. | P0 / T | Reliability |
| FR-PUB-001.1 | create a submission referencing an immutable manuscript revision and author declarations. | P0 / T | Review reproducibility |
| FR-PUB-001.2 | restrict review assignment and decisions to authorized editorial roles and notify the author of the decision. | P0 / T | Traceability |
| FR-RGT-001.1 | record versioned rights grants by work, contributor, territory, language, format, channel and term. | P0 / T | Rights are scoped, never presumed |
| FR-RGT-001.2 | block release when the proposed distribution scope is not covered by a current approved grant. | P0 / T | Rights gate |
| FR-FMT-001.1 | generate a versioned rendition from an identified revision, format profile and asset set in a resource-limited worker. | P0 / T | Reproducibility |
| FR-FMT-001.2 | retain validation results and block release of a failed or unapproved rendition. | P0 / T | Format and proof quality |
| FR-PUB-002.1 | record distinct editorial, rights, metadata, rendition and proof approvals against their approved versions before release. | P0 / T | Release control |
| FR-PUB-002.2 | publish only a versioned listing and approved rendition; later corrections create a traceable release version. | P0 / T | Stable customer artifact |
| FR-CAT-001.2 | provide an accessible 2D cover and text equivalent as the baseline preview, including when optional 3D is unavailable or unsuitable. | P0 / T | Usability independent of optional 3D |
| FR-3D-001.1 | if a 3D preview is enabled, use accurate dimensions or clearly label estimated geometry and identify the assumptions used in the mockup. | P1 / T; optional pilot candidate | Avoid misrepresenting manufacturing |
| FR-CAT-001.1 | index only released public listing data and authorized samples in the public catalog. | P0 / T | Privacy boundary |
| FR-COM-001.1 | grant an entitlement only after verified payment confirmation, and associate it with the purchased product and buyer. | P0 / T | Licensed delivery |
| FR-COM-001.2 | process repeated provider events idempotently and reconcile missing or disputed confirmations. | P0 / T | No duplicate purchase/entitlement |
| FR-FIN-001.1 | post balanced, attributable ledger entries for sale, refund and royalty adjustments with a unique source event. | P0 / T | Auditable financial truth |
| FR-FIN-001.2 | record settlement and payout status separately from earned royalty and reconcile failures without duplicate disbursement. | P0 / T | Reliable payment |
| FR-OPS-001.1 | record security, approval and financial changes in a protected audit trail with actor, time, resource and outcome. | P0 / T | Accountability |
| FR-OPS-001.2 | back up and restore document, metadata and ledger data together to a consistent recoverable point. | P0 / D | Business continuity |

## High-risk acceptance scenarios

These examples supplement, rather than replace, the tests in the catalog and assurance plan.

**FR-DOC-002 — save and conflict**
1. Given an authorized editor has changed a chapter, when the server commits the accepted version, then the UI displays “Saved” with the committed version.
2. Given a connection fails before acknowledgement, when the save fails, then the UI says “Not saved” and offers retry; it claims a local recovery copy exists only after that copy is confirmed. If local storage fails, it offers immediate copy/export where possible.
3. Given another session has committed a newer version, when a stale version is submitted, then the server rejects it and offers comparison or an exportable recovery copy; it does not overwrite the newer version.

**FR-DOC-003 — restore**
1. Given an authorized author selects an existing snapshot, when they confirm restore, then a new revision contains that snapshot and the preceding revision remains recoverable.
2. Given a viewer without edit rights, when they request restore, then the server denies the operation and the current revision remains unchanged.
3. Given the current revision changed after the restore screen loaded, when restore is confirmed, then the server reports a conflict and requires a fresh review.

**FR-PUB-002 — release**
1. Given current rights and all approvals match the exact rendition and metadata, when an authorized publisher releases, then a versioned listing becomes visible at its scheduled time.
2. Given a rights territory is missing, when release is attempted, then the operation is blocked with an actionable rights issue and no listing becomes public.
3. Given an approved artifact was replaced after approval, when release is attempted, then its prior approval is invalid for the replacement and publication is blocked.

**FR-COM-001 and FR-FIN-001 — money**
1. Given a verified successful payment event, when processed once, then one purchase, entitlement and corresponding balanced postings are recorded.
2. Given the same event is delivered again, when the handler retries, then no duplicate entitlement, charge or ledger posting is created.
3. Given a refund or payout fails or is disputed, when its status is reconciled, then the original entries remain traceable, compensating entries are linked, and support can see the unresolved status without a second disbursement.

## Operational interfaces and constraints

All mutation endpoints require authenticated, current server-side authorization, validated input, correlation ID and optimistic version or idempotency key where appropriate. Uploads have byte/type/structure limits configured by deployment; proposed limits need load and security testing before implementation. API and event shapes are defined in planned contracts (`../contracts/openapi.yaml`), not by this summary. Accessible labels, focus order, error announcements and independent UI/content direction apply to all flows. Local copies and backup retention must follow jurisdiction-approved schedules; no retention duration is asserted here. Telemetry must not include manuscript text, credentials or payment details.

## References

Source: *Online Publishing Super Mega Documentation Prompt*, version 1.0, sections 0–3 and 5–7 (user-supplied); [scope and assumptions](../00-governance/01-scope-and-assumptions.md); [decisions and open questions](../00-governance/02-decisions-and-open-questions.md). Planned downstream artifacts are identified as planned in the text.

## Open questions and review

Requirements owners must resolve launch market, valid provider event semantics, print presets, retention limits and concrete upload limits before build sign-off; see governance register. Each scenario needs test fixture, environment and evidence recorded by QA; draft scenarios are not test results.

| Role | Concern | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Document Engineering | Silent data loss | Acknowledgement and conflict clauses | Device failure before sync | Engineering lead |
| Publishing / Legal | Release without rights | Version-matched approval gates | Contract interpretation requires review | Publishing and Legal |
| Finance | Duplicate or partial settlement | Idempotency and linked entries | Provider guarantees unverified | Finance owner |
| QA | Verifiability | Atomic child IDs and explicit scenarios | Test coverage not yet implemented | QA lead |
