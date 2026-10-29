# SUPER-MEGA MASTER PROMPT
## Integrated Product, Publishing, UX, Architecture, Engineering, and Delivery Documentation

**Project:** Cloud-based Author Studio + Digital Publishing House + Book Marketplace  
**Prompt version:** 1.0 (prepared October 29, 2026)  
**Purpose:** Paste everything between `BEGIN MASTER PROMPT` and `END MASTER PROMPT` into an AI system with long-context, research, and/or file-generation capabilities. Attach any existing RFPs, competitor spreadsheets, stakeholder interviews, brand guidelines, and technical constraints. Generate documentation, not a working production application, unless separately instructed.

---

# BEGIN MASTER PROMPT

## 0. Your mission and operating contract

Act as a coordinated, senior cross-functional **product development and digital publishing organization**, not as a single generalist. Your mission is to produce an **implementation-ready, procurement-ready, design-ready and QA-verifiable documentation package** for a multi-tenant, web-based authoring and publishing platform.

The platform is simultaneously:
1. **Author Studio:** the trusted place where writers plan, draft, store, revise, collaborate, manage research, format, and export manuscripts.
2. **Publishing Operating System:** the workflow for submissions, editors, professional book production, rights, metadata, release approvals, distribution, contracts, royalties, and finances.
3. **Book Marketplace and Reader:** a discovery, purchase, library, preview, web-reading, and author-marketing experience, operating as an online publishing house.
4. **Visualization and Format Studio:** an accessible multi-format book production pipeline with attractive 3D previews of real book formats; optional future interactive/immersive experiences.

The business aims to attract a large author base, encourage a high volume of high-quality manuscripts, convert suitable projects into publishable editions, sell and distribute books, and establish enduring trust with authors and readers. **Do not confuse a large volume of book uploads with a large volume of legally compliant, quality-controlled, publishable titles.** Specify both conversion and quality gates.

**Non-negotiable principles:**
- Author trust and ownership first. Private manuscripts must never be searchable by the public or used for model training by default. Explicit, purpose-specific consent is required for any exceptional data use.
- Retain author portability. Authors must be able to export their content and relevant metadata in documented formats even when they do not publish on the marketplace.
- Distinguish a draft, manuscript revision, submission, accepted title, published edition, format-specific rendition, catalog listing, licensed product, and customer purchase. Do not collapse them into one `Book` table or one workflow state.
- Build for a configurable, jurisdiction-dependent publishing business; do not assume the platform automatically owns an author's copyright or exclusive distribution rights.
- Design accessibility, multilingual support (including RTL and bidirectional text), security, financial auditability, and recovery into architecture from the start.
- Avoid an unbounded MVP. Document the **full feature universe**, then explicitly select an achievable first release with clear dependencies and deferred capabilities.
- Treat AI and 3D as value-adding modules, not excuses to jeopardize manuscript reliability, print quality, or ordinary usability.
- Clearly distinguish **verified requirement**, **stakeholder assumption**, **industry/competitor evidence**, **design proposal**, and **legal/technical decision pending**.
- Never manufacture interviews, product test results, competitor feature absences, standards compliance, API availability, vendor prices, market-size figures, or conversion rates.

**Work method:** First produce a decision-and-assumptions register. When information is missing, choose a sensible provisional default, mark it `ASSUMPTION — VALIDATE`, explain its impact, and proceed. Ask only questions that would materially reverse the architecture, legal model, or MVP scope. If live browsing is unavailable, tag claims `NOT LIVE-VERIFIED` instead of inventing findings. If file creation is available, write real files with the paths named below; otherwise produce self-contained Markdown sections in a stable numbered sequence. Never say documents were created unless they actually exist.

## 1. Role-based expert review council

Simulate the following 22 accountable perspectives. They may be one combined reasoning system, but every artifact must show its **authoring role, consulting roles, reviewer, approver, and decision owner**. Do not imply actual human legal, financial, security, or editorial approval occurred.

**Business and discovery**
1. **Executive Sponsor / Publishing Director** — publisher strategy, imprint policy, business case, publishing selection criteria, financial guardrails.
2. **Chief Product Manager / Product Owner** — product vision, outcomes, priorities, discovery, roadmap, release acceptance.
3. **Senior Business Analyst / Requirements Engineer** — SRS, user stories, rules, traceability, ambiguities, acceptance criteria.
4. **UX Researcher / Service Designer** — personas, JTBD, author and reader research, workflows, funnel research, competitive evidence.
5. **Editorial & Publishing Operations Lead** — submissions, editorial review, developmental editing, copyediting, proofing, production, book launches.
6. **Book Designer / Print Production Expert** — typesetting, trim, binding, paper, cover, bleed, proofs, printer-specific output rules.

**Design and engineering**
7. **Lead UX/UI and Design-System Designer** — journeys, information architecture, mobile/responsive UI, accessibility patterns, visual language.
8. **Accessibility and Internationalization Specialist** — WCAG, accessible EPUB, bidirectional content, language/script support, assistive tech.
9. **Principal Software / Solution Architect** — domain decomposition, quality attributes, C4/UML, ADRs, tradeoffs, performance, scale.
10. **Frontend Engineering Lead** — app shell, author studio, bookstore, reader, state management, rendering, browser compatibility.
11. **Structured Document & Real-Time Collaboration Engineer** — editor document schema, selection behavior, CRDT/OT analysis, comments, versioning, autosave and offline conflicts.
12. **Backend/API Engineering Lead** — application services, business invariants, authz, API contracts, persistence, transactions, jobs.
13. **Publishing Conversion / Typesetting Engineer** — imports, canonical model transformations, EPUB, PDF/X, PDF/UA, export quality gates.
14. **3D/Web Graphics Engineer** — browser 3D, realistic book mockups, textures, dimensions, fallback, device performance, optional AR.
15. **AI/ML and Responsible AI Engineer** — opt-in assistance, model architecture, hallucination controls, provenance, evaluations and cost.
16. **Search / Data / Analytics Engineer** — indexing boundaries, metadata, recommendation systems, event definitions, privacy-preserving BI.
17. **Commerce / Integration Engineering Lead** — payment providers, print-on-demand, distributors, email, content delivery, webhook reliability.

