import {useState,type FormEvent} from 'react';
import {request,setCsrf,errorMessage} from './api';
import type {User} from './types';
import {messageText,useI18n,type UiMessage} from '../../../packages/i18n/index';
import {LanguageSwitcher} from './LanguageSwitcher';
import type {MessageParams} from '../../../packages/i18n/core';
export function Auth({onLogin}:{onLogin:(u:User)=>void}){
  const {t,locale}=useI18n();
  const route=window.location.pathname;const token=new URLSearchParams(window.location.search).get('token');
  const [mode,setMode]=useState<'login'|'register'|'recover'|'verify'|'reset'>(route==='/verify'?'verify':route==='/reset'?'reset':'login');
  const [busy,setBusy]=useState(false),[error,setError]=useState<string|UiMessage>(''),[message,setMessage]=useState<string|UiMessage>('');
  const submit=async(e:FormEvent<HTMLFormElement>)=>{e.preventDefault();setBusy(true);setError('');setMessage('');const fields=Object.fromEntries(new FormData(e.currentTarget));
    try{
      if(mode==='login'){const data=await request<{user:User;csrfToken:string}>('/auth/login',{method:'POST',body:fields});setCsrf(data.csrfToken);window.history.replaceState({},'','/app');onLogin(data.user);}
      else {const data=await request<{message:string;messageKey?:string;messageParams?:MessageParams}>('/auth/'+mode,{method:'POST',body:{...fields,...((mode==='verify'||mode==='reset')?{token}:{}),...(mode==='register'?{locale:locale.code}:{})}});setMessage(data.messageKey?{key:data.messageKey,params:data.messageParams}:data.message);if(mode==='reset'||mode==='verify'){window.history.replaceState({},'','/login');setMode('login');}}
    }catch(err){setError(errorMessage(err));}finally{setBusy(false);}
  };
  return <><div className="auth-language"><LanguageSwitcher/></div><div className="auth-layout"><section className="auth-story"><a className="wordmark" translate="no" href="/">Publisher<span className="logo-dot"/></a><div><h1>{t('Make room for your words.')}</h1><p>{t('A private writing space. A reliable history.')}<br/>{t('A manuscript that stays yours.')}</p></div><p className="auth-foot">{t('Write first. Decide where to publish later.')}</p></section><main className="auth-form-wrap" id="main-content"><div className="auth-form"><h2>{t(mode==='register'?'Begin your next chapter':mode==='recover'?'Recover your account':mode==='verify'?'Verify your email':mode==='reset'?'Choose a new password':'Welcome back')}</h2><p className="muted">{t(mode==='register'?'Create your private author workspace.':mode==='login'?'Sign in to your author studio.':'Keep your account and your manuscripts safe.')}</p>
    {error&&<div className="notice error" role="alert">{messageText(error)}</div>}{message&&<div className="notice success" role="status">{messageText(message)}</div>}
    <form onSubmit={submit}>
      {mode==='register'&&<label>{t('Your name')}<input name="name" autoComplete="name" dir="auto" required maxLength={100}/></label>}
      {['login','register','recover'].includes(mode)&&<label>{t('Email address')}<input type="email" name="email" autoComplete="email" dir="ltr" required maxLength={254}/></label>}
      {['login','register','reset'].includes(mode)&&<label>{t('Password')}<input type="password" name="password" aria-label={t('Password')} dir="ltr" aria-describedby={mode!=='login'?'password-hint':undefined} autoComplete={mode==='login'?'current-password':'new-password'} required minLength={12} maxLength={128}/>{mode!=='login'&&<span className="hint" id="password-hint">{t('12–128 characters. Use a unique password.')}</span>}</label>}
      <button className="primary full" disabled={busy||((mode==='verify'||mode==='reset')&&!token)}>{t(busy?'Please wait…':mode==='login'?'Sign in':mode==='register'?'Create workspace':mode==='recover'?'Send recovery link':mode==='verify'?'Verify email':'Update password')}</button>
    </form>
    {mode==='login'?<div className="auth-links"><button className="text-button" onClick={()=>{setMode('recover');setError('');}}>{t('Forgot password?')}</button><span>{t('New here?')} <button className="text-button" onClick={()=>{setMode('register');setError('');}}>{t('Create an account')}</button></span></div>:<button className="text-button" onClick={()=>{setMode('login');setError('');setMessage('');}}>{t('Back to sign in')}</button>}
    {(mode==='register'||mode==='recover'||message)&&<p className="local-mail">{t('This local build delivers verification and recovery messages to its private mailbox. Open it with {command}, then follow your link.',{command:'python3 apps/api/main.py mail'})}</p>}
  </div></main></div></>;
}
