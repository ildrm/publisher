# DISC-07 — Standards and source register

Version 0.2 · 2026-10-29 · **Draft** · Author: Accessibility and Internationalization Specialist · Accountable/decision owner: Solution Architect · Consulted: Security, Publishing Production, Legal, QA, API and 3D leads · Reviewer: QA Lead · Approver required: Product Owner and relevant domain leads

**Assumptions:** reference versions below are research observations, not evidence of product compliance. **Related:** REQ-06; DISC-02; architecture and format specifications. **Unresolved:** launch jurisdictions, retailer and printer profiles, supported reading systems, audit scope and tooling version; relevant owners must decide before production acceptance. All sources checked 2026-10-29.

| Source and status | Use / verification boundary |
|---|---|
| [WCAG 2.2](https://www.w3.org/standards/history/WCAG22/) — W3C Recommendation, revised 2024-12-12 | Proposed AA product UI target; independent audit and assistive technology testing required. |
| [EPUB 3.3](https://www.w3.org/TR/epub/all/) — W3C Recommendation, 2026-01-13; EPUB 3.4 is Candidate Recommendation Draft, 2026-10-27 | Prefer stable 3.3 as provisional baseline; check actual retailer acceptance and do not represent draft 3.4 as a final recommendation. |
| [EPUB Accessibility 1.1](https://www.w3.org/TR/epub-a11y/) — W3C Recommendation, 2024-10-17 | Semantics and discoverability metadata require format and human review, not just a UI audit. |
| [EPUBCheck changelog](https://github.com/w3c/epubcheck/blob/main/CHANGELOG.md) — 5.4.0 production release, 2026-09-15 | Pin and document test version; EPUBCheck validates aspects of format conformance, not complete accessibility or retailer acceptance. |
| [ISO 14289-2:2024 PDF/UA-2](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso%3A14289%3A-2%3Aed-1%3Av1%3Aen) — published | Accessibility-focused PDF profile; exact profile and independent evaluation remain decisions. |
| [ISO 15930-9:2020 PDF/X-6](https://www.iso.org/cms/live/live/en/sites/isoorg/contents/data/standard/07/71/77103.html?browse=tc) — published, ISO notes revision planned | Print-exchange family example, not universal printer requirement. Obtain each printer's accepted preset, proof and color requirements. PDF/X is distinct from PDF/UA. |
| [OWASP ASVS 5.0.0](https://asvs.owasp.org/) — stable, published 2025-05-30 | Select verification level and map controls after threat modeling; no certification implied. |
| [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) — SP 800-218 final | Voluntary secure-development practices reference; implementation must be evidenced. |
| [OpenAPI 3.2.1](https://spec.openapis.org/oas/v3.2) — specification published 2026-09-10 | Current specification observed; selecting 3.1.x can be justified by verified tool compatibility, with migration review. Version in contract is authoritative. |
| [Khronos glTF 2.0.1](https://registry.khronos.org/glTF/) — current registry specification | Optional interchange; does not prove visual or manufacturing accuracy. |
| [NIST AI 600-1](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — Generative AI Profile, 2024-07-26 | Voluntary risk reference for future opt-in AI; provider contracts, evaluations and consent still needed. |

## Review checkpoint

| Role | Concern and response | Residual risk | Approver |
|---|---|---|---|
| Accessibility / Production | UI and book formats have different requirements; split references | No conformance assessment performed | Accessibility and Production leads |
| Security | Standards do not establish controls are implemented | ASVS level and verification pending | Security lead |
| Legal | Applicable rules depend on jurisdiction | No legal or tax opinion given | Counsel |

References are official W3C, ISO, OWASP, NIST, OpenAPI Initiative, W3C validator and Khronos sources linked above. Recheck versions and partner acceptance before procurement and launch.
