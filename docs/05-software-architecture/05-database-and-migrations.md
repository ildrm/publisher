# ARC-05 — Database, entity dictionary and migrations

Version 0.2 · 2026-10-29 · **Draft; human approval pending**. Author/accountable/decision owner: Data Architect. Consulted: Authoring, Rights, Finance, Privacy, Security and QA. Reviewer: Backend Lead. Approver: Solution Architect with Finance/Privacy for retention. Assumptions: ASM-001–012. Related requirements: FR-DOC-001–003, FR-RGT-001, FR-PUB-002, FR-FIN-001, FR-OPS-001. References: [domain boundaries](02-domain-boundaries-and-context-map.md), [rules](../02-requirements/05-business-rules-and-permissions.md), [ERD](../diagrams/erd.mmd).

## Common fields and policy profiles

This is a conceptual-to-physical proposal, not an applied database migration. Each tenant-owned aggregate table has `id UUID PK`, `tenant_id UUID NOT NULL`, `version BIGINT`, `created_at/updated_at TIMESTAMPTZ` and actor metadata unless explicitly global. `User` is a global identity record; tenant-scoped membership references it through a narrowly authorized identity relationship and does not imply cross-tenant access. The authenticated server derives tenant scope. Tenant-owned private FKs are composite `(tenant_id,related_id)` to a unique `(tenant_id,id)` target; database row policies and API checks provide defense in depth. Cross-tenant rights grants reference an explicitly authorized publisher/author relationship, never a client-provided tenant switch. Public projection is separate from canonical tables. Data encryption at rest and TLS apply to every profile; secrets and particularly sensitive payout/contract details use field encryption where threat model requires, keys managed separately. Queries bind values and indexes begin with tenant_id for private data.

| Profile | Visibility / PII | Retention and deletion | History / additional controls |
|---|---|---|---|
| I Identity/behavior | Self and purpose-scoped staff; direct/pseudonymous PII | Retain only for service/legal purpose; proposed dormant-account review and progress deletion configurable after jurisdiction decision; no universal duration | Minimized audit, user correction/export and processor erasure jobs |
| D Draft/content | Private owner/assigned collaborator; may contain sensitive PII | Author-controlled project deletion after disclosed recovery grace; hold only named evidence; backup expiry documented; export first | Immutable revisions until approved retention expiry; no public indexing/model training |
| L Legal/editorial | Assigned rights/editorial staff; legal and contributor PII | Jurisdiction-specific evidence/contract schedule approved by counsel; deletion blocked only by scoped hold | Versioned grants, signed evidence and attributable decisions |
| F Financial | Buyer/payee and finance scope; financial PII | Statutory accounting/tax schedule approved per legal entity; no hard deletion that breaks reconciliation | Append-only posted journal, compensating changes and dual approval |
| P Public projection | Only explicitly published fields; pseudonym may be personal | Remove availability/index/cache when withdrawn; keep private source evidence per appropriate profile | Versioned listing and sample approval; no draft/contract fields |
| A Audit | Security/finance purpose access; minimized actor PII | Security/accounting/incident schedule; redaction/pseudonymization where lawful and reconciliation allows | Append-only access and signed/hash checkpoints; never raw manuscript or tokens |

Mixed profiles such as D/P mean **separate field projections**, not that private data becomes public. Exact durations are unresolved in OQ-001/003/009; Privacy and Finance must approve a named schedule at contract baseline before live retention jobs activate. Deletion traverses references with an evidence plan, does not cascade financial history, and reports remaining lawful retention to the user.

## Canonical dictionary

All rows inherit fields, tenant indexes, encryption, retention and history controls above. Listed unique keys are additionally tenant-scoped unless globally issued externally. Composite conceptual entities may map to multiple tables; small value objects (ranges, scopes, addresses) may be embedded JSON with validated schema. Conceptual entity names are not a mandate for one-table-per-concept.

