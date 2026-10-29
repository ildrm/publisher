#!/usr/bin/env python3
"""Repository documentation checks. Structural checks, not full OpenAPI/AsyncAPI or diagram rendering."""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
errors = []
def require(ok, message):
    if not ok: errors.append(message)
def load(path):
    try: return json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        errors.append(f'{path.relative_to(ROOT)}: {exc}')
        return {}
def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values(): yield from walk(child)
    elif isinstance(value, list):
        for child in value: yield from walk(child)
def pointer(doc, fragment):
    cur = doc
    if not fragment: return cur
    if not fragment.startswith('/'): raise ValueError('unsupported reference fragment')
    for part in fragment[1:].split('/'):
        part = unquote(part).replace('~1', '/').replace('~0', '~')
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur

def instance_check(value, schema, document, where):
    """Small explicit subset for the checked event fixture. Not a JSON Schema implementation."""
    if '$ref' in schema:
        file, _, fragment = schema['$ref'].partition('#')
        target = (document.parent/file).resolve() if file else document
        return instance_check(value, pointer(load(target), fragment), target, where)
    typ = schema.get('type')
    types = {'object':lambda x:isinstance(x,dict), 'array':lambda x:isinstance(x,list),
             'string':lambda x:isinstance(x,str), 'integer':lambda x:type(x) is int,
             'boolean':lambda x:type(x) is bool,'null':lambda x:x is None}
    if typ:
        allowed=typ if isinstance(typ,list) else [typ]
        valid=any(types[t](value) for t in allowed if t in types)
        require(valid,where+': wrong fixture type')
        if not valid: return
    if 'const' in schema: require(value==schema['const'],where+': wrong const')
    if 'enum' in schema: require(value in schema['enum'],where+': outside enum')
    if isinstance(value,dict):
        for key in schema.get('required',[]): require(key in value,where+': missing '+key)
        props=schema.get('properties',{})
        if schema.get('additionalProperties') is False: require(set(value)<=set(props),where+': unexpected fields')
        for key,sub in props.items():
            if key in value: instance_check(value[key],sub,document,where+'.'+key)
    if isinstance(value,list):
        if 'minItems' in schema: require(len(value)>=schema['minItems'],where+': too few items')
        for i,item in enumerate(value): instance_check(item,schema.get('items',{}),document,f'{where}[{i}]')
    if isinstance(value,str):
        if 'minLength' in schema: require(len(value)>=schema['minLength'],where+': too short')
        if 'maxLength' in schema: require(len(value)<=schema['maxLength'],where+': too long')
        if 'pattern' in schema: require(bool(re.search(schema['pattern'],value)),where+': pattern mismatch')
        if schema.get('format')=='uuid':
            import uuid
            try: uuid.UUID(value)
            except ValueError: errors.append(where+': invalid UUID fixture')
        if schema.get('format')=='date-time':
            from datetime import datetime
            try: require(datetime.fromisoformat(value.replace('Z','+00:00')).tzinfo is not None,where+': missing timezone')
            except ValueError: errors.append(where+': invalid timestamp fixture')
    if type(value) is int and 'minimum' in schema: require(value>=schema['minimum'],where+': below minimum')

manifest=load(DOCS/'document-manifest.json')
import hashlib
source_path=DOCS / manifest.get('source','source/master-prompt.md')
require(source_path.is_file() and hashlib.sha256(source_path.read_bytes()).hexdigest()==manifest.get('sourceSha256'),'Original source hash mismatch')
for relative in manifest.get('requiredMarkdown',[]): require((DOCS/relative).is_file(),'Missing required artifact: '+relative)
markdown=list(DOCS.rglob('*.md'))
ids={}; link_count=0
for file in markdown:
    data=file.read_text()
    first=data.splitlines()[0] if data else ''
    primary=re.match(r'#\s+([A-Z]+-[0-9]+)\s*[—–-]',first)
    if primary:
        require(primary[1] not in ids,f'Duplicate document ID {primary[1]}: {file.relative_to(ROOT)} and {ids.get(primary[1])}')
        ids[primary[1]]=str(file.relative_to(ROOT))
    require('source' in file.relative_to(DOCS).parts or not re.search(r'\bTBD\b',data),f'{file.relative_to(ROOT)}: unowned TBD marker')
    for target in re.findall(r'\]\(([^)]+)\)',data):
        if re.match(r'^(https?:|mailto:|#)',target): continue
        relative=unquote(target.split('#')[0].strip('<>'))
        require((file.parent/relative).resolve().exists(),f'Broken link {file.relative_to(ROOT)} -> {target}')
        link_count+=1
