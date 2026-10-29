# ARC-02 — Domain boundaries and context map

Version 0.2 · 2026-10-29 · **Draft — simulated review; human approval pending**

Author/accountable: Solution Architect. Consulted: Document Engineer, Backend, Frontend, Conversion, Security, Accessibility, SRE, Editorial and Finance. Reviewer: Engineering Lead. Approver: Product Owner and Security/Finance/Editorial owners for their gates. Decision owner: Solution Architect. Assumptions: ASM-001–012 and proposed DEC-001–010; a text-centric single-imprint pilot, not approved market or capacity. Related requirements: FR-IAM-002, FR-DOC-002, FR-PUB-002, FR-COM-001, FR-FIN-001. References: [governance](../00-governance/02-decisions-and-open-questions.md), [SRS](../02-requirements/02-system-requirements-specification-srs.md), [standards register](../01-discovery-strategy/07-standards-and-source-register.md).

## Ownership and consistency

The following are logical bounded contexts, not a commitment to 18 services. All IDs are tenant-scoped where content is private. Aggregate methods enforce invariants; application services authorize and orchestrate; adapters implement storage/provider IO.

| Context | Aggregates / data | Owning module | Example event | Strong invariant |
|---|---|---|---|---|
| Identity & Organizations | User, Membership | Identity | MembershipChanged | Current role and access epoch |
| Author Projects | Project, Manuscript | Authoring | ProjectCreated | Owner and chapter order |
| Structured Documents | ManuscriptVersion, Chapter | Authoring | RevisionSaved | No silent overwrite; durable revision |
| Collaborative Editing | Session, Suggestion | Authoring extension | SuggestionResolved | Fresh permission; presence not durable content |
| Asset Storage | Asset, AssetLicense | Assets | AssetScanned | Quarantine until clean and licensed |
| Formatting/Conversion | ConversionJob, Rendition | Production | RenditionValidated | Input manifest fixed; output immutable |
| Editorial Pipeline | Submission, EditorialAssignment | Editorial | ReviewDecided | Frozen submission and attributable decision |
| Rights & Contracts | Contract, RightsGrant | Rights | RightsChanged | Scope and term valid |
| Catalog & Editions | Edition, CatalogListing | Catalog | EditionReleased | Matched rights and approvals |
| Distribution | ChannelAvailability, Delivery | Distribution | DeliveryAcknowledged | Partner receipt reconciled |
| Storefront & Reader | ReadingProgress, Review | Reader | ProgressSaved | Only authorized sample/entitlement |
| Commerce/Payments | Order, Payment, Entitlement | Commerce | PaymentConfirmed | No duplicate capture or entitlement |
| Royalty Ledger | LedgerEntry, Payout | Finance | RoyaltyPosted | Balanced currency-specific journal |
| Community/Marketing | Consent, Campaign | Growth | ConsentChanged | No implied mailing consent |
| Notifications | Notification | Messaging | NotificationDelivered | No private text in messages |
| Search/Analytics | IndexProjection, Metric | Data | ProjectionUpdated | Public index receives allowlist only |
| Moderation/Trust | Takedown, Case | Trust | ListingHeld | Evidence preserved; appeal tracked |
| Platform Administration | AuditEvent, SupportGrant | Operations | SupportAccessGranted | No ambient manuscript permission |

## Transactions and eventual consistency

Save commits version + current pointer + idempotency receipt + outbox in one authoring transaction. Release commits edition state + approval evidence + public projection intent after checking the rights epoch; a rights change serializes with this decision. Payment inbox, verified order transition and entitlement plus financial-posting intent commit atomically when all local prerequisites are satisfied; finance may consume the intent later with a unique source key. If entitlement provisioning cannot complete in that transaction, record a distinct pending state and durable retry intent; the buyer sees “Payment confirmed; preparing access” until entitlement exists. The two paths must be explicitly modeled and reconciled, never represented as access granted before the entitlement exists. No consumer assumes exactly-once delivery.

Catalog indexing, analytics, notifications and distribution are eventual projections with event sequence/high-water marks, replay and reconciliation jobs. Public indexing reads only the catalog's explicit published projection; it never reads authoring tables. A takedown removes public availability and queues cache/index purge; direct listing/purchase APIs still check current state if purge lags. Entitlement remedies for existing buyers require the legal policy, not a silent deletion.

Anti-corruption adapters translate provider terminology into internal Payment/Settlement/Delivery states. External identifiers are scoped to provider account; external event IDs do not replace internal IDs. Modules never share mutable objects or write foreign tables directly. An integration failure is typed as retryable, terminal or ambiguous; ambiguous money operations must reconcile before retrying.

## Open decisions and cross-role review

Jurisdiction, partner eligibility, operational capacity and product targets remain decisions for their owners at market/vendor/architecture baseline milestones in the governance register. This design must be validated in a prototype and does not assert implemented security, compliance or performance. Architecture review: boundaries and invariants are explicit; Security review: deny-by-default and private data require adversarial testing; QA review: contracts and tests require integration evidence; Editorial/Finance review: release and posting rules require qualified human review. Approvals remain pending.
