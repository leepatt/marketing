# The Meta Ads Agent — Bible

_The reference doc for standing up an autonomous Meta ads agent for **Craftons**, starting with
**Radius Pro**. Digested from the Greg Isenberg × Cody Schneider episode, then translated to what
Craftons actually has, actually sells, and actually needs._

**Created:** 2026-08-03 · **Branch:** `claude/marketing-agents-setup-qamq2f`
**Status:** design locked · **Phases 1, 2, 4 and 5 BUILT** in `leepatt/cnccut-app` on the same branch —
`tools/_meta-policy.mjs`, a rewritten `tools/meta-ads.mjs` (`report` · `doctor` · `evaluate` ·
`winners` · `research` · `check-batch` · `upload-image` · `create-creative` · `propose` · `apply`),
and a weekly cron at `app/api/cron/meta-ads`. Verified against the live account 2026-08-03: 13/13
guardrail self-checks pass, `tsc --noEmit` clean, `report`/`winners`/`research` all return real data.
**Phase 0 (tracking) is the remaining gate; Phase 3 (creative production) is the remaining work.**
**Scope decisions (Lee, 2026-08-03):** Craftons only · human-approves first, autonomy earned ·
code lives in `leepatt/cnccut-app` · lightweight data layer first · **Radius Pro only** to start ·
**AI avatars approved** (§4.2) · **$2,000/month ceiling** with a staged ramp (§4.6) ·
**optimise on combined high-intent Lead, score on sales** (§4.6).

> **Read `STATUS.md` first, then this.** This doc is the *what and why*. The build steps in Part 5
> are the *how*, with the built items ticked.

---

# 🔒 LAW 1 — NO AD GOES LIVE WITHOUT LEE'S EXPLICIT APPROVAL

**Lee, 2026-08-05: _"No ads should go live without my permission."_**
**Amended by Lee, 2026-08-13: _"Change bible so I can approve the ads to go live through Claude."_**

This outranks every other rule in this document.

**What the amendment changed: the mechanism, not the substance.** Lee's approval is still required for
every single ad that goes live. What changed is *where he gives it* — he can now approve a proposal and
have Claude apply it, instead of having to toggle in Ads Manager himself.

**What did NOT change, and must never change:** the agent cannot put an ad live on its own initiative,
at any autonomy rung, ever. Activation requires an explicit, named human approval every time.

### The three activation types

`activate_campaign` · `activate_ad_set` · `activate_ad`

All three are in **`ALWAYS_REQUIRES_APPROVAL`** — at *every* rung, including rung 4. They are the only
mutations in the tool that can start money moving, so they carry more checks than anything else.

### What enforces it — verified in code 2026-08-13, not assumed

| Layer | Mechanism | Where |
|---|---|---|
| **Activation always needs a human** | All three types in `ALWAYS_REQUIRES_APPROVAL`, asserted at rung 4 by a self-check | `_meta-policy.mjs` |
| **Two independent things required** | `CONFIRM=1` **and** an `approved` row. Proven live: `CONFIRM=1` against a pending activation returns *"Refusing to proceed"* | `meta-ads.mjs` |
| **A named human approver** | `--approver` is required; `claude`/`agent`/`internal`/`bot`/`auto` are rejected | `meta-ads.mjs` |
| 🆕 **Live preflight at execution** | Before going live, re-reads the account: AU-only targeting, the $100/day cap, and the $2,000 monthly ceiling. An approval that sat in the queue while the world changed is refused | `meta-ads.mjs` |
| **Ads are still created PAUSED** | `publish_ad` hard-codes `status: "PAUSED"`. Creating and activating are separate, separately-approved steps | `meta-ads.mjs` |
| **Nothing else can set ACTIVE** | Self-check asserts `pause_ad`, `set_budget`, `publish_ad`, `create_ad_set` can never produce `status: "ACTIVE"` | `meta-ads.mjs` |
| **The weekly cron cannot spend** | Runs `report` then `evaluate --file_proposals`. It files proposals; it never applies them | `app/api/cron/meta-ads` |
| **Rung 0 permits nothing unattended** | Self-check passes | `_meta-policy.mjs` |

**The practical guarantee is unchanged: no Craftons ad goes live unless Lee said yes to that specific
ad.** The worst the agent can do unattended is leave a proposal waiting.

### Rules for anyone extending this agent

1. **Never remove an activation type from `ALWAYS_REQUIRES_APPROVAL`.** That single line is what stands
   between "Lee approves each launch" and "the agent can start spending on its own".
2. **Never grant an autonomy rung the ability to activate.** The ladder governs pausing, budget
   shifting and paused-publishing. It stops there. Rung 4 is *not* an exception.
3. **Never remove `status: "PAUSED"` from `publish_ad`,** and never make it a caller-supplied argument.
   Creating an ad and switching it on stay two separate approvals.
4. **Never weaken the activation preflight.** It exists because an approved proposal can sit in the
   queue for days; the AU rule and the spend caps must be true *at the moment of going live*, not when
   the proposal was written.
5. **Never let `--approver` accept a non-person.** An approval table whose approver reads "agent" is
   not an audit trail, and the whole amendment rests on that trail being real.
6. **If a guardrail self-check for this law fails, stop and fix it before anything else.** A failing
   check here is not a flaky test.
7. **Unpausing is not "resuming".** Re-enabling a previously approved ad that has since been paused is
   a fresh activation and needs a fresh approval — circumstances change while an ad is off.

> **Related standing rule — 🇦🇺 Australia only (Lee, 2026-08-05).** Craftons manufactures in Fairfield
> and ships Australia-wide via FedEx. There is no offer for anyone overseas. Enforced by
> `ALLOWED_COUNTRIES` + `checkTargeting()` in `_meta-policy.mjs`, asserted by five `doctor` self-checks,
> and audited live by `report` on every run. **An ad set with no geo set at all is a failure too** — it
> runs worldwide rather than erroring, which is how the account ended up with three of them.

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

