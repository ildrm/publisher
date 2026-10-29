"""Pure, bounded semantic transformations. No network IO or rendered-HTML source."""
from html import escape
from io import BytesIO
from pathlib import PurePosixPath
import re
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from .domain import uid, validate_ast, plain_text, Problem

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def text_direction(text: str, fallback: str='ltr') -> str:
    for character in text:
        strong=unicodedata.bidirectional(character)
        if strong=='L':return 'ltr'
        if strong in ('R','AL'):return 'rtl'
    return fallback


def language_direction(language: str) -> str:
    parts=language.lower().split('-')
    if any(p in ('latn','cyrl','hans','hant','deva','beng') for p in parts[1:]):return 'ltr'
    return 'rtl' if parts[0] in ('ar','arc','ckb','dv','fa','he','ks','nqo','ps','sd','syr','ug','ur','yi') or any(p in ('arab','hebr','thaa','syrc','nkoo','adlm','rohg') for p in parts[1:]) else 'ltr'

def inline_html(node: dict) -> str:
    if node['type']=='hardBreak': return '<br/>'
    value=escape(node.get('text',''))
    for mark in reversed(node.get('marks',[])):
        tag={'bold':'strong','italic':'em','strike':'s','code':'code'}.get(mark['type'])
        if tag: value=f'<{tag}>{value}</{tag}>'
        elif mark['type']=='link': value=f'<a href="{escape(mark["attrs"]["href"],quote=True)}" rel="noopener noreferrer">{value}</a>'
    return value

def block_html(node: dict) -> str:
    kind=node['type']
    if kind in ('text','hardBreak'): return inline_html(node)
    if kind=='horizontalRule':return '<hr/>'
    tag={'doc':'div','paragraph':'p','heading':'h'+str(node.get('attrs',{}).get('level',1)),
         'blockquote':'blockquote','bulletList':'ul','orderedList':'ol','listItem':'li'}[kind]
    attrs=(f' start="{node["attrs"].get("start",1)}"'+(f' type="{node["attrs"]["type"]}"' if node['attrs'].get('type') else '')) if kind=='orderedList' else ''
    return f'<{tag}{attrs}>'+''.join(block_html(n) for n in node.get('content',[]))+f'</{tag}>'

def inline_md(node: dict) -> str:
    if node['type']=='hardBreak': return '  \n'
    value=re.sub(r'([\\`*_[\]<>])',r'\\\1',node.get('text',''))
    for mark in reversed(node.get('marks',[])):
        token={'bold':'**','italic':'*','strike':'~~','code':'`'}.get(mark['type'])
        if token:value=token+value+token
        elif mark['type']=='link':value=f'[{value}]({mark["attrs"]["href"].replace(")","%29")})'
    return value

def block_md(node: dict,indent: str='') -> str:
    kind=node['type']
    if kind in ('text','hardBreak'):return inline_md(node)
    if kind=='horizontalRule':return '\n---\n\n'
    if kind in ('paragraph','heading'):
        return ('#'*node['attrs']['level']+' ' if kind=='heading' else '')+''.join(inline_md(n) for n in node.get('content',[]))+'\n\n'
    if kind=='blockquote':return ''.join('> '+line+'\n' for line in ''.join(block_md(n) for n in node.get('content',[])).rstrip().splitlines())+'\n'
    if kind in ('bulletList','orderedList'):
        result=[]
        for i,item in enumerate(node.get('content',[])):
            value=''.join(block_md(n) for n in item.get('content',[])).strip()
            prefix=f'{i+node.get("attrs",{}).get("start",1)}. ' if kind=='orderedList' else '- '
            lines=value.splitlines() or ['']
            result.append(indent+prefix+lines[0]+'\n'+''.join(indent+'  '+x+'\n' for x in lines[1:]))
        return ''.join(result)+'\n'
    return ''.join(block_md(n,indent) for n in node.get('content',[]))

def zip_bytes(files: dict[str,bytes]) -> bytes:
    stream=BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,data in files.items():
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_STORED if name=='mimetype' else zipfile.ZIP_DEFLATED
            archive.writestr(info,data)
    return stream.getvalue()

