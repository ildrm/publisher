# ARC-11 — Architecture decision records

Version 0.2 · 2026-10-29 · **Draft — simulated review; human approval pending**

Author/accountable: Solution Architect. Consulted: Document Engineer, Backend, Frontend, Conversion, Security, Accessibility, SRE, Editorial and Finance. Reviewer: Engineering Lead. Approver: Product Owner and Security/Finance/Editorial owners for their gates. Decision owner: Solution Architect. Assumptions: ASM-001–012 and proposed DEC-001–010; a text-centric single-imprint pilot, not approved market or capacity. Related requirements: FR-IAM-002, FR-DOC-002, FR-PUB-002, FR-COM-001, FR-FIN-001. References: [governance](../00-governance/02-decisions-and-open-questions.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md), [standards register](../01-discovery-strategy/07-standards-and-source-register.md).

## ADR register

These ADRs elaborate governance proposals; they are **proposed**, not separately approved decisions. Approvers must record evidence and revision when accepting. Every ADR has reversal cost and explicit trigger.

| ADR / governance | Decision, alternatives and consequence | Evidence / reversal trigger |
|---|---|---|
| ADR-001 / DEC-002 | Modular monolith + isolated workers over distributed services; avoids cross-service save/financial transactions while requiring enforceable module interfaces | Benchmark and deployment ownership review; extract when measured contention or regulatory boundaries demand |
| ADR-002 / DEC-004 | Versioned semantic AST over arbitrary HTML; import adapters disclose unsupported constructs; canonical migrations and editor integration cost are accepted | Round-trip corpus, RTL/IME/footnotes and long document spike; reopen if nontext vertical requires distinct schema |
| ADR-003 / DEC-005 | Optimistic chapter version and manual stale-write recovery for pilot; OT/CRDT deferred | Duplicate/lost-response/race tests; reopen if realtime is essential and correct merge demonstrated |
| ADR-004 / DEC-006 | Private object storage and physically/logically separate public projection; public search cannot query private content | Cross-tenant/search canary tests and support access audit; revisit for new content-sharing feature |
| ADR-005 / DEC-007 | Immutable manifest/checksum-bound rendition and version-specific approvals; no mutable “latest.pdf” release pointer | Reproducibility and physical proof evidence; changes require new release manifest |
| ADR-006 / DEC-008 | Balanced ledger by currency and unique event keys; refunds compensate rather than edit history | Accountant sign-off and duplicate/partial settlement tests; complex advances/FX need new rules |
| ADR-007 / DEC-010 | OpenAPI 3.1.1 / AsyncAPI 3.0.0 representative contracts; select stable tooling compatibility over newest spec automatically | Official standards register and validator/client-generation spike; upgrade with consumer compatibility tests |
| ADR-008 / DEC-009 | 2D/text baseline; optional dimensional 3D without automatic animation; no promise that a mockup is a manufacturing proof | Device, accessibility and vendor geometry tests; AR/page-turn separate discovery |

## Change procedure

Record context, affected requirements, options, tradeoff, data/security implications, migration/rollback, test evidence, owner and approver in each ADR update. No rewrite of historical decision status: supersede and link. Unknown license, vendor access or standards support is an open item with owner/milestone, not a fabricated reason to approve. At architecture baseline, create signed-off evidence for chosen editor/stack, durable storage failure model, provider market access and conversion quality. Current stack comparisons are in the [handbook](../06-engineering-handbook/01-reference-stack-and-tradeoffs.md).

## Open decisions and cross-role review

Jurisdiction, partner eligibility, operational capacity and product targets remain decisions for their owners at market/vendor/architecture baseline milestones in the governance register. This design must be validated in a prototype and does not assert implemented security, compliance or performance. Architecture review: boundaries and invariants are explicit; Security review: deny-by-default and private data require adversarial testing; QA review: contracts and tests require integration evidence; Editorial/Finance review: release and posting rules require qualified human review. Approvals remain pending.
