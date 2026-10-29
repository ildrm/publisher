"""Canonical semantic schema v2, independent of rendered HTML and publishing state."""
import hashlib
import json
import re
from uuid import UUID, uuid4
from urllib.parse import urlparse


class Problem(Exception):
    def __init__(self, status: int, code: str, detail: str, message_key: str | None=None, message_params: dict | None=None):
        super().__init__(detail)
        self.status, self.code, self.detail = status, code, detail
        self.message_key=message_key or detail
        self.message_params=dict(message_params or {})


def uid() -> str:
    return str(uuid4())


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def valid_unicode(value: object) -> bool:
    return isinstance(value,str) and re.search('[\ud800-\udfff]',value) is None


def label(value: object, field: str, maximum: int = 300) -> str:
    if not valid_unicode(value) or not 1 <= len(value.strip()) <= maximum or '\x00' in value:
        raise Problem(422, 'INVALID_INPUT', f'{field} must contain 1–{maximum} characters.','{field} must contain 1–{maximum} characters.',{'field':field,'maximum':maximum})
    return value.strip()


def language(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r'[a-zA-Z]{2,8}(?:-[a-zA-Z0-9]{1,8})*', value):
        raise Problem(422, 'INVALID_LANGUAGE', 'Enter a language tag such as en or fa-IR.')
    return value


def empty_ast(lang: str = 'en', direction: str = 'auto') -> dict:
    return {'schemaVersion': 2, 'language': lang, 'direction': direction,
            'content': {'type': 'doc', 'content': [{'type': 'paragraph', 'attrs': {'id': uid()}}]}}


