import test from 'node:test';
import assert from 'node:assert/strict';
import { AutosaveController } from '../frontend-autosave.mjs';

test('lost response retries identical body/key before sending a newer draft', async () => {
  const calls = []; let attempts = 0; let keys = 0;
  const c = new AutosaveController({etag:'"base"', keyFactory:()=>`key-${++keys}`,
    transport: async (ast, headers) => {
      calls.push([structuredClone(ast), {...headers}]);
      if (++attempts === 1) throw new Error('response lost after commit');
      return {etag:`"rev-${attempts}"`, revisionId:`rev-${attempts}`};
    }});
  c.edit({text:'first'});
  await assert.rejects(c.flush(), /response lost/);
  c.edit({text:'second'});
  await c.flush();
  assert.deepEqual(calls[0], calls[1]);
  assert.equal(calls[2][0].text, 'second');
  assert.notEqual(calls[2][1].idempotencyKey,calls[0][1].idempotencyKey);
  assert.equal(c.state,'saved');
});

test('in-flight edit is not marked saved by an older acknowledgement', async () => {
  const states=[]; let release; let n=0;
  const first = new Promise(resolve=>{release=resolve;});
  const c=new AutosaveController({etag:'"base"',keyFactory:()=>`k-${++n}`,onState:s=>states.push(s),
    transport:async()=>{ if(n===1) await first; return {etag:`"r${n}"`,revisionId:`r${n}`}; }});
  c.edit({text:'a'}); const flight=c.flush(); await Promise.resolve();
  c.edit({text:'b'}); release(); await flight;
  assert.deepEqual(states,['unsaved','saving','unsaved','unsaved','saving','saved']);
});

test('stale version stops automatic retry and preserves draft for manual recovery',async()=>{
  let count=0;
  const c=new AutosaveController({etag:'"stale"',keyFactory:()=> 'k',transport:async()=>{
    count++; throw Object.assign(new Error('stale'),{status:412});
  }});
  c.edit({text:'recover me'});
  await assert.rejects(c.flush(), /stale/);
  await assert.rejects(c.flush(), /Manual recovery/);
  assert.equal(count,1); assert.equal(c.draft.text,'recover me');
  assert.equal(c.state,'recovery-required');
});
