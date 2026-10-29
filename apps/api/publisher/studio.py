"""Authoring use cases. Current grants, CAS revisions, receipts, snapshots and outbox commit together."""
from pathlib import Path
import base64
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
from .database import Database, now
from .domain import Problem, uid, label, language, canonical, digest, validate_ast, empty_ast, plain_text
from .identity import audit
from .localization import translate


class Studio:
    def __init__(self,db: Database):self.db=db

    @staticmethod
    def authorize(c,actor: str,project_id: str,edit: bool=False,owner: bool=False):
        row=c.execute('SELECT p.*,m.role FROM projects p JOIN project_memberships m ON m.project_id=p.id WHERE p.id=? AND m.user_id=?',(project_id,actor)).fetchone()
        if not row:raise Problem(404,'NOT_FOUND','This project is unavailable or you no longer have access.')
        if (edit and row['role']=='viewer') or (owner and row['role']!='owner'):
            raise Problem(403,'FORBIDDEN','Your project role does not permit this action.')
        return row

    @staticmethod
    def _receipt(c,actor,op,resource,key,request):
        if not isinstance(key,str) or not re.fullmatch(r'[A-Za-z0-9._:-]{16,128}',key):raise Problem(422,'COMMAND_KEY','Provide an Idempotency-Key of 16–128 safe characters.')
        row=c.execute('SELECT * FROM command_receipts WHERE actor_id=? AND operation=? AND resource=? AND command_key=?',(actor,op,resource,key)).fetchone()
        if row:
            if row['request_hash']!=digest(request):raise Problem(409,'KEY_REUSED','This command key was already used for a different request.')
            return json.loads(row['response_json'])
        return None

    @staticmethod
    def _record(c,actor,op,resource,key,request,result):
        c.execute('INSERT INTO command_receipts VALUES(?,?,?,?,?,?)',(actor,op,resource,key,digest(request),canonical(result)))
        return result

    @staticmethod
    def _match(expected: str | None,current: str):
        if expected is None:raise Problem(428,'VERSION_REQUIRED','Reload the current version before making this change.')
        if expected!=current:raise Problem(412,'STALE_VERSION','A newer version exists. Keep your unsaved text, compare versions and review before saving.')

    @staticmethod
    def _revision(c,actor,project_id,chapter_id,ast,restored_from=None):
        prior=c.execute('SELECT COALESCE(MAX(sequence),0) FROM chapter_revisions WHERE chapter_id=?',(chapter_id,)).fetchone()[0]
        revision_id=uid();saved_at=now()
        c.execute('INSERT INTO chapter_revisions VALUES(?,?,?,?,?,?,?,?,?)',(revision_id,project_id,chapter_id,prior+1,canonical(ast),digest(ast),actor,restored_from,saved_at))
        c.execute('UPDATE chapters SET current_revision_id=? WHERE id=?',(revision_id,chapter_id))
        c.execute('UPDATE projects SET updated_at=? WHERE id=?',(saved_at,project_id))
        payload={'chapterId':chapter_id,'revisionId':revision_id,'sequence':prior+1}
        c.execute('INSERT INTO outbox VALUES(?,?,?,?,?,?)',(uid(),'RevisionSaved',2,chapter_id,canonical(payload),saved_at))
        audit(c,actor,'chapter.restore' if restored_from else 'chapter.save',chapter_id,{'revisionId':revision_id,'sequence':prior+1})
        return {'revisionId':revision_id,'chapterId':chapter_id,'sequence':prior+1,'savedAt':saved_at}

    def projects(self,actor: str) -> dict:
        with self.db.connect() as c:
            rows=c.execute('SELECT p.*,m.role,(SELECT COUNT(*) FROM chapters ch WHERE ch.project_id=p.id) chapterCount FROM projects p JOIN project_memberships m ON m.project_id=p.id WHERE m.user_id=? ORDER BY p.updated_at DESC,p.id',(actor,)).fetchall()
            return {'projects':[dict(r) for r in rows]}

    def create_project(self,actor: str,data: dict,key: str) -> dict:
        title=label(data.get('title'),'Project title');lang=language(data.get('language','en'));direction=data.get('direction','auto')
        if direction not in ('auto','ltr','rtl'):raise Problem(422,'DIRECTION','Choose a supported writing direction.')
        with self.db.transaction() as c:
            workspace=c.execute('SELECT * FROM workspaces WHERE owner_id=?',(actor,)).fetchone()
            if not workspace:raise Problem(403,'WORKSPACE','An authorized workspace is required.')
            replay=self._receipt(c,actor,'createProject',workspace['id'],key,data)
            if replay:return replay
            project_id,manuscript_id,chapter_id=uid(),uid(),uid();timestamp=now();version=uid()
            c.execute('INSERT INTO projects VALUES(?,?,?,?,?,?,?,?,?,?)',(project_id,workspace['id'],actor,title,lang,direction,version,1,timestamp,timestamp))
            c.execute('INSERT INTO project_memberships VALUES(?,?,?)',(project_id,actor,'owner'))
            c.execute('INSERT INTO manuscripts VALUES(?,?,2)',(manuscript_id,project_id))
            account=c.execute('SELECT locale FROM users WHERE id=?',(actor,)).fetchone()
            chapter_title=translate('Chapter {number}',account['locale'] or 'en',{'number':1})
            c.execute('INSERT INTO chapters VALUES(?,?,?,?,NULL)',(chapter_id,project_id,chapter_title,0))
            rev=self._revision(c,actor,project_id,chapter_id,empty_ast(lang,direction))
            audit(c,actor,'project.create',project_id)
            return self._record(c,actor,'createProject',workspace['id'],key,data,{'id':project_id,'title':title,'version':version,'chapterId':chapter_id,**rev})

    def project(self,actor,project_id):
        with self.db.connect() as c:
            project=dict(self.authorize(c,actor,project_id))
            project['manuscriptId']=c.execute('SELECT id FROM manuscripts WHERE project_id=?',(project_id,)).fetchone()[0]
            project['chapters']=[dict(r) for r in c.execute('SELECT id,title,position,current_revision_id revisionId FROM chapters WHERE project_id=? ORDER BY position,id',(project_id,))]
            return project

    def chapter(self,actor,chapter_id,revision_id=None):
        with self.db.connect() as c:
            chapter=c.execute('SELECT * FROM chapters WHERE id=?',(chapter_id,)).fetchone()
            if not chapter:raise Problem(404,'NOT_FOUND','Chapter unavailable.')
            project=self.authorize(c,actor,chapter['project_id'])
            revision=c.execute('SELECT * FROM chapter_revisions WHERE id=? AND chapter_id=?',(revision_id or chapter['current_revision_id'],chapter_id)).fetchone()
            if not revision:raise Problem(404,'NOT_FOUND','Revision unavailable.')
            return {'id':chapter_id,'title':chapter['title'],'projectId':project['id'],'revisionId':revision['id'],
                    'sequence':revision['sequence'],'savedAt':revision['created_at'],'accessEpoch':project['access_epoch'],
                    'ast':json.loads(revision['ast_json']),'role':project['role']}

    def add_chapter(self,actor,project_id,data,key,expected):
        title=label(data.get('title'),'Chapter title',150)
        with self.db.transaction() as c:
            p=self.authorize(c,actor,project_id,edit=True);request={**data,'expected':expected}
            replay=self._receipt(c,actor,'addChapter',project_id,key,request)
            if replay:return replay
            self._match(expected,p['version']);chapter_id=uid()
            position=c.execute('SELECT COALESCE(MAX(position),-1)+1 FROM chapters WHERE project_id=?',(project_id,)).fetchone()[0]
            c.execute('INSERT INTO chapters VALUES(?,?,?,?,NULL)',(chapter_id,project_id,title,position))
            result=self._revision(c,actor,project_id,chapter_id,empty_ast(p['language'],p['direction']));version=uid()
            c.execute('UPDATE projects SET version=? WHERE id=?',(version,project_id))
            return self._record(c,actor,'addChapter',project_id,key,request,{**result,'version':version,'id':chapter_id})

    def reorder(self,actor,project_id,data,key,expected):
        ids=data.get('chapterIds')
        with self.db.transaction() as c:
            p=self.authorize(c,actor,project_id,edit=True);request={**data,'expected':expected}
            replay=self._receipt(c,actor,'reorder',project_id,key,request)
            if replay:return replay
            self._match(expected,p['version'])
            current={r[0] for r in c.execute('SELECT id FROM chapters WHERE project_id=?',(project_id,))}
            if not isinstance(ids,list) or not all(isinstance(x,str) for x in ids) or len(ids)!=len(current) or set(ids)!=current:
                raise Problem(422,'CHAPTER_ORDER','Provide every project chapter exactly once.')
            for i,chapter_id in enumerate(ids):c.execute('UPDATE chapters SET position=? WHERE id=?',(i,chapter_id))
            version=uid();c.execute('UPDATE projects SET version=?,updated_at=? WHERE id=?',(version,now(),project_id));audit(c,actor,'chapter.reorder',project_id)
            return self._record(c,actor,'reorder',project_id,key,request,{'version':version})

    def save(self,actor,chapter_id,data,key,expected,restore=False):
        if not restore:validate_ast(data.get('ast'))
        with self.db.transaction() as c:
            ch=c.execute('SELECT * FROM chapters WHERE id=?',(chapter_id,)).fetchone()
            if not ch:raise Problem(404,'NOT_FOUND','Chapter unavailable.')
            project=self.authorize(c,actor,ch['project_id'],edit=True);request={**data,'expected':expected};op='restoreRevision' if restore else 'saveChapter'
            replay=self._receipt(c,actor,op,chapter_id,key,request)
            if replay:return replay
            self._match(expected,ch['current_revision_id'])
            if restore:
                if not isinstance(data.get('snapshotRevisionId'),str):raise Problem(404,'NOT_FOUND','Snapshot unavailable.')
                prior=c.execute('SELECT * FROM chapter_revisions WHERE id=? AND chapter_id=?',(data.get('snapshotRevisionId'),chapter_id)).fetchone()
                if not prior:raise Problem(404,'NOT_FOUND','Snapshot unavailable.')
                ast=json.loads(prior['ast_json'])
            else:
                if type(data.get('accessEpoch')) is not int or data['accessEpoch']!=project['access_epoch']:
                    raise Problem(409,'ACCESS_CHANGED','Project permissions changed. Reload access before saving; keep a recovery copy.')
                ast=data['ast']
            result=self._revision(c,actor,ch['project_id'],chapter_id,ast,data.get('snapshotRevisionId') if restore else None)
            return self._record(c,actor,op,chapter_id,key,request,result)

    def history(self,actor,chapter_id):
        with self.db.connect() as c:
            ch=c.execute('SELECT * FROM chapters WHERE id=?',(chapter_id,)).fetchone()
            if not ch:raise Problem(404,'NOT_FOUND','Chapter unavailable.')
            self.authorize(c,actor,ch['project_id'])
            return {'revisions':[dict(r) for r in c.execute('SELECT r.id,r.sequence,r.created_at createdAt,r.restored_from restoredFrom,u.name actorName FROM chapter_revisions r JOIN users u ON u.id=r.actor_id WHERE r.chapter_id=? ORDER BY r.sequence DESC LIMIT 100',(chapter_id,))]}

    def members(self,actor,project_id):
        with self.db.connect() as c:
            self.authorize(c,actor,project_id,owner=True)
            return {'members':[dict(r) for r in c.execute('SELECT u.id,u.name,u.email,m.role FROM project_memberships m JOIN users u ON u.id=m.user_id WHERE m.project_id=? ORDER BY m.role,u.name',(project_id,))]}

    def grant(self,actor,project_id,data,key):
        if data.get('role') not in ('editor','viewer','revoke'):raise Problem(422,'ROLE','Choose editor or viewer access.')
        with self.db.transaction() as c:
            p=self.authorize(c,actor,project_id,owner=True)
            replay=self._receipt(c,actor,'grantMembership',project_id,key,data)
            if replay:return replay
            target=c.execute('SELECT * FROM users WHERE email=? AND verified=1',(str(data.get('email','')).strip().casefold(),)).fetchone()
            if not target:raise Problem(422,'MEMBER_UNAVAILABLE','Ask this person to create and verify an account first.')
            if target['id']==p['owner_id']:raise Problem(422,'OWNER_ROLE','The project owner cannot be changed or revoked here.')
            if data['role']=='revoke':c.execute('DELETE FROM project_memberships WHERE project_id=? AND user_id=?',(project_id,target['id']))
            else:c.execute('INSERT INTO project_memberships VALUES(?,?,?) ON CONFLICT(project_id,user_id) DO UPDATE SET role=excluded.role',(project_id,target['id'],data['role']))
            c.execute('UPDATE projects SET access_epoch=access_epoch+1,version=? WHERE id=?',(uid(),project_id))
            audit(c,actor,'membership.'+data['role'],project_id,{'userId':target['id']})
            return self._record(c,actor,'grantMembership',project_id,key,data,{'state':'revoked' if data['role']=='revoke' else 'granted'})

    def _snapshot(self,c,actor,p):
        chapters=[]
        for ch in c.execute('SELECT ch.*,r.ast_json,r.sha256 FROM chapters ch JOIN chapter_revisions r ON r.id=ch.current_revision_id WHERE ch.project_id=? ORDER BY ch.position,ch.id',(p['id'],)):
            chapters.append({'id':ch['id'],'title':ch['title'],'revisionId':ch['current_revision_id'],'sha256':ch['sha256'],'ast':json.loads(ch['ast_json'])})
        manifest={'schemaVersion':2,'projectId':p['id'],'ownerId':p['owner_id'],'title':p['title'],'language':p['language'],'direction':p['direction'],'chapters':chapters,'converterVersion':'publisher-portable-2'}
        version_id=uid();manuscript=c.execute('SELECT id FROM manuscripts WHERE project_id=?',(p['id'],)).fetchone()[0]
        c.execute('INSERT INTO manuscript_versions VALUES(?,?,?,?,?,?)',(version_id,manuscript,canonical(manifest),digest(manifest),now(),actor))
        return version_id,manifest

    def export(self,actor,project_id,data,key):
        fmt=data.get('format')
        if fmt not in ('markdown','text','docx','html','bundle'):raise Problem(422,'FORMAT_UNAVAILABLE','Choose Markdown, text, DOCX, HTML or a portable project bundle. EPUB and print profiles are not yet available.')
        with self.db.transaction() as c:
            p=self.authorize(c,actor,project_id)
            replay=self._receipt(c,actor,'createExport',project_id,key,data)
            if replay:return replay
            version_id,manifest=self._snapshot(c,actor,p);job_id=uid()
            c.execute('INSERT INTO conversion_jobs VALUES(?,?,?,?,?,\'queued\',?,NULL,NULL,?)',(job_id,project_id,actor,version_id,fmt,digest({'source':digest(manifest),'format':fmt}),now()))
            audit(c,actor,'export.request',project_id,{'jobId':job_id,'sourceVersionId':version_id})
            return self._record(c,actor,'createExport',project_id,key,data,{'jobId':job_id,'state':'queued'})

    @staticmethod
    def _worker(operation: str,payload: dict) -> dict:
        root=Path(__file__).resolve().parents[1]
        # A regular file lets the child's RLIMIT_FSIZE bound stdout as well as
        # generated files. capture_output would first buffer unbounded output in
        # the API process before checking its size.
        with tempfile.TemporaryFile() as output:
            result=subprocess.run([sys.executable,'-m','publisher.worker',operation],input=canonical(payload).encode(),stdout=output,stderr=subprocess.DEVNULL,timeout=20,
                 env={'PYTHONPATH':str(root),'PATH':os.defpath,'LANG':'C.UTF-8'})
            output.seek(0);stdout=output.read(32*1024*1024+1)
        if len(stdout)>32*1024*1024:raise Problem(422,'EXPORT_LIMIT','The generated output exceeds the local limit.')
        if result.returncode!=0:
            try:error=json.loads(stdout).get('error',{})
            except (ValueError,AttributeError):error={}
            if isinstance(error,dict) and error.get('status') in (400,413,422) and isinstance(error.get('messageKey'),str):
                raise Problem(error['status'],str(error.get('code','CONVERSION_FAILED')),str(error.get('detail','Conversion failed.')),error['messageKey'],error.get('messageParams') if isinstance(error.get('messageParams'),dict) else {})
            raise Problem(422,'CONVERSION_FAILED','Conversion failed safely. Your manuscript and previous exports are unchanged.')
        return json.loads(stdout)

    def process_job(self,job_id):
        try:
            with self.db.transaction() as c:
                job=c.execute('SELECT * FROM conversion_jobs WHERE id=?',(job_id,)).fetchone()
                if not job or job['state']!='queued':return
                self.authorize(c,job['actor_id'],job['project_id'])
                source=c.execute('SELECT manifest_json FROM manuscript_versions WHERE id=?',(job['source_version_id'],)).fetchone()[0]
                c.execute("UPDATE conversion_jobs SET state='running' WHERE id=?",(job_id,))
                actor,project_id,fmt=job['actor_id'],job['project_id'],job['format']
            result=self._worker('export',{'manifest':json.loads(source),'format':fmt})
            content=base64.b64decode(result['content'],validate=True)
            if hashlib.sha256(content).hexdigest()!=result['sha256']:raise ValueError('Artifact checksum mismatch')
            with self.db.transaction() as c:
                self.authorize(c,actor,project_id)
                if c.execute("UPDATE conversion_jobs SET state='validating' WHERE id=? AND state='running'",(job_id,)).rowcount!=1:return
                artifact_id=uid();filename='manuscript-'+project_id[:8]+'.'+result['extension']
                c.execute('INSERT INTO export_artifacts VALUES(?,?,?,?,?,?,?,?)',(artifact_id,project_id,job_id,result['mediaType'],filename,content,result['sha256'],now()))
                c.execute("UPDATE conversion_jobs SET state='succeeded',artifact_id=? WHERE id=?",(artifact_id,job_id));audit(c,actor,'export.complete',project_id,{'jobId':job_id,'artifactId':artifact_id})
        except (Problem,ValueError,TypeError,AttributeError,OSError,subprocess.SubprocessError,sqlite3.Error,KeyError):
            with self.db.transaction() as c:c.execute("UPDATE conversion_jobs SET state='failed',error_code='CONVERSION_FAILED' WHERE id=? AND state!='succeeded'",(job_id,))

    def job(self,actor,job_id):
        with self.db.connect() as c:
            job=c.execute('SELECT * FROM conversion_jobs WHERE id=?',(job_id,)).fetchone()
            if not job:raise Problem(404,'NOT_FOUND','Export unavailable.')
            self.authorize(c,actor,job['project_id'])
            return {'jobId':job_id,'state':job['state'],'artifactId':job['artifact_id'],'errorCode':job['error_code'],'sourceVersionId':job['source_version_id']}

    def artifact(self,actor,artifact_id):
        with self.db.connect() as c:
            artifact=c.execute('SELECT * FROM export_artifacts WHERE id=?',(artifact_id,)).fetchone()
            if not artifact:raise Problem(404,'NOT_FOUND','Export unavailable.')
            self.authorize(c,actor,artifact['project_id'])
            return dict(artifact)

    def import_preview(self,actor,project_id,data,key):
        filename=label(data.get('filename'),'Filename',150)
        try:original=base64.b64decode(data.get('content',''),validate=True)
        except (ValueError,TypeError):raise Problem(422,'IMPORT_ENCODING','Invalid file encoding.') from None
        if len(original)>5*1024*1024:raise Problem(422,'IMPORT_SIZE','Choose a file up to 5 MiB.')
        with self.db.connect() as c:
            p=self.authorize(c,actor,project_id,edit=True);lang,direction=p['language'],p['direction']
        converted=self._worker('import',{'filename':filename,'content':base64.b64encode(original).decode(),'language':lang,'direction':direction})
        report={'warnings':converted['warnings'],'ast':converted['ast']};report_hash=digest(report)
        with self.db.transaction() as c:
            self.authorize(c,actor,project_id,edit=True)
            replay=self._receipt(c,actor,'importPreview',project_id,key,data)
            if replay:return replay
            ident=uid();c.execute('INSERT INTO import_previews VALUES(?,?,?,?,?,?,?,?,NULL,?)',(ident,project_id,actor,filename,original,canonical(converted['ast']),canonical(converted['warnings']),report_hash,now()))
            audit(c,actor,'import.preview',project_id,{'previewId':ident})
            return self._record(c,actor,'importPreview',project_id,key,data,{'id':ident,'reportHash':report_hash,'warnings':converted['warnings'],'textPreview':plain_text(converted['ast']['content'])[:4000]})

    def confirm_import(self,actor,project_id,preview_id,data,key,expected):
        with self.db.transaction() as c:
            p=self.authorize(c,actor,project_id,edit=True);request={**data,'previewId':preview_id,'expected':expected}
            replay=self._receipt(c,actor,'confirmImport',project_id,key,request)
            if replay:return replay
            preview=c.execute('SELECT * FROM import_previews WHERE id=? AND project_id=? AND actor_id=?',(preview_id,project_id,actor)).fetchone()
            if not preview:raise Problem(404,'NOT_FOUND','Import preview unavailable.')
            self._match(expected,p['version'])
            warnings=json.loads(preview['warnings_json'])
            if data.get('reportHash')!=preview['report_hash'] or data.get('acknowledgedWarningIds')!=[w['id'] for w in warnings]:
                raise Problem(422,'IMPORT_REVIEW','Review and acknowledge every transformation warning before importing.')
            if preview['confirmed_chapter_id']:raise Problem(409,'IMPORT_CONFIRMED','This preview has already been imported.')
            ch=uid();position=c.execute('SELECT COALESCE(MAX(position),-1)+1 FROM chapters WHERE project_id=?',(project_id,)).fetchone()[0]
            title=preview['filename'].rsplit('.',1)[0].strip() or preview['filename']
            c.execute('INSERT INTO chapters VALUES(?,?,?,?,NULL)',(ch,project_id,title,position))
            result=self._revision(c,actor,project_id,ch,json.loads(preview['ast_json']));version=uid()
            c.execute('UPDATE projects SET version=? WHERE id=?',(version,project_id));c.execute('UPDATE import_previews SET confirmed_chapter_id=? WHERE id=?',(ch,preview_id))
            audit(c,actor,'import.confirm',project_id,{'previewId':preview_id})
            return self._record(c,actor,'confirmImport',project_id,key,request,{**result,'version':version,'id':ch})

    def original_import(self,actor,project_id,preview_id):
        with self.db.connect() as c:
            self.authorize(c,actor,project_id)
            row=c.execute('SELECT filename,original FROM import_previews WHERE project_id=? AND id=?',(project_id,preview_id)).fetchone()
            if not row:raise Problem(404,'NOT_FOUND','Original source unavailable.')
            return dict(row)