## 4.2 AI avatars — APPROVED, with one hard line

**Decision (Lee, 2026-08-03): AI avatar UGC is approved for Meta ads.** The operational reason is
sound — real footage is pending, and the agent needs creative volume now to hit Andromeda's diversity
floor. Waiting on Tia's supply would mean not running ads for months.

This is a deliberate, scoped exception to *"Real footage leads; AI extends"*, not a repeal of it.
When real content lands, it leads; avatars fill the gap until then and remain as one creative family
among several.

**Ruling:**

| Use | Allowed? |
|---|---|
| **AI avatar as presenter/narrator** — explaining Radius Pro, walking through the problem, reading a pain point | ✅ **Yes** |
| AI-generated backgrounds, atmosphere, b-roll, explainer illustration | ✅ Yes |
| AI-generated statics seeded from real Craftons photography | ✅ Yes, through `studio.mjs brand-check` |
| Rendered-from-CAD product geometry | ✅ Yes — the doctrine's preferred path |
| **AI avatar delivering a first-person testimonial** — "I used this on my job last week", "this saved me two days" | ❌ **No — see below** |
| AI-generated curved parts, dimensions, or fake install photos | ❌ No — still banned, this is the geometry rule |

### The one hard line: presenter ≠ testimonial

This is a legal constraint, not a taste preference, so it survives the approval above.

A synthetic person **presenting** information is ordinary advertising — the same as a voiceover or a
hired actor, and universally accepted. A synthetic person giving a **first-person testimonial about
their own experience** with the product is a fabricated endorsement. Under **Australian Consumer Law**
(ACL s18 and s29(1)(e), misleading or deceptive conduct and false testimonials), a testimonial from a
person who does not exist and did not use the product is a straightforward breach — and the ACCC has
pursued exactly this. Meta's own advertising policies prohibit it as well.

**The practical test:** would the ad still be true if a caption read *"presenter is AI-generated"*?
- *"Curved plywood, cut to your set-out, dispatched in three days"* → true regardless of who says it. ✅
- *"I'm a chippie from Preston and this saved me two days on site"* → false the moment the speaker isn't real. ❌

Write avatar scripts in **second person about the product**, never first person about experience.
This costs nothing in performance — the pain-point angles from §4.1 are all phrased as *"stop
bog-and-sanding curves on site"*, which is presenter copy already.

**Encode this in `studio.mjs brand-check`** as an automated gate: flag any avatar script containing
first-person experience claims. That turns a policy into something the agent enforces on itself.

## 4.3 The creative-supply problem — and the answer

Andromeda wants 15–25 diverse creatives per ad set. Tia supplies ~2–3 hero pieces per month (per
`SETUP.md`), and real content is still pending. AI avatars (§4.2) close part of that gap, but they
should not be the *only* answer — an ad set of 20 talking heads is not creative diversity, it's one
creative twenty times, and Andromeda reads it that way.

**The other half of the answer: the configurator is the creative engine.**

Craftons has something Cody's WordPress startup doesn't — **a real interactive product that produces
infinite, genuinely different, 100% real visual output.** Every curve a person designs in Radius Pro
is a new, true, on-brand piece of creative. `content-engine/` already has the machinery: Remotion,
Playwright capture (`content-engine/capture/capture.mjs`), the brand kit (Aeonik fonts, logo, motif),
and real photography (`shop-radiuspro.png`, `shop-formwork.png`, `tradie-portrait.png`).

**Six creative families. Target roughly the mix below for the launch ad set of 15–20:**

| # | Family | Launch share | Notes |
|---|---|---|---|
| 1 | **Configurator screen-captures** — designing a specific curve end to end. Infinite variants (radii, materials, part counts). Driven through the real UI by Playwright | ~5 ads | *Real, not imagined.* The highest-leverage family — it scales without a camera and shows the product working |
| 2 | **AI avatar presenter** — reading a ranked pain point, second person, never first-person testimonial (§4.2) | ~4 ads | Fills the volume gap while real footage is pending |
| 3 | **Static text-on-craft** — real macro photography + pain-point copy in Aeonik | ~4 ads | Cheapest diversity. Craft Macro shoot brief already exists |
| 4 | **CAD renders** — auto-split with Part IDs engraved, exploded views | ~3 ads | Pixel-exact from real geometry |
| 5 | **Tia's real footage, atomised** | as it lands | Each hero piece cut into many hooks, per `SETUP.md`. **Takes over the top slots when it arrives** |
| 6 | **Before/after site reality** — bog-and-sand vs. parts that arrive cut | blocked | Likely the strongest angle available, and the one thing that genuinely cannot be assembled from existing assets. Needs real photos of both states |

> **This reframes the agent's creative job.** It is not "generate images with AI". It is
> **"combinatorially assemble assets against ranked pain points, and let Meta tell us which
> combination wins."** Diversity comes from spanning families, not from generating twenty variations
> inside one. **A batch drawn from a single family should fail the brand-check gate** — that's the
> cheapest possible defence against the entropy problem in §1.6, applied from day one instead of month three.

## 4.4 The business, in real numbers

Pulled live from Shopify 2026-08-03. **These numbers drive the optimisation-event decision in §4.6 —
they are the "learn from last campaign" evidence.**

**Radius Pro, trailing 365 days:**

| Metric | Value |
|---|---|
| Orders | **202** |
| Gross sales | **$124,164** |
| **AOV** | **$614.67** |
| Rate | ~17 orders/month · ~4/week |

Radius Pro is **60% of all Craftons orders** and the clear right choice to start with.

**Whole store, monthly trend — the business is compounding:**

