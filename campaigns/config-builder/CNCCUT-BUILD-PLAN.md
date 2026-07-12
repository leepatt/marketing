# Craftons Content Engine — Build Plan (hand this to a cnccut-app session)

> **Mission:** build a tool that turns the **real Craftons configurator** into a polished **9:16 Sell reel** each
> week, driven by a small **reel-spec** Lee briefs in chat. The approach below is already proven in a sandbox —
> this is the build, not an experiment. Deeper detail lives in the marketing repo (links at the bottom).

---

## 1. What's already proven (do NOT re-discover)
- **Driving the real app with Playwright = pixel-identical capture.** Working scripts exist:
  `campaigns/config-builder/sandbox/capture-clean.mjs` (clean baseline, uses the **real logo**) and
  `capture-real.mjs`. They run the real `craftons-curves-calculator` app on `localhost:3000`, set the real inputs
  (`#specifiedRadius`, `#width`, `#angle`) via the native value setter, scroll, click the real **Add Part**, and
  screenshot each frame → ffmpeg. Real behaviour comes free (the "split into 2 sections / Joiner Blocks" note,
  Parts list, Order Summary).
- **Deterministic frame-by-frame capture** (time → state → screenshot) is the right model. **Remotion** is the
  productionised version of it and is the compositing/render spine.
- **Real Craftons logo** saved at `sandbox/assets/craftons_logo.png`.

## 2. Guardrails (hard lessons — don't repeat them)
- **NEVER fabricate brand assets.** A hand-drawn logo + fake chrome tanked an otherwise-clean clip. Use the
  **real logo, real fonts (Aeonik), real footage** only. Let the real UI carry it.
- **The real app already looks good.** Our value-add is *camera, sound, and real footage* — not invented chrome.
- **Video-first design** (per the Remotion `video-layout` skill): one message per scene, big text (headline
  ≥84px at 1080w), safe margins, the real UI as a **hero beat** — not a dense dashboard to inspect.
- **Real footage leads; a human approves every asset** (standing Craftons rule).

## 3. Architecture (the pipeline)
```
reel-spec (Lee briefs in chat)
 → Playwright drives the REAL configurator (local npm start, or the deployed URL) → clean UI clip + a logged
    cursor/click timeline
 → REMOTION composition imports that clip as ONE layer and adds, via useCurrentFrame()/interpolate():
      • spring cursor + auto-zoom-to-click (the Screen-Studio "SaaS" camera)
      • kinetic captions in real Aeonik
      • Tia's real footage  (<Video>/<OffthreadVideo> from @remotion/media)
      • music bed + snap SFX (<Audio>), optional Gemini/ElevenLabs VO
      • hook + CTA scenes using the REAL logo
 → npx remotion render → 1080×1920 MP4 → Lee reviews → Later.com
```
Stylized 3D (optional) = `@remotion/three` (native, no Blender). Photoreal 3D (later) = headless Blender/Cycles
on a GPU box, composited as alpha frames.

## 4. Step 0 — install skills + scaffold
- Install the Remotion agent skills FIRST, **inside the cnccut-app repo**: `npx skills add remotion-dev/skills`.
  (Fallback if GitHub is unreachable: copy `campaigns/config-builder/remotion-skills/` from the marketing repo
  into `.claude/skills/` — only works if the marketing repo is added to that session.) **Then commit the skills
  into cnccut-app** (`.claude/skills/` + `.agents/skills/`) so they persist — remote sessions clone fresh each
  time, and uncommitted skills disappear next session. Verify they load, then proceed.
- Create a self-contained **`content-engine/`** package (its own `package.json`, own CLI) so the media pipeline
  doesn't entangle the Next.js app. It only needs the configurator running at a URL, so it stays decoupled.
- Deps/setup: node, ffmpeg, playwright(-core) + the pre-installed Chromium, remotion, `@remotion/media`,
  `@remotion/captions`, `@remotion/three`, whisper.cpp (captions). Point Remotion at the system Chromium.
