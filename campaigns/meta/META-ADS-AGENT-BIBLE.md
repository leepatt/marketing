# The Meta Ads Agent — Bible

_The reference doc for standing up an autonomous Meta ads agent for **Craftons**, starting with
**Radius Pro**. Digested from the Greg Isenberg × Cody Schneider episode, then translated to what
Craftons actually has, actually sells, and actually needs._

**Created:** 2026-08-03 · **Branch:** `claude/marketing-agents-setup-qamq2f`
**Status:** design locked, not yet built.
**Scope decisions (Lee, 2026-08-03):** Craftons only · human-approves first, autonomy earned ·
code lives in `leepatt/cnccut-app` · lightweight data layer first · **Radius Pro only** to start.

> **Read `STATUS.md` first, then this.** This doc is the *what and why*. The build steps in Part 5
> are the *how*. Nothing here has been implemented yet.

---

## 0. Source & provenance (what this is built from, and how confident to be)

| Source | Confidence |
|---|---|
| **Full transcript** of the episode (supplied by Lee) | ✅ Primary, verbatim |
| **Official video description** — Greg's team published numbered per-section summaries narrating each screen-share | ✅ Primary |
| **Live recon of `leepatt/cnccut-app`** (cloned 2026-08-03, HEAD `01f69e3`) | ✅ Ground truth |
| **Live recon of `leepatt/marketing`** (this repo) | ✅ Ground truth |
| **Web verification** of every tool + platform claim | ✅ Checked, see §1.7 |
| **The video's visuals** | ❌ **Not seen — see below** |

**Video:** *"Marketing Agents Are Too Good Now"* — Greg Isenberg + Cody Schneider, published
27 Jul 2026, 37:47. Cody's company is **graphed.com**.

### Honest limitation

The video could not be watched in the build environment. YouTube's media endpoints returned 403
(bot-detection / PO-token gate) across every player client; the headless browser has no egress in
this container; storyboard frames are only 160×90 and unreadable. **No frame of this video has been
seen.**

Practical impact: **low.** All four screen-shares are narrated aloud in the transcript, and the
official description independently describes each one. The load-bearing visual — the whiteboard
diagram at ~20:54–22:12 — is drawn while Cody describes every node and arrow, so it is reconstructed
in §1.3 from his own words, not from guesswork.

**Unrecovered:** the exact Kie.ai interface, the on-screen Perplexity output, the WordPress
market-share page. None affect implementation. If precision on those matters, screenshot them and
drop them in Drive.

---

# PART 1 — The doctrine

## 1.1 What actually counts as a "marketing agent"

Cody's central claim is a definition, and it's worth taking seriously because it excludes most of
what gets marketed as an agent. Three conditions, all required:

1. **Unified data.** The agent sees the whole pipeline in one place — not one channel's dashboard.
2. **Autonomous decisions on a cadence.** It runs on a clock and decides, rather than waiting to be
   prompted.
3. **A feedback loop.** It reads its own results back and changes what it does next.

His explicit exclusion: a linear automation workflow (Zapier/n8n-style) is **not** an agent. It has
no memory of outcomes and no ability to change its own behaviour.

His equally explicit *anti*-claim, which matters just as much: he does **not** want a general
reasoning agent. He wants something that runs a defined process, reads the numbers, and improves.
Narrow and measurable beats clever.

> **Why this framing is right for Craftons:** it sets the bar at "does it close the loop", not "does
> it feel autonomous". A weekly report that a human acts on is not an agent. The same report feeding
> a decision the system takes and then measures — that is.

## 1.2 The Andromeda shift — creative *is* the targeting

The single most important platform fact in the episode, and the reason the whole approach works.

**Before:** you targeted interests, demographics, lookalikes. Cody would have targeted "people with
a WordPress interest".

**Now (Andromeda):** Meta's retrieval engine reads your *ad creative* — the image, the text, the
video, the script — **and your landing page**, and decides who to show it to. Audience definitions
are advisory; creative signals override them.

**Consequence:** you no longer target an audience. You write creative that *describes* your customer's
problem, and Meta finds whoever has that problem. Cody's phrasing: Facebook has become the best B2B
channel that exists, because you can write an ad so specific that maybe ten people in the country
have that problem — and Meta will find those ten.

**Verified specifics** (independent of the video, from 2026 Andromeda coverage):

- Meta's own testing: **one ad set with 25 diverse creatives beat five ad sets with five creatives
  each — 17% more conversions at 16% lower cost.**
- The recommended shape: **fewer campaigns, fewer ad sets, more creatives per ad set, broad targeting.**
- **15–20 active ads** with genuinely different hooks and formats is the working creative-diversity floor.
- **Pixel + CAPI running simultaneously**, with **Event Match Quality above 7**, is a hard prerequisite —
  the algorithm can only read creative well if the conversion signal is clean.
