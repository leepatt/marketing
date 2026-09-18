#!/usr/bin/env python3
"""prep.py — probe, frame-grab and transcribe every clip in src/.
Writes prep/<clip>/{probe.json,frames/*.jpg,transcript.json,transcript.md}
I can't watch video; the frames are how I see it, the transcript is how I hear it."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, "/home/user/marketing/pipeline/video-edit")
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
FFPROBE = FF.replace("ffmpeg", "ffprobe")
SRC, OUT = Path("src"), Path("prep")

def probe(p):
    # ffprobe isn't shipped with imageio; parse ffmpeg -i stderr instead
    r = subprocess.run([FF, "-hide_banner", "-i", str(p)], capture_output=True, text=True)
    return r.stderr

def frames(p, d, every=2.0):
    d.mkdir(parents=True, exist_ok=True)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-i", str(p),
                    "-vf", f"fps=1/{every},scale=-2:480", "-q:v", "4", str(d / "f%03d.jpg")], check=True)
    return sorted(d.glob("*.jpg"))

for clip in sorted(SRC.iterdir()):
    if clip.suffix.lower() not in {".mov", ".mp4"}: continue
    d = OUT / clip.stem; d.mkdir(parents=True, exist_ok=True)
    info = probe(clip); (d / "probe.txt").write_text(info)
    fr = frames(clip, d / "frames")
    print(f"== {clip.name}: {len(fr)} frames")
    for line in info.splitlines():
        if any(k in line for k in ("Duration", "Stream", "rotate", "displaymatrix")):
            print("  ", line.strip()[:140])
    r = subprocess.run([sys.executable, "/home/user/marketing/pipeline/video-edit/transcribe.py",
                        str(clip), "--out", str(d), "--model", "small"], capture_output=True, text=True)
    print("  ", (r.stdout.strip().splitlines() or ["(no transcript output)"])[-1])
    if r.returncode: print("   transcribe stderr:", r.stderr.strip()[-300:])
