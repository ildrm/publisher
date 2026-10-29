# UX-002 — Navigation and journey flows

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft — not reviewed or approved.
- **Authoring/accountable:** Service Designer; **consulted:** Product, Editorial, Accessibility, Document Engineering; **reviewer:** QA lead; **approver:** Product Owner; **decision owner:** Product Owner. These are proposed roles; no human approval is implied.
- **Assumptions:** ASM-001–012; single imprint, text-centric curated pilot, accessible 2D baseline, optional later 3D. **Related requirements:** FR-DOC-002, FR-EXP-001, FR-PUB-001, FR-PUB-002, FR-COM-001.
- **Unresolved:** OQ-001, OQ-002, OQ-007 and OQ-010; Product and domain owners resolve before relevant pilot or procurement gate.
- **References:** [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [feature catalog](../02-requirements/03-feature-catalog-and-prioritization.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md), and the user-supplied master prompt v1.0 §8.

## Author and publication journey

1. A new author signs in, creates a project and chapter, types, sees pending then acknowledged save, and can export without submitting. A failure preserves visible pending state and offers recovery.
2. A migrating author imports into a preview, reviews warnings and confirms or cancels; the source file is not silently replaced. The system handles unsupported content as an explicit warning, not success.
3. An author chooses a frozen revision for consideration, reviews declarations and submits. Editorial can accept, reject or request revision. A rejection never removes author access to the project.
4. The publisher records rights and metadata, produces and reviews a versioned rendition, obtains approvals and checks release hold before creating a listing. Readers purchase in eligible territory and receive an entitlement only after verified payment.
5. Finance reviews settlement, refunds and royalties before payout; support uses a scoped case and must not bypass authorization.

See [journey diagram](../diagrams/ux-author-journey.mmd), source not render-validated. For state transitions see [editorial workflow](../04-publishing-domain/01-editorial-publishing-workflow.md). Project navigation retains current chapter and scroll position on return; use focus on the new page heading after a full navigation, preserve focus on inline updates, and announce asynchronous completion using appropriate status semantics.

## Recovery patterns

| Trigger | Action and user message | Resolution and ownership |
|---|---|---|
| Save timeout or network loss | “Changes not saved. Keep this page open and retry.” Preserve unsent text where supported. | Document engineer defines durable local recovery; never promise survival of an unsaved browser buffer. |
| Stale revision | “A newer version exists. Review your unsaved changes before retrying.” | Reject stale request; retain unsynced content and allow explicit recovery; no automatic overwrite. |
| Import invalid/unsafe | “This file could not be imported. Check its format and try again.” | Isolated worker reports safe actionable details; retain source under policy. |
| Rights missing | “Release blocked: rights are not recorded for this format or territory.” | Authorized rights officer resolves; public index remains unchanged. |
| Payment uncertain | “Payment is being confirmed. Do not pay again yet.” | Reconcile provider state; never initiate second capture on uncertainty. |
| Proof or export failed | “The file is not ready. Review the report and retry.” | Preserve approved artifact; production checks inputs and logs. |

Telemetry records scoped IDs, outcome and duration, never manuscript contents or payment secrets. Each transition needs current server permission, idempotency for retried commands and an audit event when required; the UI cannot grant rights.

## Cross-role review checkpoint

| Role | Concern / draft response | Residual risk | Required approval |
|---|---|---|---|
| UX / Document Engineering | Recovery and permission paths need clear navigation | No usability testing or storage proof | Product / Document Engineering |
