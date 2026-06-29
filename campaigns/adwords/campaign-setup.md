# AdWords campaign setup & management — Craftons

_Created 2026-06-30. Goal: leads & sales without wasting spend. Ad copy: `ads/`. Keywords: `../../brand/keyword-plan.md`._

## Campaign settings
- **Name:** Craftons – Customised Building Products
- **Type:** Search **only** — turn **OFF** "Search Partners" and "Display Network expansion"
  (these waste small budgets on low-quality clicks).
- **Daily budget:** **$50/day** (~$1,520/mo). One shared budget across the 3 ad groups — Google
  shifts spend to whatever performs.
- **Bidding:** start on **Manual CPC** (or *Maximize clicks* with a **max-CPC cap ~$3.50**) — keeps
  control while there's no data. **Switch to *Maximize Conversions* only after ~15–30 conversions.**
  (Smart bidding with zero history burns budget.)
- **Geography:**
  - **50 km radius around Melbourne CBD** (radius targeting)
  - **+ Geelong**, **+ Surf Coast Shire**, **+ Mornington Peninsula Shire** (Geelong/Surf Coast sit
    outside the 50 km radius — add them as separate location targets)
  - **Location option = "Presence: people in/regularly in your targeted locations"** (NOT "presence
    or interest"). This is a key money-saver — stops paying for out-of-area searchers.
- **Networks/devices:** all devices; review mobile vs desktop after 2 weeks.
- **Ad schedule:** start all-day. Refine to trade hours later if night clicks don't convert.

## Ad groups (3) — keep tight
Each ad group = its keywords + the 2 RSAs in `ads/` + its product landing page.

| Ad group | Match types | Landing |
|----------|-------------|---------|
| **Radius Pro** | phrase + exact | /products/radius-online |
| **Curved Bench Seat / Formwork** | phrase + exact | /products/craftons-formwork-builder-custom-online-formwork |
| **Curved Architraves** | phrase + exact | /products/curved-architraves |

> **Use Phrase + Exact match, NOT Broad.** Broad match is where small budgets bleed. Google will
> nudge you to Broad — say no until you have conversion data and negatives built up.

## Negative keyword list (add at campaign level, day 1)
free, DIY, plans, how to draw, drawing, sketchup, cheap, cheapest, second hand, used, wholesale,
job, jobs, careers, salary, course, training, **hire, rent, rental** (we sell, not hire), repair,
labourer, bunnings, minecraft. *(Add more weekly from the Search Terms report — see below.)*

## ⚠️ Do this FIRST — conversion tracking (or you're flying blind)
You cannot run efficiently without measuring what a click is worth. Before spending a dollar, set up
**Google Ads conversion tracking** for the real actions:
- **Quote / contact form submit** (primary)
- **Configurator "add to cart" / checkout started** (Radius Pro, Formwork, Architrave)
- **Phone call clicks** + **email clicks**
Without this, you optimise on clicks (vanity) instead of leads (money). This is the single biggest
efficiency lever. Wire it via the Shopify/GA4 link or the Google Ads tag.

---

## How to manage it & not waste money — the weekly routine
Every Monday, ~20 minutes. The goal: **cut what wastes, scale what converts.**

### 1. Search Terms report (the #1 money-saver)
Campaign → Keywords → **Search terms.** This shows the *actual* queries that triggered your ads.
- Add any irrelevant query as a **negative keyword** (e.g. someone searched "free curved wall plans").
- This is where most wasted spend hides. Do it every single week.

### 2. Kill the losers
Sort keywords by cost. **Pause or cut the bid** on any keyword with **≥20 clicks + ~$40 spent + 0
conversions.** It's not paying its way.

### 3. Feed the winners
Move budget/attention toward the **ad group with the lowest cost-per-conversion.** If Architraves
converts at $25/lead and Formwork at $90, weight toward Architraves.

### 4. Tidy the ads
Ad group → Ads → **Assets.** Google rates each headline Low/Good/Best. Replace "Low" headlines with
new variants (plenty spare in the `ads/` files).

### 5. Read the 4 numbers that matter
| Metric | What it tells you | Action if bad |
|--------|-------------------|---------------|
| **CTR** (click-through) | Is the ad relevant? (aim >4%) | <2% → tighten keyword/ad match |
| **Conversion rate** | Is the landing page working? | low → fix the landing page, not the ad |
| **Cost per conversion** | Is a lead cheaper than it's worth? | above your margin → cut keywords/bids |
| **Wasted spend** (clicks, 0 conv) | Money leaking | add negatives, pause keywords |

### Guardrails (so it can't run away)
- **One set of changes per week.** Changing daily resets Google's learning and hurts performance.
- **Give it 2–3 weeks** before big judgments — at ~$50/day you need click volume to be statistically real. Don't kill a keyword off 5 clicks.
- The **max-CPC cap** stops any one click eating the budget.
- **Cost-per-lead vs job value** is the real scoreboard. If a curved-bench-seat job is worth $X and a
  lead costs a small fraction of that, the campaign's working — keep going. If leads cost more than a
  job's worth, pause and rethink, don't keep feeding it.

### Monthly
- Check device + geo splits (which suburbs/areas convert) → trim the dead ones.
- Once you have ~15–30 conversions, switch bidding to **Maximize Conversions** and let Google optimise.
- Reinvest learnings into the SEO articles (the keyword plan) so paid + organic compound.