| Month | Orders | Gross |
|---|---|---|
| Aug 2025 | 7 | $2,186 |
| Jan 2026 | 21 | $10,204 |
| Apr 2026 | 20 | $16,187 |
| May 2026 | 33 | $21,823 |
| Jun 2026 | 34 | $36,363 |
| **Jul 2026** | **39** | **$41,560** |

~35 orders/month and ~$33k/month at current run rate — roughly **5× order growth YoY**. Ads are being
added to something already working, which is the right time to do it.

**Funnel, trailing 90 days:** 22,626 sessions → 216 cart adds → 131 reached checkout → 100 purchases.
**Site conversion rate 0.44%** — normal for a considered, custom-manufactured B2B purchase.

**Attribution, trailing 365 days:**

| Source | Orders | Gross |
|---|---|---|
| Direct / unattributed | 99 | $107,053 |
| `craftons` (direct) | 41 | $40,064 |
| **Curves calculator** (configurator, all deploys) | **~54** | **~$26,800** |
| `search / google` | 37 | $18,612 |
| `social / instagram` | 6 | $7,907 |
| `search / bing` | 6 | $4,164 |
| **`social / facebook`** | **3** | **$729** |

**Two things fall out of this table:**

1. **Instagram already converts organically** — 6 orders at ~$1,318 AOV, *more than double the site
   average*. The Meta audience is not hypothetical.
2. **The configurator is the top attributable path** (~54 orders). It converts. That's independent
   evidence for making it the creative engine in §4.3 — we're advertising the thing that already works.

> ⚠️ **Do NOT read Meta performance off this table.** It shows `social/facebook` at 3 orders / $729
> all time, which suggested a cold start. **That is wrong** — see §4.5. Shopify's last-click referrer
> attribution undercounts Meta by more than an order of magnitude (iOS restrictions, view-through,
> dark social). The Meta account itself reports **$17,285 of tracked revenue in the last 30 days
> alone.** Always read Meta performance from Meta.

## 4.5 The existing Meta account — and what the last campaign taught us

Pulled live from the Meta Marketing API on 2026-08-03, via the tool built this session.
**This is the "learn from last campaign" evidence, and it is the most useful data in this document.**

**Account `act_1650412872259063` is live, instrumented and has real history — not a cold start.**

| Last 30 days | |
|---|---|
| Spend | **$1,977.82** |
| Results | **21** |
| Revenue | **$17,285** |
| **ROAS** | **~8.7×** |
| Cost per result | **$94.18** |
| CTR / CPC | 8.35% / $0.09 |

**An 8.7× ROAS is a good account.** The strategic question is not "does Meta work for Craftons" —
it demonstrably does. It's "why did it stop working when it scaled", and the daily data answers that
precisely.

### The scaling failure, day by day

| Date | Spend | Clicks | Results |
|---|---|---|---|
| 17 Jul | $13.46 | 18 | 1 |
| 20 Jul | $14.43 | 23 | 1 |
| 21 Jul | $15.34 | 15 | **3** |
| 22 Jul | $86.12 | 784 | 2 |
| 23 Jul | $117.60 | 1,021 | 1 |
| 24 Jul | $146.02 | 2,244 | **0** |
| 25 Jul | $121.58 | 1,910 | **0** |
| 26 Jul | $149.70 | 2,468 | **0** |
| 27 Jul | $167.21 | 2,757 | **0** |
| 28 Jul | $201.01 | 2,476 | **0** |

**Spend went up ~13×. Clicks went up ~150×. Results went to zero.**

An **8.35% CTR at a $0.09 CPC with no conversions** is the unmistakable signature of cheap junk
traffic. The account bought an enormous amount of the least valuable attention available.

### Why it happened — three causes, all fixable

1. **The ad set optimised for `AddToCart`** (`TOF | Broad AU | AddToCart`). That is an upper-funnel
   event, and optimising there teaches Meta to find people who browse cheaply, not people who buy.
   **This is direct account evidence for the optimisation-event decision in §4.6** — we no longer have
   to reason from first principles, it was tried here and it failed exactly this way.
2. **Creative was segmented by trade** — separate ads for Landscapers, Concreters, Carpenters,
   Builders, Chippies. That is pre-Andromeda interest-thinking. Under Andromeda the creative *is* the
   targeting; hand-segmenting by trade fragments signal for no benefit.
3. **The budget was scaled ~13× in a single step.** Meta resets learning on large budget jumps. This
   is exactly what `MAX_BUDGET_INCREASE_FRACTION` (20%) in `tools/_meta-policy.mjs` now prevents.

### What actually produced the results

| Campaign | Spend (30d) | Results |
|---|---|---|
| **Retargeting — Bottom of Funnel** | ~$657 | **19 of 21** |
| TOF prospecting (all trade-segmented ads) | ~$1,300 | **~2** |

**Retargeting is carrying the entire account.** Top-of-funnel prospecting spent roughly twice as much
for a tenth of the outcome.

> **This does not mean "only run retargeting."** A retargeting pool needs new people entering it, and
> starved of TOF it decays. It means the TOF *approach* was wrong — wrong optimisation event, wrong
> segmentation, wrong ramp — not that TOF is wrong.

### Cost per result, ad by ad — and the best number in the account

From `node tools/meta-ads.mjs winners`, run against the live account:

| Ad | Spend | Results | **Cost/result** |
|---|---|---|---|
| **Retargeting — Configurator Hero Ad D** | $12.10 | 2 | **$6.05** |
| Retargeting — BOF Ad | $409.91 | 16 | $25.62 |
| AD4 Builders — curved wall frame | $144.29 | 1 | $144.29 |
| Retargeting — Radius Pro boss video | $234.71 | 1 | $234.71 |
| **AD5 Chippies — curved wall frame** | **$758.74** | 1 | **$758.74** |
| AD2 Landscapers — Ardreagh carousel | $183.24 | 0 | — |
| AD1 Concreters — Ardreagh carousel | $110.43 | 0 | — |
| AD6 Carpenters — curved wall frame | $76.81 | 0 | — |

