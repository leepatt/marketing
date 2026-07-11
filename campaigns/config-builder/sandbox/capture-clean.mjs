import { chromium } from 'playwright-core';
import { execFileSync } from 'node:child_process';
import { mkdirSync, rmSync, readFileSync } from 'node:fs';
import path from 'node:path';

const EXE='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const HERE=path.resolve('.');
const fps=parseInt(process.argv[2]??'30',10);
const DUR=parseFloat(process.argv[3]??'9.0');
const framesDir=path.join(HERE,'frames','clean'); rmSync(framesDir,{recursive:true,force:true}); mkdirSync(framesDir,{recursive:true});
mkdirSync(path.join(HERE,'out'),{recursive:true});
const LOGO=readFileSync(path.join(HERE,'assets','craftons_logo.png')).toString('base64');

const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,t)=>a+(b-a)*t;
const seg=(t,a,b)=>clamp((t-a)/(b-a));
const eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;

const b=await chromium.launch({executablePath:EXE,args:['--no-sandbox','--force-color-profile=srgb']});
const ctx=await b.newContext({viewport:{width:540,height:960},deviceScaleFactor:2});
const page=await ctx.newPage();
await page.goto('http://localhost:3000/',{waitUntil:'networkidle',timeout:60000});
await page.waitForSelector('#specifiedRadius',{timeout:30000});
await page.waitForTimeout(1500);

await page.evaluate((LOGO)=>{
  const s=document.createElement('style');
  s.textContent=`*{cursor:none!important} html,body{background:#0c0d0c!important} body{padding-top:78px!important}
   #ov-head{position:fixed;top:0;left:0;width:100%;height:78px;background:#194431;display:flex;align-items:center;justify-content:space-between;padding:0 22px;z-index:2147483000}
   #ov-head img{height:38px;position:absolute;left:50%;transform:translateX(-50%)}
   #ov-cursor{position:fixed;z-index:2147483040;width:26px;height:26px;pointer-events:none;left:0;top:0;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5));transform-origin:top left}
   #ov-tap{position:fixed;z-index:2147483039;width:70px;height:70px;border:4px solid #2d8a5b;border-radius:50%;opacity:0;pointer-events:none}`;
  document.head.appendChild(s);
  const h=document.createElement('div'); h.id='ov-head';
  h.innerHTML=`<svg width="26" height="26" viewBox="0 0 24 24" stroke="#fff" stroke-width="2.2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
   <img src="data:image/png;base64,${LOGO}"/>
   <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2"><circle cx="9" cy="20" r="1.6"/><circle cx="18" cy="20" r="1.6"/><path d="M2 3h3l2.5 13h11l2-9H6"/></svg>`;
  document.body.appendChild(h);
  const tap=document.createElement('div'); tap.id='ov-tap'; document.body.appendChild(tap);
  const c=document.createElement('div'); c.id='ov-cursor';
  c.innerHTML=`<svg viewBox="0 0 24 24" fill="#fff" stroke="#0a0a0a" stroke-width="1.3" stroke-linejoin="round"><path d="M5 2.5l4.4 17 2.7-6.7 6.6-1.7L5 2.5z"/></svg>`;
  document.body.appendChild(c);
  const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
  window.__set=(id,val)=>{const e=document.getElementById(id);if(!e)return;setter.call(e,String(val));e.dispatchEvent(new Event('input',{bubbles:true}));};
  window.__docY=(id)=>{const e=document.getElementById(id);if(!e)return 0;const r=e.getBoundingClientRect();return r.top+window.scrollY;};
  window.__rect=(id)=>{const e=document.getElementById(id);if(!e)return null;const r=e.getBoundingClientRect();return {x:r.left+r.width-34,y:r.top+r.height/2};};
  window.__frame=(o)=>{const c=document.getElementById('ov-cursor');c.style.transform=`translate(${o.cx}px,${o.cy}px)`;c.style.opacity=o.cop;
    const t=document.getElementById('ov-tap');t.style.opacity=o.top;t.style.left=(o.tx-35)+'px';t.style.top=(o.ty-35)+'px';t.style.transform=`scale(${o.ts})`;};
}, LOGO);

