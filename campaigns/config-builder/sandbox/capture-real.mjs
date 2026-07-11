import { chromium } from 'playwright-core';
import { execFileSync } from 'node:child_process';
import { mkdirSync, rmSync } from 'node:fs';
import path from 'node:path';

const EXE='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const HERE=path.resolve('.');
const fps=parseInt(process.argv[2]??'30',10);
const DUR=parseFloat(process.argv[3]??'10.5');
const framesDir=path.join(HERE,'frames','real'); rmSync(framesDir,{recursive:true,force:true}); mkdirSync(framesDir,{recursive:true});
mkdirSync(path.join(HERE,'out'),{recursive:true});

const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,t)=>a+(b-a)*t;
const seg=(t,a,b)=>clamp((t-a)/(b-a));
const eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const eo=t=>1-Math.pow(1-t,3);

const b=await chromium.launch({executablePath:EXE,args:['--no-sandbox','--force-color-profile=srgb']});
const ctx=await b.newContext({viewport:{width:540,height:960},deviceScaleFactor:2});
const page=await ctx.newPage();
await page.goto('http://localhost:3000/',{waitUntil:'networkidle',timeout:60000});
await page.waitForSelector('#specifiedRadius',{timeout:30000});
await page.waitForTimeout(1500);

// inject Craftons chrome + overlays
await page.evaluate(()=>{
  const s=document.createElement('style');
  s.textContent=`*{cursor:none!important} html,body{background:#0c0d0c!important} body{padding-top:132px!important}
   #ov-head{position:fixed;top:0;left:0;width:100%;height:132px;background:#194431;display:flex;align-items:center;justify-content:space-between;padding:0 26px;z-index:2147483000}
   #ov-head .wm{color:#fff;font-weight:700;font-size:38px;font-family:system-ui,sans-serif;letter-spacing:-.02em;position:absolute;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:12px}
   #ov-cursor{position:fixed;z-index:2147483001;width:30px;height:30px;pointer-events:none;left:0;top:0;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
   #ov-cap{position:fixed;left:5%;width:90%;bottom:56px;text-align:center;z-index:2147483001}
   #ov-cap span{display:inline-block;font-family:system-ui,sans-serif;font-weight:700;font-size:30px;color:#fff;background:rgba(12,13,12,.82);padding:12px 22px;border-radius:12px}`;
  document.head.appendChild(s);
  const h=document.createElement('div'); h.id='ov-head';
  h.innerHTML=`<svg width="30" height="30" viewBox="0 0 24 24" stroke="#fff" stroke-width="2.2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
   <div class="wm"><svg width="34" height="34" viewBox="0 0 48 48" fill="none"><path d="M24 6c-5 0-8 3-8 8 0 3 2 5 4 6-3 1-6 3-6 8 0 5 4 8 10 8" stroke="#2d8a5b" stroke-width="4.5" stroke-linecap="round"/><path d="M24 6c5 0 8 3 8 8 0 3-2 5-4 6 3 1 6 3 6 8 0 5-4 8-10 8" stroke="#2d8a5b" stroke-width="4.5" stroke-linecap="round"/></svg>Craftons</div>
   <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2"><circle cx="9" cy="20" r="1.6"/><circle cx="18" cy="20" r="1.6"/><path d="M2 3h3l2.5 13h11l2-9H6"/></svg>`;
  document.body.appendChild(h);
  const c=document.createElement('div'); c.id='ov-cursor';
  c.innerHTML=`<svg viewBox="0 0 24 24" fill="#fff" stroke="#0a0a0a" stroke-width="1.3" stroke-linejoin="round"><path d="M5 2.5l4.4 17 2.7-6.7 6.6-1.7L5 2.5z"/></svg>`;
  document.body.appendChild(c);
  const cap=document.createElement('div'); cap.id='ov-cap'; document.body.appendChild(cap);
  // helpers on window
  const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
  window.__set=(id,val)=>{const e=document.getElementById(id);if(!e)return;setter.call(e,String(val));e.dispatchEvent(new Event('input',{bubbles:true}));};
  window.__docY=(id)=>{const e=document.getElementById(id);if(!e)return 0;const r=e.getBoundingClientRect();return r.top+window.scrollY;};
  window.__rect=(id)=>{const e=document.getElementById(id);if(!e)return null;const r=e.getBoundingClientRect();return {x:r.left+r.width-30,y:r.top+r.height/2};};
  window.__cursor=(x,y,op)=>{const c=document.getElementById('ov-cursor');c.style.transform=`translate(${x}px,${y}px)`;c.style.opacity=op;};
  window.__cap=(t)=>{const c=document.getElementById('ov-cap');c.innerHTML=t?`<span>${t}</span>`:'';};
});

