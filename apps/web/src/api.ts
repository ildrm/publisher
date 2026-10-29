import {getCurrentLocale,isMessageKey,type MessageParams,type UiMessage} from '../../../packages/i18n/core';
export class ApiError extends Error {
  status:number;code:string;correlationId?:string;messageKey?:string;messageParams?:MessageParams;
  constructor(status:number,data:{detail?:string;code?:string;correlationId?:string;messageKey?:string;messageParams?:MessageParams}){
    super(data.messageKey??data.detail??'Request failed.');this.status=status;this.code=data.code??'NETWORK';this.correlationId=data.correlationId;this.messageKey=data.messageKey;this.messageParams=data.messageParams;
  }
}
let csrf='';export function setCsrf(value:string){csrf=value;}
export async function request<T>(path:string,options:{method?:string;body?:unknown;etag?:string;key?:string}={}):Promise<T>{
  const method=options.method??'GET';const headers:Record<string,string>={'Accept-Language':getCurrentLocale().code};
  if(method!=='GET'){headers['Content-Type']='application/json';headers['X-CSRF-Token']=csrf;headers['Idempotency-Key']=options.key??crypto.randomUUID();}
  if(options.etag)headers['If-Match']='"'+options.etag+'"';
  const result=await fetch('/api'+path,{method,headers,credentials:'same-origin',body:options.body===undefined?undefined:JSON.stringify(options.body),cache:'no-store'});
  const data=await result.json();if(!result.ok)throw new ApiError(result.status,data);return data as T;
}
export async function download(path:string,fallback='manuscript'){
  const response=await fetch('/api'+path,{headers:{'Accept-Language':getCurrentLocale().code},credentials:'same-origin',cache:'no-store'});
  if(!response.ok)throw new ApiError(response.status,await response.json());
  const blob=await response.blob();const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=response.headers.get('Content-Disposition')?.match(/filename="([^"]+)"/)?.[1]??fallback;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
export function recoveryDownload(value:unknown,name:string){const blob=new Blob([JSON.stringify(value,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name+'.recovery.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
/** Keep source descriptors in state so switching languages re-renders existing errors too. */
export function errorMessage(error:unknown):string|UiMessage {
  if(error instanceof ApiError){const key=error.messageKey??error.message;return {key:isMessageKey(key)?key:'The operation failed. Try again safely.',params:error.messageParams};}
  if(error instanceof Error&&isMessageKey(error.message))return error.message;
  return 'The operation failed. Try again safely.';
}