const yRad=await page.evaluate(()=>window.__docY('specifiedRadius'));
const yAdd=await page.evaluate(()=>window.__docY('part-quantity'));

const V=t=>({r:t<1.6?'':Math.round(lerp(900,800,eio(seg(t,1.6,2.3)))), w:t<2.6?'':Math.round(lerp(100,450,eio(seg(t,2.6,3.3)))), a:t<3.6?'':Math.round(lerp(90,180,eio(seg(t,3.6,4.5))))});
const SCROLL=t=>{const toI=Math.max(0,yRad-360),toA=Math.max(0,yAdd-620);
  if(t<0.9)return 0; if(t<1.5)return lerp(0,toI,eio(seg(t,0.9,1.5)));
  if(t<4.7)return toI; if(t<5.4)return lerp(toI,0,eio(seg(t,4.7,5.4)));
  if(t<6.3)return 0; if(t<7.0)return lerp(0,toA,eio(seg(t,6.3,7.0))); return toA;};
const CUR=[{t:0,p:{x:620,y:500}},{t:1.5,id:'specifiedRadius'},{t:2.5,id:'width'},{t:3.5,id:'angle'},{t:4.6,id:'angle'},{t:6.4,id:'angle'},{t:7.0,id:'part-quantity'}];

const total=Math.round(DUR*fps); let clicked=false;
console.log(`clean capture: ${total} frames @ ${fps}fps`);
for(let i=0;i<=total;i++){
  const t=i/fps, v=V(t);
  await page.evaluate(([v,sc])=>{ if(v.r!=='')window.__set('specifiedRadius',v.r); if(v.w!=='')window.__set('width',v.w); if(v.a!=='')window.__set('angle',v.a); window.scrollTo(0,sc); },[v,SCROLL(t)]);
  let cp={x:620,y:500};
  for(let k=0;k<CUR.length-1;k++) if(t>=CUR[k].t&&t<=CUR[k+1].t){ const f=eio(seg(t,CUR[k].t,CUR[k+1].t));
    const pa=CUR[k].id?await page.evaluate(id=>window.__rect(id),CUR[k].id):CUR[k].p;
    const pb=CUR[k+1].id?await page.evaluate(id=>window.__rect(id),CUR[k+1].id):CUR[k+1].p;
    if(pa&&pb)cp={x:lerp(pa.x,pb.x,f),y:lerp(pa.y,pb.y,f)}; break; }
  const tc=7.1;
  const tgi=(t>6.6)?(await page.evaluate(()=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim().startsWith('Add Part')||x.textContent.trim().startsWith('Add Another'));if(!b)return null;const r=b.getBoundingClientRect();return{x:r.left+r.width/2,y:r.top+r.height/2};})):null;
  const tt=tgi||{x:400,y:900};
  const tapG=(t>=tc&&t<tc+0.5)?Math.sin(seg(t,tc,tc+0.5)*Math.PI):0;
  await page.evaluate(o=>window.__frame(o),{cx:cp.x,cy:cp.y,cop:1,top:tapG,tx:tt.x,ty:tt.y,ts:lerp(0.4,1.3,seg(t,tc,tc+0.5))});
  if(t>=7.15&&!clicked){ try{await page.click('button:has-text("Add Part")',{timeout:800});}catch(e){} clicked=true; }
  await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  await page.screenshot({path:path.join(framesDir,`f_${String(i).padStart(4,'0')}.png`),clip:{x:0,y:0,width:1080,height:1920}});
}
await b.close();
const out=path.join(HERE,'out','clean_demo.mp4');
execFileSync('ffmpeg',['-y','-framerate',String(fps),'-i',path.join(framesDir,'f_%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',out],{stdio:'inherit'});
console.log('wrote '+out);
rmSync(framesDir,{recursive:true,force:true});
