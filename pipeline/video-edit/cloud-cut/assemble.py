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
Style: Seam,Inter SemiBold,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,80,80,0,1
Style: Card,Big Shoulders Display Thin,150,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,4,0,1,0,0,5,80,80,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for c in caps:
        txt = c["text"]
        if c.get("hi") and c["hi"] in txt:
            txt = txt.replace(c["hi"], "{\\c" + GREEN + "}" + c["hi"] + "{\\c&H00FFFFFF&}")
        style = {"top":"CapTop","seam":"Seam"}.get(c.get("pos"), "Cap")
        pos = "{\\pos(540,960)}" if style == "Seam" else ""
        lines.append(f"Dialogue: 0,{ass_time(c['start'])},{ass_time(c['end'])},{style},,0,0,0,,{pos}{txt}")
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
            dur = round((s["out"] - s["in"]) * fps) / fps      # whole frames, so the computed timeline is the real one
            vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps}"
            if s.get("push"):   # slow push-in over the segment: crop tightens with t, then rescale. ~6% over the clip
                k = float(s["push"]); nf = int(dur*fps)
                vf += f",zoompan=z='1+{k}*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={fps}"
            if s.get("card"):   # end card faded in over the clip's own picture; the clip's audio carries on underneath
                at = float(s["card_at"])
                vf += (f"[base];movie={s['card']},loop=loop=-1:size=1,setpts=N/{fps}/TB,scale={W}:{H},format=rgba,"
                       f"fade=t=in:st={at}:d=0.25:alpha=1[card];[base][card]overlay=0:0:shortest=1")
            vf += f",format=yuv420p,tpad=stop_mode=clone:stop_duration=1"   # picture never ends early
            cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(s["in"]), "-t", str(dur + 0.3),   # read extra, trim on output: never pad with zeros
                   "-i", s["src"], "-filter_complex" if s.get("card") else "-vf", ("[0:v]" + vf) if s.get("card") else vf,
                   "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad"
                          + (f",afade=t=out:st={dur-0.9:.3f}:d=0.9" if s.get("fade_out") else ""),   # no dip-to-zero at cuts: that IS a dropout
                   "-ac", "2", "-t", f"{dur:.4f}",
                   "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "160k", str(p)]
        else:
            dur = s["dur"]; ass = tmp / f"card{i:02d}.ass"
            write_ass([], ass, label=(s["card"], dur))
            cmd = [FF, "-hide_banner", "-loglevel", "error", "-y",
                   "-f", "lavfi", "-i", f"color=c=0x194431:s={W}x{H}:d={dur}:r={fps}",
                   "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={dur}",
                   "-vf", f"subtitles={ass}:fontsdir={FONTS},format=yuv420p", "-shortest",
                   "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "160k", str(p)]
        subprocess.run(cmd, check=True); parts.append(p); s["_start"] = t; s["_dur"] = dur; t += dur
    # --- picture: join video-only (stream copy is safe for video)
    lst = tmp / "list.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
    joined = tmp / "joined.mp4"
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-an", "-c", "copy", str(joined)], check=True)
    # --- sound: decode each part to PCM, cut to an exact sample count, join in ONE buffer, encode once.
    # Joining compressed AAC by stream copy leaves ~21 ms of encoder priming silence at every cut.
    import numpy as _np, wave as _wave
    SR = 48000; bufs = []
    for p, sgm in zip(parts, edl["segments"]):
        n = int(round(sgm["_dur"] * SR))
        af = "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000" + (f",afade=t=out:st={sgm['_dur']-0.9:.3f}:d=0.9" if sgm.get("fade_out") else "")
        x = _np.frombuffer(subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-ss", str(sgm["in"]), "-t", f"{sgm['_dur']+0.3:.4f}",
                                          "-i", sgm["src"], "-vn", "-af", af, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                                          capture_output=True, check=True).stdout, dtype=_np.float32).reshape(-1, 2)   # straight from the source, no compressed intermediate
        if len(x) < n:      # safety net only: top up with room tone from just BEFORE the decoder's end padding
            print(f"  note: {p.name} audio {len(x)/SR:.3f}s < {n/SR:.3f}s, topping up {(n-len(x))/SR*1000:.0f} ms")
            body = x[:-960] if len(x) > 4800 else x
            tail = body[-2400:]
            x = _np.concatenate([x] + [tail] * (1 + (n - len(x)) // max(1, len(tail))))
        bufs.append(x[:n])
    track = _np.concatenate(bufs)
    for a, b, g in edl.get("audio_ramps", []):          # sample-exact level eases: gain 1 -> g over [a, b]
        i0, i1 = int(a * SR), int(b * SR); ramp = _np.linspace(1.0, g, max(1, i1 - i0))[:, None]
        track[i0:i1] *= ramp
    track = _np.clip(track, -1, 1)
    wav = tmp / "soundtrack.wav"
    with _wave.open(str(wav), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((track * 32767).astype(_np.int16).tobytes())
    ass = tmp / "caps.ass"; write_ass(edl.get("captions", []), ass)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(joined), "-i", str(wav), "-map", "0:v", "-map", "1:a",
                    "-vf", f"subtitles={ass}:fontsdir={FONTS}", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "19", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", out], check=True)
    print(f"rendered {out}  ({t:.1f}s, {len(parts)} segments)")
    # --- dead-air guard: frames can't show silence, so measure it. Any gap over MAX_GAP fails the render.
    import re as _re
    MAX_GAP = float(edl.get("max_gap", 0.5))
    r = subprocess.run([FF, "-hide_banner", "-i", out, "-af", "silencedetect=noise=-40dB:d=0.3", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    starts = [float(x) for x in _re.findall(r"silence_start: ([\d.]+)", r)]
    ends   = [(float(a), float(b)) for a, b in _re.findall(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", r)]
    gaps = [(round(e - d, 2), round(e, 2), round(d, 2)) for e, d in ends]
    if len(starts) > len(ends): gaps.append((round(starts[-1], 2), round(t, 2), round(t - starts[-1], 2)))
    inner = [g for g in gaps if g[0] > 0.15 and g[1] < t - 0.15]          # ignore the very start and tail
    print("silences (start, end, dur):", gaps or "none")
    bad = [g for g in inner if g[2] > MAX_GAP]
    if bad:
        print(f"DEAD AIR: {bad}  (limit {MAX_GAP}s)"); sys.exit(2)
    print(f"dead-air check passed: no gap over {MAX_GAP}s")
    # --- dropout guard: inserted digital silence (exact zeros) plays as a dropout, unlike real room tone
    import numpy as _np
    pcm = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-i", out, "-vn", "-ac", "1", "-ar", "48000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = _np.frombuffer(pcm, dtype=_np.int16); z = (_np.abs(a) <= 2).astype(_np.int8)
    edges = _np.diff(_np.concatenate(([0], z, [0]))); st = _np.where(edges == 1)[0]; en = _np.where(edges == -1)[0]
    runs = [(round(s_/48000, 3), round((e_-s_)/48000, 3)) for s_, e_ in zip(st, en) if (e_-s_) > 0.02*48000 and 0.1*48000 < s_ < len(a)-0.1*48000]
    # near-silent dips too (encoder priming gaps are quiet, not exact zero): 5 ms windows below -65 dBFS for >= 10 ms
    f5 = a.astype(_np.float32) / 32768; w5 = 240
    lv = 20*_np.log10(_np.sqrt(_np.mean(f5[:len(f5)//w5*w5].reshape(-1, w5)**2, axis=1)) + 1e-9)
    low = (lv < -65).astype(_np.int8); ed = _np.diff(_np.concatenate(([0], low, [0])))
    dips = [(round(s_*w5/48000, 3), round((e_-s_)*w5/48000, 3)) for s_, e_ in zip(_np.where(ed == 1)[0], _np.where(ed == -1)[0])
            if (e_-s_) >= 2 and 0.1*48000 < s_*w5 < len(a) - (1.0 if edl["segments"][-1].get("fade_out") else 0.1)*48000]   # the closing fade-out is intended
    runs += dips
    if runs:
        print(f"DROPOUT (digital silence / near-silent dip) at {runs}"); sys.exit(3)
    print("dropout check passed: no digital silence over 20 ms")
    # --- tail guard: the last word must finish well before the video ends (frames can't show a clipped word)
    MIN_TAIL = float(edl.get("min_tail", 0.8))
    f32 = a.astype(_np.float32) / 32768; fr = 2400
    db = 20*_np.log10(_np.sqrt(_np.convolve(f32**2, _np.ones(fr)/fr, "valid")[::fr//2]) + 1e-9)
    thr = max(-38.0, _np.percentile(db, 90) - 18)
    last = _np.where(db > thr)[0]; last_t = (last[-1] * (fr//2) + fr) / 48000 if len(last) else 0
    tail = len(a)/48000 - last_t
    print(f"tail check: last speech ends {last_t:.2f}s, video ends {len(a)/48000:.2f}s, tail {tail:.2f}s")
    if tail < MIN_TAIL: print(f"TAIL TOO SHORT (< {MIN_TAIL}s): last word is clipped or rushed"); sys.exit(4)

if __name__ == "__main__": main()
