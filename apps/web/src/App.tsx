import {lazy,Suspense,useCallback,useEffect,useRef,useState} from 'react';
import {ApiError,request,setCsrf,errorMessage} from './api';
import type {User} from './types';
import {Auth} from './Auth';
import {Dashboard} from './Dashboard';
import {LanguageSwitcher} from './LanguageSwitcher';
import {messageText,isLocaleStored,useI18n,type UiMessage} from '../../../packages/i18n/index';
const Studio=lazy(()=>import('./Studio').then(module=>({default:module.Studio})));
export default function App(){
  const {t,setLocale}=useI18n();
  const [user,setUser]=useState<User|null>(null),[ready,setReady]=useState(false),[dirty,setDirty]=useState(false),[message,setMessage]=useState<string|UiMessage>('');
  const userRef=useRef(user);userRef.current=user;
  const preferenceQueue=useRef<Promise<void>>(Promise.resolve());
  const latestPreference=useRef(0);
  const [projectId,setProjectId]=useState<string|null>(()=>window.location.pathname.match(/^\/app\/projects\/([a-f0-9-]{36})$/)?.[1]??null);
  const applyUser=useCallback((next:User)=>{setUser(next);if(next.locale)setLocale(next.locale);},[setLocale]);
  useEffect(()=>{request<{user:User;csrfToken:string}>('/session').then(data=>{applyUser(data.user);setCsrf(data.csrfToken);}).catch(error=>{if(!(error instanceof ApiError&&error.status===401))setMessage('Could not connect to your studio. Check the connection before signing in.');}).finally(()=>setReady(true));},[applyUser]);
  useEffect(()=>{const pop=()=>{if(dirty){window.history.pushState({},'','/app/projects/'+projectId);setMessage('Save or download a recovery copy before leaving this manuscript.');return;}setProjectId(window.location.pathname.match(/^\/app\/projects\/([a-f0-9-]{36})$/)?.[1]??null);};window.addEventListener('popstate',pop);return()=>window.removeEventListener('popstate',pop);},[dirty,projectId]);
  const open=useCallback((id:string)=>{window.history.pushState({},'','/app/projects/'+id);setProjectId(id);},[]);
  const home=useCallback(()=>{window.history.pushState({},'','/app');setProjectId(null);setDirty(false);},[]);
  function saveLanguage(code:string){
    const actor=userRef.current?.id;if(!actor)return;const version=++latestPreference.current;
    preferenceQueue.current=preferenceQueue.current.catch(()=>{}).then(async()=>{if(userRef.current?.id!==actor)return;try{const result=await request<{user:User}>('/preferences',{method:'PUT',body:{locale:code}});if(userRef.current?.id===actor)setUser(result.user);}catch{if(userRef.current?.id===actor&&version===latestPreference.current)setMessage(isLocaleStored(code)?'Your language is saved on this device. Account synchronization failed; try again.':'Your request could not be completed. Keep unsaved changes and try again.');}});
  }
  async function logout(){try{await preferenceQueue.current;await request('/auth/logout',{method:'POST'});setCsrf('');setUser(null);setProjectId(null);window.history.replaceState({},'','/login');}catch(error){setMessage(errorMessage(error));}}
  if(!ready)return <main className="loading"><p role="status">{t('Opening your studio…')}</p></main>;
  if(!user)return <>{message&&<div className="notice warning" role="alert">{messageText(message)}</div>}<Auth onLogin={applyUser}/></>;
  return <><a className="skip-link" href="#main-content">{t('Skip to main content')}</a><header className="app-header"><button className="wordmark text-button" translate="no" onClick={()=>{if(dirty){setMessage('Save or download a recovery copy before leaving.');return;}home();}}>Publisher<span className="logo-dot"/></button><span className="app-section">{t('Author Studio')}</span><LanguageSwitcher onSelect={saveLanguage}/><div className="account-menu"><span className="avatar" aria-hidden="true">{Array.from(user.name)[0]?.toLocaleUpperCase()}</span><bdi className="account-name" translate="no">{user.name}</bdi><button className="text-button" disabled={dirty} title={t(dirty?'Save or recover changes before signing out':'Sign out')} onClick={logout}>{t('Sign out')}</button></div></header>{message&&<div className="notice warning" role="status">{messageText(message)}<button className="text-button" onClick={()=>setMessage('')}>{t('Dismiss')}</button></div>}{projectId?<Suspense fallback={<main className="loading" role="status">{t('Opening editor…')}</main>}><Studio key={projectId} id={projectId} user={user} back={home} onDirty={setDirty}/></Suspense>:<Dashboard user={user} open={open}/>}</>;
}