- Accounts on the new structure are reportedly seeing 20–35% higher ROAS than legacy structures.

> ⚠️ **This is the constraint that will bite Craftons hardest.** Andromeda wants 15–25 genuinely
> different creatives per ad set. Craftons' current real-footage supply is ~2–3 pieces/month from Tia.
> §4.3 solves this. It is the most important section in the doc.

## 1.3 The architecture (reconstructed from the whiteboard segment)

Cody draws this live at ~20:54–22:12. In his own words, the loop is:

```
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │  Meta Ads   │   │  Analytics  │   │   Stripe /  │      ← N data sources
   │    data     │   │   / GA4     │   │  CRM / rev  │
   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
          │                 │                 │
          └────────┬────────┴────────┬────────┘
                   ▼                 ▼
            ┌──────────────────────────────┐
            │       DATA WAREHOUSE         │   ← one place, all sources in context
            └───────────┬──────────────────┘
                        │  ▲
              reads     │  │   results flow back in
                        ▼  │
            ┌──────────────────────────────┐
            │      META ADS AGENT          │   ← thinking loop, on a cadence
            └───────────┬──────────────────┘
                        │  writes only
                        ▼
            ┌──────────────────────────────┐
            │   META ADS ACCOUNT           │   publish · pause · promote
            └──────────────┬───────────────┘
                           │
                           └──────► back into the warehouse ──┘
```

Three structural points he makes explicitly:

**(a) The warehouse exists so the agent sees sources *in context with each other*.** Not "Meta data"
and "revenue data" separately — the join. The question it must be able to answer is *which specific ad
produced revenue*, and you cannot answer that from inside Meta's dashboard.

**(b) The API is for writes, not reads.** This is his most actionable warning. The "my ad account got
banned by my agent" stories are not caused by agents — they're caused by people hammering the
Marketing API to pull hundreds of millions of rows, which violates the terms. **Use the API to
publish, pause, and promote. Get your reporting from the pipeline.**

**(c) The human gets the warehouse too.** A side benefit he emphasises: once the data is unified, you
can ask it questions conversationally from your own terminal, and build dashboards off it. The agent
and the operator read the same table.

**His recommended stack:** Airbyte (pipeline) → ClickHouse (warehouse), both self-hostable, plus
cloud hosting for the agent (Heroku, Railway, "any cloud"). He is explicit that a Mac Mini under your
desk is not required and slightly absurd.

## 1.4 The creative pipeline

Two tracks, both agent-driven.

**Research (seeds everything).** Perplexity, pointed at Reddit, to extract the real pain points and
desired outcomes of the target customer — *because Reddit is real people complaining*. Then a second
pass: **rank the pain points by how often they're referenced.** The top three become the ad angles.

He flags his own caveat honestly: Reddit is being polluted by people manipulating it for LLM
visibility ("I am the problem"). Still the best available source of unguarded language.

**Static creative.** Kie.ai as the aggregator (one API, many models), generating through **Google Nano
Banana**. The technique that makes it work: **seed it with an example ad already running** — from a
competitor or a tangentially related industry — rather than prompting from nothing. Then put a
**vision model over every output** to check it against brand style guides: right fonts, right colours,
text actually readable.

**Video creative.** HeyGen for AI-avatar UGC, with Seedance coming up fast. The talking head reads
the pain points and outcomes pulled from the research.

> **Correction — this part of the video is already stale.** Cody says Seedance caps around nine
> seconds and the hard part is stitching frames for a 30-second spot. As of 2026: **Seedance 2.0**
> does 10–15s per generation with a video-extension feature for arbitrary length, and **Seedance 2.5**
> does **30-second 4K clips with native audio in a single pass**, taking up to 50 multimodal reference
> inputs. The stitching problem he describes is essentially solved. Don't build a frame-stitcher.

## 1.5 The operating loop

What he's running for clients right now:

- **2 ad sets/day, 5 ads per ad set** — 10 new ads daily, published automatically.
- **2–3 day read window** per batch, to get initial signal.
- **Kill the worst performers**, using data pulled from the warehouse, not the API.
- **Winners survive and enter a winners pool**, where they compete against each other for budget.
- **Feedback:** the agent analyses what won and makes more like it.

The subtle part, and the best idea in the episode: **what gets stored is not the finished ad — it's
the recipe.** They keep a database of the actual JSON prompts sent to Nano Banana and the scripts sent
to HeyGen. The agent analyses *the recipes of winners*, so it learns "this kind of hook, this kind of
composition" rather than "this exact image". That's what makes the loop compound.

## 1.6 Entropy — the failure mode nobody talks about

Cody's most valuable warning, and he's right that it's under-discussed. **The agent gets stuck
thinking the same way.** It converges on a narrow band of creative, performance decays, and because
each day looks fine relative to yesterday, you don't notice until it's bad.

