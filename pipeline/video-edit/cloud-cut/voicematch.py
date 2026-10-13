#!/usr/bin/env python3
"""voicematch.py — derive an ffmpeg EQ chain that makes the 6013 voice match the outdoor clips (5999 + 6001).
Measures average speech spectra in 1/3-octave bands, takes the difference, smooths and clamps it, and writes
voicematch.json {"eq": "<ffmpeg filter chain>", "bands": [...]}. Run with --check to measure the result."""
import subprocess, json, sys, numpy as np, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 48000
CENTRES = [100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000]
def pcm(src, ss, t, af=None):
    cmd=[FF,"-hide_banner","-loglevel","error","-ss",str(ss),"-t",str(t),"-i",src,"-vn","-ac","1","-ar",str(SR)]+(["-af",af] if af else [])+["-f","f32le","-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True,check=True).stdout,dtype=np.float32)
def speech_spectrum(x):
    n=4096; hop=2048; win=np.hanning(n); frames=[]
    for i in range(0,len(x)-n,hop):
        seg=x[i:i+n]
        if np.sqrt(np.mean(seg**2)) > 10**(-40/20): frames.append(np.abs(np.fft.rfft(seg*win))**2)   # speech frames only
    P=np.mean(frames,axis=0); f=np.fft.rfftfreq(n,1/SR)
    return np.array([10*np.log10(np.mean(P[(f>=c/2**(1/6))&(f<c*2**(1/6))])+1e-20) for c in CENTRES])
def rel(s): return s - s[CENTRES.index(1000)]     # shape only, normalised at 1 kHz
ref = (rel(speech_spectrum(pcm("src/IMG_5999.mov",1.86,8.19))) + rel(speech_spectrum(pcm("src/IMG_6001.mov",10.74,3.7))))/2
if "--check" in sys.argv:
    eq = json.load(open("voicematch.json"))["eq"]
    after = rel(speech_spectrum(pcm("src/IMG_6013.mov",2.1,7.3, eq)))
    before= rel(speech_spectrum(pcm("src/IMG_6013.mov",2.1,7.3)))
    print("band   ref   before  after")
    for c,r,b,a in zip(CENTRES,ref,before,after): print(f"{c:5d} {r:6.1f} {b:7.1f} {a:6.1f}")
    print(f"mean abs error vs outdoor: before {np.mean(np.abs(before-ref)):.1f} dB -> after {np.mean(np.abs(after-ref)):.1f} dB"); sys.exit()
src = rel(speech_spectrum(pcm("src/IMG_6013.mov",2.1,7.3)))
diff = ref - src
diff = np.convolve(np.pad(diff,1,mode='edge'), [0.25,0.5,0.25], 'valid')   # smooth across neighbours
diff = np.clip(diff, -10, 8)
chain = ",".join(f"equalizer=f={c}:t=o:w=0.33:g={g:.1f}" for c,g in zip(CENTRES,diff) if abs(g) >= 0.5)
chain = "highpass=f=80," + chain
json.dump({"eq": chain, "bands": [[c, round(float(g),1)] for c,g in zip(CENTRES,diff)]}, open("voicematch.json","w"), indent=1)
print("correction per band (dB):", " ".join(f"{c}:{g:+.1f}" for c,g in zip(CENTRES,diff)))
