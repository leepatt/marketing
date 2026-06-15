# Craftons content production — 2026 tooling research & recommended stack

_Deep-research synthesis, 2026-06-15. Five parallel research angles, cross-checked. Sources at the end._
_Caveats: prices are order-of-magnitude — verify on live pages before committing spend. The legal
section is general IP doctrine (US-centric), not Australian legal advice — confirm under AU law for
any specific asset._

## TL;DR — the verdict

1. **Visual-style direction = a deliberate mix, not one technique:**
   - **Product hero → real 3D renders from your CAD/CNC geometry** (Blender, headless/scripted) +
     **treated real photography** (Tia's footage). You sell on precision; AI illustration *drifts*
     on edges/dimensions, which is fatal for a building-products brand. Real geometry = credibility.
   - **Explanatory / brand illustration → a locked technical line-art style** (Recraft V4 custom
     style or a trained FLUX LoRA) that echoes the curved-line motif — for diagrams, icons,
     educational carousels, compliance graphics.
   - **AI = extension only** — relighting, dropping accurate renders into jobsite/lifestyle scenes,
     b-roll. Never the hero geometry. (Matches your standing rule: real leads, AI extends, human approves.)
2. **Compositing → keep the Playwright + sharp pipeline** (you already built it; research backs it).
   Add a **design-token layer** so one token source feeds every template.
3. **Video → own an ffmpeg finishing script + Whisper captions; atomise shoots; rent AI b-roll**
   per-run on Replicate (Kling). Avoid Sora (API shuts 2026-09-24).
4. **Brand consistency → treat it as a pipeline with a gate**, with your design tokens as the
   enforced source of truth and the human-approval gate as the final check.

---

## 1. Visual style — why "mix," in detail

A building-products brand lives on **dimensional accuracy and trust**. The research is consistent:
AI image models "do not work with real geometry or precise measurements," struggle with
metallics/edges, and **change small details (logos, edges, features) between images** — exactly the
inconsistency that erodes a precision brand. Real 3D rendering gives **photoreal accuracy + full
repeatable control** and assets you re-angle/re-light/re-colour forever.

So:
- **Heroes (product-led posts, ads, spec content):** real 3D-from-CAD + treated photography.
- **Concepts/education/brand texture:** a *consistent* illustration style (line-art that matches the
  motif), where exact dimensions don't matter.
- **Scenes/atmosphere:** AI relighting + background generation around the accurate render.

This is ownable (your geometry + your motif), legally clean, and consistent.

## 2. Recommended stack (by layer)

### Generation — illustration & images
| Need | Tool | Notes / cost |
|------|------|------|
| **Consistent on-brand illustration** (vectors, icons, diagrams, in-image text) | **Recraft V4** | The standout for a brand *system*: define a Craftons custom style from ≤5 reference images, get editable **vector + raster** + reliable text. Pro ~**$48/mo** = full commercial rights + API. |
| **Locked house style at scale** | **FLUX LoRA on Replicate** | Train on approved Craftons illustrations → generate programmatically. One key, compounding reuse. |
| **Photoreal product/scene shots** | **FLUX.2 Pro** (via Replicate) | ~**$0.03/megapixel**, clean commercial license. ⚠️ Use **Pro, never FLUX *Dev*** (Dev = non-commercial). |
| **Headline-text posters/ads** | **Ideogram v3** | Best in-image typography (Midjourney mangles multi-line text). |
| **Legally-indemnified ad creative** (optional) | **Adobe Firefly** | Only major model with IP indemnification; lower photoreal quality. Use only if paid-ad legal risk matters. |

Your existing **Replicate** + **Glif** keys cover most of this. Glif = optional no-code wrapper so non-engineers can generate from templates.

### 3D from CAD (the product-hero engine)
- **Primary: Blender (free) + a STEP-import add-on** (chenpaner *Import-CAD-Model*, or *STEP Importer*/SimLab if material preservation matters). Script a **headless batch turntable + product-on-white + environmental** scene template → every SKU renders identically from its CAD file. Zero recurring cost; fully repeatable. Fits "pay setup cost once."
- **Alternative: KeyShot Studio 2026.1** (~**$1,299/yr**) — drop CAD in, render fast, now has headless animation + render queue. Faster to stand up if no 3D skills; recurring cost, less scriptable.
- **AI 3D assist (extension only):** Pebblely / Booth.ai / Shapr3D AI backgrounds to place the *accurate* render into scenes; Rendair AI for CAD-to-render concepts. Never for hero geometry.

### Compositing / templating (keep what we built)
- **Keep Playwright + sharp.** Research backs it: zero per-image cost, full CSS fidelity, no rate limits — beats **Figma API** (heavily throttled since 2025-11-17, 429s after ~10 exports) and **Canva Connect API** (enterprise-gated) as a render backend. `sharp` is ~4–5× faster than ImageMagick.
- **Add a design-token layer: Style Dictionary** → one `tokens.json` compiles to CSS variables every template consumes. (Our `pipeline/tokens.css` is the seed; formalise it.)
- **Optional fast-path:** Satori (+ resvg) for simple Flexbox-only cards. Don't replace Playwright (Satori lacks gradients, `z-index`, 3D transforms, WOFF2).
- Operationally, the only real failure modes: pool browser instances, cap concurrency, and **install brand fonts on the server** (or text renders as tofu).

### Video / Reels
- **Own an ffmpeg "finishing" script** (resize/crop to 1080×1920, burn brand captions, intro/outro, logo overlay) — zero-cost repeatable core, keep in repo.
- **Captions: Whisper (~5% WER) → SRT → burn-in**, with a Craftons term list (CNC jargon, part numbers, AU accent). Beats CapCut's ASR.
- **Atomise:** each Tia shoot → 8–12 vertical cuts (OpusClip-style first pass, human picks finals). Cadence benchmark: 5–7 short videos/week, 30–60s.
- **AI video = b-roll/extension only**, pay-per-run on Replicate — **Kling ~$0.07/s** (long clips). **Avoid Sora — API ends 2026-09-24.**
- **Remotion** (React video, data-driven templated Reels) later — free for ≤3 employees, $25/seat above.

### Brand consistency & QA
- **Design tokens = the enforced source of truth.** Feed `tokens.json` to any AI generator/assistant so output inherits correct values (the 2026 fix for AI drift). Our design system already ships an **`_adherence.oxlintrc.json`** that flags raw hex/px/off-system fonts — wire it into the pipeline as a check.
- **Gate before publish:** automated pre-check (off-brand colour / missing logo / missing compliance stamp) + the **human approval** you already require.
- Treat AI as a "production assistant needing explicit rules, not a creative director." Assume in-image text fails ~20% of the time — **human-set all type** where it matters.

## 3. Inspiration → brand (legal + practical)

**The line:** copyright protects *expression*, never the *idea*; layout/composition *structure* is
weakly protected (functional). The real risk is **trade dress** — copying a competitor's *overall
distinctive look* (their colour+shape+layout signature). So:

**Workflow (safe + effective):**
1. **Study the skeleton, not the skin.** From a reference, extract only grid, eye-flow, hierarchy,
   image-to-text ratio. That's the free "idea."
2. **Strip their colour/type/motif/copy.** Discard everything expressive.
3. **Re-pour into Craftons tokens** — rebuild the skeleton in our colour/type/motif so it's
   unmistakably ours (this is also what keeps trade dress clear).
4. **Gate before publish** (human approval + brand pre-check).

This is exactly your existing teardown model — formalise teardowns to capture *composition only*
from nominated brands (Gozney, July, BuildPass), then rebuild in Craftons tokens.

## 4. Prioritised next steps (3/10 → professional)

1. **Stand up the 3D-from-CAD render pipeline** (Blender headless + STEP import). Biggest single
   quality lever — gives every post a real, accurate product hero. _Or KeyShot if speed > scripting._
2. **Finish design-system fidelity in the pipeline:** canonical `colors_and_type.css` + Aeonik
   `.otf`s + real curve-motif PNG (already on the desktop list). Takes brand-correctness to 100%.
3. **Define the illustration style:** build a **Recraft custom style** (or train a FLUX LoRA) from a
   handful of approved references → the consistent line-art layer.
4. **Build a template library from teardowns:** product-feature, before/during/after, spec/compliance,
   testimonial, educational carousel, story 1080×1920 — skeletons from inspiration, poured into our tokens.
5. **Image-treatment pass in sharp:** green-duotone + motif overlay + grain so any photo reads as Craftons.
6. **Video finishing script + Whisper captions + atomisation.**
7. **Wire the brand-QA gate:** `tokens.json` + oxlint adherence check before the human approval.

---

## Sources
**AI generation:** [NomadLab 2026 models](https://nomadlab.cc/blog/2026/05/best-ai-image-generators-2026-midjourney-flux-ideogram-recraft-firefly) · [Recraft V4 (MindStudio)](https://www.mindstudio.ai/blog/what-is-recraft-v4-design-forward-image-model) · [Recraft custom styles](https://www.recraft.ai/blog/how-to-generate-ai-images-in-your-own-design-style) · [Recraft pricing](https://flowith.io/blog/recraft-pricing-2026-free-vs-pro-vs-team/) · [FLUX.2 (VentureBeat)](https://venturebeat.com/ai/black-forest-labs-launches-flux-2-ai-image-models-to-challenge-nano-banana) · [FLUX.2 pricing/guide](https://www.glbgpt.com/hub/flux-2-pro-guide/) · [FLUX licensing (Wikipedia)](https://en.wikipedia.org/wiki/Flux_(text-to-image_model)) · [LoRA guide](https://imagera.ai/guides/what-is-lora-guide-ai-model-fine-tuning-2026) · [Replicate FLUX fine-tunes](https://replicate.com/collections/flux-fine-tunes) · [Firefly commercial use](https://tensoria.fr/en/tools/adobe-firefly-ai-commercial-images)
**Compositing:** [Satori README](https://github.com/vercel/satori/blob/main/README.md) · [Playwright vs Puppeteer 2026](https://snapapi.pics/blog-playwright-vs-puppeteer-screenshots.html) · [Design Tokens Format](https://www.designtokens.org/tr/drafts/format/) · [Style Dictionary (DOOR3)](https://www.door3.com/blog/transforming-tokens-for-development) · [Figma API rate limits](https://developers.figma.com/docs/rest-api/rate-limits) · [Canva Connect autofill](https://www.canva.dev/docs/connect/api-reference/autofills/) · [sharp performance](https://sharp.pixelplumbing.com/performance/)
**3D/CAD:** [KeyShot 2026.1 (CG Channel)](https://www.cgchannel.com/2026/03/keyshot-releases-keyshot-studio-2026-1/) · [KeyShot pricing](https://www.myarchitectai.com/blog/keyshot-pricing) · [Blender CLI](https://renderday.com/blog/mastering-the-blender-cli) · [Blender programmatic rendering](https://blog.cg-wire.com/blender-programmatic-rendering/) · [Import CAD Model addon](https://github.com/chenpaner/Import-CAD-Model) · [AI vs 3D rendering (Pixready)](https://www.pixready.com/blog/ai-product-rendering-vs-professional-rendering) · [9 AI 3D render tools](https://brandclickx.com/9-ai-tools-for-generating-3d-product-renders-in-2026/)
**Video:** [AI video APIs guide 2026 (WaveSpeed)](https://wavespeed.ai/blog/posts/complete-guide-ai-video-apis-2026/) · [AI video pricing (FluxNote)](https://fluxnote.io/guides/ai-video-model-pricing-comparison-2026) · [Veo 3.1 pricing](https://www.aifreeapi.com/en/posts/veo-3-1-pricing) · [Replicate text-to-video](https://replicate.com/collections/text-to-video) · [Remotion](https://www.remotion.dev/) · [Subtitle accuracy 2026](https://fluxnote.io/guides/best-free-ai-subtitle-generators-2026) · [OpusClip strategy 2026](https://www.opus.pro/blog/short-form-video-strategy-2026)
**Brand QA / inspiration:** [Design tokens 2026](https://www.oneminutebranding.com/blog/design-tokens-2026) · [Linting design tokens](https://www.alwaystwisted.com/articles/where-to-lint-design-tokens) · [AI brand management (Frontify)](https://www.frontify.com/en/guide/ai-for-brand-management) · [Firefly vs Canva tested](https://aitoolscapital.com/blog/adobe-firefly-vs-canva-ai-2026) · [Idea–expression (Wikipedia)](https://en.wikipedia.org/wiki/Idea%E2%80%93expression_distinction) · [Trade dress (Wikipedia)](https://en.wikipedia.org/wiki/Trade_dress) · [Swipe Files teardowns](https://www.swipefiles.com/teardowns)
