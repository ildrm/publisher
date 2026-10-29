# ARC-03 — C4 context, container and component views

Version 0.2 · 2026-10-29 · **Draft — simulated review; human approval pending**

Author/accountable: Solution Architect. Consulted: Document Engineer, Backend, Frontend, Conversion, Security, Accessibility, SRE, Editorial and Finance. Reviewer: Engineering Lead. Approver: Product Owner and Security/Finance/Editorial owners for their gates. Decision owner: Solution Architect. Assumptions: ASM-001–012 and proposed DEC-001–010; a text-centric single-imprint pilot, not approved market or capacity. Related requirements: FR-IAM-002, FR-DOC-002, FR-PUB-002, FR-COM-001, FR-FIN-001. References: [governance](../00-governance/02-decisions-and-open-questions.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md), [standards register](../01-discovery-strategy/07-standards-and-source-register.md).

## Architecture view index

| ID | Source | Scope and requirements |
|---|---|---|
| C4-001 | [Context](../diagrams/c4-context.mmd) | Actors and partner systems; FR-EXP-001, FR-PUB-002, FR-COM-001 |
| C4-002 | [Containers](../diagrams/c4-container.mmd) | Private/public stores, API and worker isolation; FR-IAM-002, FR-FMT-001 |
| C4-003 | [Components](../diagrams/c4-component.mmd) | Authoring, edition and finance boundaries; FR-DOC-002, FR-PUB-002, FR-FIN-001 |

These Mermaid flowcharts encode C4 abstraction levels and responsibilities; they are C4-style architecture views, not UML. Legends identify external systems, private stores and optional/deferred components. The realtime service and AI provider are deferred; cache and separate search engine are conditional optimizations. The public CDN serves only released covers/samples and entitled delivery is authorized through the API. See [domain boundaries](02-domain-boundaries-and-context-map.md) for table ownership and events.

## Container responsibilities

Browser shells share identity and design tokens while exposing separate Author, Publisher, Reader and Admin navigation. The browser has no database or public storage credentials. API modules own policies and commands; relational data stores business state and outbox; private object storage holds manuscript versions and artifacts. Queue payloads contain identifiers and input hashes, not entire manuscripts. Workers get short-lived job-scoped access and cannot enumerate tenant storage or call arbitrary network endpoints. Metrics/logs are redacted; object paths and user content are not metric labels.

Sources carry render-validation status. No diagram is evidence of deployed controls.

## Open decisions and cross-role review

Jurisdiction, partner eligibility, operational capacity and product targets remain decisions for their owners at market/vendor/architecture baseline milestones in the governance register. This design must be validated in a prototype and does not assert implemented security, compliance or performance. Architecture review: boundaries and invariants are explicit; Security review: deny-by-default and private data require adversarial testing; QA review: contracts and tests require integration evidence; Editorial/Finance review: release and posting rules require qualified human review. Approvals remain pending.
