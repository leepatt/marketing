import { chromium } from 'playwright-core';
import { execFileSync } from 'node:child_process';
import { mkdirSync, rmSync, readFileSync } from 'node:fs';
import path from 'node:path';

const EXE='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const HERE=path.resolve('.');
const fps=parseInt(process.argv[2]??'30',10);
const DUR=parseFloat(process.argv[3]??'11.5');
const framesDir=path.join(HERE,'frames','real'); rmSync(framesDir,{recursive:true,force:true}); mkdirSync(framesDir,{recursive:true});
mkdirSync(path.join(HERE,'out'),{recursive:true});
const b64=f=>readFileSync(path.join(HERE,'fonts',f)).toString('base64');
const SG7=b64('sg-700.woff2'), SG5=b64('sg-500.woff2');

const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,t)=>a+(b-a)*t;
const seg=(t,a,b)=>clamp((t-a)/(b-a));
const eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const eo=t=>1-Math.pow(1-t,3);
const eob=t=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2);};

const b=await chromium.launch({executablePath:EXE,args:['--no-sandbox','--force-color-profile=srgb']});
const ctx=await b.newContext({viewport:{width:540,height:960},deviceScaleFactor:2});
const page=await ctx.newPage();
await page.goto('http://localhost:3000/',{waitUntil:'networkidle',timeout:60000});
await page.waitForSelector('#specifiedRadius',{timeout:30000});
await page.waitForTimeout(1500);

