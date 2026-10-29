import {createContext,useCallback,useContext,useEffect,useMemo,useState,type ReactNode} from 'react';
import {getCurrentLocale,setCurrentLocale,translate,dateAt,numberAt,chaptersAt,type LocaleInfo,type MessageParams} from './core';
export {languages,messageText,isLocaleStored,type UiMessage,type LocaleCode} from './core';
interface I18nContextValue {locale:LocaleInfo;t:(key:string,params?:MessageParams)=>string;formatNumber:(value:number,options?:Intl.NumberFormatOptions)=>string;formatDate:(value:Date|string,options?:Intl.DateTimeFormatOptions)=>string;chapterCount:(count:number)=>string;setLocale:(code:string)=>void}
const Context=createContext<I18nContextValue|null>(null);
export function LocaleProvider({children}:{children:ReactNode}){
  const [locale,update]=useState(getCurrentLocale);
  const setLocale=useCallback((code:string)=>{update(setCurrentLocale(code));},[]);
  const value=useMemo<I18nContextValue>(()=>({locale,setLocale,t:(key,params)=>translate(key,params,locale.code),formatNumber:(n,options)=>numberAt(n,locale.code,options),formatDate:(date,options)=>dateAt(date,locale.code,options),chapterCount:n=>chaptersAt(n,locale.code)}),[locale,setLocale]);
  useEffect(()=>{document.documentElement.lang=locale.code;document.documentElement.dir=locale.direction;document.title=translate('Publisher — Author Studio',{},locale.code);},[locale]);
  useEffect(()=>{
    function invalid(event:Event){const field=event.target;if(!(field instanceof HTMLInputElement||field instanceof HTMLSelectElement||field instanceof HTMLTextAreaElement))return;
      const validity=field.validity;let message='This value is not valid.';
      if(validity.valueMissing)message='This field is required.';else if(validity.typeMismatch&&field instanceof HTMLInputElement&&field.type==='email')message='Enter a valid email address.';
      else if(validity.tooShort&&(field instanceof HTMLInputElement||field instanceof HTMLTextAreaElement)){field.setCustomValidity(translate('Use at least {min} characters.',{min:field.minLength},locale.code));return;}
      else if(validity.tooLong&&(field instanceof HTMLInputElement||field instanceof HTMLTextAreaElement)){field.setCustomValidity(translate('Use no more than {max} characters.',{max:field.maxLength},locale.code));return;}
      field.setCustomValidity(translate(message,{},locale.code));
    }
    function clear(event:Event){const field=event.target;if(field instanceof HTMLInputElement||field instanceof HTMLSelectElement||field instanceof HTMLTextAreaElement)field.setCustomValidity('');}
    document.addEventListener('invalid',invalid,true);document.addEventListener('input',clear,true);document.addEventListener('change',clear,true);
    return()=>{document.removeEventListener('invalid',invalid,true);document.removeEventListener('input',clear,true);document.removeEventListener('change',clear,true);};
  },[locale]);
  return <Context.Provider value={value}>{children}</Context.Provider>;
}
export function useI18n(){const value=useContext(Context);if(!value)throw new Error('LocaleProvider is required');return value;}
