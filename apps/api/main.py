"""Developer CLI. This server intentionally binds loopback; production deployment is blocked."""
import argparse
import fcntl
import json
import logging
import os
from pathlib import Path
from urllib.parse import urlparse
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server
from publisher.database import Database
from publisher.http import Application

ROOT=Path(__file__).resolve().parents[2]

class Server(ThreadingMixIn,WSGIServer):
    daemon_threads=True

class PrivateLog(WSGIRequestHandler):
    def log_message(self,format,*args):pass # Application emits redacted structured fields, never URL queries.

def main():
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['serve','migrate','mail','backup','check'])
    parser.add_argument('--data-dir',type=Path,default=Path(os.environ.get('PUBLISHER_DATA_DIR',ROOT/'.data')))
    parser.add_argument('--port',type=int,default=int(os.environ.get('PORT','8000')))
    parser.add_argument('--destination',type=Path)
    args=parser.parse_args()
    if args.command in ('backup','check') and not (args.data_dir/'publisher.sqlite3').is_file():
        raise SystemExit('No existing database at this path; refusing an empty backup/check.')
    args.data_dir.mkdir(parents=True,exist_ok=True,mode=0o700)
    if os.environ.get('PUBLISHER_ENV','local') not in ('local','test'):
        raise SystemExit('Production/staging activation is blocked pending deployment, security and recovery gates. Use local/test only.')
    if args.command=='mail':
        for p in sorted((args.data_dir/'mail').glob('*.json')):print(p.read_text())
        return
    db=Database(args.data_dir/'publisher.sqlite3')
    if args.command=='migrate':print('Schema 2 applied; existing data preserved.');return
    if args.command=='backup':
        if not args.destination:raise SystemExit('--destination is required')
        db.backup(args.destination);print('Consistent SQLite backup created.');return
    if args.command=='check':
        with db.connect() as c:print(json.dumps({'integrity':c.execute('PRAGMA integrity_check').fetchone()[0],'foreignKeys':len(c.execute('PRAGMA foreign_key_check').fetchall()),'schemaVersion':c.execute('PRAGMA user_version').fetchone()[0]}))
        return
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)s %(message)s')
    origin=os.environ.get('PUBLISHER_ORIGIN',f'http://127.0.0.1:{args.port}')
    try:
        parsed_origin=urlparse(origin)
        valid_origin=(parsed_origin.scheme=='http' and parsed_origin.hostname in ('127.0.0.1','localhost') and parsed_origin.path in ('','/')
                      and parsed_origin.username is None and parsed_origin.password is None and not parsed_origin.query and not parsed_origin.fragment
                      and (parsed_origin.port is None or 1<=parsed_origin.port<=65535))
    except ValueError:valid_origin=False
    if not valid_origin:
        raise SystemExit('Local origin must be an http loopback URL. Production TLS/configuration is not enabled.')
    if not 1<=args.port<=65535:raise SystemExit('Local server port must be between 1 and 65535.')
    lock=open(args.data_dir/'server.lock','a+')
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise SystemExit('This data directory already has a running local server.') from None
    with make_server('127.0.0.1',args.port,None,server_class=Server,handler_class=PrivateLog) as server:
        app=Application(args.data_dir,ROOT/'apps/web/dist',origin);server.set_app(app)
        print(f'Publisher author studio: http://127.0.0.1:{args.port} (local only)',flush=True)
        server.serve_forever()

if __name__=='__main__':main()
