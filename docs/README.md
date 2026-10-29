# DOC-000 — Publishing documentation manifest and executive brief

Version 0.2 · 2026-10-29 · **Draft — revised after cross-document review; human approval pending**. Author/accountable: Documentation Lead. Consulted: Product, Editorial, UX, Architecture, Security, Accessibility, Finance, QA, SRE and Delivery. Reviewer: Requirements Lead. Approver/decision owner: Product Owner and Executive Sponsor. Assumptions: ASM-001–012; related requirements: core FR/NFRs and the expansion capability register. Open decisions: launch market, capacity, rights/royalty terms, providers and implementation evidence. References: [source prompt](source/master-prompt.md), [decision register](00-governance/02-decisions-and-open-questions.md), [quality audit](QUALITY_AUDIT.md) and [change log](CHANGELOG.md).

## Contents

- [Executive brief](#executive-brief)
- [Review status and coverage](#review-status-and-coverage)
- [Required document manifest](#required-document-manifest)
- [Additional artifacts and checks](#additional-artifacts-and-checks)
- [Simulated review checkpoint](#simulated-review-checkpoint)

## Implementation checkpoint

A working local Author Studio now exists. See the [implementation guide](../implementation/README.md), [execution registry](../implementation/requirements-status.json), [test evidence](../implementation/test-evidence.md), and [remaining release gates](../implementation/release-readiness.md). The documentation review status below is not application completion or approval.

## Executive brief

The proposed model is a curated publishing house with a portable author studio. Authors can write and export without publishing. Staff evaluate frozen submissions and release only versions with scoped rights, approvals and proof. A modular monolith with isolated conversion workers is proposed to protect transaction consistency and limit deployment complexity; its alternatives and extraction triggers are documented. Private drafts are excluded from public indexes and default AI use. Editing semantics, immutable revisions, submissions, editions, renditions, listings, purchases and financial records remain distinct.

This repository contains documentation, diagram sources, contracts and bounded executable reference illustrations. It is a design draft; specialist approval and production behavior require real evidence. The full feature universe is mapped, while grouped expansion features still require atomic specifications and complete traceability before phase commitment.

## Review status and coverage

71 of 71 required named Markdown artifacts exist (100.0% file-presence coverage). This denominator excludes additional source/standard/audit files, diagrams, contracts and samples, which are listed below. Presence is not completeness, implementation or conformance coverage. The [18-gate quality audit](QUALITY_AUDIT.md) records corrected findings, partial criteria, owners and decision milestones.

| Batch | Result of this review | Remaining evidence |
|---|---|---|
| 0 Alignment | Registers, glossary, 22-role RACI and control process reviewed | Named human owners and actual decisions |
| 1 Discovery | Dated competitor matrix, standards, personas, journeys, unit economics and KPIs | Interviews, independent comparison, market/vendor eligibility |
| 2 Product | Core P0 clauses/scenarios, 175 expansion records, permissions, NFRs and recovery | Atomic expansion and full P1/P2 UI/API/test mappings |
| 3 Experience / publishing | 35 screen contracts, design/accessibility, formats, rights, proof, finance and 3D sources | Prototype/usability validation, physical proof, approved policies |
| 4 Architecture | Domain/data/ADR design, C4/UML/ERD, representative API/event/AST schemas | Rendering, full validator/toolchain and implemented integration proof |
| 5 Engineering / assurance | Handbook, reference examples, QA, security and operations runbooks | Actual system tests, accessibility/security and restore evidence |
| 6 Delivery | Three scope options, dependency roadmap, team ranges, RFP/scorecard, launch/exit plan and audit | Staffed estimates, bids and real approvals |

## Required document manifest

Entries marked Missing identify absent paths; present documents are drafts, and an entry does not imply approval.

### 00-governance

| Document | Status |
|---|---|
| [01-scope-and-assumptions.md](00-governance/01-scope-and-assumptions.md) | Draft; see audit for open work |
| [02-decisions-and-open-questions.md](00-governance/02-decisions-and-open-questions.md) | Draft; see audit for open work |
| [03-glossary-and-ubiquitous-language.md](00-governance/03-glossary-and-ubiquitous-language.md) | Draft; see audit for open work |
| [04-stakeholders-roles-raci.md](00-governance/04-stakeholders-roles-raci.md) | Draft; see audit for open work |
| [05-document-control-and-traceability.md](00-governance/05-document-control-and-traceability.md) | Draft; see audit for open work |

### 01-discovery-strategy

| Document | Status |
|---|---|
| [01-vision-value-proposition-and-positioning.md](01-discovery-strategy/01-vision-value-proposition-and-positioning.md) | Draft; see audit for open work |
| [02-market-and-competitor-evidence-matrix.md](01-discovery-strategy/02-market-and-competitor-evidence-matrix.md) | Draft; see audit for open work |
| [03-personas-jtbd-and-research-plan.md](01-discovery-strategy/03-personas-jtbd-and-research-plan.md) | Draft; see audit for open work |
| [04-business-model-and-unit-economics.md](01-discovery-strategy/04-business-model-and-unit-economics.md) | Draft; see audit for open work |
| [05-service-blueprints-and-user-journeys.md](01-discovery-strategy/05-service-blueprints-and-user-journeys.md) | Draft; see audit for open work |
| [06-product-kpis-and-analytics-plan.md](01-discovery-strategy/06-product-kpis-and-analytics-plan.md) | Draft; see audit for open work |

### 02-requirements

| Document | Status |
|---|---|
| [01-complete-prd.md](02-requirements/01-complete-prd.md) | Draft; see audit for open work |
| [02-system-requirements-specification-srs.md](02-requirements/02-system-requirements-specification-srs.md) | Draft; see audit for open work |
| [03-feature-catalog-and-prioritization.md](02-requirements/03-feature-catalog-and-prioritization.md) | Draft; see audit for open work |
| [04-epics-user-stories-and-gherkin.md](02-requirements/04-epics-user-stories-and-gherkin.md) | Draft; see audit for open work |
| [05-business-rules-and-permissions.md](02-requirements/05-business-rules-and-permissions.md) | Draft; see audit for open work |
| [06-nonfunctional-requirements-and-slos.md](02-requirements/06-nonfunctional-requirements-and-slos.md) | Draft; see audit for open work |
| [07-error-recovery-and-edge-cases.md](02-requirements/07-error-recovery-and-edge-cases.md) | Draft; see audit for open work |

### 03-experience-design

| Document | Status |
|---|---|
| [01-information-architecture-and-sitemaps.md](03-experience-design/01-information-architecture-and-sitemaps.md) | Draft; see audit for open work |
| [02-navigation-and-journey-flows.md](03-experience-design/02-navigation-and-journey-flows.md) | Draft; see audit for open work |
| [03-screen-inventory-and-screen-specs.md](03-experience-design/03-screen-inventory-and-screen-specs.md) | Draft; see audit for open work |
| [04-design-system-and-design-tokens.md](03-experience-design/04-design-system-and-design-tokens.md) | Draft; see audit for open work |
| [05-interaction-and-content-guidelines.md](03-experience-design/05-interaction-and-content-guidelines.md) | Draft; see audit for open work |
| [06-accessibility-and-i18n-specification.md](03-experience-design/06-accessibility-and-i18n-specification.md) | Draft; see audit for open work |
| [07-wireframes-and-prototype-checklist.md](03-experience-design/07-wireframes-and-prototype-checklist.md) | Draft; see audit for open work |

### 04-publishing-domain

| Document | Status |
|---|---|
| [01-editorial-publishing-workflow.md](04-publishing-domain/01-editorial-publishing-workflow.md) | Draft; see audit for open work |
| [02-structured-manuscript-and-asset-model.md](04-publishing-domain/02-structured-manuscript-and-asset-model.md) | Draft; see audit for open work |
| [03-formats-typography-and-conversion.md](04-publishing-domain/03-formats-typography-and-conversion.md) | Draft; see audit for open work |
| [04-print-preflight-and-proofing.md](04-publishing-domain/04-print-preflight-and-proofing.md) | Draft; see audit for open work |
| [05-rights-contracts-and-metadata.md](04-publishing-domain/05-rights-contracts-and-metadata.md) | Draft; see audit for open work |
| [06-distribution-commerce-and-royalties.md](04-publishing-domain/06-distribution-commerce-and-royalties.md) | Draft; see audit for open work |
| [07-three-d-visualization-and-asset-pipeline.md](04-publishing-domain/07-three-d-visualization-and-asset-pipeline.md) | Draft; see audit for open work |

### 05-software-architecture

| Document | Status |
|---|---|
| [01-architecture-vision-and-quality-attributes.md](05-software-architecture/01-architecture-vision-and-quality-attributes.md) | Draft; see audit for open work |
| [02-domain-boundaries-and-context-map.md](05-software-architecture/02-domain-boundaries-and-context-map.md) | Draft; see audit for open work |
| [03-c4-context-container-component.md](05-software-architecture/03-c4-context-container-component.md) | Draft; see audit for open work |
| [04-uml-and-erd-index.md](05-software-architecture/04-uml-and-erd-index.md) | Draft; see audit for open work |
| [05-database-and-migrations.md](05-software-architecture/05-database-and-migrations.md) | Draft; see audit for open work |
| [06-api-contracts-and-event-schemas.md](05-software-architecture/06-api-contracts-and-event-schemas.md) | Draft; see audit for open work |
| [07-document-sync-autosave-and-conflict-handling.md](05-software-architecture/07-document-sync-autosave-and-conflict-handling.md) | Draft; see audit for open work |
| [08-export-and-async-job-architecture.md](05-software-architecture/08-export-and-async-job-architecture.md) | Draft; see audit for open work |
| [09-data-privacy-security-and-threat-model.md](05-software-architecture/09-data-privacy-security-and-threat-model.md) | Draft; see audit for open work |
| [10-integration-architecture.md](05-software-architecture/10-integration-architecture.md) | Draft; see audit for open work |
| [11-architecture-decision-records.md](05-software-architecture/11-architecture-decision-records.md) | Draft; see audit for open work |

### 06-engineering-handbook

| Document | Status |
|---|---|
| [01-reference-stack-and-tradeoffs.md](06-engineering-handbook/01-reference-stack-and-tradeoffs.md) | Draft; see audit for open work |
| [02-repository-module-boundaries.md](06-engineering-handbook/02-repository-module-boundaries.md) | Draft; see audit for open work |
| [03-clean-code-and-coding-standards.md](06-engineering-handbook/03-clean-code-and-coding-standards.md) | Draft; see audit for open work |
| [04-coding-patterns-and-anti-patterns.md](06-engineering-handbook/04-coding-patterns-and-anti-patterns.md) | Draft; see audit for open work |
| [05-example-code-and-contracts.md](06-engineering-handbook/05-example-code-and-contracts.md) | Draft; see audit for open work |
| [06-git-pr-review-and-definition-of-done.md](06-engineering-handbook/06-git-pr-review-and-definition-of-done.md) | Draft; see audit for open work |
| [07-database-schema-and-versioning-standards.md](06-engineering-handbook/07-database-schema-and-versioning-standards.md) | Draft; see audit for open work |
| [08-ai-coding-agent-instructions.md](06-engineering-handbook/08-ai-coding-agent-instructions.md) | Draft; see audit for open work |

### 07-assurance

| Document | Status |
|---|---|
| [01-test-strategy-and-quality-gates.md](07-assurance/01-test-strategy-and-quality-gates.md) | Draft; see audit for open work |
| [02-functional-integration-e2e-test-catalog.md](07-assurance/02-functional-integration-e2e-test-catalog.md) | Draft; see audit for open work |
| [03-book-format-and-print-fidelity-test-plan.md](07-assurance/03-book-format-and-print-fidelity-test-plan.md) | Draft; see audit for open work |
| [04-security-privacy-and-abuse-test-plan.md](07-assurance/04-security-privacy-and-abuse-test-plan.md) | Draft; see audit for open work |
| [05-accessibility-localization-and-browser-matrix.md](07-assurance/05-accessibility-localization-and-browser-matrix.md) | Draft; see audit for open work |
| [06-performance-load-resilience-and-dr-plan.md](07-assurance/06-performance-load-resilience-and-dr-plan.md) | Draft; see audit for open work |
| [07-requirements-to-test-traceability.md](07-assurance/07-requirements-to-test-traceability.md) | Draft; see audit for open work |

### 08-operations

| Document | Status |
|---|---|
| [01-cloud-deployment-and-environments.md](08-operations/01-cloud-deployment-and-environments.md) | Draft; see audit for open work |
| [02-cicd-and-supply-chain-security.md](08-operations/02-cicd-and-supply-chain-security.md) | Draft; see audit for open work |
| [03-observability-slos-and-incident-response.md](08-operations/03-observability-slos-and-incident-response.md) | Draft; see audit for open work |
| [04-backup-restore-and-business-continuity.md](08-operations/04-backup-restore-and-business-continuity.md) | Draft; see audit for open work |
| [05-data-retention-and-customer-support-runbooks.md](08-operations/05-data-retention-and-customer-support-runbooks.md) | Draft; see audit for open work |
| [06-capacity-cost-and-finops.md](08-operations/06-capacity-cost-and-finops.md) | Draft; see audit for open work |

### 09-delivery-and-procurement

| Document | Status |
|---|---|
| [01-rfp-and-vendor-response-template.md](09-delivery-and-procurement/01-rfp-and-vendor-response-template.md) | Draft; see audit for open work |
| [02-scope-phases-roadmap-and-dependencies.md](09-delivery-and-procurement/02-scope-phases-roadmap-and-dependencies.md) | Draft; see audit for open work |
| [03-team-plan-estimates-and-critical-path.md](09-delivery-and-procurement/03-team-plan-estimates-and-critical-path.md) | Draft; see audit for open work |
| [04-risk-register-and-mitigation.md](09-delivery-and-procurement/04-risk-register-and-mitigation.md) | Draft; see audit for open work |
| [05-acceptance-milestones-and-exit-criteria.md](09-delivery-and-procurement/05-acceptance-milestones-and-exit-criteria.md) | Draft; see audit for open work |
| [06-pilot-launch-growth-and-operations-readiness.md](09-delivery-and-procurement/06-pilot-launch-growth-and-operations-readiness.md) | Draft; see audit for open work |

## Additional artifacts and checks

- [Standards/source register](01-discovery-strategy/07-standards-and-source-register.md), [source prompt](source/master-prompt.md) and [source hash/required-path manifest](document-manifest.json).
- [Diagram index](05-software-architecture/04-uml-and-erd-index.md), [C4 architecture](05-software-architecture/03-c4-context-container-component.md) and actual sources in `diagrams/`.
- [OpenAPI](contracts/openapi.yaml), [AsyncAPI](contracts/asyncapi.yaml), [AST schema](contracts/schemas/manuscript-ast.v1.schema.json), [event schema](contracts/schemas/revision-saved.v1.schema.json) and [event fixture](contracts/schemas/revision-saved.v1.json).
- [Reference sample context and test instructions](samples/reference/README.md), [autosave controller](samples/frontend-autosave.mjs), [quality audit](QUALITY_AUDIT.md), [structural validation report](validation-report.json) and [change log](CHANGELOG.md).

From the repository root:

```sh
python3 scripts/update_docs_manifest.py
python3 scripts/validate_docs.py --write-report
python3 -m unittest discover -s docs/samples/tests -t docs/samples -v
node --test docs/samples/tests/autosave.test.mjs
```

The structural checker verifies file presence, relative link targets, IDs, JSON/local references, selected API rules, a bounded event fixture and PlantUML block delimiters. It does not render diagrams or fully validate OpenAPI/AsyncAPI against their standards. The sample tests exercise teaching code, not an implemented publishing service. Exact evidence and limitations are in the audit and report.

## Simulated review checkpoint

Product/Requirements corrected scope and traceability conflicts; UX/Publishing corrected screen validation, rights and proof flow; Architecture/Security corrected authorization and retry boundaries; Finance clarified balanced postings and reconciliation; QA/Delivery made validation, milestones and unresolved evidence explicit. Residual risks and required human approvers are recorded in the quality audit and governance register. No real specialist or stakeholder approval is implied.
