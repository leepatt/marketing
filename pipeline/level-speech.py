#!/usr/bin/env python3
"""Speech-aware gain riding for handheld-mic footage.

Fixes the "voice drops when I point the mic away" problem without lifting the gaps:
Whisper finds the words, only those stretches are boosted toward a target level
(capped, smoothed), and everything between words is left untouched.

Usage:
  pip install faster-whisper soundfile scipy numpy
  python3 pipeline/level-speech.py IN.MOV OUT.wav [--target -24] [--max-boost 18]

Then mux back:  ffmpeg -i IN.MOV -i OUT.wav -map 0:v -map 1:a -c:v copy -c:a aac OUT.mp4
"""
import argparse, subprocess
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
from scipy.ndimage import uniform_filter1d

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--target", type=float, default=-24.0, help="target speech RMS, dBFS")
ap.add_argument("--max-boost", type=float, default=18.0, help="max lift, dB (never cuts)")
args = ap.parse_args()

SR = 48000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", args.src, "-vn", "-ac", "1", "-ar", str(SR),
                      "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).copy()

# Where is speech? Word timestamps, padded 120 ms either side.
model = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, _ = model.transcribe(x[::3], language="en", word_timestamps=True)  # 48k -> 16k
mask = np.zeros(len(x), bool)
for s in segs:
    for w in s.words:
        mask[max(0, int((w.start - 0.12) * SR)):int((w.end + 0.12) * SR)] = True

# Gain: lift speech toward target (400 ms RMS window), unity elsewhere, 250 ms ramps.
rms = np.sqrt(uniform_filter1d(x ** 2, int(0.4 * SR)) + 1e-12)
gain = np.where(mask, np.clip(10 ** (args.target / 20) / rms, 1.0, 10 ** (args.max_boost / 20)), 1.0)
gain = uniform_filter1d(gain, int(0.25 * SR))
y = x * gain
peak = np.abs(y).max()
if peak > 0.89:
    y *= 0.89 / peak

sf.write(args.out, y, SR)
print(f"{args.src}: speech {mask.mean() * 100:.0f}% of clip, max boost {20 * np.log10(gain.max()):.1f} dB")
