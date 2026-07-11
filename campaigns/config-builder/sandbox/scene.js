/* Deterministic config-demo scene. Every frame = pure function of t (seconds). */
const DUR = 10.0;
const DIMS = { r:800, w:450, ang:180, mat:'Formply 17mm' };
const priceOf = (r,w,a)=>Math.max(45,(Math.PI*r*a/180)/1000*92 + (w/100)*6);
const PRICE = priceOf(DIMS.r,DIMS.w,DIMS.ang); // 258.22

/* ---- variants ---- */
const V = {
  0:{name:'base-paper',   theme:'paper', chrome:true,  fill:'wood', zoom:'med',    motif:true,  capCard:true,  pace:1.0, skew:0},
  1:{name:'dark-mode',    theme:'dark',  chrome:true,  fill:'wood', zoom:'med',    motif:true,  capCard:true,  pace:1.0, skew:0},
  2:{name:'green-ground', theme:'green', chrome:true,  fill:'green',zoom:'med',    motif:true,  capCard:true,  pace:1.0, skew:0},
  3:{name:'bare-card',    theme:'paper', chrome:false, fill:'wood', zoom:'strong', motif:true,  capCard:true,  pace:1.0, skew:0},
  4:{name:'punch-dark',   theme:'dark',  chrome:true,  fill:'ink',  zoom:'strong', motif:false, capCard:true,  pace:1.0, skew:0},
  5:{name:'minimal',      theme:'paper', chrome:true,  fill:'wood', zoom:'subtle', motif:false, capCard:false, pace:1.0, skew:0},
  6:{name:'fast-green',   theme:'green', chrome:true,  fill:'green',zoom:'med',    motif:true,  capCard:true,  pace:0.82,skew:0},
  7:{name:'measured',     theme:'paper', chrome:true,  fill:'wood', zoom:'med',    motif:true,  capCard:true,  pace:1.25,skew:0},
  8:{name:'iso-dark',     theme:'dark',  chrome:true,  fill:'wood', zoom:'med',    motif:true,  capCard:true,  pace:1.0, skew:14},
  9:{name:'hero-preview', theme:'paper', chrome:true,  fill:'wood', zoom:'preview',motif:true,  capCard:true,  pace:1.0, skew:0},
};
const vid = parseInt(new URLSearchParams(location.search).get('v')||'0',10);
const cfg = V[vid]||V[0];

/* ---- easing ---- */
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,t)=>a+(b-a)*t;
const seg=(t,a,b)=>clamp((t-a)/(b-a));           // 0..1 across [a,b]
const easeInOut=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const easeOut=t=>1-Math.pow(1-t,3);
const easeOutBack=t=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2);};
const P=cfg.pace;                                 // pace multiplier
const T=(x)=>x*P;                                 // scale a base time by pace

/* ---- theme ---- */
const el=id=>document.getElementById(id);
const bg=el('bg'), stage=el('stage'), card=el('card');
function theme(){
  const ground = cfg.theme==='dark'?'#0e0e0c':cfg.theme==='green'?'#194431':'#f4f1ea';
  document.body.style.background=ground; document.getElementById('viewport').style.background=ground;
  bg.style.background=ground;
  if(cfg.theme!=='paper'){ el('hl').style.color='#fff'; }
  if(cfg.theme!=='paper'){ el('eyebrow').style.color='#e7efe9'; }
  else { el('hl').style.color='#0e0e0c'; el('eyebrow').style.color='#194431'; }
  if(!cfg.chrome){ el('chrome').style.display='none'; }
  if(!cfg.capCard){ /* plain caption: no card bg */ }
  if(cfg.skew){ el('preview').style.transform=`perspective(900px) rotateX(${cfg.skew}deg) rotateZ(-6deg)`; }
}