**Assurance, operations, and growth**
18. **Finance / Royalty Accounting Specialist** — contracts-to-entitlements, royalties, ledger, refunds, settlements, tax/FX assumptions.
19. **Security, Privacy, IP and Legal Advisory Team** — threat model, privacy, licensing, content moderation, copyright, sanctions/territory issues; flag legal review rather than asserting legal conclusions.
20. **DevOps / SRE Lead** — environments, CI/CD, infrastructure-as-code, observability, backup/restore, incident response, cost.
21. **QA / Test Automation and Quality Engineering Lead** — risk-based quality, test architecture, E2E, accessibility, data migration, formatting accuracy, regression, release gates.
22. **Growth / SEO / Community and Customer Success Lead** — author activation, retention, community, catalog discovery, conversion, support workflows.

Also explicitly assign **delivery management, content/design writing, and technical documentation maintenance** responsibilities (dedicated or shared), including version control, approval workflow, glossary governance, and changelog management.

**Role checkpoints:** At the end of each documentation phase, produce a cross-role review table: role, concerns raised, changes made, residual risks, approving stakeholder required. All legal advice, tax determinations, production print samples, security certifications, and accessibility conformance claims require real-world verification.

## 2. Starting assumptions to challenge and validate

Unless provided otherwise:
- Web-first SaaS, cloud-hosted, responsive on desktop/tablet/mobile; offline-capable drafting is a considered enhancement, not guaranteed for MVP.
- International ambition; English is the initial user-interface language, but architecture must support localization, RTL scripts, Unicode, international names, and cross-language books.
- Marketplace and publisher operate initially with one imprint and can later support multiple imprints and organization tenants.
- Book categories initially prioritize **text-centric fiction and nonfiction**. Children's picture books, complex textbooks, comics, heavily illustrated books, scientific math-heavy books, and audiobooks require distinct capability/effort assessments.
- Authors retain ownership of their submitted text unless separately negotiated; rights for each edition, territory, language, format, and distribution channel are explicit.
- Multiple publishing models must be compared: curated publisher, author self-service marketplace, hybrid, and third-party distribution. Recommend one initial operating model and state why.
- 3D initially means a faithful interactive **physical-book visualization** (front, back, spine, thickness, materials, rotate/zoom, optional animated page turn). Immersive story-world 3D is a separate discovery track and cannot be inferred from the main requirement.
- Author manuscripts and customer purchases may contain personal or sensitive information. Implement least-privilege access and lawful retention policies.
- Currency, payment and taxation depend on launch markets; do not assume payment platforms, payout rails, ISBN agencies, or print partners are available everywhere.
- Costs, staffing, performance targets, project duration, demand forecasts, and adoption metrics are estimates until researched and benchmarked.

Produce a **Decision Register** (`DEC-###`), **Assumption Register** (`ASM-###`), **Open Questions** (`OQ-###`), **Risks** (`RSK-###`), and a glossary in the first batch.

## 3. Complete feature inventory — cover every area, do not imply all belong in MVP

For every feature: create an `FR-<DOMAIN>-###` record with user, value, business rule, priority, lifecycle, dependencies, role/permission, UX entry point, main/alternate/error flows, acceptance tests, telemetry, compliance implications, and a source status (`REQUIRED`, `COMPETITOR-VERIFIED`, `PROPOSED`, `ASSUMPTION`). Use MoSCoW and `P0/P1/P2/P3` plus MVP/Phase 2/Phase 3 placement. Classify `native build`, `third-party integration`, `licensed component`, or `defer` with reasons.

### A. Identity, trust, accounts, and workspace
Signup/login, OAuth/passkeys where appropriate, MFA for privileged roles, email verification, recovery, author pseudonyms and pen names, public versus private profile, verified publisher identity, organizations/imprints, workspaces, project folders/tags, memberships/invitations, fine-grained project/editor/read-only permissions, subscriptions and quotas, team management, audit history, account deletion/export, data portability, legal agreements, consent versions, notifications and privacy controls.

### B. Project setup, drafting, and structured manuscript editing
New-book wizard; genre and project-type templates; titles/subtitles; books/parts/chapters/scenes; drag-and-drop structure; collapsible navigator; headings, emphasis, block quotes, lists, scene breaks, links, tables, images, citations, endnotes, footnotes, glossary, appendices and front/back matter; markdown shortcuts; keyboard shortcuts; custom styles versus semantic roles; typography controls; find/replace across projects; cross-references; spellchecking; dictionaries; autocorrect; focus and distraction-free modes; word/character/page counts; reading-time approximations; search; copy/paste fidelity; undo/redo; version snapshots; autosave status and acknowledged-save guarantees; import errors; writing on mobile; large manuscripts; right-to-left scripts, CJK, IMEs, diacritics; editor accessibility; fallback and recovery behavior.

### C. Story planning and research
Scene/plot boards, beat sheets, index cards, narrative arcs, three-act and other structure templates, color-coded timelines, parallel story lines, character profiles and relationships, locations, settings, world-building encyclopedia, series bible, series timelines, research boards, citations, sources, images, inspiration boards, notes linked to chapters, custom metadata, tags and cross-project knowledge reuse, continuity and contradiction warnings; non-fiction outlines and research bibliographies as alternative flows.

### D. Collaboration and professional editing
Coauthor invites, differentiated roles (owner/coauthor/editor/proofreader/beta reader), simultaneous editing, presence/cursors, comments/threads/replies/mentions, suggestion mode, track changes, compare versions, approve/reject edits, chapter locks where helpful, review checklists, comment resolution, beta-reader previews, expiring share links, watermarkable review copies, private feedback forms, activity feeds, notification preferences, editorial handoff, offline reconnection and merge, permission revocation and author audit visibility.

### E. Writing productivity
Goal setting, daily targets, milestones, deadline calendar, writing sprints, streaks, focus timers, reminders, project progress, per-chapter statistics, reading-time and word-count trends, personalized dashboard, writing habit reports, privacy-conscious motivational features, optional writing groups, challenges, beta communities and mentor services.

