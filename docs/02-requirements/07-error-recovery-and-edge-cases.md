# REC-001 — Error recovery and edge cases

Version 0.2 · 2026-10-29 · Status: Draft; runbooks and recovery objectives require testing  
Authoring/accountable: Support Lead · Consulted: Document Engineering, Editorial, Finance, Security, QA, Accessibility · Reviewer: SRE Lead · Approver and decision owner: Product Owner  
Assumptions: ASM-001–012; decisions DEC-001–010. Related requirements: FR-DOC-002–003, FR-IMP-001, FR-EXP-001, FR-PUB-001–002, FR-RGT-001, FR-FMT-001, FR-COM-001, FR-FIN-001, FR-OPS-001; NFR-REL-001–004. See [business rules](05-business-rules-and-permissions.md), [SRS](02-system-requirements-specification-srs.md), and planned support runbooks (`../08-operations/05-data-retention-and-customer-support-runbooks.md`).

## Recovery contract

Every failure must preserve the last committed source, expose the affected operation and safe next step to the authorized user, and create a privacy-safe correlation ID for support. Status must distinguish pending, failed, succeeded and uncertain; never display success until the durable outcome is known. Retry only idempotent operations or reconcile first. Announce errors to assistive technology, preserve keyboard focus and do not rely on color. Notification copy must not include manuscript or financial details. Retention of local recovery data is subject to device and approved privacy policy; it is not a substitute for a committed save.

| Trigger and detection | Immediate user-facing response | System action and safe recovery | Owner / escalation |
|---|---|---|---|
| Connectivity lost before save acknowledgement | “Not saved. Retry when connected.” Confirm a local recovery copy only after verifying it exists. | Preserve recoverable local copy where available; retry with version and idempotency key; do not claim server durability. If device storage unavailable, offer immediate local export/copy where possible. | Document Engineering; unresolved loss to incident lead |
| Two sessions submit from same revision | “A newer version exists. Compare versions before saving.” | Reject stale write; retain both the accepted revision and local recovery copy. Let the author manually compare, export or deliberately create a new revision; no automatic merge or silent overwrite. | Document Engineering |
| Save committed but response lost | “Checking save status…” | Query by operation key/version. A matching commit becomes acknowledged; unknown result remains unsaved until reconciled. Retry must not create duplicate mutations. | Document Engineering / SRE |
| Restore requested while current revision changes | “This manuscript changed. Review the current version before restoring.” | Reject stale restore; keep both snapshots; confirm again with current version. A successful restore is a new revision. | Document Engineering |
| Import unsupported, corrupt, infected, oversized or contains lossy elements | “Import could not complete” or “Review changes before importing,” with safe issue list. | Quarantine or reject unsafe file; conversion runs isolated. Keep source untouched; offer a supported format or a downloadable report; never execute embedded content. | Conversion / Security |
| Export worker times out or validation fails | “Export failed. Your manuscript is safe. Review the report or retry.” | Keep original revision and job provenance; isolate worker, record warnings, retry only safe transient faults; release cannot use failed artifact. | Conversion / Production |
| EPUB has invalid structure or inaccessible reading order | “This file needs fixes before release.” | Preserve validator report, reject release, assign production task and rerun checks after remediation; manual assistive-tech review remains necessary. | Production / Accessibility |
| Print proof has wrong margins, spine, bleed or color | “Proof approval is on hold.” | Compare exact profile, assets and physical sample with printer specification. Invalidate proof approval and produce a new version; do not ship from preview alone. | Print Production / Editorial |
| Submission rejected or revision requested | Show decision, actionable reason where policy permits, and next steps. | Keep original project and frozen submission. Allow new submission referencing a new revision; no silent publication. | Editorial / Support |
| Rights absent, expired, disputed or contract changed | “Release is on hold while rights are reviewed.” | Block publication for affected scope; preserve agreement and evidence; route to legal/rights owner; recheck after resolution. | Rights / Legal |
| Metadata or rendition changes after approval | “Approval needs to be renewed for this version.” | Invalidate affected approval and prevent release until the correct version is reviewed. | Publishing / Production |
| Duplicate or delayed payment callback | “Payment is being confirmed. Do not pay again yet.” | Verify signature; deduplicate by provider event and business key; reconcile uncertain status before another charge; issue entitlement only on confirmed payment. | Commerce / Finance |
| Payment dispute, refund or chargeback | Show case status and support contact; do not promise outcome before review. | Preserve original sale, evidence and entitlement history; apply authorized reversal as linked balancing entries and follow applicable customer remedy policy. | Finance / Support / Legal |
| Payout fails, times out or provider response is ambiguous | “Payout pending review” with case reference. | Retain payable liability; reconcile provider status and destination before retry; use same idempotency key; route unresolved cases for manual review. | Finance |
| Access revoked during upload, job or open session | “Access changed. Contact the project owner.” | Recheck authorization before commit and artifact download, stop or quarantine in-flight work, avoid disclosure; preserve author's committed work. | Identity / Security |
| Backup restore fails or inconsistency found | Notify incident team and publish appropriate status. | Stop conflicting writes, restore to isolated environment, reconcile document versions, purchases and ledger; record data gap and notify affected users according to policy. | SRE incident commander / Finance |
| Optional 3D unsupported, reduced motion requested or dimension assumptions missing | Show the accessible baseline 2D cover and text equivalent. | Disable animation or 3D when appropriate; any enabled mockup requires accurate inputs or clearly labeled estimates and is not a manufacturing proof. | Frontend / Production |

## Escalation and verification

Support records symptom, operation ID, time, affected resource and permission scope, without requesting manuscript content or card credentials. Security and privacy incidents follow the incident process; financial uncertainty goes to Finance before retry; rights issues go to Legal/Publishing; no support agent unilaterally edits the ledger or bypasses access checks. QA must exercise each row with a reproducible fixture, owner, evidence and the expected user message. Particularly test power loss, stale version races, authorization revocation during a job, duplicated/out-of-order provider events, partial rollback and restore from isolated backups. The existence of this catalog is not evidence those tests passed.

## References

Source: *Online Publishing Super Mega Documentation Prompt*, version 1.0, sections 0–3 and 5–7 (user-supplied); [scope and assumptions](../00-governance/01-scope-and-assumptions.md); [decisions and open questions](../00-governance/02-decisions-and-open-questions.md). Planned downstream artifacts are identified as planned in the text.

## Open questions and review

Device-storage behavior, provider reconciliation windows, notification channels, legal hold and retention, refund policy and printer-specific proof tolerances need owner decisions and pilot tests. Assign due milestones through governance before dependent launch.

| Role | Concern | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Author / Document Engineering | Unsynced changes may be lost | Explicit status, local recovery and conflict flow | Local storage may be unavailable | Product / Engineering |
| Production | Preview mistaken for proof | Proof hold and verified printer preset | Physical testing not performed | Production owner |
| Finance | Ambiguous payments or payouts | Reconcile before retry; compensating entries | Provider behavior unverified | Finance owner |
| Support / Security | Excessive access while diagnosing | Correlation IDs and scoped escalation | Operational readiness untested | Support / Security |
