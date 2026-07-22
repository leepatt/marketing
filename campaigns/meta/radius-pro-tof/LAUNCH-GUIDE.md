# Radius Pro. Top-of-Funnel Meta Push · Step-by-Step Launch Guide

> **The bet:** bottom-of-funnel is already converting cheap. The ceiling isn't conversion. It's
> *awareness*. Radius Pro is a proven product with daily sales; the one problem is **no one knows
> it exists.** This campaign buys that awareness at the top of the funnel and feeds the BOF engine
> that already works.
>
> **Golden rule (never break):** every ad sells the **self-serve online builder**. Design online →
> instant price → delivered. **Never "send us your CAD."** All 5 ads point to **Radius Pro**:
> `https://craftons.com.au/products/radius-online`
>
> Date: 2026-07-21 · Owner: Lee · Status: creative ready to launch, this doc is the playbook.

---

## 0. What you're launching (the shape)

- **1 campaign**, **1 ad set**, **5 static ads** (a clean creative A/B test. Same audience, same
  budget, Meta decides the winner). This is the bible §9 rule: *statics on volume, let Andromeda
  (Meta's AI) eat fresh creative and find the buyer.*
- **Audiences targeted by the creative, not the settings**, 3 ads speak to **builders/carpenters**
  (curved wall plates), 2 speak to **concreters** (curved formwork). The trade word is *in the ad*
  (bible §6 hack 2: identity-keyword targeting). Run **broad AU** and let the creative sort them.
- **Start $100/day. Scale the winners.** No hero creative. A batch, judged on net cash, not ROAS %.

The 5 creatives and their copy live in **`AD-CONCEPTS.md`**. The rendered images live in
**`creative/`**. This file is *how you put them live and scale them.*

---

## 1. Before you touch Ads Manager (30-min prerequisites)

Tick these or the spend is wasted:

1. **Pixel + Conversions API firing on `radius-online`.**
   - Business Settings → Data Sources → Pixels → confirm the Craftons pixel is on the Shopify
     store and fires **PageView**, **ViewContent**, **InitiateCheckout**, **Purchase**.
   - Shopify → Settings → Customer events / the Meta (Facebook & Instagram) channel → confirm
     **Conversions API** is on (server-side. You need this now that browser tracking is leaky).
   - **Test it:** Events Manager → Test Events → load `radius-online`, add to cart → watch the
     events land. If they don't, stop and fix this first.
2. **A real conversion event to optimise toward.** TOF is awareness, but we still optimise for the
   money action so Meta finds buyers, not tyre-kickers. Use **Purchase** if the pixel has ≥~15
   purchases/week on this product; if volume is thin, optimise for **Initiate Checkout** or **Add
   to Cart** to give the algorithm enough signal, and watch Purchases as the real scoreboard.
3. **Domain verified** (Business Settings → Brand Safety → Domains → `craftons.com.au`) so you own
   the events and aggregated measurement.
4. **Payment + spend limit sane.** Set an **account spend limit** as a hard backstop (e.g. $1,500)
   so a runaway can't hurt you while you're scaling.
5. **UTMs** on the destination URL so Shopify/GA see the traffic (template in §5).

---

## 2. Campaign architecture (exact settings)

**Campaign**
- Objective: **Sales** (a.k.a. Conversions). *Not* Awareness/Traffic. We want the algorithm hunting
  buyers even at the top of the funnel; that's what makes TOF pay for itself.
- Campaign name: `RadiusPro | TOF | Statics x5 | Jul26`
- **Advantage+ campaign budget (CBO): ON**. One budget across the ad set, Meta distributes.
- Special ad categories: none.

**Ad set** (name: `TOF | Broad AU | RadiusPro`)
- **Conversion location:** Website. **Pixel:** Craftons. **Event:** per §1.2.
- **Budget:** $100/day (CBO at campaign level; single ad set = same thing).
- **Audience:** the modern default. Go **broad** and let the creative target:
  - Location: **Australia** (all). *Optional tighten later:* exclude NT/remote if delivery is a pain.
  - Age **25-64**, all genders.
  - **Detailed targeting: EMPTY.** No interests. (Advantage+ audience / broad beats hand-picked
    interests now. The creative does the targeting. This is the whole point of the identity-keyword
    hack.) If the platform forces a suggestion, leave Advantage+ audience **on** with no constraints.
  - **Advantage+ placements: ON** (all placements). Our creative is built for feed **and** stories/
    reels (4:5 + 1:1 + 9:16), so let Meta place it everywhere cheap.
- Optimisation: **Maximise number of conversions.** Bid strategy: **Highest volume** (no cap) to
  start. Add a cost cap only once you know your CPA.
- Attribution: **7-day click, 1-day view** (default).

**Ads:** all **5** in this one ad set. Each ad = one image (we'll add the 1:1 and 9:16 as placement
variants of the same ad so the creative matches the placement). See §4 for the upload map.

> **Why one ad set, not five:** five ad sets split the budget and starve the learning phase. One ad
> set + five creatives lets Meta move spend to the winner inside a single learning phase. Clean test,
> faster read.

---

## 3. Budget & the scale ramp (the "dramatically increase spend" plan)

You don't leap to big spend. You **earn** it. The ramp:

| Phase | Days | Daily budget | What you're doing | Gate to advance |
|-------|------|--------------|-------------------|-----------------|
| **0 · Learn** | 1-4 | **$100** | All 5 live, don't touch it. Let the learning phase finish (~50 conversions or 3-4 days). | ≥1 ad with CPA at/under target & CTR ok |
| **1 · Prune** | 5-7 | **$100-150** | Turn off the 1-2 worst ads (see §6 kill rules). Keep 3-4 winners. | Winners holding CPA as budget rises |
| **2 · Scale** | 8-21 | **+20-30% every 2-3 days** → $250-400 | Raise campaign budget in steps. Never more than ~30% at once (resets learning). | CPA stable / net cash positive |
| **3 · Feed the machine** | 21+ | $400 → whatever stays profitable | Add fresh statics weekly (§7), duplicate winners into new angles. | Keep scaling while net cash holds |

**Rules of the ramp**
- **Judge on net cash, not ROAS %** (bible §6). A curved job averages ~$1,450 (range $455-$3,641).
  A $30-60 CPL/CPA that lands $1,450 jobs is a licence to print. Scale it.
- **Raise budget at the campaign, in ≤30% steps, every 2-3 days.** Bigger jumps re-trigger the
  learning phase and tank delivery.
- **Don't fiddle daily.** Meta needs 48-72h per change to settle. Look, don't touch, between reads.
- **Increase only "if we can"** (your words): the gate is *CPA holding as budget climbs.* The moment
  cost-per-purchase creeps past your ceiling for 3+ days, hold budget and refresh creative instead.

**Set your numbers before launch:**
- Target CPA (cost per Radius Pro purchase) you'll accept: `$____` (suggest ≤ $120 given ~$1,450 AOV).
- Target CPL if optimising to a soft event: `$____` (suggest ≤ $40).
- Daily ceiling for this month: `$____` (start-of-ramp suggests topping out ~$400/day, revisit).

---

## 4. Upload map. Which file goes where

Each **concept = one ad**. Within the ad, load all three ratios so the creative matches the
placement (Meta calls this "customise per placement"):

| Ad in Ads Manager | Feed / main (4:5) | Square (1:1) | Stories & Reels (9:16) | Audience |
|-------------------|-------------------|--------------|------------------------|----------|
| **AD1 · Builder. Pain** | `creative/ad1-builder-pain_1080x1350.png` | `...1080x1080.png` | `...1080x1920.png` | Builders |
| **AD2 · Builder. Spec Stamp** | `creative/ad2-builder-spec_1080x1350.png` | `...1080x1080.png` | `...1080x1920.png` | Builders |
| **AD3 · Builder. Number Card** | `creative/ad3-builder-number_1080x1350.png` | `...1080x1080.png` | `...1080x1920.png` | Builders |
| **AD4 · Concreter. The Question** | `creative/ad4-concretor-question_1080x1350.png` | `...1080x1080.png` | `...1080x1920.png` | Concreters |
| **AD5 · Concreter. Ready to Pour** | `creative/ad5-concretor-pour_1080x1350.png` | `...1080x1080.png` | `...1080x1920.png` | Concreters |

Per ad, paste the **primary text / headline / description** from `AD-CONCEPTS.md`, set the
destination URL (with UTM, §5), CTA button = **"Shop now"** (or "Get quote". Test both later).

---

## 5. Tracking. The destination URL + UTMs

Base: `https://craftons.com.au/products/radius-online`

Append per ad so you can read performance in Shopify/GA, not just Ads Manager:

```
?utm_source=meta&utm_medium=paid_social&utm_campaign=radiuspro_tof_jul26&utm_content=ad1_builder_pain
```

Change only `utm_content` per ad: `ad1_builder_pain`, `ad2_builder_spec`, `ad3_builder_number`,
`ad4_concretor_question`, `ad5_concretor_pour`. Keep `utm_campaign` identical across all 5.

> Meta's dynamic params also work (`utm_content={{ad.name}}`). But hard-coding is bulletproof.

---

## 6. Measurement & decision rules (what to kill, what to scale)

Read the campaign **every 2-3 days**, never daily. Per ad, watch, in order:

1. **CPA / CPL** (the money metric). The scoreboard.
2. **CTR (link)**, < ~0.8% and it's not earning attention → creative is weak.
3. **Hook rate** (3-sec video n/a for statics; use **CTR + CPM**). High CPM + low CTR = the
   creative reads as an ad (bible §6 hack 3: don't look like an ad).
4. **Frequency**, > ~2.5 in the first 2 weeks on broad AU means creative fatigue → refresh.

**Kill an ad** when, after the learning phase (≥~1,000 impressions or ~50 clicks):
- CPA is 2× target with no purchases, **or**
- CTR < 0.6% **and** CPM above account average (nobody's biting).

**Scale an ad** (via the campaign budget, not by duplicating yet) when:
- CPA at/under target **and** it's winning the majority of spend Meta is giving it.
- Then in Phase 3, **duplicate the winner into a new angle** (swap the trade word / job type) to open
  a fresh audience. That's how you widen without just spending more on the same people.

**The learning phase is sacred.** Don't edit an ad mid-learning; you reset it. Note ideas, batch them
into the weekly refresh.

---

## 7. Keep it alive. The weekly creative cadence

Meta's Andromeda AI **eats fresh creative** (bible §9). One batch fatigues; the engine is a *feed*.

- **Every week, ship 3-5 new statics.** Source is infinite: Craft Macro stills, configurator renders,
  spec/number cards, a new job photo, a new trade word ("Formworkers, ", "Landscapers, "), a new
  job type (curved bench seat, curved stairs, arched doorway, curved retaining wall).
- **Identity-keyword variants are the cheat code** (bible §6 hack 2): take a winning layout, swap only
  the trade word. Each variant opens a new audience and drops CPL. One winning concept → 6 ads.
- **Rotate:** as an ad fatigues (frequency ↑, CTR ↓), retire it and slot a fresh one into the same
  ad set. Keep the ad set alive; recycle the creatives.
- **Match the scent:** every new static's headline must match the top of the Radius Pro page it
  points to (bible §6 hack 5). If the ad says "Curved Wall Plates, Cut to Size," that phrase should
  greet them on the page.

---

## 8. Launch-day checklist (do these in order)

- [ ] §1 prerequisites all green (pixel + CAPI test-passed, event chosen, domain verified, spend limit set).
- [ ] Fill your numbers into §3 (target CPA/CPL + monthly ceiling).
- [ ] Create campaign per §2 (Sales objective, CBO on, $100/day).
- [ ] Create the one broad-AU ad set per §2 (empty detailed targeting, Advantage+ placements on).
- [ ] Build the 5 ads per §4. For each: upload 4:5 + 1:1 + 9:16, paste copy from `AD-CONCEPTS.md`,
      set URL + UTM (§5), CTA button.
- [ ] Proof every ad in the preview (all placements). Text legible, story safe-zones clear, link works.
- [ ] Publish. **Then don't touch it for 3-4 days.**
- [ ] Diary the launch date + starting numbers so you can measure the lift.
- [ ] Day 4-5: first read (§6). Prune. Begin the ramp (§3).

---

## 9. 60-second recap

Proven product, invisible to the market → buy awareness at the top, optimise for the money action,
let broad targeting + trade-specific creative find the buyer. Five statics, one ad set, $100/day.
Read every 3 days, kill the losers, scale the winners ≤30% at a time, and **feed fresh statics
weekly**. Because the algorithm rewards volume of creative, and net cash is the only score that
matters.
