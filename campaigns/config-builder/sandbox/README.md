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

## ⭐ `capture-real.mjs` — drives the REAL app (the production approach)
This is the important one. Instead of the hand-built `scene.*` replica, it drives the **actual
`craftons-curves-calculator` app** and captures pixel-identical UI:
```bash
# 1) run the real app locally (from the cloned repo)
cd /workspace/craftons-curves-calculator && npm run build && PORT=3000 npm start
# 2) drive + capture it
cd <this sandbox> && node capture-real.mjs 30 10.5   # fps, duration -> out/real_demo.mp4
```
It sets the real React inputs (`#specifiedRadius`, `#width`, `#angle`) via the native value setter, scrolls the
real page, injects a synthetic cursor + the green Craftons header + captions as DOM overlays (so they're in the
screenshot), clicks the real **Add Part**, and screenshots each frame → ffmpeg. Because it's the real code, it
even surfaces real behaviour (e.g. the "curve split into 2 sections / Joiner Blocks" note, the Parts list +
Order Summary). **This is Stage A of the spec, proven.** Points `localhost` so no proxy is involved.

Why not the deployed URL from a Claude session? This session's egress proxy blocks headless-browser tunnelling
(curl works, Chromium resets — even example.com). Running the app locally sidesteps it entirely. On Lee's Mac /
the production cloud box there's no such proxy, so it can drive the live site directly.

## Next
- Make `capture-real.mjs` the spine; the `scene.*` replica is now just a fallback/reference.
- Add post-compositing (Remotion/ffmpeg): real footage, 3D, brand fonts (Aeonik), music, VO, curve-motif transitions.
- Fold the pacing/scroll/zoom knobs into a locked house template; drive from a reel-spec.
