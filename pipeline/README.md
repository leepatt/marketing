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
- ☐ Video: second-angle (screen recording) sync + PiP compositing from the cut sheet; brand captions burn-in.
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
