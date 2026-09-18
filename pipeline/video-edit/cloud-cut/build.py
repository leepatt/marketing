#!/usr/bin/env python3
"""build.py — Formwork Builder reel, cut 1.
seg1 IMG_5999 face | seg2 screen recording + IMG_6013 voice | seg3 IMG_6001 face (second take)"""
import json, subprocess
from pathlib import Path
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()

# ---- seg2: screen sub-clips retimed to sit under the 6013 voice ----
SUB = [  # (src_in, src_out, speed)   screen.mp4 timings, second recording
    ( 8.6, 11.5, 0.90),   # model hold + radius typed 1300     "So we built the Formwork Builder, an online tool where you can"
    (11.5, 13.4, 1.00),   # height typed 600                   "design your concrete structure"
    (15.0, 17.2, 1.60),   # Plates, Shutters, End Caps ticked  "select your formwork"
    (19.4, 22.0, 1.00),   # order summary: $675, 5-7 days      "and get an instant price"
]
VO_IN, VO_OUT = 2.1, 9.78                     # IMG_6013 audio slice
vid_dur = sum((b-a)/sp for a,b,sp in SUB)
vo_dur = VO_OUT - VO_IN
pad = max(0.0, vid_dur - vo_dur)
print(f"seg2: screen {vid_dur:.2f}s, voice {vo_dur:.2f}s, silence pad {pad:.2f}s")

fc, ins = [], []
for i,(a,b,sp) in enumerate(SUB):
    ins += ["-ss", str(a), "-t", str(b-a), "-i", "src/screen.mp4"]
    fc.append(f"[{i}:v]setpts=PTS/{sp},scale=1080:1920,fps=30[v{i}]")
n = len(SUB)
fc.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vout]")
fc.append(f"[{n}:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad=pad_dur={pad:.3f}[aout]")
subprocess.run([FF,"-hide_banner","-loglevel","error","-y", *ins,
    "-ss", str(VO_IN), "-t", str(vo_dur), "-i", "src/IMG_6013.mov",
    "-filter_complex", ";".join(fc), "-map","[vout]","-map","[aout]",
    "-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k",
    "-t", f"{vid_dur:.3f}", "src/mid.mp4"], check=True)

# ---- timeline ----
S1 = dict(src="src/IMG_5999.mov", **{"in":1.6, "out":10.05})
S2 = dict(src="src/mid.mp4", **{"in":0.0, "out":vid_dur})
S3 = dict(src="src/IMG_6001.mov", **{"in":10.6, "out":14.44})
t1, t2, t3 = 0.0, S1["out"]-S1["in"], None; t3 = t2 + vid_dur
print(f"timeline: face 0-{t2:.2f} | screen {t2:.2f}-{t3:.2f} | face {t3:.2f}-{t3+S3['out']-S3['in']:.2f}")

# ---- captions: his words, Whisper errors corrected ("concrete is"->"concreters", "we're with"->"we built") ----
def caps(cards, src_in, t_off):
    return [dict(start=round(c[0]-src_in+t_off,2), end=round(c[1]-src_in+t_off,2), text=c[2], hi=c[3], pos=(c[4] if len(c)>4 else None)) for c in cards]
C = []
C += caps([
    (1.94,3.76,"Since launching the Radius Pro","Radius Pro"),
    (3.76,5.10,"been getting a lot of concreters","concreters"),
    (5.10,6.06,"using the app",None),
    (6.06,7.76,"but also reaching out and asking",None),
    (7.76,8.98,"if we can cut the formwork","formwork"),
    (8.98,10.05,"for the whole project","whole project"),
], S1["in"], t1)
C += caps([
    (2.32,4.30,"So we built the Formwork Builder","Formwork Builder"),
    (4.30,5.68,"an online tool where you can",None),
    (5.68,7.64,"design your concrete structure","concrete structure"),
    (7.64,8.68,"select your formwork","formwork"),
    (8.68,9.78,"and get an instant price","instant price","top"),
], VO_IN, t2)
C += caps([
    (10.82,12.32,"It's then cut by us",None),
    (12.32,13.36,"and sent out to site",None),
    (13.36,14.44,"with the set-out drawings","set-out drawings"),
], S3["in"], t3)
edl = dict(fps=30, segments=[S1,S2,S3], captions=C)
Path("cut3.json").write_text(json.dumps(edl, indent=1))
subprocess.run(["python3","assemble.py","cut3.json","out/formwork-builder-cut3.mp4"], check=True)
