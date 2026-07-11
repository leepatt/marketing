/* Faithful Craftons "Configure Curve" demo. Frame = pure function of t (seconds). */
const DUR = 11.0;
const vid = parseInt(new URLSearchParams(location.search).get('v')||'0',10);
const PACE = ({0:1.0,1:0.85,2:1.2}[vid])||1.0;
const T=(x)=>x*PACE;

const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,t)=>a+(b-a)*t;
const seg=(t,a,b)=>clamp((t-a)/(b-a));
const easeInOut=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const easeOut=t=>1-Math.pow(1-t,3);
const el=id=>document.getElementById(id);

/* ---- value timeline ---- */
const START={r:900,w:100,a:90}, END={r:800,w:450,a:180};
function vals(t){
  const r=Math.round(lerp(START.r,END.r,easeInOut(seg(t,T(2.3),T(3.1)))));
  const w=Math.round(lerp(START.w,END.w,easeInOut(seg(t,T(3.4),T(4.2)))));
  const a=Math.round(lerp(START.a,END.a,easeInOut(seg(t,T(4.5),T(5.5)))));
  return {r,w,a};
}

/* ---- visualizer ---- */
const VS=el('vsvg');
function drawViz(r,w,a){
  const A=a*Math.PI/180, N=48;
  const rIn=r, rOut=r+w;
  const wp=(rr,ang)=>[rr*Math.cos(ang), rr*Math.sin(ang)];   // world, y-up, center origin
  // bbox over sector
  let xs=[0], ys=[0];
  for(let i=0;i<=N;i++){const ang=A*i/N; [rIn,rOut].forEach(rr=>{const[x,y]=wp(rr,ang);xs.push(x);ys.push(y);});}
  const minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);
  const bw=maxX-minX, bh=maxY-minY;
  const boxW=1000,boxH=640,padX=150,padTop=120,padBot=120;
  const sc=Math.min((boxW-2*padX)/bw,(boxH-padTop-padBot)/bh);
  const ox=(boxW-bw*sc)/2 - minX*sc;
  const oy=boxH-padBot + minY*sc;   // flip
  const S=(rr,ang)=>{const[x,y]=wp(rr,ang);return [ox+x*sc, oy - y*sc];};
  const arc=(rr,a0,a1,N2=48)=>{let d='';for(let i=0;i<=N2;i++){const ang=lerp(a0,a1,i/N2);const[x,y]=S(rr,ang);d+=(i?'L':'M')+x.toFixed(1)+' '+y.toFixed(1);}return d;};
  const large=A>Math.PI?1:0;
  const[ox0,oy0]=S(rOut,0),[oxe,oye]=S(rOut,A),[ix0,iy0]=S(rIn,0),[ixe,iye]=S(rIn,A);
  const band=`M ${ox0} ${oy0} A ${rOut*sc} ${rOut*sc} 0 ${large} 0 ${oxe} ${oye} L ${ixe} ${iye} A ${rIn*sc} ${rIn*sc} 0 ${large} 1 ${ix0} ${iy0} Z`;
  const cen=S(0,0);
  const pill=(rr,ang,txt,col)=>{const[x,y]=S(rr,ang);const wpx=txt.length*17+34;
    return `<g><rect x="${x-wpx/2}" y="${y-30}" width="${wpx}" height="52" rx="12" fill="#fff" stroke="#e2e0d8"/><text x="${x}" y="${y+6}" font-size="30" font-weight="700" fill="${col}" text-anchor="middle" font-family="SG">${txt}</text></g>`;};
  const midA=A/2;
  let s='';
  // internal outline (green legs + inner arc) + chord (dashed)
  s+=`<path d="M ${cen[0]} ${cen[1]} L ${ix0} ${iy0} ${arc(rIn,0,A).slice(1)} L ${cen[0]} ${cen[1]} Z" fill="none" stroke="#2d8a5b" stroke-width="3"/>`;
  s+=`<line x1="${ix0}" y1="${iy0}" x2="${ixe}" y2="${iye}" stroke="#b9b7ad" stroke-width="2.5" stroke-dasharray="10 9"/>`;
  // angle mini-arc
  s+=`<path d="${arc(r*0.2,0,A,20)}" fill="none" stroke="#8a8a82" stroke-width="2.5"/>`;
  // band (the part)
  s+=`<path d="${band}" fill="#141414"/>`;
  // pills
  s+=pill((rIn+rOut)/2, 0, 'w:', '#2d8a5b');
  s+=pill(rIn*0.55, 0.03, 'r:', '#111');
  s+=pill(rOut+ w*0.0+ 40/sc, midA, 'L:', '#2a6fd6');
  s+=pill(rIn*0.62, midA, 'c:', '#7c3aed');
  s+=pill(r*0.2+70/sc, midA, 'θ:', '#c2560f');
  VS.innerHTML=s;
}