### F. AI-assisted authoring (optional, explicit consent)
Idea and title brainstorming, outline generation, character development, editing suggestions, grammar/style, readability, summarization, dialogue checks, consistency, continuity, citation-format suggestions, multilingual proofreading, translation assistance, story analysis, semantic search over authorized manuscript content, natural-language project queries, marketing metadata and blurb drafts, alt-text proposals, book-cover ideation, TTS/audio preparation, human approval, reversible suggestion application, usage metering, cost and limits, model selection policy, provider failure modes, copyrighted-material precautions, transparent AI involvement, exportable provenance and no-training-by-default guarantees. Distinguish assistive editing from autonomous ghostwriting, and do not present generated references as verified facts.

### G. Asset and cover production
Cover designer or integration, front/back/spine templates, artwork/image assets, licensed fonts and images, rights documentation, image dimensions and resolution warnings, alt text, captions, image optimization, preflight, logos and imprint marks, cover variants/A-B test concepts, ISBN/barcode placement and requirements, collaborative designer proofs, author approval, watermark/preview protection, color-profile handling.

### H. Professional book formatting
Separation of manuscript semantics from page appearance; interior templates; layout variants by genre; trim size; page size; margins; gutters; columns; running heads/feet; page numbering; widow/orphan controls; hyphenation; chapter openers; drop caps; ornamental breaks; table of contents; font embedding/licensing; page breaks; front/back matter; cover and jacket; print previews; bleed/crop marks as printer-required; paper/binding assumptions; small-screen and large-screen previews; accessible semantic reading order; color versus monochrome requirements; PDF/X and PDF/UA distinction; printer-specific preflight and manual proof approval.

### I. Import, conversion, and delivery
Imports: DOCX, Markdown, plaintext, HTML or EPUB when licensed/feasible; optional Scrivener project import after research and licensing review. Do not promise reliable PDF-to-editable manuscript conversion without an explicit quality boundary. Exports: DOCX, Markdown/plain text, EPUB 3.x, webbook/HTML, accessible digital PDF, print-ready PDF (specific printer preset), optional fixed-layout EPUB, MOBI only if justified by current channel requirements, XML/JATS/ONIX where relevant, print assets, metadata bundle. Produce target-format compatibility matrix, semantic transformations, validator output, preview thumbnails, conversion job tracking/retry, sample comparisons, warnings, source maps where viable, idempotent job handling, and reproducibility of approved published renditions.

### J. 3D book modeling and immersive previews
Book model from actual trim, page count, paper thickness, cover geometry and binding assumptions; 3D front/back/spine display; interactive rotate/zoom; page-turn preview for authorized sample pages; cover materials/reflection if performance allows; thumbnail and social share assets; 3D previews in Studio and store; web rendering and keyboard alternatives; accessible textual equivalent; reduced-motion support; image fallback; mobile performance; optional downloadable GLB/glTF assets; optional AR via supported devices; separate feasibility track for illustrated environments/interactive story-worlds. 3D must never misrepresent actual manufacturing dimensions or visual output.

### K. Editorial production and manuscript submission
Submit for consideration, eligibility, automated structural checks, author declarations, plagiarism/duplicate-risk screening with appeals and careful human assessment, reviewer assignment, editorial notes, revise-and-resubmit, acceptance/rejection reasons, developmental editing, copyediting, proofreading, typesetting, author proof approval, legal review, cover approval, final metadata approval, release scheduling, internal SLAs, editorial checklists, permissions, escalation, embargo and release hold, cancellation, unpublishing, corrections/new editions, takedown and reinstatement.

### L. Rights, contracts, and bibliographic metadata
Author identity and contributors; rights splits; license types; exclusivity/nonexclusivity; languages, territories, formats, channels and term; contract versioning/e-signature integration; approval trail; ISBN per edition/format where applicable, ASIN and retailer IDs where assigned, DOI for eligible scholarly material, publisher/imprint, classification, keywords, categories, BISAC/THEMA where applicable, ONIX exports/integrations, descriptions, accessibility metadata, release date, edition/version relations, translation rights, permissions records, rights expiry/renewal and dispute procedures.

### M. Publisher operations and distribution
Imprint administration; acquisition pipeline and work queues; catalog; edition/product management; publication scheduling; multi-channel delivery; print-on-demand/vendor integration; proof ordering and status; wholesale/retail metadata synchronization; distribution channel mapping; format/channel availability; territories and embargoes; error reconciliation; returns/chargebacks; vendor reports; channel payout mapping; manual review of unverified partner capability; support tickets and publishing release checklist.

### N. Online bookstore and reader experience
Public catalog, categories/genres, search and facets, autocomplete, author pages, series pages, descriptions and previews, sample chapters, 2D/3D covers, price/promotions/coupons, tax and currency display, cart/checkout or direct purchase, payment confirmation, licensed digital delivery, customer library, browser reader with typography and theme preferences, text-to-speech/accessibility features, bookmarks, highlights/notes, purchase history, reading progress sync, offline access feasibility, ratings/reviews with moderation, recommendations, gift and bundle options, wishlists, returns/refunds and customer support. Separate public discovery index from private manuscript search.

### O. Author monetization and financial integrity
Paid author tiers, free tier, subscription plans, usage-based AI/conversion extras if justified, service marketplace and revenue share, royalties by title/contributor/format/channel/territory, advances and recoupment if the business model warrants them, earned versus payable amounts, royalty ledger, payout schedule, minimums and thresholds, currency/tax handling, reserves/holdbacks where lawful and disclosed, customer refunds/chargebacks, invoice/receipt export, sales analytics, reconciliation, payout failures, dispute trail, complete financial auditability and idempotent settlement jobs. Never treat a nonfinancial dashboard total as the authoritative ledger.

### P. Marketing, community and growth
Author landing pages, SEO and structured data, social sharing, book launch kits, newsletters and mailing-list consent, preorders where supported, advanced reader copies (ARCs), beta readers, referral program, writing groups, book clubs, editorial marketplace, user-generated community moderation, promotions, storefront analytics, conversion funnels, retention/activation reports, reader recommendations, featured collections, review requests, loyalty proposals, customer support/knowledge base and fraud/abuse limits.

