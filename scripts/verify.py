"""Record real local verification exit codes and logs. Browser tests are run separately."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'implementation/evidence';out.mkdir(exist_ok=True)
commands=[('build',['npm','run','build']),('application-tests',['npm','test']),('documentation',['python3','scripts/validate_docs.py']),('reference-python-tests',['python3','-m','unittest','discover','-s','docs/samples/tests','-t','docs/samples','-v']),('reference-js-tests',['node','--test','docs/samples/tests/autosave.test.mjs'])]
records=[]
for name,cmd in commands:
    started=datetime.now(timezone.utc).isoformat();tick=time.monotonic()
    result=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (out/(name+'.log')).write_text(result.stdout)
    records.append({'name':name,'command':cmd,'startedAt':started,'exitCode':result.returncode,'seconds':round(time.monotonic()-tick,3),'log':'implementation/evidence/'+name+'.log'})
    print(name+': exit '+str(result.returncode),flush=True)
versions={k:subprocess.check_output(v,text=True).strip() for k,v in {'node':['node','--version'],'npm':['npm','--version'],'python':['python3','--version']}.items()}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
build={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'apps/web/dist').rglob('*') if p.is_file()}
source_files=[p for directory in ('apps','packages','tests','scripts') for p in (ROOT/directory).rglob('*') if p.is_file() and not {'dist','__pycache__','node_modules'}&set(p.parts) and p.suffix in {'.py','.ts','.tsx','.js','.mjs','.json','.sql','.css'}]
source_files.extend(ROOT/name for name in ('package.json','package-lock.json','tsconfig.json'))
report={'generatedAt':datetime.now(timezone.utc).isoformat(),'environment':versions,'status':'PASS' if all(r['exitCode']==0 for r in records) else 'FAIL','commands':records,'sourceFilesSha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(source_files)},'packageLockSha256':sha(ROOT/'package-lock.json'),'migrationSha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'apps/api/publisher/migrations').glob('*.sql'))},'localeCatalogSha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'packages/i18n').rglob('*.json'))},'buildArtifacts':build,'scope':'Local application and existing documentation samples only. Browser evidence is separate. No production/NFR/conformance/provider assurance inferred.'}
(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
sys.exit(0 if report['status']=='PASS' else 1)
