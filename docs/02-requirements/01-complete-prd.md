# PRD-001 — Product requirements: author studio and publishing house

Version 0.2 · 2026-10-29 · Status: Draft; no stakeholder approval implied  
Authoring/accountable: Product Owner · Consulted: Editorial, UX, Engineering, Finance, Legal, Accessibility, Support · Reviewer: Requirements Engineer · Approver and decision owner: Executive Sponsor  
Assumptions: ASM-001–012; decisions DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Scope and dates are proposals until validated. Related requirements: FR-IAM-001–002, FR-DOC-001–003, FR-IMP-001, FR-EXP-001, FR-PUB-001–002, FR-RGT-001, FR-FMT-001, FR-3D-001, FR-CAT-001, FR-COM-001, FR-FIN-001, FR-OPS-001 and NFRs in [SLOs](06-nonfunctional-requirements-and-slos.md).

## Executive summary

Writers need a trustworthy place to create and recover manuscripts and a clear, optional path to professional publication. Readers need dependable access to purchased editions; publishing staff need a controlled way to validate rights, approve artifacts and account for sales. The proposed first release links private, portable drafting to a curated editorial pipeline and a limited direct digital storefront. The author retains ownership unless a separately negotiated agreement provides otherwise. A publication decision is independent of the decision to use the studio.

The proposed outcome is that an author can create a project, see that changes are durably saved, recover a revision, export without publishing, and submit a specific revision. Staff can review it, record the granted rights, approve a rendition and release a listing. A reader can purchase and access an entitled digital product, and finance can reconcile the sale and royalty. Any optional 3D mockup is illustrative, uses accurate or explicitly labeled estimated inputs, and never substitutes for an approved manufacturing proof. Scope is conditional on launch-market legal and provider decisions and passing the acceptance gates below; the publishing and commerce slices must not launch as simulated financial operations.

## Problem, users and value

| Segment | Job and outcome | First-release posture |
|---|---|---|
| Hobbyist and professional author, fiction or nonfiction | Write, recover, control, export and optionally submit work | Primary |
| Editor and publishing director | Evaluate a frozen submission and control approvals | Primary |
| Production specialist | Produce and verify text-centric edition artifacts | Primary |
| Buyer and reader | Discover, purchase and read a licensed edition | Primary, narrow digital purchase |
| Finance and support | Reconcile transactions; resolve disputes safely | Primary operational users |
| Coauthors, beta readers, designers and institutions | Collaborate or operate larger programs | Research and phased expansion; no real-time editing promised |

## Goals and measures

Baseline data and launch market are absent. Product and data owners must establish baseline, cohort, target and time window during pilot rather than treating the following as forecasts. Define author activation as a first acknowledged chapter save; measure median time from verified account to that event and the proportion completing it. Track 30/90-day active-author retention, exports, submission-to-eligibility, acceptance among reviewed submissions, approved-proof rate, listing-to-purchase and entitlement delivery. Guardrails: acknowledged text loss incidents, restore success, unlicensed/contested rights, invalid renditions, print proof rejections, failed payments and duplicate ledger postings, refund rate, accessibility failures and support contacts. Count an event only after the underlying committed action, with privacy-safe IDs and consent as applicable. Analytics is not the financial ledger.

## Scope and constraints

P0 comprises secure identity and access; structured text-centric projects; acknowledged saves and revisions; bounded import and portable export; submission and editorial queues; rights and release controls; validated EPUB and printer-specific PDF workflow; an accessible 2D cover preview; catalog, payment and entitlement; traceable financial accounting, security, audit and recovery. A 3D preview is an optional pilot candidate, conditional on accurate inputs or clearly labeled estimates and an accessible 2D baseline. Release may be staged, but publication and paid sales require all their dependencies. P1 considers collaboration, advanced planning, POD/distribution and expanded library and marketing; P2 considers consent-governed AI, complex formats, immersive 3D and institutions. No default AI training, arbitrary PDF-to-editable conversion, realtime/offline collaboration or worldwide payment/printing support is promised. Each of these requires separate discovery and approval.

Quality and privacy are differentiators to validate with research, not established market advantages. Drafts must remain private; an author must be able to export without publishing. Release artifacts must be tied to approved revisions, rights, metadata and format profiles. A public listing cannot grant more rights or territories than recorded. Private and public search boundaries are separate. Market, pricing, competitor coverage and conversion assumptions need evidence before procurement.

## Launch criteria and dependencies

1. Product and accessibility owners sign off on a representative multilingual, keyboard and screen-reader pilot, including bidirectional content; no untriaged critical defect remains.
2. SRE demonstrates a restore from an isolated backup and tests an acknowledged-save recovery scenario; security owner signs off threat mitigations and access isolation.
3. Editorial and production owners approve immutable rendition, metadata, rights and proof evidence on pilot titles; any printer preset is verified with the actual printer.
4. Finance reconciles test purchase, refund, royalty posting and payout or documented manual settlement with an independently inspectable ledger. Provider and jurisdiction capabilities are verified before enabling sales.
5. Support has runbooks, incident contacts, takedown/rights escalation and an author export path; decision owners accept residual risk in writing.

## References

Source: *Online Publishing Super Mega Documentation Prompt*, version 1.0, sections 0–3 and 5–7 (user-supplied); [scope and assumptions](../00-governance/01-scope-and-assumptions.md); [decisions and open questions](../00-governance/02-decisions-and-open-questions.md). Planned downstream artifacts are identified as planned in the text.

## Open questions and phase review

Launch territories, tax and payout rules, retention schedules, provider availability, print partnership, pricing, sample rights and editorial staffing require named decision owners and milestones in the governance register. User research must test the curated model, activation measures and willingness to submit. See [recovery](07-error-recovery-and-edge-cases.md), [business rules](05-business-rules-and-permissions.md), and delivery roadmap.

| Role | Concern raised | Change made in this draft | Residual risk | Approval required |
|---|---|---|---|---|
| Author advocacy / Product | Trust and portability | Export independent of submission | Pilot usage untested | Product Owner |
| Editorial / Production | Quality and print fidelity | Frozen revision and proof gates | Partner preset unverified | Publishing Director |
| Legal / Finance | Rights and settlement | Explicit grants and ledger dependency | Jurisdiction/provider decisions | Legal and Finance owners |
| Security / Accessibility | Isolation and usability | Release evidence gates | No certification or conformance claim | Security and Accessibility owners |