contracts=list((DOCS/'contracts').rglob('*.json'))+list((DOCS/'contracts').glob('*.yaml'))
contracts += list((ROOT/'apps/api').glob('openapi.json')) + list((ROOT/'apps/api/events').glob('*.schema.json'))
refs=0
for file in contracts:
    data=load(file)
    for node in walk(data):
        if '$ref' not in node: continue
        ref=node['$ref']; refs+=1
        if re.match(r'^https?:',ref): continue
        path,_,frag=ref.partition('#'); target=(file.parent/path).resolve() if path else file
        try: pointer(load(target),frag)
        except (KeyError,ValueError,TypeError,IndexError) as exc: errors.append(f'{file.relative_to(ROOT)}: unresolved {ref}: {exc}')
api=load(DOCS/'contracts/openapi.yaml'); operations={}
requirement_text=(DOCS/'02-requirements/02-system-requirements-specification-srs.md').read_text()+(DOCS/'02-requirements/03-feature-catalog-and-prioritization.md').read_text()
require(api.get('openapi')=='3.1.1','OpenAPI target version changed without checker review')
for route,path in api.get('paths',{}).items():
    for verb,op in path.items():
        if verb not in {'get','put','post','patch','delete','options','head','trace'}: continue
        name=op.get('operationId'); require(bool(name) and name not in operations,'Duplicate/missing operationId: '+str(name)); operations[name]=op
        require(bool(op.get('responses')),f'{name}: responses missing')
        require(bool(op.get('x-requirements')),f'{name}: requirement mapping missing')
        for requirement_id in op.get('x-requirements',[]): require(requirement_id in requirement_text,f'{name}: undefined requirement {requirement_id}')
        if not op.get('security',api.get('security')):
            require(name in {'listCatalog','receivePaymentEvent'},f'{name}: unreviewed authentication bypass')
        for parameter in re.findall(r'\{([^}]+)\}',route):
            require(any(p.get('name')==parameter and p.get('in')=='path' and p.get('required') for p in op.get('parameters',[])),f'{name}: path parameter {parameter} missing')
        if verb in {'put','post','delete'} and name!='receivePaymentEvent':
            require(any(p.get('$ref','').endswith('/IdempotencyKey') for p in op.get('parameters',[])),f'{name}: idempotency contract missing')
asyncapi=load(DOCS/'contracts/asyncapi.yaml');require(asyncapi.get('asyncapi')=='3.0.0','AsyncAPI target mismatch')
instance_check(load(DOCS/'contracts/schemas/revision-saved.v1.json'),load(DOCS/'contracts/schemas/revision-saved.v1.schema.json'),DOCS/'contracts/schemas/revision-saved.v1.schema.json','RevisionSaved fixture')
blocks=0
for file in (DOCS/'diagrams').glob('*.puml'):
    data=file.read_text(); starts=len(re.findall(r'^@startuml',data,re.M)); ends=len(re.findall(r'^@enduml',data,re.M))
    require(starts>0 and starts==ends,f'{file.name}: unbalanced PlantUML blocks');blocks+=starts
    require('SOURCE NOT RENDER-VALIDATED' in data or 'RENDER-VALIDATED' in data,f'{file.name}: render status missing')
    require('legend' in data.lower(),f'{file.name}: legend missing')
for file in (DOCS/'diagrams').glob('*.mmd'):
    require('SOURCE NOT RENDER-VALIDATED' in file.read_text() or 'RENDER-VALIDATED' in file.read_text(),f'{file.name}: render status missing')
result={'checkDate':'2026-10-29','status':'pass' if not errors else 'fail','requiredMarkdownPresent':sum((DOCS/x).is_file() for x in manifest.get('requiredMarkdown',[])),'requiredMarkdownTotal':len(manifest.get('requiredMarkdown',[])),'markdownFiles':len(markdown),'localMarkdownLinksChecked':link_count,'contractReferencesChecked':refs,'openapiOperations':len(operations),'plantUmlBlocksChecked':blocks,'diagramRenderValidated':False,'fullOpenApiAsyncApiSchemaValidation':False,'checks':'File presence, relative link targets, document ID uniqueness, unowned TBD markers, JSON syntax/local references, selected API invariants, bounded event fixture checks and PlantUML delimiters. No full standards validation or browser/production testing.','errors':errors}
if '--write-report' in sys.argv: (DOCS/'validation-report.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(bool(errors))