| Entity | Proposed physical table(s) | Service owner | Additional fields and types | Unique / query indexes | Profile | Relationships |
|---|---|---|---|---|---|---|
| User | users | Identity | email_norm:text, status:enum, auth_subject:text | auth_subject; email_norm scoped by identity policy | I | Membership,Customer |
| AuthorProfile/PenName | author_profiles | Identity | user_id:uuid, display_name:text, public_opt_in:bool | user_id,name; public slug unique | I/P | User,Contributor |
| Organization/Imprint | organizations,imprints | Identity | legal_name:text, imprint_name:text, publisher_org_id:uuid | imprint slug per org | I/P | Membership,Edition |
| Membership | memberships | Identity | user_id:uuid, scope_id:uuid, role:enum, access_epoch:int | user_id,scope_id,role; scope_id,status | I | User,Workspace,Project |
| Workspace | workspaces | Authoring | owner_org_id:uuid, name:text | owner_org_id,id | D | Organization,Project |
| Project/Work | projects | Authoring | workspace_id:uuid, title:text, language:BCP47, access_epoch:int | workspace_id,id; workspace_id,updated_at | D | Manuscript,Contributor |
| Manuscript | manuscripts | Authoring | project_id:uuid, schema_version:int, chapter_order:uuid[] | project_id,id | D | Project,Chapter |
| ManuscriptVersion | manuscript_versions | Authoring | manuscript_id:uuid, sequence:int, manifest_hash:sha256, source_revision_ids:uuid[] | manuscript_id,sequence unique | D | Chapter,Submission,Rendition |
| Chapter/DocumentNode | chapters,chapter_revisions | Authoring | manuscript_id:uuid, current_revision_id:uuid, ast:json, schema_version:int | chapter_id,sequence unique; manuscript_id,ordinal | D | Manuscript,ManuscriptVersion |
| Comment | comments | Authoring | revision_id:uuid, anchor:json, body:text, state:enum | revision_id,created_at | D | ManuscriptVersion,User |
| Suggestion | suggestions | Authoring | base_revision_id:uuid, patch:json, state:enum, reviewer_id:uuid | base_revision_id,state | D | Comment,ManuscriptVersion |
| ResearchItem | research_items | Authoring | project_id:uuid, source_url:text?, note:text, citation:json | project_id,tag | D | Project,Asset |
| Asset | assets | Assets | project_id:uuid, object_key:text, sha256:text, scan_state:enum | tenant_id,sha256; project_id,scan_state | D | AssetLicense,Rendition |
| AssetLicense | asset_licenses | Rights | asset_id:uuid, evidence_key:text, permitted_scope:json, expires_at:time? | asset_id,version unique | L | Asset,Contract |
| Contributor | contributors | Rights | work_id:uuid, party_id:uuid, role:enum, credited_name:text | work_id,party_id,role | L/P | Project,RightsGrant,RoyaltyRule |
| RightsGrant | rights_grants | Rights | contract_id:uuid, version:int, territories:code[], languages:BCP47[], formats:enum[], channels:text[], valid_range:range | contract_id,version unique; work_id,status,valid_range | L | Contract,Contributor,Edition |
| Contract | contracts | Rights | work_id:uuid, signed_artifact_key:text, version:int, status:enum | work_id,version unique | L | RightsGrant,RoyaltyRule |
| Submission | submissions | Editorial | work_id:uuid, manuscript_version_id:uuid, declarations:json, state:enum | work_id,created_at; submitter_id,idempotency_key unique | L | ManuscriptVersion,EditorialAssignment |
| EditorialAssignment | editorial_assignments | Editorial | submission_id:uuid, assignee_id:uuid, task_type:enum, state:enum, due_at:time? | submission_id,state,assignee_id | L | Submission,ReviewDecision |
| ReviewDecision | review_decisions | Editorial | assignment_id:uuid, reason:text, result:enum, evidence_version:int | assignment_id,version unique | L | EditorialAssignment,Edition |
| Publication/Edition | editions | Catalog | work_id:uuid, language:BCP47, edition_number:text, release_manifest:json, state:enum | work_id,language,edition_number unique | L/P | Rendition,CatalogListing,RightsGrant |
| Rendition/ExportArtifact | renditions | Production | edition_id:uuid?, manifest_hash:text, object_key:text, sha256:text, format:enum, validation:json | tenant_id,manifest_hash,format unique | D/P | ManuscriptVersion,ConversionJob,Edition |
| ISBN/Identifier | identifiers | Catalog | edition_id:uuid, format:text, scheme:enum, value:text | scheme,value unique where assignment rules permit | P | Edition,Rendition |
| CatalogListing | catalog_listings | Catalog | edition_id:uuid, public_metadata:json, sample_artifact_id:uuid?, state:enum | public_slug unique; state,published_at | P | Edition,Price,ChannelAvailability |
| Price | prices | Catalog | listing_id:uuid, currency:ISO4217, minor_units:int, valid_range:range | listing_id,currency,territory,valid_range nonoverlap | F/P | CatalogListing,Order |
| Territory/ChannelAvailability | channel_availability | Distribution | listing_id:uuid, territory:code, channel:text, valid_range:range, status:enum | listing_id,territory,channel,valid_range | L/P | RightsGrant,CatalogListing |
| Customer | customers | Commerce | user_id:uuid, billing_country:code, tax_reference:text? | user_id unique | I | User,Order |
| Cart | carts | Commerce | customer_id:uuid, item_refs:json, expires_at:time | customer_id,status | I | Customer,Price |
| Order | orders,order_lines | Commerce | customer_id:uuid, currency:code, total_minor:int, state:enum, price_snapshot:json | customer_id,checkout_key unique; created_at,state | F | Payment,Entitlement,Refund |
| Payment | payments,payment_events | Commerce | order_id:uuid, provider:text, account:text, external_id:text, state:enum | provider,account,external_id unique | F | Order,Sale/SettlementEvent |
| Entitlement/License | entitlements | Commerce | order_line_id:uuid, customer_id:uuid, rendition_id:uuid, scope:json, state:enum | order_line_id,customer_id unique | F | Order,Rendition,Customer |
| ReadingProgress | reading_progress | Reader | customer_id:uuid, edition_id:uuid, position:json, updated_at:time | customer_id,edition_id unique | I | Customer,Edition |
| Review | reviews | Trust | customer_id:uuid, listing_id:uuid, rating:int, body:text, moderation_state:enum | customer_id,listing_id unique | I/P | Customer,CatalogListing |
| Sale/SettlementEvent | settlement_events | Finance | provider:text, account:text, source_event_id:text, type:enum, currency:code, amount_minor:int | provider,account,source_event_id unique | F | Payment,LedgerEntry,Refund |
| RoyaltyRule | royalty_rules | Finance | contract_id:uuid, version:int, basis:enum, splits:json, valid_range:range | contract_id,version unique | F | Contributor,Contract,LedgerEntry |
| LedgerEntry | ledger_transactions,ledger_lines | Finance | source_key:text, account_id:uuid, currency:code, debit_minor:int, credit_minor:int, reversal_of:uuid? | source_key unique; transaction_id,line_number unique | F | Sale/SettlementEvent,RoyaltyStatement |
| RoyaltyStatement | royalty_statements | Finance | payee_id:uuid, period:range, currency:code, posting_high_water:text, state:enum | payee_id,period,currency,version unique | F | LedgerEntry,Payout |
| Payout | payouts | Finance | statement_id:uuid, amount_minor:int, currency:code, provider_key:text, state:enum | provider_key unique; payee_id,state | F | RoyaltyStatement,LedgerEntry |
| Refund | refunds | Commerce | order_id:uuid, source_ref:text, amount_minor:int, state:enum | provider,account,source_ref unique | F | Order,LedgerEntry,Payment |
| Notification | notifications | Messaging | recipient_id:uuid, template:text, event_id:uuid, delivery_state:enum | recipient_id,event_id,template unique | I | User,AuditEvent |
| AuditEvent | audit_events | Operations | actor_id:uuid?, purpose:text, action:text, object_id:uuid, outcome:enum, checkpoint_hash:text | tenant_id,occurred_at,id; correlation_id | A | All controlled aggregates |
| ConversionJob | conversion_jobs,job_attempts | Production | requester_id:uuid, input_hash:text, profile:text, state:enum, lease_epoch:int | tenant_id,requester_id,idempotency_key unique; optional active-work deduplication keyed by tenant,input_hash,profile with independent authorization | D | Rendition,Asset,ManuscriptVersion |
| 3DModelArtifact | model_artifacts | Production | rendition_id:uuid, geometry_manifest:json, input_hash:text, artifact_key:text?, assumptions:text | rendition_id,input_hash unique | D/P | Asset,Rendition |
| Outbox/Inbox | outbox,inbox | Per module | event_id:uuid, schema_version:int, aggregate_sequence:int, state:enum | outbox:event_id unique; inbox:consumer,event_id unique | A | All publishing/consuming modules |
| Approval | approvals | Editorial | edition_id:uuid, type:enum, input_hash:text, approver_id:uuid, result:enum | edition_id,type,input_hash,approver_id | L | Edition,RightsGrant,Rendition |

