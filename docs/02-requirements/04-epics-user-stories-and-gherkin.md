# REQ-04 — Epics, user stories and acceptance scenarios

- Version/date: 0.2 / 2026-10-29; status: **DRAFT — partial**, not approved.
- Accountable: Requirements Engineer. Consulting: authoring, editorial, legal, finance, accessibility and QA leads. Reviewer: QA lead. Approver/decision owner: Product Owner; actual approval outstanding.
- Assumptions: [governance](../00-governance/01-scope-and-assumptions.md); all thresholds and market-specific policies require approval. Related: [feature catalog](03-feature-catalog-and-prioritization.md), [SRS](02-system-requirements-specification-srs.md), [rules](05-business-rules-and-permissions.md).
- Unresolved: approved revision-retention period, idempotency window, proof acceptance, refund policy and supported markets. References: supplied master prompt; source-linked discovery documents. Scenarios are proposed, not executed tests.

These scenarios define observable behavior for selected high-risk requirements. They do not replace the full P0/P1 test catalog, schema contracts, screen specifications, or real accessibility and production proof testing. Automated test locations are proposed test layers, not existing files.

## Contents

- [EP-01: Trustworthy authoring](#ep-01-trustworthy-authoring)
- [EP-02: Editorial control and rights](#ep-02-editorial-control-and-rights)
- [EP-03: Purchase and finance](#ep-03-purchase-and-finance)
- [EP-04: Privacy and accessible discovery](#ep-04-privacy-and-accessible-discovery)
- [Cross-role review checkpoint](#cross-role-review-checkpoint)

## EP-01: Trustworthy authoring

**US-01 / FR-DOC-002 — Acknowledged save.** As an author I need to distinguish local changes from a saved revision so that a network failure cannot falsely reassure me. Preconditions: authenticated writer, existing project and expected revision. Entry: editor. Expected event: save outcome and latency without manuscript text. Proposed layers: domain concurrency tests, API integration, browser network E2E.

- **AC-01 positive:** Given an authorized writer and a valid base revision, when a change is committed durably, then the editor shows “Saved” only after the server returns the committed revision identifier.
- **AC-02 network:** Given an edit not yet acknowledged, when connectivity fails, then the editor shows “Changes not saved” and preserves recoverable local changes where supported; it never marks the edit saved without a server acknowledgement.
- **AC-03 race:** Given two requests based on the same revision, when the first commits and the second is stale, then the server rejects the second as stale, the author is shown a manual recovery path, and the committed content is not silently overwritten.
- **AC-04 access:** Given a writer whose access is revoked, when the writer next attempts a save, then the server refuses it and the UI explains that access has changed without exposing protected content.

Manual check: type an identifiable passage, observe the acknowledgement, interrupt connectivity, type a second passage and reconnect; verify the first survives and the second is never falsely labeled saved. Include keyboard and screen-reader announcement of save state. Test data: mixed RTL/LTR text, emoji, IME composition and long manuscript. No-loss claims require validated storage architecture, not this scenario alone.

**US-02 / FR-DOC-003 — Restore.** As an owner I need to restore an earlier revision without destroying later history. Proposed layers: domain and API integration; browser E2E.

- Given a readable prior snapshot, when I restore it with current-version confirmation, then a new current revision is created and the original and previously current revisions remain accessible per retention policy.
- Given an unauthorized user, when they request a restore, then the request fails and no revision changes.
- Given the current revision changes between selection and confirmation, when I confirm the restore, then the server detects the conflict and asks me to review the newer version.

**US-03 / FR-EXP-001 — Portability.** As an author I can obtain my manuscript and relevant metadata even if I never submit or publish it. Proposed layers: job integration and fidelity tests, browser E2E.

- Given an unpublished project I own, when I request an available portable format, then I receive a downloadable artifact and a clear report of transformations or unsupported features.
- Given another user's private project, when I request export without a grant, then the server denies the request and issues no usable download URL.
- Given a conversion fails or is retried, when the job terminates, then the previous good artifact remains unchanged and I can see an actionable failure and retry option.

## EP-02: Editorial control and rights

**US-04 / FR-PUB-001 — Submit a frozen revision.** As an author I want a tracked submission so that I can understand its editorial status. Proposed layers: workflow unit/API and browser E2E.

- Given a complete eligible submission, when the owner submits, then the system records the exact revision, declarations and timestamp and displays the submitted status.
- Given a required declaration is missing, when the owner submits, then submission is blocked with a field-specific correction and no editorial decision is created.
- Given a network retry of the same submission request, when the server receives it again with the same idempotency key, then one submission exists and the same outcome is returned.

**US-05 / FR-RGT-001 and FR-PUB-002 — Release with approvals.** As a publisher I need valid scoped rights and approvals before a listing is released. Proposed layers: domain transition tests, authorization API, editorial UAT.

- Given a frozen rendition, verified scoped rights, completed required approvals and no hold, when an authorized publisher releases it, then a public listing can reference that approved edition and the action is audited.
- Given rights are absent, expired, disputed or exclude a proposed territory or format, when release is attempted, then release is blocked with the reason and no public listing for that scope is created.
- Given a release hold is applied while approval is underway, when release is attempted, then the hold wins and the transition is rejected; clearing the hold requires authorized action and audit.

**US-06 / FR-FMT-001 — Reproducible rendition.** As production staff I need a traceable artifact so that the approved file matches its source and settings. Proposed layers: worker integration, validator and human proof tests.

- Given a frozen source revision, assets, converter version and preset, when conversion succeeds, then the artifact records those inputs and a checksum; warnings are presented for human review.
- Given malformed or unsafe input, when the isolated worker processes it, then the job fails safely and reports a useful error without executing embedded content or replacing an approved artifact.
- Given two deliveries of the same job command, when both are processed, then the idempotency policy prevents duplicate approval or replacement; logs identify the job and attempts.

## EP-03: Purchase and finance

**US-07 / FR-COM-001 — Purchase and entitlement.** As a reader I want access after confirmed payment without duplicate charges. Proposed layers: payment-adapter contract and integration, webhook replay, browser E2E.

- Given a purchasable edition for the customer's territory, when verified payment succeeds, then exactly one order reaches the confirmed state and an entitlement is granted for that edition.
- Given a failed or unverified payment, when the provider returns or sends a webhook, then the system does not grant paid access and displays a recoverable status.
- Given a delayed duplicate webhook or checkout retry, when processed, then idempotency and reconciliation produce at most one capture and one entitlement; conflicting provider state is escalated.

**US-08 / FR-FIN-001 — Refund and payout.** As finance staff I need an auditable ledger that reconciles sales, refunds and payouts. Proposed layers: ledger property tests, provider integration, reconciliation/UAT.

- Given a settled eligible sale and a configured royalty rule, when the sale is posted, then balanced ledger entries identify the source and beneficiary and the statement reconciles to the posting.
- Given the same refund notification arrives twice, when it is processed, then one compensating financial effect is posted and the reconciliation identifies the original sale.
- Given a requested payout exceeds cleared payable balance or rights are disputed, when payout is attempted, then it is blocked or held under approved policy and the reason is audited.

## EP-04: Privacy and accessible discovery

**US-11 / FR-IAM-001 — Sign-in and recovery.** Test data: verified author, unverified author, privileged administrator, expired recovery token. Test layers: identity adapter integration and browser E2E.

- Given a verified author with valid credentials, when sign-in succeeds, then an authenticated session opens that author's workspace.
- Given an expired recovery token or invalid credential, when recovery or sign-in is attempted, then access is denied with safe actionable feedback and no credential is disclosed.
- Given a privileged user, when sign-in requires a second factor and the challenge expires or fails, then no privileged session is issued; retry is rate limited and auditable.

**US-12 / FR-IAM-002 — Project membership.** Test data: owner, granted editor, revoked editor and unrelated tenant. Test layers: authorization API and browser E2E.

- Given a project owner, when a valid scoped invitation is accepted, then the collaborator can perform only the granted actions.
- Given a non-owner or unrelated tenant, when they attempt to grant access, then the request is denied and no membership changes.
- Given a revoked collaborator and a previously open editor, when a fresh read or write arrives, then authorization fails even if the UI has stale cached state.

**US-13 / FR-DOC-001 — Structured project and chapter.** Test data: empty project, multilingual chapter with headings, unrelated tenant. Test layers: domain/API and keyboard browser E2E.

- Given a signed-in author, when a project and chapter are created with supported semantic text, then their ordered structure can be reopened without publishing.
- Given an unauthorized user or invalid project title, when creation is requested, then it is denied or field validation explains the correction; no partial unauthorized record appears.
- Given a chapter reorder with a stale project version, when another reorder has already committed, then the stale request is rejected and the accepted ordering is retained.

**US-14 / FR-IMP-001 — Safe import.** Test data: valid DOCX, Markdown with unsupported syntax, oversized or malicious archive. Test layers: isolated worker integration, security and browser E2E.

- Given a supported DOCX or Markdown file, when an owner imports it, then recognized chapters and semantics appear in a reviewable project with a transformation report.
- Given a malicious, invalid or oversized file, when it is uploaded, then processing is rejected safely with an actionable error, and no source revision is changed.
- Given a network retry or worker restart during import, when the job resumes, then it has one traceable outcome, retains the source under policy and never silently creates duplicate projects.

**US-15 / FR-OPS-001 — Restore and audit.** Test data: synthetic manuscript and ledger canaries, backup, unauthorized support account. Test layers: disaster-recovery exercise, security integration and audit review.

- Given a tested backup and durable journal, when an authorized operator performs a recovery exercise, then acknowledged revisions and ledger records reconcile and the exercise records elapsed time and evidence.
- Given an unauthorized support account, when it requests private content or backup access, then the request fails and a privacy-aware audit event is recorded.
- Given failure immediately after a save acknowledgement or during restore, when recovery completes, then the acknowledged revision is present or launch is blocked as an integrity failure; incomplete restore is not represented as successful.

**US-09 / FR-IAM-002 and FR-CAT-001 — Private/public boundary.** As an author I need unpublished text excluded from public discovery. Proposed layers: authorization integration, search indexing and E2E.

- Given a private draft containing a unique phrase, when a public user searches the catalog, then no draft or unauthorized sample appears.
- Given an approved public sample, when the listing is published, then only the approved sample and public metadata are indexed.
- Given collaborator access is revoked, when a fresh read or write is requested, then the server denies access regardless of cached UI state; cached or offline copies require a separate policy and cannot be remotely guaranteed erased.
- Given an available listing and a cover with an approved text equivalent, when a reader opens the detail page using keyboard or a screen reader, then the 2D cover and text equivalent are available without WebGL or animation.

**US-10 / FR-3D-001 — Accessible preview.** As a reader I need an honest and operable representation of a book. Proposed layers: browser accessibility/visual tests and device testing.

- Given known trim, page count and paper assumptions, when the preview is rendered, then the UI identifies the basis and distinguishes it from a manufacturing proof.
- Given WebGL is unavailable or reduced motion is selected, when I open the preview, then an accessible 2D cover and textual description are available without animation.
- Given missing geometry inputs, when preview is requested, then the system labels the rendering illustrative or falls back instead of asserting physical accuracy.

## Cross-role review checkpoint

| Role | Concern / change | Residual risk / stakeholder approval |
|---|---|---|
| Authoring and accessibility | Explicit acknowledgement and network/revocation scenarios added. | Storage semantics, local recovery and assistive technology require real tests. |
| Editorial and legal | Release requires scoped rights and human approval. | Counsel and editorial lead must approve rights and exception policies. |
| Finance | Duplicate delivery, refund and balance controls specified. | Accountants and processor integrations must validate reconciliation. |
| QA | Scenarios are observable and identify test layers. | Coverage is partial; all P0s need negative and boundary cases and test data. |

These cases now cover the core P0 candidate IDs at scenario level; formal executable test evidence, exact retry windows and user-facing error copy remain pending. Other decomposed high-risk features require their own concrete scenarios before inclusion in a release.
