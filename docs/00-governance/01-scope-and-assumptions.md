# GOV-001 — Scope and assumptions

- **Version / date:** 0.3 / 2026-10-29
- **Status:** Draft — the user's 14-language requirement is explicit; no specialist or launch approval obtained
- **Authoring / accountable role:** Chief Product Manager / Product Owner
- **Consulted roles:** Executive Sponsor, Business Analyst, Editorial Lead, Principal Architect, Security/Privacy/Legal, Finance, Accessibility Specialist, QA Lead
- **Reviewer / approver / decision owner:** Business Analyst / Executive Sponsor / Chief Product Manager; all review and approval pending
- **Assumptions:** ASM-001–012 below; validate unless an explicit later user requirement supersedes the assumption, as recorded for ASM-002.
- **Related requirements:** Source prompt §§0–3, 5 and 15; see the draft [feature catalog](../02-requirements/03-feature-catalog-and-prioritization.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md) and [NFRs](../02-requirements/06-nonfunctional-requirements-and-slos.md). Decomposition and end-to-end traceability remain incomplete.
- **References:** [Decision and question register](02-decisions-and-open-questions.md); [glossary](03-glossary-and-ubiquitous-language.md); [roles](04-stakeholders-roles-raci.md); source master prompt, version 1.0, supplied 2026-10-29.

## Executive framing

Provide a trustworthy, portable authoring studio that is useful before and without publication. Authors may submit completed revisions to a curated publisher; editorial, rights, proof, and release checks gate any sale. The initial catalog sells selected text-centric fiction and nonfiction, with rights and customer entitlements explicit. The proposed implementation starts as a modular monolith with separate document, publishing, commerce and finance boundaries, asynchronous isolated conversion workers, and private storage. This design is a proposal, not evidence of business validation or an approval to launch. See DEC-001 and DEC-002.

Success means both productive authors and legally reviewable, quality-controlled titles: manuscript uploads alone are not publishable-title throughput. Measures and baseline values require discovery; no demand, revenue or timeline is inferred here. Loss of acknowledged manuscript edits, unauthorized exposure, invalid rights and unbalanced financial entries are launch-blocking outcomes.

## Operating-model comparison

| Model | Advantages | Costs and risks | Initial disposition |
|---|---|---|---|
| Curated publisher | Human selection, production and quality control; fewer uncontrolled releases | Editorial and proof capacity limits throughput; rights and per-title economics need review | **Proposed**: selected books enter the catalog only after rights and production approval. |
| Open self-service marketplace | Broad catalog and author autonomy | Higher moderation, support, takedown, quality and financial reconciliation burden | Defer until evidence and operating capacity exist. |
| Hybrid | Studio retains author autonomy; selected titles receive publisher services | Clear separation of independent author exports from publisher endorsement and rights is essential | Studio is open for writing/export, while publisher sales are curated; evaluate self-publishing later. |
| Third-party distribution | Access to potential external channels without owning every storefront | Partner eligibility, formats, costs, territory, settlement and contracts require validation | Plan an interface and manual pilot; do not promise an unverified integration. |

## Scope boundary

**Provisional launch candidate, subject to sizing and DEC-003:** verified identity, private workspace and least-privilege membership; structured accessible editor with clear save state, recovery and versions; author export independent of publishing; constrained text-centric import/export; submission and internal review; rights records and final approval; accessible digital and printer-specific output with human proofs; public listing and purchase/entitlement; reconciled royalty ledger; essential administration, backups, monitoring, security and support. An accessible 2D cover and description are the P0 baseline; a 3D physical preview is an optional P1 candidate, conditional on reliable dimensional inputs and a 2D equivalent. A pilot must reduce scope or delay launch if dependable document persistence, rights, finance or human QA cannot be demonstrated.

**Deferred discovery, not launch commitments:** simultaneous editing and advanced offline merge, advanced planning, broad third-party distribution, complex picture/math/fixed-layout books, audio, institutional multi-imprint workflows, AI assistance, AR and immersive story worlds. The broader feature universe still requires inventory and prioritization; exclusion here is not a claim that a feature is unwanted. The user's subsequent request makes at least 14 interface languages part of the active implementation scope. DEC-011 records the total-speaker interpretation and the 15 shipped interface choices, including Persian. This scope change does not approve production release, every regional language variant, translated legal agreements or automatic manuscript translation.

## Assumption register

Each entry is **ASSUMPTION — VALIDATE** unless marked superseded by an explicit user requirement; due milestones are relative, not calendar commitments. Owners are proposed roles, not named approvers.

