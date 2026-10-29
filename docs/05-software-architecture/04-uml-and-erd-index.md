# ARC-04 — UML and ERD index

Version 0.2 · 2026-10-29 · **Draft — simulated review; human approval pending**

Author/accountable: Solution Architect. Consulted: Document Engineer, Backend, Frontend, Conversion, Security, Accessibility, SRE, Editorial and Finance. Reviewer: Engineering Lead. Approver: Product Owner and Security/Finance/Editorial owners for their gates. Decision owner: Solution Architect. Assumptions: ASM-001–012 and proposed DEC-001–010; a text-centric single-imprint pilot, not approved market or capacity. Related requirements: FR-IAM-002, FR-DOC-002, FR-PUB-002, FR-COM-001, FR-FIN-001. References: [governance](../00-governance/02-decisions-and-open-questions.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md), [standards register](../01-discovery-strategy/07-standards-and-source-register.md).

## Required diagram coverage

All PlantUML files use local built-in syntax without remote includes. Mermaid files represent C4/ERD/flow views. Sources include scope, IDs, requirement references and legends. `SOURCE NOT RENDER-VALIDATED` means syntax rendering has not been demonstrated; delimiter and link checks are weaker checks only. The Java launcher exists, but java -version could not locate a Java runtime; no PlantUML JAR or Mermaid CLI was found in the workspace/tool PATH.

| View | Source | Explanation |
|---|---|---|
| Use cases | [uml-use-cases.puml](../diagrams/uml-use-cases.puml) | Actor-scoped author, editorial, commerce and operations capabilities |
| Domain classes | [uml-domain.puml](../diagrams/uml-domain.puml) | Distinguishes work, revision, submission, edition, rendition, listing, purchase and ledger |
| Relational model | [erd.mmd](../diagrams/erd.mmd) | Primary keys, scoped foreign keys and cardinalities; full dictionary in ARC-05 |
| Sequences | [uml-sequences.puml](../diagrams/uml-sequences.puml) | Ten named interactions: import, save, reconnect, restore, export, editorial release, purchase, refund, royalty/payout, 3D |
| States | [uml-states.puml](../diagrams/uml-states.puml) | Nine lifecycle machines, explicit guards and irreversible history |
| Activities | [uml-activities.puml](../diagrams/uml-activities.puml) | Acquisition, print proof and author journey |
| Deployment | [uml-deployment.puml](../diagrams/uml-deployment.puml) | Network trust, worker identity, private store, backups and optional regional recovery |
| Threat/data flow | [data-flow.mmd](../diagrams/data-flow.mmd) | Import, AI opt-in, release and purchased delivery trust boundaries |
| Events/consistency | [events.mmd](../diagrams/events.mmd) | Outbox/inbox, retries, poison messages and reconciliation |

Additional UX/publishing sources use `ux-`/`pub-` prefixes and are indexed by their documents. State transitions are normative proposals; diagram arrows do not authorize actions unless the [permission rules](../02-requirements/05-business-rules-and-permissions.md) allow them. New states/events must update diagrams, schema, migration and test traceability together.

## Open decisions and cross-role review

Jurisdiction, partner eligibility, operational capacity and product targets remain decisions for their owners at market/vendor/architecture baseline milestones in the governance register. This design must be validated in a prototype and does not assert implemented security, compliance or performance. Architecture review: boundaries and invariants are explicit; Security review: deny-by-default and private data require adversarial testing; QA review: contracts and tests require integration evidence; Editorial/Finance review: release and posting rules require qualified human review. Approvals remain pending.
