# UX-005 — Interaction and content guidelines

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft, no human approval.
- **Authoring/accountable:** Content Design Lead; **consulted:** Product, Frontend, Accessibility, Research, QA; **reviewer:** Accessibility lead; **approver/decision owner:** Product Owner. Roles are proposed.
- **Assumptions:** ASM-001–012, text-centric pilot with 2D baseline; **related requirements:** FR-DOC-002, FR-IMP-001, FR-PUB-001, FR-COM-001.
- **Unresolved:** OQ-002, OQ-007, OQ-010; Product and Accessibility owners resolve at prototype and pilot gates.
- **References:** [scope](../00-governance/01-scope-and-assumptions.md), [screen contracts](03-screen-inventory-and-screen-specs.md), [NFRs](../02-requirements/06-nonfunctional-requirements-and-slos.md), user-supplied prompt v1.0 §8.

## Interaction rules

Keep a single clear primary action, preserve context on navigation, and distinguish confirmation from irreversible completion. User-facing statuses must reflect server state, not a local optimistic assumption. Announce nonurgent status politely; errors require a summary and field-level instructions. Use progressive disclosure for complex rights and formats while keeping material consequences visible before confirmation. Avoid timed messages as the only location for an error. Do not auto-submit, auto-publish, or use dark patterns to pressure writers into publication.

| Situation | Proposed copy | Required control |
|---|---|---|
| Pending save | “Saving changes…” | Announce status; do not label as saved. |
| Acknowledged | “Saved” | Only after durable acknowledgement identifying revision. |
| Conflict | “A newer version exists. Review your unsaved changes before retrying.” | Preserve unsynced content where supported and present recovery. |
| Import loss | “Some formatting could not be imported. Review the report before continuing.” | Offer report, cancel and explicit confirmation. |
| Missing rights | “Release blocked: rights are missing for this format or territory.” | Point authorized user to rights record. |
| Payment uncertain | “Payment is being confirmed. Do not pay again yet.” | Reconcile before retry. |

Write in plain sentences, use sentence case, label a button with the action and object, and name the impact of destructive actions. Avoid placeholders as the sole field label, legal certainty without counsel, unexplained acronyms, guilt-inducing streaks and manuscript excerpts in notifications. Provide localizable messages with plural and grammatical context; never concatenate a sentence around a translated word.

## Cross-role review checkpoint

| Role | Concern / draft response | Residual risk | Required approval |
|---|---|---|---|
| UX / Accessibility | Status and errors must be understandable | Copy and assistive technology review outstanding | Product / Accessibility |
