# Craftons Configurator — Cinematic Content Engine (WORKSHOP — IN PROGRESS)

_Started 2026-07-11. Branch: `claude/craftons-config-builder-live-yes248`._
_This is a live workshop doc. The end product is a detailed build spec to hand to a session inside the **cnccut-app** repo. Do not treat anything here as final until the "LOCKED SPEC" section exists at the bottom._

---

## Why this exists

- Content pillar **Sell** = weekly short videos showing the Craftons configurator building real, buildable products so customers see what's possible.
- Blocker: it's **hard to get good footage of the configurator**. Screen-recording the live tool looks rough — janky 3D, browser chrome, cursor issues, wrong aspect ratio, loading states, and you can't reliably hit the same result twice.
- The live configurator instance on the cnccut-app **isn't live / doesn't work** yet.
- So we're speccing a **cinematic content engine**: a controllable system that turns the configurator + real footage into polished 9:16 reels, repeatably, every week. Quality bar is non-negotiable — this ships weekly and represents the brand.

## The vision (from Lee, Round 1)

A tool to create **clever, cinematic animations**. Ingredients, combined per clip:
1. **The Craftons website configurator** — shown building and designing products (the "software in action" beat).
2. **Real-life video** — actual products/jobs on site or in place.
3. **Signature move: the match.** Real video of, e.g., a concrete bench seat, alongside the configurator building that *exact* seat at the *exact* same dimensions. The digital twin.
4. **Compositing** — animations laid on top of real video.

## Locked so far

- **Output format:** 9:16 vertical, IG / TikTok reels. Fast, native, not agency-glossy-slow.
- **Reference register:** slick **SaaS product-demo** videos (UI motion, clean, confident). No single reference locked yet — to be gathered.
- **Tool identity:** option (D) — a combination of live-configurator capture + separate 3D/Blender animation + real-footage compositing + a "made-for-film" mode.
- **Blender:** in scope; **Claude drives Blender headless** (Python / `bpy`). Used for animating finished parts, the build process, and product-in-context / on-top-of-video work.
- **Who builds the actual tool:** a future session inside the **cnccut-app** repo, from the spec this workshop produces.

## The existing configurator (facts, for the spec)

- Repo: `leepatt/craftons-curves-calculator` — Next.js 15, TypeScript, Tailwind, **Three.js / React Three Fiber** 3D, SVG/DXF export for CNC, `/api/mcp` quote endpoint.
- Builders: Curves (`/`), Radius Pro, Ripping, Formwork, Stair, Box, Pelmet, Cut Studio, Curved Architraves, Concrete Stair Formwork, 3D Letters.
- Geometry + pricing live in code (e.g. `src/app/components/curves/pricing.ts`, per-app `manifest.ts` / `*-parts.ts`) — reusable by a renderer so animations are dimensionally-accurate to the real product/price.
- Deploys to Vercel (`craftons-curves-calculator.vercel.app`, syd1); embeds in the Craftons Shopify store via `section-*.liquid` iframes.

---

## Answers so far (Rounds 1–2)

- **Show mostly the REAL Craftons UI** — small faked details are fine, viewers won't notice/care. So the tool drives/records the actual configurator, cinematically (not a stylized replica).
- **Real footage first.** Tia films everything; no library yet (being built); only make clips for jobs we've actually done. The tool is for **much more than** the bench-seat "match" — don't over-index on that one idea.
- **Both looks** per clip: photoreal (Blender) and clean/stylized (web-3D/graphics).
- **Dream = the tool produces EVERYTHING** — incl. captions in our design-system fonts, and animated graphics composited on top of real video (that compositing likely done in "our tool").
- **Cadence:** one reel/week. **Workflow:** Lee workshops a brief with the tool → tool builds → Lee guides. Templatize after a few. Lee guides more than hand-edits.
- **Register:** slick SaaS product-demo. Output 9:16 IG/TikTok.

