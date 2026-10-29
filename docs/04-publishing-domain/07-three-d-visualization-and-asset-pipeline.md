# PUB-007 — 3D visualization and asset pipeline

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft, not reviewed or approved.
- **Authoring/accountable:** 3D / Web Graphics Engineer; **consulted:** Print, Accessibility, Frontend, Product, Security; **reviewer:** QA Lead; **approver:** Publishing Director; **decision owner:** Editorial and Publishing Operations Lead. Roles are proposed, not evidence of human review.
- **Assumptions:** ASM-001–012; curated single-imprint pilot, portable drafting, rights and jurisdiction unresolved. **Related requirements:** FR-3D-001, FR-FMT-001, FR-CAT-001.
- **Unresolved:** OQ-001, OQ-003–007, OQ-009–010; assigned governance owners resolve before contract, vendor, proof and release milestones.
- **References:** [scope](../00-governance/01-scope-and-assumptions.md), [decision register](../00-governance/02-decisions-and-open-questions.md), [business rules](../02-requirements/05-business-rules-and-permissions.md), user-supplied master prompt v1.0 §§3, 5, 11–15.

## Scope and fallback

The P0 baseline is an accessible 2D cover and textual description. A 3D physical-book preview is a P1 candidate and may be piloted only when capacity and verified geometry permit; it is never required for reading, purchasing or printing. Immersive story worlds and AR are separate future discovery tracks. No 3D visual is a manufacturing proof.

When available, inputs include trim width/height, page count, paper caliper and binding/cover thickness, front/back/spine artwork, safe areas and printer/source version. Record units, conversion, uncertainty, date, rights, hashes and named owner. A provisional page-block estimate is `page count ÷ 2 × paper caliper`, only if the vendor defines page count as printed sides and caliper as thickness per leaf; cover, glue and binding add separate vendor-specific allowances. Do not advertise exact spine size from this equation alone. Missing or unverified values require an explicitly labeled illustrative representation or the 2D fallback. Physical proof and actual printer calculations prevail.

## Pipeline and interactions

Validate uploaded artwork type, size, dimensions, license and scan status; sanitize image/SVG handling. Derive a model from approved parameters in a resource-limited worker, record source/config/artifact hashes, and store private versions privately. Only approved public cover assets can be delivered to the store. Optional glTF/GLB interchange requires toolchain and licensing evaluation. Retry jobs idempotently and retain prior approved artifacts; failures show an actionable report without exposing private assets.

Provide keyboard-operable rotate/reset/zoom controls, accessible descriptive text for title/author/format, visible focus, non-motion option, and a 2D view reachable without WebGL or a pointer. Reduced-motion preference disables nonessential animation. On unsupported/low-power devices, failures or loading timeouts fall back to 2D with a status message. No essential book information may exist only in the 3D canvas. Viewer telemetry records load, performance category and fallback, without content or identity beyond policy.

## Verification

Compare model dimensions and artwork with actual printer-approved input and physical sample; test missing/incorrect dimensions, asset licensing, mobile and low-power fallback, keyboard controls, screen reader description, zoom, motion settings and private/public authorization. Targets and representative device matrix require pilot measurement; no rendering test, proof or accessibility conformance is asserted here.

## Cross-role review checkpoint

| Role | Concern / draft response | Residual risk | Required approval |
|---|---|---|---|
| Graphics / Accessibility | Optional 3D must be labeled and retain 2D fallback | Geometry and device performance untested | Production / Accessibility |