- Secrets (repo `.env`, never the Drive brain): Epidemic Sound API, Gemini/ElevenLabs (optional VO).

## 5. Build phases (ship value early; each has an acceptance check)
- **Phase 1 — Real-capture module.** Port `capture-clean.mjs`. Drive the real app to any
  `{radius,width,angle,material}`; output a clean UI clip + `cursor-track.json`.
  ✅ *renders a chosen part reliably, pixel-identical, with the real logo header.*
- **Phase 2 — Remotion spine (the quality jump).** Import the UI clip as a layer; add **spring cursor +
  auto-zoom-to-click**, brand captions, and hook/CTA scenes with the real logo + Aeonik.
  ✅ *the config beat looks A-grade — silky camera, real assets, no invented chrome.*
- **Phase 3 — Real footage + audio.** `<Video>` slot for Tia's clip; music bed + snap SFX synced to the fills
  and the Add-Part snap; optional VO.
  ✅ *a full reel (hook → real footage → config build → CTA) renders with sound.*
- **Phase 4 — reel-spec + templatize.** One small spec → whole reel; 3–5 reusable shot templates; the
  chat loop: brief → draft → Lee guides → re-render.
  ✅ *a new weekly reel = editing last week's spec.*
- **Phase 5 — 3D (optional).** `@remotion/three` stylized build/turntable; Blender Cycles photoreal hero shots.

## 6. The reel-spec (conversational brief → structured object)
```jsonc
{
  "meta": { "title": "Curved bench seat", "product": "curves",
            "dims": { "radius": 800, "width": 450, "angle": 180 }, "material": "Formply 17mm",
            "aspect": "9:16", "durationSec": 20 },
  "shots": [
    { "type": "hook", "headline": "Design custom curves. Online." },
    { "type": "real-footage", "clip": "tia/bench-empty.mp4", "captions": ["Curved bench seat. Over there."] },
    { "type": "ui-capture", "autozoom": true, "captions": ["Four numbers. Instant part."] },
    { "type": "real-footage", "clip": "tia/bench-poured.mp4" },
    { "type": "cta", "line": "Configure yours · craftons.com.au" }
  ],
  "presenter": "none",                 // none | real:<clip> | avatar:<voice>
  "audio": { "musicMood": "monday-snappy-build", "vo": null },   // vo: null | "gemini" | "elevenlabs:<id>"
  "captions": { "on": true, "style": "kinetic-word", "font": "Aeonik" },
  "brand": { "motif": true, "look": "stylized" }                  // look: stylized | photoreal
}
```
Everything is a per-reel toggle with sensible defaults. Default house template = presenter-free, Monday.com
style, captions-on.

## 7. Assets to pull at build time
- **Real logo** — already saved at `sandbox/assets/craftons_logo.png`.
- **Aeonik** `.otf` (licensed, Drive `fonts/`), **curve-motif PNGs** + `colors_and_type.css` (Drive
  `00 Brain/Design-system/`).
- **Tia's footage** — real completed jobs only, as filmed (no stock).

## 8. House style (one line)
Monday.com energy with **Ramp's single-accent discipline**: green `#194431` is the "done / locked / active"
accent ONLY; the **curved-line motif** is the kinetic signature; **real footage leads**; the **snap-into-place**
is the payoff. Sentence case, minimal punctuation, big type, warm off-white / near-black grounds.

## 9. Deeper detail (in the marketing repo, `campaigns/config-builder/`)
- `CONTENT-ENGINE-SPEC.md` — full architecture, house style (§2b), the 3 research digs, phase detail.
- `CONTENT-ENGINE-SHOTS-AND-CALENDAR.md` — shot library + the first month's four reels.
- `CONTENT-ENGINE-WORKSHOP.md` — the workshop record + "state of play" + lessons.
- `sandbox/` — the proven capture scripts + real logo + fonts (runnable).
- `remotion-skills/` — the 8 Remotion agent skills.
