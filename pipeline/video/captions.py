"""captions.py - build Reel captions (ASS, Inter) from faster-whisper word timestamps.
Usage: captions.py words.json STYLE out.ass [marginV]   STYLE: white, green, card, highlight, ink (ink text on white ground)
Env: SHIFT=seconds (subtract from times, for test frames); ML/MR caption margins (default 40/410 = clear of a bottom-right PiP).
Burn in: ffmpeg -i in.mp4 -vf "ass=out.ass:fontsdir=fonts" ...  (fonts/ = Inter static TTFs from github.com/rsms/inter)
Colours: Craftons green-900 pill, ink text on white card, line-green #2d8a5b spoken-word highlight."""
import json, sys
words=json.load(open(sys.argv[1])); style=sys.argv[2]; out=sys.argv[3]
MV=int(sys.argv[4]) if len(sys.argv)>4 else 360
import os; SHIFT=float(os.environ.get("SHIFT","0")); ML=int(os.environ.get("ML","40")); MR=int(os.environ.get("MR","410"))
def ts(t):
    t=max(0,t-SHIFT); h=int(t//3600); m=int(t%3600//60); s=t%60
    return f"{h}:{m:02d}:{s:05.2f}"
# chunk words: max 3 words / 20 chars, break on sentence punctuation
chunks=[]; cur=[]
for w in words:
    t=w["w"].strip()
    if not t: continue
    cur.append({"t":t,"s":w["s"],"e":w["e"]})
    txt=" ".join(x["t"] for x in cur)
    if len(cur)>=3 or len(txt)>=20 or t[-1] in ".?!,":
        chunks.append(cur); cur=[]
if cur: chunks.append(cur)
# timing: chunk visible from its first word to the next chunk's first word (max 0.5s hang)
for i,c in enumerate(chunks):
    c_start=c[0]["s"]; c_end=c[-1]["e"]
    nxt=chunks[i+1][0]["s"] if i+1<len(chunks) else c_end+0.6
    c_end=min(nxt, c_end+0.5) if nxt-c_end>0 else nxt
    for x in c: x["cs"],x["ce"]=c_start,c_end
GREEN="&H00141C0A"; LINE="&H005B8A2D"; INK="&H000C0E0E"; WHITE="&H00FFFFFF"; BLACK="&H00000000"
# Style: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
styles={
 "white":     f"Style: Cap,Inter,68,{WHITE},{WHITE},{BLACK},&H80000000,-1,0,0,0,100,100,-1,0,1,4,2,2,{ML},{MR},{MV},1",
 "green":     f"Style: Cap,Inter,60,{WHITE},{WHITE},{GREEN},{GREEN},-1,0,0,0,100,100,-1,0,3,22,0,2,{ML},{MR},{MV},1",
 "card":      f"Style: Cap,Inter,60,{INK},{INK},{WHITE},{WHITE},-1,0,0,0,100,100,-1,0,3,22,0,2,{ML},{MR},{MV},1",
 "ink":       f"Style: Cap,Inter,68,{INK},{INK},{WHITE},{WHITE},-1,0,0,0,100,100,-1,0,1,3,0,2,{ML},{MR},{MV},1",
 "highlight": f"Style: Cap,Inter,68,{WHITE},{WHITE},{BLACK},&H80000000,-1,0,0,0,100,100,-1,0,1,4,2,2,{ML},{MR},{MV},1",
}
hdr=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{styles[style]}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev=[]
for c in chunks:
    if style=="highlight":
        # one event per word: current word in line-green
        for i,x in enumerate(c):
            s=x["s"] if i>0 else c[0]["cs"]
            e=c[i+1]["s"] if i+1<len(c) else c[0]["ce"]
            if e<=s: continue
            txt=" ".join((f"{{\\c{LINE}}}{y['t']}{{\\c{WHITE}}}" if j==i else y["t"]) for j,y in enumerate(c))
            ev.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{txt}")
    else:
        txt=" ".join(x["t"] for x in c)
        ev.append(f"Dialogue: 0,{ts(c[0]['cs'])},{ts(c[0]['ce'])},Cap,,0,0,0,,{txt}")
open(out,"w").write(hdr+"\n".join(ev)+"\n")
print(style, len(chunks),"chunks ->",out)