/* ---- motif (concentric curved strokes) ---- */
function motif(){
  if(!cfg.motif) return;
  const c = cfg.theme==='paper' ? 'rgba(45,138,91,.16)' : 'rgba(45,138,91,.30)';
  const mk=(cls,x,y,rot)=>{
    let s=`<svg class="motif ${cls}" width="1400" height="1400" viewBox="0 0 1400 1400" style="left:${x}px;top:${y}px;transform:rotate(${rot}deg)">`;
    for(let i=0;i<7;i++){const rr=300+i*90;s+=`<path d="M700 ${700-rr} A ${rr} ${rr} 0 0 1 ${700+rr} 700" fill="none" stroke="${c}" stroke-width="14"/>`;}
    s+='</svg>'; return s;
  };
  bg.insertAdjacentHTML('beforeend', mk('tr',360,-620,18));
  bg.insertAdjacentHTML('beforeend', mk('bl',-720,980,196));
}

/* ---- headline words ---- */
const HL='Design a curved bench seat. Online.'.split(' ');
el('hl').innerHTML = HL.map((w,i)=>`<span class="w" data-i="${i}">${w}${i<HL.length-1?' ':''}</span>`).join('');
const words=[...document.querySelectorAll('#hl .w')];

/* ---- preview arc ---- */
const PV=el('preview');
function drawPreview(f){ // f: 0..1 sweep progress
  const size=360, cx=180, cy=246;
  const scale=(size*0.44)/(DIMS.r+DIMS.w);
  const rIn=DIMS.r*scale, rOut=(DIMS.r+DIMS.w)*scale;
  const a=(DIMS.ang*Math.PI/180)*clamp(f);
  if(a<0.001){ PV.innerHTML=''; return; }
  const s=-Math.PI/2 - a/2, e=-Math.PI/2 + a/2;
  const pt=(r,ang)=>[cx+r*Math.cos(ang), cy+r*Math.sin(ang)];
  const[x1,y1]=pt(rOut,s),[x2,y2]=pt(rOut,e),[x3,y3]=pt(rIn,e),[x4,y4]=pt(rIn,s);
  const large=a>Math.PI?1:0;
  const d=`M ${x1} ${y1} A ${rOut} ${rOut} 0 ${large} 1 ${x2} ${y2} L ${x3} ${y3} A ${rIn} ${rIn} 0 ${large} 0 ${x4} ${y4} Z`;
  let fill='#d9d2bf',stroke='#7a6a3a';
  if(cfg.fill==='green'){fill='rgba(45,138,91,.16)';stroke='#2d8a5b';}
  if(cfg.fill==='ink'){fill='#e7e4dc';stroke='#0e0e0c';}
  let inner=`<defs><pattern id="wd" patternUnits="userSpaceOnUse" width="7" height="7" patternTransform="rotate(45)"><rect width="7" height="7" fill="${fill}"/><line x1="0" y1="0" x2="0" y2="7" stroke="#b8a880" stroke-width="0.6"/></pattern></defs>`;
  const useFill = cfg.fill==='wood'?'url(#wd)':fill;
  inner+=`<path d="${d}" fill="${useFill}" stroke="${stroke}" stroke-width="2"/>`;
  inner+=`<circle cx="${cx}" cy="${cy}" r="3" fill="#0e0e0c"/>`;
  PV.innerHTML=inner;
}

/* ---- typing helper ---- */
const sub=(str,p)=>str.slice(0, Math.round(clamp(p)*str.length));

/* ---- targets (rects in stage coords) ---- */
let TG={};
function measure(){
  const sr=stage.getBoundingClientRect();
  const c=(id)=>{const r=el(id).getBoundingClientRect();return{x:r.left-sr.left+r.width/2,y:r.top-sr.top+r.height/2,r:{x:r.left-sr.left,y:r.top-sr.top,w:r.width,h:r.height}};};
  TG={mat:c('f-mat'),rad:c('f-rad'),wid:c('f-wid'),ang:c('f-ang'),price:c('v-price'),cart:c('cart')};
}

