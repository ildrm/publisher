# ENG-03 — Clean code and standards

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Engineering Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Engineering Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-DOC-002, FR-RGT-001, FR-FIN-001; NFR-SEC-001–004.

## Rules for production work

Use clear names, small cohesive functions, explicit domain types, immutability for revision and ledger boundaries, dependency inversion at external edges and composition. SOLID and DRY apply where a real common rule exists; avoid premature abstraction (KISS/YAGNI). Parse untrusted input at the boundary, reject invalid or ambiguous data, and represent expected failure as typed results; unexpected errors propagate with safe context and correlation IDs. Never swallow save, conversion or payment errors. Tests should assert behavior and invariants rather than mirror implementation.

Repositories implement optimistic concurrency for mutable aggregates; document or ledger writes, constraints and outbox entries share a transaction. Money uses decimal minor units and explicit currency; balances derive from append-only balanced postings. Authorization is performed server-side using current tenant, resource and action. No secrets, manuscript text, payment details or untrusted markup in logs. Protect against injection using parameterized queries and safely rendered structured nodes; never use `eval` or execute uploaded macros. Comments explain intent and non-obvious invariants, not restate code.

## Open questions and references

Which static analysis, language style, money representation and review policy will be adopted? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Engineering Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
