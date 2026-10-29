"""Same-origin WSGI HTTP adapter. Loopback development server only; no production launch mode."""
from http.cookies import SimpleCookie
from pathlib import Path
from threading import Thread
from urllib.parse import parse_qs
import base64
import hmac
import json
import logging
import mimetypes
import re
import secrets
import sqlite3
import time
from .database import Database
from .domain import Problem, valid_unicode
from .identity import Identity
from .studio import Studio
from .localization import negotiate_locale, translate, localize_system_message

LOG=logging.getLogger('publisher')
MAX_BODY=8*1024*1024


class Application:
    def __init__(self,data_dir: Path,web_dir: Path,origin: str='http://127.0.0.1:8000',start_jobs: bool=True):
        self.db=Database(data_dir/'publisher.sqlite3')
        self.identity=Identity(self.db,data_dir,origin)
        self.studio=Studio(self.db)
        self.web_dir=web_dir.resolve();self.origin=origin.rstrip('/');self.start_jobs=start_jobs
        self.allowed_origins={self.origin,'http://127.0.0.1:5173','http://localhost:5173'}
        if start_jobs:
            with self.db.transaction() as c:
                c.execute("UPDATE conversion_jobs SET state='failed',error_code='INTERRUPTED' WHERE state IN('running','validating')")
                queued=[r[0] for r in c.execute("SELECT id FROM conversion_jobs WHERE state='queued'")]
            for job_id in queued:Thread(target=self.studio.process_job,args=(job_id,),daemon=True).start()

    def __call__(self,environ,start_response):
        correlation=secrets.token_hex(16);started=time.monotonic();headers=[];status=200
        route=environ.get('PATH_INFO','/');method=environ.get('REQUEST_METHOD','GET')
        locale=negotiate_locale(environ.get('HTTP_ACCEPT_LANGUAGE'))
        if not environ.get('HTTP_ACCEPT_LANGUAGE'):
            try:locale=self.identity.authenticate(self.token(environ)).get('locale') or 'en'
            except Problem:pass
        try:
            if method not in ('GET','POST','PUT','DELETE','HEAD'):raise Problem(405,'METHOD','Method not supported.')
            if not route.startswith('/api/'):
                status,payload,headers=self.static(route,method)
            else:
                data={}
                if method not in ('GET','HEAD'):
                    if environ.get('HTTP_ORIGIN') not in self.allowed_origins:raise Problem(403,'ORIGIN','This request must originate from the application.')
                    if environ.get('CONTENT_TYPE','').split(';')[0]!='application/json':raise Problem(415,'CONTENT_TYPE','Send application/json.')
                    try:length=int(environ.get('CONTENT_LENGTH') or 0)
                    except ValueError:raise Problem(400,'BODY','Invalid content length.') from None
                    if length>MAX_BODY or length<0:raise Problem(413,'BODY_LIMIT','Request exceeds the 8 MiB limit.')
                    raw=environ['wsgi.input'].read(length)
                    try:data=json.loads(raw or b'{}',parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON number')))
                    except (ValueError,UnicodeDecodeError,RecursionError):raise Problem(400,'JSON','Invalid JSON.') from None
                    if not isinstance(data,dict):raise Problem(422,'BODY','Expected a JSON object.')
                    pending=[data]
                    while pending:
                        value=pending.pop()
                        if isinstance(value,dict):pending.extend(value.keys());pending.extend(value.values())
                        elif isinstance(value,list):pending.extend(value)
                        elif isinstance(value,str) and not valid_unicode(value):raise Problem(400,'JSON','Invalid JSON.')
                status,payload,headers=self.dispatch(environ,route,method,data)
                if not isinstance(payload,bytes):
                    payload=json.dumps(localize_system_message(payload,locale),ensure_ascii=False,allow_nan=False).encode();headers.append(('Content-Type','application/json; charset=utf-8'))
        except Problem as error:
            status=error.status;payload=json.dumps({'type':'about:blank','title':translate('Your request could not be completed. Keep unsaved changes and try again.',locale),'status':status,'code':error.code,'detail':translate(error.message_key,locale,error.message_params),'messageKey':error.message_key,'messageParams':error.message_params,'correlationId':correlation}).encode()
            headers=[('Content-Type','application/problem+json')]
            if status==429:headers.append(('Retry-After','60'))
        except (sqlite3.Error,OSError,ValueError,TypeError,KeyError):
            # Logs deliberately omit bodies, exception text, cookies, query strings and manuscript content.
            status=500;payload=json.dumps({'type':'about:blank','title':translate('Your request could not be completed. Keep unsaved changes and try again.',locale),'status':500,'code':'INTERNAL','detail':translate('The request could not complete. Keep unsaved changes and retry safely.',locale),'messageKey':'The request could not complete. Keep unsaved changes and retry safely.','correlationId':correlation}).encode();headers=[('Content-Type','application/problem+json')]
            LOG.error('request_failed correlation=%s',correlation)
        phrase={200:'OK',201:'Created',202:'Accepted',204:'No Content',400:'Bad Request',401:'Unauthorized',403:'Forbidden',404:'Not Found',405:'Method Not Allowed',409:'Conflict',412:'Precondition Failed',413:'Content Too Large',415:'Unsupported Media Type',422:'Unprocessable Content',428:'Precondition Required',429:'Too Many Requests',500:'Internal Server Error',503:'Service Unavailable'}.get(status,'Response')
        headers += [('Content-Language',locale),('Vary','Accept-Language'),('X-Correlation-Id',correlation),('Cache-Control','no-store'),('X-Content-Type-Options','nosniff'),('Referrer-Policy','no-referrer'),('X-Frame-Options','DENY'),('Cross-Origin-Opener-Policy','same-origin'),('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"),('Content-Length',str(len(payload)))]
        start_response(f'{status} {phrase}',headers)
        LOG.info('request method=%s status=%s duration_ms=%d correlation=%s',method,status,(time.monotonic()-started)*1000,correlation)
        return [b'' if method=='HEAD' else payload]

    @staticmethod
    def token(environ):
        cookie=SimpleCookie()
        try:cookie.load(environ.get('HTTP_COOKIE',''))
        except Exception:return None
        return cookie['publisher_session'].value if 'publisher_session' in cookie else None

    def dispatch(self,e,path,method,data):
        headers=[];key=e.get('HTTP_IDEMPOTENCY_KEY','');expected=e.get('HTTP_IF_MATCH')
        if expected:
            if not re.fullmatch(r'"[a-fA-F0-9-]{36}"',expected):raise Problem(422,'ETAG','Expected a quoted version UUID.')
            expected=expected[1:-1]
        token=self.token(e)
        if method not in ('GET','HEAD'):
            allowed=None
            auth_fields={'register':{'email','name','password','locale'},'login':{'email','password'},'verify':{'token'},'recover':{'email'},'reset':{'token','password'},'logout':set()}
            if path.startswith('/api/auth/'):allowed=auth_fields.get(path.rsplit('/',1)[-1])
            elif path=='/api/preferences':allowed={'locale'}
            elif path=='/api/v1/projects':allowed={'title','language','direction'}
            elif re.fullmatch(r'/api/v1/chapters/[a-f0-9-]{36}',path):allowed={'ast','accessEpoch'}
            elif path.endswith('/restores'):allowed={'snapshotRevisionId'}
            elif '/imports/' in path and path.endswith('/confirm'):allowed={'reportHash','acknowledgedWarningIds'}
            else:allowed={'chapters':{'title'},'reorder':{'chapterIds'},'members':{'email','role'},'exports':{'format'},'imports':{'filename','content'}}.get(path.rsplit('/',1)[-1])
            if allowed is not None and set(data)-allowed:raise Problem(422,'UNEXPECTED_FIELDS','Unexpected request fields. Use the current operation contract.')
        if path=='/api/health' and method=='GET':return 200,{'status':'ok','mode':'local-authoring','schemaVersion':self.db.schema_version},headers
        if path.startswith('/api/auth/') and method=='POST':
            self.identity.rate_limit('auth:'+e.get('REMOTE_ADDR','local'),30)
            if path=='/api/auth/register':return 202,self.identity.register(data),headers
            if path=='/api/auth/verify':return 200,self.identity.verify(data.get('token')),headers
            if path=='/api/auth/recover':return 202,self.identity.recover(data.get('email')),headers
            if path=='/api/auth/reset':return 200,self.identity.verify(data.get('token'),data.get('password'),'recover'),headers
            if path=='/api/auth/login':
                user,new_token=self.identity.login(data)
                old=token
                if old:
                    try:self.identity.logout(old,self.identity.authenticate(old))
                    except Problem:pass
                secure='; Secure' if self.origin.startswith('https://') else ''
                headers.append(('Set-Cookie','publisher_session='+new_token+'; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800'+secure))
                return 200,{'user':user,'csrfToken':self.identity.csrf(new_token)},headers
        user=self.identity.authenticate(token);actor=user['id']
        if method not in ('GET','HEAD'):
            supplied=e.get('HTTP_X_CSRF_TOKEN','')
            if not isinstance(supplied,str) or not re.fullmatch(r'[a-f0-9]{64}',supplied) or not hmac.compare_digest(supplied,self.identity.csrf(token)):
                raise Problem(403,'CSRF','Your security token is missing or expired. Reload the session without discarding unsaved text.')
        if path=='/api/preferences' and method=='PUT':return 200,self.identity.preferences(user,data.get('locale')),headers
        if path=='/api/session' and method=='GET':return 200,{'user':user,'csrfToken':self.identity.csrf(token)},headers
        if path=='/api/auth/logout' and method=='POST':
            self.identity.logout(token,user);headers.append(('Set-Cookie','publisher_session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0'))
            return 200,{'message':'Signed out.'},headers
        if path=='/api/v1/projects':
            if method=='GET':return 200,self.studio.projects(actor),headers
            if method=='POST':return 201,self.studio.create_project(actor,data,key),headers
        m=re.fullmatch(r'/api/v1/projects/([a-f0-9-]{36})',path)
        if m and method=='GET':
            result=self.studio.project(actor,m[1]);headers.append(('ETag','"'+result['version']+'"'));return 200,result,headers
        m=re.fullmatch(r'/api/v1/projects/([a-f0-9-]{36})/(chapters|reorder|members|exports|imports)',path)
        if m:
            project,action=m.groups()
            if action=='members':
                if method=='GET':return 200,self.studio.members(actor,project),headers
                if method=='POST':return 200,self.studio.grant(actor,project,data,key),headers
            if action=='chapters' and method=='POST':return 201,self.studio.add_chapter(actor,project,data,key,expected),headers
            if action=='reorder' and method=='POST':return 200,self.studio.reorder(actor,project,data,key,expected),headers
            if action=='exports' and method=='POST':
                self.identity.rate_limit('export:'+actor,5)
                result=self.studio.export(actor,project,data,key)
                if self.start_jobs:Thread(target=self.studio.process_job,args=(result['jobId'],),daemon=True).start()
                return 202,result,headers
            if action=='imports' and method=='POST':
                self.identity.rate_limit('import:'+actor,5)
                return 201,self.studio.import_preview(actor,project,data,key),headers
        m=re.fullmatch(r'/api/v1/projects/([a-f0-9-]{36})/imports/([a-f0-9-]{36})/(confirm|source)',path)
        if m:
            project,preview,action=m.groups()
            if action=='confirm' and method=='POST':return 201,self.studio.confirm_import(actor,project,preview,data,key,expected),headers
            if action=='source' and method=='GET':
                original=self.studio.original_import(actor,project,preview)
                return 200,original['original'],[('Content-Type','application/octet-stream'),('Content-Disposition','attachment; filename="original-source"')]
        m=re.fullmatch(r'/api/v1/chapters/([a-f0-9-]{36})(?:/(history|restores|revisions/([a-f0-9-]{36})))?',path)
        if m:
            chapter,action,revision=m.groups()
            if action=='history' and method=='GET':return 200,self.studio.history(actor,chapter),headers
            if (action is None and method=='PUT') or (action=='restores' and method=='POST'):
                self.identity.rate_limit('save:'+actor+':'+chapter,120)
                result=self.studio.save(actor,chapter,data,key,expected,action=='restores');headers.append(('ETag','"'+result['revisionId']+'"'));return 200,result,headers
            if method=='GET' and (action is None or revision):
                result=self.studio.chapter(actor,chapter,revision);headers.append(('ETag','"'+result['revisionId']+'"'));return 200,result,headers
        m=re.fullmatch(r'/api/v1/jobs/([a-f0-9-]{36})',path)
        if m and method=='GET':return 200,self.studio.job(actor,m[1]),headers
        m=re.fullmatch(r'/api/v1/artifacts/([a-f0-9-]{36})',path)
        if m and method=='GET':
            artifact=self.studio.artifact(actor,m[1]);return 200,artifact['content'],[('Content-Type',artifact['media_type']),('Content-Disposition','attachment; filename="'+artifact['filename']+'"'),('X-Artifact-SHA256',artifact['sha256'])]
        if path=='/api/v1/audit' and method=='GET':
            with self.db.connect() as c:
                rows=c.execute('SELECT id,action,resource_id resourceId,created_at createdAt FROM audit_events WHERE actor_id=? ORDER BY rowid DESC LIMIT 100',(actor,)).fetchall()
                return 200,{'events':[dict(r) for r in rows]},headers
        # Public catalog is intentionally empty while publication gates are not implemented.
        raise Problem(404,'NOT_FOUND','This operation is unavailable in the current authoring milestone.')

    def static(self,path,method):
        if method not in ('GET','HEAD'):raise Problem(405,'METHOD','Method not supported.')
        candidate=(self.web_dir/path.lstrip('/')).resolve()
        if not candidate.is_relative_to(self.web_dir):raise Problem(404,'NOT_FOUND','Not found.')
        if not candidate.is_file():
            if '.' in Path(path).name:raise Problem(404,'NOT_FOUND','Asset not found.')
            candidate=self.web_dir/'index.html'
        if not candidate.is_file():raise Problem(503,'BUILD_REQUIRED','Build the web app with npm run build, or run npm run dev.')
        return 200,candidate.read_bytes(),[('Content-Type',mimetypes.guess_type(candidate.name)[0] or 'application/octet-stream')]
