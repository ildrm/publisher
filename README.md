# Publisher — local Author Studio

A working private authoring increment of the documented publishing platform. It includes real accounts, verified local mail, scoped project sharing, a structured Tiptap editor, acknowledged autosave and conflict recovery, immutable history/restore, reviewed imports, and portable snapshot exports. Publishing, rights release, bookstore, commerce/finance, production formats, 3D and later phases remain unimplemented.

The interface supports English, Mandarin Chinese, Hindi, Spanish, Arabic, French, Bengali, Portuguese, Indonesian, Urdu, Russian, German, Japanese and Nigerian Pidgin, plus Persian. Choose a language on the sign-in page or in the header; Arabic, Urdu and Persian use RTL layouts. Interface changes preserve manuscript language, direction, text and unsaved edits. Translations are drafts pending native-language review.

Tested with Node 26.12.0, npm 11.20.0 and Python 3.14.5. Start locally:

```sh
npm ci --ignore-scripts
npm run build
python3 apps/api/main.py serve
```

Open **http://127.0.0.1:8000**. Register, then run `python3 apps/api/main.py mail` to open the local verification link. This build sends no real email. For a synthetic demo, set a test-only `PUBLISHER_SEED_PASSWORD` and run `python3 scripts/seed.py`; sign in as `writer@example.test`.

```sh
python3 scripts/verify.py
npm run test:e2e
npm run test:i18n
```

See [implementation and run guide](implementation/README.md), [test evidence](implementation/test-evidence.md), [scope/status registry](implementation/requirements-status.json), [remaining gates](implementation/release-readiness.md), and [exact restart checkpoint](implementation/next-session-checkpoint.md). The [original design package](docs/README.md) remains available. Local persistence is SQLite WAL/FULL; production encryption, replication, recovery, providers and specialist approval remain open. The server rejects staging/production mode.

[Repository license](LICENSE).
