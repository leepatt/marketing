# Desktop to-do — pick up here

_Created 2026-06-15 from a mobile session. Everything below is saved + pushed; nothing is blocked._

## 🔴 Do first — security
- [ ] **Rotate the Google Ads credentials** (client secret + refresh token appeared in a setup screenshot).
  1. [myaccount.google.com/permissions](https://myaccount.google.com/permissions) → "Craftons Ads" → **Remove access**.
  2. Google Cloud Console → **Clients → craftons-ads-client → Reset secret**.
  3. Re-run the OAuth Playground (offline + force-consent) → new refresh token.
  4. Update the 2 values in **both** places: cnccut-app `.env` **and** the Jake cloud environment.

## 🟠 Finish the design-system wiring
- [ ] **Paste `colors_and_type.css` into the repo** for an in-repo token copy.
      Open `G:\…\00 Brain\Design-system\colors_and_type.css`, copy the plain text, paste to Claude →
      it commits to `.claude/skills/craftons-design/`. (Until then the Drive copy is canonical and fetched on demand.)
- [ ] (Optional) Same for the small text extras if wanted: `_ds_manifest.json`, `_adherence.oxlintrc.json`,
      and the `ui_kits/web/` HTML/CSS/JS. Fonts/PNGs/PDF stay in Drive.

## 🟡 Production pipeline (B9 + compositing)
- [x] **Pipeline built + working** → `pipeline/` (HTML/CSS template → PNG via Playwright + sharp).
      Proven render: `post-hero-1080x1350` IG portrait. `npm run render`.
- [ ] **Add the media tooling setup script to the Jake cloud environment** — paste
      `pipeline/setup-media-tooling.sh` body into the env's *Setup script* field (so mobile sessions have ffmpeg/Playwright cached).
- [ ] **Swap interim `pipeline/tokens.css` for the canonical `colors_and_type.css`** (from Drive) + drop
      **Aeonik `.otf`s** into `pipeline/fonts/` so headlines render in the real face (currently a fallback).
- [ ] **Pull the real curve-motif PNG + logo** from Drive `assets/` (template uses an SVG placeholder).
- [ ] **More templates:** carousel slides, quote/testimonial card, compliance block, story 1080×1920.
- [ ] **Video:** ffmpeg assembly of Tia's footage → Reels export.
- [ ] **Social/illustration style layer** (anti-slop rules) feeding AI gen (Replicate/Glif).

## 🎬 Production quality — research-driven (see `research/2026-production-stack.md`)
> Verdict: the path to pro-grade is **rendering your real CAD geometry + finishing brand fidelity**,
> not better AI prompts. Visual style = a mix: real 3D/photography for product heroes, locked
> line-art illustration for explainers, AI as extension only.
- [ ] **#1 lever — Blender CAD→render pipeline.** Blender (free) + a STEP-import add-on, scripted
      headless, with a reusable turntable / product-on-white / environmental scene template so every
      SKU renders identically from its CAD file. (Or KeyShot $1,299/yr if speed > scripting.)
- [ ] **Define the illustration style** — build a **Recraft V4** custom style (~$48/mo, vector + text)
      or train a **FLUX LoRA on Replicate** from approved references → consistent line-art layer.
- [ ] **Add a Style Dictionary token layer** (`tokens.json` → CSS vars) feeding every template; wire
      the design system's `_adherence.oxlintrc.json` check into the pipeline.
- [ ] **Build the template library from teardowns** (skeleton → Craftons tokens): product-feature,
      before/during/after, spec/compliance, testimonial, educational carousel, story 1080×1920.
- [ ] **Image-treatment pass in sharp** — green-duotone + motif overlay + grain so any photo reads as Craftons.
- [ ] **Video:** ffmpeg finishing script + **Whisper** captions (+ CNC term list) + atomise shoots
      (8–12 clips each). AI b-roll = **Kling** via Replicate (~$0.07/s). ⚠️ Avoid Sora (API ends 2026-09-24).
- [ ] **Generation cautions:** use FLUX **Pro** not Dev (Dev = non-commercial); Firefly only for
      indemnified paid-ad creative; keep the human-approval gate.

## 🎥 Formwork Builder demo reel (two-layer plan)
> Goal: a slick "watch it configure" reel — clean scripted clicks, no janky screen-record.
> Right tool per layer: **Playwright drives/records the UI**, **Blender renders the 3D plate**.
- [ ] **Layer 1 — UI capture (Playwright):** build a brand-styled standalone configurator (our tokens +
      Aeonik + motif + the existing curve maths), then a Playwright script that animates a styled cursor,
      drags the radius slider, clicks "Build" — captured frame-by-frame → ffmpeg → smooth 1080×1920 reel.
- [ ] **Layer 2 — 3D preview (Blender):** swap the flat 2D curve preview for a real 3D render of the
      radius plate (procedural from dimensions; STEP/OBJ export from the Fusion app for exact parts).
- [ ] **Phase 2 polish:** captions/intro/outro via Remotion or ffmpeg.
- [ ] **Bonus reel:** animate the **nesting** (parts slotting onto a sheet) — "precision, minimal waste."
- [ ] **Asset to fetch (desktop):** export one sample radius plate from the Fusion app as **STEP or OBJ**
      → drop in Drive (`00 Brain/product-cad/`) as a reference for the Blender setup.

## ✅ Verify
- [ ] Confirm the cnccut-app `.env` loads all 12 keys (quick check from inside the repo).
- [ ] Confirm a new session reads the keys from the Jake cloud environment.

## 🅿️ Parked decisions (yours to make, not blocking)
- [ ] Ad budget $ + per-platform split.
- [ ] LinkedIn activation timing (founder-led).
- [ ] Whether/when to add TikTok + YouTube.
- [ ] A5 — sync the Drive-side `CLAUDE.md` system map (was pending desktop).

---

### Done this session (for reference)
- 12 API keys collected → cnccut-app `.env` + Jake cloud environment.
- Decisions: Later = manual (no API); email = Shopify Email (not Klaviyo).
- `craftons-design` skill installed in the marketing repo (rules in-repo; exact tokens/assets canonical in Drive).
- `SETUP.md` / `INTEGRATIONS.md` updated (B1–B8).
