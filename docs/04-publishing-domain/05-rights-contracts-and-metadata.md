# PUB-005 — Rights, contracts and metadata

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft, not reviewed or approved.
- **Authoring/accountable:** Editorial and Publishing Operations Lead; **consulted:** Legal, Finance, Metadata, Author representative, Security; **reviewer:** QA Lead; **approver:** Publishing Director; **decision owner:** Editorial and Publishing Operations Lead. Roles are proposed, not evidence of human review.
- **Assumptions:** ASM-001–012; curated single-imprint pilot, portable drafting, rights and jurisdiction unresolved. **Related requirements:** FR-RGT-001, FR-PUB-001–002.
- **Unresolved:** OQ-001, OQ-003–007, OQ-009–010; assigned governance owners resolve before contract, vendor, proof and release milestones.
- **References:** [scope](../00-governance/01-scope-and-assumptions.md), [decision register](../00-governance/02-decisions-and-open-questions.md), [business rules](../02-requirements/05-business-rules-and-permissions.md), user-supplied master prompt v1.0 §§3, 5, 11–15.

## Rights model

A submission or account membership is not a transfer of copyright. The publisher records evidence of contracts and individual rights grants, including grantor and beneficiaries, work and edition, license type, exclusivity, languages, territories, formats, channels, effective dates, revocation/expiry, permitted actions and evidence version. Assets, fonts and contributor agreements require their own scoped licenses. Contract version and signature verification, applicable law, right to terminate, royalties and dispute resolution require counsel in each launch jurisdiction; records here are a technical proposal, not legal advice.

| State | Authorized transition and guard | Consequence |
|---|---|---|
| Draft → proposed | Rights officer attaches parties, scope and versioned evidence. | No release entitlement. |
| Proposed → active | Delegated approver records valid execution/approval, term and scope. | Grant may support release only within its exact scope and interval. |
| Active → expired / revoked / disputed | Timer or authorized action records reason and event. | Block new releases in affected scope; review live listings and obligations. |
| Disputed → active / revoked | Authorized resolution records evidence and decision. | Recheck publication and customer obligations; do not silently republish. |

Check overlapping grants for potential conflict; exclusive rights and claims of ownership are not inferred. Authorization to act, contract lifecycle and dispute holds must be logged. Takedown and reinstatement require documented notice, appeal and customer-remedy policies before launch. Legal holds and retention exceptions may constrain deletion; no universal duration is assumed.

## Metadata and identifiers

Record contributor identities/roles, public pen name, title/subtitle, imprint, edition/version relationship, language/script, description, category, keywords, release date, rights/territory, format, accessibility characteristics and identifier type/value/issuer. Validate uniqueness within identifier namespace and keep assignment status; do not fabricate an ISBN, ASIN or DOI. ISBN eligibility and per-format assignment depend on the relevant agency and actual product. BISAC/THEMA codes, ONIX output, retailer IDs and channel requirements are candidate integrations, not promised capabilities. Public listings expose only approved metadata, authorized excerpts, price and availability for allowed scopes; private contracts and manuscripts stay private.

Metadata, artwork, format and rights approval are version-bound. Any changed data that affects a listing or proof invalidates the corresponding approval and triggers revalidation. An accessibility statement must describe tested features and known limitations rather than imply certification. Resolve OQ-003 with qualified counsel and actual contract examples before any release.

## Applicability decision and audit

For each requested release tuple `(work, edition, contributor/asset, language, territory, format, channel, effective time, action)`, resolve every necessary grant and underlying licensed asset. A grant supports the tuple only when the authorized subject and permitted action match, its scope includes each dimension, its effective interval includes the execution time, and its approved evidence is current and not disputed, revoked or expired. An absent, ambiguous or conflicting grant yields **hold**, not an inference of ownership, exclusivity or permission. Record the evaluated tuple, grant and contract versions, evidence, actor, decision time and reason; re-evaluate at scheduled execution, distribution retry and reinstatement. A change in grant scope or expiry invalidates only affected approvals/listings and queues human review of existing entitlements and channel takedowns.

Example: a valid English ebook grant for territory A and direct-store channel does not authorize print, territory B, a translation, or third-party distribution. A cover image may have a narrower license than the manuscript; release is held until both scopes cover the tuple. The rules describe checks, not whether a specific real agreement is valid; Legal must approve the interpretation and customer remedies.

## Cross-role checkpoint

| Role | Concern / response | Residual risk | Required approval |
|---|---|---|---|
| Legal / Editorial | Rights differ per scope and contributor | Interpretation and evidence are unverified | Legal / Publishing |
| Finance | Contract royalty basis may differ | Calculation and withholding rules remain open | Finance lead |
