#!/usr/bin/env python3
"""build_mid2.py — the new middle section: hero slide -> close-up model with stamps -> price hold.
Voice: IMG_6013 2.10-9.78 (7.68s).  Banner on top throughout.  Writes src/mid2.mp4 and prints its duration."""
import subprocess, json
from pathlib import Path
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
VO_IN, VO_OUT = 2.1, 9.78; VO = VO_OUT - VO_IN
# word times inside the 6013 slice (t - VO_IN):  "So we built the Formwork Builder," 0.22-1.56 | "an online tool where you can" 2.2-3.44
# "design your concrete structure," 3.58-4.68 | "select your formwork" 5.54-6.08 | "and get an instant price." 6.58-7.32
HERO   = 1.9                       # hero slide, slow push-in, under "So we built the Formwork Builder"
M = [ # model.mp4 sub-clips: (in, out, speed)  -> concrete: radius+height change | formwork ticks | ply hold
    (17.0, 32.0, 5.0),            # 19s of slow input changes -> 4.75s  (under "an online tool ... concrete structure")
    (35.0, 44.0, 4.5),            # plates, shutters, end caps appear -> 3.4s (under "select your formwork")
]
model_dur = sum((b-a)/sp for a,b,sp in M)
HOLD = 2.2                         # ply model held with the price stamp (under "instant price" + a beat)
total = HERO + model_dur + HOLD
pad = max(0.0, total - VO)
print(f"hero {HERO}s | model {model_dur:.2f}s | hold {HOLD}s | total {total:.2f}s | voice {VO:.2f}s | pad {pad:.2f}s")

# overlay timings (absolute in mid2)
t_model = HERO
t_radius = t_model + 0.5                          # stamp-radius fades in once the model is up
t_form   = t_model + (M[0][1]-M[0][0])/M[0][2]    # stamp-formwork when the ticks segment starts
t_price  = t_model + model_dur                    # stamp-price on the hold
fade = 0.25
def ov(tag, start, end):   # enable window + alpha fade in/out on an overlay input
    return (f"[{tag}]format=rgba,fade=t=in:st={start}:d={fade}:alpha=1,fade=t=out:st={end-fade}:d={fade}:alpha=1[{tag}f]",
            f"enable='between(t,{start},{end})'")

ins = ["-i","ovl/hero.png"]
for a,b,sp in M: ins += ["-ss",str(a),"-t",str(b-a),"-i","src/model.mp4"]
ins += ["-loop","1","-t",str(HOLD),"-i","src/model-last.png"]          # hold on the final ply frame
n_vid = 1 + len(M) + 1
ins += ["-loop","1","-i","ovl/banner.png","-loop","1","-i","ovl/stamp-radius.png","-loop","1","-i","ovl/stamp-formwork.png","-loop","1","-i","ovl/stamp-price.png"]
i_ban, i_rad, i_frm, i_prc = n_vid, n_vid+1, n_vid+2, n_vid+3
ins += ["-ss",str(VO_IN),"-t",str(VO),"-i","src/IMG_6013.mov"]; i_aud = n_vid+4

fc = [f"[0:v]scale=1080:1920,zoompan=z='min(zoom+0.0009,1.08)':d={int(HERO*30)}:s=1080x1920:fps=30,trim=duration={HERO},setpts=PTS-STARTPTS,setsar=1[v0]"]
for k,(a,b,sp) in enumerate(M, start=1):
    fc.append(f"[{k}:v]setpts=PTS/{sp},scale=1080:1920,fps=30,setsar=1[v{k}]")
fc.append(f"[{n_vid-1}:v]scale=1080:1920,fps=30,setsar=1[v{n_vid-1}]")
fc.append("".join(f"[v{k}]" for k in range(n_vid)) + f"concat=n={n_vid}:v=1:a=0[base]")
# banner over everything after the hero (the hero already has it baked in)
fc.append(f"[base][{i_ban}:v]overlay=0:0:enable='gte(t,{HERO})'[b1]")
f1, e1 = ov(f"{i_rad}:v", t_radius, t_form-0.05);  fc += [f1, f"[b1][{i_rad}:vf]overlay=0:0:{e1}[b2]"]
f2, e2 = ov(f"{i_frm}:v", t_form, t_price-0.05);   fc += [f2, f"[b2][{i_frm}:vf]overlay=0:0:{e2}[b3]"]
f3, e3 = ov(f"{i_prc}:v", t_price, total);         fc += [f3, f"[b3][{i_prc}:vf]overlay=0:0:{e3}[vout]"]
fc.append(f"[{i_aud}:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad=pad_dur={pad:.3f}[aout]")

# last ply frame as a still for the hold
subprocess.run([FF,"-hide_banner","-loglevel","error","-y","-ss",str(M[-1][1]-0.1),"-i","src/model.mp4","-frames:v","1","src/model-last.png"],check=True)
subprocess.run([FF,"-hide_banner","-loglevel","error","-y",*ins,"-filter_complex",";".join(fc),"-map","[vout]","-map","[aout]",
    "-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-t",f"{total:.3f}","src/mid2.mp4"],check=True)
Path("mid2.json").write_text(json.dumps({"dur":round(total,3),"t_model":t_model,"t_form":round(t_form,3),"t_price":round(t_price,3)}))
print("mid2.mp4 ok")
