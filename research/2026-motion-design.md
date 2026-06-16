# Motion design for Craftons — 2026 tools, techniques & the "make it pop" playbook

_Deep-research synthesis, 2026-06-16. Five parallel angles (tools, techniques, brand teardowns,
audio/finishing, Remotion integration), cross-checked. Sources at end._
_Caveats: prices are order-of-magnitude — verify on live vendor pages. Some figures are from 2026
third-party reviews, not primary billing pages._

## TL;DR — the verdict for Craftons

1. **Lead with an interactive 3D product configurator + an exploded view** (à la Awwwards winners
   iyO / Copentek). This is almost purpose-built for a CNC building-products brand — and it converts
   for *manufacturers specifically*: **3D exploded-view video → +38% LinkedIn CTR vs 2D**;
   **3D configurator video → +22% AOV.** This is the Radius Pro / Formwork Builder story, told the best way.
2. **Make motion "pop" with physics, not luck:** never linear easing; spring-based motion; a small
   reusable easing/timing palette; Z-axis push-ins; overshoot-and-settle; count-ups; cut to the beat.
3. **Sound design is the cheapest premium upgrade** most people skip — UI click/whoosh/pop on every
   transition, synced to beats. A Google study found sound alone makes products feel more premium.
4. **Build the repeatable engine on Remotion** (free ≤3 people), with Blender for photoreal hero 3D
   and Playwright for real-UI capture. Screen recorders (Windows-friendly) cover quick founder demos.
5. **Trend tailwind:** 2026 rewards "designed UI" (not raw screen-records) + **authenticity** (real
   CNC footage, sawdust, the machine cutting). Your standing rule "real leads, AI extends" *is* the trend.

---

## 1. The proven format — interactive 3D configurator + exploded view

The strongest references are **iyO** and **Copentek** (Awwwards): a physical product shown as an
interactive, motion-driven hero — rotate, swap material/colour live, and an **exploded view** where
parts separate to reveal the join/assembly. For Craftons this maps directly:
- **Radius Pro:** a curve forming as radius/width/angle change (the configurator, animated).
- **Exploded/assembly view:** how a formwork/cavity-batten assembly goes together.
- **Nesting animation:** parts slotting efficiently onto a sheet — "precision, minimal waste."

Conversion data says this works for manufacturers (+38% CTR, +22% AOV). Lead with it.

## 2. Tool stack (the motion layer)

| Job | Tool | Notes / cost |
|-----|------|------|
| **Quick founder demos** (auto-zoom, smooth cursor) | **FocuSee** (cross-platform) or **Cursorful** | ⚠️ **Screen Studio is Mac-only — skip it, you're on Windows.** FocuSee ~$15–30/mo; Cursorful has a lifetime deal. Auto zoom-to-click + cursor smoothing. |
| **The repeatable branded engine** | **Remotion** (React video) | Free for ≤3 people. Code-driven, data-driven, version-controlled. The spine. |
| **UI micro-animations / logos / loaders** | **Lottie** (LottieFiles) | Lightweight JSON anims; AE → Lottie via Bodymovin. ~$20/mo. |
| **Interactive/stateful motion** | **Rive** | State machines; ~$9–32/mo. |
| **Fast browser motion mockups** | **Jitter** | Figma-like; ~$19/mo. |
| **Procedural/advanced vector motion** | **Cavalry** | **Now free for individuals** (Canva acquired it, Feb 2026). |
| **Photoreal 3D hero** | **Blender** (free) | Render product beauty-shots; image-sequence into Remotion. |
| **Real-UI capture** | **Playwright** (have it) | Deterministic, scripted UI recording. |

## 3. Audio & finishing — the cheapest premium upgrade

- **Sound design lifts perceived quality** (Google UX study) — layer **UI click / whoosh / pop on
  every transition + CTA, synced to beats.**
- **Library:** **Epidemic Sound** (~$10/mo yearly, biggest SFX library, ad-safe licensing) or
  **Uppbeat** (budget). Confirm the tier covers **paid advertising**.
