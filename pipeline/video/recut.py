#!/usr/bin/env python3
"""recut.py — apply beat-level keep decisions on top of a jumpcut.py result.
Inputs: SRC video, the jumpcut words.json (source-time words) and cut-sheet.txt (pause-free source ranges),
and KEEP: a list of [first-phrase, last-phrase] pairs (normalised text) marking spans to keep, in order.
Output: OUT.mp4 (1080x1920 H.264/AAC, loudnorm) + OUT.cut-sheet.txt + OUT-preview.mp4.
Usage: recut.py SRC words.json cut-sheet.txt keeps.json OUT.mp4"""
import json, re, subprocess, sys, os
src, wordsf, sheetf, keepsf, out = sys.argv[1:6]
FF = os.environ.get('FFMPEG', 'ffmpeg')
norm = lambda s: re.sub(r"[^a-z0-9' ]", "", s.lower().replace("-", " ")).strip()
words = json.load(open(wordsf)); toks = [norm(w['w']) for w in words]
def find(phrase, start=0):
    p = norm(phrase).split()
    for i in range(start, len(toks) - len(p) + 1):
        if [t for t in toks[i:i+len(p)]] == p: return i
    raise SystemExit(f"phrase not found after word {start}: {phrase!r}")
keeps = json.load(open(keepsf)); spans = []; cursor = 0
for first, last in keeps:
    a = find(first, cursor); b = find(last, a); b_end = b + len(norm(last).split()) - 1
    spans.append((words[a]['s'] - 0.08, words[b_end]['e'] + 0.22)); cursor = b_end + 1
# intersect with the jumpcut pause-free ranges so pauses inside kept spans stay removed
pf = [(float(i), float(e)) for o, i, e, d in (l.split() for l in open(sheetf) if not l.startswith('#'))]
ranges = []
for s0, s1 in spans:
    for i, e in pf:
        a, b = max(s0, i), min(s1, e)
        if b - a > 0.08: ranges.append((a, b))
ranges.sort(); merged = []
for a, b in ranges:
    if merged and a <= merged[-1][1] + 0.05: merged[-1] = (merged[-1][0], max(merged[-1][1], b))
    else: merged.append((a, b))
kept = sum(b - a for a, b in merged)
expr = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in merged)
fscript = out + ".filter.txt"
open(fscript, 'w').write(f"[0:v]select='{expr}',setpts=N/FRAME_RATE/TB[v];[0:a]aselect='{expr}',asetpts=N/SR/TB,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]")
subprocess.run([FF, '-y', '-loglevel', 'error', '-i', src, '-filter_complex_script', fscript, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out], check=True)
lines = ['# cut sheet — times in ORIGINAL source seconds', '# out_start  src_in   src_out  duration']; t = 0.0
for a, b in merged: lines.append(f"{t:8.2f}  {a:7.2f}  {b:7.2f}  {b-a:6.2f}"); t += b - a
open(os.path.splitext(out)[0] + '.cut-sheet.txt', 'w').write("\n".join(lines) + "\n")
subprocess.run([FF, '-y', '-loglevel', 'error', '-i', out, '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', '27', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', os.path.splitext(out)[0] + '-preview.mp4'], check=True)
print(f"kept {kept:.1f}s in {len(merged)} ranges -> {out}")
