# Session findings — 2026-08-03 (second session)

_Verification results and environment constraints from continuing the Meta ads agent build._
_Recorded so the next session doesn't re-derive any of it._

---

## Phase 0 — verified live today

| Item | Status | Evidence |
|---|---|---|
| **Advanced Matching** | ✅ **ON** | `enable_automatic_matching: true`, all 11 params (`em, fn, ln, ge, ph, ct, st, zp, db, country, external_id`) |
| **Pixel health** | ✅ Firing | `last_fired_time` current; ViewContent / PageView / AddToCart / ConfiguratorStarted all accruing hourly |
| **Custom conversion** | 🔴 **Still missing** | `GET act_1650412872259063/customconversions` → `{"data":[]}` |
| **Event Match Quality** | ⏳ Not yet readable | `match_rate_approx: -1`. Advanced Matching only went on 2026-08-03, so 24–48h is needed regardless |

**The combined custom conversion (InitiateCheckout OR Purchase, ~53/wk) remains the last Phase 0 gate.**
It is an account write, so it needs Lee's explicit go-ahead — asked, not yet answered.

---

## The warehouse question — answered with data

Asked directly: *has the data warehouse been built?* **Yes, and it pre-dates this work.** Queried Neon:

| Table | Rows |
|---|---|
| `marketing_metrics_cache` | **485** (261 `meta`, 224 `google_ads`) |
| `marketing_runs` | **150** |
| `marketing_assets` | **8** |
| `marketing_approvals` | **6** |

Runs are landing (`meta-ads report` + `google-ads report` both 2026-08-03 05:55).

**The decision that matters: we deliberately did NOT build a second warehouse.** Airbyte → ClickHouse
is right for an agency with 30 clients across 12 sources; for one brand and three sources it is weeks
of ops work for no gain. `marketing_metrics_cache` already is the warehouse (bible §7).

---

## 🔴 Environment constraint — Chromium has no egress

**Headless Chromium cannot reach the public internet from this container.** Verified: `example.com`
returns `net::ERR_CONNECTION_RESET`, with and without `--proxy-server=http://127.0.0.1:45091`.
`curl` to the same hosts works fine (200), so this is browser-specific, not an egress policy block.

This is the same limitation the bible records in §0 (the YouTube video couldn't be watched).

**Consequence:** any Playwright work against a *deployed* URL is impossible here. The only path is to
run the target app **locally** and drive `127.0.0.1`, which `no_proxy` covers.

### Running the Radius Pro configurator locally — the working recipe

```bash
git clone --depth 1 https://github.com/leepatt/craftons-curves-calculator /workspace/craftons-curves-calculator
cd /workspace/craftons-curves-calculator && npm install
npx next dev --turbopack -p 3210     # ✅ ready in ~2s, serves 200 on 127.0.0.1:3210
```

Runs clean with no env vars set. Next.js 16.0.10.

### The configurator's real DOM (recon, so nobody re-probes it)

Deployed at `https://craftons-curves-calculator.vercel.app`, embedded as a **cross-origin iframe** on
`craftons.com.au/products/radius-online`.

**Inputs** (all `<input type=number>`, React-controlled):
`#specifiedRadius` · `#width` · `#angle` · `#arcLength` · `#chordLength` · `#part-quantity`

**Material:** a single `<select>`. Options observed:
Formply 17mm · BC Structural Plywood 15/18/25mm · MDF Standard 12/18mm — all 2400×1200mm.

**Controls:** `3D View` · `Internal Dimensions` / `External Dimensions` toggle ·
`Add straights to curve ends` · `Add Part`

**Layout:** left = live geometry preview (black curve segment, green dimension annotations r/w/θ/L/c);
right = "Configure Curve" panel. Enter any one of Angle/Arc/Chord and the other two compute.

⚠️ **React gotcha:** setting `.value` directly is swallowed by React's value tracker. Use the native
setter then dispatch `input` + `change`:

```js
const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
setter.call(el, String(val));
el.dispatchEvent(new Event('input',  { bubbles: true }));
el.dispatchEvent(new Event('change', { bubbles: true }));
```

---

## The research pass does not work for this niche

`meta-ads.mjs research` ran twice, successfully (both wrote `marketing_assets` rows). Both **honestly
declined to produce a ranking** rather than inventing quotes — the correct behaviour, worth keeping.

| Run | Model | Returned |
|---|---|---|
| 1 | `sonar` | Vendor how-to pages, generic woodworking videos |
| 2 | `sonar-pro`, forums named in the query | r/AusRenovation threads about **finding and chasing tradies** |

**Conclusion: stop spending sessions on this.** Australian tradies discussing the specifics of kerfing
bending ply is too thin a public corpus to mine. `brand/audience.md` — real customer contact — is a
better source and already exists. Cody's step one is a dead end here; the bible predicted as much.

**What it did earn:** trade jargon worth putting in copy —
*kerf bend · kerfing · relief cuts · tear-out · splintering · good face · flush-trim · template ·
registration cut · repeat accuracy · radius formwork*

---

## Creative asset audit

Real photography in `cnccut-app/content-engine/sandbox/real/`:

| Asset | Usable for Radius Pro ads? |
|---|---|
| `shop-radiuspro.png` (1200²) | ✅ Black-faced curved ply segment, laminated edge, on white — the hero |
| `shop-radius-render.png` (873²) | ✅ Same geometry, tighter crop |
| `shop-bendingply.png` (720²) | ✅ Rolled bending ply — the natural "bendy ply" asset |
| `shop-formwork.png`, `shop-architrave.png` | ➖ Other product lines, out of scope (Radius Pro only) |
| **`tradie-portrait.png`** | ⛔ **Excluded — AI-generated stock face** |

> **On `tradie-portrait.png`:** it is a synthetic person. Placing a fake face beside product copy edges
> toward implied endorsement, which is the §4.2 line — and the `avatar` family is meant to be HeyGen
> *presenters*, not a static stock portrait. No upside, real downside. Do not use it in paid.

**The supply problem is unchanged:** three usable real stills for a batch that needs 15–20 diverse
creatives. That is exactly why the configurator family matters — it is the only source of unlimited,
genuinely different, *true* visual output.

---

## Course correction

Creative capture work was started from scratch this session and **stopped by Lee** — correctly.
Craftons already has a validated capture pipeline (a skill with `scripts/diag.mjs`,
`scripts/capture.mjs`, `scripts/wheel-cal.mjs`, `template/index.html`, `template/README.md`).
**That skill is not present in this session's container** — it must be pushed to an attached repo, or
named so it can be added, before any further capture work happens.

The bespoke script written here was deleted rather than committed: a second, unvalidated capture layer
in the repo would be worse than none. Its durable knowledge is the DOM recon above.

**Scaffolding status: ~90% complete.** The machine is built (warehouse, guardrails, 10 subcommands,
publish chain, weekly cron). What it lacks is fuel — creatives to run through it. The genuinely
scaffolding-shaped piece still missing in Phase 3 is **the asset pipeline**: the seam that turns
capture output into brand-checked, recipe-carrying `marketing_assets` rows ready for
`create-creative`. That seam is where the capture skill plugs in.
