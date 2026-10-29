import test from 'node:test';
import assert from 'node:assert/strict';
import {Autosave} from '../packages/editor/autosave.ts';

test('lost response retries identical body, version and key before later edits',async()=>{
  const calls=[];let n=0;let key=0;
  const saver=new Autosave({etag:'initial',key:()=>String(++key),report:()=>{},transport:async(ast,etag,key)=>{calls.push({ast,etag,key});if(++n===1)throw new Error('response lost');return {revisionId:'rev-'+n,savedAt:'synthetic'};}});
  saver.edit({text:'first'});await assert.rejects(saver.flush(),/response lost/);saver.edit({text:'later'});await saver.flush();
  assert.deepEqual(calls[0],calls[1]);assert.notEqual(calls[2].key,calls[0].key);assert.equal(calls[2].ast.text,'later');assert.equal(saver.dirty,false);
});
test('acknowledging an earlier generation never labels newer text saved',async()=>{
  let release;const first=new Promise(resolve=>{release=resolve;});let n=0;const states=[];
  const saver=new Autosave({etag:'initial',report:s=>states.push(s),transport:async()=>{if(++n===1)await first;return {revisionId:'revision-'+n,savedAt:'synthetic'};}});
  saver.edit({text:'a'});const saving=saver.flush();await Promise.resolve();saver.edit({text:'b'});release();await saving;
  assert.deepEqual(states,['unsaved','saving','unsaved','unsaved','saving','saved']);
});
test('concurrent flushes share one request; stale writes require explicit recovery',async()=>{
  let n=0;const saver=new Autosave({etag:'initial',report:()=>{},transport:async()=>{n++;throw Object.assign(new Error('stale'),{status:412});}});
  saver.edit({text:'retained'});const first=saver.flush(),second=saver.flush();assert.equal(first,second);await assert.rejects(first);await assert.rejects(saver.flush(),/Compare/);assert.equal(n,1);assert.equal(saver.dirty,true);
});
test('rejected validation can be corrected without replaying an invalid request',async()=>{
  const calls=[];const saver=new Autosave({etag:'initial',report:()=>{},transport:async(ast)=>{calls.push(ast);if(!ast.valid)throw Object.assign(new Error('invalid'),{status:422});return {revisionId:'accepted',savedAt:'synthetic'};}});
  saver.edit({valid:false});await assert.rejects(saver.flush());saver.edit({valid:true});await saver.flush();assert.deepEqual(calls,[{valid:false},{valid:true}]);
});
