# Desktop to-do — pick up here

_Created 2026-06-15 from a mobile session. Everything below is saved + pushed; nothing is blocked._

## 🔴 Do first — security
- [x] **Rotate the Google Ads credentials** — ✅ DONE 2026-06-23. Deleted the "Craftons Ads" OAuth
      grant (revokes leaked refresh token), disabled the leaked secret in Cloud Console (new UI uses
      "Add secret" → added a new one), re-minted the refresh token via OAuth Playground, updated both
      values in **Vercel env vars** + redeployed.
  - [ ] **Remaining:** mirror the two new values into the **Jake cloud environment**; once verified,
        **delete** the disabled old secret in Cloud Console.

## 🔎 Market intel — Facebook groups (desktop, browser) — added 2026-07-21
> Why desktop: FB group discussion is walled to Claude (no API; scraping breaks ToS + risks the account).
> Safe path = you read in a browser and feed threads in. See `MARKETING-BIBLE.md` §1 + the
> `craftons-dream-buyer` skill (Cluster 6). Goal: AU verbatim voice on curved walls + curved formwork.
- [ ] **Join the groups** (verified this session): [Tradies in Australia](https://www.facebook.com/groups/tradiesaustralia/),
      [Melbourne Carpenters/chippy's](https://www.facebook.com/groups/1568128824025391/),
      [Sydney builders & tradesmen](https://www.facebook.com/groups/1105399516186336/),
      [Owner Builders Australia](https://www.facebook.com/groups/OwnerBuildersAustralia/),
      [The Owner Builder Club (AU)](https://www.facebook.com/groups/OwnerBuilderClubAustralia/). Search+join
      concreting/formwork groups (Concreters Australia, Formwork Australia, Decorative Concrete Australia).
- [ ] **Don't browse — search inside each** for: curved · radius · bending/bendy ply · curved bench seat ·
      off form · formwork curved · kerf. Screenshot post + top comments → paste to Claude → into `QUOTE-BANK.md`.
- [ ] **Post 2–3 questions** (make them come to you): "curved walls — what bit does your head in?" ·
      "curved formwork set-out, what's working?" · "where do you get curved stuff cut to size?" Post as
      yourself (not the brand page) so answers stay candid + you don't get pinged as spam.
- [ ] **(Optional) Claude for Chrome (Max):** let Claude read the ~15 search-result threads in your
      logged-in tab, human-paced/targeted — NOT a bulk crawl (ToS + account risk).
- [ ] **Mine the bot-blocked forums too** (same paste method) — top 3: woodworkforums *"Bending Tight
      Radius in Ply"* + *"How to make curved architraves?"*; Bunnings Workshop *"besser retaining wall and curved bench seat"*.

## 📣 Facebook page auto-capture (desktop — Zapier) — added 2026-07-21
> Craftons FB page: https://www.facebook.com/profile.php?id=61574736366470 (new-Page URL format).
> Captures OUR OWN page's posts/comments only (not other groups). Low near-term value (new page) —
> it's plumbing for later + Lead-Ad capture. Zapier config: https://mcp.zapier.com/mcp/servers/1d8f79d5-5ec9-4104-8ff7-61fb14322f73/config
- [ ] Connect Facebook Pages in Zapier (OAuth — must be an admin of the Page).
- [ ] Build the Zap: trigger **Facebook Pages → New Comment/Post on our Page** → action **Google Sheets / ClickUp → new row/task**.
- [ ] Tell Claude when it's live → Claude mines the sheet on a schedule.

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
- [ ] **Motion design — "focus punch-in":** auto-zoom to the active control (the SaaS-ad look).
      Layer 1 = in-page CSS (active field scales up, rest dims, numbers count up, curve redraws);
      Layer 2 = virtual-camera push-in (animate stage scale+translate, or post-zoom in Remotion/ffmpeg);
      sequence on a timeline → capture → reel. Quick path: **Screen Studio** (auto-zoom screen recorder).
      Engine path: **Remotion** (keyframed zooms/callouts, branded cursor, deterministic).
- [ ] **Bonus reel:** animate the **nesting** (parts slotting onto a sheet) — "precision, minimal waste."
- [ ] **⭐ Lead format — interactive 3D configurator + exploded view** (à la Awwwards iyO/Copentek).
      Proven for manufacturers: 3D exploded-view +38% CTR, 3D configurator +22% AOV. This is the hero format.
- [ ] **Motion engine = Remotion** (free ≤3 ppl): `theme.ts` brand tokens + reusable scenes; `spring()`
      + a `craftonsSpring` easing preset; `@remotion/three`/Blender-image-seq for 3D; Whisper captions; Lambda for batch.
- [ ] **Quick-demo recorder (Windows):** FocuSee or Cursorful — ⚠️ NOT Screen Studio (Mac-only).
- [ ] **Sound + finishing kit:** Epidemic Sound (or Uppbeat) for SFX/music (confirm ad-license);
      ElevenLabs Starter ($5) for VO; word-by-word captions; export 1080×1920 H.264 ~12–15Mbps, design to loop.
- [ ] **Asset producers (optional):** Lottie (UI micro-anims), Rive (interactive), Cavalry (now free), Jitter.
- [ ] **First reel spec is written** → see §7 of `research/2026-motion-design.md` ("Your radius, cut to spec." 15s).
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
