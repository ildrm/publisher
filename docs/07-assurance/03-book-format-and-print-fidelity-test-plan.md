# QA-03 — Book format and proof fidelity

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Conversion QA Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Conversion QA Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-IMP-001, FR-EXP-001, FR-FMT-001, FR-PUB-002; NFR-A11Y-002.

## Corpus and checks

Use licensed or synthetic fixtures for fiction and nonfiction, 100k-word draft, nested headings, footnotes, links, tables, multilingual and bidirectional passages, images with alt text and font licensing. Keep fixture versions, source hashes and expected semantic maps. Import and export round-trip tests compare text, hierarchy, links, notes and direction, report unsupported features and require author review; compare semantics, not exact office markup.

For each rendition record revision, configuration, fonts and asset hashes, converter version and validation result. Validate EPUB with the selected current EPUBCheck version, inspect reading order and metadata, then open in at least two target reading systems and check screen reader navigation. Test accessible digital PDF separately from a printer-specific PDF/X profile: neither validator alone proves accessibility or print readiness. Run PDF/UA checks and manual reading-order review where applicable. Print fixtures exercise trim, bleed, crop, gutters, overflows, missing/embedded fonts and spine computed from confirmed paper/binding/page count; compare a physical proof to the actual vendor specification. Block release until named production and author approval matches the artifact hash.

Repeat conversions under identical pinned inputs to detect nondeterminism; document expected timestamp or metadata differences. Corrupt assets, missing fonts, renderer failure and incompatible printer profiles must result in actionable reports, not overwrite a good approved artifact. Estimates and mockups are labeled and never substitute for proof.

## Open questions and references

Which reading systems, validators, print provider, physical proof criteria and licensed fonts form the pilot acceptance matrix? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Conversion QA Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
