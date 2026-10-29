"""Persistent domain, API, adversarial and conversion tests using synthetic private content."""
import base64
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
from pathlib import Path
import sqlite3
import sys
import subprocess
import tempfile
from threading import Event
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs,urlparse
import zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'apps/api'))
from publisher.database import Database,ClosingConnection
from publisher.domain import Problem,empty_ast,validate_ast,uid,digest,plain_text
from publisher.formats import parse_import,export_document,W
from publisher.identity import Identity,password_hash,password_matches
from publisher.http import Application
from publisher.studio import Studio

PASSWORD='synthetic-long-test-password'

class AppTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.app=Application(self.root,self.root/'web',start_jobs=False)
        self.auth,self.studio=self.app.identity,self.app.studio
        self.user,self.token=self.account('author@example.test')
        self.other,self.other_token=self.account('other@example.test')
        self.project=self.studio.create_project(self.user['id'],{'title':'Private canary','language':'en'},uid())
        self.chapter=self.studio.chapter(self.user['id'],self.project['chapterId'])
    def tearDown(self):self.temp.cleanup()
    def account(self,email):
        self.auth.register({'email':email,'name':email.split('@')[0],'password':PASSWORD})
        mails=[json.loads(p.read_text()) for p in (self.root/'mail').glob('*.json')]
        message=next(m for m in mails if m['to']==email and m['subject']=='Verify your account')
        token=parse_qs(urlparse(message['url']).query)['token'][0];self.auth.verify(token)
        return self.auth.login({'email':email,'password':PASSWORD})
    def ast(self,text='A private manuscript. العربية فارسی 日本語 e\u0301 🖋️'):
        ast=empty_ast();ast['content']['content'][0]['content']=[{'type':'text','text':text}];return ast
    def save(self,ast=None,key=None,expected=None,actor=None):
        return self.studio.save(actor or self.user['id'],self.chapter['id'],{'ast':ast or self.ast(),'accessEpoch':self.studio.project(self.user['id'],self.project['id'])['access_epoch']},key or uid(),expected or self.chapter['revisionId'])
    def invoke(self,path,method='GET',body=None,token=None,csrf=True,origin=True,extra=None):
        raw=json.dumps(body or {}).encode();environ={'REQUEST_METHOD':method,'PATH_INFO':path,'wsgi.input':BytesIO(raw),'CONTENT_LENGTH':str(len(raw)),'CONTENT_TYPE':'application/json','REMOTE_ADDR':'synthetic-test'}
        if origin:environ['HTTP_ORIGIN']='http://127.0.0.1:8000'
        if token:
            environ['HTTP_COOKIE']='publisher_session='+token
            if csrf:environ['HTTP_X_CSRF_TOKEN']=self.auth.csrf(token)
        environ.update(extra or {});result={}
        def start(status,headers):result.update(status=int(status.split()[0]),headers=dict(headers))
        payload=b''.join(self.app(environ,start));result['body']=json.loads(payload) if result['headers'].get('Content-Type','').startswith(('application/json','application/problem')) else payload
        return result
    def test_registration_verification_is_single_use_and_required(self):
        self.auth.register({'email':'unverified@example.test','name':'Synthetic','password':PASSWORD})
        with self.assertRaises(Problem) as e:self.auth.login({'email':'unverified@example.test','password':PASSWORD})
        self.assertEqual(e.exception.status,401)
        mail=next(json.loads(p.read_text()) for p in (self.root/'mail').glob('*.json') if json.loads(p.read_text())['to']=='unverified@example.test')
        token=parse_qs(urlparse(mail['url']).query)['token'][0]
        self.auth.verify(token)
        with self.assertRaises(Problem):self.auth.verify(token)
        self.assertTrue(self.auth.login({'email':'unverified@example.test','password':PASSWORD})[1])
    def test_recovery_invalidates_sessions_and_consumes_token(self):
        self.auth.recover(self.user['email'])
        mail=next(json.loads(p.read_text()) for p in (self.root/'mail').glob('*.json') if json.loads(p.read_text())['subject']=='Reset your password')
        token=parse_qs(urlparse(mail['url']).query)['token'][0]
        self.auth.verify(token,'another-synthetic-password','recover')
        with self.assertRaises(Problem):self.auth.authenticate(self.token)
        with self.assertRaises(Problem):self.auth.verify(token,'third-synthetic-password','recover')
    def test_login_does_not_lock_other_writes_or_reuse_credentials_after_reset(self):
        replacement=password_hash('replacement-synthetic-password')
        def reset_during_verification(password,stored):
            correct=password_matches(password,stored)
            # A separate writer must be able to complete during slow scrypt.
            with sqlite3.connect(self.app.db.path,timeout=.1,factory=ClosingConnection) as c:
                c.execute('UPDATE users SET password_hash=? WHERE id=?',(replacement,self.user['id']))
                c.execute('DELETE FROM sessions WHERE user_id=?',(self.user['id'],))
            return correct
        with patch('publisher.identity.password_matches',side_effect=reset_during_verification):
            with self.assertRaises(Problem) as error:self.auth.login({'email':self.user['email'],'password':PASSWORD})
        self.assertEqual(error.exception.code,'LOGIN_FAILED')
        with self.app.db.connect() as c:self.assertEqual(c.execute('SELECT COUNT(*) FROM sessions WHERE user_id=?',(self.user['id'],)).fetchone()[0],0)
    def test_concurrent_initializers_observe_only_complete_session_keys(self):
        import secrets
        data_dir=self.root/'key-race';data_dir.mkdir()
        blocked=Event();release=Event();original=secrets.token_bytes
        def pause_first_key(size):
            if size==32 and not blocked.is_set():blocked.set();release.wait(5)
            return original(size)
        with patch('publisher.identity.secrets.token_bytes',side_effect=pause_first_key):
            with ThreadPoolExecutor(max_workers=1) as pool:
                first=pool.submit(Identity,self.app.db,data_dir,'http://127.0.0.1:8000')
                self.assertTrue(blocked.wait(3))
                try:second=Identity(self.app.db,data_dir,'http://127.0.0.1:8000')
                finally:release.set()
                self.assertEqual(first.result().key,second.key)
        self.assertEqual(len(second.key),32);self.assertEqual((data_dir/'session.key').stat().st_mode&0o777,0o600)
        self.assertEqual(list(data_dir.glob('.session-key-*')),[])
    def test_real_http_login_cookie_and_no_credential_storage(self):
        response=self.invoke('/api/auth/login','POST',{'email':self.user['email'],'password':PASSWORD})
        self.assertEqual(response['status'],200);self.assertIn('HttpOnly',response['headers']['Set-Cookie']);self.assertIn('SameSite=Strict',response['headers']['Set-Cookie'])
        with self.app.db.connect() as c:
            self.assertNotIn(PASSWORD,c.execute('SELECT password_hash FROM users LIMIT 1').fetchone()[0])
            self.assertIsNone(c.execute('SELECT 1 FROM sessions WHERE token_hash=?',(self.token,)).fetchone())
    def test_csrf_origin_and_anonymous_access(self):
        path='/api/v1/projects'
        self.assertEqual(self.invoke(path)['status'],401)
        self.assertEqual(self.invoke(path,'POST',{'title':'bad'},self.token,csrf=False)['status'],403)
        self.assertEqual(self.invoke(path,'POST',{'title':'bad'},self.token,origin=False)['status'],403)
        self.assertEqual(self.invoke(path,'POST',{'title':'Safe'},self.token,extra={'HTTP_IDEMPOTENCY_KEY':uid()})['status'],201)
        self.assertEqual(self.invoke(path,'POST',{'title':'Bad token'},self.token,extra={'HTTP_X_CSRF_TOKEN':'غير صالح'})['status'],403)
    def test_cross_tenant_denials_and_public_privacy(self):
        p=self.project['id'];ch=self.chapter['id']
        for path in [f'/api/v1/projects/{p}',f'/api/v1/chapters/{ch}',f'/api/v1/chapters/{ch}/history']:
            self.assertEqual(self.invoke(path,token=self.other_token)['status'],404)
        self.assertEqual(self.invoke('/api/v1/projects',token=self.other_token)['body']['projects'],[])
        self.assertEqual(self.invoke('/api/v1/catalog')['status'],401)
    def test_creation_receipt_and_key_collision(self):
        key=uid();data={'title':'One project','language':'en'}
        first=self.studio.create_project(self.user['id'],data,key)
        self.assertEqual(first,self.studio.create_project(self.user['id'],data,key))
        with self.assertRaises(Problem) as e:self.studio.create_project(self.user['id'],{'title':'Different'},key)
        self.assertEqual(e.exception.status,409)
    def test_save_http_etag_and_reload(self):
        expected_ast=self.ast()
        response=self.invoke('/api/v1/chapters/'+self.chapter['id'],'PUT',{'ast':expected_ast,'accessEpoch':1},self.token,extra={'HTTP_IDEMPOTENCY_KEY':uid(),'HTTP_IF_MATCH':'"'+self.chapter['revisionId']+'"'})
        self.assertEqual(response['status'],200);revision=response['body']['revisionId'];self.assertEqual(response['headers']['ETag'],'"'+revision+'"')
        fresh=Application(self.root,self.root/'web',start_jobs=False)
        self.assertEqual(fresh.studio.chapter(self.user['id'],self.chapter['id'])['ast'],expected_ast)
    def ast_same_ids(self,revision):
        with self.app.db.connect() as c:return json.loads(c.execute('SELECT ast_json FROM chapter_revisions WHERE id=?',(revision,)).fetchone()[0])
    def test_lost_response_replays_original_even_after_later_commit(self):
        ast=self.ast();data={'ast':ast,'accessEpoch':1};key=uid()
        first=self.studio.save(self.user['id'],self.chapter['id'],data,key,self.chapter['revisionId'])
        second=self.studio.save(self.user['id'],self.chapter['id'],{'ast':self.ast('Later'),'accessEpoch':1},uid(),first['revisionId'])
        self.assertEqual(first,self.studio.save(self.user['id'],self.chapter['id'],data,key,self.chapter['revisionId']))
        self.assertEqual(self.studio.chapter(self.user['id'],self.chapter['id'])['revisionId'],second['revisionId'])
    def test_concurrent_stale_save_has_one_winner(self):
        def attempt(i):
            try:return self.save(self.ast('Concurrent '+str(i)))['sequence']
            except Problem as e:return e.status
        with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(attempt,[1,2]))
        self.assertEqual(sorted(results),[2,412]);self.assertEqual(len(self.studio.history(self.user['id'],self.chapter['id'])['revisions']),2)
    def test_viewer_no_write_non_owner_no_grant_and_revocation_before_replay(self):
        owner=self.user['id'];other=self.other['id'];p=self.project['id']
        self.studio.grant(owner,p,{'email':self.other['email'],'role':'viewer'},uid())
        with self.assertRaises(Problem) as e:self.save(actor=other)
        self.assertEqual(e.exception.status,403)
        with self.assertRaises(Problem):self.studio.grant(other,p,{'email':self.user['email'],'role':'editor'},uid())
        self.studio.grant(owner,p,{'email':self.other['email'],'role':'editor'},uid());epoch=self.studio.project(owner,p)['access_epoch'];key=uid();data={'ast':self.ast(),'accessEpoch':epoch}
        self.studio.save(other,self.chapter['id'],data,key,self.chapter['revisionId'])
        self.studio.grant(owner,p,{'email':self.other['email'],'role':'revoke'},uid())
        with self.assertRaises(Problem) as e:self.studio.save(other,self.chapter['id'],data,key,self.chapter['revisionId'])
        self.assertEqual(e.exception.status,404)
    def test_restore_creates_new_revision_and_history_is_immutable(self):
        saved=self.save();restored=self.studio.save(self.user['id'],self.chapter['id'],{'snapshotRevisionId':self.chapter['revisionId']},uid(),saved['revisionId'],True)
        self.assertEqual(restored['sequence'],3);self.assertNotEqual(restored['revisionId'],self.chapter['revisionId'])
        self.assertEqual(self.studio.chapter(self.user['id'],self.chapter['id'])['ast'],self.chapter['ast'])
        with self.app.db.transaction() as c:
            with self.assertRaises(sqlite3.IntegrityError):c.execute('UPDATE chapter_revisions SET ast_json=\'{}\' WHERE id=?',(saved['revisionId'],))
    def test_reorder_exact_members_and_stale_version(self):
        new=self.studio.add_chapter(self.user['id'],self.project['id'],{'title':'Second'},uid(),self.project['version'])
        with self.assertRaises(Problem) as e:self.studio.reorder(self.user['id'],self.project['id'],{'chapterIds':[new['id'],self.chapter['id']]},uid(),self.project['version'])
        self.assertEqual(e.exception.status,412)
        self.studio.reorder(self.user['id'],self.project['id'],{'chapterIds':[new['id'],self.chapter['id']]},uid(),new['version'])
        self.assertEqual(self.studio.project(self.user['id'],self.project['id'])['chapters'][0]['id'],new['id'])
    def test_untrusted_ast_and_duplicate_ids_fail_without_mutation(self):
        bad=self.ast();bad['content']['content'][0]['content'][0]['marks']=[{'type':'link','attrs':{'href':'javascript:alert(1)'}}]
        with self.assertRaises(Problem):self.save(bad)
        duplicate=self.ast();duplicate['content']['content']*=2
        with self.assertRaises(Problem):self.save(duplicate)
        self.assertEqual(len(self.studio.history(self.user['id'],self.chapter['id'])['revisions']),1)
    def test_100000_words_unicode_roundtrip(self):
        ast=self.ast(('word فارسی 日本語 e\u0301 🖋️ '*20000).strip());saved=self.save(ast)
        self.assertEqual(digest(self.studio.chapter(self.user['id'],self.chapter['id'])['ast']),digest(ast));self.assertEqual(saved['sequence'],2)
    def test_private_export_portability_reproducible_docx_and_html_safe(self):
        self.save(self.ast('PRIVATE_CANARY <script>alert(1)</script>'))
        outputs=[]
        for i in range(2):
            job=self.studio.export(self.user['id'],self.project['id'],{'format':'docx'},uid());self.studio.process_job(job['jobId']);status=self.studio.job(self.user['id'],job['jobId']);self.assertEqual(status['state'],'succeeded');artifact=self.studio.artifact(self.user['id'],status['artifactId']);outputs.append(artifact['content'])
        self.assertEqual(outputs[0],outputs[1])
        with zipfile.ZipFile(BytesIO(outputs[0])) as z:self.assertIn(b'PRIVATE_CANARY',z.read('word/document.xml'))
        with self.assertRaises(Problem):self.studio.artifact(self.other['id'],status['artifactId'])
        manifest={'title':'Test','language':'en','chapters':[{'title':'Chapter','ast':self.ast('<script>bad()</script>')}]}
        html=export_document(manifest,'html')[0];self.assertNotIn(b'<script>',html);self.assertIn(b'&lt;script&gt;',html)
    def test_docx_preserves_manuscript_languages_bidi_and_deterministic_bytes(self):
        cases=[('ar','rtl','عنوان','مرحبا بالعالم'),('fa','rtl','عنوان فارسی','سلام دنیا'),('ur','rtl','عنوان اردو','دنیا کو سلام'),('hi','ltr','शीर्षक','नमस्ते दुनिया'),('bn','ltr','শিরোনাম','ওহে বিশ্ব'),('zh','ltr','章节','你好世界')]
        chapters=[]
        for language,direction,title,text in cases:
            ast=empty_ast(language,'auto')
            ast['content']['content']=[{'type':'paragraph','attrs':{'id':uid()},'content':[{'type':'text','text':value}]} for value in (text,'123','English first فارسی')]
            chapters.append({'title':title,'ast':ast})
        manifest={'title':'مشروع','language':'ar','direction':'rtl','chapters':chapters};before=digest(manifest)
        first=export_document(manifest,'docx')[0];self.assertEqual(first,export_document(manifest,'docx')[0]);self.assertEqual(digest(manifest),before)
        with zipfile.ZipFile(BytesIO(first)) as archive:document=ET.fromstring(archive.read('word/document.xml'))
        paragraphs=list(document.iter(f'{{{W}}}p'))
        for i,(language,direction,title,text) in enumerate(cases):
            for offset in (1,2,3):
                p=paragraphs[i*4+offset]
                self.assertEqual(p.find(f'{{{W}}}pPr/{{{W}}}bidi').get(f'{{{W}}}val'),'1' if direction=='rtl' and offset!=3 else '0')
                self.assertEqual(p.find(f'{{{W}}}pPr/{{{W}}}rPr/{{{W}}}lang').get(f'{{{W}}}val'),language)
                for lang in p.iter(f'{{{W}}}lang'):
                    self.assertEqual(set(lang.attrib.values()),{language})
            self.assertEqual(''.join(t.text or '' for t in paragraphs[i*4+1].iter(f'{{{W}}}t')),text)
        self.assertIn(b'<html lang="ar" dir="rtl">',export_document(manifest,'html')[0])
    def test_docx_breaks_tabs_optional_marks_and_ordered_list_fidelity(self):
        xml=f'<w:document xmlns:w="{W}"><w:body><w:p><w:r><w:rPr><w:b w:val="false"/><w:i w:val="off"/><w:strike w:val="0"/></w:rPr><w:t>A</w:t><w:tab/><w:t>B</w:t><w:br/><w:t>C</w:t><w:cr/><w:t>D</w:t><w:noBreakHyphen/><w:t>E</w:t><w:softHyphen/><w:t>F</w:t></w:r><w:r><w:rPr><w:b/></w:rPr><w:t>Z</w:t></w:r></w:p></w:body></w:document>'
        original=BytesIO()
        with zipfile.ZipFile(original,'w') as archive:
            archive.writestr('[Content_Types].xml','x');archive.writestr('word/document.xml',xml)
        imported,_=parse_import('format.docx',original.getvalue(),'fa','rtl')
        self.assertEqual(plain_text(imported['content']),'A\tB\nC\nD\u2011E\u00adFZ')
        content=imported['content']['content'][0]['content']
        self.assertTrue(all('marks' not in n for n in content[:-1]));self.assertEqual(content[-1]['marks'],[{'type':'bold'}])
        def paragraph(text):return {'type':'paragraph','attrs':{'id':uid()},'content':[{'type':'text','text':text}]}
        def item(nodes):return {'type':'listItem','attrs':{'id':uid()},'content':nodes}
        imported['content']['content'] += [
            {'type':'orderedList','attrs':{'id':uid(),'start':7,'type':'I'},'content':[item([paragraph('first'),paragraph('continued'),{'type':'bulletList','attrs':{'id':uid()},'content':[item([paragraph('nested')])]}])]},
            {'type':'orderedList','attrs':{'id':uid(),'start':3,'type':'a'},'content':[item([paragraph('second')])]}
        ]
        exported=export_document({'title':'Source','language':'fa','chapters':[{'title':'Chapter','ast':imported}]},'docx')[0]
        with zipfile.ZipFile(BytesIO(exported)) as archive:
            document=ET.fromstring(archive.read('word/document.xml'));numbering=ET.fromstring(archive.read('word/numbering.xml'))
        self.assertEqual(len(list(document.iter(f'{{{W}}}tab'))),1);self.assertEqual(len(list(document.iter(f'{{{W}}}br'))),2)
        self.assertEqual([n.get(f'{{{W}}}val') for n in numbering.iter(f'{{{W}}}start')],['7','1','3'])
        self.assertEqual([n.get(f'{{{W}}}val') for n in numbering.iter(f'{{{W}}}numFmt')],['upperRoman','bullet','lowerLetter'])
        continuation=next(p for p in document.iter(f'{{{W}}}p') if ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))=='continued')
        self.assertIsNone(continuation.find(f'{{{W}}}pPr/{{{W}}}numPr'))
    def test_invalid_xml_source_is_retained_and_never_exported_as_a_broken_docx(self):
        ast=self.ast('Preserved\x01source');validate_ast(ast)
        manifest={'title':'Source','language':'en','chapters':[{'title':'Chapter','ast':ast}]};before=digest(manifest)
        with self.assertRaises(Problem) as error:export_document(manifest,'docx')
        self.assertEqual(error.exception.code,'CONVERSION_FAILED');self.assertEqual(digest(manifest),before)
        self.assertIn(b'Preserved\x01source',export_document(manifest,'text')[0])
    def test_portable_bundle_preserves_complete_canonical_source_and_metadata(self):
        ast=self.ast('Portable original source فارسی');self.save(ast)
        job=self.studio.export(self.user['id'],self.project['id'],{'format':'bundle'},uid());self.studio.process_job(job['jobId'])
        artifact=self.studio.artifact(self.user['id'],self.studio.job(self.user['id'],job['jobId'])['artifactId'])
        with zipfile.ZipFile(BytesIO(artifact['content'])) as archive:
            source=json.loads(archive.read('manuscript.json'))
            self.assertEqual(source['ownerId'],self.user['id']);self.assertEqual(source['title'],'Private canary')
            self.assertEqual(source['chapters'][0]['ast'],ast);self.assertIn('manuscript.docx',archive.namelist())
    def test_failed_export_preserves_previous_artifact(self):
        job=self.studio.export(self.user['id'],self.project['id'],{'format':'text'},uid());self.studio.process_job(job['jobId']);good=self.studio.job(self.user['id'],job['jobId'])['artifactId']
        before=self.studio.artifact(self.user['id'],good)['sha256']
        broken=self.studio.export(self.user['id'],self.project['id'],{'format':'docx'},uid())
        self.studio._worker=lambda *_: (_ for _ in ()).throw(ValueError('synthetic failure'))
        self.studio.process_job(broken['jobId']);self.assertEqual(self.studio.job(self.user['id'],broken['jobId'])['state'],'failed')
        self.assertEqual(self.studio.artifact(self.user['id'],good)['sha256'],before)
    def test_export_reauthorizes_before_promotion(self):
        self.studio.grant(self.user['id'],self.project['id'],{'email':self.other['email'],'role':'viewer'},uid())
        job=self.studio.export(self.other['id'],self.project['id'],{'format':'text'},uid());original=self.studio._worker
        def revoke(*args):
            result=original(*args);self.studio.grant(self.user['id'],self.project['id'],{'email':self.other['email'],'role':'revoke'},uid());return result
        self.studio._worker=revoke;self.studio.process_job(job['jobId'])
        self.assertEqual(self.studio.job(self.user['id'],job['jobId'])['state'],'failed')
    def test_malformed_worker_output_and_interrupted_jobs_cannot_publish_artifacts(self):
        real=self.studio._worker
        for output in (None,{'content':None}):
            job=self.studio.export(self.user['id'],self.project['id'],{'format':'text'},uid())
            self.studio._worker=lambda *_,value=output:value
            self.studio.process_job(job['jobId'])
            self.assertEqual(self.studio.job(self.user['id'],job['jobId'])['state'],'failed')
        job=self.studio.export(self.user['id'],self.project['id'],{'format':'text'},uid())
        def interrupt(*args):
            result=real(*args)
            with self.app.db.transaction() as c:c.execute("UPDATE conversion_jobs SET state='failed',error_code='INTERRUPTED' WHERE id=?",(job['jobId'],))
            return result
        self.studio._worker=interrupt;self.studio.process_job(job['jobId'])
        status=self.studio.job(self.user['id'],job['jobId'])
        self.assertEqual(status['state'],'failed');self.assertEqual(status['errorCode'],'INTERRUPTED');self.assertIsNone(status['artifactId'])
    def test_import_review_is_explicit_idempotent_and_preserves_original(self):
        original='# Imported\n\nSome **literal** Markdown and فارسی.'
        preview=self.studio.import_preview(self.user['id'],self.project['id'],{'filename':'source.md','content':base64.b64encode(original.encode()).decode()},uid())
        self.assertTrue(preview['warnings']);self.assertEqual(len(self.studio.project(self.user['id'],self.project['id'])['chapters']),1)
        data={'reportHash':preview['reportHash'],'acknowledgedWarningIds':[]}
        with self.assertRaises(Problem):self.studio.confirm_import(self.user['id'],self.project['id'],preview['id'],data,uid(),self.project['version'])
        data['acknowledgedWarningIds']=[w['id'] for w in preview['warnings']];key=uid()
        first=self.studio.confirm_import(self.user['id'],self.project['id'],preview['id'],data,key,self.project['version'])
        self.assertEqual(first,self.studio.confirm_import(self.user['id'],self.project['id'],preview['id'],data,key,self.project['version']))
        self.assertEqual(self.studio.original_import(self.user['id'],self.project['id'],preview['id'])['original'],original.encode())
    def test_hidden_filename_import_keeps_a_nonempty_chapter_title(self):
        preview=self.studio.import_preview(self.user['id'],self.project['id'],{'filename':'.md','content':base64.b64encode(b'Source').decode()},uid())
        result=self.studio.confirm_import(self.user['id'],self.project['id'],preview['id'],{'reportHash':preview['reportHash'],'acknowledgedWarningIds':[w['id'] for w in preview['warnings']]},uid(),self.project['version'])
        self.assertEqual(self.studio.chapter(self.user['id'],result['id'])['title'],'.md')
    def test_import_rejects_path_traversal_active_xml_and_archive_bomb(self):
        for name,body in [('../escape',b'x'),('word/document.xml',b'<!DOCTYPE a [<!ENTITY x "bad">]><a>&x;</a>')]:
            f=BytesIO()
            with zipfile.ZipFile(f,'w') as z:z.writestr('[Content_Types].xml','x');z.writestr(name,body)
            with self.assertRaises(Problem):parse_import('evil.docx',f.getvalue(),'en','auto')
        f=BytesIO()
        with zipfile.ZipFile(f,'w',compression=zipfile.ZIP_DEFLATED) as z:z.writestr('[Content_Types].xml','x');z.writestr('word/document.xml',b'a'*200000)
        with self.assertRaises(Problem):parse_import('bomb.docx',f.getvalue(),'en','auto')
    def test_backup_restore_and_audit_do_not_leak_manuscript_text(self):
        canary='SECRET_CANARY_DO_NOT_LOG';saved=self.save(self.ast(canary));destination=self.root/'restore.sqlite';self.app.db.backup(destination)
        restored=Studio(Database(destination));self.assertEqual(restored.chapter(self.user['id'],self.chapter['id'])['revisionId'],saved['revisionId'])
        with self.app.db.connect() as c:
            self.assertEqual(c.execute('PRAGMA integrity_check').fetchone()[0],'ok');self.assertEqual(c.execute('PRAGMA foreign_key_check').fetchall(),[])
            for row in c.execute('SELECT metadata_json FROM audit_events'):self.assertNotIn(canary,row[0])
            for row in c.execute('SELECT payload_json FROM outbox'):self.assertNotIn(canary,row[0])
        with self.assertRaises(ValueError):self.app.db.backup(destination)
    def test_backup_failure_removes_partial_target_and_restored_database_stays_private(self):
        partial=self.root/'failed-backup.sqlite'
        with patch.object(self.app.db,'connect',side_effect=sqlite3.OperationalError('synthetic read failure')):
            with self.assertRaises(sqlite3.OperationalError):self.app.db.backup(partial)
        self.assertFalse(partial.exists())
        restored=self.root/'private.sqlite';self.app.db.backup(restored);restored.chmod(0o644)
        db=Database(restored)
        with db.transaction() as c:
            c.execute('UPDATE workspaces SET name=name')
            for suffix in ('','-wal','-shm'):
                path=Path(str(restored)+suffix)
                if path.exists():self.assertEqual(path.stat().st_mode&0o777,0o600)
    def test_static_traversal_security_headers_and_unknown_operations(self):
        response=self.invoke('/../../session.key');self.assertEqual(response['status'],404);self.assertIn('nosniff',response['headers']['X-Content-Type-Options']);self.assertEqual(response['headers']['Cache-Control'],'no-store')
        self.assertEqual(self.invoke('/api/v1/publish','POST',{},self.token)['status'],404)
    def test_export_unsupported_format_fails_closed(self):
        with self.assertRaises(Problem) as e:self.studio.export(self.user['id'],self.project['id'],{'format':'print-pdf'},uid())
        self.assertEqual(e.exception.status,422)
    def test_process_exit_after_acknowledgement_preserves_revision(self):
        script="""import sys,json,os
from pathlib import Path
from publisher.database import Database
from publisher.studio import Studio
result=Studio(Database(Path(sys.argv[1]))).save(sys.argv[2],sys.argv[3],json.loads(sys.stdin.read()),sys.argv[5],sys.argv[4])
print(json.dumps(result),flush=True)
os._exit(0)
"""
        ast=self.ast('ACK_SURVIVES_PROCESS_EXIT فارسی')
        import os
        result=subprocess.run([sys.executable,'-c',script,str(self.app.db.path),self.user['id'],self.chapter['id'],self.chapter['revisionId'],uid()],input=json.dumps({'ast':ast,'accessEpoch':1}),text=True,capture_output=True,env={**os.environ,'PYTHONPATH':str(Path('apps/api').resolve())},check=True)
        acknowledgement=json.loads(result.stdout)
        restarted=Studio(Database(self.app.db.path))
        self.assertEqual(restarted.chapter(self.user['id'],self.chapter['id'])['revisionId'],acknowledgement['revisionId'])
        self.assertEqual(restarted.chapter(self.user['id'],self.chapter['id'])['ast'],ast)
    def test_interrupted_job_is_failed_explicitly_after_restart(self):
        job=self.studio.export(self.user['id'],self.project['id'],{'format':'text'},uid())
        with self.app.db.transaction() as c:c.execute("UPDATE conversion_jobs SET state='running' WHERE id=?",(job['jobId'],))
        restarted=Application(self.root,self.root/'web',start_jobs=True)
        state=restarted.studio.job(self.user['id'],job['jobId'])
        self.assertEqual(state['state'],'failed');self.assertEqual(state['errorCode'],'INTERRUPTED')
        self.assertIsNone(state['artifactId'])
    def test_malformed_structures_and_unknown_fields_are_safe_validation_errors(self):
        malformed=self.ast();malformed['content']['content'][0]['type']=['invalid']
        with self.assertRaises(Problem) as e:validate_ast(malformed)
        self.assertEqual(e.exception.status,422)
        result=self.invoke('/api/v1/projects','POST',{'title':'No mass assignment','owner_id':self.other['id']},self.token,extra={'HTTP_IDEMPOTENCY_KEY':uid()})
        self.assertEqual(result['status'],422)
    def test_malformed_unicode_and_snapshot_types_fail_without_new_revisions(self):
        malformed=self.ast('\ud800')
        with self.assertRaises(Problem) as error:validate_ast(malformed)
        self.assertEqual(error.exception.code,'AST_TEXT')
        for data in ({'title':'bad\ud800'},{'title':'valid','language':'en','direction':{'bad\ud800':'auto'}}):
            self.assertEqual(self.invoke('/api/v1/projects','POST',data,self.token,extra={'HTTP_IDEMPOTENCY_KEY':uid()})['status'],400)
        result=self.invoke('/api/v1/chapters/'+self.chapter['id']+'/restores','POST',{'snapshotRevisionId':{}},self.token,extra={'HTTP_IDEMPOTENCY_KEY':uid(),'HTTP_IF_MATCH':'"'+self.chapter['revisionId']+'"'})
        self.assertEqual(result['status'],404);self.assertEqual(len(self.studio.history(self.user['id'],self.chapter['id'])['revisions']),1)
    def test_seed_is_repeatable_without_overwriting_existing_revisions(self):
        import os
        data_dir=self.root/'seed-data'
        env={**os.environ,'PUBLISHER_ENV':'test','PUBLISHER_DATA_DIR':str(data_dir),'PUBLISHER_SEED_PASSWORD':PASSWORD}
        for _ in range(2):
            result=subprocess.run([sys.executable,'scripts/seed.py'],env=env,text=True,capture_output=True,check=True)
            self.assertNotIn(PASSWORD,result.stdout)
        with Database(data_dir/'publisher.sqlite3').connect() as c:
            self.assertEqual(c.execute('SELECT COUNT(*) FROM projects').fetchone()[0],1)
            self.assertEqual(c.execute('SELECT COUNT(*) FROM chapter_revisions').fetchone()[0],2)
    def test_rate_limit_has_bounded_window(self):
        self.auth.rate_limit('test-bucket',1)
        with self.assertRaises(Problem) as e:self.auth.rate_limit('test-bucket',1)
        self.assertEqual(e.exception.status,429)

if __name__=='__main__':unittest.main()
