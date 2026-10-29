import {languages,useI18n} from '../../../packages/i18n/index';
/** Selection changes interface chrome only; document metadata and editor state are untouched. */
export function LanguageSwitcher({onSelect}:{onSelect?:(code:string)=>void}){
  const {locale,t,setLocale}=useI18n();
  return <div className="language-switcher"><label><span className="language-switcher-label">{t('Interface language')}</span><select aria-label={t('Interface language')} title={t('Interface language is independent of manuscript language.')} value={locale.code} onChange={event=>{setLocale(event.target.value);onSelect?.(event.target.value);}}>{languages.map(language=><option key={language.code} value={language.code} lang={language.code} dir="auto">{language.nativeName}{language.code==='en'?'':' — '+language.englishName}</option>)}</select></label></div>;
}