### Q. Platform administration and operations
Feature flags, configuration per plan/imprint/tenant, moderation queues, complaint/takedown workflow, admin RBAC, fraud signals, user support impersonation protections, audit events, content backup/export/deletion, subscription management, customer service tools, abuse prevention, reporting, search index management, data retention jobs, disaster-recovery tooling, incident management, status reporting, legal hold, compliance audit, vendor integration status and SLO dashboards.

### R. Advanced verticals to research separately
Audiobooks/voice narration, multilingual translation and localization services, comics and graphic novels, children's books, textbook learning interactions, equation/math support, references and citation management, academic peer review, multimedia books, interactive fiction/branching narrative, subscription reading plans, library lending, classrooms, collaborative anthologies and revenue splits, white-label institutional publishing, marketplaces for editors/designers/narrators, B2B publishing APIs, immersive 3D worlds/AR. Document each as optional with new technical, rights, accessibility, and economic implications.

## 4. Competitive intelligence: evidence-based, not speculative

Benchmark at minimum the following **categories and named examples**, adding current relevant challengers discovered through research:
- Authoring/workflow: Scrivener, Reedsy Studio, Atticus, Dabble, Novlr, LivingWriter.
- Planning/worldbuilding: Plottr, Campfire, World Anvil, Novelcrafter.
- AI/editorial: Sudowrite, ProWritingAid, AutoCrit, Grammarly, Hemingway.
- Book design and formats: Vellum, Pressbooks, Adobe InDesign, Kotobee Author, Book Creator.
- Publishing/distribution: Amazon KDP, Draft2Digital, IngramSpark, PublishDrive, StreetLib, Lulu.
- Reader growth/marketplaces: Reedsy Marketplace, BookFunnel, StoryOrigin, Wattpad, Inkitt.
- 3D/interactive: Book Brush, Publuu, Flipsnack, plus comparable contemporary products.

For each product and capability, capture: source URL, source type (official documentation/demo/independent hands-on review), date last checked, exact capability and edition/plan constraints, supported platforms, exports, collaboration, publishing/distribution scope, accessibility, AI policy, business-model pricing (if verified), documented limitation, and confidence. Classification MUST use **YES VERIFIED / PARTIAL VERIFIED / NO EXPLICITLY CONFIRMED / NOT FOUND IN PUBLIC DOCUMENTATION / UNKNOWN / NOT APPLICABLE**. `NOT FOUND` is **not** proof that the feature is absent. When no up-to-date evidence is available, mark `RESEARCH NEEDED`; never fabricate negative features.

Produce the following outputs:
1. Competitor-by-feature matrix with evidence links and confidence.
2. Feature union (all distinct capabilities demonstrated by products), with duplicates normalized.
3. Proven unmet-needs / opportunity list, separated from speculative innovation hypotheses.
4. Top ten friction points in the cross-product writer-to-publisher journey, labeled as research hypotheses if not interview-validated.
5. Build / integrate / partner / deliberately omit analysis, including costs and interoperability implications.
6. Competitive parity targets vs meaningful differentiation; do **not** blindly adopt features simply because they exist.

## 5. Product strategy, experience, and business analysis

Create a rigorous product vision and business model with target segments: hobbyist authors, professional fiction authors, nonfiction writers, collaborative authors, freelance editors, publishing staff, cover designers, beta readers, individual readers, and institutional publishers (later). Prioritize segments with evidence and cost-to-serve.

Compare curated publishing, open self-publishing marketplace, and hybrid models; document legal, catalog-quality, support, and royalty implications. Describe product-led author acquisition through free trustworthy drafting/storage, valuable export even without publishing, accessible onboarding, templates, writing communities, referral and educational content. Define first-author success, time to first chapter, completion metrics, submitted manuscript quality rate, acceptance rate, publishable output, purchases, royalties and author retention. Define guardrail metrics (lost text, support volume, rejected print proofs, unlicensed content, fraud, accessibility failures, reader refunds).

Produce personas and Jobs-to-be-Done; complete user journeys for new author, migrating author, coauthor, editor, publishing director, design/production specialist, buyer/reader, finance admin and support agent. Map frontstage/backstage actions and third-party dependencies. Define high-risk service recovery: connectivity failure, import failure, editor merge conflict, rejected manuscript, rights conflict, invalid EPUB, print proof error, payment dispute and failed royalty transfer.

Create an **MVP recommendation** with explicit exclusions. As a provisional baseline:
- **P0 Launch foundation:** secure accounts and workspace; excellent structured editor; reliable autosave/recovery/version snapshots; project/chapter organization; essential DOCX/Markdown import and exports; templates; submission/editorial queue; accessibility-aware EPUB and print PDF pipeline for text-centric books; basic book cover metadata; 2D plus realistic 3D cover mockup; public catalog/preview; initial reader/purchase model; basic rights tracking; traceable royalty accounting; publishing/admin controls; QA/security/backup.
- **P1 Professional expansion:** advanced story planning, collaboration/track changes, design controls, POD/distribution partnerships, service marketplace, marketing workflows, refined royalties, complex formats, author analytics, richer reader library and recommendation features.
- **P2 Differentiators:** consent-governed AI agents and manuscript analysis, multimodal authoring, advanced 3D/page animations/AR, audio and translation workflows, interactive educational books, institution/multi-imprint features, extensible ecosystem and APIs.
Validate the ordering via a RICE/WSJF or other disclosed prioritization model; identify dependencies that force some features earlier.

## 6. Documentation package to produce

Deliver a cohesive, numbered, cross-referenced repository of Markdown source files and diagram source files. Include a README/manifest listing actual files, versions and completion status. The following inventory is the **minimum**; extend where justified:

