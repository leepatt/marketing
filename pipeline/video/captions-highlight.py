"""captions-highlight.py - Reel captions in the Craftons style chosen for the Radius Pro reel (2026-09-04).
MODE=green (default): Inter Bold in Craftons green with a thin off-white edge, two words at a time, centred;
  the word being spoken flips to white inside a Craftons-green rounded box.
MODE=white: white text, spoken word boxed in green (Bluebeam-style).
Word widths come from the Inter Bold hmtx table so the box lands on the word. Needs: pip install fonttools.
Placement used: SIZE=84 BOTTOM=1190 on a 1080x1350 frame (just above the Reels username/caption overlay).
Usage: captions-highlight.py words.json out.ass  Env: SIZE(80) BOTTOM(1100) CX(540) PLAYH(1350) MAXW(2) MAXC(16) SHIFT(0) PAD(14) R(14)"""
import json, os, sys
from fontTools.ttLib import TTFont
words=json.load(open(sys.argv[1])); out=sys.argv[2]
SIZE=int(os.environ.get("SIZE",80)); BOTTOM=int(os.environ.get("BOTTOM",1100)); CX=int(os.environ.get("CX",540))
PLAYH=int(os.environ.get("PLAYH",1350)); MAXW=int(os.environ.get("MAXW",2)); MAXC=int(os.environ.get("MAXC",16))
SHIFT=float(os.environ.get("SHIFT",0)); PAD=int(os.environ.get("PAD",14)); R=int(os.environ.get("R",14))
f=TTFont(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fonts","Inter-Bold.ttf")); cmap=f.getBestCmap(); hmtx=f["hmtx"]; upm=f["head"].unitsPerEm
asc=f["hhea"].ascent; desc=f["hhea"].descent; LH=(asc-desc)*SIZE/upm
def wid(s): return sum(hmtx[cmap.get(ord(c),cmap[ord('?')])][0] for c in s)*SIZE/upm
SP=wid(" ")
def ts(t):
    t=max(0,t-SHIFT); h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
chunks=[]; cur=[]
for w in words:
    t=w["w"].strip()
    if not t: continue
    cur.append({"t":t,"s":w["s"],"e":w["e"]})
    if len(cur)>=MAXW or len(" ".join(x["t"] for x in cur))>=MAXC or t[-1] in ".?!,": chunks.append(cur); cur=[]
if cur: chunks.append(cur)
for i,c in enumerate(chunks):
    nxt=chunks[i+1][0]["s"] if i+1<len(chunks) else c[-1]["e"]+0.6
    c[0]["cs"]=c[0]["s"]; c[0]["ce"]=min(nxt, c[-1]["e"]+0.5)
GREEN="&H00314419"; WHITE="&H00FFFFFF"; PAPER="&H00F4F1EA"
MODE=os.environ.get("MODE","green")  # green: green text, live word white-in-green-box | white: white text, live word in green box
TXT,OUT,SHD,BORD,SHADOW=(GREEN,PAPER,"&H90000000",3,1) if MODE=="green" else (WHITE,"&H70000000","&H80000000",3,3)
hdr=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: {PLAYH}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter,{SIZE},{TXT},{TXT},{OUT},{SHD},-1,0,0,0,100,100,0,0,1,{BORD},{SHADOW},2,0,0,0,1
Style: Box,Inter,{SIZE},{GREEN},{GREEN},{GREEN},{GREEN},0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev=[]
def rrect(x1,y1,x2,y2,r):
    k=0.5523*r
    return (f"m {x1+r:.0f} {y1:.0f} l {x2-r:.0f} {y1:.0f} b {x2-r+k:.0f} {y1:.0f} {x2:.0f} {y1+r-k:.0f} {x2:.0f} {y1+r:.0f} "
            f"l {x2:.0f} {y2-r:.0f} b {x2:.0f} {y2-r+k:.0f} {x2-r+k:.0f} {y2:.0f} {x2-r:.0f} {y2:.0f} "
            f"l {x1+r:.0f} {y2:.0f} b {x1+r-k:.0f} {y2:.0f} {x1:.0f} {y2-r+k:.0f} {x1:.0f} {y2-r:.0f} "
            f"l {x1:.0f} {y1+r:.0f} b {x1:.0f} {y1+r-k:.0f} {x1+r-k:.0f} {y1:.0f} {x1+r:.0f} {y1:.0f}")
for c in chunks:
    W=sum(wid(x["t"]) for x in c)+SP*(len(c)-1); x0=CX-W/2
    txt=" ".join(x["t"] for x in c)
    off=0
    for i,x in enumerate(c):
        s=x["s"] if i>0 else c[0]["cs"]; e=c[i+1]["s"] if i+1<len(c) else c[0]["ce"]
        if e>s:
            xs=x0+off; xe=xs+wid(x["t"])
            ev.append(f"Dialogue: 0,{ts(s)},{ts(e)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\p1}}{rrect(xs-PAD,BOTTOM-LH+2,xe+PAD,BOTTOM+2,R)}{{\\p0}}")
        off+=wid(x["t"])+SP
    if MODE=="green":
        for i,x in enumerate(c):
            s_=x["s"] if i>0 else c[0]["cs"]; e_=c[i+1]["s"] if i+1<len(c) else c[0]["ce"]
            if e_<=s_: continue
            t2=" ".join((f"{{\\c{WHITE}\\bord0\\shad0}}{y['t']}{{\\c{GREEN}\\bord{BORD}\\shad{SHADOW}}}" if j==i else y["t"]) for j,y in enumerate(c))
            ev.append(f"Dialogue: 1,{ts(s_)},{ts(e_)},Cap,,0,0,0,,{{\\an2\\pos({CX},{BOTTOM})}}{t2}")
    else:
        ev.append(f"Dialogue: 1,{ts(c[0]['cs'])},{ts(c[0]['ce'])},Cap,,0,0,0,,{{\\an2\\pos({CX},{BOTTOM})}}{txt}")
open(out,"w").write(hdr+"\n".join(ev)+"\n"); print(len(chunks),"chunks, LH",round(LH,1))