await page.evaluate(({SG7,SG5})=>{
  const s=document.createElement('style');
  s.textContent=`
   @font-face{font-family:'SG';font-weight:700;src:url(data:font/woff2;base64,${SG7}) format('woff2')}
   @font-face{font-family:'SG';font-weight:500;src:url(data:font/woff2;base64,${SG5}) format('woff2')}
   *{cursor:none!important} html,body{background:#0c0d0c!important} body{padding-top:150px!important}
   #ov-head{position:fixed;top:0;left:0;width:100%;height:150px;background:#194431;display:flex;align-items:center;justify-content:space-between;padding:0 30px;z-index:2147483000}
   #ov-head .wm{color:#fff;font-weight:700;font-size:44px;font-family:'SG',sans-serif;letter-spacing:-.02em;position:absolute;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:14px}
   #ov-cursor{position:fixed;z-index:2147483040;width:34px;height:34px;pointer-events:none;left:0;top:0;filter:drop-shadow(0 2px 4px rgba(0,0,0,.55));transform-origin:top left}
   #ov-tap{position:fixed;z-index:2147483039;width:90px;height:90px;border:5px solid #2d8a5b;border-radius:50%;opacity:0;pointer-events:none}
   #ov-cap{position:fixed;left:5%;width:90%;bottom:64px;text-align:center;z-index:2147483041}
   #ov-cap span{display:inline-block;font-family:'SG',sans-serif;font-weight:700;font-size:36px;color:#fff;background:rgba(12,13,12,.85);padding:14px 26px;border-radius:14px;letter-spacing:-.01em}
   .ov-cover{position:fixed;inset:0;z-index:2147483050;background:#194431;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-family:'SG',sans-serif}
   #ov-hook .eb{color:#7fdcab;font-weight:500;font-size:30px;letter-spacing:.2em;text-transform:uppercase;margin-bottom:26px;display:flex;align-items:center;gap:14px}
   #ov-hook .eb i{width:12px;height:12px;border-radius:50%;background:#2d8a5b;display:block}
   #ov-hook h1{color:#fff;font-weight:700;font-size:82px;line-height:1.02;letter-spacing:-.03em;max-width:80%}
   #ov-hook h1 em{font-style:normal;color:#7fdcab}
   #ov-cta .wm{color:#fff;font-weight:700;font-size:96px;letter-spacing:-.03em;margin-top:30px}
   #ov-cta .cta{color:#7fdcab;font-weight:500;font-size:34px;margin-top:22px;font-family:'SG'}`;
  document.head.appendChild(s);
  const clover=`<svg width="var(--sz)" height="var(--sz)" viewBox="0 0 48 48" fill="none"><path d="M24 6c-5 0-8 3-8 8 0 3 2 5 4 6-3 1-6 3-6 8 0 5 4 8 10 8" stroke="#2d8a5b" stroke-width="4.5" stroke-linecap="round"/><path d="M24 6c5 0 8 3 8 8 0 3-2 5-4 6 3 1 6 3 6 8 0 5-4 8-10 8" stroke="#2d8a5b" stroke-width="4.5" stroke-linecap="round"/></svg>`;
  const h=document.createElement('div'); h.id='ov-head';
  h.innerHTML=`<svg width="32" height="32" viewBox="0 0 24 24" stroke="#fff" stroke-width="2.2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
   <div class="wm">${clover.replace('var(--sz)','38').replace('var(--sz)','38')}Craftons</div>
   <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2"><circle cx="9" cy="20" r="1.6"/><circle cx="18" cy="20" r="1.6"/><path d="M2 3h3l2.5 13h11l2-9H6"/></svg>`;
  document.body.appendChild(h);
  const tap=document.createElement('div'); tap.id='ov-tap'; document.body.appendChild(tap);
  const c=document.createElement('div'); c.id='ov-cursor';
  c.innerHTML=`<svg viewBox="0 0 24 24" fill="#fff" stroke="#0a0a0a" stroke-width="1.3" stroke-linejoin="round"><path d="M5 2.5l4.4 17 2.7-6.7 6.6-1.7L5 2.5z"/></svg>`;
  document.body.appendChild(c);
  const cap=document.createElement('div'); cap.id='ov-cap'; document.body.appendChild(cap);
  const hook=document.createElement('div'); hook.className='ov-cover'; hook.id='ov-hook';
  hook.innerHTML=`<div class="eb"><i></i>Radius Pro · Online</div><h1>Design custom curves. <em>Online.</em></h1>`;
  document.body.appendChild(hook);
  const cta=document.createElement('div'); cta.className='ov-cover'; cta.id='ov-cta'; cta.style.opacity='0';
  cta.innerHTML=`<div style="width:150px;height:150px">${clover.replace(/var\(--sz\)/g,'150')}</div><div class="wm">Craftons</div><div class="cta">Configure yours · craftons.com.au</div>`;
  document.body.appendChild(cta);
  const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
  window.__set=(id,val)=>{const e=document.getElementById(id);if(!e)return;setter.call(e,String(val));e.dispatchEvent(new Event('input',{bubbles:true}));};
  window.__docY=(id)=>{const e=document.getElementById(id);if(!e)return 0;const r=e.getBoundingClientRect();return r.top+window.scrollY;};
  window.__rect=(id)=>{const e=document.getElementById(id);if(!e)return null;const r=e.getBoundingClientRect();return {x:r.left+r.width-34,y:r.top+r.height/2};};
  window.__frame=(o)=>{
    const c=document.getElementById('ov-cursor');c.style.transform=`translate(${o.cx}px,${o.cy}px) scale(${o.cs})`;c.style.opacity=o.cop;
    document.getElementById('ov-cap').innerHTML=o.cap?`<span>${o.cap}</span>`:'';
    const tp=document.getElementById('ov-tap');tp.style.opacity=o.top;tp.style.left=(o.tx-45)+'px';tp.style.top=(o.ty-45)+'px';tp.style.transform=`scale(${o.ts})`;
    document.getElementById('ov-hook').style.opacity=o.hook; document.getElementById('ov-hook').style.pointerEvents='none';
    document.getElementById('ov-cta').style.opacity=o.cta;
  };
}, {SG7, SG5});

const yRad=await page.evaluate(()=>window.__docY('specifiedRadius'));
const yAdd=await page.evaluate(()=>window.__docY('part-quantity'));

const V=t=>({r: t<2.4?'':Math.round(lerp(900,800,eio(seg(t,2.4,3.2)))), w: t<3.5?'':Math.round(lerp(100,450,eio(seg(t,3.5,4.3)))), a: t<4.6?'':Math.round(lerp(90,180,eio(seg(t,4.6,5.6))))});
const SCROLL=t=>{const toI=Math.max(0,yRad-360),toA=Math.max(0,yAdd-620);
  if(t<1.8)return 0; if(t<2.4)return lerp(0,toI,eio(seg(t,1.8,2.4)));
  if(t<5.8)return toI; if(t<6.6)return lerp(toI,0,eio(seg(t,5.8,6.6)));
  if(t<7.7)return 0; if(t<8.5)return lerp(0,toA,eio(seg(t,7.7,8.5))); return toA;};