```text
/docs
  README.md
  00-governance/
    01-scope-and-assumptions.md
    02-decisions-and-open-questions.md
    03-glossary-and-ubiquitous-language.md
    04-stakeholders-roles-raci.md
    05-document-control-and-traceability.md
  01-discovery-strategy/
    01-vision-value-proposition-and-positioning.md
    02-market-and-competitor-evidence-matrix.md
    03-personas-jtbd-and-research-plan.md
    04-business-model-and-unit-economics.md
    05-service-blueprints-and-user-journeys.md
    06-product-kpis-and-analytics-plan.md
  02-requirements/
    01-complete-prd.md
    02-system-requirements-specification-srs.md
    03-feature-catalog-and-prioritization.md
    04-epics-user-stories-and-gherkin.md
    05-business-rules-and-permissions.md
    06-nonfunctional-requirements-and-slos.md
    07-error-recovery-and-edge-cases.md
  03-experience-design/
    01-information-architecture-and-sitemaps.md
    02-navigation-and-journey-flows.md
    03-screen-inventory-and-screen-specs.md
    04-design-system-and-design-tokens.md
    05-interaction-and-content-guidelines.md
    06-accessibility-and-i18n-specification.md
    07-wireframes-and-prototype-checklist.md
  04-publishing-domain/
    01-editorial-publishing-workflow.md
    02-structured-manuscript-and-asset-model.md
    03-formats-typography-and-conversion.md
    04-print-preflight-and-proofing.md
    05-rights-contracts-and-metadata.md
    06-distribution-commerce-and-royalties.md
    07-three-d-visualization-and-asset-pipeline.md
  05-software-architecture/
    01-architecture-vision-and-quality-attributes.md
    02-domain-boundaries-and-context-map.md
    03-c4-context-container-component.md
    04-uml-and-erd-index.md
    05-database-and-migrations.md
    06-api-contracts-and-event-schemas.md
    07-document-sync-autosave-and-conflict-handling.md
    08-export-and-async-job-architecture.md
    09-data-privacy-security-and-threat-model.md
    10-integration-architecture.md
    11-architecture-decision-records.md
  06-engineering-handbook/
    01-reference-stack-and-tradeoffs.md
    02-repository-module-boundaries.md
    03-clean-code-and-coding-standards.md
    04-coding-patterns-and-anti-patterns.md
    05-example-code-and-contracts.md
    06-git-pr-review-and-definition-of-done.md
    07-database-schema-and-versioning-standards.md
    08-ai-coding-agent-instructions.md
  07-assurance/
    01-test-strategy-and-quality-gates.md
    02-functional-integration-e2e-test-catalog.md
    03-book-format-and-print-fidelity-test-plan.md
    04-security-privacy-and-abuse-test-plan.md
    05-accessibility-localization-and-browser-matrix.md
    06-performance-load-resilience-and-dr-plan.md
    07-requirements-to-test-traceability.md
  08-operations/
    01-cloud-deployment-and-environments.md
    02-cicd-and-supply-chain-security.md
    03-observability-slos-and-incident-response.md
    04-backup-restore-and-business-continuity.md
    05-data-retention-and-customer-support-runbooks.md
    06-capacity-cost-and-finops.md
  09-delivery-and-procurement/
    01-rfp-and-vendor-response-template.md
    02-scope-phases-roadmap-and-dependencies.md
    03-team-plan-estimates-and-critical-path.md
    04-risk-register-and-mitigation.md
    05-acceptance-milestones-and-exit-criteria.md
    06-pilot-launch-growth-and-operations-readiness.md
  diagrams/
    [descriptive .puml and/or .mmd files for every indexed diagram]
  contracts/
    openapi.yaml
    asyncapi.yaml
    [versioned schema examples]
  samples/
    [validated feature, test, ADR, event and component examples]
```

Every document MUST contain: document ID/title, version/date, status (draft/reviewed/approved—not falsely approved), accountable role, consulted roles, assumptions, related requirements, table of contents if long, substantive detail, unresolved questions, and references. Ensure each file's claims agree with every other file. No placeholders such as `TBD` without corresponding recorded owner and decision due milestone.

## 7. PRD, SRS, feature catalog and precise requirements

Produce one-page executive summary plus full PRD: problem, users, goals, out-of-scope, rationale, measured outcomes, assumptions, differentiators, constraints and launch criteria. SRS must follow an ISO/IEC/IEEE 29148-style discipline where practical: uniquely identified and atomic requirements, unambiguous language, verifiability, consistency, traceability, rationale and priority. Do not claim formal standard certification merely for adopting its structure.

For **every feature** provide:
- Requirement ID, title, persona, value proposition, benefit/evidence, priority, release, domain owner, dependencies, estimated complexity band and confidence.
- Preconditions; happy path; alternate path; error conditions; offline/slow network/permissions/race conditions; accessibility and i18n requirements; data retention and privacy.
- UI entry points, loading/empty/success/error/disabled states, exact actionable feedback text, responsive and keyboard behavior, analytics events.
- Input constraints, schema and validation; API operations and authorization checks; failure/retry behavior; audit events.
- Minimum three concrete `Given / When / Then` acceptance scenarios for high-risk requirements, including negative and boundary cases.
- Manual end-user test case and automated test location/level; release acceptance evidence and cross-links.

For cross-functional processes, specify BPMN-like narrative or activity diagram plus state machine, authorized transitions, invariants, compensation actions and notification rules. Be especially rigorous about manuscript autosave, revision restore, edition publication, refunds and royalty posting.

## 8. UX/UI and design-system requirements

Create an information architecture for four separate but coherent workspaces: **Author**, **Publisher/Editorial**, **Reader/Bookstore**, and **Platform Admin/Finance**. Describe global navigation, scoped project navigation, content hierarchy, breadcrumbs, search, command palette, notifications, and mobile breakpoints. Name all screens and routes, with screen IDs `SCR-###` and dependencies; avoid designing publishing controls into the ordinary reader interface.

Required screens include at least: landing page, pricing/onboarding, login, author dashboard/library, project wizard, project overview, rich manuscript editor, outline/plot board, character/research database, collaboration/comments, writing goals/statistics, import/export center, format designer, cover designer, 3D book viewer, submission wizard, manuscript status, editor work queue, editorial review/track changes, proof approval, rights/contracts, metadata/ISBN, release planning, publisher catalog, public store listing, book details/3D preview, checkout, reader library, web reader, ratings/reviews, author sales/royalty dashboard, finance payouts, support/takedown, permission management, and platform administration.

For each screen create a **screen contract**: goal, persona, data, components, hierarchy, navigation, sample labels, responsive layout, keyboard/focus order, WCAG considerations, empty/loading/error/success states, destructive action confirmation, validation, telemetry, permissions, design tokens and testable acceptance criteria. Specify essential design tokens (typography, spacing, color semantic roles, breakpoints, radii, shadows, focus states, motion). Include a11y contrast, touch target, reduced-motion and screen-reader considerations. Support right-to-left both in UI and independent document direction; do not confuse RTL UI with bi-directional editorial content.

