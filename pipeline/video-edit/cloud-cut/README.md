# cloud-cut — editing from the cloud session (no CapCut needed)

What produced `formwork-builder-cut3.mp4` and the matching CapCut draft on 18 Sep 2026. Kept here so it
isn't lost between branches again.

| File | Does |
|---|---|
| `prep.py` | Probe, frame-grab (so Claude can *see* the clip) and transcribe every clip in `src/` |
| `record-formwork-builder.mjs` | Playwright screen-recording of the live Formwork Builder at 1080×1920. Page zoomed 2× so the app keeps its stacked phone layout. Trusts the proxy CA by SPKI pin |
| `build.py` | The edit: retimes screen sub-clips under the voice, computes caption timings from the transcript, renders via `assemble.py` |
| `assemble.py` | Generic renderer: EDL → 1080×1920 H.264 with burned ASS captions (Inter, green highlight, above the bottom 672px band), loudnorm per clip |
| `capcut_draft.py` | Same EDL → CapCut draft via VectCutAPI's Python layer, asset paths rewritten for Windows, zipped |
| `cut3.json` | The EDL that shipped |

**Needs:** `pip install faster-whisper imageio-ffmpeg fontTools brotli`, the brand woff2 fonts converted to
TTF in `fonts/`, and a clone of `sun-guannan/VectCutAPI` beside this folder with `stubs/oss2/` so the
cloud-upload dependency is never imported.

**Known limits:** Claude can't watch video, only frames and transcripts. The CapCut draft was written
without CapCut to test against. The Windows username in the draft paths is a placeholder (`LEE`).
