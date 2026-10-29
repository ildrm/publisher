# QA-02 — P0 functional, integration and E2E cases

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: QA Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: QA Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-IAM-001–002, FR-DOC-001–003, FR-IMP-001, FR-EXP-001, FR-PUB-001–002, FR-RGT-001, FR-FMT-001, FR-3D-001, FR-CAT-001, FR-COM-001, FR-FIN-001, FR-OPS-001.

## Case convention

Each row defines three proposed cases: `TC-<FR-ID>-P` positive, `-N` negative and `-R` boundary/race/network. P0 is the priority for each row except optional P1 FR-3D-001. The accessible 2D baseline is FR-CAT-001.2; FR-3D-001 remains optional P1. Execute tests at the layer shown and capture fixture, build, steps, expected/actual, screenshots/log correlation and defect reference. No case has been executed. Fixtures use two isolated tenants, synthetic roles and synthetic text unless stated otherwise.

| Requirement / layer | P — positive expected result | N — negative expected result | R — boundary/race expected result |
|---|---|---|---|
| FR-IAM-001 / API+browser | Verified user signs in and enters own workspace. | Wrong credentials cannot enter; privileged user without MFA denied. | Expired session during save prompts reauthentication without false acknowledgement. |
| FR-IAM-002 / API+integration | Assigned editor accesses granted revision. | Tenant B and unassigned user receive denial without content. | Revoke while request/job is in flight; recheck before commit/download and deny. |
| FR-DOC-001 / browser+domain | Create project with two ordered semantic chapters; reload preserves order. | Viewer cannot create or edit. | Concurrent reorder with stale version is rejected, not silently overwritten. |
| FR-DOC-002 / integration+browser | Edit then durable commit returns revision and Saved. | Failed commit shows unsaved; if local recovery is confirmed, offer it, and if unavailable show the risk and offer immediate copy/export where possible. | Commit then lose response; query operation key, reconcile once; stale write rejected with manual recovery. |
| FR-DOC-003 / API+browser | Restore snapshot creates new revision, retaining prior one. | Viewer cannot restore. | Current version changes before confirm; reject stale restore and preserve both. |
| FR-IMP-001 / worker+browser | Valid DOCX/Markdown yields reviewed report and confirmed project. | Corrupt, executable or archive-bomb upload rejected/quarantined. | Timeout after conversion retains original upload and source; retry creates no duplicate project. |
| FR-EXP-001 / worker+browser | Unpublished author exports content and metadata successfully. | Unassigned user cannot download private artifact. | Worker dies before finalization; retry preserves source and emits one finalized artifact. |
| FR-PUB-001 / API+browser | Author submits a frozen revision and authorized editor sees it. | Unassigned editor cannot decide. | Author edits after submission; review still references original revision. |
| FR-PUB-002 / integration+browser | Authorized publisher releases exact approved artifacts with valid grants. | Missing rights, proof or approval blocks release. | Artifact changes between approval and release; recheck rejects stale approval atomically. |
| FR-RGT-001 / domain+API | Active grant covers matching territory, format, channel and term. | Missing or expired grant blocks that scope. | Grant expires or is disputed immediately before release; release rechecks and holds. |
| FR-FMT-001 / worker+integration | Fixed inputs produce versioned rendition with validation report. | Invalid EPUB or unapproved proof cannot release. | Worker retry or crash cannot replace good artifact and records single final output. |
| FR-3D-001 / browser, P1 optional | Enabled 3D displays geometry using verified inputs and identifies dimensions. | Missing or unsafe texture never removes accessible 2D fallback. | Estimated dimensions are visibly labeled; reduced-motion and low-power operation preserve the accessible 2D baseline. |
| FR-CAT-001 / search+integration+browser | Released title and approved sample appear publicly with keyboard-accessible 2D cover and text equivalent (FR-CAT-001.2). | Private draft and unapproved samples are absent; 3D failure never hides 2D. | Revoke/unpublish while index updates; serving path denies stale listing and index reconciles. |
| FR-COM-001 / API+integration | Signed successful payment creates one purchase and entitlement. | Invalid signature or unconfirmed payment grants none. | Duplicate/out-of-order callback and response timeout are reconciled without second charge or entitlement. |
| FR-FIN-001 / domain+integration | Sale, royalty and refund produce attributable balanced postings. | Payout above cleared payable or unauthorized posting is rejected. | Replay event and ambiguous payout response produce no double posting/disbursement; reconcile first. |
| FR-OPS-001 / integration+DR | Authorized audit entry includes actor/time/outcome; restore verifies committed data. | Private text is absent from logs; unauthorized audit alteration denied. | Crash during backup/restore tests acknowledged-save guarantee and reconciliation without false success. |

## Repeatable fixture and execution protocol

Use tenant A author `A1`, tenant B author `B1`, assigned editor `E1`, a revoked editor `E2`, purchaser `C1` and finance reviewer `F1`; these are synthetic role labels, not real accounts. Create project `P-A` with two ordered chapters, one mixed Persian/English paragraph containing an IME-composed character and a unique private canary, then record revision `v1`. For race cases send two writes based on `v1`; permit exactly one commit, reject the stale write, and show a recovery path without claiming device persistence until confirmed. For FR-CAT-001.2 navigate SCR-026 with keyboard and screen reader with WebGL disabled; verify the 2D cover text equivalent and price remain available. For commerce use synthetic sale event `sale-1`, duplicate `sale-1`, `refund-1` and payout request greater than cleared balance; assert one effect per unique source, balanced entries and denied overpayment. Reset fixtures between cases and retain only privacy-safe logs.

A case is **pass** only when the observable result matches its criterion in the named build and environment; otherwise record defect, severity and owner. Record skipped cases and unresolved dependencies separately. Browser, API and worker tests need distinct evidence; one passing layer does not prove the others. This is an unexecuted test specification.

## Exploratory user acceptance charters

An author drafts 50k words, disconnects and reconnects; record every acknowledged version. Recover unsynced content only where a local recovery copy is verified; separately test unavailable or denied local storage, a visible unsaved warning, and an immediate copy/export option where possible. A coauthor simulation attempts concurrent same-paragraph writes and access revocation; no realtime collaboration is promised, stale saves must fail. Paste DOCX with footnotes, tables and mixed Persian/English; inspect semantic warnings and exports. Publish only after rights/proof checks, then purchase, refund and reconcile royalty. Keyboard and screen-reader users complete author and reader flows; low-power devices retain 2D preview. Capture observed barriers without claiming conformance.

## Open questions and references

Which reference devices, exact fixture limits, provider sandbox behaviors and UAT participants will be selected? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| QA Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
