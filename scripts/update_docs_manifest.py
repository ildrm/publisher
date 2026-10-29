#!/usr/bin/env python3
"""Rebuild the human manifest from tracked requirements and actual files."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1];docs=root/'docs'
m=json.loads((docs/'document-manifest.json').read_text());required=m['requiredMarkdown']
present=sum((docs/p).is_file() for p in required)
header='''# DOC-000 — Publishing documentation manifest and executive brief

Version 0.2 · 2026-10-29 · **Draft — revised after cross-document review; human approval pending**. Author/accountable: Documentation Lead. Consulted: Product, Editorial, UX, Architecture, Security, Accessibility, Finance, QA, SRE and Delivery. Reviewer: Requirements Lead. Approver/decision owner: Product Owner and Executive Sponsor. Assumptions: ASM-001–012; related requirements: core FR/NFRs and the expansion capability register. Open decisions: launch market, capacity, rights/royalty terms, providers and implementation evidence. References: [source prompt](source/master-prompt.md), [decision register](00-governance/02-decisions-and-open-questions.md), [quality audit](QUALITY_AUDIT.md) and [change log](CHANGELOG.md).

## Contents

- [Executive brief](#executive-brief)
- [Review status and coverage](#review-status-and-coverage)
- [Required document manifest](#required-document-manifest)
- [Additional artifacts and checks](#additional-artifacts-and-checks)
- [Simulated review checkpoint](#simulated-review-checkpoint)

## Implementation checkpoint

A working local Author Studio now exists. See the [implementation guide](../implementation/README.md), [execution registry](../implementation/requirements-status.json), [test evidence](../implementation/test-evidence.md), and [remaining release gates](../implementation/release-readiness.md). The documentation review status below is not application completion or approval.

## Executive brief

The proposed model is a curated publishing house with a portable author studio. Authors can write and export without publishing. Staff evaluate frozen submissions and release only versions with scoped rights, approvals and proof. A modular monolith with isolated conversion workers is proposed to protect transaction consistency and limit deployment complexity; its alternatives and extraction triggers are documented. Private drafts are excluded from public indexes and default AI use. Editing semantics, immutable revisions, submissions, editions, renditions, listings, purchases and financial records remain distinct.

This repository contains documentation, diagram sources, contracts and bounded executable reference illustrations. It is a design draft; specialist approval and production behavior require real evidence. The full feature universe is mapped, while grouped expansion features still require atomic specifications and complete traceability before phase commitment.

## Review status and coverage

__PRESENT__ of __TOTAL__ required named Markdown artifacts exist (__PERCENT__% file-presence coverage). This denominator excludes additional source/standard/audit files, diagrams, contracts and samples, which are listed below. Presence is not completeness, implementation or conformance coverage. The [18-gate quality audit](QUALITY_AUDIT.md) records corrected findings, partial criteria, owners and decision milestones.

| Batch | Result of this review | Remaining evidence |
|---|---|---|
| 0 Alignment | Registers, glossary, 22-role RACI and control process reviewed | Named human owners and actual decisions |
| 1 Discovery | Dated competitor matrix, standards, personas, journeys, unit economics and KPIs | Interviews, independent comparison, market/vendor eligibility |
| 2 Product | Core P0 clauses/scenarios, 175 expansion records, permissions, NFRs and recovery | Atomic expansion and full P1/P2 UI/API/test mappings |
| 3 Experience / publishing | 35 screen contracts, design/accessibility, formats, rights, proof, finance and 3D sources | Prototype/usability validation, physical proof, approved policies |
| 4 Architecture | Domain/data/ADR design, C4/UML/ERD, representative API/event/AST schemas | Rendering, full validator/toolchain and implemented integration proof |
| 5 Engineering / assurance | Handbook, reference examples, QA, security and operations runbooks | Actual system tests, accessibility/security and restore evidence |
| 6 Delivery | Three scope options, dependency roadmap, team ranges, RFP/scorecard, launch/exit plan and audit | Staffed estimates, bids and real approvals |

## Required document manifest

Entries marked Missing identify absent paths; present documents are drafts, and an entry does not imply approval.

'''
header=header.replace('__PRESENT__',str(present)).replace('__TOTAL__',str(len(required))).replace('__PERCENT__',f'{present/len(required)*100:.1f}')
out=[header];groups={}
for p in required:
 if p!='README.md':groups.setdefault(p.split('/')[0],[]).append(p)
for group,paths in groups.items():
 out.append(f'### {group}\n\n| Document | Status |\n|---|---|\n')
 for p in paths:
  out.append(f'| [{Path(p).name}]({p}) | Draft; see audit for open work |\n' if (docs/p).exists() else f'| {p} | Missing |\n')
 out.append('\n')
out.append('''## Additional artifacts and checks

- [Standards/source register](01-discovery-strategy/07-standards-and-source-register.md), [source prompt](source/master-prompt.md) and [source hash/required-path manifest](document-manifest.json).
- [Diagram index](05-software-architecture/04-uml-and-erd-index.md), [C4 architecture](05-software-architecture/03-c4-context-container-component.md) and actual sources in `diagrams/`.
- [OpenAPI](contracts/openapi.yaml), [AsyncAPI](contracts/asyncapi.yaml), [AST schema](contracts/schemas/manuscript-ast.v1.schema.json), [event schema](contracts/schemas/revision-saved.v1.schema.json) and [event fixture](contracts/schemas/revision-saved.v1.json).
- [Reference sample context and test instructions](samples/reference/README.md), [autosave controller](samples/frontend-autosave.mjs), [quality audit](QUALITY_AUDIT.md), [structural validation report](validation-report.json) and [change log](CHANGELOG.md).

From the repository root:

```sh
python3 scripts/update_docs_manifest.py
python3 scripts/validate_docs.py --write-report
python3 -m unittest discover -s docs/samples/tests -t docs/samples -v
node --test docs/samples/tests/autosave.test.mjs
```

The structural checker verifies file presence, relative link targets, IDs, JSON/local references, selected API rules, a bounded event fixture and PlantUML block delimiters. It does not render diagrams or fully validate OpenAPI/AsyncAPI against their standards. The sample tests exercise teaching code, not an implemented publishing service. Exact evidence and limitations are in the audit and report.

## Simulated review checkpoint

Product/Requirements corrected scope and traceability conflicts; UX/Publishing corrected screen validation, rights and proof flow; Architecture/Security corrected authorization and retry boundaries; Finance clarified balanced postings and reconciliation; QA/Delivery made validation, milestones and unresolved evidence explicit. Residual risks and required human approvers are recorded in the quality audit and governance register. No real specialist or stakeholder approval is implied.
''')
(docs/'README.md').write_text(''.join(out))
print(f'{present}/{len(required)} required Markdown files present')
