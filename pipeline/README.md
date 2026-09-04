# Craftons production pipeline

Turn a **content JSON** into a finished, on-brand image by rendering an **HTML/CSS template**
(styled with the Craftons design-system tokens) through a headless browser, then normalising with
sharp. Video assembly (ffmpeg) plugs in the same way later.

```
content/*.json  +  templates/*.html  ──render.mjs──▶  exports/*.png
        (the words)        (the design)         (the finished asset)
```

This is the execution end of the `craftons-design` skill: the skill holds the brand rules; this
pipeline produces the files.

## Setup (once)
```bash
cd pipeline
bash setup-media-tooling.sh      # ffmpeg, ImageMagick, SVG tools, fonts, playwright, sharp
```
On the Claude Code **cloud environment**, paste `setup-media-tooling.sh`'s body into the
environment's *Setup script* field so every (incl. mobile) session has it cached.

## Render
```bash
npm run render -- \
  --template templates/post-hero-1080x1350.html \
  --content  content/example-radius-pro.json \
  --out      exports/radius-pro.png
# optional: --width 1080 --height 1350 --scale 2
```

## How templating works
Templates contain `{{PLACEHOLDER}}` tokens; the content JSON supplies the values. Add a new post
by writing a new JSON in `content/` — no code changes. Add a new layout by writing a new HTML file
in `templates/` that `@import`s `../tokens.css` and uses `var(--token)` (never raw hex/px).

## Tokens — important
`tokens.css` is an **interim fallback** with confirmed brand values only. For the complete, exact
token set, replace it with the canonical `colors_and_type.css` from the Drive brain
(`00 Brain/Design-system/`, file id `1KMBH74vo-tSqim_7WnI9dFaee3aWuo9M`).

## Fonts
**Aeonik** (display) is licensed — its `.otf` files live in the Drive brain `fonts/`. Drop them into
`pipeline/fonts/` (git-ignored) and uncomment the install line in `setup-media-tooling.sh` so
headlines render in the real face. Until then Aeonik falls back to Space Grotesk/Inter. Inter,
Anton, Big Shoulders Display, and JetBrains Mono load from Google Fonts.

## Status / next
- ✅ `post-hero-1080x1350` template (IG portrait) — renders.
- ☐ Swap interim `tokens.css` for canonical CSS; add Aeonik `.otf`s.
- ☐ Pull the real curve-motif PNG + logo from Drive `assets/` (current motif is an SVG placeholder).
- ☐ More templates: carousel slides, quote/testimonial card, compliance block, story 1080×1920.
- ✅ Video: `video/jumpcut.py` — talking-head clip → pause/filler-free Reel cut + cut sheet (first used on the Radius Pro Reel, 2026-09-04).
- ✅ Video: `video/compose-reel.sh` (screen recording + avatar PiP, 9:16) and `video/captions.py` (Inter captions, 4 styles). Second-angle sync = audio cross-correlation of the two tracks (see jumpcut cut sheet).
- ☐ The social/illustration **style layer** (anti-slop rules) feeding AI gen (Replicate/Glif).

## Video: jump-cut a talking-head clip
```bash
pip install imageio-ffmpeg faster-whisper        # once; ffmpeg comes with the wheel
python3 video/jumpcut.py IMG_1234.MOV out/reel-v1.mp4 --preview
```
Removes every pause ≥0.6 s (keeps 0.12 s handles), removes um/uh, normalises loudness, exports
1080×1920 H.264. Also writes `reel-v1.cut-sheet.txt` — the keep-list in *source* timecode — so a
screen recording of the same take can be cut to match once its start is aligned to the phone clip.
Large sources: Drive → "Anyone with the link" → `curl "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`.
The chat upload cap is 30 MiB, so hand back the `--preview` file or a 2-pass ~1250 kbps render.

### Two-angle Reel (screen recording + talking head)
1. `jumpcut.py` the phone clip → cut + `.cut-sheet.txt` + `.words.json`.
2. Find the offset between recordings by cross-correlating the two audio envelopes (numpy, 100 Hz log-envelope FFT
   correlation — 0.94 score on the Radius Pro take), then apply the same keep-list shifted by that offset to the screen recording.
3. Crop the avatar tight (Radius Pro take: `crop=742:1320:249:600` on the 1080×1920 phone clip → 9:16 head-and-shoulders).
4. `python3 video/captions-highlight.py reel.words.json caps.ass` — the approved Craftons style (white Inter Bold, spoken word in a green box).
   `video/captions.py` keeps the earlier plain styles (white / green / card / highlight / ink).
5. `bash video/compose-reel.sh white9x16 screen-cut.mp4 avatar-cut.mp4 reel-final.mp4 caps.ass` (layouts: white9x16, full4x5, green9x16)
