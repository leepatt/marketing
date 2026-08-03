# How to sell more — Craftons, August 2026

_Written 2026-08-03 from live Google Ads API + Shopify analytics. Companion to
`optimisation-plan-2026-08.md`._
_Scope: ads run for **Radius Pro, Architrave Builder, Formwork Builder** only. Cavity Battens is
discontinued; Rip Pro is not advertised (Lee, 2026-08-03)._

---

## Where the business actually stands

**Last 90 days:** 22,664 sessions → 101 orders → **0.45% site-wide conversion rate.**

| Source | Sessions | Share | Orders | CVR |
|---|---|---|---|---|
| **Social** | 14,926 | 66% | **5** | **0.034%** |
| **Direct** | 4,174 | 18% | **69** | **1.65%** |
| Search | 3,358 | 15% | 19 | 0.57% |
| Email | 5 | 0% | 0 | — |

**Direct traffic produces 68% of orders from 18% of sessions.** Social produces two-thirds of the
traffic and 5% of the orders. Email is functionally non-existent.

**Product mix, 12 months:**

| Product | Sales | Orders | AOV |
|---|---|---|---|
| Radius Pro | $126,995 | 204 | $623 (rising — $794 last 90d) |
| Formwork Builder | $13,914 | 12 | $1,159 |
| Architrave Builder | $9,830 | 9 | $1,092 |

---

## 1. Don't scale ads yet — the maths doesn't work at today's numbers

This is the most important thing in this document, because it's the thing most likely to be done
wrong: the instinct with a flat month is to raise budgets.

Two independent sources say the same thing:

- Site-wide **search** traffic converts at **0.57%**
- The **ads** converted at **0.32%** (1 purchase / 316 clicks)

At the current **$5.07 CPC** and ~0.5% conversion, cost per sale is roughly **$1,000** on a product
with a **$623–794 order value.** Every extra dollar of budget currently loses money.

The fix isn't more spend, it's changing the inputs:

| | Today | After page fixes | Effect |
|---|---|---|---|
| CPC | $5.07 | ~$3.00 (QS 1→5+) | −40% |
| CVR | 0.5% | 2.0% | 4x |
| **Cost per sale** | **~$1,000** | **~$150** | **works** |

Both improvements come from the same job: the landing page work in `optimisation-plan-2026-08.md`.
**That work is the prerequisite for every other paid idea here.** Do it first.

---

## 2. Put ad money on Formwork and Architraves, not Radius Pro — for now

Counter-intuitive, because Radius Pro is the flagship. But:

| | Radius Pro | Formwork | Architraves |
|---|---|---|---|
| AOV | $623 | **$1,159** | **$1,092** |
| Landing page keyword match | "curved" ×1 | **"formwork" ×8** ✅ | "moulding" ×0 |
| Ad group conversions (33 days) | **0** | **2** | 1 |
| Ad strength | POOR (paused) + AVERAGE | **GOOD** + AVERAGE | AVERAGE |

Formwork has **~2x the order value, the only decent landing page, the only GOOD-rated ad, and half
the account's conversions.** It is the one place where the economics already nearly work.

**Move the marginal dollar to Formwork** until the Radius Pro page is fixed. Then swing back —
Radius Pro has 17x the order volume and is the long-term prize.

---

## 3. The biggest untapped asset: 15,000 social visits a quarter with no way to capture them

Social sends **14,926 sessions per quarter** and produces **5 orders**. Meanwhile email sent **5
sessions in 90 days** — there is effectively no email channel.

That's the leak. Fifteen thousand people who are interested enough in curved building work to click,
arriving, browsing, and leaving with no way to ever reach them again.

**Two caveats before anyone concludes the content isn't working:**

1. **Last-click attribution badly undervalues social.** Direct is the highest-converting channel at
   1.65%, and "direct" is largely people who already know Craftons. A lot of that recall is being
   built by the social content — it just gets credited to direct when they come back to buy. The
   content is likely working; it's the *measurement* that's flattering direct.
2. Social is browse-intent by nature. 0.034% is low, but nobody buys $800 of custom curved plywood
   off an Instagram tap.

So don't cut the content. **Build the bridge instead:**

