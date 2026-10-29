# GOV-002 — Decision, question and risk registers

- **Version / date:** 0.3 / 2026-10-29
- **Status:** Draft — DEC-011 records the user's explicit requirement and the implementer's interpretation; other proposals and specialist approvals remain open
- **Authoring / accountable role:** Senior Business Analyst / Requirements Engineer
- **Consulted roles:** Sponsor, Product, Editorial, Principal Architect, Finance, Legal/Privacy, SRE, QA, Accessibility/i18n
- **Reviewer / approver / decision owner:** Product Owner / Sponsor / owner named per entry; review and approval pending
- **Assumptions:** ASM-001–012 in [scope](01-scope-and-assumptions.md).
- **Related requirements:** Source prompt §§0–2, 5, 9, 11–16; see the draft [feature catalog](../02-requirements/03-feature-catalog-and-prioritization.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md) and [NFRs](../02-requirements/06-nonfunctional-requirements-and-slos.md). Decision-to-requirement links remain incomplete.
- **References:** [Scope and assumptions](01-scope-and-assumptions.md); [roles and RACI](04-stakeholders-roles-raci.md); source master prompt v1.0.

## Register conventions

A **proposed** decision directs drafting, not procurement or launch. Decision owners must record evidence, alternatives, date, approval and affected artifacts when making an actual decision. Reopen when the trigger materializes. Milestones below are dependencies, not invented dates; the Delivery Manager schedules them after an investment decision. Risk severity is a qualitative planning estimate.

## Decision register

| ID | Proposal and alternatives | Rationale / consequence | Owner | Validation / reopen trigger | Status |
|---|---|---|---|---|---|
| DEC-001 | Curated publisher with a portable free writing studio; alternatives: open marketplace, hybrid self-publishing, distributor-led. | Separates author value from publisher quality control; limits title throughput and requires editorial capacity. | Sponsor | Model and cost-to-serve research, legal and operational review; reopen if launch strategy changes. | Proposed |
| DEC-002 | Modular monolith with explicit domain boundaries and isolated conversion workers; alternative: microservices or single undifferentiated service. | Keeps transactional operations tractable while isolating untrusted conversion; extract only with evidence. | Principal Architect | Prototype reliability and deployment boundaries; reopen if scale, regulatory isolation or team evidence demands it. | Proposed |
| DEC-003 | Scope a text-centric curated pilot; defer unproven advanced collaboration, offline merge, AI and complex formats. | Protects persistence and production gates; may reduce early market coverage. | Product Owner | Pilot demand, estimates and capacity; revisit before scope baseline. | Proposed |
| DEC-004 | Use canonical structured semantics separate from rendering themes and commercial state. | Enables portable exports and independent edition snapshots; import mappings must disclose loss. | Document Engineer | Representative manuscript round-trip and accessibility testing; revisit if fidelity fails. | Proposed |
| DEC-005 | Treat server-acknowledged saves as a defined durability contract; visible pending/error state for unacknowledged edits. | Prevents misleading success feedback; exact storage, recovery and target require proof. | Document Engineer / SRE | Failure injection and restore tests; revisit when infrastructure and RPO are selected. | Proposed |
| DEC-006 | Private by default; no public indexing or model training; processing beyond ordinary service requires purpose-specific opt-in. | Protects author trust; terms, providers and access controls require verification. | Privacy Lead | Data-flow and processor review; revisit for each new purpose. | Proposed |
| DEC-007 | Edition releases bind approved source revision, configuration and artifact hashes; corrections create traceable versions. | Reproducible output and auditability, with storage and production costs. | Publishing Operations | Conversion reproducibility and proof testing; revisit for legitimate correction workflow. | Proposed |
| DEC-008 | Purchases, entitlements, sales, refunds, royalty accruals and payouts are separate events and records; balanced ledger is financial authority. | Reconciliation is explicit and retry-safe; accounting treatment requires local expertise. | Finance Lead | Accounting and provider reconciliation exercise; reopen on settlement or contract change. | Proposed |
| DEC-009 | Accessible 2D cover and description are the P0 baseline. An optional P1 dimension-based 3D view requires verified inputs; use a labeled illustrative or 2D view when inputs are missing. | Avoids misleading proof expectations and preserves access on constrained devices. | Print Production | Compare real proof and viewer; revisit per binding and paper supplier. | Proposed |
| DEC-010 | Jurisdiction, vendors, target standards versions and exact technology choices remain open pending evidence. | Avoids false compatibility and compliance claims but prevents final implementation estimates. | Sponsor / Principal Architect | Market and vendor selection; standards review before release. | Open |
| DEC-011 | Implement the user's request that the website support the top 14 world languages. Interpret this as total first- plus additional-language speakers: English, Mandarin Chinese (Simplified UI), Hindi, Spanish, Standard Arabic, French, Bengali, Portuguese, Indonesian, Urdu, Russian, German, Japanese and Nigerian Pidgin. Keep Persian as an additional fifteenth interface. Alternative definitions include native-speaker or web-usage rankings and would produce a different list. | The minimum language requirement is user-authorized; the ranking method, script and default formatting regions are documented implementation choices, not separate user or native-language approval. The [dated AWS 2024 source](https://reinvent.awsevents.com/content/dam/reinvent/2024/slides/dev/DEV340_Build-LLMs-for-low-resource-languages-with-SageMaker-HyperPod-clusters.pdf) and [2026 secondary summary](https://www.visualcapitalist.com/ranked-the-worlds-most-spoken-languages-in-2026/) support this set. No exact speaker-count or live Ethnologue verification claim is made; its primary ranking page returned HTTP 403 during review. | Product / Accessibility-i18n | Revisit if the user specifies a different ranking method, script or regional variants; obtain actual language review before pilot. Evidence and locale limits: [multilingual review](../../implementation/multilingual-review.md). | User requirement recorded; implementation interpretation applied; linguistic and production acceptance pending |

