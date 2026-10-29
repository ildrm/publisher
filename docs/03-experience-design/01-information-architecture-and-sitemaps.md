# UX-001 — Information architecture and sitemaps

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft — not reviewed or approved.
- **Authoring/accountable:** UX/UI lead; **consulted:** Product, Research, Editorial, Accessibility, Security; **reviewer:** QA lead; **approver:** Product Owner; **decision owner:** Product Owner. These are proposed roles; no human approval is implied.
- **Assumptions:** ASM-001–012; single imprint, text-centric curated pilot, accessible 2D baseline, optional later 3D. **Related requirements:** FR-IAM-002, FR-DOC-001, FR-PUB-001, FR-CAT-001, FR-COM-001.
- **Unresolved:** OQ-001, OQ-002, OQ-007 and OQ-010; Product and domain owners resolve before relevant pilot or procurement gate.
- **References:** [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [feature catalog](../02-requirements/03-feature-catalog-and-prioritization.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md), and the user-supplied master prompt v1.0 §8.

## Four scopes

- **Author:** Dashboard → project → manuscript, versions, import/export, permissions and submission. Workspace search is authorization-filtered. Ordinary writing and export never require a submission.
- **Publisher/editorial:** Queue → assigned submission → review, rights, metadata, rendition, proof, release plan and catalog. Production sees only assigned material.
- **Reader/bookstore:** Public store → listing → checkout → customer library → reader; public index includes released metadata and specifically approved samples only.
- **Platform admin/finance:** Role-scoped operations, support/takedown and finance; administrative status does not confer manuscript access. Privileged pages require server authorization and additional authentication per policy.

Global navigation identifies active scope and offers search, notifications and account controls; project navigation adds title, chapters, import/export and history. Breadcrumbs show current scope and parent context. A command palette is optional and must offer only authorized actions; search results identify scope and never blend private manuscript content into public results. Navigation changes cannot silently discard pending edits. Direct routes recheck authorization and cannot use possession of a URL as a grant.

## Proposed routes and hierarchy

Routes in the [screen inventory](03-screen-inventory-and-screen-specs.md) are design identifiers, not implemented API endpoints. `/app` is author, `/publisher` is editorial, `/store` and `/library` are reader and `/admin` is operational. A signed-out user can discover `/store` but is redirected to sign in for private routes without exposing private object names. Public and private search use separate access boundaries. Shared account shell does not imply shared data permissions.

On wide screens use persistent side navigation and a reading/editor workspace; on narrow screens replace side navigation with a labeled menu and show one panel at a time. Restore focus to menu opener on close. Keep the editor's document direction independent from the shell's direction. Notification content avoids manuscript text, payment details and sensitive rights data.

## Review checkpoint

| Role / concern | Draft response | Residual risk / required approval |
|---|---|---|
| Security: scope leakage | Separate public/private boundaries and per-route checks | Threat testing; Security lead |
| Accessibility: mobile focus | Named menus, single-panel navigation and focus restoration | Device and assistive technology validation; Accessibility lead |
| Product: writing locked to publishing | Separate author route and export | Journey validation; Product Owner |
