# GOV-005 — Document control and traceability

- **Version / date:** 0.2 / 2026-10-29
- **Status:** Draft — workflow proposed; not stakeholder approved
- **Authoring / accountable role:** Technical Documentation Maintainer / Business Analyst
- **Consulted roles:** Product, Delivery, Architect, Editorial, QA, Security/Legal, Finance, A11y
- **Reviewer / approver / decision owner:** QA Lead / Product Owner / Business Analyst; actual review pending
- **Assumptions:** ASM-011–012; the repository is the source of truth for the documentation when adopted.
- **Related requirements:** Source prompt §§6–16; a draft [feature catalog](../02-requirements/03-feature-catalog-and-prioritization.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md) and [NFRs](../02-requirements/06-nonfunctional-requirements-and-slos.md) exist. Full decomposition and links to screens, APIs and tests remain incomplete.
- **References:** [roles and RACI](04-stakeholders-roles-raci.md); [scope](01-scope-and-assumptions.md); [decision, question and risk registers](02-decisions-and-open-questions.md); source master prompt v1.0.

## Document lifecycle

1. **Draft:** accountable author makes a versioned change with source status, assumptions, affected IDs and unresolved questions. Links may identify absent future artifacts as open gaps, not completed work.
2. **Review requested:** maintainer checks links and cross-references; relevant domain, security, privacy, accessibility, financial, editorial and QA reviewers check substance. Reviewer comments and ownership remain visible in change history.
3. **Reviewed:** an identified human reviewer records date, scope, evidence and remaining issues. Simulated review is never treated as this state.
4. **Approved:** an authorized human approver records date, version, decision, accepted residual risks and evidence. Legal and other specialist approvals remain separate. An approval can be superseded or revoked when its assumptions change.
5. **Superseded/retired:** preserve the historical version, replacement link and migration or impact note. Never reuse identifiers for a different meaning.

Each artifact needs document ID, title, version/date, status, author/accountable role, consulted roles, reviewer, approver, decision owner, assumptions, related requirements, substantive content, unresolved questions and references. Use a table of contents for long documents. Assign every unresolved decision an owner and milestone in the register; do not conceal a missing decision with an unowned placeholder. The root manifest reports actual files and status, not aspirational files as complete.

## Identifiers and provenance

| Prefix | Meaning / assignment |
|---|---|
| GOV-### | Governance document, stable across revisions. |
| ASM-### / DEC-### / OQ-### / RSK-### | Assumption / decision / open question / risk, assigned in their registers. |
| BG-### / KPI-### / JRN-### | Business goal / indicator / journey; assign when discovery artifacts exist. |
| FR-<DOMAIN>-### / NFR-<DOMAIN>-### | Functional capability / measurable nonfunctional requirement, using domain-qualified identifiers (for example FR-DOC-002 and NFR-REL-001). The SRS uses suffixes such as FR-DOC-002.1 for verifiable clauses. Maintain a single catalog owner. |
| SCR-### / API-### / EVT-### | Screen / API contract or operation / versioned event, allocated in relevant inventories. |
| TC-<FR-ID>-P/N/R / TC-<NFR-ID> / ADR-### / ISS-### | Positive, negative and boundary functional case / NFR test / architecture decision / audit issue. Case conventions are defined in the QA catalog. Do not claim a test passed without evidence. |

Classify each claim as prompt requirement, stakeholder assumption, dated external evidence, design proposal, or pending legal/technical decision. Official source URL, check date, scope, plan/version and confidence accompany competitive and standards claims. “Not found” means unknown, not absence. No benchmark, interview, partner agreement, test outcome or certification may be invented. The source prompt is an input and priority signal; it is not validation of business demand or compliance.

## Traceability contract and gap handling

Maintain a machine-readable or reviewable matrix with rows connecting **business goal → KPI → journey → FR/NFR → screen → domain/API/event → test → milestone**, plus owner, priority, status and evidence link. A branch can have multiple entries on either side. Requirements must have a verifiable criterion; tests must identify expected observable results and a responsible layer. Non-UI security and financial requirements may map to an operational interface or control rather than inventing a public screen. Missing references are explicit open issues with owner and milestone.

Before marking a batch ready for review, run a link/ID check and report orphan requirements, untested P0/P1 requirements, missing owners, dangling IDs, unsupported source claims and state/invariant conflicts. A completeness percentage is `actual required artifacts created / required artifact paths enumerated × 100`, with numerator and denominator shown; it describes file coverage only, not substantive completeness, implementation, approval or compliance. An artifact is not complete merely because a stub exists. Record exceptions and their risk owner instead of silently omitting them.

## Change-control procedure

A change request identifies trigger and evidence, affected decisions, assumptions, rights, interfaces, storage, tests, diagrams, owner and release impact. The Product Owner triages scope; the Architect, Editorial, Finance, Security/Legal and A11y leads review their affected areas. The decision owner accepts or rejects, gives rationale and records date and version; Delivery updates dependencies. Any change to a published contract or event considers compatibility and migration. The maintainer updates the manifest, glossary and changelog in the same change. A reopened assumption invalidates dependent approval until the owner reassesses it.

## Initial changelog

| Version | Date | Change | Recorded by |
|---|---|---|---|
| 0.1 | 2026-10-29 | Initial proposed governance baseline and registers; no actual human review. | Documentation authoring role (simulated) |

## Unresolved questions

OQ-010: appoint named owners and reviewers, approve workflow and determine repository protections. The catalog and SRS are draft and partial; until they are decomposed and linked to the design, diagrams, contracts and tests, traceability is incomplete; the maintainer must report those gaps rather than infer them. Legal, editorial, security, financial and accessibility evidence remain separate review obligations.
