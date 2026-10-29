# PUB-001 — Editorial publishing workflow

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft, not reviewed or approved.
- **Authoring/accountable:** Editorial and Publishing Operations Lead; **consulted:** Product, Print, Legal, Finance, Accessibility, QA; **reviewer:** QA Lead; **approver:** Publishing Director; **decision owner:** Editorial and Publishing Operations Lead. Roles are proposed, not evidence of human review.
- **Assumptions:** ASM-001–012; text-centric curated pilot and scoped rights. **Related requirements:** FR-PUB-001–002, FR-RGT-001, FR-FMT-001.
- **Unresolved:** OQ-001, OQ-003–007, OQ-009–010; assigned governance owners resolve before contract, vendor, proof and release milestones.
- **References:** [scope](../00-governance/01-scope-and-assumptions.md), [decision register](../00-governance/02-decisions-and-open-questions.md), [business rules](../02-requirements/05-business-rules-and-permissions.md), user-supplied prompt v1.0 §§3, 5, 11–15.

## Acquisition and production

A submitting author selects a saved, immutable source revision and declares eligibility and permissions; submission does not transfer copyright. Intake validates structure and declarations, then an authorized editor accepts the work for review or asks for corrections. Screening results are risk signals, not automated plagiarism findings; human review and an appeal channel are required. Editorial assigns a reviewer, records a reasoned decision and tells the author. A rejected or withdrawn submission leaves the private project and export intact. A revise request is answered by a new submission tied to a new revision; the old submission remains historical.

After acceptance, editorial assigns editing and production work, records contributor and grant evidence, prepares metadata, produces rendition(s) from frozen inputs and obtains appropriate author, editorial, rights, metadata and proof approvals. Before release, the publisher checks all approvals are current for exact artifacts and rights cover language, territory, format, channel and effective time. A hold or unresolved dispute blocks release. Scheduler rechecks at execution, not just at scheduling; status and authorized public index change via a reliable event. Corrections create a traceable release/version; takedown restricts availability and triggers support/legal review without destroying financial or audit records.

## Transition contract

Every transition is authorized, checks expected version, persists actor/reason/time and writes an event atomically. Notifications contain status and safe links, not private manuscript or contract text. Repeated commands use an idempotency key; failure leaves prior state and queues reconciliation. An approval is invalidated when its relevant source, grant, metadata, preset or artifact changes.

| Object | From → to | Actor / guard | Failure or compensation |
|---|---|---|---|
| Submission | draft → submitted → screening → in review | Owner submits revision and declarations; assigned editor screens | Missing fields block; retry cannot create duplicate. |
| Submission | in review → accepted / rejected / revise requested | Authorized editor records reason; author notified | No implicit publication rights; appeal via support. |
| Submission | submitted/screening/in review → withdrawn | Owner or authorized publisher with reason | Close assignments; preserve audit and author project. |
| Editorial task | open → assigned → in progress → completed | Editorial manager assigns scope; assignee completes checklist | Reassign or cancel with reason; do not imply release approval. |
| Edition | preparation → proof pending → approved → scheduled → released | Production prepares; delegated approvers sign exact versions; publisher rechecks rights and holds | Missing/stale approval or grant blocks release; failed output cannot replace approved file. |
| Edition | preparation/proof pending/approved/scheduled → held; released → held/withdrawn | Scoped publisher or trust officer records reason | Suspend affected availability; customer remedy/entitlement treatment requires legal policy. |
| Edition | held → preparation / proof pending / approved | Authorized reviewer clears hold after checking the reason and version-matched evidence; return to the earliest unmet gate. | Otherwise remain held; no automatic republication. |
| Edition | held → scheduled | Authorized publisher clears hold only when all current approval, rights and timing gates pass; scheduler rechecks at execution. | Otherwise remain held; public index and distribution reconcile. |
| Conversion job | queued → running → succeeded / failed; failed → queued | Worker validates inputs and idempotency; bounded retries | Dead-letter and actionable error; keep previous artifact. |

[Editorial activity source](../diagrams/pub-editorial-activity.mmd) illustrates this workflow; source is not render-validated. No decision or proof has actually been approved.

## Cross-role checkpoint

| Role / concern | Response | Residual risk / required approver |
|---|---|---|
| Author / Editorial | Review must not transfer ownership | Frozen submissions, separate grants, author notifications | Counsel and Editorial lead |
| Print / Accessibility | Proofs may conceal defects | Version-bound validation and human proof | Print and Accessibility leads |
| Finance / Security | Release after rights expiry or stale approval | Recheck at execution, audit and hold | Finance, Legal and Security owners |

## Additional legal-transition rules

An editorial task may be cancelled from open, assigned or in progress by its manager with a reason; completion cannot approve a release by itself. A failed conversion retry reuses the operation key for the same input and is bounded; altered inputs create a new job/version. A scheduled release cannot skip the execution-time rights, embargo, approval and hold checks. A withdrawn edition requires a documented new release/reinstatement decision rather than an unguarded state reset. An expired or revoked grant does not automatically terminate already licensed customer access; Finance and Legal decide contractual remedies. Invalid transitions are rejected with unchanged prior state and an audit event; an event-delivery failure after commit enters outbox reconciliation rather than rolling back the already committed state.
