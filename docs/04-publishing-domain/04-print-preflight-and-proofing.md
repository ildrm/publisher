# PUB-004 — Print preflight and proofing

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft, not reviewed or approved.
- **Authoring/accountable:** Book Designer / Print Production Expert; **consulted:** Editorial, Conversion, Accessibility, Legal, QA; **reviewer:** QA Lead; **approver:** Publishing Director; **decision owner:** Editorial and Publishing Operations Lead. Roles are proposed, not evidence of human review.
- **Assumptions:** ASM-001–012; text-centric curated pilot and scoped rights. **Related requirements:** FR-FMT-001, FR-PUB-002.
- **Unresolved:** OQ-001, OQ-003–007, OQ-009–010; assigned governance owners resolve before contract, vendor, proof and release milestones.
- **References:** [scope](../00-governance/01-scope-and-assumptions.md), [decision register](../00-governance/02-decisions-and-open-questions.md), [business rules](../02-requirements/05-business-rules-and-permissions.md), user-supplied prompt v1.0 §§3, 5, 11–15.

## Preflight and proof

1. Freeze source revision, approved metadata, licensed assets and printer preset; record trim, binding, paper, page count and font licenses. Printer-specific bleed, safe area, color profile and allowable file format must be confirmed with the actual vendor.
2. Generate a versioned interior and cover. Check missing fonts, illegal embedding, images below agreed effective resolution, missing alt text for digital equivalents, wrong color space, overflow, clipping, blank/unexpected pages, running heads, page numbering, widows/orphans, chapter breaks and page count. Treat warnings as visible decisions, not silently successful output.
3. Derive cover/spine geometry only from approved printer parameters. Compare title, author, ISBN/barcode if applicable, cover wrap and safe zones to actual vendor specifications. Print and digital outputs have separate validation paths.
4. Produce a digital proof and, when required, an actual physical proof from the target printer; editorial and author inspect against a versioned checklist. Record artifact hash, printer/preset version, proof type, reviewer, decision, reason and time. A digital preview does not certify manufactured color, binding or dimensions.
5. Reject/hold on failed validation, missing rights or unresolved proof issue. An approved change to source, layout, cover, printer parameters or metadata invalidates affected approvals and triggers a new proof. Release links the approved artifact, not the most recently generated job.

Acceptance requires human-readable preflight reports, an accountable approval trail and an actual print sample where applicable; no evidence of such a proof exists yet. Printing/distribution partnership and vendor profile remain OQ-005/007. Compare low-resolution and oversized inputs, RTL rendering, page overflow, font failures and spine errors in fixture-based QA before pilot.

## Cross-role review checkpoint

| Role | Concern / draft response | Residual risk | Required approval |
|---|---|---|---|
| Print / Editorial | Proof must bind actual preset and artifact | No physical sample or vendor preset | Production / Publishing |
