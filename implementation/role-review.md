# Simulated cross-role review of the local authoring milestone

Version 0.2, 2026-10-29. This table records engineering review perspectives, not actual human consultation/sign-off. Responsible implementer and delivery/document maintenance owner: Engineering Lead; UX copy: UX/Content; glossary and traceability: Requirements. Actual approvals below remain pending before corresponding activation. The subsequent [multilingual 22-role review](multilingual-review.md) records the user's 14-language requirement, fifteen implemented interfaces, concrete repaired omissions and remaining platform gaps. Strict build, 47 Python/9 JS application tests, separate reference tests and both browser suites passed. Nine backend regressions cover the additional source review fixes.

| Perspective | Concern / reflected correction | Residual / actual approver needed |
|---|---|---|
| 1 Sponsor / Publishing Director | Export independent of publisher selection; no public release control shipped prematurely | Approve real operating market/scope before pilot |
| 2 Product Owner | Complete author path prioritized over empty modules | Accept scope and atomic later backlog |
| 3 Requirements Engineer | Stable IDs, actual document versions and evidence normalized; digit-containing I18N/A11Y families restored to the generated registry | Decompose compound P1/P2 requirements; no release-ready state inferred |
| 4 UX Research / Service | Recovery and rejected/stale actions explain next steps | Real user task research absent |
| 5 Editorial Operations | No submission/release disguised as author save | Staff scope and editorial decision policy pending |
| 6 Print Production | DOCX is portable draft, not printer-ready proof | Printer profiles/physical proof absent |
| 7 UX/UI | Consistent layout, labeled forms, visible states and modal behavior | Full screen contracts and user validation pending |
| 8 Accessibility/i18n | Fifteen catalog-backed interfaces, localized names/messages, persistent language preferences, independent UI/manuscript direction, RTL and Intl formatting; all-language browser switching passed and Arabic/Urdu axe scans reported zero violations | Native language, screen-reader/IME/manual WCAG review absent; browser checks cover exercised states only |
| 9 Architect | Modular local app, immutable AST/history and explicit topology limit | Approved production database/recovery model absent |
| 10 Frontend | Real Tiptap/API state, serial autosave, same editor and Undo/Redo across language switches; paste/recovery/mobile and truthful persistence fixes | Physical selection/IME, cross-browser and performance profiling pending |
| 11 Document/Collaboration | Stale writes reject; replay precedes stale check after current auth; restore creates new | Realtime/track changes explicitly deferred |
| 12 Backend/API | Transactions, current grants, localized CSRF-protected preferences; reset/write-lock, atomic key, malformed-input and worker state defects repaired | Full runtime response schema coverage and standards validators remain incomplete |
| 13 Conversion | Original preserved; warnings require review; DOCX language/bidi and break/tab/list/disabled-mark XML semantics repaired and tested | No Word-rendering certification; full malware/kernel sandbox and EPUB/PDF QA absent |
| 14 Graphics | No illustrative CSS mockup is called real geometry-derived 3D | Optional P1 3D remains unimplemented |
| 15 AI/Responsible AI | No AI endpoint/provider, no private content transfer | Consent/evaluation/terms required before enablement |
| 16 Search/Data | No private public index or prose logging | Public catalog and approved telemetry not implemented |
| 17 Commerce/Integration | No false payment/mail/distribution success | Real mail/provider sandbox contracts pending |
| 18 Finance | No authoritative money totals or payout controls simulated in UI | G5 ledger/accounting/provider evidence absent |
| 19 Security/Privacy/IP/Legal | Deny-by-default, current permission and private artifacts; scope/retention gaps visible | Independent audit, counsel, encryption/retention/MFA gates open |
| 20 SRE | WAL/FULL, process exit, backup/check and interrupted-job handling tested locally; failed backup cleanup/private restore and bounded worker output repaired | Host/region failure and production observability unproven |
| 21 QA | Meaningful negative/race/browser checks, errors repaired and rerun | No full release/conformance pass asserted |
| 22 Growth/Support | Trustworthy first-author journey and actionable messages | SEO/community/support operations unimplemented |
