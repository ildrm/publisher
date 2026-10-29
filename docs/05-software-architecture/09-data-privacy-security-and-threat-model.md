# ARC-09 — Privacy, security and threat model

Version 0.2 · 2026-10-29 · **Draft — simulated review; human approval pending**

Author/accountable: Solution Architect. Consulted: Document Engineer, Backend, Frontend, Conversion, Security, Accessibility, SRE, Editorial and Finance. Reviewer: Engineering Lead. Approver: Product Owner and Security/Finance/Editorial owners for their gates. Decision owner: Solution Architect. Assumptions: ASM-001–012 and proposed DEC-001–010; a text-centric single-imprint pilot, not approved market or capacity. Related requirements: FR-IAM-002, FR-DOC-002, FR-PUB-002, FR-COM-001, FR-FIN-001. References: [governance](../00-governance/02-decisions-and-open-questions.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md), [standards register](../01-discovery-strategy/07-standards-and-source-register.md).

## Data flows and trust boundaries

[Data-flow diagram](../diagrams/data-flow.mmd) distinguishes browser input, authenticated API, quarantine/worker, private storage, public projection, payment provider and optional AI processor. Private drafts never enter public search/CDN or analytics. Release deliberately copies only approved metadata/sample/artifacts to public or entitled channels; full paid files remain restricted. An AI request must identify selected content, purpose, provider, retention and estimated cost before opt-in. Consent is not a blanket permission for model training, marketing or unrelated analytics.

## STRIDE and abuse backlog

| ID / threat | Boundary / attack | Mitigation and required test | Owner |
|---|---|---|---|
| TH-001 S | Stolen session / support impersonation | MFA for privileged access, session rotation, device/session revoke, time-bound support grant; token/recovery abuse tests | Identity/Security |
| TH-002 T | Tenant IDOR or stale grant modifies draft | Server resource authorization, access epoch and scoped keys; cross-tenant and revoke/write race tests | Backend |
| TH-003 R | Denied release or payout actor | Append-only audit with actor, purpose, version and correlation; hash/sign checkpoint to restricted store; tamper-evidence drill | Security/Finance |
| TH-004 I | Draft in CDN, search, logs or AI | Separate allowlisted projection, no private logs, explicit processor consent; canary phrase search and log tests | Privacy/Data |
| TH-005 D | Archive bomb, 100k-word runaway rendering or 3D GPU abuse | Byte/entry/decompression/CPU/memory budgets, sandbox, quotas and fallback; malicious corpus and device tests | Conversion/Frontend |
| TH-006 E | Admin bypasses rights or finance approval | No ambient content access, role separation, dual approval, immutable release manifest and ledger; privilege escalation tests | Security |
| TH-007 T/R | Forged or replayed payment webhook | Raw-body signature, timestamp, account match, permanent dedupe, provider reconciliation; replay/out-of-order tests | Commerce |
| TH-008 I/T | SSRF/XSS via HTML, EPUB, SVG, remote URL or AI tool text | Reject scriptable formats initially; canonical allowlist, sanitizer, CSP, egress deny, metadata-safe escaping; no model tool execution from manuscript | Assets/AI |
| TH-009 D/E | Fraud, abusive reviews, mass uploads or stolen entitlements | Rate/volume limits, moderated reviews, fraud queue, accessible challenge/recovery; appeal and false-positive metrics | Trust |

TLS and encryption-at-rest use managed KMS with separated production roles and rotation. Secrets are never in code, client bundles or logs. SQL is parameterized; CSRF is controlled for cookie sessions; CSP restricts script/frame origins; CORS is allowlisted. Dependency updates, SBOM, secret/SAST/DAST scans and vulnerability response map to ASVS/SSDF in the standards register. No certification is asserted.

## Privacy inventory and DPIA screening

Identity/contact, manuscript-sensitive content, payment/payout references, behavior/reading history and legal evidence have distinct retention/access purposes in ARC-05. Card data is handled by hosted payment pages; only processor tokens/references enter the platform. Processors need contracts, residency/subprocessor and deletion evidence. Screen DPIA need when profiling/read history is large-scale, sensitive manuscripts are processed, minors may participate, AI is added, or monitoring creates high rights/freedoms risk. Privacy lead records lawful purpose, necessity, alternatives, subject risks, mitigations and residual approval before enabling the processing; consent alone is not assumed to legalize everything.

Launch market review must assess GDPR or local equivalents, age-appropriate policies, author copyright and notice/takedown, consumer digital remedies, sanctions/territory restrictions and EU ebook European Accessibility Act/national rules where applicable. Legal counsel owns applicability, not this design. No universal compliance conclusion is made. Legal holds restrict deletion only for documented data/scope/time; author access/export and evidence minimization remain supported.

## Breach and AI incident response

Contain credentials/access and preserve minimized evidence; page incident commander and privacy/security owners; determine affected tenants, data, processors and time range from audit; assess actual named-market notification deadlines with counsel; communicate factual scope and updates; restore from validated clean state, rotate secrets and confirm no public projections remain. Record chronology and follow-up tests. Do not predeclare a universal 72-hour notification rule.

AI is deferred. Enable only after purpose-specific opt-in, provider disclosure/DPA/retention controls, no-training contract verification, PII minimization and tool isolation. Treat manuscript/model text as untrusted data; never as instructions to access other tenants. Measure hallucinated quotations/citations, inappropriate copying, multilingual quality, cost and reversible suggestion acceptance. Human review and provenance accompany exports; provider fallback requires equivalent consent/data terms, not silent rerouting. NIST AI RMF/GenAI profile is a risk framework reference, not certification.

## Open decisions and cross-role review

Jurisdiction, partner eligibility, operational capacity and product targets remain decisions for their owners at market/vendor/architecture baseline milestones in the governance register. This design must be validated in a prototype and does not assert implemented security, compliance or performance. Architecture review: boundaries and invariants are explicit; Security review: deny-by-default and private data require adversarial testing; QA review: contracts and tests require integration evidence; Editorial/Finance review: release and posting rules require qualified human review. Approvals remain pending.
