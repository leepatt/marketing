# Craftons content — quality doctrine (the anti-slop rules)

_Why our output won't look like generic AI slop. Design every asset to this. 2026-06-16._

## The one-line principle
**Render real things; constrain the AI; a human curates.** AI proposes, Craftons disposes.

## The anti-slop stack (it's a system, not one setting)
Quality comes from layers, not a single "train" button or the inspo folder alone:

1. **Render the real thing, don't generate a fake one.** The heroes — product shots, the Formwork
   Builder reel — are *rendered from real data* (Blender on real CAD geometry; Playwright on the real
   UI). Pixel-exact, not "imagined." This removes slop risk entirely for the most important content.
2. **Design tokens (enforced).** The design system forces on-brand colour/type/spacing; the
   `_adherence` lint flags raw hex/px/off-system fonts. Brand-correct by construction.
3. **A locked style.** For AI illustration, train a **Recraft custom style or FLUX LoRA on ~10–30
   *approved* Craftons pieces** so every output shares one look. Consistency = not slop.
   ⚠️ Train on our *best, approved* work — garbage in = slop out.
4. **Inspiration teardowns.** The inspo folder sets the quality *bar* and a composition vocabulary —
   study the **skeleton (grid/hierarchy/eye-flow), not the skin**; rebuild in Craftons tokens.
   It informs templates/prompts; it is *one* layer, not the whole answer.
5. **The human gate (decisive).** Nothing publishes without a person picking the good output and
   killing the rest. Slop is what you get when nobody curates. Taste stays human.
6. **Iterate.** Winners → swipe file → tighten the rules/style → next batch is better. Compounding.

## Where AI is allowed vs not
- **AI generates:** background scenes, b-roll, explainer illustration, atmosphere. (The edges.)
- **AI never generates:** the product's hero geometry or exact dimensions. Those are *rendered* from
  CAD/real footage. (Per standing rule: real leads, AI extends, a human approves every asset.)

## Motion rules (for animation/video — full detail in `research/2026-motion-design.md`)
Premium motion is physics, not luck. Encode these in every template:
- **Never linear easing.** Default `ease-out`; standard `cubic-bezier(0.4,0,0.2,1)`; UI moves ≤300ms.
  Use a fixed palette of 3–4 easings everywhere (spring-based where possible).
- **2–3% overshoot-then-settle** on pop-ins; **stagger** grouped elements 0.05–0.15s.
- **One focal move per shot:** Z-axis push-in to the active element, dim/spotlight the rest; parallax for depth.
- **Reveal with a sweep/Z-zoom**, not a hard cut. **Count-ups** for numbers. **Cut to the beat.**
- **Hook ≤2.5s**, pattern-interrupt open; micro-cuts (0.4–1.2s) early then every 3–5s; design to **loop**.
- **Sound design on every transition/CTA** (click/whoosh/pop) — the cheapest premium upgrade.
- **Motion blur on big moves only**; animate transform/opacity only at 60fps; **restraint** (every motion has a job).
- **Lead with the product in interactive 3D** (configurator + exploded view) — proven to convert for manufacturers.

## Practical checklist before any asset ships
- [ ] On-brand tokens (colour/type/spacing) — passes the adherence check?
- [ ] Hero product/UI = rendered from real data (not AI-imagined)?
- [ ] If AI illustration: from the locked Craftons style, not a one-off random look?
- [ ] Composition has a clear focal point + hierarchy (not flat text-on-colour)?
- [ ] In-image text is human-set/verified (AI text fails ~20% of the time)?
- [ ] A human approved it (Gate 2)?
