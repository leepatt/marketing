"""overlays.py - extra caption/graphic layers for a Reel, as ASS files to chain after the karaoke captions
(ffmpeg: ass=caps.ass,ass=overlay.ass). Built for the Radius Pro reel variants (2026-09-04).

  title     hook title card 0-2.4 s (green panel, curve arcs, big Inter line) + "n / N  Step" pill top-left,
            step times hard-coded for reel 01 - edit `steps` per video.
  callouts  UI callout pills with a leader line to the on-screen control. Each entry:
            (start, duration, label, pill top-left (x,y), target point (x,y)). Positions were read off gridded
            frames (drawgrid=w=100:h=100) at each moment - re-read them per video, the page scrolls.
  lower     editorial lower-third: sentence-level, Inter 50 px in Craftons green, 4 px green rule, left-aligned
            to the right of a bottom-left avatar. No karaoke captions with this one.
  mask      the knockout opener text mask ("Curves.") - render on black, then feed maskedmerge (see REEL-PROCESS).
Usage: overlays.py <mode> out.ass   (reads cut_words_fixed.json from cwd for `lower`)
"""
import json, sys, os
GREEN="&H00314419"; PAPER="&H00F4F1EA"; LINE="&H005B8A2D"; INK="&H000C0E0E"
HDR="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1350
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Inter,108,%s,%s,%s,%s,-1,0,0,0,100,100,-1,0,1,0,0,5,60,60,0,1
Style: Step,Inter,42,%s,%s,%s,%s,-1,0,0,0,100,100,0,0,3,16,0,7,0,0,0,1
Style: Pill,Inter,40,%s,%s,%s,%s,-1,0,0,0,100,100,0,0,3,14,0,7,0,0,0,1
Style: Lower,Inter,50,%s,%s,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,0,0,1,0,0,0,1
Style: Draw,Inter,20,%s,%s,%s,%s,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Mask,Inter,300,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,-4,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" % (PAPER,PAPER,GREEN,GREEN, PAPER,PAPER,GREEN,GREEN, PAPER,PAPER,GREEN,GREEN, GREEN,GREEN, GREEN,GREEN,GREEN,GREEN)
def ts(t):
    t=max(0,t); h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
def rect(x1,y1,x2,y2): return f"m {x1} {y1} l {x2} {y1} l {x2} {y2} l {x1} {y2}"
def line(x1,y1,x2,y2,w=4):
    # thin quad along the segment
    import math
    dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1; nx,ny=-dy/L*w/2,dx/L*w/2
    return f"m {x1+nx:.0f} {y1+ny:.0f} l {x2+nx:.0f} {y2+ny:.0f} l {x2-nx:.0f} {y2-ny:.0f} l {x1-nx:.0f} {y1-ny:.0f}"
mode=sys.argv[1]; out=sys.argv[2]; ev=[]
END=151.2
if mode=="title":   # V2: hook card 0-2.4s + step counter
    ev.append(f"Dialogue: 0,{ts(0)},{ts(2.4)},Draw,,0,0,0,,{{\\an7\\pos(0,0)\\p1\\bord0\\fad(0,350)}}{rect(0,0,1080,1350)}{{\\p0}}")
    ev.append(f"Dialogue: 1,{ts(0)},{ts(2.4)},Draw,,0,0,0,,{{\\an7\\pos(0,0)\\p1\\1c{LINE}\\1a&HA0&\\bord0\\fad(0,350)}}m -200 1350 b 300 250 800 250 1400 1350 m -100 1350 b 350 370 800 370 1300 1350 m 0 1350 b 400 490 800 490 1200 1350{{\\p0}}")
    ev.append(f"Dialogue: 2,{ts(0)},{ts(2.4)},Title,,0,0,0,,{{\\fad(200,350)}}Curves are on\\Nevery plan now.")
    steps=[(13.2,"Floor plan"),(24.4,"Pick your ply"),(31.4,"Dimensions"),(42.0,"Straight legs"),(76.8,"Name and quantity"),(93.2,"Parts list"),(118.6,"Quote and order")]
    for i,(t,lab) in enumerate(steps):
        e=steps[i+1][0] if i+1<len(steps) else END
        ev.append(f"Dialogue: 3,{ts(t)},{ts(e)},Step,,0,0,0,,{{\\an7\\pos(40,36)\\fad(150,150)}}{i+1} / {len(steps)}   {lab}")
elif mode=="callouts":   # V3: UI callout pills with leader lines
    C=[(24.4,3.0,"Pick your ply",(350,300),(525,351)),
       (31.4,2.5,"External dims",(790,405),(860,480)),
       (32.6,2.5,"Radius 900",(560,700),(600,591)),
       (42.0,3.0,"Straight legs",(790,720),(850,789)),
       (76.8,3.0,"Part name",(350,940),(540,990)),
       (83.1,2.5,"Quantity",(350,940),(525,1080)),
       (108.9,3.5,"Splits for 2.4 m sheets",(60,800),(527,450)),
       (121.4,2.5,"Add to cart",(290,880),(600,1000)),
       (128.9,2.5,"Save and share",(290,880),(600,1060))]
    for t,d,lab,(px,py),(tx,ty) in C:
        ax,ay=px+20,py+25   # leader starts near the pill's left-middle; pill is ~50px tall
        ev.append(f"Dialogue: 0,{ts(t)},{ts(t+d)},Draw,,0,0,0,,{{\\an7\\pos(0,0)\\p1\\bord0\\fad(120,120)}}{line(ax,ay,tx,ty)} {rect(tx-6,ty-6,tx+6,ty+6)}{{\\p0}}")
        ev.append(f"Dialogue: 1,{ts(t)},{ts(t+d)},Pill,,0,0,0,,{{\\an7\\pos({px},{py})\\fad(120,120)}}{lab}")
elif mode=="lower":   # V4: editorial lower-third, sentence level
    w=json.load(open("cut_words_fixed.json")); sents=[]; cur=[]
    for x in w:
        t=x["w"].strip()
        if not t: continue
        cur.append(x)
        if t[-1] in ".?!" or len(" ".join(y["w"].strip() for y in cur))>70: sents.append(cur); cur=[]
    if cur: sents.append(cur)
    for i,s in enumerate(sents):
        txt=" ".join(y["w"].strip() for y in s)
        # wrap to <=36 chars per line, max 2 lines
        words=txt.split(); lines=[]; l=""
        for wd in words:
            if len(l)+len(wd)+1>36 and l: lines.append(l); l=wd
            else: l=(l+" "+wd).strip()
        if l: lines.append(l)
        lines=lines[:3]
        st=s[0]["s"]; en=sents[i+1][0]["s"] if i+1<len(sents) else s[-1]["e"]+0.6
        raise_=200 if st>=143 else 0
        n=len(lines); by=1190-raise_; top=by-n*62
        ev.append(f"Dialogue: 0,{ts(st)},{ts(en)},Draw,,0,0,0,,{{\\an7\\pos(0,0)\\p1\\bord0}}{rect(330,top+8,338,by+4)}{{\\p0}}")
        ev.append(f"Dialogue: 1,{ts(st)},{ts(en)},Lower,,0,0,0,,{{\\an1\\pos(362,{by})}}"+"\\N".join(lines))
elif mode=="mask":   # V5: knockout text mask (white on black), static
    ev.append(f"Dialogue: 0,{ts(0)},{ts(10)},Mask,,0,0,0,,{{\\an5\\pos(540,640)}}Curves.")
open(out,"w").write(HDR+"\n".join(ev)+"\n"); print(mode,len(ev),"events")