def validate_ast(ast: object) -> dict:
    if not isinstance(ast, dict) or set(ast) != {'schemaVersion','language','direction','content'} or ast['schemaVersion'] != 2:
        raise Problem(422,'AST_SCHEMA','Expected canonical manuscript schema version 2.')
    language(ast['language'])
    if ast['direction'] not in ('ltr','rtl','auto'):
        raise Problem(422,'AST_DIRECTION','Choose auto, left-to-right or right-to-left direction.')
    rules = {'doc': {'paragraph','heading','blockquote','bulletList','orderedList','horizontalRule'},
             'blockquote': {'paragraph','heading','bulletList','orderedList'},
             'bulletList': {'listItem'}, 'orderedList': {'listItem'},
             'listItem': {'paragraph','bulletList','orderedList'},
             'paragraph': {'text','hardBreak'}, 'heading': {'text','hardBreak'},
             'horizontalRule': set(), 'text': set(), 'hardBreak': set()}
    ids: set[str] = set()
    count, text_count = 0, 0

    def visit(node: object, parent: str | None, depth: int) -> None:
        nonlocal count, text_count
        count += 1
        if count > 25000 or depth > 24:
            raise Problem(422,'AST_LIMIT','This chapter exceeds the structural limit. Split it into chapters.')
        if not isinstance(node, dict) or set(node) - {'type','attrs','content','text','marks'}:
            raise Problem(422,'AST_NODE','Unsupported document node or attributes.')
        kind = node.get('type')
        if not isinstance(kind,str) or kind not in rules or (parent is None and kind != 'doc') or (parent and kind not in rules[parent]):
            raise Problem(422,'AST_STRUCTURE','Unsupported or incorrectly nested document structure.')
        attrs = node.get('attrs', {})
        allowed_attrs = {'id'} | ({'level'} if kind == 'heading' else {'start','type'} if kind == 'orderedList' else set())
        if kind in ('text','hardBreak','doc'): allowed_attrs=set()
        if not isinstance(attrs, dict) or set(attrs) - allowed_attrs:
            raise Problem(422,'AST_ATTRIBUTES','Unsupported document attributes.')
        if kind not in ('text','hardBreak','doc'):
            ident = attrs.get('id')
            try:
                UUID(ident)
            except (ValueError,TypeError,AttributeError):
                raise Problem(422,'AST_ID','Each block requires a stable UUID.') from None
            if ident in ids: raise Problem(422,'AST_ID','Block identifiers must be unique.')
            ids.add(ident)
        if kind == 'heading' and (type(attrs.get('level')) is not int or not 1 <= attrs['level'] <= 3):
            raise Problem(422,'AST_HEADING','Heading level must be 1, 2 or 3.')
        if kind == 'orderedList' and (type(attrs.get('start',1)) is not int or not 1 <= attrs.get('start',1) <= 100000):
            raise Problem(422,'AST_LIST','Invalid starting list number.')
        if kind == 'orderedList' and attrs.get('type') not in (None,'1','a','A','i','I'):
            raise Problem(422,'AST_LIST','Unsupported list numbering style.')
        if kind == 'text':
            if not valid_unicode(node.get('text')) or not node['text'] or '\x00' in node['text']:
                raise Problem(422,'AST_TEXT','Text must be a nonempty Unicode string without null characters.')
            text_count += len(node['text'])
        elif 'text' in node:
            raise Problem(422,'AST_TEXT','Only text nodes may contain text.')
        marks = node.get('marks', [])
        if kind != 'text' and marks:
            raise Problem(422,'AST_MARK','Marks are supported on text only.')
        if not isinstance(marks, list) or len(marks)>5:
            raise Problem(422,'AST_MARK','Invalid text formatting.')
        seen_marks=set()
        for mark in marks:
            if not isinstance(mark,dict) or mark.get('type') not in ('bold','italic','strike','code','link') or set(mark)-{'type','attrs'} or mark['type'] in seen_marks:
                raise Problem(422,'AST_MARK','Unsupported or duplicate text formatting.')
            seen_marks.add(mark['type'])
            if mark['type']=='link':
                ma=mark.get('attrs',{})
                if not isinstance(ma,dict) or set(ma)-{'href','target','rel','class'}:
                    raise Problem(422,'AST_LINK','Unsupported link attributes.')
                href=ma.get('href')
                try: scheme=urlparse(href).scheme.lower() if isinstance(href,str) else ''
                except ValueError: scheme=''
                if not valid_unicode(href) or len(href)>2048 or scheme not in ('https','http','mailto') or any(ord(c)<32 for c in href):
                    raise Problem(422,'AST_LINK','Links must use http, https or mailto.')
                if ma.get('target') not in (None,'_blank','_self') or ma.get('class') is not None or ma.get('rel') not in (None,'noopener noreferrer nofollow','noopener noreferrer','nofollow','noopener'):
                    raise Problem(422,'AST_LINK','Unsupported link behavior.')
            elif mark.get('attrs'):
                raise Problem(422,'AST_MARK','Unexpected formatting attributes.')
        children=node.get('content',[])
        if not isinstance(children,list) or len(children)>20000:
            raise Problem(422,'AST_LIMIT','Invalid document children.')
        if kind in ('bulletList','orderedList','listItem','blockquote') and not children:
            raise Problem(422,'AST_STRUCTURE','Lists and quotations cannot be empty containers.')
        if kind=='listItem' and children and (not isinstance(children[0],dict) or children[0].get('type')!='paragraph'):
            raise Problem(422,'AST_STRUCTURE','A list item must start with a paragraph.')
        if kind=='doc' and not children:
            raise Problem(422,'AST_STRUCTURE','A chapter needs at least one block.')
        for child in children: visit(child,kind,depth+1)
    visit(ast['content'],None,0)
    if text_count>1_000_000 or len(canonical(ast).encode())>4_000_000:
        raise Problem(422,'AST_LIMIT','This chapter is too large. Split it into smaller chapters.')
    return ast


def plain_text(node: dict) -> str:
    if node['type']=='text': return node['text']
    if node['type']=='hardBreak': return '\n'
    children = [plain_text(n) for n in node.get('content',[])]
    return ('' if node['type'] in ('paragraph','heading') else '\n').join(children)