## Open questions

| ID | Decision question and material consequence | Proposed owner | Resolve by | Evidence needed |
|---|---|---|---|---|
| OQ-001 | What launch jurisdictions and legal entities apply? Determines privacy, tax, consumer and accessibility obligations. | Sponsor / Legal | Market selection | Counsel assessment for named markets; residency requirements. |
| OQ-002 | Which author segments and book types justify the first launch? Determines pilot scope and fidelity needs. | Product / Research | Scope baseline | Interviews and representative manuscript samples. |
| OQ-003 | What author agreement, territories, channels, term, exclusivity and royalty bases apply? Changes rights and financial flows. | Editorial / Legal / Finance | Contract baseline | Actual draft contracts and jurisdiction-specific advice. |
| OQ-004 | What publisher capacity and acceptance policy are available? Determines SLA and title throughput. | Editorial Lead | Pilot plan | Staffing and end-to-end review/proof exercise. |
| OQ-005 | Which payment, payout, tax, print and distribution partners are available in the selected markets? Determines integration scope. | Commerce / Finance | Vendor selection | Dated capability, fees, sandbox and contract evidence. |
| OQ-006 | What loss, recovery and availability targets can the business afford? Determines infrastructure and acceptance. | SRE / Product | Architecture baseline | Restore tests, workload and cost model; distinguish acknowledged durability from backup RPO. |
| OQ-007 | Which imports/exports, language samples and reading systems must pass the pilot? Determines editor and conversion complexity. | Conversion / Accessibility | Content pilot entry | Licensed samples, validators, assistive technology and target reading-system matrix. |
| OQ-008 | Is collaboration or offline authoring essential on day one? Could materially change sync architecture and release scope. | Product / Document Engineer | Scope baseline | Author research, concurrency prototype and failure tests. |
| OQ-009 | What payment, refund, reserve, royalty and payout policies apply per contract and jurisdiction? Determines posting and settlement rules. | Finance / Legal | Contract baseline | Contract examples, accountant review and provider settlement samples. |
| OQ-010 | What budget, deadline, team and measurable pilot thresholds are approved? Determines feasible release shape. | Sponsor / Delivery Manager | Investment decision | Staffing estimates, critical path and risk-adjusted capacity. |

## Risk register

| ID | Risk / impact | Severity | Proposed mitigation and trigger | Owner | Due |
|---|---|---|---|---|---|
| RSK-001 | Acknowledged edits lost or silently overwritten; irreversible author harm. | Critical | Define acknowledgement boundary, version restore, conflict handling and destructive failure tests; block pilot on any unexplained loss. | Document Engineer / SRE | Pilot entry |
| RSK-002 | Private manuscript exposed through search, storage, staff access or processors. | Critical | Tenant authorization, private buckets, separately published index, scoped audited support access and penetration tests. | Security / Privacy | Pilot entry |
| RSK-003 | Invalid rights or missing approvals cause unauthorized publication. | Critical | Grant dimensions, expiration checks, human approval and release hold; counsel reviews policy. | Editorial / Legal | First release |
| RSK-004 | Duplicate capture, royalty posting or payout produces financial loss. | Critical | Idempotency, balanced ledger, reconciliations and independent finance review. | Finance / Commerce | First transaction |
| RSK-005 | Import/export changes semantic content or produces inaccessible output. | High | Representative corpus, loss reports, validators, assistive technology checks and human proofs. | Conversion / Accessibility | Content pilot entry |
| RSK-006 | Print product differs from preview or dimensions. | High | Printer-specific configuration and physical proof approval; clearly labeled 3D or fallback. | Print Production | First print release |
| RSK-007 | Unclear launch market prevents lawful/provider-ready operating model. | High | Resolve OQ-001/005/009 before live transactions; qualified counsel and finance approval. | Sponsor / Legal | Vendor selection |
| RSK-008 | Scope exceeds team capacity, delaying reliable launch. | High | Prioritize by evidence and dependencies; deliver small pilot, defer nonessential features. | Product / Delivery | Investment decision |
| RSK-009 | Dependencies unavailable, prohibitively priced or incompatible in target territory. | High | Capability evidence, sandbox tests, contractual exit and fallback plans. | Commerce / Procurement | Vendor selection |
| RSK-010 | Inadequate backup, restore or incident response extends data loss/outage. | High | Define backup RPO/RTO separately from save durability and run timed restoration exercises. | SRE | Pilot entry |
| RSK-011 | AI or analytics uses content without valid consent or leaks prompts to third parties. | High | Defer AI; explicit purpose-specific opt-in, processor terms, data minimization and audit before enabling. | Privacy / AI Lead | Any AI launch |
| RSK-012 | Accessibility or RTL failures prevent authors or readers completing core journeys. | High | Keyboard, screen reader, mixed-script/IME and format testing; remediation gate. | Accessibility / QA | Pilot entry |

## Unresolved questions and references

All OQ entries are open. Actual owners must be appointed and milestone dates set by the Sponsor and Delivery Manager. The original decisions and risks are simulated drafting proposals; DEC-011 separately records a real user requirement and the implementer's stated interpretation. This register is not a legal opinion, a quantified risk assessment, or evidence of native language or specialist review. References are listed in the document header.
