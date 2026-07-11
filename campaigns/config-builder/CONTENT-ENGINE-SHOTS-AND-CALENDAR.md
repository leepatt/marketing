# Content Engine — Shot Library & First-Month Reels (draft)

_Companion to `CONTENT-ENGINE-SPEC.md`. The reusable shot modules + the first month's actual reels._
_Draft 2026-07-11 — motion/type treatment to be finalised from the Monday.com house-style research._

---

## Shot library (reusable modules)

Every reel is assembled from these. Each is a spec-driven module; mix/match/reorder per brief.

| # | Shot | What it is | Render path |
|---|------|-----------|-------------|
| S1 | **Hook card** | Bold kinetic title on brand ground + curve motif ("SO WE BUILT… / DESIGN CUSTOM CURVES. ONLINE.") | Remotion (type) |
| S2 | **Config demo** ⭐ | The hero beat: real configurator UI, synthetic cursor, auto-zoom, dims typed, **price ticks up**, Add to Cart. Stepped captions. | puppeteer-capture → Remotion |
| S3 | **Native-3D build** | The part draws/extrudes/assembles/nests itself; exploded view; parametric to the exact dims | @remotion/three |
| S4 | **Photoreal turntable** | Cinematic beauty spin of the finished part (real timber grain / concrete) | Blender Cycles |
| S5 | **The match / digital twin** | Real footage of the finished product ↔ configurator building the same dims, side-by-side or morph | footage + S2/S3 |
| S6 | **Screen → machine** | Transition from the on-screen part to real CNC/factory footage cutting it | Tia footage + Remotion |
| S7 | **Product in place** | Tia's footage of the finished install, with animated dimension callouts over it | OffthreadVideo + Remotion |
| S8 | **Promise / stat card** | Kinetic type stat (lead time, 0.5mm tolerance, free shipping, "Pre-Fab. Pre-Cut. Site-Ready.") | Remotion (type) |
| S9 | **Logo outro + CTA** | Curve-motif draw-on, wordmark, CTA ("Configure yours · craftons.com.au") | Remotion |
| S0 | **Presenter (optional)** | Overlay layer: none / real (Lee/Tia) / AI avatar — can sit over any shot | footage / avatar |

**House skeleton (default, presenter-free, ~18–24s):**
`S1 hook → S2 config demo → S6 screen→machine → S7/S4 real or photoreal product → S8 promise → S9 outro`
(the proven arc from the current Radius Pro ad, upgraded — S2 is the beat that jumps most in quality.)

---

## First month — 4 reels (one/week)

Anchored to confirmed converters ("curved bench seat", "bendy ply") and the hero products. Same skeleton, swap
product + dims + footage → this is how the house **template** gets locked (Lee: "when we create a few, we'll have
a template").

### Week 1 — Radius Pro · Curved bench seat
- **Story:** "Design a curved bench seat. Online." Configure R800 × W450 × 180° → price → dispatched in 3 days.
- **Beats:** S1 → S2 (Radius Pro, live) → S3 build → S7 Tia's real curved bench install → S8 "3 business days" → S9.
- **Footage need (Tia):** a finished curved bench seat / curved feature. **Confirmed converter — lead with this.**
- **Note:** direct upgrade of the existing Radius Pro ad — same story, far better config beat.

### Week 2 — Formwork Builder · Curved concrete formwork
- **Story:** the "world-first" in-house tool. "Curved bench seat… over there." Configure → formwork → pour → done.
- **Beats:** S1 → S2 (Formwork) → S4 photoreal formwork/curve → S5 match: configurator ↔ real poured bench → S8
  "Pre-Fab. Pre-Cut. Site-Ready." → S9. (Reuses the written Formwork promo script — see `Craftons-formwork-builder-promo.md`.)
- **Footage need:** concrete pour into curved timber formwork + finished poured bench.

### Week 3 — Curved Architraves
- **Story:** curved architrave around an arch window/doorway — "the curve no one else will cut."
- **Beats:** S1 → S2 (Curved Architraves) → S3 build → S7 real arch install + callouts → S8 tolerance/AU-made → S9.
- **Footage need:** an arched doorway/window with curved architrave installed.

### Week 4 — Bendy Ply / Radius Pro · Curved feature wall  (or Stair Builder)
- **Story:** "bendy ply" (confirmed converter) → a curved feature wall. Alt: Stair Builder curved stringer.
- **Beats:** S1 → S2 → S4 photoreal curved ply → S6 screen→machine (CNC cutting the curve) → S8 → S9.
- **Footage need:** curved feature wall / bendy-ply install, or CNC cutting footage.

---

## Production notes
- **Footage is the gating input** — Tia films real completed jobs; only build a reel for a job we've actually
  done. Start the footage library now (Drive) so Weeks 1–4 have real product to cut to.
- **Reuse across reels:** S1/S8/S9 are near-identical templates (swap text); S2 differs only by route + dims;
  S3/S4 are parametric. After Week 4, the house template is locked and weekly effort ≈ "edit last week's spec."
- **Per-reel toggles** (option-for-everything): presenter none/real/avatar · VO on/off (Gemini default) ·
  captions kinetic · look stylized/photoreal · music (Monday-snappy).

## TODO after house-style research
- Fill in the exact motion/type/color treatment for S1–S9 (Monday.com-adapted).
- Lock durations per shot and the cut rhythm.
- Decide the recurring transition device (motif wipe? color-block? spring cut?).
