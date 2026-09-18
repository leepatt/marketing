#!/usr/bin/env python3
"""capcut_draft.py EDL.json  — write a CapCut draft that mirrors the rendered cut, for manual edits on Lee's desktop.

Uses VectCutAPI's Python layer directly (no server, no CapCut needed here). Materials are served over a
local http server because the library downloads them by URL at save time. The draft is written locally,
then every asset path in draft_content.json is rewritten to the Windows CapCut drafts folder, and the
result is zipped.  Lee unzips it into:
   %LOCALAPPDATA%\\CapCut\\User Data\\Projects\\com.lveditor.draft\\
"""
import json, os, sys, threading, shutil, re, subprocess, functools, http.server, socketserver
from pathlib import Path
HERE = Path(__file__).parent.resolve()
VC = HERE.parent / "VectCutAPI"
sys.path.insert(0, str(VC / "stubs")); sys.path.insert(0, str(VC)); os.chdir(VC)
import create_draft, add_video_track, add_audio_track, add_text_impl, save_draft_impl

WIN_USER = os.environ.get("WIN_USER", "LEE")            # <-- Lee's Windows username
WIN_DRAFTS = rf"C:\Users\{WIN_USER}\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft"
PORT = 8765

def serve(root):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    srv = socketserver.TCPServer(("127.0.0.1", PORT), h); srv.allow_reuse_address = True
    threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv

def main():
    edl = json.loads((HERE / sys.argv[1]).read_text())
    srv = serve(HERE)
    url = lambda rel: f"http://127.0.0.1:{PORT}/{rel}"
    d = create_draft.create_draft(1080, 1920); did = d[1] if isinstance(d, tuple) else d["draft_id"]
    t = 0.0
    for s in edl["segments"]:
        dur = s["out"] - s["in"]
        if s["src"].endswith("mid.mp4"):
            # keep the editable pieces separate: screen picture on one track, 6013 voice on the audio track
            add_video_track.add_video_track(video_url=url("src/mid.mp4"), start=0, end=dur, target_start=t,
                                            draft_id=did, track_name="main", volume=0.0)
            add_audio_track.add_audio_track(audio_url=url("src/IMG_6013.mov"), start=2.1, end=9.78, target_start=t,
                                            draft_id=did, track_name="voice")
        else:
            add_video_track.add_video_track(video_url=url(s["src"]), start=s["in"], end=s["out"], target_start=t,
                                            draft_id=did, track_name="main")
        t += dur
    for c in edl["captions"]:
        add_text_impl.add_text_impl(text=c["text"], start=c["start"], end=c["end"], draft_id=did,
                                    font_color="#ffffff", font_size=8.0, transform_y=-0.25,
                                    shadow_enabled=True, shadow_alpha=0.8, shadow_distance=6.0,
                                    track_name="captions")
    r = save_draft_impl.save_draft_impl(did, draft_folder=None, auto_deploy=False)
    print("save:", {k: v for k, v in r.items() if k != "draft_url"})
    draft_dir = VC / did
    assert draft_dir.exists(), f"draft folder missing: {draft_dir}"
    # rewrite asset paths for Windows
    content = draft_dir / "draft_content.json"
    j = content.read_text()
    local_prefix = str(VC / did)
    win_prefix = WIN_DRAFTS + "\\" + did
    n = j.count(local_prefix)
    j = j.replace(local_prefix, win_prefix.replace("\\", "\\\\")).replace("/", "\\\\") if False else j.replace(local_prefix, win_prefix)
    # JSON needs backslashes escaped; do it only inside the paths we just wrote
    j = re.sub(re.escape(win_prefix) + r"[^\"]*", lambda m: m.group(0).replace("/", "\\").replace("\\", "\\\\"), j)
    content.write_text(j)
    out_zip = HERE / "out" / f"capcut-draft-{did}"
    shutil.make_archive(str(out_zip), "zip", root_dir=VC, base_dir=did)
    print(f"rewrote {n} asset paths -> {win_prefix}")
    print(f"zip: {out_zip}.zip")
    srv.shutdown()

if __name__ == "__main__": main()