/* ---- cursor path waypoints (base times) ---- */
const WP=[
  {t:0.0, k:null, p:{x:980,y:1620}},
  {t:1.9, k:'mat'},
  {t:2.75,k:'rad'},
  {t:3.95,k:'wid'},
  {t:4.65,k:'ang'},
  {t:5.7, k:'price'},
  {t:7.05,k:'cart'},
];
function cursorAt(t){
  const wps=WP.map(w=>({t:T(w.t),p:w.p||(TG[w.k]?{x:TG[w.k].x,y:TG[w.k].y}:{x:980,y:1620})}));
  if(t<=wps[0].t) return wps[0].p;
  for(let i=0;i<wps.length-1;i++){
    if(t>=wps[i].t&&t<=wps[i+1].t){
      const f=easeInOut(seg(t,wps[i].t,wps[i+1].t));
      return {x:lerp(wps[i].p.x,wps[i+1].p.x,f), y:lerp(wps[i].p.y,wps[i+1].p.y,f)};
    }
  }
  return wps[wps.length-1].p;
}

/* ---- zoom ---- */
function zoomAt(t){
  const strong=cfg.zoom==='strong', subtle=cfg.zoom==='subtle', prev=cfg.zoom==='preview';
  let s=1, fx=540, fy=960;
  const cardC={x:540,y:card.getBoundingClientRect().top+ (card.offsetHeight/2)};
  // phases
  const zBody = subtle?1.03: strong?1.16: prev?1.1:1.08;
  const zPrice= subtle?1.12: strong?1.5:  prev?1.28:1.34;
  const zCart = subtle?1.1:  strong?1.32: prev?1.18:1.22;
  if(t<T(1.4)){ s=1; fx=540; fy=960; }
  else if(t<T(5.1)){ const f=easeInOut(seg(t,T(1.4),T(2.0))); s=lerp(1,zBody,f);
    const foc= prev? {x:360,y:760} : {x:540,y:820}; fx=foc.x; fy=foc.y; }
  else if(t<T(6.5)){ const f=easeInOut(seg(t,T(5.1),T(5.7))); s=lerp(zBody,zPrice,f);
    fx=(TG.price&&TG.price.x)||560; fy=(TG.price&&TG.price.y)||1150; }
  else if(t<T(8.0)){ const f=easeInOut(seg(t,T(6.5),T(7.0))); s=lerp(zPrice,zCart,f);
    fx=(TG.cart&&TG.cart.x)||620; fy=(TG.cart&&TG.cart.y)||1300; }
  else { const f=easeInOut(seg(t,T(8.0),T(8.5))); s=lerp(zCart,1,f); fx=540; fy=960; }
  return {s,fx,fy};
}

/* ---- captions ---- */
const CAPS=[
  {a:1.35,b:2.45,txt:'Choose your material.'},
  {a:2.5, b:3.65,txt:'Set the radius.'},
  {a:3.7, b:5.05,txt:'Width and angle.'},
  {a:5.25,b:6.5, txt:'Instant price.'},
  {a:6.65,b:8.0, txt:'Add to cart. Done.'},
];

/* ---- outro monogram (two curved halves) ---- */
el('mono').innerHTML=`<path d="M50 8 A 42 42 0 0 0 50 92" fill="none" stroke="#fff" stroke-width="9"/><path d="M50 8 A 42 42 0 0 1 50 92" fill="none" stroke="#2d8a5b" stroke-width="9"/><circle cx="50" cy="50" r="7" fill="#fff"/>`;