His framing: it might feel good on day one, slightly worse on day two, and by day five you have a
problem. Marketing is no longer campaigns with a start and a stop — it's a continuous system that
needs deliberate novelty injected.

**Three sources of fresh DNA:**

1. **Meta Ad Library** — pull competitors' live ads. Free, public, no auth.
2. **YouTube + podcast transcripts** in your category — extract insights, run ads off them.
3. **Short-form trend data** — he names the tool as (transcribed) "Viral Low"; the real product is
   **Virlo** (`virlo.ai`), which scrapes TikTok / Reels / Shorts and has a **Trends & Virality API**.
   Query it for what's spiking in a category and let that shape creative format.

## 1.7 Transcript corrections (verified)

The auto-transcript garbles several names. Corrected here so nobody chases a ghost:

| Transcript says | Actually | Note |
|---|---|---|
| "companiesgraph.com" | **graphed.com** | Cody's company |
| "air bite" | **Airbyte** | open-source data pipeline |
| "Kai AI" | **Kie.ai** (high confidence, not certain) | one-stop image/video model API, credit billing — matches his description exactly |
| "Viral Low" | **Virlo** (`virlo.ai`) | ✅ confirmed; has a public Trends & Virality API |
| "a kismmet" | **Akismet** | WordPress spam plugin |
| "Seed Dance" | **Seedance** | ByteDance video model |
| "Google Nana Banana" | **Nano Banana** | Google's image model (Gemini image) |
| "Yoast" (pronounced) | **Yoast SEO** | correct, just phonetic |

**Not verified / open:** Kie.ai is the strongest match for "Kai AI" — an API aggregator for image and
video models with credit billing — but Cody never spells it on the transcript. Confirm before wiring.

**Also worth noting:** the first ~10 minutes and the closing are a WordPress startup pitch and a
channel-feedback ask. Zero relevance to Craftons. Everything useful is 09:55–34:26.

---

# PART 2 — Where Craftons actually is (the surprise)

**The single most important finding of this session.** The marketing repo's notes describe
`tools/meta-ads.mjs` as a thing that "already exists with a CONFIRM=1 guardrail" and otherwise imply
the ads engine is unbuilt. That is badly out of date.

Recon of `leepatt/cnccut-app` (HEAD `01f69e3`) shows **most of Cody's architecture is already
built** — under different names, and better suited to Craftons than his version.

### Already built — do NOT rebuild

| Cody's component | What Craftons already has | Where |
|---|---|---|
| Data warehouse | **`marketing_metrics_cache`** on Neon Postgres — source, scope, metric, value, jsonb payload, period start/end | `drizzle/marketing/0001_marketing_cockpit.sql` |
| Agent run history | **`marketing_runs`** — tool, subcommand, args, status, output markdown, structured result, cost, timings | same |
| The human gate | **`marketing_approvals`** — module, action, payload, `pending\|approved\|rejected`, approver, source/executed run IDs | same |
| Creative memory | **`marketing_assets`** — kind, brand-check status, storage ref, **`provenance` jsonb** | same |
| Meta reporting | **`tools/meta-ads.mjs report`** — live Graph API insights at account / campaign / **ad** level, prior-period deltas, daily trend, and a **wasted-spend flag** (`spend > 0 && results === 0`) | `tools/meta-ads.mjs` |
| Image generation | **`tools/studio.mjs generate`** — Replicate **and** Glif wired | `tools/studio.mjs:151-221` |
| **Cody's vision-model brand check** | **`tools/studio.mjs brand-check`** — already exists as a subcommand | `tools/studio.mjs:386` |
| Rate-limit discipline | **`_lib.mjs fetchJson`** — backoff, honours `Retry-After` | `tools/_lib.mjs` |
| Agent hosting | **Vercel** (Next.js 16.1.6), with `POST /api/marketing/run` dispatching by tool name | `vercel.json`, `lib/marketing/run-tool.ts` |
| Operator dashboard | **Marketing Cockpit** at `/marketing` — 8 modules, all `status: "built"`, with a Run panel that renders each run's markdown | `lib/marketing/modules.ts` |
| Google Ads equivalent | **`tools/google-ads.mjs`** (41KB) — full `propose` → approve → `apply` pattern | `tools/google-ads.mjs` |

### The three things this changes

**1. The "lightweight data layer" decision is already made and already shipped.** `marketing_metrics_cache`
is exactly the Airbyte+ClickHouse replacement — one table, timestamped, jsonb payload, already being
written to by `meta-ads.mjs report` via `cacheMetric()`. **No Airbyte. No ClickHouse. No new database.**
Cody's stack is right for an agency running many clients across many sources. For one brand and three
sources it is enormous overkill.

**2. The autonomy dial is already built.** `marketing_approvals` with `pending → approved → rejected`
*is* the "human approves first, agent earns autonomy later" model, in schema form. The graduation
path in §6 is a change to which actions require a row — not new infrastructure.

