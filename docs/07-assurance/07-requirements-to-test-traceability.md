# QA-07 — Requirements-to-test traceability

Version 0.2 · 2026-10-29 · **Draft — unexecuted** · Author: Requirements Engineer · Accountable/decision owner: QA Lead · Consulted: Product, Architecture, Security, Editorial, Finance, Accessibility · Reviewer: Product Owner · Approver required: QA Lead and Product Owner

Assumptions: proposed balanced pilot and the core IDs in [REQ-03](../02-requirements/03-feature-catalog-and-prioritization.md). Related requirements: core FRs and NFRs listed below; see [acceptance scenarios](../02-requirements/04-epics-user-stories-and-gherkin.md), [NFRs](../02-requirements/06-nonfunctional-requirements-and-slos.md), [test catalog](02-functional-integration-e2e-test-catalog.md). Open questions: actual screen, API and domain implementation, executed results, staff and launch jurisdiction; owners QA and Product before pilot. A mapping is a planned test, not a passing test.

## Pilot feature links

Screen IDs are provisional design references. Use `TC-<FR ID>-P`, `-N`, and `-R` for positive, negative and boundary/race/network cases; REQ-04 gives narrative acceptance and test fixtures. P0 release milestone is pilot, subject to sizing and approval. Product goals below refer to DISC-06 outcomes.

| Goal / requirement | Screens | Domain / primary object and role | Planned tests | Status |
|---|---|---|---|---|
| Trust / FR-IAM-001 | SCR-003 | Identity / User; author, privileged staff | TC-FR-IAM-001-P/N/R | Draft |
| Trust / FR-IAM-002 | SCR-034 | Authorization / Membership; owner, collaborator | TC-FR-IAM-002-P/N/R | Draft |
| Activation / FR-DOC-001 | SCR-004, SCR-005, SCR-007 | Authoring / Project, Chapter; owner | TC-FR-DOC-001-P/N/R | Draft |
| Durability / FR-DOC-002 | SCR-007 | Authoring / ManuscriptVersion; authorized writer | TC-FR-DOC-002-P/N/R | Draft |
| Recovery / FR-DOC-003 | SCR-007 | Authoring / ManuscriptVersion; owner or granted writer | TC-FR-DOC-003-P/N/R | Draft |
| Portability / FR-IMP-001 | SCR-012 | Import / ConversionJob, Project; owner | TC-FR-IMP-001-P/N/R | Draft |
| Portability / FR-EXP-001 | SCR-012 | Export / ConversionJob, ExportArtifact; owner | TC-FR-EXP-001-P/N/R | Draft |
| Submission / FR-PUB-001 | SCR-016, SCR-018 | Editorial / Submission, ManuscriptVersion; author/editor | TC-FR-PUB-001-P/N/R | Draft |
| Safe release / FR-PUB-002 | SCR-020, SCR-023 | Publication / Edition, approval; publisher admin | TC-FR-PUB-002-P/N/R | Draft |
| Rights / FR-RGT-001 | SCR-021 | Rights / RightsGrant; rights officer | TC-FR-RGT-001-P/N/R | Draft |
| Fidelity / FR-FMT-001 | SCR-013, SCR-020 | Production / Rendition, ConversionJob; production staff | TC-FR-FMT-001-P/N/R | Draft |
| Discovery / FR-CAT-001, including 2D/text FR-CAT-001.2 | SCR-025, SCR-026 | Catalog / CatalogListing; public reader | TC-FR-CAT-001-P/N/R | Draft |
| Purchase / FR-COM-001 | SCR-027, SCR-028 | Commerce / Order, Payment, Entitlement; customer | TC-FR-COM-001-P/N/R | Draft |
| Financial integrity / FR-FIN-001 | SCR-031, SCR-032 | Finance / LedgerEntry, RoyaltyStatement, Payout; finance | TC-FR-FIN-001-P/N/R | Draft |
| Recovery / FR-OPS-001 | SCR-035 | Operations / AuditEvent, backup; scoped operator | TC-FR-OPS-001-P/N/R | Draft |
| Optional preview / FR-3D-001 (P1) | SCR-015, SCR-026 | Visualization / 3DModelArtifact; author/reader | TC-FR-3D-001-P/N/R | Draft; 2D baseline in pilot |

