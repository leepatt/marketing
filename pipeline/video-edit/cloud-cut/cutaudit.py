#!/usr/bin/env python3
"""cutaudit.py — measure speech energy at every in/out point. Reports where each word REALLY starts/ends near a
cut and whether the cut lands inside speech. Whisper word times are not trusted for cuts."""
import subprocess, numpy as np, imageio_ffmpeg, sys, json
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 48000; HOP = 0.01
def env(src, a, b):
    x = np.frombuffer(subprocess.run([FF,"-hide_banner","-loglevel","error","-ss",str(max(0,a)),"-t",str(b-a),"-i",src,"-vn","-ac","1","-ar",str(SR),"-f","f32le","-"],
                      capture_output=True, check=True).stdout, dtype=np.float32)
    w = int(0.02*SR); h = int(HOP*SR)
    return 20*np.log10(np.sqrt(np.convolve(x**2, np.ones(w)/w, "valid")[::h]) + 1e-9)
def audit(src, t, kind, look=1.2):
    """kind='out': where does speech before t really end? kind='in': where does speech after t really start?"""
    whole = env(src, 0, 60); floor = np.percentile(whole, 15); thr = floor + 10
    if kind == "out":
        a = t - look; e = env(src, a, t + look); on = np.where(e > thr)[0]
        before = on[on*HOP + a <= t + 0.6]       # speech that belongs to the phrase ending at this cut
        end = a + (before[-1]+2)*HOP if len(before) else None
        inside = e[int((look-0.03)/HOP):int((look+0.03)/HOP)].max() > thr
        return f"OUT {t:6.2f}: speech really ends {end:6.2f} -> {'CLIPS THE WORD' if end and end > t else 'clean'}  (margin {t-end:+.2f}s)"
    else:
        a = t - 0.6; e = env(src, a, t + look); on = np.where(e > thr)[0]
        after = on[on*HOP + a >= t - 0.6]
        start = a + (after[0]-2)*HOP if len(after) else None
        return f"IN  {t:6.2f}: speech really starts {start:6.2f} -> {'CLIPS THE WORD' if start and start < t else 'clean'}  (lead {start-t:+.2f}s)"
if __name__ == "__main__":
    for src, t, kind in json.loads(sys.argv[1]): print(f"{src.split('/')[-1]:14}", audit(src, t, kind))
