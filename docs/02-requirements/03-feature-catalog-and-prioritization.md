# REQ-03 — Feature catalog and prioritization

- Version/date: 0.2 / 2026-10-29; status: **DRAFT — partial**, not approved.
- Accountable: Product Owner. Consulting: requirements, editorial, architecture, accessibility, finance, legal and QA leads. Reviewer: QA lead. Approver/decision owner: Product Owner and Publishing Director; real approval outstanding.
- Assumptions: [scope and assumptions](../00-governance/01-scope-and-assumptions.md); provisional single-imprint curated model and portable studio. Source status: **REQUIRED** means explicitly requested in the supplied brief; it is not proof of market demand. **PROPOSED** means a design hypothesis.
- Related requirements: [SRS](02-system-requirements-specification-srs.md), [stories](04-epics-user-stories-and-gherkin.md), [business rules](05-business-rules-and-permissions.md), [NFRs](06-nonfunctional-requirements-and-slos.md).
- Open questions: launch jurisdictions, partners, content formats, rights and payment settlement remain open in the decision register. References: supplied master prompt; discovery evidence matrix.

## Contents

- [Prioritization method](#prioritization-method)
- [Core pilot candidate records](#core-pilot-candidate-records)
- [Full-universe inventory and scope boundaries](#full-universe-inventory-and-scope-boundaries)
- [Review checkpoint and outstanding work](#review-checkpoint-and-outstanding-work)
- [Decomposed capability register — scope map, not approved backlog](#decomposed-capability-register--scope-map-not-approved-backlog)

## Prioritization method

Priority P0 is a release-blocking condition of the proposed balanced pilot, P1 is the next professional expansion, P2 is later discovery/extension, and P3 is explicitly deferred pending a business case. MoSCoW is Must, Should, Could, Won't for this pilot; phase is Pilot, Phase 2, or Phase 3. A P0 label does not constitute a commitment that the pilot is small enough: capacity and external dependencies must be validated. Complexity bands S/M/L/XL are relative and **not estimates of time or cost**; confidence is low until engineering spikes. Alternative lean author-studio-only release is discussed in governance and is not silently combined with this pilot.

The ranking uses a dependency and risk gate before numerical scoring: portability and durable saves precede acquisition; rights and approvals precede publication; entitlement and balanced ledger precede selling. P0 core is selected by that gate, not by a fabricated RICE value. The directional scores below are subjective planning hypotheses: `score = 2 × user/risk value + dependency leverage + readiness`, each input 1 (low) to 3 (high), yielding 4–12. Scores are not measured impact, reach or effort; readiness is not an engineering estimate. Higher scores indicate a suggested research/order discussion, not automatic release admission. Score confidence is low across all areas. Product and affected owners must revisit after discovery, a technical spike and pilot capacity sizing.

| Area | Value | Dependency leverage | Readiness | Score | Provisional rationale |
|---|---:|---:|---:|---:|---|
| A account and B authoring | 3 | 3 | 2 | 11 | Durable access and content precede other flows |
| I conversion and portability | 3 | 3 | 1 | 10 | Exit and production depend on fidelity spikes |
| K editorial and L rights | 3 | 3 | 1 | 10 | Publication is blocked without decisions and rights |
| N store and O finance | 3 | 3 | 1 | 10 | Sales require entitlement, ledger and market partners |
| Q operations | 3 | 3 | 1 | 10 | Recovery and scoped operations are release controls |
| G assets and H formatting | 3 | 2 | 1 | 9 | Approved renditions depend on production tooling |
| D collaboration | 2 | 2 | 1 | 7 | Useful workflow, synchronization remains high risk |
| M distribution | 2 | 2 | 1 | 7 | External reach depends on provider diligence |
| C planning, E productivity and P growth | 2 | 1 | 2 | 7 | Potential adoption benefits are unvalidated |
| J visualization | 1 | 1 | 1 | 4 | Optional enhancement; 2D accessible preview suffices initially |
| F AI and R advanced verticals | 1 | 1 | 1 | 4 | Separate privacy, legal and economic discovery needed |

These aggregate scores do not override the Must/Should/Could/Won't placement of individual records. The same domain may contain mandatory pilot controls and deferred capabilities; e.g. safe accounts and manuscript persistence are P0 while advanced features in A/B are P1. Equal scores are ties, not evidence that items cost the same. Validate sensitivity by re-ranking with each input ±1 within its 1–3 range; if the scope decision changes, investigate before committing. RICE may be applied later when cohort reach, impact and effort have evidence.

## Core pilot candidate records

Each row is a **capability-level draft**, not the prompt's requested complete atomic inventory. The detailed requirement expansion, route/API mappings, individual input schemas, test cases and telemetry for every feature remain work for the next documentation increment. The shared acceptance scenarios for high-risk capabilities are in [REQ-04](04-epics-user-stories-and-gherkin.md). User-visible action entry points are provisional screen names, not completed screen contracts. Source for each row: REQUIRED unless stated otherwise.

| ID | User/value and business rule | Priority / phase | Build and rationale | Entry / permission | Dependencies; effort / confidence | Telemetry and privacy |
|---|---|---|---|---|---|---|
| FR-IAM-001 | Author authenticates and recovers account; verify email and protect privileged roles with MFA. | Must P0 / Pilot | Integrate identity; avoid custom authentication. | Sign in; account holder | Email delivery, provider review; L / low | auth success/failure counts; never log secrets |
| FR-IAM-002 | Owner grants scoped project access and can revoke it; new reads/writes fail immediately after revocation. | Must P0 / Pilot | Native authorization; provider identity does not define project rights. | Project access; owner | IAM-001, audit; L / low | access changes; no manuscript text |
| FR-DOC-001 | Author creates a project with ordered chapters and semantic content independent of publishing. | Must P0 / Pilot | Native domain, licensed editor candidate subject to evaluation. | Dashboard/editor; owner | IAM-002, schema; XL / low | project/chapter created; aggregate counts |
| FR-DOC-002 | Author receives a saved acknowledgement only after durable server commit; unsynced changes remain visibly distinct. | Must P0 / Pilot | Native save protocol; editor component may be licensed. | Editor; authorized writer | DOC-001, concurrency, durable storage; XL / low | save outcome, latency, queue depth; never capture text |
| FR-DOC-003 | Author snapshots and restores a revision as a new version without erasing history. | Must P0 / Pilot | Native versioning. | Editor history; owner/authorized writer | DOC-002, retention policy; L / low | snapshot/restore outcome, version IDs |
| FR-IMP-001 | Author imports supported DOCX/Markdown, sees unsupported constructs and can recover the source file. | Must P0 / Pilot | Isolated converter with evaluated components. | Import center; author | DOC-001, scanning, format spike; XL / low | format, warnings and outcome; no content |
| FR-EXP-001 | Author exports manuscript and metadata independently of submitting or publishing. | Must P0 / Pilot | Native orchestration, licensed converters as evaluated. | Export center; authorized owner | DOC-003, jobs, storage; L / low | format, job outcome and latency |
| FR-PUB-001 | Author submits a specific revision; editorial staff triage and return decisions with reasons. | Must P0 / Pilot | Native workflow. | Submit / editorial queue; owner/editor | DOC-003, role grants; L / low | submission transition IDs |
| FR-PUB-002 | Publisher releases only an approved edition whose rights and rendition checks pass; holds block release. | Must P0 / Pilot | Native state machine with human gates. | Release plan; publisher admin | PUB-001, RGT-001, FMT-001; XL / low | approval and release audit events |
| FR-RGT-001 | Publisher records scoped rights grants and their evidence; no assumed copyright transfer. | Must P0 / Pilot | Native records; contract signing partner only after diligence. | Rights record; rights officer | legal model, contributors, retention; L / low | grant lifecycle; contracts restricted |
| FR-FMT-001 | Production creates versioned EPUB and printer-preset PDF from a frozen source/configuration; failed jobs cannot replace an approved artifact. | Must P0 / Pilot | Isolated worker and evaluated converters. | Format/export; production | DOC-003, assets, validator, printer preset; XL / low | job state, checksum, diagnostics without content |
| FR-3D-001 | Reader/author sees a 3D cover only with disclosed geometry assumptions or a 2D accessible fallback. | Should P1 / Phase 2; optional pilot candidate | Native viewer using evaluated library; accessible 2D cover is the P0 baseline. | Preview; authorized author or public catalog viewer | cover assets, binding and page dimensions; L / low | load/fallback/error counts |
| FR-CAT-001 | Reader discovers only released, authorized public listings and samples and can access a 2D cover and text equivalent without 3D. | Must P0 / Pilot | Native catalog; separate public index. | Store/listing; public | PUB-002, permissions, metadata; L / low | privacy-reviewed discovery events |
| FR-COM-001 | Buyer pays once and receives the licensed edition after confirmed payment, with support for failed and disputed payment. | Must P0 / Pilot | Integrate a payment processor with hosted checkout; native entitlement. | Checkout/library; customer | availability by market, catalog, webhooks; XL / low | order, payment status and reconciliation; no card data |
| FR-FIN-001 | Finance posts sales/refunds once, reconciles balances and pays only cleared eligible amounts. | Must P0 / Pilot | Native ledger; payout partner dependent. | Finance statement; finance role | rights/royalty rule, verified payment and payout rails; XL / low | ledger IDs, discrepancies, payout status; restricted PII |
| FR-OPS-001 | Operators restore tested backups and produce access/financial audit evidence under controlled access. | Must P0 / Pilot | Native controls plus cloud capabilities. | Operations console; scoped ops | retention, storage, incident policy; L / low | redacted audit and restore test outcomes |

**Cross-cutting record expectations:** every operation must enforce authorization server-side, expose accessible progress/error states, support localization and RTL without conflating UI and manuscript direction, and avoid logging private content. Every change in access, rights, publication or financial state requires an attributable audit event. Requirements are not implemented or tested by this document.

## Full-universe inventory and scope boundaries

This map enumerates the brief's domains and major sub-capabilities; it does **not** claim that each named item has its own atomic FR yet. Each grouping needs decomposition, flows, UI/error states, compliance analysis and tests before procurement-ready status. Proposed phases can change when the release is sized.

| Brief area | Normalized scope to decompose | Initial placement / approach |
|---|---|---|
| A Identity/trust | login, recovery, MFA, pseudonyms, profiles, organizations, invitations, scoped rights, quotas, consent, export/deletion, audits, notifications | P0 essentials; P1 organizations/quotas; integrate identity |
| B Manuscript | wizard, structural nodes, editing/semantics, navigator, search, style, citations, notes, images, IME/RTL, mobile, autosave, undo, snapshots | P0 essentials; complex tables/citations after fidelity spike; evaluated editor component |
| C Planning/research | plots, beats, scenes, characters, timelines, world/series bible, notes, sources, bibliography, continuity | P1 planning basics; P2 automation; native or component |
| D Collaboration | roles, invites, realtime presence, comments, suggestions, compare/approve, beta links, revocation, reconnect | P0 scoped access; P1 reviews/realtime after sync evaluation |
| E Productivity | goals, milestones, streaks, timers, trends, reminders, groups and challenges | P1 basic goals; P2 community; native |
| F AI | ideation, proofreading, translation, search, metadata, alt text, provenance, human approval, consent, metering | P2; opt-in provider integration only after privacy/IP review; no training by default |
| G Cover/assets | uploads, rights, licenses, resolutions, templates, variants, proof, colors and barcode | P0 controlled assets/metadata; P1 cover tools; integrate or license |
| H Formatting | semantics, trim/gutters, templates, typography, reading order, fonts, PDF/UA, PDF/X and printer proof | P0 text-centric preset and manual approval; P1 richer layout |
| I Conversion | DOCX/Markdown/plaintext, HTML/EPUB, portable outputs, EPUB, web, PDFs, metadata, validation and provenance | P0 DOCX/Markdown and EPUB/print preset; other formats P1/P2; no general PDF-to-editable promise |
| J 3D | actual geometry, rotation, materials, page-turn, alternate text, low-power fallback, glTF and AR | P0 accessible 2D; P1 static 3D candidate, potentially piloted if capacity and geometry allow; P2 animation/AR; separate immersive research |
| K Editorial | intake, declarations, screening, review, revise, editorial tasks, approvals, hold, corrections and takedown | P0 controlled queue/release; P1 enhanced screening and workflow; human decisions |
| L Rights/metadata | contributors, grants, scope, contracts, identifiers, classifications, ONIX, expiry and disputes | P0 scoped rights/basic metadata; P1 e-sign and ONIX integration after validation |
| M Distribution | imprint, catalog, schedule, POD, proofs, channel sync, returns, reconciliation | P0 internal release; P1 partner distribution after vendor diligence |
| N Store/reader | discovery, search, samples, cart/payment, library, accessible reader, reviews, recommendation, gifts/refunds | P0 listing/purchase/entitlement and basic reading model; P1 richer library/reviews |
| O Finance | tiers, royalties, sales, refunds, payouts, statements, tax/FX, recoupment, audit | P0 ledger and reconciliation; P1 subscriptions and advanced rules; market-specific partner |
| P Growth | SEO, launches, consented email, referrals, communities, moderation, support | P0 discoverability/support basics; P1 marketing; P2 communities |
| Q Administration | roles, flags, takedown, abuse, retention, incident, recovery, integrations, monitoring | P0 scoped admin/audit/recovery; P1 richer automation |
| R Verticals | audio, translation, comics, children, educational, academic, interactive, lending, B2B, immersive | P3 research individually; each needs new rights, accessibility, cost and format analysis |

## Review checkpoint and outstanding work

| Role | Concern / response | Residual risk and required decision |
|---|---|---|
| Product / delivery | Scope is broad; dependencies prioritized before scoring. | Feasible pilot cutoff and capacity approval required. |
| Authoring / accessibility | Save, portability and RTL put before growth features. | Editor and import fidelity need prototype evidence. |
| Editorial / legal | Rights and human release gates precede catalog. | Counsel and editorial leadership must approve policy by launch milestone. |
| Finance / integration | Payment and royalty are separate authoritative states. | Market-specific settlement and ledger design need review. |
| QA / security | Failure states and private-data boundaries are explicit. | Feature-level test and threat coverage remains incomplete. |

No simulated review in this file represents human approval. Remaining work: expand every inventory item into atomic FR records with all requested fields; enumerate P0/P1 UI/API/data/test links; establish evidence-backed scores and executable traceability.

## Decomposed capability register — scope map, not approved backlog

The following records give each named capability a stable reference and provisional placement. They supplement, do not replace, the P0 core records above; matching core records are the authoritative pilot acceptance criteria. Where a grouped row overlaps a P0 core capability, its P1/P2 label applies **only to the extended features beyond that baseline**; it does not defer the core. Each record inherits its domain dependencies in the table below. Baseline privacy, applicable access/export/deletion obligations, accessibility and security cannot be postponed by these expansion labels; legal counsel must determine applicable requirements before launch. **REQUIRED** means present in the supplied brief, not approved funding or validated need. Phase assignments are proposed: P1/Should = Phase 2, P2/Could = Phase 3 discovery, P3/Won't = deferred research. Do not infer release promises from P1/P2. Each record inherits the shared contract below; items marked as collections still need decomposition to atomic requirements before implementation or procurement.

| Every grouped record in domain | Mandatory baseline and inherited dependency |
|---|---|
| IAM, COL | FR-IAM-001/002 and NFR-SEC-001/004; consent and applicable export/deletion controls before launch |
| DOC, PLAN, PROD | FR-DOC-001/002/003, FR-EXP-001 and NFR-A11Y-001, NFR-I18N-001/002, NFR-PERF-001 |
| AI | NFR-PRIV-002 and explicit consent before enabling any processing; no training by default now |
| ASSET, FMT, CONV | FR-IMP-001, FR-EXP-001, FR-FMT-001 and NFR-SEC-003/A11Y-002 |
| VIS | FR-CAT-001.2 P0 2D/text baseline; FR-3D-001 P1 optional pilot geometry and fallback |
| EDIT, RIGHTS, DIST | FR-PUB-001/002, FR-RGT-001, FR-FMT-001 |
| STORE | FR-CAT-001, FR-COM-001, FR-FIN-001 and NFR-A11Y-001 |
| FINANCE | FR-COM-001, FR-FIN-001 and NFR-FIN-001; jurisdiction and provider policy |
| GROWTH, ADMIN | FR-IAM-002, FR-OPS-001, NFR-PRIV-001/002 and applicable user rights |
| VERT | Relevant baseline security, accessibility, rights and finance controls; separate business case and capability review |

**Shared record contract:** user and owning domain are in the table; value is successful completion of the named job while preserving author ownership. Preconditions: valid scoped authority, supported format and required consent. Main flow: enter the named workspace, provide valid input, review warnings and persist a versioned result. Alternate: cancel without changing the authoritative state. Error: deny unauthorized requests, retain prior good state, identify the failed operation and offer a safe retry or support route. All views require keyboard access, localized text and independent text direction; inputs are validated server-side; no private text enters telemetry or public search; changes to rights, access, editorial or financial state are audited. Default telemetry: privacy-reviewed operation, result and latency without manuscript content; opt-in rules apply. Compliance: legal, format, IP, accessibility and retention decisions remain jurisdiction- and product-specific. Dependencies: identity, scoped authorization, domain data and relevant core P0 prerequisites; exact UI/API/schema/test links are **OPEN**, owned by Requirements Lead before scope commitment. Complexity is M/L, confidence low, until a spike; build classification is provisional. Shared test obligation: valid action succeeds; unauthorized or invalid input fails with no mutation; retry, race, network or boundary input preserves the last valid state. Named records containing multiple functions need more granular acceptance, edge cases and test data; this is not evidence of completeness or testing.

| Requirement | Job / value | Role / domain and entry | Priority / release | Approach |
|---|---|---|---|---|
| FR-IAM-101 | Signup, login and verified email | Account holder / Identity and access | P0 baseline FR-IAM-001; P1 extensions | integration |
| FR-IAM-102 | Credential recovery and privileged MFA | Account holder / Identity and access | P0 baseline FR-IAM-001/NFR-SEC-004; P1 extensions | integration |
| FR-IAM-103 | Public profile and pseudonyms | Account holder / Identity and access | Should / P1 / Phase 2 | integration |
| FR-IAM-104 | Organizations and imprints | Account holder / Identity and access | Should / P1 / Phase 2 | integration |
| FR-IAM-105 | Workspace and project folders | Account holder / Identity and access | P0 private workspace FR-DOC-001; P1 advanced folders | integration |
| FR-IAM-106 | Invitations and scoped memberships | Account holder / Identity and access | P0 scoped access FR-IAM-002; P1 role extensions | integration |
| FR-IAM-107 | Subscription quotas and team administration | Account holder / Identity and access | Should / P1 / Phase 2 | integration |
| FR-IAM-108 | Privacy settings and versioned consents | Account holder / Identity and access | P0 applicable purpose and consent controls; P1 enhancements | integration |
| FR-IAM-109 | Account export and deletion | Account holder / Identity and access | P0 portability FR-EXP-001 and applicable deletion rights; P1 enhancements | integration |
| FR-IAM-110 | Notifications and access audit | Account holder / Identity and access | Should / P1 / Phase 2 | integration |
| FR-DOC-101 | Project setup and genre templates | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-102 | Parts chapters scenes and navigation | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-103 | Semantic headings emphasis and quotations | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-104 | Lists links scene breaks and tables | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-105 | Images captions and alt text | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-106 | Footnotes endnotes citations and bibliography | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-107 | Front matter back matter and appendices | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-108 | Keyboard and Markdown shortcuts | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-109 | Find and replace across project | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-110 | Undo redo and revision comparison | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-111 | Focus mode and manuscript statistics | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-112 | Paste fidelity and mobile editing | Author / Authoring | Should / P1 / Phase 2 | licensed component |
| FR-DOC-113 | RTL CJK diacritics and IME composition | Author / Authoring | P0 baseline NFR-I18N-001/002; P1 enhancements | licensed component |
| FR-DOC-114 | Large manuscript performance and recovery | Author / Authoring | P0 baseline NFR-PERF-001/006 and FR-DOC-002/003; P1 enhancements | licensed component |
| FR-PLAN-101 | Scene and plot boards | Author / Planning | Should / P1 / Phase 2 | native build |
| FR-PLAN-102 | Beat sheets and narrative structure templates | Author / Planning | Should / P1 / Phase 2 | native build |
| FR-PLAN-103 | Timelines and parallel story lines | Author / Planning | Should / P1 / Phase 2 | native build |
| FR-PLAN-104 | Character profiles and relationships | Author / Planning | Should / P1 / Phase 2 | native build |
| FR-PLAN-105 | Locations and world encyclopedia | Author / Planning | Should / P1 / Phase 2 | native build |
| FR-PLAN-106 | Series bible and cross-project knowledge | Author / Planning | Should / P1 / Phase 2 | native build |
| FR-PLAN-107 | Research notes citations and source assets | Author / Planning | Should / P1 / Phase 2 | native build |
| FR-PLAN-108 | Linked notes tags and custom metadata | Author / Planning | Should / P1 / Phase 2 | native build |
| FR-PLAN-109 | Continuity warning review | Author / Planning | Should / P1 / Phase 2 | native build |
| FR-PLAN-110 | Nonfiction outlines and bibliography | Author / Planning | Should / P1 / Phase 2 | native build |
| FR-COL-101 | Coauthor and editor invitation roles | Owner and collaborator / Collaboration | Should / P1 / Phase 2 | native build |
| FR-COL-102 | Concurrent editing and presence | Owner and collaborator / Collaboration | Should / P1 / Phase 2 | native build |
| FR-COL-103 | Threaded comments replies and mentions | Owner and collaborator / Collaboration | Should / P1 / Phase 2 | native build |
| FR-COL-104 | Suggestions and track changes | Owner and collaborator / Collaboration | Should / P1 / Phase 2 | native build |
| FR-COL-105 | Accept reject and compare revisions | Owner and collaborator / Collaboration | Should / P1 / Phase 2 | native build |
| FR-COL-106 | Chapter locks and review checklists | Owner and collaborator / Collaboration | Should / P1 / Phase 2 | native build |
| FR-COL-107 | Expiring beta reader shares | Owner and collaborator / Collaboration | Should / P1 / Phase 2 | native build |
| FR-COL-108 | Watermarkable review copies and feedback | Owner and collaborator / Collaboration | Should / P1 / Phase 2 | native build |
| FR-COL-109 | Activity and notification preferences | Owner and collaborator / Collaboration | Should / P1 / Phase 2 | native build |
| FR-COL-110 | Offline reconnect and conflict recovery | Owner and collaborator / Collaboration | Should / P1 / Phase 2 | native build |
| FR-COL-111 | Permission revocation and audit | Owner and collaborator / Collaboration | Should / P1 / Phase 2 | native build |
| FR-PROD-101 | Daily goals milestones and deadlines | Author / Productivity | Should / P1 / Phase 2 | native build |
| FR-PROD-102 | Writing sprints and focus timers | Author / Productivity | Should / P1 / Phase 2 | native build |
| FR-PROD-103 | Progress and chapter statistics | Author / Productivity | Should / P1 / Phase 2 | native build |
| FR-PROD-104 | Reminder preferences and trends | Author / Productivity | Should / P1 / Phase 2 | native build |
| FR-PROD-105 | Writing groups and challenges | Author / Productivity | Should / P1 / Phase 2 | native build |
| FR-AI-101 | Idea title and outline brainstorming | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-AI-102 | Character and dialogue suggestions | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-AI-103 | Grammar style and readability assistance | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-AI-104 | Summarization and continuity review | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-AI-105 | Citation and translation suggestions | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-AI-106 | Authorized semantic manuscript queries | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-AI-107 | Marketing metadata and alt-text proposals | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-AI-108 | Cover ideation and audio preparation | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-AI-109 | Purpose-specific consent and provider disclosure | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-AI-110 | Human approval and reversible changes | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-AI-111 | Usage metering limits and provenance | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-AI-112 | Provider failure and training prohibition | Author / AI | Could / P2 / Phase 3 | third-party integration |
| FR-ASSET-101 | Cover templates and variants | Author and production designer / Asset production | Should / P1 / Phase 2 | licensed component |
| FR-ASSET-102 | Front back and spine artwork | Author and production designer / Asset production | Should / P1 / Phase 2 | licensed component |
| FR-ASSET-103 | Asset upload and rights evidence | Author and production designer / Asset production | Should / P1 / Phase 2 | licensed component |
| FR-ASSET-104 | Font and image license tracking | Author and production designer / Asset production | Should / P1 / Phase 2 | licensed component |
| FR-ASSET-105 | Image resolution and optimization warnings | Author and production designer / Asset production | Should / P1 / Phase 2 | licensed component |
| FR-ASSET-106 | Captions and alternative text | Author and production designer / Asset production | Should / P1 / Phase 2 | licensed component |
| FR-ASSET-107 | ISBN and barcode placement | Author and production designer / Asset production | Should / P1 / Phase 2 | licensed component |
| FR-ASSET-108 | Designer proofs and author approval | Author and production designer / Asset production | Should / P1 / Phase 2 | licensed component |
| FR-ASSET-109 | Color profiles and imprint marks | Author and production designer / Asset production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-101 | Semantic manuscript to layout separation | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-102 | Interior templates and genre variants | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-103 | Trim margins gutter and columns | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-104 | Headers footers page numbers and breaks | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-105 | Widow orphan and hyphenation controls | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-106 | Chapter openers and ornaments | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-107 | Table of contents and front back matter | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-108 | Font embedding and licensing | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-109 | Screen and print preview | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-110 | Accessible reading order and digital PDF | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-111 | Printer profile bleed crop and color checks | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-FMT-112 | Proof approval and sample comparison | Production designer / Production | Should / P1 / Phase 2 | licensed component |
| FR-CONV-101 | DOCX and Markdown import | Author and production / Conversion | Should / P1 / Phase 2 | licensed component |
| FR-CONV-102 | Plaintext HTML and EPUB import | Author and production / Conversion | Should / P1 / Phase 2 | licensed component |
| FR-CONV-103 | Loss warnings and source recovery | Author and production / Conversion | Should / P1 / Phase 2 | licensed component |
| FR-CONV-104 | DOCX Markdown and plaintext export | Author and production / Conversion | Should / P1 / Phase 2 | licensed component |
| FR-CONV-105 | EPUB and accessible digital PDF export | Author and production / Conversion | Should / P1 / Phase 2 | licensed component |
| FR-CONV-106 | Printer-specific print PDF export | Author and production / Conversion | Should / P1 / Phase 2 | licensed component |
| FR-CONV-107 | Webbook and metadata bundle export | Author and production / Conversion | Should / P1 / Phase 2 | licensed component |
| FR-CONV-108 | Optional XML JATS and ONIX export | Author and production / Conversion | Should / P1 / Phase 2 | licensed component |
| FR-CONV-109 | Optional fixed-layout EPUB and Scrivener investigation | Author and production / Conversion | Should / P1 / Phase 2 | licensed component |
| FR-CONV-110 | Job status retries and checksums | Author and production / Conversion | Should / P1 / Phase 2 | licensed component |
| FR-CONV-111 | Validators preview and reproducible outputs | Author and production / Conversion | Should / P1 / Phase 2 | licensed component |
| FR-VIS-101 | Geometry from trim page count and paper | Author and reader / Visualization | Could / P2 / Phase 3 | licensed component |
| FR-VIS-102 | Front back spine and binding display | Author and reader / Visualization | Could / P2 / Phase 3 | licensed component |
| FR-VIS-103 | Rotate zoom keyboard alternative | Author and reader / Visualization | Could / P2 / Phase 3 | licensed component |
| FR-VIS-104 | Authorized sample page turn | Author and reader / Visualization | Could / P2 / Phase 3 | licensed component |
| FR-VIS-105 | Materials reflections and performance | Author and reader / Visualization | Could / P2 / Phase 3 | licensed component |
| FR-VIS-106 | Enhanced accessible controls and reduced-motion handling for future 3D interactions; the 2D/text baseline remains P0 under FR-CAT-001.2 | Author and reader / Visualization | Could / P2 / Phase 3 | licensed component |
| FR-VIS-107 | Thumbnail and social assets | Author and reader / Visualization | Could / P2 / Phase 3 | licensed component |
| FR-VIS-108 | GLB glTF export and AR feasibility | Author and reader / Visualization | Could / P2 / Phase 3 | licensed component |
| FR-VIS-109 | Immersive story world research | Author and reader / Visualization | Could / P2 / Phase 3 | licensed component |
| FR-EDIT-101 | Eligibility and author declarations | Author and editor / Editorial | Should / P1 / Phase 2 | native build |
| FR-EDIT-102 | Structural checks and manuscript submission | Author and editor / Editorial | Should / P1 / Phase 2 | native build |
| FR-EDIT-103 | Screening and human appeal | Author and editor / Editorial | Should / P1 / Phase 2 | native build |
| FR-EDIT-104 | Reviewer assignment and editorial notes | Author and editor / Editorial | Should / P1 / Phase 2 | native build |
| FR-EDIT-105 | Revise and resubmit decision workflow | Author and editor / Editorial | Should / P1 / Phase 2 | native build |
| FR-EDIT-106 | Developmental editing copyediting and proofreading | Author and editor / Editorial | Should / P1 / Phase 2 | native build |
| FR-EDIT-107 | Typesetting proof and author approval | Author and editor / Editorial | Should / P1 / Phase 2 | native build |
| FR-EDIT-108 | Legal cover and metadata approvals | Author and editor / Editorial | Should / P1 / Phase 2 | native build |
| FR-EDIT-109 | Release scheduling hold and cancellation | Author and editor / Editorial | Should / P1 / Phase 2 | native build |
| FR-EDIT-110 | Correction new edition takedown and reinstatement | Author and editor / Editorial | Should / P1 / Phase 2 | native build |
| FR-RIGHTS-101 | Contributors identity and rights splits | Rights officer / Rights | Should / P1 / Phase 2 | native build |
| FR-RIGHTS-102 | Format language territory channel and term grants | Rights officer / Rights | Should / P1 / Phase 2 | native build |
| FR-RIGHTS-103 | Contract versions and signature trail | Rights officer / Rights | Should / P1 / Phase 2 | native build |
| FR-RIGHTS-104 | Identifiers ISBN and retailer IDs | Rights officer / Rights | Should / P1 / Phase 2 | native build |
| FR-RIGHTS-105 | Classification keywords and accessibility metadata | Rights officer / Rights | Should / P1 / Phase 2 | native build |
| FR-RIGHTS-106 | Publisher imprint and release metadata | Rights officer / Rights | Should / P1 / Phase 2 | native build |
| FR-RIGHTS-107 | Permissions evidence and expiry renewal | Rights officer / Rights | Should / P1 / Phase 2 | native build |
| FR-RIGHTS-108 | Dispute workflow and ONIX integration | Rights officer / Rights | Should / P1 / Phase 2 | native build |
| FR-DIST-101 | Imprint administration and catalog | Publishing staff / Distribution | Should / P1 / Phase 2 | third-party integration |
| FR-DIST-102 | Edition product and scheduling management | Publishing staff / Distribution | Should / P1 / Phase 2 | third-party integration |
| FR-DIST-103 | Print on demand and proof orders | Publishing staff / Distribution | Should / P1 / Phase 2 | third-party integration |
| FR-DIST-104 | Channel availability and embargoes | Publishing staff / Distribution | Should / P1 / Phase 2 | third-party integration |
| FR-DIST-105 | Metadata synchronization and vendor errors | Publishing staff / Distribution | Should / P1 / Phase 2 | third-party integration |
| FR-DIST-106 | Returns and chargeback reconciliation | Publishing staff / Distribution | Should / P1 / Phase 2 | third-party integration |
| FR-DIST-107 | Vendor reports and settlement mapping | Publishing staff / Distribution | Should / P1 / Phase 2 | third-party integration |
| FR-STORE-101 | Public catalog category search and filters | Reader / Commerce | Should / P1 / Phase 2 | native build |
| FR-STORE-102 | Author series and book detail pages | Reader / Commerce | Should / P1 / Phase 2 | native build |
| FR-STORE-103 | Samples and accessible preview | Reader / Commerce | Should / P1 / Phase 2 | native build |
| FR-STORE-104 | Prices coupons and currency display | Reader / Commerce | Should / P1 / Phase 2 | native build |
| FR-STORE-105 | Cart checkout and confirmed purchase | Reader / Commerce | Should / P1 / Phase 2 | native build |
| FR-STORE-106 | Licensed delivery and customer library | Reader / Commerce | Should / P1 / Phase 2 | native build |
| FR-STORE-107 | Web reader themes typography and bookmarks | Reader / Commerce | Should / P1 / Phase 2 | native build |
| FR-STORE-108 | Highlights notes and reading progress | Reader / Commerce | Should / P1 / Phase 2 | native build |
| FR-STORE-109 | Ratings moderation and recommendations | Reader / Commerce | Should / P1 / Phase 2 | native build |
| FR-STORE-110 | Gifts bundles wishlists and refunds | Reader / Commerce | Should / P1 / Phase 2 | native build |
| FR-STORE-111 | Offline reading and support workflow | Reader / Commerce | Should / P1 / Phase 2 | native build |
| FR-FINANCE-101 | Author plans and service revenue share | Finance and author / Finance | Should / P1 / Phase 2 | native build |
| FR-FINANCE-102 | Royalty rules by contributor channel and format | Finance and author / Finance | Should / P1 / Phase 2 | native build |
| FR-FINANCE-103 | Advances recoupment and reserves | Finance and author / Finance | Should / P1 / Phase 2 | native build |
| FR-FINANCE-104 | Earned cleared and payable balances | Finance and author / Finance | Should / P1 / Phase 2 | native build |
| FR-FINANCE-105 | Sales refunds chargebacks and adjustments | Finance and author / Finance | Should / P1 / Phase 2 | native build |
| FR-FINANCE-106 | Balanced ledger and reconciliation | Finance and author / Finance | Should / P1 / Phase 2 | native build |
| FR-FINANCE-107 | Payout scheduling thresholds and failures | Finance and author / Finance | Should / P1 / Phase 2 | native build |
| FR-FINANCE-108 | Invoices receipts and statement export | Finance and author / Finance | Should / P1 / Phase 2 | native build |
| FR-FINANCE-109 | Tax currency exchange and dispute audit | Finance and author / Finance | Should / P1 / Phase 2 | native build |
| FR-GROWTH-101 | Author pages SEO and structured data | Author and growth team / Growth | Should / P1 / Phase 2 | native build |
| FR-GROWTH-102 | Book launch kits social sharing and previews | Author and growth team / Growth | Should / P1 / Phase 2 | native build |
| FR-GROWTH-103 | Consent-based newsletters and lists | Author and growth team / Growth | Should / P1 / Phase 2 | native build |
| FR-GROWTH-104 | Preorders and advanced review copies | Author and growth team / Growth | Should / P1 / Phase 2 | native build |
| FR-GROWTH-105 | Referrals and promotional campaigns | Author and growth team / Growth | Should / P1 / Phase 2 | native build |
| FR-GROWTH-106 | Writing groups clubs and moderation | Author and growth team / Growth | Should / P1 / Phase 2 | native build |
| FR-GROWTH-107 | Discovery collections and recommendations | Author and growth team / Growth | Should / P1 / Phase 2 | native build |
| FR-GROWTH-108 | Funnel analytics and customer support | Author and growth team / Growth | Should / P1 / Phase 2 | native build |
| FR-ADMIN-101 | Feature flags and plan configuration | Platform operator / Operations | Should / P1 / Phase 2 | native build |
| FR-ADMIN-102 | Moderation complaints and takedowns | Platform operator / Operations | Should / P1 / Phase 2 | native build |
| FR-ADMIN-103 | Administrative roles and audited support access | Platform operator / Operations | Should / P1 / Phase 2 | native build |
| FR-ADMIN-104 | Fraud controls and abuse limits | Platform operator / Operations | Should / P1 / Phase 2 | native build |
| FR-ADMIN-105 | Backup export deletion and retention | Platform operator / Operations | Should / P1 / Phase 2 | native build |
| FR-ADMIN-106 | Subscription and service configuration | Platform operator / Operations | Should / P1 / Phase 2 | native build |
| FR-ADMIN-107 | Incident response and status reporting | Platform operator / Operations | Should / P1 / Phase 2 | native build |
| FR-ADMIN-108 | Search management and integration health | Platform operator / Operations | Should / P1 / Phase 2 | native build |
| FR-ADMIN-109 | Legal holds and security dashboards | Platform operator / Operations | Should / P1 / Phase 2 | native build |
| FR-VERT-101 | Audiobook production and voice narration | Author and institutional publisher / Product | Won't / P3 / research | defer |
| FR-VERT-102 | Translation and localization services | Author and institutional publisher / Product | Won't / P3 / research | defer |
| FR-VERT-103 | Comics graphic novels and childrens books | Author and institutional publisher / Product | Won't / P3 / research | defer |
| FR-VERT-104 | Textbook interactions equations and citations | Author and institutional publisher / Product | Won't / P3 / research | defer |
| FR-VERT-105 | Academic review and scholarly metadata | Author and institutional publisher / Product | Won't / P3 / research | defer |
| FR-VERT-106 | Multimedia and interactive fiction | Author and institutional publisher / Product | Won't / P3 / research | defer |
| FR-VERT-107 | Library lending and subscription reading | Author and institutional publisher / Product | Won't / P3 / research | defer |
| FR-VERT-108 | Collaborative anthologies and revenue splits | Author and institutional publisher / Product | Won't / P3 / research | defer |
| FR-VERT-109 | Institutional white label and B2B APIs | Author and institutional publisher / Product | Won't / P3 / research | defer |
| FR-VERT-110 | Service marketplaces and immersive worlds | Author and institutional publisher / Product | Won't / P3 / research | defer |