**The configurator ad converts at $6.05 per result. The trade-segmented TOF ad converts at $758.74 —
125× worse.** It also beats break-even CAC (~$277) by a factor of 45, while AD5 Chippies misses it by
almost 3×.

> **This is independent evidence for §4.3.** The recommendation to make the configurator the creative
> engine was reasoned from the fact that it converts on-site. The account says it is *also already the
> single most efficient ad Craftons has ever run on Meta* — on $12 of spend, admittedly, so treat the
> precision with care. But the direction is unambiguous, and it is the cheapest possible thing to test
> next.

**Also note what is absent:** all 10 ads show `unrecorded` for their recipe, because they were built
by hand in Ads Manager. The loop cannot learn from them beyond the aggregate. Everything published
through `create-creative` from here carries its recipe, and `winners` will aggregate by creative
family instead of returning one undifferentiated row.

**Current state:** everything is paused (0 live ad sets), $248.26 spent month-to-date. The account is
dark, which makes this a clean moment to restart properly.

## 4.6 Optimisation event — the decision

> **Lee's brief:** *"You tell me. At the end of the day we want and need sales."*

**Ruling: optimise for a combined high-intent Lead event (quote request + configurator submission),
NOT Purchase — while measuring the scoreboard exclusively in sales.**

> ### 🔄 REFINED 2026-08-03 — the specific events are now known
>
> The ruling below stands; the arithmetic that produced it was right. But it was written before I read
> the configurator's tracking code, and the concrete answer is better than the plan.
>
> **There is no need to build a `QuoteRequested` event — `InitiateCheckout` already is it.** The
> configurator fires it on handoff to the Shopify cart, with the real cart total, only after parts
> have been configured. Measured volumes:
>
> | Candidate | Per week | vs ~50/wk threshold |
> |---|---|---|
> | Purchase (real, 36/mo) | ~8 | ❌ 6× short |
> | **InitiateCheckout** (193/mo) | **~45** | ✅ at threshold |
> | **InitiateCheckout + Purchase** | **~53** | ✅ **clears it** |
> | AddToCart (920/mo) | ~215 | ❌ fires per part; the July failure |
> | ConfiguratorStarted (812/mo) | ~190 | ❌ top of funnel |
>
> **Final: optimise on a custom conversion of `InitiateCheckout` OR `Purchase` (~53/week).** This is
> the first configuration that genuinely clears Meta's learning threshold at $2k/month, which the
> original analysis concluded nothing would. Nothing needs building — only the custom conversion.
>
> Caveat: a buyer fires both events, so "results" is not a clean headcount. That's a stronger
> optimisation signal, not a corrupted one — but **read revenue, not result count, as the scoreboard.**
> Setup steps → `campaigns/meta/conversion-tracking.md` §Step 4–5.

That looks like a contradiction. It isn't, and here's the arithmetic that forces it.

### Why not Purchase

Meta's learning phase needs roughly **50 optimisation events per ad set per week** to exit. Below
that, an ad set sits in *Learning Limited*: delivery gets erratic, CPMs rise, and — critically under
Andromeda — **the algorithm has too little conversion signal to correlate against creative**, which is
the entire mechanism we're relying on.

Now the volumes, at $2,000/month = **~$65/day**:

| Candidate event | Actual volume | Per week | vs 50/wk threshold |
|---|---|---|---|
| **Purchase** (Radius Pro) | ~17/mo | **~4** | ❌ **12× short** |
| Purchase (whole store) | ~35/mo | ~8 | ❌ 6× short |
| Reached checkout | ~44/mo | ~10 | ❌ 5× short |
| Add to cart | ~72/mo | ~17 | ❌ 3× short |
| **Lead forms** (Google-tracked) | 443 tracked | ~8–34 | ⚠️ Closest available |

**The finding that matters more than the purchase-vs-lead question: at this budget and this AOV,
*nothing* in this business reaches 50 events/week.** Anyone promising otherwise hasn't done the
arithmetic. So the job is not "pick the perfect event" — it's **maximise signal density and stop
diluting it.**

Purchase optimisation at ~4 events/week would leave the ad set permanently learning-limited, spending
$65/day while telling Andromeda almost nothing. That is how you burn $2k/month and conclude "Meta
doesn't work for us."

### The design that makes it work anyway

1. **ONE campaign, ONE ad set. Never split.** Every event concentrates in a single learning entity.
   This happens to be exactly what Andromeda wants anyway (1 ad set × 25 creatives beat 5 × 5).
   Here it's not an optimisation — it's survival. **Splitting the ad set is the single fastest way to
   kill this account.**
2. **Combine events into one custom conversion.** Count quote request **and** configurator submission
   **and** purchase as the same optimisation event. Maximum density from the same traffic.
3. **High-intent leads only.** The event is a *configured quote request* — someone who has specified a
   curve. **Not** a generic contact form. This is what keeps "lead" tethered to "sale" and stops the
   agent optimising toward tyre-kickers.
4. **Send Purchase with real `value` via CAPI from day one**, even though we don't optimise on it.
   This builds the history so switching to Purchase/Value optimisation later is a step change, not a
   cold start.
5. **Score on revenue, never on cost-per-lead.** Track lead → sale close rate so CPL converts to true
   CAC. Cost-per-lead is the dial we turn; **revenue is the only number that judges it.**

### Graduation to Purchase optimisation

Switch when Meta-attributed purchases sustain **~30+/month for two consecutive months**. At that point
the signal supports it and value-based optimisation becomes the better setting. Until then, switching
early is the classic way to stall an account.

### The CAC maths — what "working" means