const CUR=[{t:0,p:{x:640,y:1040}},{t:2.2,id:'specifiedRadius'},{t:3.4,id:'width'},{t:4.5,id:'angle'},{t:5.7,id:'angle'},{t:7.6,id:'angle'},{t:8.5,id:'part-quantity'}];
const CAP=[[1.9,2.4,'Choose your material.'],[2.5,3.3,'Set your radius.'],[3.6,4.4,'Set the width.'],[4.7,5.7,'Set the angle.'],[6.6,7.6,'Made to your millimetre.'],[8.0,9.3,'Add the part. Done.']];

const total=Math.round(DUR*fps); let clicked=false;
console.log(`real reel: ${total} frames @ ${fps}fps`);
for(let i=0;i<=total;i++){
  const t=i/fps, v=V(t);
  await page.evaluate(([v,sc])=>{ if(v.r!=='')window.__set('specifiedRadius',v.r); if(v.w!=='')window.__set('width',v.w); if(v.a!=='')window.__set('angle',v.a); window.scrollTo(0,sc); },[v,SCROLL(t)]);
  // cursor
  let cp={x:640,y:1040};
  for(let k=0;k<CUR.length-1;k++) if(t>=CUR[k].t&&t<=CUR[k+1].t){ const f=eio(seg(t,CUR[k].t,CUR[k+1].t));
    const pa=CUR[k].id?await page.evaluate(id=>window.__rect(id),CUR[k].id):CUR[k].p;
    const pb=CUR[k+1].id?await page.evaluate(id=>window.__rect(id),CUR[k+1].id):CUR[k+1].p;
    if(pa&&pb)cp={x:lerp(pa.x,pb.x,f),y:lerp(pa.y,pb.y,f)}; break; }
  let cop=1; if(t<1.9)cop=0; if(t>9.2)cop=clamp(1-seg(t,9.2,9.5));
  const press = (Math.abs(t-8.7)<0.15)?0.82:1;
  let cap=''; for(const c of CAP) if(t>=c[0]&&t<=c[1]) cap=c[2];
  const tc=8.65, tg=await page.evaluate(id=>window.__rect(id),'part-quantity')||{x:400,y:900};
  const tgi=(t>7.9)? (await page.evaluate(()=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim().startsWith('Add Part')||x.textContent.trim().startsWith('Add Another'));if(!b)return null;const r=b.getBoundingClientRect();return{x:r.left+r.width/2,y:r.top+r.height/2};})):null;
  const tt=tgi||tg;
  const tapG=(t>=tc&&t<tc+0.5)?Math.sin(seg(t,tc,tc+0.5)*Math.PI):0;
  const hook = t<1.1?1: (t<1.7?1-eio(seg(t,1.1,1.7)):0);
  const cta = t<9.4?0: eio(seg(t,9.4,10.1));
  await page.evaluate(o=>window.__frame(o),{cx:cp.x,cy:cp.y,cs:press,cop, cap, top:tapG, tx:tt.x, ty:tt.y, ts:lerp(0.4,1.35,seg(t,tc,tc+0.5)), hook, cta});
  if(t>=8.55&&!clicked){ try{await page.click('button:has-text("Add Part")',{timeout:800});}catch(e){} clicked=true; }
  await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  await page.screenshot({path:path.join(framesDir,`f_${String(i).padStart(4,'0')}.png`),clip:{x:0,y:0,width:1080,height:1920}});
}
await b.close();
const out=path.join(HERE,'out','real_reel.mp4');
execFileSync('ffmpeg',['-y','-framerate',String(fps),'-i',path.join(framesDir,'f_%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',out],{stdio:'inherit'});
console.log('wrote '+out);
rmSync(framesDir,{recursive:true,force:true});
