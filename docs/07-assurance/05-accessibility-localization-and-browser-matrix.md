# QA-05 — Accessibility, localization and browser matrix

Version 0.3 · 2026-10-29 · Status: Draft assurance plan; local aggregate and both browser suites passed; independent manual acceptance pending  
Authoring/accountable: Accessibility Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Accessibility Lead  
Assumptions: ASM-001–012 and DEC-001–011 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-001–003, FR-EXP-001, FR-3D-001, FR-CAT-001; NFR-A11Y-001–002, NFR-I18N-001–002.

## Proposed matrix and evidence

Target WCAG 2.2 AA for applicable UI; conformance is not asserted. Verify full author, reader, purchase, proof and recovery tasks with keyboard only, visible focus, zoom/reflow, contrast, error announcements, reduced motion and accessible names. Check editor selection, dialogs, import report, 2D preview, reader landmarks and note navigation with a representative screen reader and browser pairing. Test touch targets and orientation on a phone/tablet. Record observed barriers, environment, severity and remediation; independent manual evaluation complements automated scanning.

| Environment candidate | Critical coverage | Status |
|---|---|---|
| Current Chrome and Firefox on desktop | keyboard, editor, checkout and RTL | Versions and support policy pending |
| Current Safari on desktop and mobile | screen reader, touch, editor and reader | Versions and devices pending |
| Current Edge on desktop | keyboard, authoring and payment | Version pending |
| Low-power mobile / degraded network | 2D fallback, unsaved status, focus and reduced motion | Device/network profile pending |

The dedicated [multilingual Chrome run](../../implementation/evidence/i18n-e2e-results.json) passed all 15 entry-interface choices and unsaved/account switches, same editor DOM, working Undo/Redo, source/metadata preservation until retry, exact Unicode after save, French native validation and Japanese reload persistence. It exercised 1440×960 and selected 390×844 states with no document-width overflow. [Arabic desktop/Urdu mobile axe scans](../../implementation/evidence/i18n-axe-results.json) reported zero violations. Strict build, 47 Python/9 JS application tests, separate 16 Python/3 JS reference tests and the authoring browser regression also passed; [verification](../../implementation/test-evidence.md) records scope/hashes/logs. Installed Chrome via Playwright was the fallback because IAB was unavailable. These checks do not establish physical selection/IME, actual mobile devices, cross-browser support, native language approval or assistive-technology conformance.

Test all 15 interface choices: `en`, `zh`, `hi`, `es`, `ar`, `fr`, `bn`, `pt`, `id`, `ur`, `ru`, `de`, `ja`, `pcm`, `fa`. Validate exact catalog key/placeholder parity and nonempty translations, relevant count plural categories, locale-aware dates/numbers, localized error descriptors and accessible names, device/browser/account preference precedence, current-user-only preference updates, and schema-1 upgrades through migration 002. Exercise switching while unsaved without editor remount, text/selection/undo loss, metadata mutation or extra revision. Check account synchronization failures and restricted device storage. Exact current results must be recorded in [implementation evidence](../../implementation/test-evidence.md); prior English-interface logs do not establish multilingual acceptance. Catalogs are implementer drafts without native human approval.

Test English UI with Persian/Arabic manuscript, Arabic/Persian/Urdu RTL UI with LTR quotes and mixed numbers, German/French expanded copy, CJK IME composition, combining marks, Unicode normalization and search, save/reload/restore and currently implemented portable exports. UI direction and document direction are independent. EPUB/PDF, publisher proof and purchase journeys are planned later features and cannot be tested as implemented flows yet. When implemented, check export semantics with assistive technology on at least two reading systems; include publisher preview and author proof approval. No independent manual audits or broad browser/assistive-technology compatibility claims have occurred. See [multilingual review](../../implementation/multilingual-review.md).

## Open questions and references

Which browser versions, assistive technologies, locales and external reviewers constitute the signed support matrix? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Accessibility Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