- **AI voiceover:** **ElevenLabs Starter ($5/mo)** = minimum tier with commercial rights.
- **AI music (optional):** **Suno Pro ($10/mo)** — paid tier grants commercial rights (monetizable,
  not copyrightable). **Avoid Udio** (walled garden, can't export).
- **Captions:** word-by-word animated **lifts retention ~30–40%** vs static. Bold sans, white/yellow
  + black outline, lower-middle third, **inside safe zones** (top ~250px / bottom ~350px).
- **Export:** 1080×1920, 9:16, H.264, 30fps, ~12–15 Mbps (survives IG re-encode). Design a seamless **loop**.

## 4. Motion rules that make it "pop" (encode in every template)

1. **Never linear easing.** Default `ease-out`; standard curve `cubic-bezier(0.4, 0, 0.2, 1)`; UI moves ≤300ms.
2. **Fixed easing palette** of 3–4 curves (fast / standard / emphatic / decelerated) reused everywhere.
3. **2–3% overshoot-then-settle** on pop-ins. **Stagger** grouped elements/text 0.05–0.15s.
4. **One focal move per shot:** Z-axis push-in to the active element (~85% of premium SaaS uses this),
   dim/spotlight the rest. Add subtle **parallax** for depth.
5. **Reveal UI with a sweep or Z-zoom**, not a hard cut-on (~71% of premium SaaS).
6. **Count-ups** for every metric/spec; pace text to the beat.
7. **Hook ≤2.5s**, open with a pattern interrupt; micro-cuts (0.4–1.2s) in first 3 shots, then cut every 3–5s; **cut to the beat**.
8. **Design the last frame to loop to the first.**
9. **Motion blur on big moves only.** Animate `transform`/`opacity` only; hold 60fps.
10. **Restraint** — every motion needs a job (explain / signal state / transition). Physics-led
    (Vercel-style: panels grow from their trigger, settle with weight, resolve where the eye is).

## 5. The 15–30s demo-ad structure
**Hook the builder's pain (<2s)** → **problem** (sourcing / cut accuracy / lead time) → **product in
action** (configurator producing a real part) → **proof** (CNC-cut, spec-true, fast) → **CTA**.
One idea per ad. Front-load the result. Stylise the UI so the ad survives product updates.

## 6. Remotion build setup for Craftons (technical)
- **Remotion 4.0 + TypeScript.** Centralise brand tokens in `theme.ts` + a reusable scene-component library.
- **Motion:** `spring()` + `interpolate()` with a brand `craftonsSpring` preset; `@remotion/motion-blur`
  `<CameraMotionBlur>` on fast moves; `@remotion/shapes` for the curve motif; `@remotion/transitions`.
- **3D (hybrid):** Blender → image-sequence for photoreal heroes; `@remotion/three` + `useGLTF` for
  shots where the model/spec varies per render (part number, dimension, colour). (`layout="none"` on
  inner Sequences; `gl:"angle"` for Lambda.)
- **Assets:** AE → Bodymovin → `@remotion/lottie` (prefer baked keyframes; expressions can flicker);
  `@remotion/rive` for state-machine motion.
- **Data-driven:** each video = `inputProps` JSON (product, headline, dimensions, CTA) → one
  composition, many videos. Fits "Claude drafts props/code → Lee approves preview → render."
- **Captions:** `@remotion/install-whisper-cpp` → `@remotion/captions` → animated caption component.
- **Scale:** local CLI for one-offs; **Remotion Lambda** for batch (pennies/video, 1,000-way parallel).
- A native **Claude Code ↔ Remotion** integration shipped Jan 2026 (describe a video → Claude writes the code).

## 7. Recommended first reel (concrete spec)
**"Your radius, cut to spec. Online." — 15s, 1080×1920.**
- 0–2s: hook — a builder problem ("Curved formwork? Days of templating.") on a dark-green motif frame.
- 2–9s: the **configurator in action** — Playwright-driven, brand-styled; radius slider drags, the
  curve redraws, numbers count up, **punch-in** on the active field, dim the rest.
- 9–12s: the curve **becomes a 3D render** of the real plate (Blender), rotates, exploded-view beat.
- 12–15s: payoff + CTA — "CNC-cut. Spec-true. Delivered." → craftons.com.au. Loop to first frame.
- Throughout: UI click/whoosh SFX on each interaction, cut to a beat, word-by-word captions.

---

## Sources
**Tools:** [Screen Studio review](https://scribehow.com/page/Screen_Studio_Review_2026__Best_Mac_Screen_Recorder__pkHh5vHIQjaHUuE0qxv8bw) · [FocuSee](https://focusee.imobie.com/features/auto-zoom-and-cursor-animation.htm) · [Cursorful](https://cursorful.com/) · [Remotion license](https://www.remotion.pro/license) · [Rive pricing](https://aistackpicks.com/reviews/rive-pricing-2026/) · [LottieFiles](https://vijaytalksai.com/lottiefiles-review/) · [Jitter pricing](https://vijaytalksai.com/jitter-pricing-explained/) · [Canva acquires Cavalry](https://www.cgchannel.com/2026/02/canva-acquires-next-gen-motion-graphics-tool-cavalry/)
**Techniques:** [Great UI animations — Emil Kowalski](https://emilkowal.ski/ui/great-animations) · [Disney principles for UI — IxDF](https://ixdf.org/literature/article/ui-animation-how-to-apply-disney-s-12-principles-of-animation-to-ui-design) · [SaaS motion examples — Advids](https://advids.co/blog/30-best-saas-motion-graphic-video-examples-to-inspire-creativity) · [Kinetic typography — IK Agency](https://www.ikagency.com/graphic-design-typography/kinetic-typography/) · [Hook formulas — OpusClip](https://www.opus.pro/blog/youtube-shorts-hook-formulas) · [Retention cutting — AIR](https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8)
**Brand teardowns:** [Stripe/Linear/Vercel premium UI — Mantlr](https://mantlr.com/blog/stripe-linear-vercel-premium-ui) · [UI motion patterns — uimotion.fyi](https://uimotion.fyi/) · [UI trends 2026 — Lummi](https://www.lummi.ai/blog/ui-trends-2026) · [SaaS demo videos — Vidico](https://vidico.com/news/top-12-outstanding-saas-product-demo-videos/) · [SaaS demo structure — Levitate](https://levitatemedia.com/learn/saas-product-demo-videos) · [iyO configurator (Awwwards)](https://www.awwwards.com/sites/iyo) · [Copentek configurator (Awwwards)](https://www.awwwards.com/inspiration/3d-product-configurator-copentek-website) · [3D exploded-view — Advids](https://advids.co/blog/30-creative-3d-exploded-view-video-examples-to-showcase-technical-insights)
**Audio/finishing:** [Sound design & UX — MusicGrid](https://www.musicgrid.com/blog/forgotten-ux-sound-design-digital-products) · [Epidemic vs Artlist — cchound](https://www.cchound.com/epidemic-sound/artlist-vs-epidemic-sound/) · [Suno commercial rights — Terms.law](https://terms.law/ai-output-rights/suno/) · [ElevenLabs pricing — BIGVU](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/) · [Reels safe zones — Zeely](https://zeely.ai/blog/master-instagram-safe-zones/) · [Caption styles — Blitzcut](https://blitzcutai.com/blog/best-caption-style-tiktok)
**Remotion:** [spring()](https://www.remotion.dev/docs/spring) · [@remotion/three](https://www.remotion.dev/docs/three) · [GLTF example](https://github.com/remotion-dev/remotion-three-gltf-example) · [@remotion/lottie](https://www.remotion.dev/docs/lottie/) · [@remotion/rive](https://www.remotion.dev/docs/rive) · [@remotion/captions](https://www.remotion.dev/docs/captions/api) · [dataset render](https://www.remotion.dev/docs/dataset-render) · [Remotion Lambda](https://www.remotion.dev/docs/lambda)
