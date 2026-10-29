"""Shared, local UI catalogs. These functions never translate author content."""
from functools import lru_cache
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[3]
CATALOGS=ROOT/'packages/i18n/locales'
LANGUAGES=json.loads((ROOT/'packages/i18n/languages.json').read_text())
SUPPORTED={language['code'] for language in LANGUAGES}


def resolve_locale(value: object) -> str | None:
    if not isinstance(value,str) or len(value)>64:return None
    code=value.strip().lower().replace('_','-').split('-')[0]
    return code if code in SUPPORTED else None


def negotiate_locale(header: str | None,default: str='en') -> str:
    choices=[]
    for position,entry in enumerate((header or '').split(',')[:30]):
        parts=entry.strip().split(';');code=resolve_locale(parts[0]);quality=1.0
        for part in parts[1:]:
            if part.strip().startswith('q='):
                try:quality=float(part.strip()[2:])
                except ValueError:quality=0
        if code and 0<quality<=1:choices.append((-quality,position,code))
    return min(choices)[2] if choices else resolve_locale(default) or 'en'


@lru_cache(maxsize=16)
def catalog(locale: str) -> dict[str,str]:
    code=resolve_locale(locale) or 'en'
    return json.loads((CATALOGS/(code+'.json')).read_text())


def translate(message: str,locale: str='en',params: dict | None=None) -> str:
    entries=catalog(locale);template=entries.get(message,catalog('en').get(message,message));values=dict(params or {})
    if 'field' in values:values['field']=entries.get(str(values['field']),str(values['field']))
    separator='، ' if resolve_locale(locale) in ('ar','fa','ur') else '、' if resolve_locale(locale) in ('zh','ja') else ', '
    for key,value in list(values.items()):
        if isinstance(value,list):values[key]=separator.join(translate(str(item),locale) for item in value)
    return re.sub(r'\{([A-Za-z]\w*)\}',lambda match:str(values.get(match[1],match[0])),template)


def localize_system_message(item: dict,locale: str) -> dict:
    """Only explicit system messages; never recurse through project/manuscript strings."""
    result=dict(item)
    if isinstance(result.get('message'),str):
        key=result.get('messageKey',result['message']);params=result.get('messageParams',{})
        result['messageKey']=key;result['messageParams']=params;result['message']=translate(key,locale,params)
    if isinstance(result.get('warnings'),list):result['warnings']=[localize_system_message(warning,locale) for warning in result['warnings']]
    return result