## Research — recommended stack (dig #1, 2026)

**Unfair advantage:** the configurator is a web app, so we drive it deterministically and re-render at film quality instead of fragile screen-capture. Trend is strongly toward **code-driven, deterministic video** (Remotion is the most-used programmatic-video tool; ships a Claude Code skill).

**Recommended spine (agent-controllable end to end):**
1. **Playwright** — drives the real configurator headlessly; frame-accurate 1080×1920 viewport capture; we author the click/cursor timeline (so our click data is authoritative, unlike reverse-engineered capture).
2. **Remotion** (React video) — the compositor/renderer: synthetic **spring cursor**, **auto-zoom-to-click** camera, device/browser frame, gradient bg, spring UI reveals, kinetic **captions in brand fonts**, and **compositing overlays over real footage** via `<OffthreadVideo>`. Deterministic; parametrized per brief. Free at our size.
3. **FFmpeg** — final crop/pad, speed-ramps, audio mux, 9:16 finish.
4. **Headless Blender (`bpy`)** — bolt-on for photoreal 3D hero shots: export configurator geometry → glTF/DXF → Cycles/OptiX turntable/reveal → frames into the Remotion timeline.
5. **DaVinci Resolve (Python, headless)** — held in reserve as a pro finisher (motion-tracked callouts / colour) if ever needed.

**How the "Screen Studio look" is reproduced:** hide the OS cursor; render a **synthetic cursor** that follows the authored path via a **spring** (lag + settle); generate **auto-zoom** camera keyframes from click timestamps (ease to ~1.4–2× on click, hold, ease out on idle); float the capture in a rounded device frame on a padded brand-colour canvas; author at 60fps with spring/overshoot easing; **speed-ramp** boring stretches (typing/loading) and slow to real-time on the payoff (price appears / 3D part completes); kinetic word-by-word captions synced to VO.

**Tools to mine for aesthetics but NOT build on** (GUI-only, no agent API): Screen Studio (the quality bar; macOS-only), Cursorful, Tella, Loom, CapCut, After Effects (unless `aerender`).

_This maps onto the existing `pipeline/` pattern (content JSON + templates + headless render + ffmpeg) — same idea, extended to video._

### Research dig #2 — technical refinements (locked corrections)

- **Capture:** do NOT use Playwright's built-in video (hardcoded ~1 Mbit/s, looks soft on 3D). Use **`puppeteer-capture`** (Chrome CDP `HeadlessExperimental.beginFrame` — pull frames on demand) → deterministic, high-res, 60fps, frame-perfect regardless of render speed. Drive configurator state directly via `page.evaluate()` (set radius/width/angle/material) rather than fumbling the UI; freeze animations/seed RNG for byte-identical reruns.
- **Remotion is the keystone** and absorbs capture-compositing, callouts, captions, audio in one React tree. Crucially, **`@remotion/three`** can re-render the configurator's OWN Three.js geometry natively in the video (drive with `useCurrentFrame()`, not R3F `useFrame`) → film-quality 3D without any screen-capture quality ceiling. Real footage via `<OffthreadVideo>`.
- **Blender:** pin one version in Docker; give the agent a **known-good parametric template** (import SVG/DXF → extrude → material → turntable → render) it *edits*, and iterate live via **`blender-mcp`** (Claude drives a live Blender session, inspects state, retries) — far more reliable than one-shot `bpy` script generation. **Eevee** = stylized/preview (near-instant), **Cycles** = photoreal hero (GPU). Render parts with **transparent background** (alpha PNG seq / ProRes 4444) → composite in Remotion/FFmpeg, no chroma-key artifacts.
- **Captions:** Whisper / `whisper.cpp` (fast on Apple Silicon) → `@remotion/captions`; brand webfont in Remotion CSS for exact type.
- **Music:** Epidemic Sound has a real REST **Music API** (programmatic track fetch + clean licensing) — right fit for automation. **VO optional** (ElevenLabs) — for builder-to-builder, captions-over-music is often stronger.
- **Compositing over real video:** default to Remotion (stack layers over `<OffthreadVideo>`); FFmpeg (`overlay`/`blend`/`enable=between`) as a utility; Blender compositor only for true-3D-depth overlays.
- **Hosting/cost:** capture + Remotion + FFmpeg + Whisper + **Eevee** all run **locally on a Mac (no GPU needed for Remotion)**; only **Cycles** hero shots burst to a cloud RTX box (~$0.02–0.05/frame → ~$4–5 for a 200-frame shot). Weekly cadence = huge slack, no Lambda needed.
- **The one bespoke component:** synthetic eased cursor + auto-zoom-to-click — port the easing/zoom logic from OSS **OpenScreen** (Electron+PixiJS) into a Remotion layer. Budget for this explicitly.