## Database integrity and migrations

Transactions enforce no negative payable after reservation, currency-balanced journals and immutable posted financial records. Each ledger transaction has nonempty debit/credit lines, one currency and equal totals; integer minor units and recorded currency scale avoid floating-point error. FX is a separate explicit conversion event with rate/date/source; never balance unrelated currencies by adding them. RoyaltyRule references the exact contract version and settlement basis; rates/splits must validate within contract-approved bounds.

A versioned migration first expands nullable/new structures, deploys tolerant readers/writers, backfills with checkpoints and tenant counts, verifies referential and balance invariants, switches reads behind a flag, then contracts only after the rollback window. Large indexes use deployment-appropriate online/concurrent methods after staging rehearsal. Migration failure stops rollout; down-migrating a destructive content/schema change is not a safe rollback. Restore original AST and rerun a corrected migration into a new revision. Record converter/schema versions in each artifact, and never mutate an approved source to fit a new schema.

## Open questions and review

Data/Privacy must approve retention durations and deletion evidence by contract baseline; Finance must approve chart of accounts, currency precision, reserves and royalty basis by first financial pilot. Backend/QA must prove composite foreign keys, tenant policies, optimistic version constraints, event uniqueness and restore consistency using adversarial fixtures. Simulated review raised cross-tenant FK and deletion-cascade risks; common tenant constraints and profile retention address design intent, but no schema has been deployed or certified.
