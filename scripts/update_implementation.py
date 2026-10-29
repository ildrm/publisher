"""Reconcile declared identifiers with implemented local-slice evidence; never infer release approval."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'implementation'
SOURCES={'FR':'docs/02-requirements/03-feature-catalog-and-prioritization.md','CLAUSE':'docs/02-requirements/02-system-requirements-specification-srs.md','NFR':'docs/02-requirements/06-nonfunctional-requirements-and-slos.md','SCR':'docs/03-experience-design/03-screen-inventory-and-screen-specs.md','ADR':'docs/05-software-architecture/11-architecture-decision-records.md','BR':'docs/02-requirements/05-business-rules-and-permissions.md'}
def document_version(source):
 text=(ROOT/source).read_text().replace('**','')
 match=re.search(r'Version(?:/date)?\s*:?[ \t]*(\d+\.\d+(?:\.\d+)?)',text,re.I)
 if not match:raise ValueError('Missing document version: '+source)
 return match[1]
records={}
implemented={
'FR-IAM-001':('IN_PROGRESS','Identity','apps/api/publisher/identity.py; apps/api/publisher/http.py; apps/web/src/Auth.tsx','test_registration_verification_is_single_use_and_required; test_recovery_invalidates_sessions_and_consumes_token','/login; /verify; /reset','register; login; verify; recover; reset','users; sessions; account_tokens','Production mail and privileged MFA absent; BLK-002'),
'FR-IAM-002':('TESTED','Identity/Authoring','apps/api/publisher/studio.py; apps/web/src/Studio.tsx','test_viewer_no_write_non_owner_no_grant_and_revocation_before_replay; test_cross_tenant_denials_and_public_privacy','SCR-034 /app/projects/:id','grantMembership; project reads','project_memberships; projects.access_epoch','Existing verified accounts only; invitation delivery not implemented'),
'FR-DOC-001':('TESTED','Authoring','apps/api/publisher/domain.py; apps/api/publisher/studio.py; apps/web/src/Editor.tsx; apps/web/src/Dashboard.tsx','test_creation_receipt_and_key_collision; test_reorder_exact_members_and_stale_version; test_100000_words_unicode_roundtrip','SCR-004/005/006/007 /app/projects/:id','createProject; getProject; addChapter; reorder; getChapter','projects; manuscripts; chapters; chapter_revisions','Restricted schema v2; not full complex manuscript universe'),
'FR-DOC-002':('TESTED','Authoring','apps/api/publisher/studio.py; apps/api/publisher/database.py; packages/editor/autosave.ts; apps/web/src/Studio.tsx','test_concurrent_stale_save_has_one_winner; test_process_exit_after_acknowledgement_preserves_revision; tests/autosave.test.mjs; tests/e2e.mjs','SCR-007 /app/projects/:id','saveChapter; RevisionSaved v2 outbox','chapter_revisions; command_receipts; outbox','Local process/SQLite boundary only; BLK-001 regional guarantee unresolved'),
'FR-DOC-003':('TESTED','Authoring','apps/api/publisher/studio.py; apps/web/src/Studio.tsx','test_restore_creates_new_revision_and_history_is_immutable; tests/e2e.mjs','SCR-007 history panel','listRevisions; getRevision; restoreRevision','chapter_revisions.restored_from','No destructive history pruning or retention policy enabled'),
'FR-IMP-001':('IN_PROGRESS','Conversion','apps/api/publisher/formats.py; apps/api/publisher/worker.py; apps/web/src/Studio.tsx','test_import_review_is_explicit_idempotent_and_preserves_original; test_import_rejects_path_traversal_active_xml_and_archive_bomb','SCR-012 import dialog','importPreview; confirmImport; originalImport','import_previews; chapters; revisions','Structural checks only; malware/kernel sandbox/fidelity remain BLK-005'),
'FR-EXP-001':('TESTED','Conversion','apps/api/publisher/studio.py; apps/api/publisher/formats.py; apps/api/publisher/worker.py; apps/web/src/Studio.tsx','test_portable_bundle_preserves_complete_canonical_source_and_metadata; test_private_export_portability_reproducible_docx_and_html_safe; test_failed_export_preserves_previous_artifact','SCR-012 export panel','createExport; getJob; downloadArtifact','manuscript_versions; conversion_jobs; export_artifacts','Five portable formats including canonical metadata bundle; not EPUB/PDF or full print/a11y conformance'),
'FR-OPS-001':('IN_PROGRESS','Operations','apps/api/publisher/database.py; apps/api/main.py; apps/api/publisher/identity.py','test_backup_restore_and_audit_do_not_leak_manuscript_text','CLI backup/check; /api/v1/audit','getOwnAudit; backup','audit_events; all application tables','Local backup/restore and hash chain only; no external audit anchoring or regional DR')}
feature_sections={}
for kind,source in SOURCES.items():
 lines=(ROOT/source).read_text().splitlines();section=''
 for line_number,line in enumerate(lines,1):
  if line.startswith('## '):section=line[3:]
  if not line.startswith('|'):continue
  first=line.split('|')[1].strip()
  pattern={'FR':r'FR-[A-Z0-9]+-\d{3}$','CLAUSE':r'FR-[A-Z0-9]+-\d{3}\.\d+$','NFR':r'NFR-[A-Z0-9]+-\d{3}$','SCR':r'SCR-\d{3}','ADR':r'ADR-\d{3}','BR':r'BR-\d{3}$'}[kind]
  match=re.match(pattern,first)
  if not match:continue
  ident=match[0]
  if ident in records:continue
  title=line.split('|')[2].strip() if len(line.split('|'))>2 else ident
  state='DEFERRED' if kind=='FR' and int(ident.rsplit('-',1)[-1])>=100 else 'NOT_ASSESSED'
  phase='P2' if 'P2' in line else 'P3' if 'P3' in line else 'P1' if ('P1' in line or state=='DEFERRED') else 'P0'
  if kind=='SCR':phase='P1' if 'P1' in line else 'P0'
  fields={'id':ident,'kind':kind,'source':source,'section':section,'line':line_number,'sourceVersion':'0.2','sourceApproval':'DRAFT / human approval not supplied','outcome':title,'release':phase,'moscow':'Could' if phase=='P2' else "Won’t until approved" if phase=='P3' else 'Should' if phase=='P1' else 'Must candidate','owner':'Product/Engineering; domain specialist before activation','dependencies':'Core identity, current resource permission and previous phase gates','constraints':'Private-by-default; no AI/live money/public release by default; rights, consent and finance gates fail closed','boundedContext':'Unnormalized expansion' if state=='DEFERRED' else kind,'ui':'Not implemented/normalized for this record','apiEvent':'Not implemented/normalized for this record','dataMigration':'Not implemented/normalized for this record','tests':'No execution evidence for this record','evidence':'','state':state,'codePaths':'','risk':'Grouped/unapproved design must not be mistaken for implementation','blocker':'BLK-006 / atomic expansion and actual scope approval' if state=='DEFERRED' else 'Pending implementation and applicable specialist evidence','nextAtomicTask':'Decompose and approve before enabling phase' if state=='DEFERRED' else 'Assess concrete acceptance and dependencies before implementation'}
  if kind=='FR' and int(ident.rsplit('-',1)[-1])>=100 and 'P0' in line:
   fields.update(state='IN_PROGRESS',release='P0',moscow='Must baseline; extensions not approved',codePaths='apps/api/publisher/; apps/web/src/ (linked core subset only)',tests='See referenced core FR/NFR tests, not complete compound acceptance',evidence='implementation/coverage-and-gaps.md; implementation/evidence/verification.json',boundedContext='Compound baseline plus unapproved expansion',blocker='P0 core subset implemented where mapped; remaining compound requirement, deletion/privacy/MFA/performance/IME details remain open',nextAtomicTask='Split baseline from enhancement and close each missing acceptance clause without deferring mandatory controls')
  fields['sourceVersion']=document_version(source)
  if kind=='FR':
   cells=[cell.strip() for cell in line.split('|')[1:-1]]
   source_approach=cells[3 if len(cells)==7 else -1].lower()
   planned='BUILD_NATIVE' if source_approach.startswith('native') else 'INTEGRATE' if source_approach.startswith('integrat') else 'LICENSE' if 'licensed' in source_approach else 'PARTNER' if 'partner' in source_approach else 'DEFER' if 'defer' in source_approach else 'BUILD_NATIVE'
   fields['plannedApproach']=planned;fields['buildApproach']='DEFER' if fields['state']=='DEFERRED' else planned
  else:fields['plannedApproach']='N/A';fields['buildApproach']='N/A'
  parent=ident.split('.')[0]
  if parent in implemented:
   st,context,code,tests,ui,api,data,risks=implemented[parent]
   fields.update(state=st,boundedContext=context,codePaths=code,tests=tests,ui=ui,apiEvent=api,dataMigration='apps/api/publisher/migrations/001_authoring.sql: '+data,risk=risks,blocker=risks,evidence='implementation/evidence/verification.json; implementation/evidence/e2e-results.json',nextAtomicTask='Close remaining clause/manual/production gaps before advancing beyond TESTED')
  if ident=='FR-IAM-001.2':fields.update(state='READY',codePaths='',tests='',evidence='',blocker='Privileged roles not yet implemented; they must fail closed until MFA exists',nextAtomicTask='Implement staff enrollment and step-up MFA with tests')
  if ident in ('FR-3D-001',):fields.update(state='DEFERRED',release='P1',blocker='Optional P1; geometry/printer inputs and funded scope not supplied')
  if parent in ('FR-FMT-001','FR-COM-001','FR-FIN-001'):fields.update(state='BLOCKED_INPUT',blocker='BLK-003/004/005: provider/contract/profile or standards evidence absent',nextAtomicTask='Implement only independently testable sandbox/domain rules; obtain missing activation evidence')
  if parent in ('FR-PUB-001','FR-PUB-002','FR-RGT-001','FR-CAT-001'):fields.update(state='READY',blocker='Publication activation still requires BLK-003 and predecessor gates; no runtime code',nextAtomicTask='Staff MFA → frozen submission/review → scoped rights → immutable edition release tests')
  records[ident]=fields
# Cross-cutting requirements are assessed independently from their parent features.
nfr_states={'NFR-SEC-001':'TESTED','NFR-SEC-002':'BLOCKED_INPUT','NFR-SEC-003':'IN_PROGRESS','NFR-SEC-004':'READY','NFR-PRIV-001':'TESTED','NFR-PRIV-002':'BLOCKED_INPUT','NFR-REL-001':'TESTED','NFR-REL-003':'BLOCKED_INPUT','NFR-REL-004':'TESTED','NFR-A11Y-001':'IN_PROGRESS','NFR-A11Y-002':'IN_PROGRESS','NFR-I18N-001':'IN_PROGRESS','NFR-I18N-002':'IN_PROGRESS','NFR-PERF-004':'BLOCKED_INPUT','NFR-PERF-005':'DEFERRED','NFR-OPS-001':'READY','NFR-OPS-002':'TESTED','NFR-FIN-001':'BLOCKED_INPUT'}
for ident,state in nfr_states.items():
 if ident in records:records[ident].update(state=state,boundedContext='Cross-cutting assurance',tests='tests/test_application.py; tests/e2e.mjs (bounded local coverage only)',codePaths='apps/api/publisher/; apps/web/src/; packages/editor/',evidence='implementation/security-review.md; implementation/accessibility-review.md; implementation/evidence/verification.json',blocker='See BLK-001–008; local tests do not establish full target or independent review',nextAtomicTask='Measure/prove the exact remaining NFR scope before any conformance or release claim')
for ident in ('NFR-I18N-001','NFR-I18N-002'):
 if ident in records:records[ident].update(boundedContext='Interface localization and manuscript independence',ui='All implemented Author Studio screens; LanguageSwitcher',apiEvent='Accept-Language; PUT /api/preferences; localized message descriptors',dataMigration='apps/api/publisher/migrations/002_interface_locales.sql: users.locale; manuscripts unchanged',codePaths='packages/i18n/; apps/web/src/; apps/api/publisher/localization.py',tests='tests/test_localization.py; tests/i18n.test.mjs; tests/i18n.e2e.mjs; test_docx_preserves_manuscript_languages_bidi_and_deterministic_bytes',evidence='implementation/multilingual-review.md; implementation/evidence/i18n-e2e-results.json; implementation/evidence/i18n-axe-results.json; implementation/evidence/verification.json',blocker='15 catalogs and automated interface/RTL/draft checks implemented; native linguistic review, physical IME/screen reader and full format fidelity remain open',nextAtomicTask='Native-language editorial review and real assistive/IME device testing across selected locales')
for ident in ['ADR-001','ADR-002','ADR-003','ADR-004','ADR-005']:
 if ident in records:records[ident].update(state='IN_PROGRESS',codePaths='apps/api/publisher/; apps/web/src/; packages/editor/',evidence='implementation/decisions.md; implementation/document-conflicts.md',blocker='Proposed architecture applied locally only; production/approved rendition boundaries remain unproven')
for ident in ['BR-001','BR-009','BR-010']:
 if ident in records:records[ident].update(state='TESTED',codePaths='apps/api/publisher/',tests='tests/test_application.py',evidence='implementation/evidence/verification.json',blocker='Implemented-resource scope and local durability only; full phase audit pending')
if 'SCR-010' in records:records['SCR-010'].update(state='DEFERRED',release='P1',blocker='Comments/track changes screen not implemented or approved; current sharing is SCR-034')
# Screen records map to implemented surfaces without claiming all screen acceptance criteria satisfied.
for screen in ['SCR-003','SCR-004','SCR-005','SCR-006','SCR-007','SCR-012','SCR-034']:
 if screen in records:
  records[screen].update(state='IN_PROGRESS' if screen=='SCR-010' else 'TESTED',codePaths='apps/web/src/',tests='tests/e2e.mjs',evidence='implementation/evidence/e2e-results.json',blocker='Full screen contract, manual a11y and later-phase functionality remain unverified')
api=json.loads((ROOT/'docs/contracts/openapi.yaml').read_text())
for path,methods in api['paths'].items():
 for method,op in methods.items():
  if 'operationId' not in op:continue
  ident=op['operationId'];base=next(iter(records.values())).copy();base.update(id=ident,kind='API',source='docs/contracts/openapi.yaml',section=method.upper()+' '+path,line=next((i for i,line in enumerate((ROOT/'docs/contracts/openapi.yaml').read_text().splitlines(),1) if '\"operationId\": \"'+ident+'\"' in line),1),sourceVersion='0.2.0',boundedContext='API reference (not runtime conformance)',ui='See runtime screen mapping where implemented',dataMigration='No persistence implied by a reference API operation',outcome=op['summary'],state='NOT_ASSESSED',codePaths='',evidence='',tests='',apiEvent=ident,blocker='Representative API may differ from local cookie/schema-v2 runtime; see CF-001/002',nextAtomicTask='Reconcile against apps/api/openapi.json before implementation');records[ident]=base
for operation in ['createProject','getChapter','saveChapter','restoreRevision','createExport','getJob','grantMembership','revokeMembership','getAudit','createImport','confirmImport']:
 if operation in records:records[operation].update(state='IN_PROGRESS',codePaths='apps/api/publisher/http.py; apps/api/openapi.json',tests='tests/test_application.py; tests/e2e.mjs',evidence='implementation/document-conflicts.md; implementation/evidence/verification.json',blocker='Runtime cookie/AST-v2 or route/input deltas in CF-001/002; not exact representative-v1 contract conformance')
for event in ['RevisionSaved']:
 base=next(iter(records.values())).copy();base.update(id=event,kind='EVENT',source='docs/contracts/asyncapi.yaml',section='revisionSaved',line=1,sourceVersion='v1 reference / v2 local',outcome='Private committed revision reference only',state='IN_PROGRESS',codePaths='apps/api/publisher/studio.py',tests='test_backup_restore_and_audit_do_not_leak_manuscript_text',evidence='implementation/evidence/verification.json',apiEvent='Local RevisionSaved v2 outbox; v1 payload not emitted',blocker='Dispatcher, inbox consumers and v2 AsyncAPI remain unimplemented',nextAtomicTask='Specify and test v2 event consumers with durable outbox dispatch');records[event]=base
runtime=json.loads((ROOT/'apps/api/openapi.json').read_text())
for path,methods in runtime['paths'].items():
 for method,op in methods.items():
  ident=op['operationId']
  if ident not in records:
   base=next(iter(records.values())).copy();base.update(id=ident,kind='API_RUNTIME',source='apps/api/openapi.json',section=method.upper()+' '+path,line=1,sourceVersion='0.1.0',sourceApproval='Local implementation decision; no production approval',outcome=op['summary'],state='IN_PROGRESS',release='P0',codePaths='apps/api/publisher/http.py',boundedContext='Local runtime API',tests='tests/test_application.py; tests/e2e.mjs (operation coverage varies)',evidence='implementation/evidence/verification.json; implementation/evidence/e2e-results.json',blocker='Response schemas and exact per-operation HTTP coverage remain partial; no production activation',nextAtomicTask='Complete explicit response schemas and operation-level contract tests');records[ident]=base
  records[ident]['runtimeContract']='apps/api/openapi.json: '+method.upper()+' '+path
journeys={'IAM':('Trustworthy onboarding and least privilege','New author / coauthor'), 'DOC':('Author activation and durable writing','New author / migrating author'), 'IMP':('Migration and semantic fidelity','Migrating author'), 'EXP':('Author portability and trust','New or migrating author without publication'), 'PUB':('Quality-controlled publishable titles','Editor / publishing director'), 'RGT':('Rights-valid release and author ownership','Publishing director / production specialist'), 'CAT':('Public discovery and safe samples','Buyer / reader'), 'COM':('Licensed purchase and reader access','Buyer / reader'), 'FIN':('Auditable author earnings and payouts','Finance admin'), 'OPS':('Recovery, privacy and support','Support agent')}
for ident,r in records.items():
 family=ident.split('-')[1] if ident.startswith('FR-') else None
 goal,journey=journeys.get(family,('Requires exact per-record KPI normalization before phase commitment','See source journey; detailed association not yet normalized'))
 r['businessGoal']=goal;r['journey']=journey
 for field,source in [('journeySource','docs/01-discovery-strategy/05-service-blueprints-and-user-journeys.md'),('goalSource','docs/01-discovery-strategy/06-product-kpis-and-analytics-plan.md')]:r[field]=source+' v'+document_version(source)
 if r['kind'] in ('API','API_RUNTIME','EVENT'):
  r.update(plannedApproach='N/A',buildApproach='N/A',owner='API/domain engineering; security and QA review',risk='Only mapped runtime behavior has evidence; reference operation is not a completion claim')
 if r['kind']=='API_RUNTIME':
  r.update(sourceVersion=runtime['info']['version'],apiEvent=ident,dataMigration='See runtime domain migrations; no unrelated identity mapping inferred',ui='See linked implemented screen; operation-specific mapping remains partial')
 r.setdefault('runtimeContract','')
old_path=OUT/'requirements-status.json';old={r['id']:r for r in json.loads(old_path.read_text()).get('records',[])} if old_path.exists() else {}
for ident,r in records.items():
 history=old.get(ident,{}).get('history',[])
 if not history or history[-1]['state']!=r['state']:history.append({'date':'2026-10-29','state':r['state'],'evidence':r['evidence'] or 'Source normalization only; no implemented result'})
 r['history']=history
counts=Counter(r['state'] for r in records.values());phase_counts=Counter(r['release'] for r in records.values())
old_path.write_text(json.dumps({'date':'2026-10-29','scope':'Local authoring increment; status is never inferred from file presence. P1/P2 grouped drafts are not accepted implementation-ready commitments.','counts':dict(counts),'releaseCounts':dict(phase_counts),'records':list(records.values())},indent=2,ensure_ascii=False)+'\n')
with (OUT/'requirements-status.csv').open('w',newline='') as stream:
 fields=[k for k in next(iter(records.values())) if k!='history'];writer=csv.DictWriter(stream,fields,extrasaction='ignore');writer.writeheader();writer.writerows(records.values())
summary='# Requirement coverage and remaining gaps\n\nGenerated 2026-10-29. Counts include capability parents, atomic SRS clauses, NFRs, screens, ADRs, business rules, API operations and event records; they are **not independent feature counts**. All evidence is scoped to the local authoring increment. No item is RELEASE_READY.\n\n| State | Records |\n|---|---|\n'+''.join(f'| {k} | {v} |\n' for k,v in sorted(counts.items()))+'\n| Declared release | Records |\n|---|---|\n'+''.join(f'| {k} | {v} |\n' for k,v in sorted(phase_counts.items()))+'\nSee requirements-status.json/CSV for exact source version/line, code/data/API/test/evidence, missing scope, owner and next task for every record. Browser checks do not establish production durability, full accessibility or later-phase functionality. Expansion A–R records remain explicit; none is silently shipped.\n'
(OUT/'coverage-and-gaps.md').write_text(summary)
source='# Adopted source map\n\nSource drafts carry their actual per-document versions below. The user authorized reversible local implementation and expanded language support; this does not imply specialist or production approval. The complete source inventory includes hashes; this map links the implemented core to actual code and evidence. Parent rows are partial where stated.\n\n| ID | Exact source | Runtime code / behavior | Evidence |\n|---|---|---|---|\n'
for ident in implemented:
 r=records[ident];source+=f"| {ident} | [{Path(r['source']).name}](../{r['source']}) line {r['line']} ({r['section']}) v{r['sourceVersion']} | {r['codePaths']} | {r['tests']} |\n"
source+='\nDesign tokens and screen contracts come from docs/03-experience-design/03 and /04; persistence/authorization/save protocol from ARC-05/06/07; portability/recovery from PUB-002/003 and REQ-07; tests from QA-01/02/04/06 and runtime tests named above. Stack/schema/cookie differences are explicitly recorded as CF-001/002 and IMP-DEC-001–005, not attributed to human approval.\n'
source+='\nLanguage scope: NFR-I18N-001/002 in '+SOURCES['NFR']+' v'+document_version(SOURCES['NFR'])+'; packages/i18n/languages.json and 15 catalogs; migration 002; tests/test_localization.py, tests/i18n.test.mjs and tests/i18n.e2e.mjs. See multilingual-review.md for language-selection sources, 22-role critique and remaining manual evidence.\n'
(OUT/'source-map.md').write_text(source)
inventory=[]
for path in sorted((ROOT/'docs').rglob('*')):
 if not path.is_file() or '__pycache__' in path.parts or path.suffix not in {'.md','.json','.yaml','.mmd','.puml','.py','.mjs'}:continue
 data=path.read_bytes();lines=data.decode().splitlines()
 inventory.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'title':lines[0] if lines else ''})
(OUT/'source-inventory.json').write_text(json.dumps(inventory,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'records':len(records),'counts':dict(counts),'releaseCounts':dict(phase_counts)}))