/* ---- main render ---- */
function render(t){
  // headline word reveal
  words.forEach((w,i)=>{
    const a=T(0.25+i*0.12), f=easeOutBack(seg(t,a,a+T(0.5)));
    w.style.opacity=clamp(f*1.6); w.style.transform=`translateY(${lerp(26,0,clamp(f))}px)`;
  });
  // card entrance
  const ce=easeOutBack(seg(t,T(0.5),T(1.35)));
  card.style.opacity=clamp(ce*1.4); card.style.transform=`scale(${lerp(0.9,1,clamp(ce))})`;
  // field values
  el('v-mat').textContent = t>T(1.6)? DIMS.mat : '';
  el('v-rad').textContent = sub(String(DIMS.r), seg(t,T(2.55),T(3.35)));
  el('v-wid').textContent = sub(String(DIMS.w), seg(t,T(3.8),T(4.35)));
  el('v-ang').textContent = sub(String(DIMS.ang), seg(t,T(4.5),T(5.05)))+(seg(t,T(4.5),T(5.05))>=1?'°':'');
  // active field borders
  const setAct=(id,a,b)=>el(id).classList.toggle('active', t>=T(a)&&t<=T(b));
  setAct('f-mat',1.5,2.4); setAct('f-rad',2.5,3.5); setAct('f-wid',3.75,4.4); setAct('f-ang',4.45,5.15);
  // preview sweep: grows as radius+angle set
  let pf=0;
  pf=Math.max(seg(t,T(2.7),T(3.4))*0.15, seg(t,T(4.45),T(5.15))); // starts small when radius in, completes with angle
  if(t>T(3.4)&&t<T(4.45)) pf=lerp(0.15,0.15,0); // hold thin until angle
  if(t>=T(4.45)) pf=seg(t,T(4.45),T(5.15));
  else if(t>=T(2.7)) pf=seg(t,T(2.7),T(3.4))*0.5;
  drawPreview(pf);
  // price count-up + glow
  const pf2=easeOut(seg(t,T(5.2),T(6.2)));
  el('v-price').textContent='$'+(PRICE*pf2).toFixed(2);
  const gl=el('glow'), pr=TG.price&&TG.price.r;
  if(pr){ const g=Math.sin(clamp(seg(t,T(5.9),T(6.6)))*Math.PI);
    gl.style.left=(pr.x-8)+'px'; gl.style.top=(pr.y-8)+'px'; gl.style.width=(pr.w+16)+'px'; gl.style.height=(pr.h+16)+'px';
    gl.style.opacity=g*0.9; gl.style.boxShadow=`0 0 ${20+g*30}px ${g*8}px rgba(45,138,91,${0.5*g})`; }
  el('v-price').style.color = t>T(6.0)? '#194431' : '#0e0e0c';
  // cursor
  const cp=cursorAt(t); el('cursor').style.transform=`translate(${cp.x}px,${cp.y}px)`;
  // tap ring on cart click
  const tr=el('tapring'); const tclick=T(7.15);
  if(TG.cart){ const g=Math.sin(clamp(seg(t,tclick,tclick+T(0.5)))*Math.PI);
    tr.style.left=(TG.cart.x-40)+'px'; tr.style.top=(TG.cart.y-40)+'px'; tr.style.opacity=g; tr.style.transform=`scale(${lerp(0.4,1.3,clamp(seg(t,tclick,tclick+T(0.5))))})`; }
  // cart added check
  document.querySelector('#cart .chk').style.opacity = t>T(7.25)?clamp(seg(t,T(7.25),T(7.6))):0;
  // caption
  const capBox=el('caption'); let cur=null;
  for(const c of CAPS){ if(t>=T(c.a)&&t<=T(c.b)) cur=c; }
  if(cur){ const inF=easeOutBack(seg(t,T(cur.a),T(cur.a)+T(0.28))); const outF=1-seg(t,T(cur.b)-T(0.25),T(cur.b));
    const op=clamp(Math.min(inF*1.5,outF*3));
    const style=cfg.capCard? '' : 'background:transparent;box-shadow:none;color:'+(cfg.theme==='paper'?'#0e0e0c':'#fff');
    capBox.innerHTML=`<span class="cap" style="${style};opacity:${op};transform:translateY(${lerp(16,0,clamp(inF))}px)">${cur.txt}</span>`;
  } else capBox.innerHTML='';
  // zoom transform
  const z=zoomAt(t); stage.style.transform=`translate(${540-z.fx*z.s}px,${960-z.fy*z.s}px) scale(${z.s})`;
  // outro
  const oF=easeInOut(seg(t,T(8.2),T(9.0)));
  const outro=el('outro'); outro.style.opacity=clamp(oF*1.2);
  el('cursor').style.opacity = t>T(7.9)?clamp(1-seg(t,T(7.9),T(8.3))):(t<T(1.6)?clamp(seg(t,T(1.4),T(1.7))):1);
}

/* ---- boot ---- */
theme(); motif();
window.__ready=false;
document.fonts.ready.then(()=>{ measure(); window.__ready=true; window.__seek=render; window.__duration=T(DUR); render(0); });
window.__seek=(t)=>render(t); window.__duration=T(DUR);
