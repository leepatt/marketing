# pipeline/video — talking head + product demo → 9:16 reel, made in a session

Everything here ran end to end on 2026-09-11 for the Formwork Builder soft-launch reel, and on 2026-09-04
for the first Radius Pro reel. Two kinds of source, one output: a 1080×1920 H.264 reel with karaoke captions.

| Stage | Tool | Notes |
|---|---|---|
| Pull Lee's phone take | `curl` from a link-shared Drive file (`drive.usercontent.google.com/download?id=…&confirm=t`) | 300 MB is fine. The Drive connector cannot move video. |
| Jump-cut + transcribe | `jumpcut.py IN.MOV cut/phone-cut.mp4 --preview` | silencedetect + faster-whisper medium. Writes `words.json` (source time) + `cut-sheet.txt`. |
| Cut-timeline words | re-run faster-whisper on the cut (see `REEL-PROCESS.md`) → `out-words.json` | Captions must come from the cut, not the source. Proofread: 17mm, cantilever, formworkers, delivered. |
| Builder footage | `builder-capture/` | Real UI, captured headless in the sandbox. See below. |
| Assemble | `hyperframes/fw-reel/` | HyperFrames composition: intro clip → demo clip with punch-ins → end card, voiceover under it all. |
| Captions | `captions-highlight.py out-words.json caps.ass` then ffmpeg `ass=` burn-in | Locked style: Inter Bold, Craftons green, live word in line green, 2×2 words. 9:16: `SIZE=72 BOTTOM=1478 PLAYH=1920 BOX=0 HL=linegreen`. |
| Legacy compositor | `compose-reel.sh` + `overlays.py` | The ffmpeg-only path from reel 01 (screen recording + PiP). Still valid when Lee screen-records himself. |

## builder-capture/ — filming the live builder without a phone

Headless Chrome in the Claude sandbox cannot reach the internet directly (the egress proxy drops Chrome's TLS),
so `rproxy.mjs` runs a tiny reverse proxy on `127.0.0.1:8787` that forwards to `builder.craftons.com.au` through
Node's proxy-aware fetch. Chrome loads `http://127.0.0.1:8787/apps/formwork` and renders the real app, Three.js
preview included, on software WebGL.

```bash
NODE_USE_ENV_PROXY=1 node rproxy.mjs &                 # RPROXY_ORIGIN overrides the target
CAP_URL=http://127.0.0.1:8787/apps/formwork node capture-fw.mjs   # → cap/frames/*.png + cap/steps.json
python3 build-demo.py cues.json demo.mp4 --length 78.1  # lay steps onto the voiceover timeline
```

- `capture-fw.mjs` is a scripted walkthrough (shapes → dimensions → straights → angle → rounded ends → backrest →
  cantilever → plates/shutters/end caps → summary). It types values React-safely (native setter + `input` event),
  clicks rows by their label text, pins the 3D preview to the top of the viewport, disables CSS transitions so the
  ~8 fps screencast captures every discrete change, and records each step's frames with timestamps.
- `build-demo.py` places each step at its cue (seconds after the cut to the builder), holds the final frame until
  the next cue, and speeds a step up (never below 0.45×) if it would overrun its voiceover slot.
- Cues come from the cut sheet: `jumpcut.py` prints source→output mapping; the beat map for this reel is
  `cues-formwork-soft-launch.json`.
- Known limits: the interaction is a cursor-less typed demo (no thumb). Switching shapes resets the angle, so type
  the angle after the final shape. On the blank `/apps/formwork` route the Plates/Shutters/End Caps rows are
  toggled by clicking their label text; the In/Out/Both buttons appear after that.

## Sandbox gotchas (solved, do not re-solve)
- Playwright's ffmpeg has no H.264/MP4: use `@ffmpeg-installer/linux-x64` + `@ffprobe-installer/linux-x64` (npm).
- Google Fonts are unreachable from headless Chrome: self-host woff2 (fontsource) + Aeonik from Drive.
- HyperFrames `<audio>` needs an `id` or it renders silent.
- The old static ffmpeg build has no `xstack fill`; use `concat,tile` for contact sheets.
- `pip install` can time out on files.pythonhosted.org; retry with `--timeout 120`.