Provide textual low-fidelity wireframes and mermaid journey/flow diagrams; identify what must be mocked in Figma or another prototyping tool. Do not claim that an actual prototype has been created unless it has. Include usability test tasks and success metrics, and a copy style guide that is supportive of authors without manipulating them into publishing.

## 9. Architecture and implementation rigor

Evaluate at least three viable architecture directions: modular monolith, service-oriented modular application, and microservices. Recommend an initial solution based on team size, deployment complexity, authoring consistency, transaction needs, and likely traffic; include scaling/extraction triggers. **A modular monolith with isolated asynchronous conversion jobs is a reasonable hypothesis, not an unquestioned mandate.** Document tradeoffs and ADRs.

Analyze the following bounded contexts: Identity & Organizations, Author Projects, Structured Documents, Collaborative Editing, Asset Storage, Formatting/Conversion, Editorial Pipeline, Rights & Contracts, Catalog & Editions, Distribution, Storefront & Reader, Commerce/Payments, Royalty Ledger, Community/Marketing, Notifications, Search/Analytics, Moderation/Trust, and Platform Administration. Identify aggregates, invariants, ownership, transactional consistency requirements, eventual-consistency boundaries, domain events, and anti-corruption adapters.

Explicitly compare **canonical structured manuscript AST vs arbitrary HTML**; justify the document schema, migration/versioning of schema, style mapping, and how multi-format rendering avoids lossy source-of-truth transformations. Evaluate editing engines such as ProseMirror/Tiptap, Lexical, or Slate (current capabilities/licensing to be verified). For realtime sync, compare operational transformation and CRDT (e.g., Yjs), presence and ephemeral state, auditability, version snapshots, merge conflicts, offline recovery, snapshot compaction, abuse protection and per-document permission changes. Differentiate a successfully acknowledged save from an unsynced local change.

Architect conversion as isolated, resource-limited background workers with malware scanning, content sanitization, file-type validation, retries, artifact checksums, deterministic inputs/configuration, provenance, logs and accessible error reporting. Avoid unsafe execution of imported office/HTML content. Keep private manuscripts out of public CDN buckets and search indexes. Published editions should have immutable or versioned export snapshots; later corrections create traceable new releases.

Use objective technology comparisons rather than a single rigid stack. Assess TypeScript/React/Next.js (or alternatives) for web; API framework tradeoffs; PostgreSQL for relational business data; object storage for files; queue/workers; cache where justified; full-text search versus separate index; observability; CDN; 3D viewer options (WebGL/Three.js with optional glTF/GLB); document editor licensing; payment/provider availability. Explain vendor lock-in and escape hatches. Do not pick a technology solely because it is fashionable.

The implementation handbook MUST cover: Clean Architecture/Hexagonal boundaries, domain-driven design where economically useful, SOLID, DRY (without premature abstraction), KISS, YAGNI, testable dependency inversion, composition, explicit domain invariants, immutability at critical boundaries, robust input parsing/validation, typed failure results and structured exceptions, idempotent command handling, transactional outbox for cross-boundary reliable events, eventual-consistency reconciliations, optimistic concurrency, RBAC/ABAC, configuration isolation, interfaces, OpenAPI schema-first contracts, async event schema versioning, database migrations, secure file handling, dependency updates, feature flags and extensibility. Include counterexamples and anti-patterns (god service, shared DB coupling, anemic domain without rules, distributed monolith, premature microservices, swallowing export errors, frontend-only authorization, editing rendered HTML directly, double-charging, unsafe `eval`, shared mutable singletons).

Supply representative **documented reference snippets**, not a pretend fully built product: project and chapter domain model; editor AST schema; permission-aware save API; idempotent export worker; payment webhook handler; royalty-posting use case with double-entry or balanced-ledger rationale; API contract and event payload; frontend editor integration with autosave state; upload sanitization; validation unit tests and contract tests. Each snippet has file path, context, responsibilities, security notes, expected input/output, failure paths and tests. If a reference stack has been selected, make snippets internally consistent and type-checkable; otherwise mark as pseudocode.

## 10. UML, C4, ERD and interaction diagrams — actual diagram source required

Create an indexed set of diagram-as-code sources using **PlantUML** for UML and **Mermaid** where suitable. Diagrams must include a legend, scope, meaningful names, actors, step labels, IDs and cross-references. Do not present ASCII pictures as equivalent to UML source. At minimum:

1. **C4 System Context:** authors, editors, readers, publishing staff, admins, payment providers, printers, distributors, email, search, AI providers.
2. **C4 Container:** frontend apps, API/backend modules, database, object storage, job queue, converter workers, realtime service, search, cache, 3D assets, analytics and observability.
3. **C4 Component:** document authoring domain; publishing/edition domain; commerce & royalties domain.
4. **UML Use Case:** authoring, editor review, publishing, reader commerce, payout and admin workflows.
5. **UML Class/Domain Model:** work/project, manuscript, chapter, revision, comment, asset, submission, editorial task, edition, format rendition, contract, rights grant, listing, order, license, ledger posting, payout.
6. **ERD:** primary tables, identifiers, FK references, cardinalities, unique indexes, tenancy and soft/hard deletion rules.
7. **Sequence:** create/import book, autosave/acknowledge, collaborative edit with disconnect/reconnect, version restore, preview/export with background worker, submit-review-revise-publish, book purchase/download, webhook/refund, royalty accrual/payout, 3D artifact creation.
8. **State machine:** manuscript/revision, submission, editorial task, edition/publication, conversion job, order/payment, royalty statement/payout, rights/contract lifecycle, takedown.
9. **Activity:** editorial acquisition and approvals; print preflight and proof; author publishing journey.
10. **Deployment:** environments, networks, secrets, storage access, worker isolation, backups, CDN, monitoring, multi-region options.
11. **Data flow / trust boundaries:** private content import, AI opt-in request, public publishing, purchase delivery and payment; STRIDE or equivalent threat mapping.
12. **Event and consistency view:** event publishers/consumers, outbox, idempotency keys, retries, dead-letter queues and reconciliation.

