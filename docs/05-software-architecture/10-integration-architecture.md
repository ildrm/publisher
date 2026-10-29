# ARC-10 — Integration architecture

Version 0.2 · 2026-10-29 · **Draft — simulated review; human approval pending**

Author/accountable: Solution Architect. Consulted: Document Engineer, Backend, Frontend, Conversion, Security, Accessibility, SRE, Editorial and Finance. Reviewer: Engineering Lead. Approver: Product Owner and Security/Finance/Editorial owners for their gates. Decision owner: Solution Architect. Assumptions: ASM-001–012 and proposed DEC-001–010; a text-centric single-imprint pilot, not approved market or capacity. Related requirements: FR-IAM-002, FR-DOC-002, FR-PUB-002, FR-COM-001, FR-FIN-001. References: [governance](../00-governance/02-decisions-and-open-questions.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md), [standards register](../01-discovery-strategy/07-standards-and-source-register.md).

## Partner qualification and adapter contract

| Adapter | Required evidence before commitment | Failure/exit behavior |
|---|---|---|
| Identity/email | Territory, recovery, MFA, domain verification, deliverability and export | Never grant access because email send succeeded; portable identity mapping and signed recovery workflow |
| Payment/payout | Legal entity/market eligibility, currency/tax handling, signatures, refunds, idempotency and sandbox statements | Ambiguous result reconciles before retry; provider-scoped external IDs and exportable ledger |
| Print/POD | Actual trim, binding, paper caliper, cover formula, color profile, bleed, accepted PDF profile and physical proof | No generic printer-ready claim; manual fulfillment fallback only after disclosed workflow |
| Distribution/retailer | Accepted EPUB/metadata/ONIX edition, territories, ISBN rules, accessible metadata, delivery/withdrawal receipts | Versioned payloads and status reconciliation; partner rejection never silently marked delivered |
| E-sign/rights | Signatory evidence, document versions, access/retention and export | Native evidence bundle and manual signed-contract path; legal review required |
| AI (deferred) | Provider terms, no-training/retention guarantees, jurisdiction, model version and evaluation | Explicit consent, budget limit, provider-specific failure, no silent data-routing change |
| Search/analytics | Index isolation, consent and deletion/opt-out behavior | Start relational search; rebuild projection from approved catalog; raw text excluded |
| Conversion/graphics | License, deterministic outputs, patching and resource limits | Canonical source/artifact manifest and replaceable worker; GLB optional |

Use typed adapters with provider error classifications, deadlines, circuit breakers and rate limits. Correlation and stable command keys cross retries; HTTP 200 from a transport does not imply successful publication or settlement. Secrets are per environment and adapter; workers do not inherit payment keys. Scheduled reconciliation compares internal status against partner receipts/settlements; DLQ replay requires a reviewed repair action, not changing the original audit event. External availability and vendor prices remain unknown until verified for OQ-005. Integration staging uses synthetic accounts/files and representative sanitized settlement reports, never production secrets or private drafts.

## Open decisions and cross-role review

Jurisdiction, partner eligibility, operational capacity and product targets remain decisions for their owners at market/vendor/architecture baseline milestones in the governance register. This design must be validated in a prototype and does not assert implemented security, compliance or performance. Architecture review: boundaries and invariants are explicit; Security review: deny-by-default and private data require adversarial testing; QA review: contracts and tests require integration evidence; Editorial/Finance review: release and posting rules require qualified human review. Approvals remain pending.
