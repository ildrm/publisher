# DISC-03 — Personas, jobs and research plan

Version 0.2 · 2026-10-29 · **Draft** · Author: UX Researcher · Accountable/decision owner: Product Owner · Consulted: Editorial, Accessibility, Support, Finance · Reviewer: Product Owner · Approver required: Product Owner

**Assumptions:** personas are provisional composites, not interview findings. **Related:** DISC-01, DISC-02, DISC-05, DISC-06. **Unresolved:** segment size, recruitment access, support needs, language and jurisdiction; Product Owner to resolve before pilot recruiting.

## Personas and jobs

| Segment / provisional priority | Job to be done | Success and risk | Research question |
|---|---|---|---|
| Independent fiction author / first | Draft and revise a long work without losing control | Recoverable text, chapters, viable export; fear of silent loss | What evidence creates enough trust to migrate? |
| Nonfiction author / first, text-centric | Structure and retrieve long text with references | Preserve semantics; citations and notes may exceed pilot limits | Which features prevent loss during import/export? |
| Hobbyist / second | Sustain writing without committing to publication | Low-friction free tier; storage cost and privacy | Which limits are acceptable? |
| Coauthor / later | Coordinate edits without overwriting another writer | Attribution and access revocation; concurrent editing is deferred | Can sequential review satisfy initial needs? |
| Freelance editor / later | Review an authorized version and return clear feedback | Scoped access and clear handoff | Which review workflow is mandatory? |
| Publisher editor / first | Decide on eligible submissions and communicate status | Evidence and traceable human decisions; confidentiality | How many submissions can a team assess? |
| Production designer / first | Turn approved text into verifiable formats | Accessible exports and physical proof; no false promises | Which warnings require human intervention? |
| Beta reader / later | Read an authorized sample and provide feedback | Expiring access; avoid exposure of private draft | What feedback and expiry controls matter? |
| Reader / first | Discover, buy and read a trustworthy book | Price clarity and licensed access; accessible reader | Which purchase and recovery barriers matter? |
| Finance administrator / first | Reconcile sales, refunds and contributor balances | Auditable, balanced entries; no duplicate payouts | Which settlement evidence is needed? |
| Support agent / first | Resolve access and delivery incidents | Purpose-limited access with an audit trail | What can be resolved without opening a manuscript? |
| Institutional publisher / later | Govern multiple imprints and teams | Complex tenancy, contracts, exports | Is there demand to justify a separate B2B product? |

## Research protocol

Recruit a purposive set across genres, disability/access needs, language/script, publishing experience and market. Proposed first wave: 5–8 authors, 3–5 editors/production staff, 3–5 readers and 2 finance/support practitioners; these are planning targets, not evidence of statistical representation. Separate interviews from usability tests; consent, compensation, anonymization and recruitment exclusions need local policy review. Never collect unpublished manuscript text without explicit, limited-purpose consent; supply synthetic fixtures by default.

1. Interview about last real drafting, publishing or purchase experience before showing a solution. Ask participants to demonstrate their own workflow only if consented; record barriers and alternatives, not just preferences.
2. Run a moderated prototype test: create chapter, identify save state, export, submit a fixed revision, find its status, purchase a sample and recover access. Include keyboard/screen-reader and mixed RTL/LTR tasks with qualified participants.
3. Test 10 friction hypotheses in DISC-02 with behavior, frequency and consequence. Record disconfirming evidence, confidence and who was excluded. Do not generalize sample frequencies to a market.
4. Compare import/export on licensed, synthetic DOCX and Markdown fixtures; track lost structure, unsupported elements and recovery time. Run vendor tests without transferring confidential work.
5. Decision workshop: publish an evidence log, prioritize problems with severity and cost, retain a dissent register and revise MVP. Escalate architecture-reversing findings on offline/collaboration and jurisdiction before committing implementation.

Success thresholds are to be set in advance with stakeholders, not retrofitted to the results. Review recruitment and consent with privacy counsel. Research owner: UX Researcher; decision owner: Product Owner; next decision milestone: pilot scope approval.

## Review checkpoint

| Role | Concern / response | Residual risk | Approval required |
|---|---|---|---|
| Research | Small samples can overrepresent vocal users; recruit diversity and record limits | Not representative | Product Owner |
| Accessibility | Include assistive technology and mixed-script tasks | Participants and support not yet recruited | Accessibility lead |
| Privacy | Use synthetic material and explicit consent for any real text | Consent wording not reviewed | Privacy lead |

References: [evidence and hypotheses](02-market-and-competitor-evidence-matrix.md); [journeys](05-service-blueprints-and-user-journeys.md).
