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

## Cut 7 additions (18 Sep, evening)

| File | Does |
|---|---|
| `record-formwork-builder-closeup.mjs` | Records only the 3D viewer at full frame (config panel moved off-screen, inputs driven via DOM events so the model still updates and the formwork ticks register) |
| `overlays.py` | Draws the brand overlays with Pillow straight from the TTFs: green banner + logo, the homepage hero slide rebuilt at 9:16, and the spec stamps (R1300 / FORMWORK SELECTED / $675) |
| `build_mid2.py` | Composites hero → close-up model → ply hold with the stamps fading in, under the 6013 voice |
| `assets/` | Craftons logo and the homepage bench photo, pulled from craftons.com.au |

**Fonts:** the woff2 files in `remotion/public/fonts` are Google-Fonts subsets with almost no glyphs — converting
them to TTF gives boxes. Full fonts come from rsms/inter and JetBrains/JetBrainsMono releases and the
google/fonts repo (Big Shoulders as a variable font). Put them in `fonts/`. This also means the Remotion
compositions' condensed numerals fall back in this sandbox.

**zoompan gotcha:** its `d=` is frames *per input frame*. Feed it one frame, never a looped image.

## Cut 10 (19 Sep, overnight) — split-screen

| File | Does |
|---|---|
| `split-layout.mjs` | Restyles the live Formwork Builder into a 1080×1920 split: 3D viewer fixed in the top half, config panel (zoomed 2×) in the bottom half. Both moved to `body` so no ancestor clips them |
| `record-split.mjs` | The take: zoom in, orbit by mouse-drag, radius/height, backrest (taper 15°), cantilever (200 deep), formwork ticks, pan across the ply, order summary. Prints timestamped marks |
| `build_mid3.py` | Picks sub-clips from the marks, retimes them under the 6013 voice, hero slide in front, banner + green seam bar on top. No text over the iframe |
| `capcut_draft2.py` | Layered CapCut draft: pre-renders the four retimed sub-clips as small files, fills the durations the library leaves at zero, strips the two raw phone clips (Lee has them) |

**Gotchas:** headless three.js at 1080×960 paints ~5 fps, so an orbit of 50 mouse steps takes 60–100 s of
wall-clock and the raw take runs 6–7 minutes; it looks smooth once sped up 20–60× because every captured
frame is a distinct pose. `pkill -f <script>` kills the shell that ran it too — use `pgrep -f "[n]ode …"`.
The app intermittently never mounts its canvas under load; the recorder screenshots `fail.png` when that happens.
