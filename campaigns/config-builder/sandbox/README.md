# Config-demo reel — sandbox prototype

A working proof-of-concept of the content engine's hero beat (**S2 config demo**): a Craftons configurator
building a curved bench seat (r800 × w450 × 180°), rendered as a **9:16 MP4**. Proves the real pipeline pattern
end-to-end: **a time-driven HTML scene → headless Chromium screenshots each frame → ffmpeg → MP4** (deterministic;
same input → identical output — the Remotion model, hand-rolled).

## Files
- `scene.html` / `scene.js` — the scene. Every frame is a pure function of `t` (seconds); `window.__seek(t)`
  renders that instant. 10 **variants** (`?v=0..9`) vary theme (paper/dark/green), browser frame, zoom strength,
  motif, pacing, and preview fill — see the `V` table in `scene.js`.
- `capture.mjs` — drives headless Chromium (the pre-installed Playwright browser), seeks every frame, screenshots,
  and encodes with ffmpeg. `node capture.mjs <variant> <fps> <width> <height>`.
- `fonts/` — Space Grotesk (Aeonik stand-in) + JetBrains Mono, both OFL.

## Run
```bash
npm install
node capture.mjs 0 30 1080 1920   # variant 0, 30fps, 1080x1920 -> out/demo_v0.mp4
for v in $(seq 0 9); do node capture.mjs $v 30 1080 1920; done   # all variants
```
Requires `ffmpeg` on PATH and the Playwright Chromium at `/opt/pw-browsers/chromium-*/chrome-linux/chrome`
(adjust `EXE` in `capture.mjs` for other machines).

## What it demonstrates (vs. the full spec)
- The **deterministic timeline** approach the real engine uses (Remotion is the productionised version of this).
- **Brand system in motion**: green-as-"done" accent, curve motif, kinetic sentence-case headline, price count-up
  + green lock, synthetic cursor + auto-zoom, "Added ✓" snap payoff.
- **Not yet**: real footage compositing, native/photoreal 3D, captions-from-VO, music — those are Remotion/Blender
  stages in `../CONTENT-ENGINE-SPEC.md`. This is the UI beat only, hand-built to lock the look/pacing template.

## Next
- Pick the winning variant(s) → fold the knobs into the locked house template.
- Swap Space Grotesk → licensed **Aeonik**; pull the real curve-motif PNG + logo from the Drive brain.
- Port to Remotion for the full pipeline (real footage, 3D, audio, captions).
