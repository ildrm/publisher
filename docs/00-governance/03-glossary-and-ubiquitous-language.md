# GOV-003 — Glossary and ubiquitous language

- **Version / date:** 0.2 / 2026-10-29
- **Status:** Draft — review and approval pending
- **Authoring / accountable role:** Business Analyst / Requirements Engineer
- **Consulted roles:** Editorial, Document Engineering, Conversion, Legal, Finance, Commerce, Accessibility, Technical Documentation
- **Reviewer / approver / decision owner:** Domain leads / Product Owner / Business Analyst; no human approval recorded
- **Assumptions:** ASM-004–010; definitions describe the proposed model, not an assertion of law or physical database schema.
- **Related requirements:** Source prompt §§0, 9, 11 and 15; the draft [feature catalog](../02-requirements/03-feature-catalog-and-prioritization.md) and [SRS](../02-requirements/02-system-requirements-specification-srs.md) exist, but glossary-to-requirement traceability is incomplete.
- **References:** [scope](01-scope-and-assumptions.md); [decision register](02-decisions-and-open-questions.md); source master prompt v1.0.

## Language rules

Use these names consistently in UI, contracts, events, diagrams and tests. A conceptual entity is not automatically one database table. “Book” is a user-facing umbrella term only; in technical specifications name the precise object below. A status transition must not imply that another object's rights or approvals have been granted. The glossary owner reviews changes and records terminology conflicts through document control.

| Term | Meaning and boundary |
|---|---|
| User / author profile / pen name | An authenticated account / author-facing identity / optional public name. One account can use several names subject to policy. |
| Organization / imprint | Administrative tenant or business organization / publishing brand under which a release appears. Their relationship is not fixed before OQ-001/003. |
| Workspace / membership | An authorization and organization boundary for projects / a role-bearing relationship to that boundary. Project permissions may be narrower. |
| Work / project | The intellectual creation as a concept / its managed authoring workspace and administrative container. Neither implies permission to publish. |
| Manuscript / document node / chapter | Structured author content / a semantic element of that content / a named structural unit; presentation is a separate concern. |
| Draft | Mutable authoring state, potentially containing pending unacknowledged changes; it is private unless access is explicitly granted. |
| Acknowledged save | Server response only after the specified durable commit boundary has succeeded; the exact durability and recovery guarantee remain to be proven under DEC-005. |
| Manuscript version or revision | Identifiable snapshot of structured source and metadata; a restorable author version is not an approved publishing edition. |
| Submission | Author's deliberate request for publisher consideration, tied to a version and declarations; it does not transfer copyright or guarantee acceptance. |
| Review decision / accepted title | Editorial decision on a submission / a work selected for production. Acceptance does not itself grant missing rights or approve publication. |
| Contract / rights grant | Signed or otherwise authorized agreement / a scoped permission with parties, terms, language, territory, format, channel and effective interval; subject to legal validation. |
| Publication / edition | Authorized release action and record / a distinct version of a work prepared for publication. Corrections and later editions must retain lineage. |
| Rendition / export artifact | Format-specific output derived from a specified version and configuration / stored file and provenance. An approved rendition is immutable or versioned. |
| Catalog listing / product | Public descriptive discovery record / purchasable offer with format, territory and commercial terms. Neither grants access without an entitlement. |
| Order / payment / refund | Customer purchase intent / transaction outcome / later monetary reversal; each has separate lifecycle and provider reconciliation. |
| Entitlement / license | Recorded customer's scoped access right to an acquired product. Its legal terms are jurisdiction and agreement dependent. |
| Sale / settlement event | Sale attributed to an order or channel / externally reported clearing or settlement fact. Dashboard counters are not the authoritative ledger. |
| Royalty rule / ledger entry / statement / payout | Contract-derived calculation / auditable financial posting / period report / transfer of cleared payable funds. Each is separate and retry-safe. |
| Asset / asset license | Image, cover, font or other file / evidence of permission to use it in specified contexts. Uploading does not establish rights. |
| Conversion job / preflight / proof | Tracked asynchronous transformation / checks on outputs and configuration / human-reviewed representation or physical sample. Validation does not replace proof approval. |
| 3D model artifact | Derived visual representation with geometry inputs and provenance; illustrative dimensions must be disclosed, and 2D equivalent available. |
| Public search / private search | Index of authorized released public records / search confined to authorized workspace content; they require separate access boundaries. |
| Audit event | Access or business action recorded with actor, scope, time and outcome under retention and privacy rules; not a substitute for a financial ledger. |
| RPO / acknowledged-save durability / RTO | Permitted recovery point gap for backups / survival promise for a successful write / target restoration duration. These are distinct and require measured proof. |

## Unresolved questions

OQ-001, OQ-003 and OQ-009 can change legal meanings, settlement states and contract terms. Domain owners must settle overlaps between work/project, publication/edition and entitlement/license before implementing database constraints. No claim of formal legal terminology is made.