def export_document(manifest: dict, format_name: str) -> tuple[bytes,str,str]:
    chapters=manifest['chapters']
    for chapter in chapters: validate_ast(chapter['ast'])
    title=manifest['title'];lang=manifest['language']
    if format_name=='bundle':
        from .domain import canonical
        markdown=export_document(manifest,'markdown')[0]
        docx=export_document(manifest,'docx')[0]
        return zip_bytes({'manuscript.json':canonical(manifest).encode(),'manuscript.md':markdown,'manuscript.docx':docx,'README.txt':b'Canonical source and metadata are in manuscript.json. Export does not grant publishing rights. DOCX conversion limitations: hyperlink targets, quote styles and nested numbering need review. No print/accessibility certification is claimed.'}),'application/zip','zip'
    if format_name in ('markdown','text'):
        content='# '+title+'\n\n' if format_name=='markdown' else title+'\n\n'
        for c in chapters:
            content += ('# '+c['title']+'\n\n'+block_md(c['ast']['content']) if format_name=='markdown' else c['title']+'\n\n'+plain_text(c['ast']['content'])+'\n\n')
        return content.encode(), 'text/markdown; charset=utf-8' if format_name=='markdown' else 'text/plain; charset=utf-8','md' if format_name=='markdown' else 'txt'
    if format_name=='html':
        body=''.join(f'<section lang="{escape(c["ast"]["language"])}" dir="{c["ast"]["direction"]}"><h1>{escape(c["title"])}</h1>{block_html(c["ast"]["content"])}</section>' for c in chapters)
        return f'<!doctype html><html lang="{escape(lang)}" dir="{escape(manifest.get("direction","auto"))}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{escape(title)}</title></head><body><header><h1>{escape(title)}</h1></header><main>{body}</main></body></html>'.encode(),'text/html; charset=utf-8','html'
    if format_name=='docx':
        ET.register_namespace('w',W)
        document=ET.Element(f'{{{W}}}document');body=ET.SubElement(document,f'{{{W}}}body')
        numbering_definitions=[]
        def paragraph(text: str,language: str,direction: str,style: str | None=None,list_id=None,list_depth=0):
            p=ET.SubElement(body,f'{{{W}}}p')
            props=ET.SubElement(p,f'{{{W}}}pPr')
            if style:ET.SubElement(props,f'{{{W}}}pStyle',{f'{{{W}}}val':style})
            if list_id:
                np=ET.SubElement(props,f'{{{W}}}numPr');ET.SubElement(np,f'{{{W}}}ilvl',{f'{{{W}}}val':'0'});ET.SubElement(np,f'{{{W}}}numId',{f'{{{W}}}val':str(list_id)})
            ET.SubElement(props,f'{{{W}}}bidi',{f'{{{W}}}val':'1' if direction=='rtl' else '0'})
            if list_id:ET.SubElement(props,f'{{{W}}}ind',{f'{{{W}}}right' if direction=='rtl' else f'{{{W}}}left':str(720*(list_depth+1)),f'{{{W}}}hanging':'360'})
            mark=ET.SubElement(props,f'{{{W}}}rPr')
            ET.SubElement(mark,f'{{{W}}}lang',{f'{{{W}}}val':language,f'{{{W}}}bidi':language,f'{{{W}}}eastAsia':language})
            return p
        def run(p,node,language,direction):
            r=ET.SubElement(p,f'{{{W}}}r')
            props=ET.SubElement(r,f'{{{W}}}rPr')
            for m in node.get('marks',[]):
                tag={'bold':'b','italic':'i','strike':'strike','code':'rFonts'}.get(m['type'])
                if tag:ET.SubElement(props,f'{{{W}}}{tag}',{f'{{{W}}}ascii':'monospace',f'{{{W}}}hAnsi':'monospace'} if tag=='rFonts' else {})
            ET.SubElement(props,f'{{{W}}}rtl',{f'{{{W}}}val':'1' if text_direction(node.get('text',''),direction)=='rtl' else '0'})
            ET.SubElement(props,f'{{{W}}}lang',{f'{{{W}}}val':language,f'{{{W}}}bidi':language,f'{{{W}}}eastAsia':language})
            if node['type']=='hardBreak': ET.SubElement(r,f'{{{W}}}br');return
            for part in re.split(r'(\r\n|[\r\n\t])',node.get('text','')):
                if part=='\t':ET.SubElement(r,f'{{{W}}}tab')
                elif part in ('\r','\n','\r\n'):ET.SubElement(r,f'{{{W}}}br')
                elif part:ET.SubElement(r,f'{{{W}}}t',{'{http://www.w3.org/XML/1998/namespace}space':'preserve'}).text=part
        def visit(node,language,base_direction,list_id=None,list_depth=0):
            kind=node['type']
            if kind in ('paragraph','heading'):
                direction=text_direction(plain_text(node),language_direction(language)) if base_direction=='auto' else base_direction
                p=paragraph('',language,direction,'Heading'+str(node['attrs']['level']) if kind=='heading' else None,list_id,list_depth)
                for child in node.get('content',[]):run(p,child,language,direction)
            elif kind=='horizontalRule':
                direction=language_direction(language) if base_direction=='auto' else base_direction
                run(paragraph('',language,direction),{'type':'text','text':'* * *'},language,direction)
            elif kind in ('bulletList','orderedList'):
                attrs=node.get('attrs',{});number_id=len(numbering_definitions)+1
                fmt={'a':'lowerLetter','A':'upperLetter','i':'lowerRoman','I':'upperRoman'}.get(attrs.get('type'),'decimal') if kind=='orderedList' else 'bullet'
                numbering_definitions.append((number_id,fmt,attrs.get('start',1),'•' if kind=='bulletList' else '%1.'))
                for child in node.get('content',[]):visit(child,language,base_direction,number_id,list_depth)
            elif kind=='listItem':
                for i,child in enumerate(node.get('content',[])):
                    visit(child,language,base_direction,list_id if i==0 else None,list_depth+1 if child['type'] in ('bulletList','orderedList') else list_depth)
            else:
                for child in node.get('content',[]):visit(child,language,base_direction,list_id,list_depth)
        for c in chapters:
            language=c['ast']['language'];base_direction=c['ast']['direction']
            direction=text_direction(c['title'],language_direction(language)) if base_direction=='auto' else base_direction
            run(paragraph('',language,direction,'Heading1'),{'type':'text','text':c['title']},language,direction)
            for n in c['ast']['content']['content']:visit(n,language,base_direction)
        styles=f'<w:styles xmlns:w="{W}">'+''.join(f'<w:style w:type="paragraph" w:styleId="Heading{i}"><w:name w:val="heading {i}"/><w:pPr><w:outlineLvl w:val="{i-1}"/></w:pPr></w:style>' for i in range(1,4))+'</w:styles>'
        numbering=f'<w:numbering xmlns:w="{W}">'+''.join(f'<w:abstractNum w:abstractNumId="{i}"><w:lvl w:ilvl="0"><w:start w:val="{start}"/><w:numFmt w:val="{fmt}"/><w:lvlText w:val="{t}"/></w:lvl></w:abstractNum>' for i,fmt,start,t in numbering_definitions)+''.join(f'<w:num w:numId="{i}"><w:abstractNumId w:val="{i}"/></w:num>' for i,fmt,start,t in numbering_definitions)+'</w:numbering>'
        document_xml=ET.tostring(document,encoding='utf-8',xml_declaration=True)
        try:ET.fromstring(document_xml)
        except ET.ParseError:raise Problem(422,'CONVERSION_FAILED','Conversion failed safely. Your manuscript and previous exports are unchanged.') from None
        files={'[Content_Types].xml':b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>',
        '_rels/.rels':b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>',
        'word/_rels/document.xml.rels':b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="styles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="numbering" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/></Relationships>',
        'word/document.xml':document_xml,'word/styles.xml':styles.encode(),'word/numbering.xml':numbering.encode()}
        return zip_bytes(files),'application/vnd.openxmlformats-officedocument.wordprocessingml.document','docx'
    raise Problem(422,'FORMAT_UNAVAILABLE','This export format is not implemented in this milestone.')


