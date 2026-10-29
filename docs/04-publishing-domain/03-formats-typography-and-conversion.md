# PUB-003 — Formats, typography and conversion

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft, not reviewed or approved.
- **Authoring/accountable:** Publishing Conversion / Typesetting Engineer; **consulted:** Print, Accessibility, Document Engineering, Security; **reviewer:** QA Lead; **approver:** Publishing Director; **decision owner:** Editorial and Publishing Operations Lead. Roles are proposed, not evidence of human review.
- **Assumptions:** ASM-001–012; text-centric curated pilot and scoped rights. **Related requirements:** FR-IMP-001, FR-EXP-001, FR-FMT-001.
- **Unresolved:** OQ-001, OQ-003–007, OQ-009–010; assigned governance owners resolve before contract, vendor, proof and release milestones.
- **References:** [scope](../00-governance/01-scope-and-assumptions.md), [decision register](../00-governance/02-decisions-and-open-questions.md), [business rules](../02-requirements/05-business-rules-and-permissions.md), user-supplied prompt v1.0 §§3, 5, 11–15.

## Format compatibility and boundaries

This is a planning matrix, not a vendor capability or standards-conformance claim. Pilot selection and real fixtures require OQ-007, provider diligence and approval. Portable author export is independent of publication; preserve content and relevant metadata even if styling differs.

| Format | Input | Output | Proposed phase / conversion and validation |
|---|---|---|---|
| DOCX | Yes, bounded styles, notes and images after safe parse | Yes, portable export | P0; map styles to semantic roles; report unsupported structures and compare fixtures. |
| Markdown | Yes | Yes | P0; preserve headings, lists and links; disclose unsupported rich nodes. |
| Plain text | Candidate | Candidate | P1 or earlier if confirmed; lossy structural/semantic mapping report. |
| HTML / reflowable EPUB | Candidate only after sanitizer and licensing review | Accessible webbook / EPUB | EPUB output P0; HTML and EPUB input P1; validate package, reading order, links and assistive technology behavior. |
| Accessible digital PDF | No editable-PDF conversion guarantee | Candidate separate digital profile | P1 pending PDF/UA toolchain and validation; preserve tags and reading order. |
| Printer-specific PDF | Not an import source | P0 only with approved printer preset | Check trim, bleed, fonts, page count, color and proof; PDF/X profile only if printer accepts it. |
| Fixed-layout EPUB, MOBI, JATS/ONIX, Scrivener | Research only | Research only | P2/P3 subject to channel requirements, licensing and fidelity; MOBI only if justified. |

Source nodes map to a target intermediate semantic tree; transformation records unsupported content and per-node diagnostics, then applies a template and format profile. Typography controls include trim, gutter, margins, chapter openers, running heads, page numbering, page breaks, widow/orphan/hyphenation policy and font licensing. Any manual override and its authorizing person are versioned; accessibility semantics must survive visual styling. Output jobs are isolated, resource-limited and reject executable or unsafe input. Preserve original under retention policy; checksum source, assets, configuration, converter version and artifact. Retry idempotently and retain prior approved output on failure.

Validate EPUB using an agreed current stable EPUB specification and EPUBCheck, and manually open representative output in at least two selected reading systems; selection and acceptance evidence are open. For digital PDF validate the applicable accessible profile and tags; for print validate the vendor-specific PDF/X profile only when accepted. Distinguish validator pass, visual comparison, human approval and real-world distribution acceptance. No conformance or reproduction claim exists until tests and proof evidence are recorded.

## Versioned format profile contract

| Profile | Required inputs / version evidence | Blocking validation and human review |
|---|---|---|
| Reflowable EPUB candidate | Source revision/schema, ordered semantic nodes, language/direction, licensed assets, metadata, converter and profile versions, hashes | EPUBCheck on selected stable target; required navigation, links, alternative text and reading order; representative screen-reader and two selected reading-system reviews. Do not claim conformance from validator pass. |
| Accessible digital PDF candidate | Semantic source, tagging/reading order, font licensing, accessible-profile and renderer version | Applicable PDF/UA profile validation, manual reading-order and assistive-tech review; never assume print PDF is an accessible substitute. |
| Print PDF candidate | Printer identity and dated preset, trim, paper/binding, page count, margins/gutter, bleed, color profile, fonts and cover geometry | Actual printer's accepted PDF/X profile if applicable, dimensions, embedded fonts, overflow and preflight; approved physical proof when required. Preset and proof hashes must match release. |
| DOCX / Markdown portable export | Source revision, schema/mapping version, metadata and asset references | Report unsupported structure and losses; round-trip semantic fixture comparison; author can download without publication. |

For each job freeze the full profile and dependencies, assign an idempotency key to the same inputs and record checksums and structured warnings. Approval is not transferable to a new profile or different artifact. Profile parameters and accepted validation tolerances are selected from actual provider specifications; no common trim, bleed, PDF/X variant or universal retailer support is assumed.

## Cross-role checkpoint

| Role | Concern / response | Residual risk | Required approval |
|---|---|---|---|
| Conversion / Accessibility | Semantic structure survives output | Validator and reading-system compatibility unverified | Conversion / Accessibility leads |
| Print / Editorial | Artifact and actual vendor preset must match | No printer profile or physical proof selected | Print / Publishing leads |
