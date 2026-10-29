"""Single-command conversion child. Resource limited locally; no kernel network sandbox claim."""
import base64
import hashlib
import json
import sys
import resource
from .formats import export_document, parse_import
from .domain import Problem


def main() -> None:
    resource.setrlimit(resource.RLIMIT_CPU,(15,15))
    resource.setrlimit(resource.RLIMIT_FSIZE,(32*1024*1024,32*1024*1024))
    # macOS does not reliably enforce RLIMIT_AS. Container memory/network isolation remains G3 work.
    if sys.platform!='darwin':resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024))
    raw=sys.stdin.buffer.read(16*1024*1024+1)
    if len(raw)>16*1024*1024:raise ValueError('Input limit')
    data=json.loads(raw)
    if sys.argv[1]=='export':
        content,media,extension=export_document(data['manifest'],data['format'])
        result={'content':base64.b64encode(content).decode(),'mediaType':media,'extension':extension,'sha256':hashlib.sha256(content).hexdigest()}
    elif sys.argv[1]=='import':
        ast,warnings=parse_import(data['filename'],base64.b64decode(data['content'],validate=True),data['language'],data['direction'])
        result={'ast':ast,'warnings':warnings}
    else:raise ValueError('Unknown worker command')
    sys.stdout.write(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    try:main()
    except Problem as error:
        sys.stdout.write(json.dumps({'error':{'status':error.status,'code':error.code,'detail':error.detail,'messageKey':error.message_key,'messageParams':error.message_params}},ensure_ascii=False))
        sys.exit(1)
