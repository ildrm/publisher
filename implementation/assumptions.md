# Implementation assumptions

Version 0.1 · 2026-10-29 · Local implementation checkpoint; no production or human specialist approval. Owner: Engineering Lead; consulted/review perspectives: Product, Requirements, Architecture, Document Engineering, Security, Accessibility, QA, SRE, Editorial and Finance. Actual approval: pending where required.

| ID | ASSUMPTION — VALIDATE | Impact / owner / milestone |
|---|---|---|
| IMP-ASM-001 | Loopback local development is authorized independently of commercial launch decisions. | No external publication, paid transaction or production account activation; Product, before pilot. |
| IMP-ASM-002 | A single application server owns each local SQLite directory. | File lock enforces CLI ownership; distributed queue/database topology requires redesign, SRE before staging. |
| IMP-ASM-003 | First editor supports paragraphs, headings 1–3, quotes, simple/nested lists, scene breaks, emphasis and safe link semantics; complex assets/tables/notes are not ready. | Warnings/rejections and source preservation instead of silent loss; Document/Conversion before format expansion. |
| IMP-ASM-004 | Recovery copies are tab-scoped session storage, unencrypted by the application. | Browser availability/quota are checked; user gets truthful copy/export warning. No offline-first or device-loss guarantee; Privacy before pilot. |
| IMP-ASM-005 | Local mailbox adapter substitutes delivery only in local/test. | Verification/recovery tokens are real, single-use and hashed in DB; mail file is private. Real provider/DPA/abuse/delivery proof required; Identity before staging. |
| IMP-ASM-006 | Dependency mirror is acceptable for development when main registry is unreachable. | Lockfile integrity and exact versions retained; independent maintenance/license/advisory review required before release; Security/Procurement. |
