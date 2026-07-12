# Craftons Cinematic Content Engine — Build Spec (v1 draft)

> **What this is:** the build spec for a tool that turns the Craftons configurator + real footage into
> polished 9:16 vertical reels, weekly, driven by an AI agent (Claude) with a human (Lee) guiding.
> **Who it's for:** a Claude Code session inside the **`leepatt/cnccut-app`** repo, which will build it.
> **Status:** v1 draft from a workshop (2026-07-11). Treat as the plan to build against; refine as you go.
> This file is self-contained — a fresh session need not have seen the workshop chat.

---

## Guiding principle — "option for everything"
Every element is a **modular toggle with a sensible default**, set per reel in the reel-spec: presenter
(none/real/avatar), VO (on/off, voice choice), captions (on/off, style), 3D look (stylized/photoreal), real
footage, music, motif, speed-ramps, aspect. **Default house template = presenter-free, Monday.com-style,
captions-on.** Nothing is hard-wired; Lee flips any switch by talking to the tool.

## Agent skills to install FIRST (Remotion)
Before building, install the official **Remotion agent skills** into this repo — they teach the agent to author
the Remotion compositing/render layer (Stage E/F below):
```bash
npx skills add remotion-dev/skills    # → ./.agents/skills + symlinks into ./.claude/skills
```
A saved copy also lives in the marketing repo at `campaigns/config-builder/remotion-skills/` (copy into
`.claude/skills/` if the installer can't reach GitHub). The 8 skills and where they apply:

| Skill | Use in this build |
|-------|-------------------|
| `remotion-best-practices` | Umbrella — invoke when unsure which applies |
| `remotion-create` | Scaffold the Remotion project / compositions (Tailwind, 9:16 layout) |
| `remotion-markup` | The reel compositions — animation, layout, typography, media, audio, fonts, timing, transitions |
| `remotion-render` | Render the final MP4 (incl. transparent renders for Blender-alpha composites) |
| `remotion-captions` | Burn captions (import SRT / transcribe via Whisper / display) — Stage F |
| `remotion-saas` | Architecture for a Remotion-powered app + product integration (player, framework, rendering) |
| `remotion-interactivity` | Editable elements in Remotion Studio (for tweaking a reel-spec live) |
| `mediabunny` | Read real-footage/audio metadata (dimensions, duration) before compositing |

Also relevant: `@remotion/three` (native 3D — Stage B), `@remotion/captions`, `<OffthreadVideo>` (real footage — Stage D).

## 0. TL;DR for the builder

Build a **local-CLI / cloud-run pipeline** (its own self-contained package inside cnccut-app, e.g. `content-engine/`)
that takes a **reel-spec** (a versioned JSON/TS object produced by chatting with Claude) and renders a
finished **1080×1920 MP4**. The spine is:

```
reel-spec → [capture the REAL configurator UI]  ┐
           → [native 3D via @remotion/three]     ├─► REMOTION compose ─► FFmpeg finish ─► review ─► Later.com
           → [photoreal 3D via headless Blender]  │   (+ real footage, cursor, auto-zoom,
           → [Tia's real footage]                 ┘    callouts, brand captions, music, VO)
```

Everything is a code library or CLI an agent controls directly. **Determinism is the whole point:** the same
reel-spec renders the same reel, so specs become reusable templates and the weekly job is "edit last week's spec."

---

## 1. Why this exists (context)

- Content pillar **Sell** = one short video per week showing the Craftons configurator building real, buildable
  products so customers see what's possible. This tool is used **every week** — quality bar is non-negotiable.
- The blocker: screen-recording the live configurator looks rough (janky 3D, browser chrome, cursor issues,
  wrong aspect ratio, loading states, non-repeatable). We fix that by **driving and re-rendering** the app
  rather than filming it.
- **Craftons' unfair advantage:** the "product" being demoed is itself a web app (Next.js + Three.js), so we
  can drive it deterministically and re-render its 3D at film quality.

## 2. What the reels are

- **Format:** 1080×1920, 9:16, ~15–30s, IG Reels / TikTok. Fast, native — not slow agency-gloss.
- **Register / benchmark:** **Monday.com and modern SaaS product videos** — bright, snappy, bold kinetic
  typography, clean confident UI motion, energetic. (Gozney is a *secondary* warmth cue for the real-footage
  beats — tactile close-ups, premium-but-grounded — **not** the primary bar.) Real footage leads; motion/3D
  extends. A human approves every asset.
- **Ingredients, mixed per reel:**
  1. The **real Craftons configurator UI** building/designing a product (mostly-real UI; small faked details fine).
  2. **Real footage** (Tia films actual completed jobs — no stock).
  3. **3D of the product** — stylized or photoreal — including build/exploded/turntable moves.
  4. **The "match"**: real footage of a finished product next to the configurator building it at the exact dims
     (a signature move, not the only one — the tool is general-purpose).
  5. **Animated callouts / captions** composited over real video, in the Craftons design system.

## 2a. Reference teardown — current Radius Pro ad (what to beat)
A 17s Radius Pro reel exists (Drive/uploads) as the baseline. Structure = a proven skeleton to reuse:
1. **Hook title card** (~0–1s): "SO WE BUILT CRAFTONS RADIUS PRO".
2. **Config demo** (~1–5s): configurator on a phone, stepped captions — choose material → input radius → wall
   dimensions → instant quote. _This beat is currently a low-fi phone screen-grab — it's the #1 thing our
   pipeline upgrades: real UI, synthetic cursor, auto-zoom on the price, 60fps._
3. **Screen→machine** (~6–7s): real factory/CNC footage — "From your screen to our cutting machines."
4. **Real product** (~8–10s): real curved plywood parts + big kinetic type ("CURVED TOP AND BOTTOM PLATES").
5. **Promise** (~11–12s): bold kinetic type ("DISPATCHED IN JUST 3 BUSINESS DAYS").
6. **Presenter + logo outro** (~13–16s): talking-head, logo draw-on, wordmark.
- Persistent talking-head presenter (VO) over everything + IG chrome.
- **Verdict (Lee):** good type of shots ("clever SaaS shots"), but not the template — we make it more engaging,
  and **one per product**. Benchmark shifts from this toward Monday.com-style energy.
- **Resolved:** presenter is an **optional, pluggable layer** — support **all** modes: none / real-footage
  presenter (Lee/Tia) / AI avatar. **Default house template = presenter-free, Monday.com style** for now.

## 2b. House style (Monday.com energy, Craftons discipline)
Benchmark = Monday.com's *motion energy*, but rebuilt with **one accent** like **Ramp** (Monday's rainbow is the
one thing NOT to copy — Craftons has one green). One-line house style:
> _Monday's satisfying self-assembling-UI energy + confident plain voice — rebuilt in one forest-green accent
> instead of a rainbow, with the curved-line motif as the kinetic signature, real CNC/timber footage leading,
> and the "snap-into-place" as the payoff beat._

