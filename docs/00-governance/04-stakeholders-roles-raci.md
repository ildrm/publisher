# GOV-004 — Stakeholders, accountable roles and RACI

- **Version / date:** 0.2 / 2026-10-29
- **Status:** Draft — simulated roles, not staffed, reviewed or approved
- **Authoring / accountable role:** Chief Product Manager / Product Owner
- **Consulted roles:** All 22 perspectives below; consultation is simulated, not a claim that people were consulted.
- **Reviewer / approver / decision owner:** Delivery Manager / Executive Sponsor / Product Owner; actual appointments pending
- **Assumptions:** ASM-011–012; one person may hold multiple roles if capacity and independence are adequate.
- **Related requirements:** Source prompt §§1, 6, 14–15; the draft [feature catalog](../02-requirements/03-feature-catalog-and-prioritization.md) and [SRS](../02-requirements/02-system-requirements-specification-srs.md) exist; role-to-requirement traceability is incomplete.
- **References:** [scope](01-scope-and-assumptions.md); [decision and risk registers](02-decisions-and-open-questions.md); [document control](05-document-control-and-traceability.md); source master prompt v1.0.

## Role roster

Roles are accountability assignments to be filled by real people; none of these labels implies a human expert performed work or granted approval.

| # | Perspective | Responsibility |
|---|---|---|
| 1 | Executive Sponsor / Publishing Director (Sponsor) | Business strategy, imprint policy, investment and publishing guardrails. |
| 2 | Chief Product Manager / Product Owner (Product) | Outcomes, scope, priorities and release acceptance. |
| 3 | Senior Business Analyst / Requirements Engineer (BA) | Atomic requirements, business rules and traceability. |
| 4 | UX Researcher / Service Designer (Research) | Personas, evidence, service journeys and research. |
| 5 | Editorial & Publishing Operations Lead (Editorial) | Acquisition, review, production and publishing operations. |
| 6 | Book Designer / Print Production Expert (Print) | Typography, print configuration, physical proofs and production quality. |
| 7 | Lead UX/UI and Design-System Designer (Design) | Interaction, visual system, navigation and usable content. |
| 8 | Accessibility and Internationalization Specialist (A11y) | Accessibility, international text, assistive technology and localization. |
| 9 | Principal Software / Solution Architect (Architect) | Architecture, quality attributes, domain boundaries and decisions. |
| 10 | Frontend Engineering Lead (Frontend) | Application shell, editor/reader integration and browser behavior. |
| 11 | Structured Document & Real-Time Collaboration Engineer (Document) | Editor schema, save, versioning, collaboration and recovery. |
| 12 | Backend/API Engineering Lead (Backend) | Business services, authorization, APIs and transactions. |
| 13 | Publishing Conversion / Typesetting Engineer (Conversion) | Semantic transformations, workers, outputs and validators. |
| 14 | 3D/Web Graphics Engineer (3D) | Dimension-based graphics, performance and fallback. |
| 15 | AI/ML and Responsible AI Engineer (AI) | Optional consent-governed assistance, provenance and evaluations. |
| 16 | Search / Data / Analytics Engineer (Data) | Index isolation, metrics and privacy-conscious analytics. |
| 17 | Commerce / Integration Engineering Lead (Commerce) | Payment, printing, delivery, integrations and webhook reliability. |
| 18 | Finance / Royalty Accounting Specialist (Finance) | Royalty rules, ledger, settlement, payout and reconciliation. |
| 19 | Security, Privacy, IP and Legal Advisory Team (Security/Legal) | Threats, privacy, rights and jurisdiction-specific advice; independent qualified counsel required. |
| 20 | DevOps / SRE Lead (SRE) | Operations, deployments, observability and restore. |
| 21 | QA / Test Automation and Quality Engineering Lead (QA) | Risk-based test plans, release evidence and defects. |
| 22 | Growth / SEO / Community and Customer Success Lead (Growth) | Acquisition, discovery, community, support and customer feedback. |

**Additional assigned responsibilities:** Delivery Manager (may be shared with Product) maintains dependencies, milestones and change control. Design owns content/design writing with Editorial and A11y consultation. Technical Documentation Maintainer (may be shared with BA) maintains the repository manifest, version history, glossary change log and broken-link report; domain leads own technical accuracy. These assignments must be confirmed and funded, not presumed sufficient staffing.

## RACI by deliverable and decision

A = accountable for the decision; R = responsible for producing it; C = consulted before decision; I = informed. One A per row; responsibility can be shared. This is a proposed operating model and never substitutes for required independent professional review.

| Deliverable or decision | A | R | C | I |
|---|---|---|---|---|
| Business model and investment | Sponsor | Product, Delivery | Finance, Editorial, Legal, Research | All leads |
| Scope and prioritized requirements | Product | BA | Research, Editorial, Architect, QA, A11y | Sponsor, Delivery |
| Research and competitive evidence | Product | Research | Growth, Editorial, Data | Sponsor, Design |
| Editorial acceptance and proof | Editorial | Editorial, Print | Author, Conversion, Legal | Product, Sponsor |
| Rights and contract policy | Sponsor | Legal, Editorial | Finance, author representative | Product, Commerce |
| Product interaction and content | Design | Design, Frontend | A11y, Research, Editorial | Product, QA |
| Domain architecture and API | Architect | Backend, Document, Conversion | Security, SRE, Commerce, A11y | Product, QA |
| Manuscript save and recovery | Document | Document, Backend, SRE | Architect, QA, Security | Product, Support |
| Conversion and print fidelity | Conversion | Conversion, Print | A11y, Editorial, QA | Architect, Product |
| 3D dimensions and fallback | Print | 3D, Frontend | A11y, Editorial, QA | Product |
| Privacy and security control design | Security/Legal | Security, Backend, SRE | Legal counsel, Document, Data, QA | Sponsor, Product |
| Royalty and financial reconciliation | Finance | Finance, Commerce | Legal, Backend, QA | Sponsor, Editorial |
| Release quality recommendation | QA | QA, domain leads | Product, SRE, Security, A11y, Editorial, Finance | Sponsor |
| Launch go/no-go | Product | Delivery, QA | Sponsor, Legal, Security, A11y, Finance, Editorial, SRE | All stakeholders |
| Documentation, IDs and glossary | BA | Technical Documentation Maintainer | Domain leads, Product | Delivery, QA |
| Support and incident communication | SRE | SRE, Growth/Support | Security, Legal, Product | Sponsor and affected stakeholders |

## Unresolved questions

OQ-010: the Sponsor and Delivery Manager must appoint named people, confirm capacity and authorize decision rights before the investment decision. Required independent specialist approvals are not yet recorded.

## Review and approval boundaries

Each document records authoring/accountable role, consulted roles, reviewer, approver, decision owner, status and outstanding questions. Simulation can identify concerns, but only a real authorized stakeholder may change status to reviewed or approved. Legal advice, tax determinations, financial controls, accessibility conformance, security certifications and physical proof acceptance require independent real-world evidence and appropriate qualified approval. Product launch cannot waive those approvals implicitly. OQ-010 remains open until real stakeholders, staffing and decision authorities are named.