**3. `google-ads.mjs` is the blueprint.** It already implements `propose` (write an approval row,
never touch the account) → human approves → `apply` (dry-run without `CONFIRM=1`, refuses
non-approved rows even with it). **The Meta agent copies this pattern rather than inventing one.**

---

# PART 3 — The gap (what's genuinely missing)

Eight items. Ordered by what blocks what.

| # | Gap | Severity | Detail |
|---|---|---|---|
| **G1** | **Meta Pixel + CAPI + Event Match Quality** | 🔴 **Blocker** | Andromeda needs a clean conversion signal (EMQ > 7) to read creative properly. Craftons' *Google* tracking is verified solid; **Meta-side tracking is unverified**. This is the same lesson STATUS.md already learned the hard way with CNC Cut's $2k/mo of blind spend. **Nothing else starts until this is green.** |
| **G2** | **Write paths are stubs** | 🔴 Blocker | `pauseCampaign` in `meta-ads.mjs:416` never POSTs — it prints "would POST" and returns `executed: false`. Every outward action needs building for real. |
| **G3** | **Graph API v19.0 is stale** | 🟠 High | `meta-ads.mjs:37` pins `v19.0`. Needs a current version + a documented upgrade cadence, since Meta deprecates versions on a fixed schedule. |
| **G4** | **No creative → Meta publish path** | 🟠 High | Nothing implements the `adimages` → `adcreatives` → `ads` chain. This is the actual publishing mechanism and does not exist. |
| **G5** | **No research subcommand** | 🟡 Medium | No pain-point extraction, no angle ranking. `PERPLEXITY_API_KEY` and `FIRECRAWL_API_KEY` are collected but unwired. |
| **G6** | **No cadence** | 🟡 Medium | Everything is manually invoked. No scheduler — so no "runs on a clock", so by Cody's own definition, not yet an agent. |
| **G7** | **No creative-performance memory** | 🟡 Medium | `marketing_assets.provenance` (jsonb) is the right home for Cody's "store the recipe, not the ad" idea, but nothing writes structured generation recipes into it, and nothing reads winners back out. |
| **G8** | **No entropy source** | 🟢 Low (later) | No Ad Library pull, no Virlo, no transcript mining. Doesn't bite until the loop has been running a few weeks — but it *will* bite. |

---

# PART 4 — The Craftons translation

Cody's example is a SaaS product with infinite AI-generatable creative sold to a global audience.
Craftons is CNC-manufactured building products sold to Melbourne tradies. Three things do not
transfer, and pretending otherwise would produce a bad system.

## 4.1 The product — Radius Pro only

| | |
|---|---|
| **What it is** | Design curved plywood / formply / MDF parts online; CNC-cut and dispatched in 3 business days. Large curves auto-split with **Part IDs engraved**. |
| **Landing page** | `https://craftons.com.au/products/radius-online` |
| **Core promise** | Your curve, designed online, delivered cut to your set-out. No on-site curve cutting. |
| **Primary audience** | Carpenters, formworkers, shopfitters, cabinetmakers. **High sophistication** — they know set-out, tolerances, NCC. Do not explain basics. |
| **Secondary** | Architects / specifiers — care about finish, compliance, what's buildable. |
| **Geography** | Melbourne metro (Fairfield VIC), broader by arrangement. |
| **Known-converting language** | **"bendy ply"**, **"curved bench seat"** (from `brand/keyword-plan.md` — proven in search) |

**The pain points are already documented** in `brand/audience.md` — which means **step one of Cody's
pipeline is already done, and done better than Perplexity would do it.** These came from real customer
contact, not scraped Reddit:

- Curved work on site is slow, wasteful, inconsistent — bog-and-sand, kerf-cutting, laminating sheets
- Cracks at the join
- Hard to quote
- Tight deadlines
- **What they want:** parts that turn up cut to their set-out, ready to fix; less rework; faster quotes

> **Implication:** run the Reddit/Perplexity research pass as *validation and language-mining*, not as
> discovery. We already know the pains. What we don't have is the exact phrasing tradies use when
> they're venting — and that's what makes ad copy land.

## 4.2 Doctrine conflict — AI avatar UGC is banned for Craftons

Cody's video pipeline is HeyGen AI-avatar UGC at volume. **This must not be adopted, and the reason
isn't squeamishness — it's that it would not work.**

`QUALITY-DOCTRINE.md` states: *"Render real things; constrain the AI; a human curates"*, and
*"AI never generates the product's hero geometry or exact dimensions."* `CLAUDE.md` states: *"Real
footage leads; AI extends."*

Beyond the standing rule, the audience is the problem. Tradies with high domain sophistication will
clock a synthetic spokesperson instantly, and a fake tradie talking about set-out tolerances is a
credibility hole in a product whose entire promise is *precision*. The cost of being caught is much
higher than the creative saved.

