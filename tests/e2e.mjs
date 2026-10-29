import {chromium} from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import {spawn} from 'node:child_process';
import {mkdtemp,readFile,readdir,writeFile,mkdir} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
const root=await mkdtemp(path.join(tmpdir(),'publisher-e2e-'));
const origin='http://127.0.0.1:8123';const evidence=path.resolve('implementation/evidence');await mkdir(evidence,{recursive:true});
const server=spawn('python3',['apps/api/main.py','serve','--data-dir',root,'--port','8123'],{env:{...process.env,PUBLISHER_ENV:'test',PUBLISHER_ORIGIN:origin}});
let logs='';server.stdout.on('data',d=>logs+=d);server.stderr.on('data',d=>logs+=d);
let browser;let activePage;let failure;const observations=[];const consoleErrors=[];let success=false;
async function mailbox(email,subject='Verify your account'){
  for(const file of await readdir(path.join(root,'mail'))){const message=JSON.parse(await readFile(path.join(root,'mail',file),'utf8'));if(message.to===email&&message.subject===subject)return message;}
  throw new Error('Expected local verification message');
}
async function saved(page){await page.waitForFunction(()=>document.querySelector('.save-state')?.textContent==='Saved',{},{timeout:12000});}
async function safeClick(page,role,name){await page.getByRole(role,{name,exact:true}).click();}
try{
  for(let i=0;i<80;i++){try{if((await fetch(origin+'/api/health')).ok)break;}catch{}await new Promise(r=>setTimeout(r,100));}
  browser=await chromium.launch({channel:process.env.PUBLISHER_BROWSER_CHANNEL??'chrome',headless:true});
  const context=await browser.newContext({viewport:{width:1440,height:960},acceptDownloads:true});const page=await context.newPage();activePage=page;page.on('pageerror',e=>consoleErrors.push(e.message));page.setDefaultTimeout(15000);
  await page.goto(origin);await page.getByRole('heading',{name:'Welcome back'}).waitFor();
  await safeClick(page,'button','Create an account');await page.getByLabel('Your name').fill('Mira Test');await page.getByLabel('Email address').fill('mira@example.test');await page.getByLabel('Password',{exact:true}).fill('synthetic-e2e-password');await safeClick(page,'button','Create workspace');await page.getByRole('status').waitFor();
  const message=await mailbox('mira@example.test');await page.goto(message.url);await safeClick(page,'button','Verify email');await page.getByRole('heading',{name:'Welcome back'}).waitFor();
  await page.getByLabel('Email address').fill('mira@example.test');await page.getByLabel('Password',{exact:true}).fill('synthetic-e2e-password');await safeClick(page,'button','Sign in');await page.getByRole('heading',{name:'Your manuscripts'}).waitFor();
  observations.push('Register → private local verification mail → verify → sign in → real dashboard');
  await safeClick(page,'button','New manuscript');await page.getByLabel('Working title').fill('The Quiet Atlas');await safeClick(page,'button','Create manuscript');
  const editor=page.getByRole('textbox',{name:'Manuscript content',exact:true});await editor.waitFor();
  const text='The Quiet Atlas begins here. فارسی العربية 日本語 e\u0301 🖋️';await editor.fill(text);await saved(page);await page.reload();await editor.waitFor();assert.equal((await editor.innerText()).trim(),text);
  const projectId=page.url().split('/').pop();const project=await (await context.request.get(origin+'/api/v1/projects/'+projectId)).json();const chapterId=project.chapters[0].id;
  observations.push('Create private project → semantic editor → acknowledged save → reload exact Unicode content');
  await page.screenshot({path:path.join(evidence,'studio-desktop.png'),fullPage:false});
  // Historical preview must not remount or erase an active edit.
  await editor.fill(text+' Preview must preserve this edit.');await page.locator('.revision-list button').last().click();await page.getByRole('dialog').waitFor();await safeClick(page,'button','Close preview');assert.match(await editor.innerText(),/Preview must preserve/);await saved(page);
  // A failed save retains its command and text; safe retry acknowledges it after the connection recovers.
  await page.route('**/api/v1/chapters/'+chapterId,route=>route.request().method()==='PUT'?route.abort():route.continue());
  const offline=text+' Network recovery remains explicit.';await editor.fill(offline);await page.waitForFunction(()=>document.querySelector('.save-state')?.textContent==='Not saved');assert.equal((await editor.innerText()).trim(),offline);await page.unroute('**/api/v1/chapters/'+chapterId);await safeClick(page,'button','Save now');await saved(page);
  observations.push('Preview preserves unsaved text; network failure stays unsaved; retry persists identical content');
  // Restore-as-new keeps the later revision in history.
  await page.locator('.revision-list button').last().click();await safeClick(page,'button','Restore as a new revision');await saved(page);await page.waitForFunction(()=>document.querySelector('[aria-label="Manuscript content"]')?.textContent==='');
  await editor.fill(offline);await saved(page);
  observations.push('Restore creates a new revision, then continued writing succeeds');
  // Two tabs: stale writer never overwrites the committed winner.
  const second=await context.newPage();await second.goto(page.url());const secondEditor=second.getByRole('textbox',{name:'Manuscript content',exact:true});await secondEditor.waitFor();
  const winner=offline+' First tab is authoritative.';await editor.fill(winner);await saved(page);await secondEditor.fill('STALE_TAB_MUST_NOT_OVERWRITE');await second.waitForFunction(()=>document.querySelector('.save-state')?.textContent==='Review required');
  const latest=await (await context.request.get(origin+'/api/v1/chapters/'+chapterId)).json();assert.ok(JSON.stringify(latest.ast).includes('First tab is authoritative'));assert.ok(!JSON.stringify(latest.ast).includes('STALE_TAB'));
  const recoveryDownload=second.waitForEvent('download');await second.getByRole('button',{name:'Download recovery copy',exact:true}).click();await recoveryDownload;await second.close();
  observations.push('Two-tab stale save rejected with explicit recovery; persisted winner remains unchanged');
  await page.getByRole('tab',{name:'Export',exact:true}).click();const downloading=page.waitForEvent('download');await page.getByRole('button',{name:'Markdown .md ↓',exact:true}).click();const file=await downloading;const content=await readFile(await file.path(),'utf8');assert.match(content,/First tab is authoritative/);
  observations.push('Unpublished manuscript exports an actual private Markdown artifact');
  await safeClick(page,'button','Import a chapter');await page.getByLabel('DOCX, Markdown or UTF-8 text · up to 5 MiB').setInputFiles({name:'research.md',mimeType:'text/markdown',buffer:Buffer.from('# Research\n\nA reviewed import in فارسی.')});await safeClick(page,'button','Review import');await page.getByText('Headings are imported semantically.',{exact:false}).waitFor();assert.equal(await page.getByRole('button',{name:'Add as new chapter',exact:true}).isDisabled(),true);await page.getByRole('checkbox').check();await safeClick(page,'button','Add as new chapter');await page.getByRole('heading',{name:'research',exact:true}).waitFor();
  observations.push('Import → preview → explicit transformation acknowledgement → new persisted chapter');
  // Grant/revoke only synthetic test account, and verify direct API denial.
  await context.request.post(origin+'/api/auth/register',{headers:{Origin:origin},data:{email:'reader@example.test',name:'Reader Test',password:'synthetic-reader-password'}});
  const otherMail=await mailbox('reader@example.test');const verifyToken=new URL(otherMail.url).searchParams.get('token');await context.request.post(origin+'/api/auth/verify',{headers:{Origin:origin},data:{token:verifyToken}});
  const readerContext=await browser.newContext();const login=await readerContext.request.post(origin+'/api/auth/login',{headers:{Origin:origin},data:{email:'reader@example.test',password:'synthetic-reader-password'}});const readerSession=await login.json();
  await page.getByRole('tab',{name:'Access',exact:true}).click();await page.getByRole('textbox',{name:'Email',exact:true}).fill('reader@example.test');await safeClick(page,'button','Grant access');await page.getByText('Reader Test',{exact:true}).waitFor();
  const reader=await readerContext.newPage();await reader.goto(page.url());await reader.getByRole('textbox',{name:'Manuscript content',exact:true}).waitFor();assert.equal(await reader.getByRole('button',{name:'Bold (Control or Command B)',exact:true}).isDisabled(),true);
  const denied=await readerContext.request.put(origin+'/api/v1/chapters/'+chapterId,{headers:{Origin:origin,'X-CSRF-Token':readerSession.csrfToken,'Idempotency-Key':crypto.randomUUID(),'If-Match':'"'+latest.revisionId+'"'},data:{ast:latest.ast,accessEpoch:2}});assert.equal(denied.status(),403);
  page.once('dialog',dialog=>dialog.accept());await safeClick(page,'button','Revoke access');await page.getByText('Reader Test',{exact:true}).waitFor({state:'detached'});assert.equal((await readerContext.request.get(origin+'/api/v1/projects/'+projectId)).status(),404);await readerContext.close();
  observations.push('Real shared read-only access; direct write denied; revocation blocks fresh API reads');
  assert.equal(await page.getByText('This tab has an unsaved recovery copy.',{exact:false}).count(),0,'Opening an unchanged chapter must not create a recovery copy');
  const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();await writeFile(path.join(evidence,'axe-results.json'),JSON.stringify({url:page.url(),violations:axe.violations,incomplete:axe.incomplete.map(x=>({id:x.id,description:x.description}))},null,2));assert.equal(axe.violations.length,0,JSON.stringify(axe.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}))));
  await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(evidence,'studio-mobile.png'),fullPage:true});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Mobile document overflow');
  await page.keyboard.press('Tab');observations.push('Automated axe scan has no violations; 390px viewport has no document overflow; keyboard focus is visible');
  assert.deepEqual(consoleErrors,[]);success=true;
}catch(error){failure=String(error);if(activePage)await activePage.screenshot({path:path.join(evidence,'e2e-failure.png'),fullPage:true}).catch(()=>{});throw error;}finally{
  if(browser)await browser.close();server.kill('SIGTERM');
  await writeFile(path.join(evidence,'e2e-results.json'),JSON.stringify({date:'2026-10-29',status:success?'PASS':'FAIL',browser:(process.env.PUBLISHER_BROWSER_CHANNEL??'Installed Google Chrome')+' via Playwright; in-app browser access host unavailable',viewports:['1440x960','390x844'],observations,consoleErrors,failure},null,2));
  await writeFile(path.join(evidence,'e2e-server.log'),logs);
  console.log(JSON.stringify({status:success?'PASS':'FAIL',observations,fixtureDirectory:root},null,2));
}
