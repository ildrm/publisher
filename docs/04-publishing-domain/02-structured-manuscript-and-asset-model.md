# PUB-002 — Structured manuscript and asset model

- **Version/date:** 0.2 / 2026-10-29; **status:** Draft, not reviewed or approved.
- **Authoring/accountable:** Document Engineering Lead; **consulted:** Editorial, Conversion, Accessibility, Security; **reviewer:** QA Lead; **approver:** Publishing Director; **decision owner:** Editorial and Publishing Operations Lead. Roles are proposed, not evidence of human review.
- **Assumptions:** ASM-001–012; text-centric curated pilot and scoped rights. **Related requirements:** FR-DOC-001–003, FR-IMP-001, FR-EXP-001, FR-FMT-001.
- **Unresolved:** OQ-001, OQ-003–007, OQ-009–010; assigned governance owners resolve before contract, vendor, proof and release milestones.
- **References:** [scope](../00-governance/01-scope-and-assumptions.md), [decision register](../00-governance/02-decisions-and-open-questions.md), [business rules](../02-requirements/05-business-rules-and-permissions.md), user-supplied prompt v1.0 §§3, 5, 11–15.

## Canonical source

A project belongs to a workspace and contains ordered manuscript chapters. Manuscript revision identifies a schema version, content nodes and ordering; a submission references a frozen revision. Model document semantics as typed nodes such as document, part, chapter, paragraph, heading level, list/list item, block quote, scene break, link, image, caption and note reference, with inline text/emphasis and language/direction attributes. User-entered formatting is mapped to constrained marks or named semantic roles, not trusted arbitrary executable HTML. Preview typography, trim and color are separate versioned presentation profiles. The canonical source is never replaced by its rendered HTML/PDF output.

Each node has a stable identifier where meaningful, type, validated attributes and ordered children. Schema migration is versioned and reversible where feasible; unsupported nodes must be reported before import acceptance and preserved as source/attachments only where safe and policy permits. Copy/paste, DOCX import and export require semantic round-trip tests including notes, lists, mixed script and unsupported structures. Selection, IME composition and accessibility behavior require evaluation of the selected editor component. Large documents may load chapter slices but version/permissions remain enforced at whole-project boundaries.

Assets have owner/workspace, content hash, detected media type, dimensions, alt text/caption, provenance, license scope and expiry where applicable, scan and validation status. A rendition snapshot records asset versions, schema and converter versions, approved layout profile and hashes. Asset attachment does not prove a license. Uploads are bounded, type-inspected, scanned and parsed in isolated workers; untrusted SVG/HTML and archives need safe handling. Private objects and source files use scoped access, encryption and audited retention policy; no private draft enters public search or CDN.

## Save and recovery boundary

Local edits, in-flight operations, acknowledged revision and failure are distinct. A write includes expected revision; stale writes are rejected, unsent content remains recoverable where supported, and explicit user review precedes resubmission. A successful server response is issued only after the defined durable commit. Backup RPO does not define acknowledged-save durability; full disaster recovery mechanism and limits remain OQ-006. Restoring a revision creates a new revision rather than erasing history.

## Schema and validation boundaries

The document root contains ordered chapters; each chapter contains block nodes, while text, emphasis and links occur only in permitted inline positions. Heading level and node type use an enumerated schema, link protocols are allowlisted, and image nodes reference an authorized scanned asset version rather than embedding executable markup. Enforce depth, node count, text length and asset size via configured limits tested with representative manuscripts; unknown node types produce an actionable error or a loss report, never silent deletion. Schema version is mandatory; migration records source and target versions, warnings and original revision. No canonical node may point across tenant boundaries without an explicit valid grant.

To assess fidelity, compare paragraph and chapter order, heading level, notes, link targets, image descriptions and language/direction before/after an import-export round trip. Preserve independent source files safely when a transformation cannot represent their content, and tell the user exactly which content needs review. Recovery copies are claimed only after local storage confirms them; stale saves do not merge automatically.

## Cross-role review checkpoint

| Role | Concern / response | Residual risk | Required approval |
|---|---|---|---|
| Document / Accessibility | Semantics and bidirectional text survive conversion | Editor/IME and round-trip evidence absent | Document / Accessibility leads |
| Security / SRE | Untrusted assets and acknowledged saves | Sandbox and recovery design unproven | Security / SRE leads |
