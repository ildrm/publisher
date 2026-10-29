/** Locale data never changes or translates manuscript content. No network translation services. */
import metadata from './languages.json' with {type:'json'};
import en from './locales/en.json' with {type:'json'};
import zh from './locales/zh.json' with {type:'json'};
import hi from './locales/hi.json' with {type:'json'};
import es from './locales/es.json' with {type:'json'};
import ar from './locales/ar.json' with {type:'json'};
import fr from './locales/fr.json' with {type:'json'};
import bn from './locales/bn.json' with {type:'json'};
import pt from './locales/pt.json' with {type:'json'};
import id from './locales/id.json' with {type:'json'};
import ur from './locales/ur.json' with {type:'json'};
import ru from './locales/ru.json' with {type:'json'};
import de from './locales/de.json' with {type:'json'};
import ja from './locales/ja.json' with {type:'json'};
import pcm from './locales/pcm.json' with {type:'json'};
import fa from './locales/fa.json' with {type:'json'};
export type LocaleCode='en'|'zh'|'hi'|'es'|'ar'|'fr'|'bn'|'pt'|'id'|'ur'|'ru'|'de'|'ja'|'pcm'|'fa';
export interface LocaleInfo {code:LocaleCode;nativeName:string;englishName:string;direction:'ltr'|'rtl';formatLocale:string}
export type MessageParams=Record<string,string|number|string[]>;
export interface UiMessage {key:string;params?:MessageParams}
export const languages=metadata as LocaleInfo[];
export const catalogs:Record<LocaleCode,Record<string,string>>={en,zh,hi,es,ar,fr,bn,pt,id,ur,ru,de,ja,pcm,fa};
export const preferenceStorageKey='publisher.ui.locale';
export function resolveLocale(value:unknown):LocaleCode|null {
  if(typeof value!=='string'||value.length>64)return null;
  const first=value.trim().toLowerCase().replaceAll('_','-').split('-')[0];
  return languages.some(language=>language.code===first)?first as LocaleCode:null;
}
export function initialLocale(storage:unknown,browserLanguages:readonly string[]=[]):LocaleCode {
  const saved=resolveLocale(storage);if(saved)return saved;
  for(const language of browserLanguages){const found=resolveLocale(language);if(found)return found;}
  return 'en';
}
function browserLocale():LocaleCode {
  if(typeof location!=='undefined'){const linked=resolveLocale(new URLSearchParams(location.search).get('lang'));if(linked)return linked;}
  let stored:unknown;
  try{if(typeof window!=='undefined')stored=window.localStorage.getItem(preferenceStorageKey);}catch{/* Preference storage is optional; never blocks authoring. */}
  return initialLocale(stored,typeof navigator==='undefined'?[]:navigator.languages);
}
let current:LocaleCode=browserLocale();
export function getCurrentLocale():LocaleInfo{return languages.find(language=>language.code===current)!;}
export function setCurrentLocale(value:string):LocaleInfo {
  const code=resolveLocale(value);if(!code)throw new RangeError('Unsupported interface language');current=code;
  try{if(typeof window!=='undefined')window.localStorage.setItem(preferenceStorageKey,code);}catch{/* In-memory selection still works. */}
  return getCurrentLocale();
}
/** Confirm the preference survived storage; an in-memory change alone is not persistence. */
export function isLocaleStored(value:string):boolean {
  const code=resolveLocale(value);if(!code)return false;
  try{return typeof window!=='undefined'&&window.localStorage.getItem(preferenceStorageKey)===code;}catch{return false;}
}
export function isMessageKey(value:string):boolean{return Object.hasOwn(en,value);}
export function translate(key:string,params:MessageParams={},code:LocaleCode=current):string {
  const template=catalogs[code][key]??catalogs.en[key]??key;
  const locale=languages.find(item=>item.code===code)!;
  return template.replace(/\{([A-Za-z]\w*)\}/g,(placeholder,name)=>{
    const value=params[name];if(Array.isArray(value))return new Intl.ListFormat(locale.formatLocale,{style:'long',type:'conjunction'}).format(value.map(item=>isMessageKey(item)?translate(item,{},code):item));return value===undefined?placeholder:typeof value==='number'?new Intl.NumberFormat(locale.formatLocale).format(value):name==='field'&&isMessageKey(String(value))?translate(String(value),{},code):String(value);
  });
}
export function messageText(message:string|UiMessage,code:LocaleCode=current):string{return typeof message==='string'?translate(message,{},code):translate(message.key,message.params??{},code);}
export function numberAt(value:number,code:LocaleCode=current,options?:Intl.NumberFormatOptions):string{return new Intl.NumberFormat(languages.find(item=>item.code===code)!.formatLocale,options).format(value);}
export function dateAt(value:Date|string,code:LocaleCode=current,options: Intl.DateTimeFormatOptions={month:'short',day:'numeric'}):string{return new Intl.DateTimeFormat(languages.find(item=>item.code===code)!.formatLocale,options).format(typeof value==='string'?new Date(value):value);}
export function chaptersAt(count:number,code:LocaleCode=current):string {
  const locale=languages.find(item=>item.code===code)!;const category=new Intl.PluralRules(locale.formatLocale).select(count);
  return translate('chapterCount.'+category,{count},code);
}
