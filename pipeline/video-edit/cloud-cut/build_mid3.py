#!/usr/bin/env python3
"""build_mid3.py — middle section v3: hero slide -> split-screen take (form top, inputs bottom), no text on the iframe.
Sub-clips of src/split.mp4 are chosen from rec3/marks.log and retimed under the 6013 voice.
Banner on top, green seam bar between the halves (captions sit in it, added later by assemble.py).
Writes src/mid3.mp4 + mid3.json."""
import subprocess, json, re, sys, os
from pathlib import Path
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
VO_IN, VO_OUT = 2.1, 9.78; VO = VO_OUT - VO_IN
HERO = 1.9
marks = {m.group(2): float(m.group(1)) for m in re.finditer(r"^([\d.]+)s\s+(.+)$", Path(os.environ.get("MARKS","../rec3/marks.log")).read_text(), re.M)}
def T(k): return marks[next(x for x in marks if x.startswith(k))]
# sub-clips (in, out, speed): each covers a phrase of the voice
SUB = [
    (T("A start")+2.6,      T("B height 600")+0.3,  None),  # zoom + orbit + radius/height   "an online tool where you can"  (1.56s)
    (T("C backrest on")-0.4, T("C orbit3")-33.0,     None),   # stop before the orbit drops below the bench  # backrest, taper, cantilever, orbit  "design your concrete structure" (2.0s)
    (T("D tick Plates")-0.3, T("D orbit4")+0.1,      None),  # formwork ticks + pan across ply   "select your formwork" (1.5s)
    (T("E order summary")-0.6, T("END"),              None),  # price + last orbit              "and get an instant price" + hold (2.9s)
]
TARGET = [1.5, 2.1, 1.5, 2.2]          # seconds each, sums to 8.2 -> total 10.1 with the hero; voice 7.68 -> pad ~2.4
speeds = [ (b-a)/t for (a,b,_),t in zip(SUB, TARGET) ]
print("sub-clips:", [(round(a,1), round(b,1), f"x{s:.1f}") for (a,b,_),s in zip(SUB, speeds)])
total = HERO + sum(TARGET); pad = max(0.0, total - VO)
print(f"hero {HERO} | split {sum(TARGET):.1f} | total {total:.2f} | voice {VO:.2f} | pad {pad:.2f}")

ins = ["-i","ovl/hero.png"]
for a,b,_ in SUB: ins += ["-ss",f"{a:.2f}","-t",f"{b-a:.2f}","-i",os.environ.get("SPLIT","src/split.mp4")]
n_vid = 1 + len(SUB)
ins += ["-loop","1","-i","ovl/banner.png","-loop","1","-i","ovl/seam.png"]; i_ban, i_seam = n_vid, n_vid+1
ins += ["-ss",str(VO_IN),"-t",str(VO),"-i","src/IMG_6013.mov"]; i_aud = n_vid+2
fc = [f"[0:v]scale=1080:1920,zoompan=z='min(zoom+0.0009,1.08)':d={int(HERO*30)}:s=1080x1920:fps=30,trim=duration={HERO},setpts=PTS-STARTPTS,setsar=1[v0]"]
for k,((a,b,_),sp) in enumerate(zip(SUB,speeds), start=1):
    fc.append(f"[{k}:v]setpts=PTS/{sp:.4f},scale=1080:1920,fps=30,setsar=1[v{k}]")
fc.append("".join(f"[v{k}]" for k in range(n_vid)) + f"concat=n={n_vid}:v=1:a=0[base]")
fc.append(f"[base][{i_seam}:v]overlay=0:0:enable='gte(t,{HERO})'[b1]")
fc.append(f"[b1][{i_ban}:v]overlay=0:0:enable='gte(t,{HERO})'[vout]")
fc.append(f"[{i_aud}:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad=pad_dur={pad:.3f}[aout]")
subprocess.run([FF,"-hide_banner","-loglevel","error","-y",*ins,"-filter_complex",";".join(fc),"-map","[vout]","-map","[aout]",
    "-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-t",f"{total:.3f}","src/mid3.mp4"],check=True)
Path("mid3.json").write_text(json.dumps({"dur":round(total,3),"hero":HERO,"targets":TARGET}))
print("mid3.mp4 ok")
