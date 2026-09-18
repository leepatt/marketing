#!/usr/bin/env python3
"""capcut_draft2.py — layered CapCut draft for the split-screen cut. Every element on its own track so Lee can
nudge timings by hand: face clips | hero slide (image) | split-screen sub-clips (with speed) | banner + seam (images)
| voice (6013) | caption text.  Env: WIN_USER, MARKS (../rec3/marks.log), SPLIT (src/split.mp4)."""
import json, os, sys, threading, shutil, re, functools, http.server, socketserver
from pathlib import Path
HERE = Path(__file__).parent.resolve(); VC = HERE.parent / "VectCutAPI"
sys.path.insert(0, str(VC / "stubs")); sys.path.insert(0, str(VC)); os.chdir(VC)
import create_draft, add_video_track, add_audio_track, add_text_impl, add_image_impl, save_draft_impl
WIN_USER = os.environ.get("WIN_USER", "LEE"); PORT = 8770 + int(os.getpid()) % 200
socketserver.TCPServer.allow_reuse_address = True
WIN_DRAFTS = rf"C:\Users\{WIN_USER}\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft"
url = lambda rel: f"http://127.0.0.1:{PORT}/{rel}"

def main():
    edl = json.loads((HERE / sys.argv[1]).read_text()); mid = json.loads((HERE/"mid3.json").read_text())
    marks = {m.group(2): float(m.group(1)) for m in re.finditer(r"^([\d.]+)s\s+(.+)$", Path(os.environ.get("MARKS","../rec3/marks.log")).read_text(), re.M)}
    T = lambda k: marks[next(x for x in marks if x.startswith(k))]
    SUB = [(T("A start")+2.6, T("B height 600")+0.3), (T("C backrest on")-0.4, T("C orbit3")+0.2), (T("D tick Plates")-0.3, T("D orbit4")+0.1), (T("E order summary")-0.6, T("END"))]
    TARGET = mid["targets"]; HERO = mid["hero"]; split_src = os.environ.get("SPLIT","src/split.mp4")
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE)); srv = socketserver.TCPServer(("127.0.0.1", PORT), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    d = create_draft.create_draft(1080, 1920); did = d[1] if isinstance(d, tuple) else d["draft_id"]
    segs = edl["segments"]; s1, s2, s3 = segs
    t = 0.0
    add_video_track.add_video_track(video_url=url(s1["src"]), start=s1["in"], end=s1["out"], target_start=t, draft_id=did, track_name="main"); t += s1["out"]-s1["in"]
    t_mid = t
    add_image_impl.add_image_impl(image_url=url("ovl/hero.png"), start=t, end=t+HERO, draft_id=did, track_name="main", width=1080, height=1920)
    tt = t + HERO
    import subprocess, imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
    for i,((a,b),tgt) in enumerate(zip(SUB, TARGET), start=1):   # pre-render each retimed sub-clip as a small file (the raw take is 6+ min)
        sub = HERE/"src"/f"split-sub{i}.mp4"
        subprocess.run([FF,"-hide_banner","-loglevel","error","-y","-ss",f"{a:.2f}","-t",f"{b-a:.2f}","-i",str(HERE/split_src),"-vf",f"setpts=PTS/{(b-a)/tgt:.4f},fps=30","-an","-c:v","libx264","-preset","fast","-crf","18","-t",f"{tgt:.3f}",str(sub)],check=True)
        add_video_track.add_video_track(video_url=url(f"src/split-sub{i}.mp4"), start=0, end=tgt, target_start=tt, draft_id=did, track_name="main", volume=0.0); tt += tgt
    mid_dur = mid["dur"]
    add_image_impl.add_image_impl(image_url=url("ovl/seam.png"), start=t+HERO, end=t+mid_dur, draft_id=did, track_name="seam", width=1080, height=1920)
    add_image_impl.add_image_impl(image_url=url("ovl/banner.png"), start=t+HERO, end=t+mid_dur, draft_id=did, track_name="banner", width=1080, height=1920)
    add_audio_track.add_audio_track(audio_url=url("src/IMG_6013.mov"), start=2.1, end=9.78, target_start=t, draft_id=did, track_name="voice")
    t += mid_dur
    add_video_track.add_video_track(video_url=url(s3["src"]), start=s3["in"], end=s3["out"], target_start=t, draft_id=did, track_name="main")
    for c in edl["captions"]:
        y = {"top": 0.62, "seam": 0.0}.get(c.get("pos"), -0.25)
        add_text_impl.add_text_impl(text=c["text"], start=c["start"], end=c["end"], draft_id=did, font_color="#ffffff", font_size=8.0 if c.get("pos")!="seam" else 6.5,
                                    transform_y=y, shadow_enabled=(c.get("pos")!="seam"), shadow_alpha=0.8, shadow_distance=6.0, track_name="captions")
    r = save_draft_impl.save_draft_impl(did, draft_folder=None, auto_deploy=False); print("save:", r.get("success"))
    D = VC / did; local = str(D); WIN = WIN_DRAFTS + "\\" + did; n = 0
    for jf in D.glob("*.json"):
        s = jf.read_text(encoding="utf-8", errors="ignore")
        if local not in s: continue
        s, k = re.subn(r'"' + re.escape(local) + r'[^"]*"', lambda m: json.dumps(m.group(0)[1:-1].replace(local, WIN).replace("/", "\\")), s); jf.write_text(s, encoding="utf-8"); n += k
    # audio asset is the .mov bytes renamed .mp3 -> transcode to a real mp3; drop the big raw clips (Lee has them)
    # fill durations/sizes the library leaves at zero, from the real files (or known values for the two raw clips)
    KNOWN = {"IMG_5999": 13.33, "IMG_6001": 16.37}
    def dur_of(path):
        r = subprocess.run([FF,"-hide_banner","-i",str(path)],capture_output=True,text=True).stderr
        m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r); return int(m[1])*3600+int(m[2])*60+float(m[3]) if m else 0
    dj = json.load(open(D/"draft_info.json"))
    for m_ in dj["materials"]["videos"] + dj["materials"]["audios"]:
        f = D/"assets"/("video" if m_ in dj["materials"]["videos"] else "audio")/m_["path"].split("\\")[-1]
        if not m_.get("duration") and f.exists(): m_["duration"] = int(dur_of(f)*1e6)
        if m_ in dj["materials"]["videos"] and not m_.get("width"): m_["width"], m_["height"] = 1080, 1920
    json.dump(dj, open(D/"draft_info.json","w"), ensure_ascii=False)
    for a in (D/"assets/audio").glob("*.mp3"):
        subprocess.run([FF,"-hide_banner","-loglevel","error","-y","-i",str(HERE/"src/IMG_6013.mov"),"-vn","-c:a","libmp3lame","-b:a","192k",str(a)+".tmp.mp3"],check=True); os.replace(str(a)+".tmp.mp3", a)
    note = []
    for v in (D/"assets/video").glob("*.mp4"):
        if v.stat().st_size > 20_000_000:
            note.append(v.name); k = "IMG_5999" if v.stat().st_size < 30_000_000 else "IMG_6001"
            for m_ in dj["materials"]["videos"]:
                if m_["path"].endswith(v.name): m_["duration"] = int(KNOWN[k]*1e6)
            v.unlink()
    json.dump(dj, open(D/"draft_info.json","w"), ensure_ascii=False)
    (D/"PUT-YOUR-CLIPS-HERE.txt").write_text("Copy your originals into assets\\video\\ with these names:\n" + "\n".join(f"  {n}" for n in note) + "\n(IMG_5999.mov is the shorter one, IMG_6001.mov the longer; rename .mov -> .mp4)\n")
    out = HERE/"out"/"capcut-draft-split-slim"; shutil.make_archive(str(out), "zip", root_dir=VC, base_dir=did)
    print(f"paths rewritten: {n}; removed raw clips: {note}; zip: {out}.zip ({Path(str(out)+'.zip').stat().st_size/1e6:.1f} MB)"); srv.shutdown()
if __name__ == "__main__": main()
