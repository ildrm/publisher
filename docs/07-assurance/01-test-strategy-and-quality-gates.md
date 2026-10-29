# QA-01 — Test strategy and quality gates

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: QA Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: QA Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002–003, FR-RGT-001, FR-PUB-002, FR-COM-001, FR-FIN-001; NFR-REL-001–004.

## Risk-based approach

Unit tests exercise domain invariants and validation; contract tests enforce API and event shapes, versioning and authorization errors; integration tests use isolated stores and provider sandboxes; browser end-to-end tests cover author, publisher and reader journeys. The release suite must also execute fault-injected persistence, restore, hostile imports, format validation, accessibility/RTL and financial reconciliation. Prioritize irreversible author loss, privacy breaches, unauthorized publication and financial misposting above convenience regressions. See [functional cases](02-functional-integration-e2e-test-catalog.md), [security cases](04-security-privacy-and-abuse-test-plan.md), [format plan](03-book-format-and-print-fidelity-test-plan.md), and [resilience](06-performance-load-resilience-and-dr-plan.md).

Test data uses synthetic manuscripts with seeded unique canaries, representative scripts and formatting, deliberately invalid assets, synthetic identities and ledger fixtures. No production manuscript, real payment data, or real provider credentials enter shared test environments. Test owner records environment, fixture version, steps, actual result, evidence and defect ID; proposed cases are not results.

## Gates and severity

Definition of Ready: independently testable acceptance, owner, role/permissions, privacy classification, failure/rollback plan and dependencies agreed. Definition of Done: reviewed change, unit and contract checks, migration and rollback reviewed, accessible states, privacy/security checks, telemetry, runbook and trace links updated. CI blocks on compile, lint, unit/contract, dependency and secret checks; staged integration/E2E, a11y and security gates run before release. Formal accessibility and penetration testing require qualified reviewers and are not replaced by automated checks.

S1 is data loss, private exposure, unauthorized publication or incorrect money: block launch; S2 blocks a core workflow: block affected launch; S3 degrades a workaround: owner-approved deferral; S4 is cosmetic. Exceptions name owner, impact, mitigation and expiry; never waive save durability or financial integrity. Independent Product, Security, Editorial, Finance and SRE approvals and demonstrated rollback/restore are required before production. Pilot exit additionally requires reviewed user tasks and no unresolved S1/S2. A suspected acknowledged-loss event stops the pilot until investigated and remediated.

## Open questions and references

Who supplies representative corpus, accessibility reviewers, provider sandboxes and launch signatories? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| QA Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
