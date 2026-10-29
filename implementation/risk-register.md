# Execution risk register

Version 0.1 · 2026-10-29 · Local implementation checkpoint; no production or human specialist approval. Owner: Engineering Lead; consulted/review perspectives: Product, Requirements, Architecture, Document Engineering, Security, Accessibility, QA, SRE, Editorial and Finance. Actual approval: pending where required.

| Risk | Severity | Mitigation / residual / owner |
|---|---|---|
| IMP-RSK-001 Local data loss or stale overwrite | Critical | WAL/FULL + atomic receipts/revisions/outbox + CAS + immutable triggers and tests; host/disk/region failures unproven; SRE. |
| IMP-RSK-002 Private content leakage | Critical | Current resource grants on reads/writes/jobs/downloads; private file permissions; no public index/AI endpoints; at-rest encryption and independent tests pending; Security. |
| IMP-RSK-003 Conversion abuse/fidelity loss | High | Type/size/archive/XML checks, bounded child, warnings and original preservation; not full malware or kernel isolation; Conversion/Security. |
| IMP-RSK-004 Local recovery on shared device | High | Session storage scoped by user/chapter; only claim copy after verification; tab close/quota/device loss and encryption unresolved; Privacy. |
| IMP-RSK-005 Scope mistaken for whole platform | High | Requirements registry and gate report expose all phases; no inert publisher/finance screens; Product. |
| IMP-RSK-006 Dependency or deployment drift | High | Version/integrity lock, reproducible build and CI definition; mirror/advisory review, action SHA pins and target infrastructure pending; DevOps/Security. |
