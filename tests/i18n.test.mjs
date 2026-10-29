import test from 'node:test';
import assert from 'node:assert/strict';
import {languages,catalogs,initialLocale,resolveLocale,translate,numberAt,dateAt,chaptersAt,getCurrentLocale,setCurrentLocale,isLocaleStored} from '../packages/i18n/core.ts';

test('all fourteen global locales plus Persian have complete placeholder-safe catalogs',()=>{
  assert.equal(languages.length,15);const keys=Object.keys(catalogs.en).sort();
  for(const language of languages){const messages=catalogs[language.code];assert.deepEqual(Object.keys(messages).sort(),keys);for(const key of keys){assert.equal(typeof messages[key],'string');assert.ok(messages[key].trim());const source=[...catalogs.en[key].matchAll(/\{(\w+)\}/g)].map(m=>m[1]).sort();const result=[...messages[key].matchAll(/\{(\w+)\}/g)].map(m=>m[1]).sort();if(key.startsWith('chapterCount.'))assert.ok(result.every(param=>source.includes(param)));else assert.deepEqual(result,source,key);}}
});
test('language negotiation preserves explicit preference and handles regional tags safely',()=>{
  assert.equal(initialLocale('ar',['de-DE']),'ar');assert.equal(initialLocale('bad',['zh-Hans','en-US']),'zh');assert.equal(initialLocale(null,['xx']),'en');assert.equal(resolveLocale('pt-BR'),'pt');assert.equal(resolveLocale('../../private'),null);
});
test('device persistence is confirmed only when preference storage can read back the selected locale',()=>{
  const original=Object.getOwnPropertyDescriptor(globalThis,'window');const previous=getCurrentLocale().code;
  function storage(value){Object.defineProperty(globalThis,'window',{configurable:true,value:{localStorage:value}});}
  try{
    let saved=null;storage({setItem:(_key,value)=>{saved=value;},getItem:()=>saved});
    setCurrentLocale('ar');assert.equal(isLocaleStored('ar'),true);assert.equal(isLocaleStored('en'),false);
    storage({setItem:()=>{throw new Error('Storage denied');},getItem:()=>null});
    setCurrentLocale('fr');assert.equal(getCurrentLocale().code,'fr');assert.equal(isLocaleStored('fr'),false);
    storage({setItem:()=>{},getItem:()=>null});setCurrentLocale('ja');assert.equal(isLocaleStored('ja'),false);
    storage({getItem:()=>{throw new Error('Storage denied');}});assert.equal(isLocaleStored('ja'),false);
    Object.defineProperty(globalThis,'window',{configurable:true,value:undefined});assert.equal(isLocaleStored('ja'),false);
  }finally{setCurrentLocale(previous);if(original)Object.defineProperty(globalThis,'window',original);else delete globalThis.window;}
});
test('numbers dates plural forms and source message parameters use the selected locale',()=>{
  for(const language of languages){const code=language.code;assert.equal(numberAt(12345,code),new Intl.NumberFormat(language.formatLocale).format(12345));assert.equal(dateAt('2026-10-29T12:00:00Z',code,{month:'long'}),new Intl.DateTimeFormat(language.formatLocale,{month:'long'}).format(new Date('2026-10-29T12:00:00Z')));for(const n of [0,1,2,3,11,100]){const value=chaptersAt(n,code);assert.ok(!value.includes('{count}'));}}
  assert.notEqual(chaptersAt(1,'ru'),chaptersAt(5,'ru'));
  const key='{field} must contain 1–{maximum} characters.';assert.ok(translate(key,{field:'Project title',maximum:300},'fa').includes(catalogs.fa['Project title']));
});
test('warning descriptors retranslate feature lists instead of freezing prior-language prose',()=>{
  const key='Review these unsupported structures: {features}. Text is retained where readable; original source is preserved.';
  const params={features:['tables','images']};const arabic=translate(key,params,'ar'),french=translate(key,params,'fr');assert.ok(arabic.includes(catalogs.ar.tables));assert.ok(french.includes(catalogs.fr.tables));assert.ok(!french.includes(catalogs.ar.tables));assert.deepEqual(params.features,['tables','images']);
});