**Borrow (the energy):**
- **State-flip payoff.** Monday flips a status dot green as the emotional beat. Craftons' version: the part
  **snaps into place / price locks / Add-to-Cart confirms** — land it on a beat, green `#194431` glows on resolve, with a clunk/pop SFX.
- **Self-assembling subject.** The part/curve builds itself (fields fill, preview draws, part nests) — snap +
  spring easing (slight overshoot then settle). Most transferable move.
- **Big bold sentence-case headline beside a floating UI card.** Aeonik Bold, one short phrase at a time,
  word-by-word entry with soft spring. **Sentence case, minimal punctuation** (steal Monday's type rules).
- **Comparison device:** CNC-precise part vs. hand-cut/gappy version (precision sells to builders).
- **Captions-first** (reels play muted; kinetic Aeonik carries it) + SFX synced to each assembly beat.
- **Arc** (9:16, ~8–15s): hook (jobsite truth, 0–3s) → precision reveal → self-assembly → snap payoff → CTA;
  ~1–2s/beat; logo/curve-motif in first 3s; confident, fluff-free close.

**Change (don't copy the rainbow):**
- **One brand color = meaning.** Green is the "done/locked/active" accent ONLY (seated joint, price, CTA,
  check) — like Ramp's single chartreuse. Black + warm off-white carry everything else.
- **Curve motif is the kinetic signature** (replaces Monday's color-block wipes): a curve sweeps to wipe scenes,
  draws on to underline, traces a cut edge, nests two shots (draw-on ~0.4–0.6s ease-out).
- **Warm off-white** ground (not cool lavender); **near-black not pure #000** (softer/premium).
- **Real footage leads, motion extends** — Craftons feels *made*, not illustrated. The **CNC toolpath itself**
  can be the animated protagonist (glowing green path tracing the cut = our "self-building board").
- **No mascot** — the material + the machine are the character.

**Easing tokens (standardize weekly):** entrances = spring ~5–10% overshoot `cubic-bezier(0.34,1.56,0.64,1)`;
curve-wipes = ease-in-out 0.4–0.6s; assembly snaps = fast ease-out + hard stop + SFX.

_Type note: Aeonik is licensed (Drive `fonts/`); use a bold geometric fallback (Poppins/Space Grotesk) until the
`.otf`s are loaded. Monday uses Poppins — a friendly geometric — so the fallback is on-register._

## 3. The configurator it drives (facts)

- Repo: **`leepatt/craftons-curves-calculator`** — Next.js 15, TypeScript, Tailwind, **Three.js / React Three
  Fiber** 3D, SVG/DXF export for CNC, `/api/mcp` quote endpoint.
- Deployed live on Vercel: **`https://craftons-curves-calculator.vercel.app`** (region syd1). This is the URL
  the engine drives for "real UI" capture.
- Builders/routes: Curves (`/`), Radius Pro (`/apps/radius-pro`), Ripping, Formwork (`/apps/formwork`), Stair,
  Box, Pelmet, Cut Studio, Curved Architraves, Concrete Stair Formwork, 3D Letters.
- Geometry + pricing live in code (e.g. `src/app/components/curves/pricing.ts`, per-app `manifest.ts` /
  `*-parts.ts`, SVG/DXF exporters under `src/app/api/export/*`). These can be **imported as a shared module**
  so native/Blender 3D is dimensionally identical to the real product and price.
- Config state can be set directly (skip UI fumbling) via `page.evaluate()` or URL params / share links
  (`/share/[id]`, `/api/cart/get-configuration/[id]`).

## 4. Home & compute model

- **Home repo:** `cnccut-app` (the umbrella hosting all calculators/tools). Build as a **self-contained
  subsystem** (own `package.json`, own CLI) so a heavy media pipeline doesn't entangle the Next.js app. Adapt
  the exact folder to cnccut-app's real structure; suggested `content-engine/`.
- **Control surface:** Claude Code (Lee's laptop / mobile / web) — where Lee chats a brief and guides.
- **Render environment (cloud-first — laptop has no GPU):**
  - CPU stages — puppeteer capture, Remotion render, FFmpeg, Whisper captions — run on a **cloud Linux box**
    (the Claude Code cloud exec env works: Chromium preinstalled at `/opt/pw-browsers`; ffmpeg via a setup
    script). No GPU needed for these.
  - **Photoreal (Cycles) only** bursts to an **on-demand cloud GPU box** (rented RTX). ~$0.02–0.05/frame →
    ~$4–5 for a 200-frame hero shot. One reel/week has huge slack.
  - **Design decision to minimise Blender dependence:** do **stylized 3D via `@remotion/three`** (no Blender).
    Reserve **Blender strictly for photoreal Cycles** hero shots. Simplifies the common path enormously.

## 5. Architecture — the pipeline stages

### Stage A — Capture the real configurator UI  (fidelity path) — ✅ PROVEN in sandbox
_Validated 2026-07-11: `campaigns/config-builder/sandbox/capture-real.mjs` drives the real
`craftons-curves-calculator` app (run locally on `localhost:3000`) with Playwright, sets the real inputs
(`#specifiedRadius`/`#width`/`#angle`) via the native value setter, scrolls, injects a synthetic cursor + green
Craftons header + captions as DOM overlays, clicks the real Add Part, and screenshots each frame → ffmpeg →
pixel-identical MP4. Real behaviour comes for free (the "curve split / Joiner Blocks" note, Parts list, Order
Summary). In production, point at the live URL instead of localhost (no proxy there)._

- **Do NOT use Playwright's built-in video** (hardcoded ~1 Mbit/s → soft on 3D). Use **`puppeteer-capture`**
  (Chrome CDP `HeadlessExperimental.beginFrame`, pull-frames-on-demand) → deterministic, high-res, 60fps,
  frame-perfect regardless of render speed. (`puppeteer-screen-recorder` is a simpler fallback.)
- Drive the **live Vercel URL**; set configurator state directly via `page.evaluate()` / share-link URL; wait
  on explicit selectors / `waitForFunction`; freeze animations + seed RNG for byte-identical reruns.
- **Hide the OS cursor** (`cursor:none`); the engine **authors the cursor path + click timestamps as data**
  (we scripted them, so they're authoritative). The synthetic cursor + zoom are added later in Remotion.
- Output: a clean, high-res clip of the real UI + a `cursor-track.json` (`{t,x,y,click}[]`).

### Stage B — Native 3D  (stylized path, no Blender)
- **`@remotion/three`** (`<ThreeCanvas>` + React-Three-Fiber) re-renders the configurator's **own geometry**
  natively in the video, driven by `useCurrentFrame()` (never R3F `useFrame`, for determinism). Import the
  geometry/param builders from `craftons-curves-calculator` as a shared module (or reimplement the small math).
- Use for: build/assembly animations, exploded views, turntables, camera flythroughs — unlimited camera moves,
  no capture quality ceiling, brand-styled materials/line-motif.

### Stage C — Photoreal 3D  (Blender, GPU)
- Export configurator geometry as **SVG/DXF/glTF** → headless **Blender** via **`blender-mcp`** (Claude drives a
  live Blender session, inspects state, retries — far more reliable than one-shot `bpy` scripts) editing a
  **known-good parametric template** (`import → extrude/bevel → PBR material (timber/concrete) → turntable →
  render`). **Cycles** on the GPU box for photoreal; render with **transparent background** (alpha PNG seq /
  ProRes 4444) so it composites cleanly (no chroma-key). Pin one Blender version in Docker.
- `bpy` import ops: `import_curve.svg()` (curves — ideal, our parts *are* curves), `io_import_dxf`, STL native.

### Stage D — Real footage
- Tia's clips enter Remotion via **`<OffthreadVideo>`** (frame-accurate, fast). Only real completed jobs.
- The **"match"** = a Stage B/C render at the clip's exact dims placed beside/over the real footage.

### Stage E — Compose (Remotion is the keystone)
- One React composition (1080×1920, 30fps) stacks: recorded UI clip (A), native 3D (B), Blender alpha frames
  (C), real footage (D), the **synthetic spring-cursor + auto-zoom** layer, animated callouts, brand captions,
  and audio. Deterministic; parametrized by the reel-spec.
- **The one bespoke component:** the synthetic eased cursor + auto-zoom-to-click. Port the easing/zoom math from
  OSS **OpenScreen** (`github.com/siddharthvaddem/openscreen`, Electron+PixiJS) into a Remotion layer:
  synthetic cursor follows the authored path via a **spring** (lag+settle); on each click, ease the composition
  `scale`/`translate` to ~1.4–2× centered on the click, hold, ease out on idle. **Budget real time for this.**

### Stage F — Audio, captions, finish
- **Captions:** Whisper / `whisper.cpp` (fast on Apple Silicon; runs cloud too) → `@remotion/captions`; render
  in **brand webfonts** (Aeonik display / Inter body / JetBrains Mono for specs) — word-by-word kinetic reveal.
- **Music:** **Epidemic Sound Music API** (programmatic fetch + clean licensing), mood = Gozney register.
- **VO (optional):** default to the existing **Gemini voice**; ElevenLabs as alternative. Often skip VO in
  favour of captions-over-music.
- **Finish:** FFmpeg — 9:16 crop/pad, **speed-ramps** (fast through typing/loading, real-time on the payoff:
  price appears / 3D part completes), audio mux → final MP4.
- **Handoff:** Lee reviews → approve → **Later.com** (nothing auto-publishes).

## 6. Premium-look checklist (bake into the Remotion templates)
- Auto-zoom-to-click camera (ease in ~1.4–2×, hold, ease out on idle).
- Synthetic spring cursor (hidden OS cursor; spring lag + settle).
- Rounded device/browser frame + soft shadow, floated ~85–90% on a padded brand-colour / motif canvas.
- Spring / overshoot easing on all UI reveals; author at 60fps feel.
- Speed-ramping (boring fast, payoff slow).
- Kinetic captions synced to VO/beats; big bold brand type; high contrast.
- Curve-line motif behind hero text (once, big); logo lockup; signature "Pre-Fab. Pre-Cut. Site-Ready."
- Voice = builder-to-builder; ALL CAPS reserved for compliance/spec stamps only.

## 7. The reel-spec (conversational brief → structured object)
Lee chats a brief (here in Claude Code or with the tool); the agent emits a versioned object like:

```jsonc
{
  "meta": { "title": "Curved bench seat", "product": "formwork",
            "dims": { "radius": 800, "width": 450, "angle": 180 },
            "aspect": "9:16", "durationSec": 22 },
  "shots": [
    { "type": "real-footage", "clip": "tia/bench-empty-yard.mp4", "speed": 1.0,
      "captions": ["Yeah, just a curved bench seat... over there."] },
    { "type": "ui-capture", "route": "/apps/formwork", "state": { "radius":800,"width":450,"angle":180 },
      "cursor": "auto", "autozoom": true, "captions": ["Four numbers."] },
    { "type": "native-3d", "move": "build-assemble", "style": "stylized" },
    { "type": "real-footage", "clip": "tia/bench-poured.mp4", "captions": ["Pre-Fab. Pre-Cut. Site-Ready."] }
  ],
  "presenter": "none",            // none | real:<clip> | avatar:<voice>
  "audio": { "musicMood": "monday-snappy-build", "vo": null },  // vo: null | "gemini" | "elevenlabs:<id>"
  "captions": { "on": true, "style": "kinetic-word", "font": "Aeonik" },
  "brand": { "motif": true, "look": "stylized" }   // look: stylized | photoreal
}
```
The agent decides sensible defaults (camera moves, easing, framing); Lee overrides by talking.

## 7a. How Lee talks to the tool (interaction model)
- **Model 1 — Claude Code IS the chat (start here, zero extra build).** Lee talks to the agent in Claude Code
  (laptop/phone/web) in plain English. The agent drafts a **reel-spec** (saved file), renders a draft MP4, shows
  it; Lee **directs changes in the same chat** ("shot 2 slower, zoom the price, captions not VO, swap music");
  agent edits the spec and re-renders. Specs are versioned files → nothing lost; last week's reel = this week's
  starting point. This matches how the workshop itself ran.
- **Model 2 — dedicated chat box in the cnccut-app dashboard (later).** A web page where Lee types briefs and
  sees previews inline; same engine underneath, driven via an endpoint (reuse the configurator's `/api/mcp`
  pattern). Nicer non-technical/mobile surface; a Phase 5+ goal once templates are locked.
- **The loop is identical either way:** brief → draft → Lee directs → re-render → approve → Later.com.
- **VO vs captions is a per-reel choice** (`audio.vo` in the spec): both supported — VO (default = the existing
  Gemini voice; ElevenLabs alt) and/or kinetic captions. Lee picks per reel in the chat.

## 8. Build phases (ship value early)
- **Phase 0 — scaffold:** install the **Remotion agent skills** (`npx skills add remotion-dev/skills` — see
  "Agent skills to install FIRST" above); `content-engine/` package in cnccut-app; setup script (node, ffmpeg,
  chromium/puppeteer, whisper.cpp, remotion); secrets (Epidemic Sound, Gemini/ElevenLabs). Reel-spec type + a sample.
- **Phase 1 — MVP "real-UI reel":** puppeteer-capture of the live configurator → Remotion compose with the
  **spring cursor + auto-zoom** + brand captions + one Epidemic track → 1080×1920 MP4. One shot type, end to end.
  _This proves the hardest bespoke piece first._
- **Phase 2 — real footage + callouts:** `<OffthreadVideo>` + animated callouts over Tia's clips; the "match" template.
- **Phase 3 — native 3D:** `@remotion/three` build / exploded / turntable (stylized), from shared geometry.
- **Phase 4 — photoreal:** Blender via `blender-mcp` + template, Cycles on the GPU box, alpha composite.
- **Phase 5 — templatize:** the weekly one-command "reel-spec → reel"; a library of 3–5 shot templates; Whisper
  auto-captions; Later.com handoff. After a few reels, lock a house template.

## 9. Risks / open items
- **Bespoke cursor+auto-zoom** is the real engineering; do it in Phase 1, port OpenScreen's math.
- **Blender reliability:** pin version in Docker; drive live via `blender-mcp` + template, not one-shot scripts.
- **Geometry sharing** across repos: decide import-as-module vs. reimplement the small param math vs. drive via
  the configurator's export API. Keep the price/geometry identical to the live product.
- **Fonts:** Aeonik is licensed (Drive `fonts/`); load real `.otf`s, don't substitute when available.
- **Secrets** live in cnccut-app's env, never in the Drive brain.
- Confirm the GPU box provider/setup for Cycles; confirm Epidemic Sound API access + licensing scope.

## 10. Assets & sources to pull at build time
- Brand: `colors_and_type.css` (Drive `00 Brain/Design-system/`), Aeonik `.otf`s, curve-motif PNGs, logo.
- Creative register: the **Gozney playbook** — Drive `02 Strategy/Craftons-Marketing-Engine-Notes.md`.
- This repo's `pipeline/` (content-JSON + template + headless render + ffmpeg) is the same pattern to extend.
- Key tech refs: Remotion (`remotion.dev/docs` — `offthreadvideo`, `three`, `captions`, `render`),
  `puppeteer-capture` (`alexey-pelykh.com/blog/why-i-built-puppeteer-capture`), `blender-mcp`
  (`github.com/ahujasid/blender-mcp`), OpenScreen (`github.com/siddharthvaddem/openscreen`),
  Epidemic Sound API (`epidemicsound.com/business/developers`), `whisper.cpp`.
