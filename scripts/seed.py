"""Create an original synthetic demo in local/test only; never overwrite existing manuscript revisions."""
import argparse
import json
import os
from pathlib import Path
import sys
from urllib.parse import parse_qs,urlparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'apps/api'))
from publisher.database import Database
from publisher.identity import Identity
from publisher.studio import Studio
from publisher.domain import empty_ast

parser=argparse.ArgumentParser();parser.add_argument('--email',default='writer@example.test');args=parser.parse_args()
if os.environ.get('PUBLISHER_ENV','local') not in ('local','test') or not args.email.endswith('.test'):
    raise SystemExit('Seed is restricted to synthetic .test accounts in local/test.')
password=os.environ.get('PUBLISHER_SEED_PASSWORD')
if not password:raise SystemExit('Set PUBLISHER_SEED_PASSWORD to a synthetic password of at least 12 characters. It will not be printed.')
root=Path(os.environ.get('PUBLISHER_DATA_DIR',Path(__file__).resolve().parents[1]/'.data'))
db=Database(root/'publisher.sqlite3');identity=Identity(db,root,'http://127.0.0.1:8000');studio=Studio(db)
with db.connect() as c:existing=c.execute('SELECT verified FROM users WHERE email=?',(args.email,)).fetchone()
if not existing or not existing['verified']:
    identity.register({'email':args.email,'name':'Demo Author','password':password})
    messages=[json.loads(p.read_text()) for p in (root/'mail').glob('*.json')]
    message=next(m for m in messages if m['to']==args.email and m['subject']=='Verify your account')
    identity.verify(parse_qs(urlparse(message['url']).query)['token'][0])
user,token=identity.login({'email':args.email,'password':password})
project=studio.create_project(user['id'],{'title':'The Quiet Atlas','language':'en','direction':'auto'},'seed-original-project-v1')
chapter=studio.chapter(user['id'],project['chapterId'])
if chapter['sequence']==1:
    ast=empty_ast();ast['content']['content'][0]['content']=[{'type':'text','text':'At the edge of the old harbor, Mara found a map that named no countries. It marked the places where people had changed their minds. A narrow blue line led from the room she had left to the road she had not yet taken.'}]
    studio.save(user['id'],chapter['id'],{'ast':ast,'accessEpoch':chapter['accessEpoch']},'seed-original-chapter-v1',chapter['revisionId'])
identity.logout(token,user)
print('Synthetic demo ready for '+args.email+'; project '+project['id']+'. Existing revisions were preserved.')
