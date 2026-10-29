export type SaveState = 'saved'|'unsaved'|'saving'|'not-saved'|'recovery-required';
export interface SaveReply {revisionId:string;savedAt:string}
export interface Pending<T> {generation:number;ast:T;etag:string;key:string}
/** Serializes saves and retains an identical request across uncertain-response retries. */
export class Autosave<T> {
  private transport:(ast:T,etag:string,key:string)=>Promise<SaveReply>;
  private report:(state:SaveState,result?:SaveReply)=>void;
  private key:()=>string;
  private generation=0;private savedGeneration=0;private draft:T|null=null;
  private pending:Pending<T>|null=null;private flight:Promise<void>|null=null;
  private blocked=false;
  etag:string;
  constructor(options:{etag:string;transport:(ast:T,etag:string,key:string)=>Promise<SaveReply>;report:(state:SaveState,result?:SaveReply)=>void;key?:()=>string}) {
    this.etag=options.etag;this.transport=options.transport;this.report=options.report;this.key=options.key??(()=>crypto.randomUUID());
  }
  edit(ast:T){this.draft=structuredClone(ast);this.generation++;this.report(this.blocked?'recovery-required':'unsaved');}
  get dirty(){return this.savedGeneration<this.generation;}
  flush():Promise<void>{
    if(this.blocked)return Promise.reject(new Error('Compare versions before saving again.'));
    if(this.flight)return this.flight;
    this.flight=Promise.resolve().then(()=>this.run()).finally(()=>{this.flight=null;});return this.flight;
  }
  private async run(){
    while(this.savedGeneration<this.generation){
      this.pending??={generation:this.generation,ast:structuredClone(this.draft as T),etag:this.etag,key:this.key()};
      this.report('saving');let result:SaveReply;
      try{result=await this.transport(this.pending.ast,this.pending.etag,this.pending.key);}
      catch(error){const status=(error as {status?:number}).status;if(status===422)this.pending=null;else if(status&&[401,403,404,409,412].includes(status))this.blocked=true;this.report(this.blocked?'recovery-required':'not-saved');throw error;}
      this.etag=result.revisionId;this.savedGeneration=this.pending.generation;this.pending=null;
      this.report(this.dirty?'unsaved':'saved',result);
    }
  }
}
