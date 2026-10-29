"""Multilingual catalogs, migration, preferences and UI/content privacy boundaries."""
from io import BytesIO
from pathlib import Path
import json
import re
import sqlite3
import sys
import tempfile
import unittest
from urllib.parse import parse_qs,urlparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'apps/api'))
from publisher.database import Database,now
from publisher.domain import canonical,digest,empty_ast,uid
from publisher.http import Application
from publisher.identity import password_hash
from publisher.localization import LANGUAGES,SUPPORTED,catalog,negotiate_locale,resolve_locale,translate,localize_system_message

ROOT=Path(__file__).resolve().parents[1]
PASSWORD='synthetic-localization-password'

class CatalogTests(unittest.TestCase):
    def test_top_fourteen_and_persian_have_complete_nonempty_catalogs(self):
        self.assertEqual(SUPPORTED,{'en','zh','hi','es','ar','fr','bn','pt','id','ur','ru','de','ja','pcm','fa'})
        base=catalog('en')
        for language in LANGUAGES:
            with self.subTest(locale=language['code']):
                translated=catalog(language['code']);self.assertEqual(set(translated),set(base))
                self.assertTrue(all(isinstance(v,str) and v.strip() for v in translated.values()))
                for key,value in translated.items():
                    source_params=set(re.findall(r'\{([A-Za-z]\w*)\}',base[key]));params=set(re.findall(r'\{([A-Za-z]\w*)\}',value))
                    if key.startswith('chapterCount.'):
                        self.assertTrue(params<=source_params)
                    else:self.assertEqual(params,source_params,key)
                if language['code'] not in ('en','pcm'):
                    self.assertNotEqual(translated['Your manuscripts'],base['Your manuscripts'])
    def test_regional_negotiation_quality_and_invalid_input(self):
        self.assertEqual(negotiate_locale('es-MX;q=0.4,ar-EG;q=0.9,en;q=0.8'),'ar')
        self.assertEqual(negotiate_locale('ar;q=0,fr-FR;q=0.8'),'fr')
        self.assertEqual(negotiate_locale('zz-ZZ,zh-Hans;q=0.5'),'zh')
        self.assertEqual(negotiate_locale('ar;q=nan,fa;q=2,xx'),'en')
        self.assertIsNone(resolve_locale('../../secret'));self.assertIsNone(resolve_locale(['ar']))
        self.assertEqual(resolve_locale('FA_ir'),'fa')
    def test_descriptors_preserve_source_feature_keys_for_later_language_switch(self):
        key='Review these unsupported structures: {features}. Text is retained where readable; original source is preserved.'
        source={'message':key,'messageKey':key,'messageParams':{'features':['tables','images']}}
        arabic=localize_system_message(source,'ar')
        self.assertEqual(arabic['messageParams']['features'],['tables','images'])
        self.assertIn(catalog('ar')['tables'],arabic['message'])
        french=localize_system_message(arabic,'fr')
        self.assertIn(catalog('fr')['tables'],french['message']);self.assertNotIn(catalog('ar')['tables'],french['message'])
        self.assertEqual(source['messageParams']['features'],['tables','images'])
    def test_localizer_never_recurses_into_manuscript_or_author_names(self):
        source={'title':'Your manuscripts','ast':{'text':'Saved'},'user':{'name':'Name'},'message':'Language preference updated.'}
        localized=localize_system_message(source,'ja')
        self.assertEqual(localized['title'],'Your manuscripts');self.assertEqual(localized['ast'],source['ast']);self.assertEqual(localized['user'],source['user'])
        self.assertEqual(localized['message'],catalog('ja')['Language preference updated.'])

class LocaleApiTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.app=Application(self.root,self.root/'web',start_jobs=False);self.auth=self.app.identity
    def tearDown(self):self.temp.cleanup()
    def account(self,email='author@example.test',locale=None):
        body={'email':email,'name':'Locale Author','password':PASSWORD}
        if locale:body['locale']=locale
        self.auth.register(body)
        message=next(json.loads(p.read_text()) for p in (self.root/'mail').glob('*.json') if json.loads(p.read_text())['to']==email)
        self.auth.verify(parse_qs(urlparse(message['url']).query)['token'][0])
        user,token=self.auth.login({'email':email,'password':PASSWORD});return user,token,message
    def invoke(self,path,method='GET',body=None,token=None,locale=None,csrf=True):
        raw=json.dumps(body or {}).encode();env={'REQUEST_METHOD':method,'PATH_INFO':path,'wsgi.input':BytesIO(raw),'CONTENT_LENGTH':str(len(raw)),'CONTENT_TYPE':'application/json','HTTP_ORIGIN':'http://127.0.0.1:8000','REMOTE_ADDR':'locale-fixture'}
        if token:
            env['HTTP_COOKIE']='publisher_session='+token
            if csrf:env['HTTP_X_CSRF_TOKEN']=self.auth.csrf(token)
        if locale:env['HTTP_ACCEPT_LANGUAGE']=locale
        result={}
        def start(status,headers):result.update(status=int(status.split()[0]),headers=dict(headers))
        result['body']=json.loads(b''.join(self.app(env,start)));return result
    def test_errors_are_localized_in_every_supported_language(self):
        for code in SUPPORTED:
            with self.subTest(locale=code):
                response=self.invoke('/api/v1/projects',locale=code)
                self.assertEqual(response['status'],401);self.assertEqual(response['headers']['Content-Language'],code)
                self.assertEqual(response['body']['detail'],catalog(code)['Sign in to continue.'])
                self.assertEqual(response['body']['messageKey'],'Sign in to continue.')
    def test_account_preference_is_authenticated_csrf_protected_and_persisted(self):
        user,token,_=self.account()
        self.assertEqual(self.invoke('/api/preferences','PUT',{'locale':'ar'})['status'],401)
        self.assertEqual(self.invoke('/api/preferences','PUT',{'locale':'ar'},token,csrf=False)['status'],403)
        for code in ['ar','zh','fa','pcm','de']:
            response=self.invoke('/api/preferences','PUT',{'locale':code},token,code)
            self.assertEqual(response['status'],200);self.assertEqual(response['body']['user']['locale'],code)
        fresh=Application(self.root,self.root/'web',start_jobs=False)
        self.assertEqual(fresh.identity.authenticate(token)['locale'],'de')
        self.assertEqual(self.invoke('/api/preferences','PUT',{'locale':'../bad'},token)['status'],422)
        self.assertEqual(self.invoke('/api/preferences','PUT',{'locale':'en','userId':uid()},token)['status'],422)
        self.assertEqual(self.auth.authenticate(token)['locale'],'de')
    def test_preferences_do_not_modify_authored_text_or_manuscript_direction(self):
        user,token,_=self.account();studio=self.app.studio
        p=studio.create_project(user['id'],{'title':'Original عنوان','language':'ja','direction':'ltr'},uid());ch=studio.chapter(user['id'],p['chapterId'])
        ast=empty_ast('ja','ltr');ast['content']['content'][0]['content']=[{'type':'text','text':'Original 日本語 العربية e\u0301 🖋️'}]
        studio.save(user['id'],ch['id'],{'ast':ast,'accessEpoch':1},uid(),ch['revisionId']);before=studio.chapter(user['id'],ch['id'])
        self.invoke('/api/preferences','PUT',{'locale':'ar'},token,'ar');after=studio.chapter(user['id'],ch['id'])
        self.assertEqual(before,after);self.assertEqual(after['ast'],ast)
        self.assertEqual(studio.project(user['id'],p['id'])['language'],'ja')
    def test_registration_mail_and_default_new_chapter_use_account_ui_locale(self):
        user,token,message=self.account(locale='fa')
        self.assertEqual(message['subject'],catalog('fa')['Verify your account']);self.assertEqual(parse_qs(urlparse(message['url']).query)['lang'],['fa'])
        project=self.app.studio.create_project(user['id'],{'title':'Untouched Title','language':'en'},uid())
        chapter=self.app.studio.chapter(user['id'],project['chapterId'])
        self.assertEqual(chapter['title'],translate('Chapter {number}','fa',{'number':1}));self.assertEqual(chapter['ast']['language'],'en')
        self.assertEqual(self.invoke('/api/session',token=token)['headers']['Content-Language'],'fa')
    def test_dynamic_validation_has_language_neutral_parameters(self):
        user,token,_=self.account()
        response=self.invoke('/api/v1/projects','POST',{'title':''},token,'bn')
        self.assertEqual(response['status'],422)
        self.assertEqual(response['body']['messageKey'],'{field} must contain 1–{maximum} characters.')
        self.assertEqual(response['body']['messageParams'],{'field':'Project title','maximum':300})
        self.assertIn(catalog('bn')['Project title'],response['body']['detail'])
    def test_schema_one_migration_preserves_existing_content_and_null_preference(self):
        directory=self.root/'legacy';directory.mkdir();path=directory/'publisher.sqlite3'
        owner,workspace,project,manuscript,chapter,revision=[uid() for _ in range(6)];text=canonical(empty_ast('fa','rtl'))
        with sqlite3.connect(path) as c:
            c.executescript((ROOT/'apps/api/publisher/migrations/001_authoring.sql').read_text())
            c.execute('INSERT INTO schema_migrations VALUES(1,?)',(now(),));c.execute('PRAGMA user_version=1')
            c.execute('INSERT INTO users VALUES(?,?,?,?,1,?)',(owner,'legacy@example.test','Legacy',password_hash(PASSWORD),now()))
            c.execute('INSERT INTO workspaces VALUES(?,?,?)',(workspace,owner,'Legacy workspace'))
            c.execute('INSERT INTO projects VALUES(?,?,?,?,?,?,?,?,?,?)',(project,workspace,owner,'Legacy عنوان','fa','rtl',uid(),1,now(),now()))
            c.execute('INSERT INTO manuscripts VALUES(?,?,2)',(manuscript,project));c.execute('INSERT INTO project_memberships VALUES(?,?,?)',(project,owner,'owner'))
            c.execute('INSERT INTO chapters VALUES(?,?,?,?,NULL)',(chapter,project,'Legacy',0))
            c.execute('INSERT INTO chapter_revisions VALUES(?,?,?,?,?,?,?,?,?)',(revision,project,chapter,1,text,digest(json.loads(text)),owner,None,now()))
            c.execute('UPDATE chapters SET current_revision_id=? WHERE id=?',(revision,chapter))
        migrated=Database(path)
        with migrated.connect() as c:
            self.assertEqual(c.execute('PRAGMA user_version').fetchone()[0],2)
            self.assertIsNone(c.execute('SELECT locale FROM users WHERE id=?',(owner,)).fetchone()[0])
            self.assertEqual(c.execute('SELECT ast_json FROM chapter_revisions WHERE id=?',(revision,)).fetchone()[0],text)
            self.assertEqual([r[0] for r in c.execute('SELECT version FROM schema_migrations ORDER BY version')],[1,2])
        Database(path)

if __name__=='__main__':unittest.main()
