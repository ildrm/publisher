"""Account lifecycle, hashed opaque sessions and local mail adapter."""
from pathlib import Path
import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import tempfile
import time
from .database import Database, now
from .domain import Problem, label, uid, valid_unicode
from .localization import resolve_locale, translate


def secret_hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def password_hash(password: str) -> str:
    if not valid_unicode(password) or not 12<=len(password)<=128 or len(password.encode())>512:
        raise Problem(422,'PASSWORD_POLICY','Use a password between 12 and 128 characters.')
    salt=secrets.token_bytes(16)
    key=hashlib.scrypt(password.encode(),salt=salt,n=32768,r=8,p=1,maxmem=64*1024*1024)
    return salt.hex()+':'+key.hex()


def password_matches(password: object, stored: str) -> bool:
    if not isinstance(password,str) or len(password)>128:return False
    try:
        salt,expected=stored.split(':')
        actual=hashlib.scrypt(password.encode(),salt=bytes.fromhex(salt),n=32768,r=8,p=1,maxmem=64*1024*1024)
        return hmac.compare_digest(actual,bytes.fromhex(expected))
    except (ValueError,TypeError):return False


def audit(connection: sqlite3.Connection,actor: str | None,action: str,resource: str,metadata: dict | None=None) -> None:
    from .domain import canonical, digest
    previous=connection.execute('SELECT event_hash FROM audit_events ORDER BY rowid DESC LIMIT 1').fetchone()
    prior=previous[0] if previous else '0'*64
    event={'id':uid(),'actor':actor,'action':action,'resource':resource,'metadata':metadata or {},'time':now(),'previous':prior}
    connection.execute('INSERT INTO audit_events VALUES(?,?,?,?,?,?,?,?)',
        (event['id'],actor,action,resource,canonical(event['metadata']),prior,digest(event),event['time']))


