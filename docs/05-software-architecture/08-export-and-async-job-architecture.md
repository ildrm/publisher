# ARC-08 — Export and asynchronous job architecture

Version 0.2 · 2026-10-29 · **Draft — simulated review; human approval pending**

Author/accountable: Solution Architect. Consulted: Document Engineer, Backend, Frontend, Conversion, Security, Accessibility, SRE, Editorial and Finance. Reviewer: Engineering Lead. Approver: Product Owner and Security/Finance/Editorial owners for their gates. Decision owner: Solution Architect. Assumptions: ASM-001–012 and proposed DEC-001–010; a text-centric single-imprint pilot, not approved market or capacity. Related requirements: FR-IMP-001, FR-EXP-001, FR-FMT-001, FR-PUB-002. References: [governance](../00-governance/02-decisions-and-open-questions.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md), [standards register](../01-discovery-strategy/07-standards-and-source-register.md).

## Immutable input manifest

A job records tenant, requester, exact source revision IDs, canonical-schema version, asset hashes and licenses, output profile, converter/container digest, font hashes/licenses, locale/hyphenation settings and deterministic seed/time controls. Hash the canonical manifest. Identical in-flight work may be deduplicated by `(tenant,input_hash,target_profile)`, but each requester and subsequent redemption must pass current source and artifact authorization; matching a hash is never an access grant. A failed or cancelled job may start a new authorized job after correction or retry, using a distinct command key; request-key deduplication is separate from work deduplication. New source or configuration means a new manifest. Source-map feasibility varies by format and must not be promised without a spike. Rendition stores checksum, media type, byte length, validation report and approval status; an approved rendition is immutable.

## Execution and state

`queued → running → validating → succeeded` or `failed/cancelled`; a lease with fencing token prevents a stale worker overwriting a newer attempt. Retries occur only for transient failures; invalid input is terminal until corrected. Proposed limits are 50 MiB compressed import, 250 MiB expanded, 1,000 archive entries, 20:1 expansion ratio, 120 seconds CPU and 512 MiB memory for an initial text-centric job; these are restrictive spike defaults subject to representative corpus testing, not universal safe thresholds. Limits are enforced during streaming extraction, not only from archive headers. Disable external network and embedded code, external XML entities, remote fonts and file:// references. Quarantine input and scan, inspect MIME/magic, parse with patched tooling and treat malware scanning as one defense, not a proof of safety.

Write output under private attempt-specific staging keys. Validate EPUB with selected EPUBCheck, semantic/reading-order tests and two target readers; print PDF with actual printer preset and human physical proof; PDF/UA requires separate accessibility validation. On success register artifact/checksum and outbox atomically; only then update the job's result pointer. Failure preserves the last known good artifact. Orphan attempts are swept after leases expire and retention grace allows investigation.

## Reconciliation and author feedback

UI provides queued/running/validating/completed/failed states, progress only when measurable, downloadable diagnostics without secrets, retry for transient error and source-correction action for invalid structure. A retry uses the same manifest but a new attempt. Scheduled reconciler compares jobs, object checksums, leases and registered artifacts; detects missing output, duplicate messages and stuck jobs. Publication uses approved frozen renditions, never the newest export by accident. Portability exports remain available without marketplace publication; signed delivery requires fresh permission at redemption.

## Open decisions and cross-role review

Jurisdiction, partner eligibility, operational capacity and product targets remain decisions for their owners at market/vendor/architecture baseline milestones in the governance register. This design must be validated in a prototype and does not assert implemented security, compliance or performance. Architecture review: boundaries and invariants are explicit; Security review: deny-by-default and private data require adversarial testing; QA review: contracts and tests require integration evidence; Editorial/Finance review: release and posting rules require qualified human review. Approvals remain pending.
