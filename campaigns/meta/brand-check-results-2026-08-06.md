# Brand-check results — full 36-creative batch, 2026-08-06

_First live run of the vision quality gate. Every verdict is from real pixels: `studio.mjs
brand-check --asset_id=<id>` per keeper row, model `claude-fable-5`, scored against the inline
Craftons rubric. Full per-asset reasons live in `marketing_assets.provenance->'brand_check'`._

**33 pass · 3 fail · 0 errors.** Median pass score 86.

| Creative | Verdict | Score |
|---|---|---:|
| `a1-design-with-confidence` | ✅ pass | 84 |
| `a1-less-measuring-mono` | ✅ pass | 84 |
| `a1-marked-out-wrong` | ✅ pass | 88 |
| `a1-measure-specify-build` | ✅ pass | 86 |
| `a1-no-templates` | ✅ pass | 82 |
| `a1-nobody-marks-out` | ✅ pass | 92 |
| `a1-put-the-jigsaw-down` | ✅ pass | 78 |
| `a1-straight-off-the-plans` | ✅ pass | 82 |
| `a1-the-maths-done` | ✅ pass | 88 |
| `a2-less-in-the-bin` | ✅ pass | 92 |
| `a2-mono-waste` | ✅ pass | 78 |
| `a2-nested-not-guessed` | ✅ pass | 86 |
| `a2-offcuts-problem` | ✅ pass | 82 |
| `a2-pay-for-parts` | ✅ pass | 92 |
| `a2-price-before-commit` | ✅ pass | 83 |
| `a3-add-a-tail` | ✅ pass | 86 |
| `a3-any-radius` | ✅ pass | 80 |
| `a3-cut-labelled-done` | ✅ pass | 86 |
| `a3-double-them-up` | ✅ pass | 92 |
| `a3-engineered` | ✅ pass | 86 |
| `a3-interstate` | ✅ pass | 70 ⚠️ |
| `a3-nobody-measures-onsite` | ✅ pass | 88 |
| `a3-three-days` | ✅ pass | 74 ⚠️ |
| `a4-any-trade` | ✅ pass | 84 |
| `a4-builders` | ✅ pass | 86 |
| `a4-builders-price` | ✅ pass | 85 |
| `a4-chippies` | ✅ pass | 92 |
| `a4-chippies-jigsaw` | 🔴 fail | 55 |
| `a4-concreters` | ✅ pass | 88 |
| `a4-formworkers` | ✅ pass | 92 |
| `a4-landscapers` | ✅ pass | 92 |
| `brand-radius-pro-deep` | ✅ pass | 86 |
| `brand-radius-pro-sage` | ✅ pass | 84 |
| `lf1-control-lawless` | ✅ pass | 74 ⚠️ |
| `lf2-pay-for-parts` | 🔴 fail | 55 |
| `lf3-nobody-sets-out` | 🔴 fail | 58 |

---

## The fails split into two different problems

### 1. A real catch — the empty-canvas layout (regenerate these)

**`a4-chippies-jigsaw` (fail, 55):** _"roughly two-thirds of the canvas is empty black space
where product imagery clearly belongs — the layout reads as unfinished... it would ship looking
broken at feed size."_ The same note holds `a3-interstate` (70) and `a3-three-days` (74) to low
passes: type-only layouts whose big empty region reads as a missing hero image rather than
deliberate whitespace.

**Action:** regenerate these three with real product/photo content in the void. This is also
one more argument for the photography lever — the checker keeps asking for exactly the raking-light
real-product imagery the shot list (`creative-strategy.md` §4.1) already calls for.

### 2. A rubric mismatch — bare real-footage creatives (Lee's call, nothing relabelled)

**`lf2-pay-for-parts` (55) and `lf3-nobody-sets-out` (58)** are `bare`-template real-footage
creatives: the winning site photo with **no overlay by design**, because the account's best-ever
ad (10.45% CTR) was exactly that — their six-paragraph copy runs as *primary text*, not in-image.
The checker is fed "the headline it should carry: X" from the recipe, so it fails them for
carrying no text; it also docks genuine outdoor photography for sky ("blue cast").
`lf1-control-lawless` scraped through at 74 with identical notes — on both fails the checker
itself calls the photograph "strong and on-brand... not AI slop."

**The verdicts stand — nothing was relabelled.** The honest fix is to make the checker accurate
for this family: tell it when a creative is `bare`/real-footage (copy lives off-image; natural sky
≠ palette violation). That loosens what the quality gate accepts, so it needs Lee's explicit OK
before anyone touches the rubric in `tools/studio.mjs`.

---

## What this run proved about the machine

- The vision path works end-to-end: it reads real pixels, catches genuine layout problems,
  verifies headlines word-for-word, and even re-derives the arc/chord maths shown in configurator
  screenshots to check the geometry is real.
- First live run exposed a real bug, now fixed and pushed (`cnccut-app` `01bd418`): a 500-token
  `max_tokens` cap truncated every response (thinking shares the budget on `claude-fable-5`), and
  the old fallback recorded truncation as a fail with score 0. Unreadable responses now error and
  leave the asset outstanding instead of writing a false verdict.
- Scoring was done per-asset against the 36 keeper rows, so the 36 duplicate `pending` rows
  (still awaiting Lee's approved DELETE) were never scored — no double spend, no double review.
