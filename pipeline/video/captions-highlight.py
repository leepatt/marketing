"""captions-highlight.py - the Craftons Reel caption style, chosen on the Radius Pro reel (2026-09-04).
Stacked Reel captions: up to 2 lines x 2 words per block, Craftons green Inter Bold, spoken word flips to
white in a green rounded box. Env: SIZE(84) BOTTOM(1190) CX(540) PLAYH(1350) WPL(2 words/line) LINES(2)
GAP(10 px between lines) PAD(14) R(14) SHIFT(0) RAISE="t:px" (raise blocks starting after t seconds by px, e.g. RAISE=143:200 to clear the quote page's own
Accept Quote button). Needs: pip install fonttools. Burn in: ffmpeg ass=out.ass:fontsdir=pipeline/video/fonts.
Usage: captions-highlight.py words.json out.ass"""
import json, os, sys
from fontTools.ttLib import TTFont
words=json.load(open(sys.argv[1])); out=sys.argv[2]
E=os.environ.get
SIZE=int(E("SIZE",84)); BOTTOM=int(E("BOTTOM",1190)); CX=int(E("CX",540)); PLAYH=int(E("PLAYH",1350))
WPL=int(E("WPL",2)); LINES=int(E("LINES",2)); GAP=int(E("GAP",10)); PAD=int(E("PAD",14)); R=int(E("R",14))
SHIFT=float(E("SHIFT",0)); RAISE=E("RAISE","0:0"); RT,RPX=[float(x) for x in RAISE.split(":")]
f=TTFont(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fonts","Inter-Bold.ttf")); cmap=f.getBestCmap(); hmtx=f["hmtx"]; upm=f["head"].unitsPerEm
LH=(f["hhea"].ascent-f["hhea"].descent)*SIZE/upm
def wid(s): return sum(hmtx[cmap.get(ord(c),cmap[ord('?')])][0] for c in s)*SIZE/upm
SP=wid(" ")
def ts(t):
    t=max(0,t-SHIFT); h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
MAXW=WPL*LINES
chunks=[]; cur=[]
for w in words:
    t=w["w"].strip()
    if not t: continue
    cur.append({"t":t,"s":w["s"],"e":w["e"]})
    if len(cur)>=MAXW or t[-1] in ".?!": chunks.append(cur); cur=[]
if cur: chunks.append(cur)
for i,c in enumerate(chunks):
    nxt=chunks[i+1][0]["s"] if i+1<len(chunks) else c[-1]["e"]+0.6
    c[0]["cs"]=c[0]["s"]; c[0]["ce"]=min(nxt, c[-1]["e"]+0.5)
GREEN="&H00314419"; WHITE="&H00FFFFFF"; PAPER="&H00F4F1EA"
hdr=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: {PLAYH}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter,{SIZE},{GREEN},{GREEN},{PAPER},&H90000000,-1,0,0,0,100,100,0,0,1,3,1,2,0,0,0,1
Style: Box,Inter,{SIZE},{GREEN},{GREEN},{GREEN},{GREEN},0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
def rrect(x1,y1,x2,y2,r):
    k=0.5523*r
    return (f"m {x1:.0f} {y1+r:.0f} b {x1:.0f} {y1+r-k:.0f} {x1+r-k:.0f} {y1:.0f} {x1+r:.0f} {y1:.0f} l {x2-r:.0f} {y1:.0f} "
            f"b {x2-r+k:.0f} {y1:.0f} {x2:.0f} {y1+r-k:.0f} {x2:.0f} {y1+r:.0f} l {x2:.0f} {y2-r:.0f} "
            f"b {x2:.0f} {y2-r+k:.0f} {x2-r+k:.0f} {y2:.0f} {x2-r:.0f} {y2:.0f} l {x1+r:.0f} {y2:.0f} "
            f"b {x1+r-k:.0f} {y2:.0f} {x1:.0f} {y2-r+k:.0f} {x1:.0f} {y2-r:.0f}")
ev=[]
for c in chunks:
    bottom=BOTTOM-(RPX if c[0]["cs"]>=RT else 0)
    lines=[c[i:i+WPL] for i in range(0,len(c),WPL)]
    n=len(lines)
    # line k (0=top) bottom y:
    ly=[bottom-(n-1-k)*(LH+GAP) for k in range(n)]
    for k,line in enumerate(lines):
        W=sum(wid(x["t"]) for x in line)+SP*(len(line)-1); x0=CX-W/2; off=0
        for x in line:
            x["x1"]=x0+off; x["x2"]=x0+off+wid(x["t"]); x["ly"]=ly[k]; off+=wid(x["t"])+SP
    for i,x in enumerate(c):
        s_=x["s"] if i>0 else c[0]["cs"]; e_=c[i+1]["s"] if i+1<len(c) else c[0]["ce"]
        if e_<=s_: continue
        ev.append(f"Dialogue: 0,{ts(s_)},{ts(e_)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\p1}}{rrect(x['x1']-PAD,x['ly']-LH+2,x['x2']+PAD,x['ly']+2,R)}{{\\p0}}")
        for k,line in enumerate(lines):
            t2=" ".join((f"{{\\c{WHITE}\\bord0\\shad0}}{y['t']}{{\\c{GREEN}\\bord3\\shad1}}" if y is x else y["t"]) for y in line)
            ev.append(f"Dialogue: 1,{ts(s_)},{ts(e_)},Cap,,0,0,0,,{{\\an2\\pos({CX},{ly[k]:.0f})}}{t2}")
open(out,"w").write(hdr+"\n".join(ev)+"\n"); print(len(chunks),"blocks; avg",round(sum(len(c) for c in chunks)/len(chunks),2),"words/block")