class Identity:
    def __init__(self,db: Database,data_dir: Path,origin: str):
        self.db,self.data_dir,self.origin=db,data_dir,origin.rstrip('/')
        self.maildir=data_dir/'mail';self.maildir.mkdir(exist_ok=True,mode=0o700)
        keyfile=data_dir/'session.key'
        # Publish only complete keys. O_EXCL followed by a write exposes an empty key
        # to another initializer and can leave one behind after a process crash.
        descriptor,temporary=tempfile.mkstemp(prefix='.session-key-',dir=data_dir)
        try:
            with os.fdopen(descriptor,'wb') as stream:
                stream.write(secrets.token_bytes(32));stream.flush();os.fsync(stream.fileno())
            try:os.link(temporary,keyfile)
            except FileExistsError:pass
        finally:os.unlink(temporary)
        keyfile.chmod(0o600)
        self.key=keyfile.read_bytes()
        if len(self.key)!=32:raise RuntimeError('Invalid local session key')
        self.dummy=password_hash('synthetic-dummy-password-not-an-account')

    def rate_limit(self,bucket: str,limit: int=12,seconds: int=60) -> None:
        timestamp=int(time.time())
        with self.db.transaction() as c:
            c.execute('DELETE FROM rate_limits WHERE expires_at<=?',(timestamp,))
            row=c.execute('SELECT * FROM rate_limits WHERE bucket=?',(bucket,)).fetchone()
            if row and row['count']>=limit:raise Problem(429,'RATE_LIMIT','Too many requests. Retry in a minute.')
            c.execute('INSERT INTO rate_limits VALUES(?,1,?) ON CONFLICT(bucket) DO UPDATE SET count=count+1',(bucket,timestamp+seconds))

    def _email(self,email: object) -> str:
        if not valid_unicode(email) or len(email)>254 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email.strip()):
            raise Problem(422,'EMAIL_INVALID','Enter a valid email address.')
        return email.strip().casefold()

    def _send(self,c,user: sqlite3.Row | dict,purpose: str) -> None:
        token=secrets.token_urlsafe(32)
        c.execute('UPDATE account_tokens SET used=1 WHERE user_id=? AND purpose=?',(user['id'],purpose))
        c.execute('INSERT INTO account_tokens VALUES(?,?,?,?,0)',(secret_hash(token),user['id'],purpose,int(time.time())+1800))
        route='verify' if purpose=='verify' else 'reset'
        locale=user.get('locale') if isinstance(user,dict) else user['locale']
        locale=locale or 'en'
        message={'to':user['email'],'subject':translate('Verify your account' if purpose=='verify' else 'Reset your password',locale),
                 'url':self.origin+'/'+route+'?token='+token+'&lang='+locale,'locale':locale,'createdAt':now(),'adapter':'LOCAL_MAILBOX_ONLY'}
        fd=os.open(self.maildir/(uid()+'.json'),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as stream:json.dump(message,stream)

    def register(self,data: dict) -> dict:
        locale=resolve_locale(data.get('locale'))
        if data.get('locale') is not None and not locale:raise Problem(422,'LOCALE_INVALID','Choose a supported interface language.')
        email=self._email(data.get('email'));name=label(data.get('name'),'Name',100);hashed=password_hash(data.get('password'))
        with self.db.transaction() as c:
            existing=c.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone()
            if existing:
                if not existing['verified']:self._send(c,existing,'verify')
            else:
                user={'id':uid(),'email':email,'name':name,'locale':locale}
                c.execute('INSERT INTO users(id,email,name,password_hash,verified,created_at,locale) VALUES(?,?,?,?,0,?,?)',(user['id'],email,name,hashed,now(),locale))
                c.execute('INSERT INTO workspaces VALUES(?,?,?)',(uid(),user['id'],name+'’s workspace'))
                self._send(c,user,'verify');audit(c,user['id'],'account.register',user['id'])
        return {'message':'If this address can be registered, a verification message is available. Check your email.'}

    def verify(self,token: object,password: object=None,purpose: str='verify') -> dict:
        if not isinstance(token,str) or not 20<=len(token)<=200:raise Problem(422,'TOKEN_INVALID','This link is invalid or expired.')
        hashed=password_hash(password) if purpose=='recover' else None
        with self.db.transaction() as c:
            row=c.execute('SELECT * FROM account_tokens WHERE token_hash=? AND purpose=? AND used=0 AND expires_at>?',(secret_hash(token),purpose,int(time.time()))).fetchone()
            if not row:raise Problem(422,'TOKEN_INVALID','This link is invalid or expired.')
            c.execute('UPDATE account_tokens SET used=1 WHERE token_hash=?',(secret_hash(token),))
            if purpose=='recover':
                c.execute('UPDATE users SET password_hash=? WHERE id=?',(hashed,row['user_id']))
                c.execute('DELETE FROM sessions WHERE user_id=?',(row['user_id'],))
            else:c.execute('UPDATE users SET verified=1 WHERE id=?',(row['user_id'],))
            audit(c,row['user_id'],'account.'+purpose,row['user_id'])
        return {'message':'Password updated. Sign in again.' if purpose=='recover' else 'Email verified. You can now sign in.'}

    def recover(self,email: object) -> dict:
        email=self._email(email)
        with self.db.transaction() as c:
            user=c.execute('SELECT * FROM users WHERE email=? AND verified=1',(email,)).fetchone()
            if user:self._send(c,user,'recover')
        return {'message':'If this address has a verified account, a recovery message is available.'}

    def login(self,data: dict) -> tuple[dict,str]:
        email=self._email(data.get('email'))
        # Scrypt is deliberately expensive; do not hold SQLite's global writer
        # lock during password verification. Recheck the observed hash below so
        # a concurrent password reset cannot create a session with old credentials.
        with self.db.connect() as c:
            observed=c.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone()
        correct=password_matches(data.get('password'),observed['password_hash'] if observed else self.dummy)
        if not observed or not correct or not observed['verified']:
            raise Problem(401,'LOGIN_FAILED','Could not sign in. Check your credentials and verify your email.')
        with self.db.transaction() as c:
            user=c.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone()
            if not user or user['password_hash']!=observed['password_hash'] or not user['verified']:
                raise Problem(401,'LOGIN_FAILED','Could not sign in. Check your credentials and verify your email.')
            token=secrets.token_urlsafe(32)
            c.execute('DELETE FROM sessions WHERE expires_at<=?',(int(time.time()),))
            c.execute('INSERT INTO sessions VALUES(?,?,?)',(secret_hash(token),user['id'],int(time.time())+28800))
            audit(c,user['id'],'session.login',user['id'])
            return self._public(user),token

    def authenticate(self,token: str | None) -> dict:
        if not token or len(token)>200:raise Problem(401,'AUTH_REQUIRED','Sign in to continue.')
        with self.db.connect() as c:
            user=c.execute('SELECT u.* FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=? AND s.expires_at>? AND u.verified=1',(secret_hash(token),int(time.time()))).fetchone()
            if not user:raise Problem(401,'AUTH_REQUIRED','Your session expired. Sign in again; keep any unsaved changes.')
            return self._public(user)

    @staticmethod
    def _public(user) -> dict:return {'id':user['id'],'email':user['email'],'name':user['name'],'locale':user['locale']}

    def csrf(self,token: str) -> str:
        return hmac.new(self.key,token.encode(),hashlib.sha256).hexdigest()

    def logout(self,token: str,user: dict) -> None:
        with self.db.transaction() as c:
            c.execute('DELETE FROM sessions WHERE token_hash=?',(secret_hash(token),));audit(c,user['id'],'session.logout',user['id'])

    def preferences(self,user: dict,value: object) -> dict:
        locale=resolve_locale(value)
        if not locale:raise Problem(422,'LOCALE_INVALID','Choose a supported interface language.')
        with self.db.transaction() as c:
            c.execute('UPDATE users SET locale=? WHERE id=?',(locale,user['id']))
            audit(c,user['id'],'account.locale',user['id'],{'locale':locale})
            fresh=c.execute('SELECT * FROM users WHERE id=?',(user['id'],)).fetchone()
            return {'user':self._public(fresh),'message':'Language preference updated.'}
