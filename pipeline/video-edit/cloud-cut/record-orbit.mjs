import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
const spki = readFileSync('spki.txt','utf8').trim();
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: [`--ignore-certificate-errors-spki-list=${spki}`] });
const ctx = await b.newContext({ viewport: { width: 1080, height: 1920 }, recordVideo: { dir: 'rec5', size: { width: 1080, height: 1920 } } });
const p = await ctx.newPage(); const t0 = Date.now(); const mark = (l) => console.log(`${((Date.now()-t0)/1000).toFixed(2)}s  ${l}`);
await p.goto('https://craftons-curves-calculator.vercel.app/apps/formwork', { waitUntil: 'domcontentloaded', timeout: 90000 });
await p.waitForSelector('canvas', { timeout: 120000 }); await p.waitForTimeout(4000);
await p.addStyleTag({ content: `
  #__viewer{position:fixed!important;inset:0;width:1080px;height:1920px;background:#f6f6f4;z-index:2147483000;margin:0;border-radius:0}
  #__viewer *:not(canvas):not(:has(canvas)){display:none!important}
  #__viewer canvas{width:1080px!important;height:1920px!important}
  #__wrap{position:fixed!important;left:-4000px;top:0;width:1080px;height:1920px;overflow:hidden}
  main, main *{visibility:hidden!important}` });
await p.evaluate(() => {
  let host = document.querySelector('canvas'); for (let i=0;i<3;i++) host = host.parentElement; host.id='__viewer';
  const aside = document.querySelector('aside'); const panel = aside.firstElementChild || aside;
  const wrap = document.createElement('div'); wrap.id='__wrap'; wrap.appendChild(panel); panel.id='__panel';
  document.body.appendChild(host); document.body.appendChild(wrap); window.dispatchEvent(new Event('resize')); });
await p.waitForTimeout(2500);
const setv = (sel, v) => p.evaluate(([sel,v])=>{ const el=document.querySelector(sel); const s=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set; s.call(el,v); el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true})); }, [sel,v]);
const clickText = (t) => p.evaluate((t)=>{ const el=[...document.querySelectorAll('#__panel *')].find(e=>e.children.length===0 && (e.innerText||'').trim()===t); (el.closest('label')||el.closest('button')||el).click(); }, t);
// the same configuration as the video: R1300, 600 high, angled backrest, cantilever, full formwork
await setv('#radius','1300'); await setv('#wall-height','600'); await p.waitForTimeout(800);
await clickText('Backrest'); await p.waitForTimeout(800); await setv('#backrest-taper','15'); await p.waitForTimeout(500);
await clickText('Cantilever'); await p.waitForTimeout(800); await setv('#cantilever-depth','200'); await p.waitForTimeout(500);
for (const n of ['Plates','Shutters','End Caps']) { await clickText(n); await p.waitForTimeout(700); }
await p.waitForTimeout(2000);
const zoom = async (n, dir=-1) => { await p.mouse.move(540, 960); for (let i=0;i<n;i++){ await p.mouse.wheel(0, dir*100); await p.waitForTimeout(80);} };
const orbit = async (dx, dy, steps, ms=30) => { const sx=540, sy=960; await p.mouse.move(sx,sy); await p.mouse.down(); for (let i=1;i<=steps;i++){ await p.mouse.move(sx+dx*i/steps, sy+dy*i/steps); await p.waitForTimeout(ms);} await p.mouse.up(); };
await p.screenshot({ path: 'rec5/pose0.png' }); mark('configured');
await zoom(3); await p.waitForTimeout(800); await p.screenshot({ path: 'rec5/pose1.png' }); mark('zoomed');
await orbit(0, 60, 15); await p.waitForTimeout(600); await p.screenshot({ path: 'rec5/pose2.png' }); mark('tilted down');
mark('ORBIT start'); await orbit(-700, 0, 140, 30); mark('ORBIT end');
await p.waitForTimeout(800); await p.screenshot({ path: 'rec5/pose3.png' }); mark('END');
await ctx.close(); await b.close();