def parse_import(filename: str, data: bytes, lang: str, direction: str) -> tuple[dict,list[dict]]:
    if not data or len(data)>5*1024*1024:raise Problem(422,'IMPORT_SIZE','Choose a nonempty file up to 5 MiB.')
    nodes=[];warnings=[]
    def add(kind,text,attrs=None):
        node={'type':kind,'attrs':{'id':uid(),**(attrs or {})}}
        if text:node['content']=[{'type':'text','text':text}]
        nodes.append(node)
    extension=filename.lower().rsplit('.',1)[-1]
    if extension in ('md','txt'):
        try:text=data.decode('utf-8-sig')
        except UnicodeDecodeError:raise Problem(422,'IMPORT_ENCODING','Choose a UTF-8 text file.') from None
        if '\x00' in text:raise Problem(422,'IMPORT_ENCODING','Binary content is not accepted as text.')
        for block in re.split(r'\n\s*\n',text):
            if not block.strip():continue
            match=re.match(r'^(#{1,3}) (.*)$',block,re.S)
            if match and extension=='md':add('heading',match[2],{'level':len(match[1])})
            else:add('paragraph',block)
        if extension=='md':warnings.append({'id':'markdown-literal','message':'Headings are imported semantically. Other Markdown syntax is preserved as literal text; review formatting before confirming.'})
    elif extension=='docx':
        try:
            with zipfile.ZipFile(BytesIO(data)) as z:
                names=set();total=0
                if len(z.infolist())>1000:raise ValueError('Too many archive entries')
                for f in z.infolist():
                    name=f.filename;parts=PurePosixPath(name).parts
                    if name in names or name.startswith('/') or '..' in parts or '\\' in name or ':' in name or f.flag_bits&1 or (f.external_attr>>16)&0o170000==0o120000:
                        raise ValueError('Unsafe archive entry')
                    names.add(name);total+=f.file_size
                    if total>20*1024*1024 or f.file_size>10*1024*1024 or (f.file_size>100000 and f.file_size/max(f.compress_size,1)>100):raise ValueError('Archive expansion limit')
                    if f.compress_type not in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED):raise ValueError('Unsupported compression')
                    if any(x in name.lower() for x in ('vbaproject','activex','embeddings/')):raise ValueError('Active content is not supported')
                if '[Content_Types].xml' not in names or 'word/document.xml' not in names:raise ValueError('Not a DOCX document')
                raw=z.read('word/document.xml').decode('utf-8-sig')
                if '<!DOCTYPE' in raw.upper() or '<!ENTITY' in raw.upper():raise ValueError('Unsafe XML declarations')
                doc=ET.fromstring(raw)
                for p in doc.iter(f'{{{W}}}p'):
                    content=[]
                    for run in p.iter(f'{{{W}}}r'):
                        marks=[]
                        for tag,kind in [('b','bold'),('i','italic'),('strike','strike')]:
                            prop=run.find(f'{{{W}}}rPr/{{{W}}}{tag}')
                            if prop is not None and prop.get(f'{{{W}}}val','true').lower() not in ('0','false','off'):marks.append({'type':kind})
                        for part in run:
                            if part.tag in (f'{{{W}}}br',f'{{{W}}}cr'):
                                content.append({'type':'hardBreak'})
                            else:
                                txt=(part.text or '') if part.tag==f'{{{W}}}t' else '\t' if part.tag==f'{{{W}}}tab' else '\u2011' if part.tag==f'{{{W}}}noBreakHyphen' else '\u00ad' if part.tag==f'{{{W}}}softHyphen' else ''
                                if txt:content.append({'type':'text','text':txt,**({'marks':marks} if marks else {})})
                    style=p.find(f'{{{W}}}pPr/{{{W}}}pStyle');level=re.search(r'heading\s*([123])',style.get(f'{{{W}}}val',''),re.I) if style is not None else None
                    n={'type':'heading' if level else 'paragraph','attrs':{'id':uid(),**({'level':int(level[1])} if level else {})}}
                    if content:n['content']=content
                    nodes.append(n)
                features=[]
                for tag,name in [('tbl','tables'),('drawing','images'),('footnoteReference','footnotes'),('endnoteReference','endnotes'),('hyperlink','hyperlink targets'),('numPr','list numbering'),('sectPr','page layout')]:
                    if next(doc.iter(f'{{{W}}}{tag}'),None) is not None:features.append(name)
                if features:warnings.append({'id':'docx-transforms','message':'Review these unsupported structures: '+', '.join(features)+'. Text is retained where readable; original source is preserved.','messageKey':'Review these unsupported structures: {features}. Text is retained where readable; original source is preserved.','messageParams':{'features':features}})
        except (zipfile.BadZipFile,KeyError,ValueError,UnicodeDecodeError,ET.ParseError,RuntimeError,NotImplementedError) as exc:
            raise Problem(422,'UNSAFE_IMPORT','Import could not be processed safely. Choose a supported DOCX, Markdown or text file.') from None
    else:raise Problem(422,'IMPORT_TYPE','Supported imports are DOCX, Markdown and UTF-8 text.')
    if not nodes:nodes=[{'type':'paragraph','attrs':{'id':uid()}}]
    ast={'schemaVersion':2,'language':lang,'direction':direction,'content':{'type':'doc','content':nodes}}
    return validate_ast(ast),warnings