### Planned API operation mapping

These operation IDs cross-reference the draft [OpenAPI contract](../contracts/openapi.yaml). Local structural checks confirm declared names; authorization, inputs/outputs and runtime behavior still require implementation and contract tests. Coverage is partial, and names do not imply a running service.

| Core requirement | Planned operation IDs | Explicit gap |
|---|---|---|
| FR-IAM-001 / FR-IAM-002 | `grantMembership`, `revokeMembership` | Identity provider/recovery flows remain external or unspecified; membership scope and revocation race tests required. |
| FR-DOC-001 | `createProject` | getChapter covers a single chapter read; chapter creation/reorder, manuscript-version read and authorization tests still need coverage. |
| FR-DOC-002 | `saveChapter` | Durable acknowledgement, recovery status and retry semantics require tested contract. |
| FR-DOC-003 | `restoreRevision` | Snapshot creation/list and history access need contract coverage. |
| FR-IMP-001 | `initiateUpload`, `completeUpload`, `createImport`, `confirmImport`, `getJob` | getJob provides a completed import report and source artifact; safety, warning fidelity, confirmation and source recovery still require runtime evidence. |
| FR-EXP-001 | `createExport`, `getJob`, `redeemArtifact` | Formats, job permissions and artifact expiry require review. |
| FR-PUB-001 | `createSubmission`, `decideSubmission` | Assignment and notification delivery need further contracts. |
| FR-PUB-002 | `getEdition`, `approveEdition`, `releaseEdition`, `holdEdition` | Approval scopes, proof evidence and reinstatement need deeper contracts/tests. |
| FR-RGT-001 | `recordRights` | Validity, contributor/asset evidence, rights query and disputes need deeper contracts. |
| FR-FMT-001 | `createExport`, `getJob`, `redeemArtifact` | Production presets, approval and immutable rendition workflow require contract. |
| FR-CAT-001 and FR-CAT-001.2 | `listCatalog` | listCatalog requires 2D URL/alt; dedicated detail/sample operations and stale-index authorization still need deeper contract/tests. |
| FR-COM-001 | `createCheckout`, `receivePaymentEvent` | Provider capture/reconciliation, entitlement and download contract require design. |
| FR-FIN-001 | `postRoyalty`, `createPayout`, `refundPayment` | Settlement import, approval and reconciliation require deeper contracts. |
| FR-OPS-001 | `getAudit` | Protected audit writes, backup and restore remain operational contracts, not implied by read access. |
| FR-3D-001 | No operation supplied | Optional P1 geometry, assets and fallback contracts are unresolved. |

HTTP endpoints and event contracts remain design references until implemented and verified. Proposed NFR checks follow `TC-<NFR ID>` and require measured evidence from [performance/resilience plan](06-performance-load-resilience-and-dr-plan.md). Full-domain P1/P2 requirements require equivalent mappings before their release.

## Broken links and risk exceptions

| Issue | Severity / owner | Resolution milestone |
|---|---|---|
| TRC-001: named UI screens are specifications, not implemented or tested screens | High / UX and QA | Pilot readiness |
| TRC-002: API operation and event links need reconciliation with reviewed contracts | High / API lead | Contract baseline before implementation |
| TRC-003: P1/P2 feature-level test, route, permission and data mappings are incomplete | High / Requirements lead | Before corresponding phase commitment |
| TRC-004: only bounded reference-example tests have executed; production tests, proofs, conformance audits and provider reconciliation evidence are absent | Critical / QA and release owner | Before launch approval |

## Review checkpoint

| Role | Concern / response | Residual risk | Approver |
|---|---|---|---|
| QA | Scenario links are planned, not results | No execution or evidence | QA Lead |
| Product | Broad scope may exceed pilot capacity | Release cutoff remains undecided | Product Owner |
| Finance and Security | Permission and financial mappings require negative testing | Partner behavior and local rules unknown | Finance and Security leads |

References: [DISC-06 KPI definitions](../01-discovery-strategy/06-product-kpis-and-analytics-plan.md); REQ-03, REQ-04 and REQ-06 linked above.
