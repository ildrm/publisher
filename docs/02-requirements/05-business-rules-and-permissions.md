# REQ-05 — Business rules and permissions

Version 0.2 · 2026-10-29 · Status: Draft, not approved  
Authoring/accountable: Business Analyst · Consulted: Editorial, Security, Legal, Finance, Product · Reviewer: Solution Architect · Approver and decision owner: Publishing Director  
Assumptions: ASM-001–012; decisions DEC-001–010. Related requirements: FR-IAM-001–002, FR-DOC-001–003, FR-PUB-001–002, FR-RGT-001, FR-CAT-001, FR-COM-001, FR-FIN-001, FR-OPS-001. See [SRS](02-system-requirements-specification-srs.md) and planned publishing workflow (`../04-publishing-domain/01-editorial-publishing-workflow.md`).

## Invariants

| Rule | Testable policy and outcome |
|---|---|
| BR-001 | Content is private by default; public discovery receives only released listing data and authorized samples. An author can export without submitting. |
| BR-002 | Account, workspace and project membership do not transfer copyright. Each contract and grant is separately versioned, scoped by language, territory, format, channel and term, and subject to legal review. |
| BR-003 | A submission points to a frozen revision. Later edits do not silently alter that submission or its review; resubmission references a new revision. |
| BR-004 | Release requires matched, current approvals for the editorial decision, rights, metadata, rendition and proof; changed inputs invalidate the affected approval. Missing, expired or disputed rights hold release. |
| BR-005 | A published rendition is immutable or versioned; a correction creates an attributable new release. Takedown changes availability, preserves audit evidence and triggers a rights/support review. |
| BR-006 | A verified payment is not itself a royalty payout. Purchases, entitlements, refunds, earned royalties, payable balances and payouts have separate records and states. |
| BR-007 | A financial event is posted once using a unique source key; corrections use linked compensating entries. Balanced ledger records, not dashboard aggregates, are authoritative. |
| BR-008 | No model training or external AI use of private manuscripts by default. Any exceptional purpose requires a separate, specific, revocable permission and provider terms reviewed before use. Revocation cannot erase processing already completed; retention/deletion obligations must be specified. |
| BR-009 | Authorization is server-side, tenant-scoped, resource-scoped and checked at every read and mutation, including background jobs and downloads. Default deny; changing membership revokes future access. |
| BR-010 | An acknowledged save represents committed storage, not a local edit or queued request. Stale saves must not overwrite a newer revision. |

## Permission matrix

Legend: ✓ allowed within assigned scope; A = action requires explicit assignment or approval; — = denied by default. Authentication and resource scope are always required. A support role has no silent impersonation or routine manuscript access; exceptional access requires a recorded grant, reason, duration and audit, subject to policy. The owner can grant and revoke collaborators but cannot elevate an unrelated publisher/finance role.

| Action | Project owner | Assigned editor | Publisher/release manager | Production | Reader | Finance | Support/admin |
|---|---|---|---|---|---|---|---|
| Read private manuscript | ✓ | A, only assigned revision/project | A, only assigned scope | A, only needed artifact | — | — | A, exceptional grant |
| Edit project / restore revision | ✓ | A if edit grant | — | — | — | — | — |
| Invite/revoke project member | ✓ | — | — | — | — | — | A for account recovery with audit |
| Submit frozen revision | ✓ | — | — | — | — | — | — |
| Decide editorial review | — | A | ✓ | — | — | — | — |
| Record rights or approve release | View/author consent as applicable | — | A by delegated authority | — | — | — | — |
| Generate / approve proof | View and approve own proof | A | A | A | — | — | — |
| Purchase / read entitled rendition | As reader | As reader | As reader | As reader | ✓, only own entitlement | — | A for support, never bypass entitlement |
| Reconcile ledger / issue payout | View own statements | — | View scoped report | — | — | ✓, with separation-of-duties controls | — |
| Moderate / hold / reinstate | Request review | A | A | — | Report | — | A, scoped moderation |
| Configure access, recover backups | — | — | — | — | — | — | A, least privilege, audited |

Separation of duties: the person preparing a release, changing payout destination, or creating a payout should not alone approve that same operation. A small pilot lacking staffing must document a compensating review and Finance/Security acceptance before activation. Admin privileges are not an implicit grant to manuscript content. Public access serves only a released listing or explicitly approved sample.