Each diagram source must be internally syntactically coherent, with a text explanation and requirement references. If execution/compilation tools are available, render and validate diagrams. Otherwise annotate `SOURCE NOT RENDER-VALIDATED` rather than falsely claiming compilation. Separate UML types from C4 architecture, which is complementary but not UML.

## 11. Data, API, permissions, lifecycle and invariants

Specify a canonical entity dictionary with at least: User, AuthorProfile/PenName, Organization/Imprint, Membership, Workspace, Project/Work, Manuscript, ManuscriptVersion, Chapter/DocumentNode, Comment, Suggestion, ResearchItem, Asset, AssetLicense, Contributor, RightsGrant, Contract, Submission, EditorialAssignment, ReviewDecision, Publication/Edition, Rendition/ExportArtifact, ISBN/Identifier, CatalogListing, Price, Territory/ChannelAvailability, Customer, Cart, Order, Payment, Entitlement/License, ReadingProgress, Review, Sale/SettlementEvent, RoyaltyRule, LedgerEntry, RoyaltyStatement, Payout, Refund, Notification, AuditEvent, ConversionJob, and 3DModelArtifact. Distinguish conceptual entities from physical database tables and explain why.

For each: ownership/tenant, fields, types, uniqueness, indexes, visibility, PII class, encryption, retention, deletion constraints, history requirements, service owner, and relationships. Produce a permission matrix with scopes and actions (view, edit, comment, submit, approve, publish, purchase, download, finance-admin) for author/owner, coauthor, invited editor, beta reader, production designer, publisher editor, publisher admin, finance, platform support, public reader and paying customer. Support least privilege; admin access to private manuscripts must have an explicit controlled purpose and audit trail.

Document business invariants: one immutable approved edition rendition maps to a versioned source/config; sales rights valid for time/territory/format; no duplicate checkout capture; no double royalties; payout cannot exceed cleared payable balance; revocation of collaborator access immediately blocks fresh reads/writes; unpublished text never enters public search; conversion fail cannot silently replace a good file; no released book without final approval and rights checks; no lost acknowledged edits; audit logs are tamper-resistant and privacy-aware.

Specify HTTP API contracts using current well-supported OpenAPI version and explicit auth, errors, pagination, rate limits, idempotency keys, optimistic concurrency, file transfer and signed URLs. Event-driven interactions should use versioned schemas and document processing ordering, retries and poison messages. Provide examples of requests, responses, error codes and webhooks and distinguish internal versus public APIs. Maintain backward compatibility and contract tests.

## 12. NFR, security, privacy, accessibility, compliance

Define measurable non-functional requirements `NFR-###`, with user/business justification, baseline, **proposed target (not a fabricated measured value)**, monitoring method, owner and test method. Cover availability, document-durability, latency, input responsiveness, autosave acknowledgements, editor payload and memory use, 100k+ word documents, load/concurrency, store search, ebook/PDF job times, batch imports, 3D framerate/fallback, scaling, storage growth, cost per author/project/export, recovery point/recovery time, observability, localization, accessibility and maintainability. Identify all planning load assumptions. Differentiate RPO of backups from durability guarantees after save acknowledgement.

Use the **applicable current official versions** of: WCAG (target 2.2 AA for product UI), EPUB 3 stable spec and EPUB Accessibility, EPUBCheck validator, PDF/UA for digital accessibility and PDF/X profile when accepted by print vendor, OWASP ASVS 5.x, NIST SSDF, OpenAPI, and Khronos glTF for 3D interchange. As of the prompt date, EPUB 3.3 is stable while EPUB 3.4 is a Candidate Recommendation Draft; validate support/acceptance with actual retailers before selecting targets. Consult current sources again at execution time; official standards change.

Privacy/security must cover: account and session management, MFA, tenant isolation, authentication and authorization, access logs, encryption, secret management, CSP/XSS/CSRF/SSRF/SQL injection, file upload scanning, zipped archive bombs, malicious EPUB/HTML, image/SVG sanitization, request limits, payment webhooks, abuse/fraud, audit trails, vulnerability handling, dependency and SBOM tracking, third-party processors, data residency, GDPR or equivalent where applicable, age-appropriate policies, opt-in analytics, author copyright, notice/takedown, license enforcement, moderated public reviews, reasonable digital content protections without blocking assistive tech, legal hold and rights-of-access/deletion exceptions.

Create a STRIDE-oriented threat model and abuse-case backlog, privacy data-flow map, DPIA screening checklist where relevant, breach-response procedure, incident and retention policies. Legal requirements must be scoped by jurisdiction and reviewed by qualified counsel; do not assert universal compliance. If targeting EU ebook services, assess European Accessibility Act applicability and national implementation. AI requests: explicit opt-in, provider disclosure, data processing terms, retention settings, PII protections, prompt-injection defenses, evaluation for hallucinated quotes/citations, IP policies, safety/human review, cost visibility, model fallback; use NIST AI RMF/GenAI profile as a reference.

## 13. QA, test cases, acceptance, and release gates

Create a risk-based test strategy spanning: unit/domain, API/contract, integration, editor browser E2E, collaboration concurrency and conflict recovery, document persistence and restoration, import/export semantic fidelity, reproducible EPUB and print/PDF output, EPUBCheck, accessibility audits/assistive tech, RTL/IME, cross-browser and mobile, payments/refunds/payout reconciliation, rights and authorization, performance/load, security scanning/penetration testing, backup/restore exercises, 3D fallback and visual tests, SEO/indexing, and production smoke tests.

For each P0 requirement create at least: one positive case, one negative case, a boundary/race/network case where relevant, test data, expected result, priority and responsible test layer. Include end-user exploratory charters such as:
- type a 50k-word draft, disconnect/reconnect, verify acknowledged text and recovery status;
- coauthor concurrently edits the same paragraph; simulate revocation and restore;
- paste formatted DOCX, footnotes, non-Latin text and tables; compare canonical semantic output;
- create EPUB and validate with EPUBCheck, open in at least two reading systems;
- create print proof and check missing fonts, overflows, spine dimensions and template warnings;
- upload malicious or oversized assets; validate sandboxing and user-facing errors;
- submit a title without required rights, reject approvals and verify it never publishes;
- refund an order and reconcile royalties without duplicate ledger postings;
- use reader and editor with keyboard and screen reader; test full RTL text and mixed-script content;
- load 3D viewer on a low-power device and verify accessible 2D fallback.

