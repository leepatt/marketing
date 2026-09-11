#!/usr/bin/env python3
"""build-demo.py — lay captured builder steps onto the voiceover (cut) timeline and encode demo.mp4.
Reads cap/steps.json (from capture-fw.mjs) and a cue map {step-name: start-seconds-in-demo}. Each step plays at its
real captured timing from its cue (or right after the previous step if that ran long), then holds its final frame.
Usage: build-demo.py CUES.json OUT.mp4 [--length SECONDS] [--fps 30]"""
import json, sys, subprocess, argparse, os
ap = argparse.ArgumentParser(); ap.add_argument('cues'); ap.add_argument('out'); ap.add_argument('--length', type=float, required=True); ap.add_argument('--fps', type=int, default=30)
ap.add_argument('--steps', default='cap/steps.json'); ap.add_argument('--frames', default='cap/frames')
a = ap.parse_args()
FF = os.environ.get('FFMPEG', 'ffmpeg')
steps = json.load(open(a.steps)); cues = json.load(open(a.cues))
timeline = []  # (file, start, end)
t = 0.0; prev_end = 0.0
for i, s in enumerate(sorted([x for x in steps if x['name'] in cues], key=lambda x: cues[x['name']])):
    cue = cues.get(s['name'])
    start = max(cue, prev_end)
    fr = s['frames']
    # fit the step to its voiceover slot: if it runs longer than the gap to the next cue, play it faster (never below 0.45x)
    ordered = sorted(cues.values()); nxt = next((c for c in ordered if c > cue), None)
    slot = (nxt - start) if nxt is not None else fr[-1]['t']
    k = 1.0 if fr[-1]['t'] <= slot or slot <= 0 else max(0.45, slot / fr[-1]['t'])
    fr = [dict(f, t=round(f['t'] * k, 4)) for f in fr]
    if k < 1: print(f"  {s['name']}: {fr[-1]['t']/k:.2f}s -> fit to {slot:.2f}s (x{1/k:.2f})")
    for j, f in enumerate(fr):
        f0 = start + f['t']; f1 = start + (fr[j+1]['t'] if j+1 < len(fr) else f['t'])
        if j+1 < len(fr): timeline.append((f['file'], f0, f1))
        else: timeline.append((f['file'], f0, None))   # hold until next step
    prev_end = start + fr[-1]['t']
# resolve holds
for i, (f, s0, s1) in enumerate(timeline):
    if s1 is None:
        nxt = next((x[1] for x in timeline[i+1:] if True), None)
        timeline[i] = (f, s0, nxt if nxt is not None else a.length)
# leading gap: hold the first frame from 0
if timeline and timeline[0][1] > 0: timeline.insert(0, (timeline[0][0], 0.0, timeline[0][1]))
timeline[-1] = (timeline[-1][0], timeline[-1][1], max(timeline[-1][2], a.length))
lines = ['ffconcat version 1.0']
for f, s0, s1 in timeline:
    d = max(1.0 / a.fps, s1 - s0)
    lines.append(f"file '{os.path.abspath(os.path.join(a.frames, f))}'"); lines.append(f'duration {d:.4f}')
lines.append(f"file '{os.path.abspath(os.path.join(a.frames, timeline[-1][0]))}'")
open(a.out + '.concat.txt', 'w').write('\n'.join(lines) + '\n')
subprocess.run([FF, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', a.out + '.concat.txt', '-vf', f'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=white,fps={a.fps},format=yuv420p', '-t', str(a.length), '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-movflags', '+faststart', a.out], check=True)
print(f'wrote {a.out}: {len(timeline)} frame spans, {a.length}s; steps placed at:')
for s in steps:
    if s['name'] in cues: print(f"  {s['name']:20s} cue {cues[s['name']]:6.2f}")