| | |
|---|---|
| Radius Pro AOV | **$614.67** |
| **Gross margin — MEASURED 52.4%** (Xero, Feb–Jul 2026) | **~$322/order** |
| **Break-even CAC** | **~$322** |
| Break-even volume at $2k/mo | **~6.2 orders/month** |
| Healthy target (3× ROAS) | ~10–12 orders/month at **CAC < $180** |

**Ten extra Radius Pro orders per month would lift it from ~17 to ~27 — a ~60% increase on the
product line.** Ambitious, not fantasy, for a business already growing 5× YoY.

**Kill criteria, agreed up front:** if after 6 full weeks at full budget CAC is above ~$322
(break-even) with no improving trend, stop and reassess. Deciding this now is what prevents the sunk-cost
argument later.

## 4.7 Budget and ramp

**$2,000/month ceiling, enforced in code before every write. Start small, ramp on evidence.**

| Stage | Daily | Monthly pace | Gate to advance |
|---|---|---|---|
| **1. Validation** (wk 1–2) | **$35/day** | ~$1,050 | Tracking fires correctly, EMQ > 7, no policy rejections, creative approved |
| **2. Signal** (wk 3–6) | **$65/day** | ~$2,000 | Ad set out of erratic delivery; CPL established; at least one clear winner |
| **3. Sustain** (wk 7+) | **$65/day** | $2,000 | Hold. This is the ceiling |
| **4. Ramp** | above $65/day | — | **Only** on sustained CAC < $180 **and** Lee's explicit approval. Raise ≤20% at a time — bigger jumps reset learning |

**Do not spread $2k across multiple ad sets to "test more".** At this volume that guarantees every ad
set starves. Budget concentration *is* the test.

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
- [ ] **0.5** **Build the combined custom conversion** (§4.5): configured quote request **+** configurator submission **+** purchase, as one optimisation event. High-intent only — a generic contact form must not qualify
- [ ] **0.6** **Send `Purchase` with real `value` (AUD) via CAPI from day one**, even though we optimise on the combined event — this builds the history for the later switch to value optimisation
- [ ] **0.7** Instrument **lead → sale close rate** so cost-per-lead can be converted to true CAC. Without this the scoreboard is a vanity metric
- [x] **0.8** ✅ **Written → `campaigns/meta/conversion-tracking.md`** — full step-by-step, grounded in live pixel recon

**Done when:** a test purchase and a test quote request both appear in Events Manager with **EMQ > 7** via both pixel and CAPI, and purchase events carry a value.