const yRad=await page.evaluate(()=>window.__docY('specifiedRadius'));
const yAdd=await page.evaluate(()=>window.__docY('part-quantity'));

// value + scroll timeline
const V=t=>({
  r: t<2.0? '' : Math.round(lerp(900,800,eio(seg(t,2.0,2.8)))),
  w: t<3.1? '' : Math.round(lerp(100,450,eio(seg(t,3.1,3.9)))),
  a: t<4.2? '' : Math.round(lerp(90,180,eio(seg(t,4.2,5.2)))),
});
const SCROLL=t=>{
  const toInputs=Math.max(0,yRad-360), toAdd=Math.max(0,yAdd-620);
  if(t<1.4) return 0;
  if(t<2.0) return lerp(0,toInputs,eio(seg(t,1.4,2.0)));
  if(t<5.4) return toInputs;
  if(t<6.2) return lerp(toInputs,0,eio(seg(t,5.4,6.2)));   // scroll up to curve
  if(t<7.4) return 0;
  if(t<8.2) return lerp(0,toAdd,eio(seg(t,7.4,8.2)));
  return toAdd;
};
const CUR=[{t:0,id:null,p:{x:640,y:1040}},{t:1.9,id:'specifiedRadius'},{t:3.0,id:'width'},{t:4.1,id:'angle'},{t:5.3,id:'angle'},{t:7.3,id:'angle'},{t:8.2,id:'part-quantity'}];
const CAP=[[1.4,2.0,'Choose your material.'],[2.1,2.9,'Set your radius.'],[3.2,3.9,'Set the width.'],[4.3,5.3,'Set the angle.'],[6.2,7.3,'Made to your millimetre.'],[7.6,9.2,'Add the part. Done.']];

const total=Math.round(DUR*fps);
let clickedAdd=false;
console.log(`real capture: ${total} frames @ ${fps}fps`);
for(let i=0;i<=total;i++){
  const t=i/fps;
  const v=V(t);
  await page.evaluate(([v,sc])=>{
    if(v.r!=='')window.__set('specifiedRadius',v.r); if(v.w!=='')window.__set('width',v.w); if(v.a!=='')window.__set('angle',v.a);
    window.scrollTo(0,sc);
  },[v,SCROLL(t)]);
  // cursor position (screen coords, live rect)
  const cur=CUR;
  let cpos={x:640,y:1040},op=1;
  for(let k=0;k<cur.length-1;k++){ if(t>=cur[k].t&&t<=cur[k+1].t){
    const f=eio(seg(t,cur[k].t,cur[k+1].t));
    const pa=cur[k].id?await page.evaluate(id=>window.__rect(id),cur[k].id):cur[k].p;
    const pb=cur[k+1].id?await page.evaluate(id=>window.__rect(id),cur[k+1].id):cur[k+1].p;
    if(pa&&pb){cpos={x:lerp(pa.x,pb.x,f),y:lerp(pa.y,pb.y,f)};}
    break; } }
  if(t<1.0)op=clamp(seg(t,0.6,1.0)); if(t>9.4)op=clamp(1-seg(t,9.4,9.8));
  let cap=''; for(const c of CAP) if(t>=c[0]&&t<=c[1]) cap=c[2];
  await page.evaluate(([x,y,op,cap])=>{window.__cursor(x,y,op);window.__cap(cap);},[cpos.x,cpos.y,op,cap]);
  if(t>=8.5&&!clickedAdd){ try{await page.click('button:has-text("Add Part")',{timeout:1000});}catch(e){} clickedAdd=true; }
  await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  await page.screenshot({path:path.join(framesDir,`f_${String(i).padStart(4,'0')}.png`),clip:{x:0,y:0,width:1080,height:1920}});
}
await b.close();
const out=path.join(HERE,'out','real_demo.mp4');
execFileSync('ffmpeg',['-y','-framerate',String(fps),'-i',path.join(framesDir,'f_%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',out],{stdio:'inherit'});
console.log('wrote '+out);
rmSync(framesDir,{recursive:true,force:true});
