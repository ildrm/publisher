# UX-007 — Wireframes and prototype checklist

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft, no human approval.
- **Authoring/accountable:** UX Research / Design Lead; **consulted:** Product, Frontend, Accessibility, Research, QA; **reviewer:** Accessibility lead; **approver/decision owner:** Product Owner. Roles are proposed.
- **Assumptions:** ASM-001–012, text-centric pilot with 2D baseline; **related requirements:** FR-DOC-002, FR-EXP-001, FR-PUB-002, FR-COM-001.
- **Unresolved:** OQ-002, OQ-007, OQ-010; Product and Accessibility owners resolve at prototype and pilot gates.
- **References:** [scope](../00-governance/01-scope-and-assumptions.md), [screen contracts](03-screen-inventory-and-screen-specs.md), [NFRs](../02-requirements/06-nonfunctional-requirements-and-slos.md), user-supplied prompt v1.0 §8.

## Low-fidelity content structure

These are text descriptions, not a created Figma prototype. Screen IDs and full contracts are in [screen inventory](03-screen-inventory-and-screen-specs.md).

- **SCR-007 editor:** top bar = project title, save status, history and export; left = ordered chapters; center = semantic manuscript editor; contextual panel = selected node actions. Compact view exposes one panel at a time. Keyboard focus travels skip link → navigation → chapter list → editor → contextual actions.
- **SCR-012 transfer:** heading and source revision → import section with type/size rules → warnings and confirmation → export format → job progress/report. Clearly distinguish imported preview from confirmed new revision.
- **SCR-023 release:** heading and edition identity → rights scope → approvals and artifact versions → blocking holds → “Schedule release” control. Failed or stale checks appear before action; an authorized confirmation states territory and effective date.
- **SCR-027 checkout:** order and item → price/tax disclosure → provider payment control → status. If outcome is unknown, display pending and reconciliation instruction, never invite a duplicate charge.
- **SCR-029 reader:** table of contents toggle → content heading and semantic reading area → typography controls/bookmark. Reading order remains coherent with visual layout.

## Prototype and research checklist

Prototype editor save/offline/conflict, import warnings, release blockers, proof version change, 2D book detail and payment-pending recovery in a design tool; no prototype currently exists. Include desktop, narrow mobile, RTL shell with independent LTR manuscript, and keyboard focus/announcements. Recruit authors with and without screen readers, editorial, finance and multilingual writers under a consented research plan; avoid implying interviews have happened.

| Task | Proposed observation / threshold selection |
|---|---|
| Locate an unsaved change and recover after disconnect | Record completion, time, error and participant explanation; set threshold before study. |
| Export a draft without submitting | Record independent completion and any belief that publication is required. |
| Identify a missing rights territory and block release | Record false-release attempts and whether blocker was understood. |
| Retry a payment with uncertain status | Record whether participant tries to pay twice and whether status is understood. |
| Use editor/reader with keyboard and screen reader | Record blocked steps, focus and announcements; no untriaged critical barrier at pilot gate. |

Report sample, methods, success definition and uncertainty. Test with real content only with permission and appropriate privacy safeguards. Research Lead owns recruitment and protocol; Product Owner chooses targets before the pilot.

## Cross-role review checkpoint

| Role | Concern / draft response | Residual risk | Required approval |
|---|---|---|---|
| Research / UX | Wireframes need observed author and reader tasks | No live prototype or participants | Product / UX Research |
