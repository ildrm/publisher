# DISC-05 — Service blueprints and user journeys

Version 0.2 · 2026-10-29 · **Draft** · Author: Service Designer · Accountable/decision owner: Product Owner · Consulted: Author support, Editorial, Production, Finance, Security · Reviewer: Publishing Director · Approver required: Product Owner

**Assumptions:** supervised curated pilot, digital purchase and limited text-centric production; no validated user research. **Related:** DISC-01, DISC-03, DISC-06; future screen, domain and test catalogs. **Unresolved:** provider, launch market, response-time policy and supported file details; Product Owner and operations before pilot.

## Frontstage and backstage

| Actor and trigger | Frontstage journey and user-visible success | Backstage and external dependencies | Recovery / control |
|---|---|---|---|
| New author starts | Register, create project/chapter, type, see acknowledged save and export | Auth, tenant check, durable versioned storage, export worker | Unsaved changes remain visibly distinct; retry and recovery path; never report a failed write as saved |
| Migrating author imports | Select supported document, review conversion warnings and check chapters before saving | Validate type/size, scan and parse in isolated worker; retain original only per policy | On failure keep source intact; show actionable errors and retry; do not silently discard unsupported structures |
| Coauthor invited, later phase | Owner grants scope, collaborator opens permitted content | Membership and per-request authorization | Revocation blocks fresh reads/writes; offline copies and disclosure limits explained |
| Editor evaluates | Open authorized submission revision, decide or request changes; author sees status | Assignment and access audit; immutable submission snapshot and decision history | Decline with appropriate explanation; appeal or revise according to policy; never imply acceptance grants rights |
| Publishing director accepts | Review rights, editorial decisions and approval checklist | Rights grant, contract and release policy; human legal review | Missing/expired rights blocks release; record owner and escalation |
| Production specialist | Generate formats, inspect warnings, request author approval and physical print proof if applicable | Isolated conversion, version/config checksums, validation, printer requirements | Failed job preserves prior valid artifact; proof discrepancies block release until resolved |
| Reader buys | Discover published title, inspect sample and price, pay and open licensed copy | Public-only index, payment provider, verified webhook, order and entitlement | Duplicate webhook is idempotent; failed payment gives no entitlement; support can restore access |
| Finance administers | Review reconciled sale, refund, royalty and payout history | Balanced ledger, settlement reports, clearance and approval | Reversal is a new linked entry; duplicate delivery cannot double post; failed payout remains traceable |
| Support responds | Confirm identity and issue; provide status and limited remedy | Purpose-bound access, redacted logs, audit and escalation | No unrestricted manuscript inspection or routine impersonation; security incident response for suspected exposure |

## Service recovery and notifications

Connectivity loss: display local pending versus server-acknowledged state; on return retry safely or present conflict while preserving the committed revision and any confirmed local recovery copy. If local storage is unavailable, offer immediate copy/export where possible and do not claim a recovery copy exists. Collaborative conflict handling is a later feature and must be designed before enabling concurrent writes. Import or EPUB validation failure: give file-level and structural feedback and a retry route, without exposing system internals. Rejected submission: provide a policy-approved reason and next permitted action; protect reviewer confidentiality. Rights dispute or takedown: hold release or listing, retain evidence under policy and provide an appeal route; do not silently delete an author’s work. Print proof mismatch: compare revision, configuration and actual sample; halt approval. Payment dispute/refund: update entitlement under policy and post a traceable financial reversal; reconcile provider records. Failed transfer: alert finance, retain payable and retry only after cause/authorization is resolved.

Delivery notifications should include project or order reference, state, user action and safe support route; never include manuscript text or sensitive financial details in an email. Notification timing and SLAs require staffed operational capacity. Accessibility, language direction, small screens and keyboard access apply at each step.

## Review checkpoint

| Role | Concern / response | Residual risk | Approver required |
|---|---|---|---|
| Editorial | A rejection and a rights hold must be distinguishable | Policies and timelines not decided | Publishing Director |
| SRE and support | Save and conversion failures need recoverable states | Durability not demonstrated | Engineering lead |
| Finance | Refunds change entitlement and liability separately | Contract-specific policy not established | Finance lead |

References: [research plan](03-personas-jtbd-and-research-plan.md); [unit economics](04-business-model-and-unit-economics.md).