### Role-by-action expansion

The following is a conceptual policy proposal, not evidence that every role exists in the pilot. `O` means own authorized project or purchase; `A` means explicitly assigned scope and any required grant; `P` means public listing/approved sample only; `E` means a valid purchased entitlement; `—` means denied by default. Purchase is separately available to an authenticated customer identity. “Approve” covers only a role's assigned task, never all release, rights or finance approvals. An assigned publisher admin still requires the distinct release/rights permissions and separation of duties. Support exception access is purpose-limited, time-bound and logged. Fresh reads/downloads must reauthorize; already obtained offline copies cannot be remotely erased.

| Role | View | Edit | Comment | Submit | Approve | Publish | Purchase | Download | Finance admin |
|---|---|---|---|---|---|---|---|---|---|
| Author / owner | O | O | O | O | O, own proof | — | O | O, project export | — |
| Coauthor | A | A | A | — | — | — | O | A | — |
| Invited editor | A | A | A | — | A, assigned review | — | O | A | — |
| Beta reader | A | — | A, if granted | — | — | — | O | A, if explicitly allowed | — |
| Production designer | A | A, production artifacts | A | — | A, production task | — | O | A | — |
| Publisher editor | A | A, editorial scope | A | — | A, editorial decision | — | O | A | — |
| Publisher admin | A | A, assigned scope | A | — | A, delegated release/rights | A | O | A | — |
| Finance | A, statements/ledger only | — | — | — | A, finance approval | — | O | A, finance records | A |
| Platform support | A, exceptional purpose-bound grant | — | — | — | — | — | O | A, exceptional grant | — |
| Public reader | P | — | — | — | — | — | — | P, if sample download allowed | — |
| Paying customer | P and E | — | — | — | — | — | O | E | — |

Owner and coauthor publishing rights do not arise from their project permissions. The platform must enforce the above at the resource level, not infer private access from a broad organization or administrator role. Any separately granted action must be recorded and expire or be revoked according to the approved policy.

## State transitions and controls

- **Submission:** draft → submitted → screening → in review → accepted / rejected / revise requested; a withdrawn submission closes the current review. Assignment and decision are role-gated, reasons and notifications are recorded; a resubmission is a new immutable revision reference. A rejection does not delete the author's project.
- **Edition:** preparation → proof pending → approved → scheduled → released → held / withdrawn. Release verifies matching approvals, current rights and approved artifacts atomically. A hold prevents future access according to entitlement/legal policy; existing customer remedies require legal review. Reinstatement requires rechecking rights and approvals.
- **Purchase:** pending → paid → entitled; payment failure → failed; refund requested → reviewed → refunded or denied; chargeback → disputed → resolved. Verify provider signature and status; reconcile ambiguous callbacks before recharging or revoking access. Refunds and chargebacks create compensating financial records.
- **Payout:** calculated → reviewed → eligible → initiated → paid / failed / disputed. Unique payout idempotency keys and reconciled provider status prevent accidental repeated payment. A failure keeps a traceable liability and produces an actionable queue item.

Every decision transition records actor, prior and next state, version, timestamp, reason and correlation ID; notify affected parties without disclosing private content in notification text. State changes and their durable event should commit together; retries are idempotent.

## References

Source: *Online Publishing Super Mega Documentation Prompt*, version 1.0, sections 0–3 and 5–7 (user-supplied); [scope and assumptions](../00-governance/01-scope-and-assumptions.md); [decisions and open questions](../00-governance/02-decisions-and-open-questions.md). Planned downstream artifacts are identified as planned in the text.

## Open questions and review

Legal and Finance must determine ownership evidence, contract language, retention and jurisdiction-specific refunds, tax, dispute, payout and hold rules before activation. Security must approve exceptional support access and role separation. See governance questions and risks; no legal approval is implied.

| Role | Concern | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Author / Security | Private access and support abuse | Default deny and scoped time-limited grants | Operational controls untested | Security owner |
| Legal / Editorial | Rights and release | Scoped grants and versioned approval | Legal interpretation and takedown remedies | Legal / Publishing |
| Finance | Double payment | Unique source keys, balanced entries, compensations | Partner behavior and segregation capacity | Finance owner |
