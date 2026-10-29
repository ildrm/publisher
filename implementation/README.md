# Working local Author Studio — implementation checkpoint

Version 0.2, October 29, 2026. This is a functioning local authoring increment with a multilingual interface, not the completed publishing platform. The original design documents remain drafts; no commercial, legal, financial, accessibility or production approval is implied. Aggregate verification and both browser suites passed: 47 Python application/localization tests, 9 JS autosave/i18n tests and separate 16 Python/3 JS reference tests. The [multilingual browser run](evidence/i18n-e2e-results.json) passed all 15 interfaces, same-editor Undo/Redo, unsaved switching and account persistence; Arabic/Urdu automated axe scans reported zero violations. See [test evidence](test-evidence.md) for the exact scope and limits.

## What works

Real account creation, private local verification/recovery messages, sign-in/out, password recovery and hashed sessions; private workspaces/projects; verified-account editor/viewer grants and revocation; structured Tiptap chapters with headings, emphasis, quotations, lists, undo/redo and independent language/direction; server-acknowledged autosave, exact retries, stale-version conflict, confirmed tab recovery, immutable history and restore-as-new; chapter creation/order; reviewed DOCX/Markdown/text import with preserved originals; asynchronous private snapshot exports as a full project bundle, DOCX, Markdown, text and HTML; checksummed artifacts, audit/outbox records, SQLite migrations and backup/check commands.

The full bundle includes canonical source, chapter/revision metadata and portable files. DOCX/Markdown conversions have explicitly disclosed fidelity limits. No arbitrary HTML is the canonical manuscript. Nothing is published, indexed publicly or sent to an AI provider.

The interface now offers English, Simplified Mandarin Chinese, Hindi, Spanish, Standard Arabic, French, Bengali, Portuguese, Indonesian, Urdu, Russian, German, Japanese and Nigerian Pidgin, plus Persian: 15 choices meeting the user's minimum 14-language request. Select a language before or after sign-in. Device and authenticated account preferences persist independently of manuscript language/direction; Arabic, Persian and Urdu have RTL interfaces. Application labels, accessible names, validation, recovery/status and conversion messages use local catalogs. Catalogs are implementer translation drafts without native human approval. See [language behavior, source interpretation and 22-role review](multilingual-review.md) for regional/formatting choices and remaining manual review.

## Run it

Tested with Node **26.12.0**, npm **11.20.0**, Python **3.14.5**, installed Google Chrome and macOS. No Python packages or commercial account are needed.

```sh
npm ci --ignore-scripts
npm run build
python3 apps/api/main.py serve
```

Open **http://127.0.0.1:8000**. Create an account, then inspect its private local message with `python3 apps/api/main.py mail` and follow the verification link. The mailbox adapter does not send real email. `npm run dev` runs the API at port 8000 and Vite at http://127.0.0.1:5173. If both modes are used, stop the earlier server first. Each local data directory permits one server process.

The main npm registry was unreachable during development; the lockfile records packages fetched through the Liara npm mirror. If the lockfile’s mirror is unreachable in your environment, configure an approved reachable registry/mirror and preserve package versions/integrity rather than silently upgrading. Independent dependency-source and maintenance review remains a release gate.

Optional synthetic demo (choose a new test-only password):

```sh
export PUBLISHER_SEED_PASSWORD='choose-a-new-synthetic-password'
python3 scripts/seed.py
```

Sign in as `writer@example.test` with that password. The command verifies only its synthetic `.test` account and does not overwrite existing manuscript revisions. No default password or live account credential is committed.

## Verify and inspect

```sh
python3 scripts/verify.py
npm run test:e2e
npm run test:i18n
python3 scripts/update_implementation.py
python3 apps/api/main.py check
python3 apps/api/main.py backup --destination /private/tmp/publisher-backup.sqlite3
```

Browser tests use installed Chrome by default, synthetic data in a fresh temporary directory, and a separate port 8123. For an installed Playwright Chromium runtime, set `PUBLISHER_BROWSER_CHANNEL=chromium`. The in-app browser host was unavailable, so Playwright was the recorded fallback. See [test evidence](test-evidence.md), [browser observations](evidence/e2e-results.json), [axe output](evidence/axe-results.json), [desktop](evidence/studio-desktop.png), [mobile](evidence/studio-mobile.png), [verification log/index](evidence/verification.json) and generated [SBOM](evidence/sbom.cdx.json).

Actual runtime operations are in [OpenAPI](../apps/api/openapi.json), canonical v2 in [schema](../docs/contracts/schemas/manuscript-ast.v2.schema.json), source migrations in [001](../apps/api/publisher/migrations/001_authoring.sql) and [002 account interface locale](../apps/api/publisher/migrations/002_interface_locales.sql). The runtime contract is partial for some responses and differs explicitly from the representative design API; see [conflicts](document-conflicts.md). Database schema version 2 and manuscript AST version 2 are separate version domains.

## Scope, gaps and next task

The [execution registry](requirements-status.json) and [CSV](requirements-status.csv) track all extracted FR/NFR clauses, screens, ADRs, business rules and reference operations/events. Counts include parents and child clauses and are not independent feature totals. [Coverage](coverage-and-gaps.md) and [release gates](release-readiness.md) prevent file presence or local test results from being called full completion.

Publishing/rights/editions/catalog, commerce/ledger/payouts, EPUB/PDF/print, actual 3D, planning/realtime collaboration, AI and later verticals are not implemented in this checkpoint. Production storage/replication/encryption, privileged MFA, real mail, malware/kernel isolation, manual accessibility/IME tests, providers and specialist approvals remain open in [blockers](blockers.md). The local server rejects staging/production mode.

Next unblocked atomic task: privileged staff MFA and authorization tests, then frozen author submissions and assigned editorial decisions. Follow [next-session checkpoint](next-session-checkpoint.md), not assumptions about a completed platform. No work continues asynchronously after this handoff.