> 🔴 **Recon 2026-08-03 found the tracking is NOT clean, and one problem is serious.**
> The pixel (`677437638374055`, "Craftons Web") is healthy and firing the full funnel — including an
> existing `ConfiguratorStarted` custom event — **but it recorded 97 Purchases in 30 days against
> Shopify's 36 actual orders. The conversion signal is inflated ~2.7×.**
> Andromeda correlates creative against conversion signal, so roughly two of every three conversions
> it learned from never happened. **This is a plausible contributor to the July collapse in §4.5.**
> Also found: Advanced Matching is **off** (caps EMQ), **zero** custom conversions exist (so the
> combined high-intent event doesn't yet), and traffic is **72% iPhone** (making CAPI critical).
> Full diagnosis and the fix sequence → `campaigns/meta/conversion-tracking.md`.

## Phase 1 — Make the existing tool real

Turn the stub into a working read/write tool. No agent yet.

- [x] **1.1** ✅ Bump `GRAPH_VERSION` off `v19.0` (`tools/meta-ads.mjs:37`) to current; add a note on Meta's deprecation cadence
- [x] **1.2** ✅ Verify `META_ACCESS_TOKEN` / `META_AD_ACCOUNT_ID` are live in Vercel; run `node tools/meta-ads.mjs report` and confirm it returns real data rather than the `configured: false` sample
- [x] **1.3** ✅ Extend `report` to pull **creative-level** fields (`creative{id,name,object_story_spec}`) — needed for the feedback loop to know *what* won, not just *which ad ID*
- [x] **1.4** ✅ **Implement the real write** in `pauseCampaign` — replace the stub at `meta-ads.mjs:416` with an actual `POST` to `{ad_id}` setting `status=PAUSED`, keeping both existing guards (`CONFIRM=1` **and** an approved `marketing_approvals` row)
- [x] **1.5** ✅ Add `pause-ad` (ad-level, not just campaign) — the loop kills ads, not campaigns
- [x] **1.6** ✅ Add `set-budget` behind the same guards
- [x] **1.7** ✅ Copy `google-ads.mjs`'s `propose` → `apply` pattern into `meta-ads.mjs` verbatim in shape

**Done when:** a real ad can be paused from the CLI, only with `CONFIRM=1` + an approved row, and it shows in `marketing_runs`.

## Phase 2 — Research + angle ranking

- [x] **2.1** ✅ Add `meta-ads.mjs research` — Perplexity against Reddit/forums for how Australian tradies talk about curved work. **Validation and language-mining, not discovery** — we already have the pains in `brand/audience.md`
- [ ] **2.2** Rank pain points by reference frequency (Cody's second pass) — top 3 become the launch angles
- [x] **2.3** ✅ Encoded in the tool's own output footer. Cross-check against `brand/audience.md` and `brand/keyword-plan.md`. **Conflicts favour our own data** — it came from real customers
- [x] **2.4** ✅ Write ranked angles to `marketing_assets` (kind `angle`) so creative generation reads from one place
- [ ] **2.5** Seed the swipe file: pull competitor ads from the **Meta Ad Library** (free, public, no auth) for Australian building products

**Done when:** three ranked, evidenced Radius Pro angles exist as rows, each with the source language that supports it.

## Phase 3 — Creative assembly (the Craftons-specific part)

Per §4.3 — assembling real assets, not generating fake ones.

- [ ] **3.1** Build the **configurator capture pipeline** — Playwright drives Radius Pro through N different curve designs, records each. Extend `content-engine/capture/capture.mjs`
- [ ] **3.2** Build the **static template set** in `content-engine/` — real photography + Aeonik + pain-point copy, on brand tokens
- [x] **3.3** ✅ (partial) Batch gate built as `meta-ads.mjs check-batch`; wire `studio.mjs brand-check` as a **mandatory gate** on every generated asset — this is Cody's vision-model check, already built, currently unused for ads
- [ ] **3.4** Copy comes from the **`direct-response-copy`** skill + **`craftons-voice`**, both installed. ⚠️ Per STATUS.md's own learning: **ad tone ≠ social tone.** Ads use direct CTAs; social is value-first/soft-CTA. Do not let the social voice profile leak into paid
- [x] **3.5** ✅ **Store the recipe, not just the asset** — write the full generation spec (template ID, angle ID, copy variant, source asset, params) into `marketing_assets.provenance`. **This is the single highest-leverage step in the build** — it's what makes the feedback loop compound instead of just reporting
  > 🐞 **This was silently broken until 2026-08-03.** `recentAssets()` in `_lib.mjs` never selected the
  > `provenance` column, so `asset.provenance.recipe` was **always `undefined`**. `winners` had been
  > joining against recipes that could never be there — the compounding step compounded nothing, and
  > nothing surfaced an error because a missing recipe just renders as "unrecorded".
  >
  > Found by building `entropy` on the same helper and getting "0 batches" immediately after a
  > successful ingest. One column added to one SELECT. **Worth remembering: the recipe loop's failure
  > mode is silence, not an exception** — if `winners` ever shows everything as `unrecorded` again,
  > check the read path before assuming the writes are missing.
- [x] **3.7** ✅ **The ingest seam** — `meta-ads.mjs ingest --file=<manifest.json>`. Turns produced
  files + recipes into validated `marketing_assets` rows. Rejects: missing file, unknown family, no
  angle, and any avatar script failing the ACL test. **Capture-agnostic by design** — it knows nothing
  about how the pixels were made, which is exactly what lets the capture layer be swapped without
  touching the publish path. This is where the capture pipeline plugs in.
- [x] **3.6** ✅ Enforced in code (`MIN_CREATIVES_PER_BATCH`). Target **15–20 diverse creatives** for the first ad set, per Andromeda's diversity floor

**Done when:** 15+ brand-checked Radius Pro creatives exist as `marketing_assets` rows, each with a complete, replayable recipe in `provenance`.

## Phase 4 — Publishing

- [x] **4.1** ✅ Implement the Meta publish chain: **`POST /adimages`** (upload) → **`POST /adcreatives`** (build creative) → **`POST /ads`** (create, `status=PAUSED`)
- [x] **4.2** ✅ **Always create paused.** Human flips to active in Phase 4. This is the approval gate at its most literal
- [x] **4.3** ✅ (enforced in policy) Campaign structure: **one campaign, one ad set, many creatives.** Meta's own test says 1×25 beats 5×5 — but at Craftons' event volume (§4.6) this is not an optimisation, it's survival. **Splitting the ad set starves every one of them and kills the account.** Enforce it in code: the publish path refuses to create a second ad set
- [x] **4.4** ✅ Add `meta-ads.mjs publish --approval_id=<uuid>` behind the standard guards
- [x] **4.5** ✅ Surface the whole batch in the Cockpit for one-screen approval — built as
  `components/marketing/meta-ads/creative-batch-approval.tsx` + `POST /api/marketing/approvals/batch`.
  Same human gate, one screen: every item individually selectable, **nothing pre-selected**, and
  deliberately **no "approve all pending" shortcut** that skips looking at the list. Shows family mix
  and synthetic share so the batch can be judged *as a batch* — a batch that is all one family passes
  every per-item check and still fails the diversity rule. Capped at 50 per request; `decideApproval`
  still refuses anything not currently pending, so a replayed request can't flip a decided row.

**Done when:** an approved batch of 15 creatives appears in the Meta account as paused ads, correctly structured.

## Phase 5 — The loop (this is where it becomes an agent)

- [x] **5.1** ✅ Add `meta-ads.mjs evaluate` — read `marketing_metrics_cache` (**not** the API — Cody's rule), apply kill/keep rules
- [x] **5.2** ✅ Kill rules, explicit and tunable. Starting point: **≥3 days live AND ≥$X spend AND zero results** → propose pause. Never kill on under-spend; never kill inside 48h
- [x] **5.3** ✅ **Winners pool** — built as `meta-ads.mjs pool`.
  > ⚠️ **Corrected 2026-08-03: "surviving ads compete for budget" is not implementable as written.**
  > On Meta the budget lives on the **ad set**, not on individual ads, and Craftons runs exactly one
  > ad set (§4.6). There is no per-ad budget to shift between winners.
  >
  > What the pool actually is: **the set of ads left ACTIVE.** Meta's delivery optimisation then
  > concentrates the ad set budget on whichever performs — which it does better than we could from
  > outside. Our job is to curate the pool it chooses from, not to second-guess the allocation.
  >
  > Ranking is lexicographic, not a blended score: **an ad with results always outranks a cheaper one
  > without.** A $0.09 CPC on zero conversions is the July failure, not a near miss. Pool size 8, and
  > dropping below 5 flags "publish fresh creative" rather than letting the pool run thin.
- [x] **5.4** ✅ Built as `meta-ads.mjs winners`. **The compounding step:** join winners back to their `provenance` recipes and generate the next batch weighted toward winning *recipe patterns* — hook type, composition, angle — not winning images
- [x] **5.5** ✅ **Cadence** via Vercel Cron — `app/api/cron/meta-ads`, Sun 22:00 UTC. Start weekly, not daily. Cody runs 10 ads/day for clients with real budget; Craftons at Melbourne-metro scale needs a slower clock or it'll burn budget on noise
- [x] **5.6** ✅ Every cycle proposes; a human approves. Autonomy is Phase 6

**Done when:** a scheduled run reads real performance, proposes kills and a next batch, and files them as approval rows without being asked.

## Phase 6 — Entropy + earned autonomy

- [~] **6.1** **Meta Ad Library** puller — client built inside `meta-ads.mjs entropy`, **but blocked on access**.
  > 🔴 **Corrected 2026-08-03: it is NOT "free, no auth".** Tested live against `/ads_archive` both
  > with and without a token — both return `OAuthException` code 10, **subcode 2332002**:
  > *"To access the API, you'll need to follow the steps at facebook.com/ads/library/api."*
  >
  > The API needs a **separately approved app plus ID verification**. The general (non-political) ad
  > archive is not open. The **web UI at `facebook.com/ads/library` remains browsable by hand**, so
  > manual swipe-file gathering still works — it just isn't automatable yet.
  >
  > ### 🛑 Do NOT apply for API access — it would not help
  >
  > Checked Meta's own `ads_archive` reference before recommending the application. The
  > `ad_reached_countries` parameter documentation states:
  >
  > > *"Ads that did not reach any location in the EU will only return if they are about social
  > > issues, elections or politics."*
  >
  > **Craftons' competitors are Melbourne building-products suppliers advertising to Australia.**
  > They never reach the EU and they are not political — so they are **not in the archive at all**.
  > A fully-verified, fully-approved app would return an **empty set** for any AU query.
  >
  > **This is a coverage limit, not a permissions one.** The government-ID verification would have
  > bought nothing. Worth knowing before anyone repeats the exercise.
  >
  > **What actually works:**
  > - **The web UI at `facebook.com/ads/library`** does show Australian commercial ads and needs no
  >   API access whatsoever. Swipe-file gathering is a manual job — that's the honest answer
  > - **The API is genuinely useful for EU/UK** reference, where commercial ads *are* archived.
  >   `entropy --countries=GB` works if we ever want overseas creative as fresh DNA
  >
  > Consequence for Phase 6: **entropy cannot be fully automated from competitor ads in Australia.**
  > The novelty check (6.4) carries more weight here than it would elsewhere, because it's the
  > anti-convergence mechanism that doesn't depend on an external feed.
- [ ] **6.2** **Virlo API** (`virlo.ai`) — trending short-form formats, if the category justifies the cost
- [ ] **6.3** Trade YouTube/podcast transcript mining for angles
- [x] **6.4** ✅ **Novelty check** — built into `meta-ads.mjs entropy` + `checkNovelty()` in policy.
  Compares a proposed batch against a **3-batch lookback window** (comparing against only the previous
  batch reproduces exactly the blind spot Cody warns about). Flags >50% recipe reuse, and separately
  flags **one idea repeated** — a batch of 8 with 1 distinct pattern fails even with no history.
  Recipe signature is deliberately coarse: `family | angle | template`, **not** the image or exact
  copy, because two photos carrying the same angle in the same format are the same idea twice.
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
| **3** | Rung 2 + publish new creative **PAUSED**, from already-approved templates and angles | New angles, new templates, budget increases, **switching any ad on** | 8 weeks at Rung 2, brand-check pass rate > 95% |
| **4** | Full loop within a hard monthly spend ceiling — **still publishing paused only** | Ceiling changes, new product lines, **switching any ad on** | Sustained performance + Lee's explicit call |

> 🔒 **The ladder never grants activation — including after the 2026-08-13 amendment.** Read the
> "publish" rungs precisely: rung 3 and rung 4 permit publishing an ad **in a paused state**. Not one
> rung on this ladder — including rung 4 — lets the agent set an ad live *unattended*.
>
> The amendment made activation *possible*, not *automatic*: `activate_campaign`/`activate_ad_set`/
> `activate_ad` sit in `ALWAYS_REQUIRES_APPROVAL`, so every rung still needs Lee's explicit approval for
> each one. See **LAW 1** at the top. "Full loop" at rung 4 means research → creative → paused publish
> → measure → propose, with **Lee's approval** in the middle.

**Implementation:** this is a policy table, not new code. `marketing_approvals` already exists; the
ladder is a config listing which `action` values require a row at the current rung. Store the rung in
config, not in code, so it can be lowered instantly if something goes wrong.

**Non-negotiable at every rung:**
- 🔒 **No ad goes live without Lee's explicit approval (LAW 1). No rung changes this, ever** — the
  2026-08-13 amendment moved *where* he approves, never *whether* he approves.
- 🇦🇺 **Australia-only targeting** — enforced by `checkTargeting()`, audited live by `report`
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
| **`META_APP_ID`** = `993965426717610` | ✅ **Already exists — app "Craftons Ads API".** No lookup needed | Free | 🟢 tidy-up |
| **`META_APP_SECRET`** | `appsecret_proof` request signing only — **not** token refresh | Free | 🟢 optional |

> ### ⚠️ Corrected 2026-08-03 — this row said "required for long-lived token refresh"
>
> **The access token does not expire.** Checked via `/debug_token`:
>
> ```
> type: SYSTEM_USER · expires_at: 0 · data_access_expires_at: 0 · is_valid: True
> scopes: ads_management, ads_read, business_management
> ```
>
> `expires_at: 0` means never — that is how system-user tokens work. There is no refresh flow to
> build and no expiry cliff coming, so the app secret is **not** a Phase 1 blocker. Its only use here
> is `appsecret_proof` request signing, which is optional unless the app is set to require it.
>
> Also settled: the "second dataset `993965426717610` (Craftons Ads API, app-type)" in earlier notes
> is **not a dataset** — it is the **app ID**.
| **Meta Marketing API access level** | Dev tier = 60 quota points / 300s. Standard = 9,000, needs App Review | Free, but App Review has lead time — **start early** | 🔴 Phase 1 |
| **Meta Pixel + CAPI on Shopify** | Phase 0 gate | Free | 🔴 Phase 0 |
| **HeyGen** (`HEYGEN_API_KEY`) | AI avatar presenters (§4.2) — ~4 of the launch 15–20 creatives | ~$30–90/mo depending on tier | 🟠 Phase 3 |

> **Note:** the **HyperFrames by HeyGen MCP connector is already live in this session**, so avatar
> video may be reachable without a raw API key at all. Check the connector before buying a plan —
> per the standing "invest in integrations" rule, the connector is the cheaper durable path if it covers
> the need.

## Explicitly NOT needed (and why)

| Cody uses | We don't | Because |
|---|---|---|
| **Airbyte** | ❌ | 3 sources, all with direct APIs. `cacheMetric()` already does this |
| **ClickHouse** | ❌ | Neon Postgres is live and adequate at this volume. Revisit only if the data outgrows it |
| **Heroku / Railway** | ❌ | Vercel is already the deploy target |
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
- 🔒 **LAW 1 — no ad goes live without Lee's explicit approval.** Nothing publishes active; ads are
  created `PAUSED` and stay that way until Lee approves an activation. Since 2026-08-13 the
  `activate_*` mutations exist so he can approve through Claude instead of Ads Manager, but all three
  sit in `ALWAYS_REQUIRES_APPROVAL` at every rung, need `CONFIRM=1` plus a named human approver, and
  pass a live preflight (AU targeting + spend caps re-read from the account) before anything goes live.
  **No autonomy rung grants activation.** Full enforcement table at the top of this doc
- 🇦🇺 **Australia only.** `ALLOWED_COUNTRIES = ["AU"]`. An ad set with **no** geo set fails too — it
  runs worldwide rather than erroring, which is how three of them got onto the account unnoticed
- `brand-check` gates every asset, always
- Never AI-generate product geometry or dimensions — that rule survives the avatar approval
- **Hard $2,000/month ceiling in code**, checked before every write (§4.6)
- Australian/British spelling in all copy ("Optimise", "Centre")
- Ad tone ≠ social tone

**New, specific to this build:**
- **ONE ad set. The publish path must refuse to create a second one** — at Craftons' event volume,
  splitting starves everything (§4.6)
- **Never kill an ad inside 48 hours** — Cody's own window is 2–3 days for initial signal
- **Never kill on insufficient spend** — no data is not the same as bad data
- **Avatar scripts: second person about the product, never first person about experience.** Enforced
  automatically in `brand-check` (§4.2) — a fabricated testimonial is an ACL breach, not a style choice
- **A creative batch drawn from a single family fails brand-check** — day-one entropy defence (§4.3)
- **Log every autonomous decision with its reasoning**, so a bad rule can be traced and reverted
- **Score on revenue, never on cost-per-lead** — CPL is the dial, revenue is the judge

---

# PART 9 — Open questions

### ✅ Resolved 2026-08-03

1. ~~**Optimisation event?**~~ → **Combined high-intent Lead** (quote + configurator + purchase as one
   custom conversion), scored on revenue. Full reasoning and arithmetic in **§4.6**.
2. ~~**Budget ceiling?**~~ → **$2,000/month**, enforced in code, with the staged ramp in **§4.7**.
3. ~~**AI avatars?**~~ → **Approved as presenters**, banned as testimonial-givers (**§4.2**).
4. ~~**Is the Meta account clean?**~~ → **Corrected 2026-08-03.** Not a cold start at all — it is live,
   instrumented, and running at **~8.7x ROAS** over 30 days. The earlier "3 orders / $729" reading came
   from Shopify referrer attribution, which undercounts Meta by more than 10x. Full post-mortem in **§4.5**.

### 🔴 Still blocking

5. ~~**What is the actual gross margin?**~~ ✅ **RESOLVED 2026-08-03 from Xero.**
   Peninsula Studio, Feb–Jul 2026: income **$594,223**, COGS **$282,592**, gross profit **$311,631**
   → **gross margin 52.4%**. On a $614.67 Radius Pro AOV that is **~$322 gross profit per order**,
   so **break-even CAC ≈ $322** (my 45% assumption was slightly conservative — there is more headroom,
   not less). Break-even volume at $2k/month drops to **~6.2 orders**.
   ⚠️ **Caveat:** this is business-wide margin. Craftons is $165,140 of the $594,223 income, and
   Radius Pro specifically may differ from the blended figure. Good enough to set kill criteria;
   worth refining if Craftons-only COGS can be split out.
6. **Where does a "configured quote request" fire?** §4.6 depends on a high-intent lead event existing
   and being distinguishable from a generic contact form. Needs confirming in the Shopify/configurator
   setup before Phase 0 can be completed.

### 🟡 Blocking Phase 3

7. **Real before/after site photography** — the strongest angle available (§4.3, family 6) and the only
   one that cannot be assembled from existing assets. Two photos: a bog-and-sanded on-site curve, and
   Craftons parts arriving cut.
8. **Confirm footage rights** for any of Tia's material used in paid ads.
9. **Which HeyGen avatar + voice?** Needs to be picked once and locked, then reused — a different
   presenter every batch reads as inconsistent rather than diverse. Note the **HyperFrames/HeyGen MCP
   connector is already live in this session**.

### 🟢 Decide later

10. **Does the Cockpit need a Meta-specific approval UI?** Approving 15 creatives one at a time will
    not survive a real week (Phase 4.5).
11. **When does CNC Cut get the same treatment?** Keep the architecture multi-account-capable so this
    isn't a rewrite.

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
