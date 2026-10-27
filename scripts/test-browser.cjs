const {chromium}=require('playwright');
const {pathToFileURL}=require('url');
const path=require('path'),fs=require('fs'),assert=require('assert');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||require('child_process').execFileSync('which',['chromium'],{encoding:'utf8'}).trim(),headless:true,args:['--no-sandbox']});
 const results=[];
 try{
 for(const version of ['before','after']){
 const page=await browser.newPage({viewport:{width:1280,height:1000}});
 await page.goto(pathToFileURL(path.resolve(__dirname,'..',version,'index.html')).href);
 const aria=await page.locator('#searchBtn').getAttribute('aria-label');
 assert.equal(aria,version==='after'?'Поиск':null);
 const snapshot=await page.locator('#searchBtn').ariaSnapshot();
 assert(version==='after'?snapshot.includes('Поиск'):!snapshot.includes('Поиск'));
 await page.locator('#name').fill('Анна');assert.equal(await page.locator('#name').inputValue(),'Анна');
 await page.locator('#volume').fill('70');assert.equal(await page.locator('#volume').inputValue(),'70');
 await page.locator('#agree').check();assert(await page.locator('#agree').isChecked());
 await page.locator('#searchInput').fill('расписание');await page.locator('#searchBtn').click();assert((await page.locator('#status').textContent()).includes('расписание'));
 await page.locator('#openDialog').click();assert(await page.locator('#dialog').isVisible());
 if(version==='after')await page.screenshot({path:'/data/lab-dialog.png'});
 await page.locator('#closeDialog').click();assert(!(await page.locator('#dialog').isVisible()));assert.equal(await page.evaluate(()=>document.activeElement.id),'openDialog');
 const pop=page.waitForEvent('popup');await page.locator('#openWindow').click();const popup=await pop;await popup.waitForLoadState();assert.equal(await popup.title(),'Справка — ЛР 1');await popup.screenshot({path:'/data/lab-help.png'});await popup.close();
 await page.setViewportSize({width:390,height:1000});await page.screenshot({path:`/data/lab-${version}-mobile.png`,fullPage:true});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 results.push({version,checks:['DOM/ARIA name','text input','slider','checkbox','search action','dialog and focus return','separate popup','390px no horizontal overflow'],result:'PASS',buttonBrowserSnapshot:snapshot});
 await page.close();
 }
 const page=await browser.newPage({viewport:{width:1280,height:1000}});await page.goto(pathToFileURL(path.resolve(__dirname,'..','index.html')).href);await page.screenshot({path:'/data/lab-index.png'});await page.close();
 fs.writeFileSync(path.resolve(__dirname,'../docs/BROWSER-CHECKS.json'),JSON.stringify({environment:'Linux Chromium / Playwright',scope:'Browser checks only. Not Windows UIA or NVDA.',results},null,2));
 console.log(JSON.stringify(results));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