### Reference architecture (from research)
```
Brief (Lee) → agent authors a TS "reel spec" (shots, configurator states, copy, music mood)
 → Capture: puppeteer-capture records the REAL configurator, cursor hidden, cursor path logged as data
 → 3D (optional/shot): agent edits parametric bpy template via blender-mcp; Eevee stylized / Cycles hero; alpha bg
 → Compose in REMOTION: OffthreadVideo (Tia's clips + recorded UI) + @remotion/three native 3D
   + synthetic cursor/auto-zoom + animated callouts + brand-font captions (Whisper) + Epidemic music + optional VO
 → npx remotion render → 1080×1920 MP4 → Lee reviews → approve → Later.com
```

## Answers — Round 3 (logistics locked)

- **Compute = cloud-first.** Lee's laptop is old, no GPU (can get one). Yes to a **cloud box**. → Laptop is just the control surface (Claude Code); all rendering runs in the cloud, with an on-demand GPU box for photoreal (Cycles) hero shots.
- **Home repo = `cnccut-app`** (option B). cnccut-app is the umbrella that hosts all calculators/tools; the configurator's actual code lives in the separate `craftons-curves-calculator` repo. The engine sits in cnccut-app and **drives the live configurator URL** (cross-repo) — it doesn't need the configurator source in-repo (can optionally import geometry as a shared module).
- **VO:** AI VO fine; currently a **Gemini voice** — keep that as default (ElevenLabs as alt). Captions-over-music often preferred.
- **Music:** **Gozney pizza-video register** — warm, cinematic, tactile, premium-but-grounded, mid-tempo build. Pull the actual "Gozney playbook" from Drive `02 Strategy/Craftons-Marketing-Engine-Notes.md` at production time. Programmatic fetch via Epidemic Sound Music API.
- **Brief = conversational.** Lee chats (here in Claude Code, or with the tool) → the agent emits a structured **reel-spec** (versioned JSON/TS). No rigid form.

→ See the standalone build spec: **`CONTENT-ENGINE-SPEC.md`** (the handoff doc for a cnccut-app session).

## Answers — Round 4 (reference ad + benchmark + interaction)

- Lee uploaded a **current 17s Radius Pro reel** as baseline (teardown now in the spec §2a). Verdict: right *type*
  of shots ("clever SaaS shots") but **not the template** — make it more engaging; **one per product**.
- **Benchmark corrected: Monday.com / modern SaaS** (bright, snappy, bold kinetic type, clean UI motion).
  Gozney demoted to a secondary warmth cue for real-footage beats only.
- **VO + captions both**, with a **per-reel choice** (toggle in the reel-spec).
- **Interaction model answered** (spec §7a): start with **Claude Code as the chat** (Lee briefs in plain English,
  agent drafts the reel-spec + renders + re-renders on direction); a dedicated dashboard chat box is a later option.
- **Open creative call raised:** keep a recurring **talking-head presenter** (real or AI avatar) vs. go **pure
  kinetic-UI SaaS** (no persistent presenter). To decide before locking the house template.