**Ruling:**

| Use | Allowed? |
|---|---|
| AI-generated backgrounds, atmosphere, b-roll, explainer illustration | ✅ Yes — per doctrine, these are "the edges" |
| AI-generated statics seeded from real Craftons photography | ✅ Yes, through `studio.mjs brand-check` |
| Rendered-from-CAD product geometry | ✅ Yes — this is the doctrine's preferred path |
| **AI avatar / synthetic person delivering a testimonial or pitch** | ❌ **No** |
| AI-generated curved parts, dimensions, or fake install photos | ❌ **No** |

## 4.3 The creative-supply problem — and the answer

**This is the hardest genuine problem in the whole build, and the video does not help with it.**

Andromeda wants 15–25 diverse creatives per ad set. Cody gets there with AI avatars and synthetic
UGC. We've just banned that. Tia supplies ~2–3 hero pieces per month (per `SETUP.md`). Naively, the
maths doesn't work.

**The answer: the configurator is the creative engine.**

Craftons has something Cody's WordPress startup doesn't — **a real interactive product that produces
infinite, genuinely different, 100% real visual output.** Every curve a person designs in Radius Pro
is a new, true, on-brand piece of creative. `content-engine/` already has the machinery: Remotion,
Playwright capture (`content-engine/capture/capture.mjs`), the brand kit (Aeonik fonts, logo, motif),
and real photography (`shop-radiuspro.png`, `shop-formwork.png`, `tradie-portrait.png`).

**Five creative families, all doctrine-compliant, all scalable without a camera:**

1. **Configurator screen-captures** — designing a specific curve, end to end. Infinite variants (different
   radii, materials, part counts). Rendered from the real UI via Playwright. *Real, not imagined.*
2. **CAD renders** — the auto-split with Part IDs engraved, exploded views. Pixel-exact from real geometry.
3. **Tia's real footage, atomised** — each hero piece cut into many hooks, as `SETUP.md` already
   requires for social.
4. **Static text-on-craft** — real macro photography (the Craft Macro shoot brief already exists) with
   pain-point copy set in Aeonik. This is where the 15–25 diversity target actually gets hit cheaply.
5. **Before/after site reality** — bog-and-sand vs. parts that arrive cut. The strongest angle available,
   and it needs real photos of both.

> **This reframes the whole build.** The agent's creative job for Craftons is not "generate images with
> AI". It is **"combinatorially assemble real assets against ranked pain points, and let Meta tell us
> which combination wins."** That is more defensible than Cody's approach, not less — and it's the
> reason the anti-slop doctrine and Andromeda's diversity requirement can both be satisfied at once.

## 4.4 Cold start

Meta ad history for Craftons appears to be **zero**. `META_ACCESS_TOKEN` and `META_AD_ACCOUNT_ID` were
collected 2026-06-15 but the account has no documented spend, and `marketing_metrics_cache` will be
empty on the Meta side.

**Implication:** the agent has no winners to learn from on day one. Phase 1 is deliberately
human-heavy — not because we don't trust the agent, but because it has nothing to read yet. The
feedback loop needs roughly 2–3 batches before its judgement is worth anything.

---

# PART 5 — Implementation

Six phases. Each ends in something that works. **Do not start a phase before the one above it is green** —
that's the standing "build deliberately, lock each piece" rule, and it matters more here than usual
because every phase feeds the next one's data.

## Phase 0 — Conversion tracking (🔴 THE GATE)

Nothing else starts until this is green. This is the lesson STATUS.md already paid for once.

- [ ] **0.1** Confirm the Meta Pixel is live on `craftons.com.au` (Shopify) and firing `Purchase` + `Lead`
- [ ] **0.2** Enable **Conversions API** alongside the pixel — Shopify has native CAPI support; both must run
- [ ] **0.3** Verify **Event Match Quality > 7** in Events Manager. Below 7, Andromeda cannot read creative properly — fix before proceeding
- [ ] **0.4** Confirm the Radius Pro conversion path end-to-end: configurator → add to cart → purchase, **and** the quote-request path
- [ ] **0.5** Decide the optimisation event — **purchase vs lead**. Open question, see §8
- [ ] **0.6** Document it all in `campaigns/meta/conversion-tracking.md`, mirroring the AdWords equivalent

**Done when:** a test purchase and a test lead both appear in Events Manager with EMQ > 7 via both pixel and CAPI.

## Phase 1 — Make the existing tool real

Turn the stub into a working read/write tool. No agent yet.

