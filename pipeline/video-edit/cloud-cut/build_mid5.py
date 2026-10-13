#!/usr/bin/env python3
"""build_mid5.py (from mid4): NO L-cut. 6013 voice EQ-matched to the outdoor clips (voicematch.json),
natural room tone after "price" taken from the source (never inserted silence), straight cut out.
 — screen section timed TO THE VOICE (not the other way round), with an L-cut out.
Audio: 6013 "So we built ... instant price." + 0.25s breath + 6001 "It's" -> the cut to the face lands on "then".
Beats are pinned to the words, so there is no padding anywhere."""
import subprocess, json, re, os
from pathlib import Path
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
VO_IN = 2.1                     # 6013 slice start
PRICE_END = 7.32 + 0.05         # end of "price." relative to VO_IN
BREATH = 0.30                  # real room tone from 6013 after "price." (the clip runs to 9.78)
HERO = 1.9                      # "So we built the Formwork Builder" (0.22-1.56)
# word-pinned beats after the hero (seconds on screen):
#   inputs   "an online tool where you can"   -> to 3.50
#   build    "design your concrete structure" -> to 5.40
#   ply      "select your formwork"           -> to 6.45
#   price    "and get an instant price" + breath + "It's" -> to the end
AUDIO = PRICE_END + BREATH
TARGET = [3.50-HERO, 5.40-3.50, 6.45-5.40, AUDIO-6.45]
marks = {m.group(2): float(m.group(1)) for m in re.finditer(r"^([\d.]+)s\s+(.+)$", Path(os.environ.get("MARKS","../rec3/marks.log")).read_text(), re.M)}
T = lambda k: marks[next(x for x in marks if x.startswith(k))]
SUB = [(T("A start")+2.6, T("B height 600")+0.3),
       (T("C backrest on")-0.4, T("C cantilever depth")+0.7 + 0.58*(T("C orbit3")-T("C cantilever depth")-0.7)),   # first 58% of the orbit, before it dips under the bench
       (T("D tick Plates")-0.3, T("D orbit4")+0.1),
       (T("E order summary")-0.6, T("END"))]
speeds = [(b-a)/t for (a,b),t in zip(SUB,TARGET)]
print("beats:", [round(t,2) for t in TARGET], "speeds:", [f"x{s:.0f}" for s in speeds], f"total {AUDIO:.2f}s")
split = os.environ.get("SPLIT","src/split.mp4")
ins = ["-i","ovl/hero.png"]
for a,b in SUB: ins += ["-ss",f"{a:.2f}","-t",f"{b-a:.2f}","-i",split]
n = 1+len(SUB); ins += ["-loop","1","-i","ovl/banner.png","-loop","1","-i","ovl/seam.png",
    "-ss",str(VO_IN),"-t",f"{AUDIO+0.3:.3f}","-i","src/IMG_6013.mov"]   # extra real room tone; output -t trims
iban, iseam, ia = n, n+1, n+2
EQ = json.load(open("voicematch.json"))["eq"]
fc = [f"[0:v]scale=1080:1920,zoompan=z='min(zoom+0.0009,1.08)':d={int(HERO*30)}:s=1080x1920:fps=30,trim=duration={HERO},setpts=PTS-STARTPTS,setsar=1[v0]"]
for k,s in enumerate(speeds,1): fc.append(f"[{k}:v]setpts=PTS/{s:.4f},scale=1080:1920,fps=30,setsar=1[v{k}]")
fc.append("".join(f"[v{k}]" for k in range(n))+f"concat=n={n}:v=1:a=0[base]")
fc.append(f"[base][{iseam}:v]overlay=0:0:enable='gte(t,{HERO})'[b1]")
fc.append(f"[b1][{iban}:v]overlay=0:0:enable='gte(t,{HERO})',tpad=stop_mode=clone:stop_duration=0.5[vout]")   # picture never shorter than the audio
fc.append(f"[{ia}:a]{EQ},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[aout]")
subprocess.run([FF,"-hide_banner","-loglevel","error","-y",*ins,"-filter_complex",";".join(fc),"-map","[vout]","-map","[aout]",
  "-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-t",f"{AUDIO:.3f}","src/mid5.mp4"],check=True)
Path("mid5.json").write_text(json.dumps({"dur":round(AUDIO,3),"hero":HERO,"targets":TARGET}))
print("mid5.mp4 ok")