/* ---- targets ---- */
const stage=el('stage');
function rc(id){const s=stage.getBoundingClientRect(),r=el(id).getBoundingClientRect();return{x:r.left-s.left+r.width/2,y:r.top-s.top+r.height/2};}

/* ---- scroll & zoom ---- */
function scrollY(t){ return lerp(0, 900, easeInOut(seg(t,T(6.7),T(7.8)))); }
function zoom(t){
  let s=1,fx=540,fy=560;
  if(t>=T(5.4)&&t<T(6.9)){ const f=easeInOut(seg(t,T(5.4),T(6.0))); s=lerp(1,1.12,f); fx=540; fy=470; }
  else if(t>=T(6.9)){ s=1; }
  return {s,fx,fy};
}

/* ---- cursor waypoints ---- */
const WP=[{t:0.0,p:{x:1180,y:1720}},{t:1.6,k:'f-mat'},{t:2.5,k:'f-rad'},{t:3.6,k:'f-wid'},{t:4.7,k:'f-ang'},{t:6.9,k:'f-ang'},{t:7.9,k:'addp'}];
function cursor(t){
  const w=WP.map(o=>({t:T(o.t),p:o.p?o.p:rc(o.k)}));
  if(t<=w[0].t)return w[0].p;
  for(let i=0;i<w.length-1;i++)if(t>=w[i].t&&t<=w[i+1].t){const f=easeInOut(seg(t,w[i].t,w[i+1].t));return{x:lerp(w[i].p.x,w[i+1].p.x,f),y:lerp(w[i].p.y,w[i+1].p.y,f)};}
  return w[w.length-1].p;
}

/* ---- captions ---- */
const CAP=[{a:1.5,b:2.4,t:'Pick your material.'},{a:2.5,b:3.5,t:'Set your radius.'},{a:3.6,b:4.5,t:'Set the width.'},{a:4.6,b:5.9,t:'Set the angle — it builds itself.'},{a:6.0,b:6.9,t:'Made to your millimetre.'},{a:7.3,b:8.8,t:'Add the part. Done.'}];

/* ---- render ---- */
function render(t){
  const {r,w,a}=vals(t);
  el('v-rad').textContent=r; el('v-wid').textContent=w; el('v-ang').textContent=a;
  // arc & chord fill once angle editing starts
  const showLC = t>T(4.6);
  const L=Math.round(Math.PI*r*a/180), c=Math.round(2*r*Math.sin(a*Math.PI/360));
  const av=el('v-arc'), cv=el('v-cho');
  if(showLC){av.textContent=L;av.classList.remove('ph');cv.textContent=c;cv.classList.remove('ph');}
  else {av.textContent='—';av.classList.add('ph');cv.textContent='—';cv.classList.add('ph');}
  drawViz(r,w,a);
  // active borders
  const act=(id,x,y)=>el(id).classList.toggle('act',t>=T(x)&&t<=T(y));
  el('f-mat').classList.toggle('act',t>=T(1.5)&&t<=T(2.3));
  act('f-rad',2.3,3.3); act('f-wid',3.4,4.3); act('f-ang',4.5,5.6);
  // scroll
  el('content').style.transform=`translateY(${-scrollY(t)}px)`;
  // zoom
  const z=zoom(t); stage.style.transform=`translate(${540-z.fx*z.s}px,${960-z.fy*z.s}px) scale(${z.s})`;
  // cursor
  const cp=cursor(t); el('cursor').style.transform=`translate(${cp.x}px,${cp.y}px)`;
  el('cursor').style.opacity = t<T(1.2)?clamp(seg(t,T(0.8),T(1.2))):(t>T(9.2)?clamp(1-seg(t,T(9.2),T(9.6))):1);
  // tap on add part
  const tap=el('tap'), tc=T(8.2);
  if(t>T(7.9)){const tg=rc('addp');const g=Math.sin(clamp(seg(t,tc,tc+T(0.5)))*Math.PI);tap.style.left=(tg.x-42)+'px';tap.style.top=(tg.y-42)+'px';tap.style.opacity=g;tap.style.transform=`scale(${lerp(0.4,1.3,clamp(seg(t,tc,tc+T(0.5))))})`;}
  else tap.style.opacity=0;
  document.querySelector('#addp .done').style.opacity = t>T(8.3)?clamp(seg(t,T(8.3),T(8.7))):0;
  // caption
  const box=el('caption'); let cur=null; for(const c2 of CAP) if(t>=T(c2.a)&&t<=T(c2.b)) cur=c2;
  if(cur){const inF=easeOut(seg(t,T(cur.a),T(cur.a)+T(0.25)));const outF=1-seg(t,T(cur.b)-T(0.2),T(cur.b));box.innerHTML=`<span class="cap" style="opacity:${clamp(Math.min(inF*1.5,outF*3))}">${cur.t}</span>`;}
  else box.innerHTML='';
}

window.__ready=false;
document.fonts.ready.then(()=>{ window.__seek=render; window.__duration=T(DUR); render(0); window.__ready=true; });
window.__seek=render; window.__duration=T(DUR);