- [ ] **1.1** Bump `GRAPH_VERSION` off `v19.0` (`tools/meta-ads.mjs:37`) to current; add a note on Meta's deprecation cadence
- [ ] **1.2** Verify `META_ACCESS_TOKEN` / `META_AD_ACCOUNT_ID` are live in Vercel; run `node tools/meta-ads.mjs report` and confirm it returns real data rather than the `configured: false` sample
- [ ] **1.3** Extend `report` to pull **creative-level** fields (`creative{id,name,object_story_spec}`) — needed for the feedback loop to know *what* won, not just *which ad ID*
- [ ] **1.4** **Implement the real write** in `pauseCampaign` — replace the stub at `meta-ads.mjs:416` with an actual `POST` to `{ad_id}` setting `status=PAUSED`, keeping both existing guards (`CONFIRM=1` **and** an approved `marketing_approvals` row)
- [ ] **1.5** Add `pause-ad` (ad-level, not just campaign) — the loop kills ads, not campaigns
- [ ] **1.6** Add `set-budget` behind the same guards
- [ ] **1.7** Copy `google-ads.mjs`'s `propose` → `apply` pattern into `meta-ads.mjs` verbatim in shape

**Done when:** a real ad can be paused from the CLI, only with `CONFIRM=1` + an approved row, and it shows in `marketing_runs`.

## Phase 2 — Research + angle ranking