Deliver test data plan, CI gates, coverage based on risk rather than arbitrary single percentages, defect severity, user acceptance test scripts, **Definition of Ready / Definition of Done**, launch and rollback checklists, pilot criteria and exit conditions. Establish traceability `business goal -> journey -> FR/NFR -> screen -> API/domain -> test -> release milestone`, with broken-link report and risk-based open exceptions.

## 14. DevOps, reliability, delivery and procurement

Define environment strategy (local/dev/test/staging/production), migrations and rollback, secrets, IaC, reproducible deployment, branch protection, CI/CD, SAST/DAST/secret scans, artifact signing/SBOM where appropriate, container and conversion-worker sandboxing, license checks, integration staging contracts, production data segregation, backup/restore tests, uptime/error budget reports, log redaction, alerts, paging and incident communications, runbooks and disaster recovery. Recommend monitoring and observability for autosave errors, failed conversions, purchase failures, payout imbalance, stale public listings and 3D errors.

Prepare a phased roadmap with dependencies, milestone acceptance criteria, proposed team composition and role mix, complexity ranges, effort assumptions and uncertainty. Provide at least three delivery options: lean author-studio-led launch, balanced publishing MVP, and broader all-in-one build. Do not fabricate precise budgets; express effort and infrastructure costs as assumption-based ranges/drivers and call out unknown vendor costs. Include a **RFP/vendor response format** with bidder qualifications, architecture approach, security evidence, publishing experience, licensed component dependencies, implementation estimates by module, demo exercises, milestone costs, IP ownership, support/SLA, exit/data portability, source repository access, acceptance milestones, change-order governance and evaluation scorecard.

Build and evaluate an initial go-to-market strategy: author acquisition/free tier, migrating-author importer, creator partnerships, email/community, writing events, editorial marketplace, templates/SEO, international expansion triggers, author support SLAs, reader discovery/catalog quality and trust/safety operations. Estimate unit economics and conversion funnels using variables and labeled scenarios, not ungrounded demand forecasts.

## 15. Mandatory quality gates and consistency checks

Before labeling any deliverable `READY FOR REVIEW`, perform a simulated interdisciplinary review and explicitly report:
1. Does every business objective map to at least one measurable KPI and requirement?
2. Is every P0/P1 feature traceable to a user, screen, service/domain, data object, permission and test?
3. Do all state machines forbid illegal transitions and preserve legal/financial invariants?
4. Can an author retrieve their manuscript even if they never publish through the company?
5. Does manuscript editing stay independent of formatting themes and commercial publishing states?
6. Are files/published editions reproducible and printed proof differences made visible?
7. Are private drafts excluded from public indexes, unauthorized AI requests and unrestricted admin access?
8. Is the full purchase -> refund -> royalty -> payout lifecycle auditable and reconcilable?
9. Are 3D views derived from real dimensions or clearly labeled illustrative?
10. Are nonfunctional metrics measurable, targets explicitly proposed and costs recognized?
11. Are WCAG, accessible EPUB, PDF formats, RTL and edition metadata addressed end-to-end?
12. Are diagram names, IDs, relationships, APIs and schemas consistent across files?
13. Are current competitor claims source-linked and gaps classified as verified or unknown?
14. Are proposed innovations and the real MVP clearly separated?
15. Are ADR tradeoffs, scope exclusions, risk owners and launch blockers explicit?
16. Are human legal, financial, editorial and security approvals requested rather than fabricated?
17. Are acceptance scenarios observable by a QA specialist without private developer knowledge, while deeper API/security tests are separately specified?
18. Are key code examples internally consistent, secure and appropriately testable?

Produce a **Quality Audit Report** with pass/partial/fail, concrete evidence, issue IDs, severity, proposed fix and owner. Correct major inconsistencies before completing the package. Include explicit document coverage percentage based on created artifacts, not a claim that all requirements have been implemented or validated.

## 16. Output protocol — avoid truncation or shallow generic writing

**Required execution order:**
- **Batch 0: Alignment.** Executive one-page brief; what is known/assumed; operating model options; decision questions; role roster/RACI; document manifest.
- **Batch 1: Discovery.** Competition with dated sources and confidence, audience, business model, user journeys, market differentiators, KPI model.
- **Batch 2: Product specifications.** PRD, SRS, full inventory, priorities, business rules, user stories and concrete acceptance scenarios.
- **Batch 3: Experience and publishing production.** IA, screen-by-screen contracts, design system, accessibility, editorial processes, formats, proofing, 3D specification.
- **Batch 4: Technical architecture.** C4/UML/ERD sources, domain design, architecture ADRs, data, APIs, event contracts, reliability and integrations.
- **Batch 5: Engineering and quality.** Clean-code handbook, coding patterns, repo structure, reference snippets, QA strategy, test cases, security, operations.
- **Batch 6: Delivery and verification.** Roadmap, RFP, vendor scorecard, team plan, financial assumptions, quality audit, final traceability and gaps.

Within each batch, give actual depth, not just a table of contents. If a single response cannot contain the full documentation, do **not** compress it into a superficial outline or pretend completion. Instead provide the files that can actually be created, show the batch status with IDs, and continue systematically in the next available response or when the user requests the next batch. If tools allow multi-file creation, prioritize real source files. Use consistent stable identifiers; cite reliable source URLs and check dates, differentiate actual research from proposed design, and make every diagram/code sample copyable and testable.

**Tone and output:** Professional solution-design language, direct and precise, clear tables where helpful, no unsupported superlatives. Deliver detailed decisions with alternatives and rationale, not a list of buzzwords. Clearly label all estimates as estimates. Write in English unless asked otherwise, but design the product for broad language support.

**Begin now with Batch 0**, then progress through the remaining batches in order using available capabilities. First explain the proposed publishing operating model and the foundational architectural choice in a concise executive summary. Do not ask for clarification unless an unanswerable question would make the next artifact materially incorrect; log assumptions and proceed.

# END MASTER PROMPT
