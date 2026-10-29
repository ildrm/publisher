# OPS-02 — CI/CD and supply-chain security

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: SRE Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: SRE Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-OPS-001; NFR-SEC-003–004.

## Pipeline and release controls

On pull request run lint/type checks, unit/domain and contract tests, secret and dependency scans, license policy and review; build once, create SBOM and sign immutable artifacts where tooling permits. Verify pinned sources, provenance and signatures before deployment. Staging runs integration, browser, privacy/a11y, malicious conversion fixtures, migration and rollback exercises; release requires reviewed evidence and a named decision owner. DAST and independent penetration testing are scheduled with explicit scope and safe test data.

Store secrets in a dedicated manager, rotate on exposure, use short-lived least-privilege workload identities and keep them out of build logs. Isolate untrusted conversion with resource, filesystem and network restrictions. Review urgent vulnerabilities by exploitability and exposure; document owner, deadline and mitigation. Deployment gates do not imply certification or eliminate manual review.

## Open questions and references

Which CI platform, signing chain, dependency policy, vulnerability SLAs and package registries are selected? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| SRE Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
