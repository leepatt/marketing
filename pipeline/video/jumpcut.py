#!/usr/bin/env python3
"""
jumpcut.py — turn a raw talking-head clip into a continuous, pause-free Reel cut.

What it does (the exact process used for the Radius Pro Reel, 2026-09-04):
  1. extract mono 16 kHz audio
  2. ffmpeg silencedetect  -> every pause >= --min-cut seconds
  3. faster-whisper (medium, filler-word prompt) -> word timestamps, flags "um/uh/er..."
  4. build keep-list: cut each long pause down to 2x --pad handles, drop fillers, merge
  5. render with select/aselect + loudnorm -> 1080x1920 H.264/AAC 48 kHz, faststart
  6. write <out>.cut-sheet.txt (original-timecode EDL) so a second angle
     (e.g. a screen recording) can be cut to the same list later.

Usage:
  python3 jumpcut.py IN.MOV OUT.mp4 [--min-cut 0.6] [--pad 0.12] [--noise -35]
                                    [--model medium] [--no-fillers] [--preview]
  --preview also writes OUT-preview.mp4 (540x960, ~6 MB) for phone review.

Needs: ffmpeg (imageio-ffmpeg wheel is enough: pip install imageio-ffmpeg faster-whisper).
Whisper on CPU: ~1x realtime for "medium", ~4x for "small".
"""
import argparse, json, os, re, subprocess, sys

def ffmpeg_bin():
    try:
        import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"

def run(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)

def duration(ff, path):
    out = subprocess.run([ff, "-i", path], text=True, capture_output=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    h, mi, s = m.groups(); return int(h)*3600 + int(mi)*60 + float(s)

def silences(ff, wav, noise, min_len):
    out = subprocess.run([ff, "-i", wav, "-af", f"silencedetect=noise={noise}dB:d={min_len}", "-f", "null", "-"],
                         text=True, capture_output=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends   = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(starts, ends))

FILLERS = {"um", "uh", "er", "erm", "ah", "hmm", "mm"}
def fillers(wav, model):
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(wav, word_timestamps=True, language="en", vad_filter=False,
                           condition_on_previous_text=False,
                           initial_prompt="Um, uh, so, um, you know, like, uh, we're going to, um, do this.")
    hits, words = [], []
    for s in segs:
        for w in s.words or []:
            words.append({"w": w.word, "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)})
            if w.word.strip().lower().strip(",.?!") in FILLERS:
                hits.append((w.start - 0.04, w.end + 0.04))
    return hits, words

def build_keeps(dur, sil, fill, min_cut, pad):
    removes = []
    for s, e in sil:
        if s < 0.05:           removes.append((0.0, max(0.0, e - 0.2)))   # head
        elif e > dur - 0.3:    removes.append((s + 0.4, dur))             # tail
        elif e - s >= min_cut: removes.append((s + pad, e - pad))
    removes += fill
    removes.sort(); merged = []
    for s, e in removes:
        if merged and s <= merged[-1][1] + 0.05: merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else: merged.append((s, e))
    keeps, t = [], 0.0
    for s, e in merged:
        if s - t >= 0.1: keeps.append((t, s))
        t = e
    if dur - t >= 0.1: keeps.append((t, dur))
    return keeps

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--min-cut", type=float, default=0.6)
    ap.add_argument("--pad", type=float, default=0.12)
    ap.add_argument("--noise", type=float, default=-35)
    ap.add_argument("--model", default="medium")
    ap.add_argument("--no-fillers", action="store_true")
    ap.add_argument("--crf", type=int, default=20)
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    ff = ffmpeg_bin(); base = os.path.splitext(a.out)[0]
    wav = base + ".16k.wav"
    run([ff, "-y", "-loglevel", "error", "-i", a.src, "-vn", "-ac", "1", "-ar", "16000", wav])
    dur = duration(ff, a.src)
    sil = silences(ff, wav, a.noise, 0.4)
    fill, words = ([], []) if a.no_fillers else fillers(wav, a.model)
    json.dump(words, open(base + ".words.json", "w"))
    keeps = build_keeps(dur, sil, fill, a.min_cut, a.pad)
    kept = sum(e - s for s, e in keeps)
    print(f"source {dur:.1f}s -> cut {kept:.1f}s  ({len(keeps)} segments, {len(fill)} fillers removed)")
    expr = "+".join(f"between(t,{s:.3f},{e:.3f})" for s, e in keeps)
    fscript = base + ".filter.txt"
    open(fscript, "w").write(
        f"[0:v]select='{expr}',setpts=N/FRAME_RATE/TB[v];"
        f"[0:a]aselect='{expr}',asetpts=N/SR/TB,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]")
    run([ff, "-y", "-loglevel", "error", "-i", a.src, "-filter_complex_script", fscript,
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf),
         "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-movflags", "+faststart", a.out])
    lines = ["# cut sheet — times in ORIGINAL source seconds; apply to a second angle after aligning starts",
             "# out_start  src_in   src_out  duration"]
    t = 0.0
    for s, e in keeps:
        lines.append(f"{t:8.2f}  {s:7.2f}  {e:7.2f}  {e-s:6.2f}"); t += e - s
    open(base + ".cut-sheet.txt", "w").write("\n".join(lines) + "\n")
    if a.preview:
        run([ff, "-y", "-loglevel", "error", "-i", a.out, "-vf", "scale=540:960", "-c:v", "libx264",
             "-preset", "fast", "-crf", "27", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart",
             base + "-preview.mp4"])
    os.remove(wav)
    print("wrote", a.out, "and", base + ".cut-sheet.txt")

if __name__ == "__main__":
    main()
