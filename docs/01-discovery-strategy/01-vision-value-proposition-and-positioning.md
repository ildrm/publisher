# DISC-01 — Vision, value proposition and positioning

Version 0.3 · 2026-10-29 · **Draft** · Author: Chief Product Manager · Accountable/decision owner: Publishing Director · Consulted: UX Research, Editorial, Architecture, Security, Finance, Accessibility · Reviewer: Product Owner · Approver required: Executive Sponsor

**Assumptions:** single initial imprint, text-centric books, limited launch markets, curated publishing, portable free drafting. All are provisional. **Related:** DISC-02–06; governance registers; future authoring, publishing and commerce requirements. **Unresolved:** launch jurisdiction, acquisition budget, contractual terms and payment eligibility; owner: Publishing Director; resolve before provider selection/pilot.

## Vision and user problem

Offer a dependable place to create and retrieve a manuscript, with a transparent optional route through editorial selection, rights clearance, production and reader purchase. Existing tools demonstrate parts of this workflow (DISC-02), but user frustration or a gap in the market has not been established by interviews. The product promise is a **proposed position**, not an evidence-backed claim of uniqueness: authors keep their work, can leave with useful exports, and can see how a submitted revision moves through editorial decisions.

## Strategic choices

Prioritize independent fiction and text-centric nonfiction authors who want a credible, optional editorial path; next serve the publisher's editors and production staff, then readers of accepted titles. Hobbyists benefit from portable drafting, but free storage has cost. Coauthors, freelancers and institutional publishers remain research segments until access, collaboration and tenant economics are validated. Reader demand and acquisition costs are unknown. Accessibility, localization and rights boundaries apply to all segments. The user's subsequent minimum 14-language request makes multilingual interface support active scope; [DEC-011](../00-governance/02-decisions-and-open-questions.md) records the selected total-speaker set plus Persian. Regional variants, real language review and translated public/legal/support content require their own acceptance evidence.

| Option | Benefit | Cost and exposure | Provisional decision |
|---|---|---|---|
| Curated publisher | Editorial and rights gates make quality controllable | Limited catalog throughput; editorial staffing and rejection support | Select for initial publishing operation |
| Open self-service | Author autonomy and larger potential catalog | Moderation, rights enforcement and support burden | Defer; investigate economics and legal basis |
| Hybrid | Both acquisition paths | Two distinct operating policies and attribution | Reconsider after curated pilot |
| Third-party distribution | Reach existing outlets | Contracts, territories, settlement and reconciliation differ | Manual or partner pilot only after due diligence |

Free Studio access does not grant publication rights. Acceptance does not itself create an edition, a listing or a purchase. Rights are explicit by format, language, territory, channel and term; counsel must approve contracts. Versioned production approvals and proof checks precede release. Initial architecture is a modular monolith with isolated conversion workers and separate private/public storage and indexes; this is a design proposal, not a proof of scale. Favor evidence of successful restores and reconciled accounting over feature breadth.

## Outcome model and positioning

Business outcomes: authors can reach a first acknowledged chapter and retrieve their text; qualified submissions can reach an editorial decision; approved, rights-cleared editions can be purchased and reconciled. DISC-06 defines numerator, denominator, safeguards and instrumentation. Position against fragmented handoffs as a hypothesis for testing, not a claim that alternatives cannot do this. Quality and trust must be demonstrated with recovery exercises, clear rights disclosures and a human-assisted pilot before being marketed as strengths.

**Release boundary:** first prove reliable authoring, export, editorial decisions and a small manually supervised digital publishing/commerce path. Automated external distribution, simultaneous editing, AI and immersive reading are deferred. An optional 3D preview uses verified dimensions or clearly labels estimates and provides an accessible 2D fallback; it is not a substitute for a print proof. Scope still requires explicit stakeholder acceptance and risk-based effort validation.

## Review checkpoint

| Role | Concern / proposed response | Residual risk | Human approval |
|---|---|---|---|
| Product and UX | Free drafting may not drive submissions; measure both paths | Acquisition assumptions untested | Product Owner |
| Editorial and legal | Curated decisions and grants need human policy | No jurisdiction selected | Publishing Director and counsel |
| Architecture and security | Keep private text out of public indexes and AI providers by default | Implementation not yet tested | Security lead |
| Finance | Ledger and reconciliation precede payouts | Pricing and merchant-of-record undecided | Finance lead |

References: [Competitor evidence](02-market-and-competitor-evidence-matrix.md); [research plan](03-personas-jtbd-and-research-plan.md); [KPIs](06-product-kpis-and-analytics-plan.md).