| ID | Provisional assumption | Impact if false / validation | Owner | Due |
|---|---|---|---|---|
| ASM-001 | Web-first cloud service; responsive layouts. | Native or air-gapped requirements alter platform and cost; interview sponsor and target users. | Product | Scope baseline |
| ASM-002 | Original English-only UI assumption superseded by the user's explicit requirement: support the 14-language total-speaker set plus Persian. The interpretation and variants are recorded in DEC-011; manuscript language/direction stays independent. | Exact key coverage, translated drafts, preference migration, RTL/CJK layouts and Unicode round trips require evidence; real language, screen-reader and IME review remains open. | Accessibility/i18n | Active local increment; specialist review before pilot |
| ASM-003 | One imprint at launch, tenant boundaries designed for later organizations. | Multiple launch imprints expand permissions and operations; confirm organizational model. | Publisher Director | Scope baseline |
| ASM-004 | Launch content is predominantly text-centric fiction and nonfiction. | Complex layouts increase conversion, rights and QA effort; inspect representative manuscripts. | Print Production | Content pilot entry |
| ASM-005 | Authors retain ownership except under separately negotiated agreements. | Contract and ownership model changes require legal redesign; counsel reviews each applicable jurisdiction. | Legal | Contract baseline |
| ASM-006 | Editorial curation gates marketplace publication; exporting remains independent. | Open self-service requires additional moderation and financial controls; verify business strategy. | Sponsor | Scope baseline |
| ASM-007 | Launch market, currency, taxes, payment and payout rails are unresolved. | Market choice changes legal, integration and ledger needs; conduct market/provider/counsel assessment. | Finance | Vendor selection |
| ASM-008 | Internet connection is normally available; offline drafting and conflict merge are not guaranteed at launch. | Offline-first usage changes persistence and sync architecture; research author conditions. | Document Engineer | Architecture baseline |
| ASM-009 | No manuscript enters a public index or model training by default; exceptional processing requires explicit purpose-specific consent. | Different requested processing needs policy, processor and legal review; privacy threat-model validation. | Privacy Lead | Architecture baseline |
| ASM-010 | Three-dimensional view represents physical dimensions when trustworthy inputs exist, with 2D accessible equivalent. | Missing paper/binding specifications require labeled illustrative view or fallback; validate against printer proofs. | Print Production | Production pilot |
| ASM-011 | Cost, schedule, staffing, load and adoption are planning estimates until measured. | Incorrect sizing can break financial or reliability assumptions; obtain vendor quotes and pilot measurements. | Delivery Manager | Investment decision |
| ASM-012 | No interviews, partner commitments, compliance certificates, production proofs or human approvals were supplied. | Treat all corresponding claims as unverified; collect dated evidence and approvals. | Research Lead | Respective gate |

## Boundaries and unresolved questions

The prompt is the supplied requirement source, not evidence of customer demand, jurisdictional law or actual supplier capabilities. Publisher ownership and exclusivity must never be inferred from submission. Publication proceeds only with a recorded rights grant appropriate to format, language, territory, channel and time plus production and release approvals. OQ-001–010 and RSK-001–012 are maintained in [the register](02-decisions-and-open-questions.md).

## Simulated Batch 0 cross-role checkpoint

This is a design review simulation; no named person has reviewed or approved it.

| Role | Concern raised | Change reflected here | Residual risk | Required human approver |
|---|---|---|---|---|
| Product / Sponsor | A broad platform could exceed an initial release. | Curated text-centric pilot and explicit deferrals. | Scope and funding not validated. | Sponsor and Product Owner |
| Author trust / Privacy | Private draft leakage and lock-in destroy trust. | Private default and export without publication. | Operational enforcement and processor terms unverified. | Privacy and Security leads |
| Editorial / Print | Upload counts do not prove a publishable book. | Rights, editorial and proof gates. | Real print proof and capacity untested. | Editorial and Print leads |
| Architect / Document Engineer | Save loss or premature service splitting. | Modular boundaries and acknowledged-save priority. | Durability targets and failure behavior still need tests. | Principal Architect and SRE |
| Finance / Legal | Sales without valid rights or balanced accounting. | Explicit grants and ledger requirements. | Market, tax and royalty terms unresolved. | Finance lead and qualified counsel |
| Accessibility / QA | Accessibility and RTL need evidence, not labels. | Included from inception, with no conformance claim. | Assistive technology and reading-system verification pending. | Accessibility and QA leads |
