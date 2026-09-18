#!/usr/bin/env python3
"""assemble.py EDL.json out.mp4 — render a 1080x1920 reel from a cut list.

EDL: {"fps":30, "segments":[
        {"src":"src/IMG_5999.mov","in":1.2,"out":4.8},            # clip slice (autorotated, cover-cropped to 9:16)
        {"card":"SCREEN RECORDING","dur":8.0}                     # solid brand-green placeholder with a label
      ],
      "captions":[{"start":0.0,"end":2.1,"text":"since word spread about the Radius Pro","hi":"Radius Pro"}]}
Captions: Inter SemiBold, white + shadow, one term highlighted #2d8a5b, sitting above the bottom 672px band.
"""
import json, subprocess, sys, tempfile, shlex
from pathlib import Path
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
FONTS = str(Path(__file__).parent / "fonts")
W, H = 1080, 1920
GREEN = "&H005B8A2D"   # ASS is BGR: #2d8a5b -> 5B 8A 2D

def ass_time(t):
    h, m = divmod(t, 3600); m, s = divmod(m, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

def write_ass(caps, path, label=None):
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter SemiBold,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,3,2,80,80,720,1
Style: CapTop,Inter SemiBold,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,3,8,80,80,300,1
Style: Card,Big Shoulders Display Thin,150,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,4,0,1,0,0,5,80,80,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for c in caps:
        txt = c["text"]
        if c.get("hi") and c["hi"] in txt:
            txt = txt.replace(c["hi"], "{\\c" + GREEN + "}" + c["hi"] + "{\\c&H00FFFFFF&}")
        style = "CapTop" if c.get("pos") == "top" else "Cap"
        lines.append(f"Dialogue: 0,{ass_time(c['start'])},{ass_time(c['end'])},{style},,0,0,0,,{txt}")
    if label:
        lines.append(f"Dialogue: 0,{ass_time(0)},{ass_time(label[1])},Card,,0,0,0,,{label[0]}")
    Path(path).write_text(hdr + "\n".join(lines) + "\n")

def main():
    edl = json.loads(Path(sys.argv[1]).read_text()); out = sys.argv[2]
    fps = edl.get("fps", 30); tmp = Path(tempfile.mkdtemp(prefix="asm_"))
    parts, t = [], 0.0
    for i, s in enumerate(edl["segments"]):
        p = tmp / f"seg{i:02d}.mp4"
        if "src" in s:
            dur = s["out"] - s["in"]
            vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps},format=yuv420p"
            cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(s["in"]), "-t", str(dur),
                   "-i", s["src"], "-vf", vf, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000", "-ac", "2",
                   "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "160k", str(p)]
        else:
            dur = s["dur"]; ass = tmp / f"card{i:02d}.ass"
            write_ass([], ass, label=(s["card"], dur))
            cmd = [FF, "-hide_banner", "-loglevel", "error", "-y",
                   "-f", "lavfi", "-i", f"color=c=0x194431:s={W}x{H}:d={dur}:r={fps}",
                   "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={dur}",
                   "-vf", f"subtitles={ass}:fontsdir={FONTS},format=yuv420p", "-shortest",
                   "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "160k", str(p)]
        subprocess.run(cmd, check=True); parts.append(p); s["_start"] = t; t += dur
    lst = tmp / "list.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
    joined = tmp / "joined.mp4"
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(joined)], check=True)
    ass = tmp / "caps.ass"; write_ass(edl.get("captions", []), ass)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(joined),
                    "-vf", f"subtitles={ass}:fontsdir={FONTS}", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", out], check=True)
    print(f"rendered {out}  ({t:.1f}s, {len(parts)} segments)")

if __name__ == "__main__": main()