- [ ] **2.1** Add `meta-ads.mjs research` — Perplexity against Reddit/forums for how Australian tradies talk about curved work. **Validation and language-mining, not discovery** — we already have the pains in `brand/audience.md`
- [ ] **2.2** Rank pain points by reference frequency (Cody's second pass) — top 3 become the launch angles
- [ ] **2.3** Cross-check the output against `brand/audience.md` and `brand/keyword-plan.md`. **Conflicts favour our own data** — it came from real customers
- [ ] **2.4** Write ranked angles to `marketing_assets` (kind `angle`) so creative generation reads from one place
- [ ] **2.5** Seed the swipe file: pull competitor ads from the **Meta Ad Library** (free, public, no auth) for Australian building products

**Done when:** three ranked, evidenced Radius Pro angles exist as rows, each with the source language that supports it.

## Phase 3 — Creative assembly (the Craftons-specific part)

Per §4.3 — assembling real assets, not generating fake ones.

- [ ] **3.1** Build the **configurator capture pipeline** — Playwright drives Radius Pro through N different curve designs, records each. Extend `content-engine/capture/capture.mjs`
- [ ] **3.2** Build the **static template set** in `content-engine/` — real photography + Aeonik + pain-point copy, on brand tokens
- [ ] **3.3** Wire `studio.mjs brand-check` as a **mandatory gate** on every generated asset — this is Cody's vision-model check, already built, currently unused for ads
- [ ] **3.4** Copy comes from the **`direct-response-copy`** skill + **`craftons-voice`**, both installed. ⚠️ Per STATUS.md's own learning: **ad tone ≠ social tone.** Ads use direct CTAs; social is value-first/soft-CTA. Do not let the social voice profile leak into paid
- [ ] **3.5** **Store the recipe, not just the asset** — write the full generation spec (template ID, angle ID, copy variant, source asset, params) into `marketing_assets.provenance`. **This is the single highest-leverage step in the build** — it's what makes the feedback loop compound instead of just reporting
- [ ] **3.6** Target **15–20 diverse creatives** for the first ad set, per Andromeda's diversity floor

**Done when:** 15+ brand-checked Radius Pro creatives exist as `marketing_assets` rows, each with a complete, replayable recipe in `provenance`.

## Phase 4 — Publishing

- [ ] **4.1** Implement the Meta publish chain: **`POST /adimages`** (upload) → **`POST /adcreatives`** (build creative) → **`POST /ads`** (create, `status=PAUSED`)
- [ ] **4.2** **Always create paused.** Human flips to active in Phase 4. This is the approval gate at its most literal
- [ ] **4.3** Campaign structure per Andromeda: **one campaign, one ad set, many creatives.** Resist the instinct to segment — Meta's own test says 1×25 beats 5×5
- [ ] **4.4** Add `meta-ads.mjs publish --approval_id=<uuid>` behind the standard guards
- [ ] **4.5** Surface the whole batch in the Cockpit Run panel for one-screen approval — approving 15 ads one at a time will not survive contact with a working week

**Done when:** an approved batch of 15 creatives appears in the Meta account as paused ads, correctly structured.

## Phase 5 — The loop (this is where it becomes an agent)

- [ ] **5.1** Add `meta-ads.mjs evaluate` — read `marketing_metrics_cache` (**not** the API — Cody's rule), apply kill/keep rules
- [ ] **5.2** Kill rules, explicit and tunable. Starting point: **≥3 days live AND ≥$X spend AND zero results** → propose pause. Never kill on under-spend; never kill inside 48h
- [ ] **5.3** **Winners pool** — surviving ads compete for budget
- [ ] **5.4** **The compounding step:** join winners back to their `provenance` recipes and generate the next batch weighted toward winning *recipe patterns* — hook type, composition, angle — not winning images
- [ ] **5.5** **Cadence** via Vercel Cron. Start weekly, not daily. Cody runs 10 ads/day for clients with real budget; Craftons at Melbourne-metro scale needs a slower clock or it'll burn budget on noise
- [ ] **5.6** Every cycle proposes; a human approves. Autonomy is Phase 6

**Done when:** a scheduled run reads real performance, proposes kills and a next batch, and files them as approval rows without being asked.

## Phase 6 — Entropy + earned autonomy

- [ ] **6.1** **Meta Ad Library** puller — competitor creative as fresh DNA (free, no auth)
- [ ] **6.2** **Virlo API** (`virlo.ai`) — trending short-form formats, if the category justifies the cost
- [ ] **6.3** Trade YouTube/podcast transcript mining for angles
- [ ] **6.4** **Novelty check** — flag when N consecutive batches are too similar. Cody's warning is that decay is invisible day to day; make it visible
- [ ] **6.5** Begin the autonomy ladder (§6)

---

# PART 6 — The autonomy ladder

Lee's decision: *"We approve at the start. Eventually the agent runs autonomously."* This is the
graduation path. **Each rung requires the one below it to have run clean for the stated period.**

| Rung | Agent may do unattended | Still needs approval | Graduation criteria |
|---|---|---|---|
| **0 — Now** | Nothing. Reports and proposes only | Everything | — |
| **1** | Pause ads meeting an explicit, pre-agreed kill rule | All spend increases, all new creative | 4 weeks at Rung 0, zero bad kill proposals |
| **2** | Rung 1 + shift budget **between existing approved ads** within a fixed total | New creative, total budget changes | 4 weeks at Rung 1, positive trend |
| **3** | Rung 2 + publish new creative **from already-approved templates and angles** | New angles, new templates, budget increases | 8 weeks at Rung 2, brand-check pass rate > 95% |
| **4** | Full loop within a hard monthly spend ceiling | Ceiling changes, new product lines | Sustained performance + Lee's explicit call |

**Implementation:** this is a policy table, not new code. `marketing_approvals` already exists; the
ladder is a config listing which `action` values require a row at the current rung. Store the rung in
config, not in code, so it can be lowered instantly if something goes wrong.

**Non-negotiable at every rung:**
- Hard monthly spend ceiling, enforced in code, checked before every write
- Kill switch — one setting that returns everything to Rung 0
- Every autonomous action still writes a `marketing_runs` row
- **`brand-check` never becomes optional**

---

# PART 7 — Tools, keys and costs

## Already in place — nothing to do

| Tool | Status |
|---|---|
| Neon Postgres (`DATABASE_URL`) | ✅ Live, tables exist |
| Vercel hosting + cron capability | ✅ Live |
| `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID` | ✅ Collected 2026-06-15 — **verify they still work** |
| `ANTHROPIC_API_KEY` | ✅ In base app |
| `REPLICATE_API_TOKEN`, `GLIF_API_TOKEN` | ✅ Collected, wired in `studio.mjs` |
| `PERPLEXITY_API_KEY`, `FIRECRAWL_API_KEY` | ✅ Collected — **not yet wired** |
| Shopify connector | ✅ Live |

## Needed

| Tool | Why | Cost | Priority |
|---|---|---|---|
| **`META_APP_ID` + `META_APP_SECRET`** | Required for the publish chain; long-lived token refresh | Free | 🔴 Phase 1 |
| **Meta Marketing API access level** | Dev tier = 60 quota points / 300s. Standard = 9,000, needs App Review | Free, but App Review has lead time — **start early** | 🔴 Phase 1 |
| **Meta Pixel + CAPI on Shopify** | Phase 0 gate | Free | 🔴 Phase 0 |

## Explicitly NOT needed (and why)

| Cody uses | We don't | Because |
|---|---|---|
| **Airbyte** | ❌ | 3 sources, all with direct APIs. `cacheMetric()` already does this |
| **ClickHouse** | ❌ | Neon Postgres is live and adequate at this volume. Revisit only if the data outgrows it |
| **Heroku / Railway** | ❌ | Vercel is already the deploy target |
| **HeyGen** | ❌ | AI avatars banned for Craftons (§4.2) |
| **Seedance** | ⏸ | Possible later for b-roll only, never for product geometry |
| **Kie.ai** | ⏸ | Replicate + Glif already wired. Only if we need a model neither has |
| **Virlo** | ⏸ | Phase 6 entropy. Real value, but not before there's a loop to un-stick |

> **The "invest in integrations now" rule cuts both ways.** It means paying setup costs once for
> things that recur — not adopting a tool because it appeared in a video. Airbyte and ClickHouse are
> correct for an agency with 30 clients and 12 sources each. For one brand and three sources they are
> weeks of ops work for no gain.

---

# PART 8 — Guardrails

**From Cody, verified:**
- **Writes only through the Marketing API.** Publish, pause, promote. Never bulk-read — that's what
  gets accounts banned, and it's a TOS violation, not an anti-agent policy
- **Reporting comes from the cache**, never from hammering insights endpoints
- Respect Business Use Case rate limits; exponential backoff on 429 (`_lib.mjs fetchJson` already does)
- Use async jobs for heavy breakdowns — capped at 10/day/account

**From Craftons' own doctrine:**
- Nothing publishes active. Ads are created `PAUSED`
- `brand-check` gates every asset, always
- Real leads, AI extends. Never AI-generate product geometry or dimensions
- Hard spend ceiling in code, checked before every write
- Australian/British spelling in all copy ("Optimise", "Centre")
- Ad tone ≠ social tone

**New, specific to this build:**
- **Never kill an ad inside 48 hours** — Cody's own window is 2–3 days for initial signal
- **Never kill on insufficient spend** — no data is not the same as bad data
- **Log every autonomous decision with its reasoning**, so a bad rule can be traced and reverted
- **Watch for entropy from week one.** Do not wait for performance to decay to notice convergence

---

# PART 9 — Open questions

Blocking Phase 0:

1. **Optimisation event — purchase or lead?** Radius Pro can be bought online *and* quote-requested.
   Andromeda optimises hard toward whichever it's told. Craftons' Google data shows 23 purchases vs
   443 lead forms — which suggests lead volume dwarfs purchase volume, and that the right answer may
   be *lead*, at least initially. Needs a call.
2. **Monthly Meta budget ceiling?** Not answered. Needed before any write path goes live, because the
   ceiling is enforced in code. For reference, CNC Cut historically ran ~$2k/mo on Google.
3. **Is the Meta ad account clean?** Zero history assumed. If there's prior spend or a policy strike,
   that changes the cold-start plan.

Blocking Phase 3:

4. **Do we have real before/after site photography?** §4.3 calls this the strongest available angle,
   and it's the one thing on the list that genuinely cannot be assembled from existing assets.
5. **Confirm Tia's footage rights** for paid use, if any of it goes into ads.

Not blocking, decide later:

6. **Does the Cockpit need a Meta-specific approval UI**, or does the existing Run panel carry it?
   Approving 15 creatives one at a time will not survive a real week (§4.5 flags this).
7. **When does CNC Cut get the same treatment?** Architecture should stay multi-account-capable even
   though we're building Craftons-only, so this isn't a rewrite later.

---

## Appendix A — Where each idea comes from

| § | Transcript timestamp | Topic |
|---|---|---|
| 1.1 | 01:54–04:00 | Defining a marketing agent |
| 1.2 | 09:55–12:48 | Andromeda; creative as targeting |
| 1.4 | 13:00–15:23 | Perplexity → Reddit research; ranking pain points |
| 1.4 | 15:23–17:25 | Static + video creative pipelines |
| 1.3 | 17:25–24:11 | Data pipeline, warehouse, the whiteboard diagram |
| 1.3 | 17:52–18:31 | **API for writes only** — the ban warning |
| 1.5 | 24:11–25:51 | Ad strategy; 2 ad sets × 5 ads/day; winners pool |
| 1.5 | 25:20–25:50 | **Store the JSON prompts, not the ads** |
| 1.6 | 25:51–28:01 | Entropy and its three fixes |
| 1.2 | 28:01–34:26 | Let the market pick the winner; test many angles |

Sections 04:00–09:55 (the WordPress startup pitch) and 34:26–end (channel feedback) contain nothing
applicable to Craftons.

## Appendix B — Key file references

**In `leepatt/cnccut-app`:**
- `tools/meta-ads.mjs` — the tool to extend. Stub write at :416, `GRAPH_VERSION` at :37
- `tools/google-ads.mjs` — **the pattern to copy** (`propose` → approve → `apply`)
- `tools/studio.mjs` — `generate` at :221, `brand-check` at :386
- `tools/_lib.mjs` — `fetchJson`, `startRun`/`finishRun`, `cacheMetric`
- `drizzle/marketing/0001_marketing_cockpit.sql` — the four tables
- `docs/marketing/APP-NOTES.md` — env var names (**match these, do not invent**)
- `lib/marketing/modules.ts` — Cockpit module registry
- `content-engine/` — Remotion, Playwright capture, brand kit, real photography

**In `leepatt/marketing` (this repo):**
- `QUALITY-DOCTRINE.md` — the anti-slop rules; the source of the AI-avatar ban
- `brand/audience.md` — pain points, already documented from real customers
- `brand/keyword-plan.md` — proven converting language
- `campaigns/adwords/` — the equivalent Google build, worth mirroring in structure
- `campaigns/adwords/conversion-tracking.md` — the template for Phase 0's deliverable