- **Email capture.** A lead magnet aimed at exactly this audience — a curve/radius setout guide, a
  "how to spec curved work" PDF, a radius calculator. The repo already has `lead-magnet`,
  `email-sequences` and `newsletter` skills sitting unused. Even a 2% capture rate on 15,000 visits
  is **300 emails a quarter** from traffic that currently leaves no trace.
- **Retargeting.** 15,000 warm sessions a quarter is a large, cheap, completely unused audience.
  Retargeting them costs a fraction of search CPCs because there's no auction competition for
  "people who already visited craftons.com.au".

**Rough size of the prize:** lifting social from 0.034% to just 0.3% — still 5x worse than direct —
is ~45 orders a quarter instead of 5. At ~$700 AOV that's **+$28,000 a quarter**. For comparison, the
entire Google Ads account spends about $17,000 a year.

---

## 4. Interstate: 23% of revenue, no ads behind it

| State | 12-month sales | Orders | Advertised? |
|---|---|---|---|
| Victoria | $158,640 | 187 | ✅ |
| **NSW** | **$26,614** | **44** | Architraves only |
| **QLD** | **$10,252** | **10** | Architraves only |
| SA / TAS / ACT | $12,139 | 13 | ❌ |

**$49,006 and 67 orders from outside Victoria with essentially no advertising.** NSW alone did 44
orders unassisted. That's proven demand in a market you aren't bidding in.

Note interstate customers spend *more* per order (QLD AOV $1,285 vs VIC $828) — freight cost
naturally selects for bigger jobs.

**Sequence matters:** extend to Sydney and Brisbane on a separate test budget **after** the page
fixes. Extending reach while landing pages score Below Average just buys expensive clicks in a new
market. This is step 3, not step 1.

---

## 5. Speak the customer's language, not the product's

Two concrete cases from the search data, both costing money right now:

- **Architraves:** customers search **"arch moulding"**, "hallway arch moulding", "archway trim".
  The page uses the word "moulding" **zero times**. Fixing the vocabulary is free and lifts both paid
  Quality Score and organic search.
- **Radius Pro:** customers search **"bendy ply"**, "bendable plywood", "flexible plywood". The page
  contains none of those words. They're not looking for a product name, they're looking for a curve —
  meet them with their words, then reframe to "we cut the curve for you".

This is the cheapest lever on the list. It's copywriting, not development.

---

## 6. Measurement gaps worth closing

- **Lead values.** `form_submit` carries a $1 placeholder, so bidding optimises for lead count, not
  value — treating a $200 architrave enquiry the same as a $6,000 formwork package. Needs a close
  rate from Lee and a site-side tagging change (see `optimisation-plan-2026-08.md`).
- **Attribution.** Last-click is crediting direct for sales that social started. Worth at least
  looking at assisted conversions before making budget decisions between channels.

---

## Do this, in this order

| # | Action | Effort | Why it's ranked here |
|---|---|---|---|
| 1 | **Fix the three landing pages** — keyword vocabulary + readable content | Medium | Unlocks everything paid; halves CPC and lifts CVR |
| 2 | **Shift ad budget to Formwork** while Radius Pro's page is fixed | Trivial | 2x AOV, best page, only GOOD ad |
| 3 | **Lead magnet + email capture** for social traffic | Medium | 15,000 warm visits/quarter currently leave no trace |
| 4 | **Retarget social visitors** | Low | Cheapest warm audience available, entirely unused |
| 5 | **Extend Radius Pro ads to NSW + QLD** | Low | $37k of proven unassisted demand — but only after #1 |
| 6 | **Set real lead values** | Low | Blocked on close rate + tagging |

### And explicitly, don't:

- **Don't raise budgets before the pages are fixed.** At ~$1,000 cost per sale, more budget = more loss.
- **Don't rebuild for mobile.** Mobile converts *identically* to desktop on direct traffic (1.72% vs
  1.69%). The earlier mobile recommendation in `optimisation-plan-2026-08.md` was wrong and is retracted.
- **Don't cut the social content** because of its 0.034% last-click rate. It's very likely feeding the
  1.65%-converting direct channel.
- **Don't prune keywords on zero conversions.** At a ~1% conversion rate you'd need ~230 clicks per
  keyword to judge; the busiest has 28.
