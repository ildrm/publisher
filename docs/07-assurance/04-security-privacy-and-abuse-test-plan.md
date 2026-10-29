# QA-04 — Security, privacy and abuse tests

Version 0.2 · 2026-10-29 · Status: Draft; not approved or implemented  
Authoring/accountable: Security Lead · Consulted: Product, Security, Accessibility, Finance, SRE and QA · Reviewer: Solution Architect · Approver and decision owner: Security Lead  
Assumptions: ASM-001–012 and DEC-001–010 in [governance](../00-governance/02-decisions-and-open-questions.md). Related requirements: FR-IAM-001–002, FR-CAT-001, FR-COM-001, FR-OPS-001; NFR-SEC-001–004, NFR-PRIV-001–002.

## Threat-driven scenarios

Exercise unauthorized cross-tenant read/write and signed URL reuse, privilege escalation, revoked access during worker processing, support access without purpose and audit tampering. Test MFA/session expiry, CSRF, XSS in document HTML/SVG, injection, SSRF through imported links, unsafe archives, file-type spoofing, decompression bombs and resource exhaustion against isolated workers. Scan dependencies, secrets, images and licenses; review CSP, encryption, key access, network policies and least privilege. Verify webhook signatures, event replay and missing/out-of-order provider notifications.

Seed private canaries in manuscript and metadata; check logs, metrics, public indexes, CDN, notifications, AI adapters and inaccessible object paths for leakage. Test consent creation, specific-purpose scope, revocation and processor retention separately before any AI feature is enabled. Exercise moderation, duplicate/impersonation, bot signup, rate limits and takedown appeals without treating an automated risk signal as proof of misconduct. Verify export/deletion/legal-hold handling after counsel selects jurisdictional policy. A breach drill must cover detection, containment, evidence preservation, legal notification decision and recovery; avoid contaminating evidence.

Penetration testing and legal/DPIA screening require qualified independent review; no result or compliance claim is asserted. Use OWASP ASVS 5.x and applicable NIST SSDF as review references after checking current official versions; only enable partners after confirming contractual and technical controls.

## Abuse cases and expected outcomes

| Case / scope | Attack and control verification | Expected outcome / escalation |
|---|---|---|
| SEC-T01 tenant isolation | Authenticated tenant B requests tenant A's project, export URL and job ID directly. | Deny each request without private metadata; alert only per abuse policy, record privacy-safe correlation. |
| SEC-T02 import | Upload file with spoofed extension, active HTML/SVG, archive expansion bomb and external-network reference. | Reject or safely quarantine within limits; sandbox makes no unauthorized network call and source is not published. |
| SEC-T03 revocation | Revoke a collaborator while a worker or download URL is pending. | Fresh authorization denies subsequent read/write and rechecks before delivery; already downloaded copies cannot be remotely erased. |
| SEC-T04 money replay | Submit unsigned, altered, duplicate and out-of-order provider callbacks. | Reject unverified messages; process each valid event once and reconcile uncertain provider state before retry. |
| SEC-T05 support and AI | Attempt unscoped support access or external AI request without purpose-specific consent. | Deny, audit attempted access and test approved provider terms separately before AI activation. |

Security owner records fixture, environment, exact request, safe response, audit evidence, severity and follow-up. Any detected actual private disclosure triggers incident response, rather than being handled solely as a test defect. No test or penetration assessment has been performed.

## Open questions and references

What jurisdictions, processor retention terms, age policy, penetration-test scope and incident contacts apply? Owners must resolve these by the relevant milestone in the governance register; no stakeholder decision is implied. References: [scope and assumptions](../00-governance/01-scope-and-assumptions.md), [decisions and risks](../00-governance/02-decisions-and-open-questions.md), [requirements](../02-requirements/02-system-requirements-specification-srs.md), and user-supplied *Online Publishing Super Mega Documentation Prompt* v1.0, sections 9–15. External standards and partner capabilities must be checked at execution time.

## Cross-role review checkpoint

| Role | Concern raised in simulated review | Draft response | Residual risk | Approval required |
|---|---|---|---|---|
| Security Lead | Scope and implementation evidence | Explicit controls and acceptance below | No production evidence or actual approval | Accountable owner |
| Security / Accessibility | Private data and equitable access | Default deny, privacy-safe logging and manual review | Independent assurance not performed | Security and Accessibility leads |
| Finance / Editorial | Rights, ledger and proof integrity | Release and reconciliation gates | Provider and legal rules unresolved | Finance and Publishing leads |
