# Craftons — Weekly Marketing Review

_A repeatable ~20–30 min ritual (do it every **Monday**). Pull the numbers, look at the drop-off,
make one set of decisions, log it. Claude can run the Ads + Shopify pulls for you — you review
Clarity + decide. Fill in the **Weekly Log** at the bottom each week so we see the trend._

> **The real scoreboard:** cost per lead/sale vs. what a job is worth. Everything else is diagnostic.
> Change **one set of things per week** — changing daily resets Google's learning.

---

## 1. Google Ads — 5 min
Run (or ask Claude to run):
```bash
cd tools && node google-ads.mjs report            # last 7 days, by campaign
node google-ads.mjs report --days 30              # 30-day view
```
Then ask Claude for the **architrave deep-dive** (daily trend · impression share · geo split · funnel
micro-conversions view→cart→purchase · search terms).

**Look at:**
- Spend, clicks, **conversions**, cost/conv per campaign. Is spend where you want it?
- **Search terms report** → add any junk queries as **negatives** (biggest weekly money-saver).
- Architrave **geo split** — is Victoria still getting the majority (not starved by interstate)?
- Impression share — lost to **budget** (raise budget) vs **rank** (raise bid / improve QS)?
- Kill losers: any keyword with **≥20 clicks + ~$40 spent + 0 conv** → pause or cut bid.

## 2. Microsoft Clarity — architrave page — 5–10 min
`clarity.microsoft.com` → filter to **`/products/curved-architraves`**. (Claude can't log in — screen-grab
the heatmap + note what recordings show, and we'll read it together.)

**Look at:**
- Do visitors **open/use the builder**, or land-look-leave?
- **Where in the builder do they stop** — first field? after entering sizes? at the **price** (price shock)?
- **Scroll depth** — do they reach the images/copy, or exit above them?
- **Rage clicks / dead clicks** (Clarity flags these) — a fiddly/broken element (esp. iframe on mobile).
- **Mobile vs desktop** behaviour. **Exit points.**

## 3. Shopify — where sales come from — 5 min
Run (or ask Claude):
```
FROM sales SHOW orders, total_sales GROUP BY product_title ORDER BY total_sales DESC LIMIT 10 SINCE -30d UNTIL today
FROM sales SHOW orders, total_sales GROUP BY order_referrer_source SINCE -30d UNTIL today
FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout, conversion_rate TIMESERIES week SINCE -28d UNTIL today
```
**Look at:** top sellers (Radius Pro is #1), **where sales come from** (direct dominates ≈86% → awareness/
nurture is the engine, not search), site **conversion rate** (~1–2%) and **add-to-cart %** (~3%), and
**architrave orders** (lumpy — judge over weeks, not days).

## 4. Decisions + log — 5 min
Apply the triggers below, make **one** set of changes, then fill in the Weekly Log.

---

## Decision triggers (rules of thumb)
| See this | Do this |
|---|---|
| Junk search terms with clicks | Add as **negatives** |
| Keyword ≥20 clicks / ~$40 / 0 conv | Pause or cut bid |
| A geo spends but never converts | Bid it down (−50/−70%) or remove |
| IS lost mostly to **budget** + it's converting | Raise budget |
| IS lost mostly to **rank** | Raise max CPC or improve Quality Score |
| Clarity shows price-shock exits | Fix pricing clarity on the page |
| Clarity shows they never reach images | Surface images/proof higher |
| Cost/lead **> job value** | Pause/rethink — don't keep feeding it |
| Cost/lead **< job value** and converting | Scale it (budget/bids) |

## Current focus (update as it changes)
- **Architraves** = the profit bet. Victoria-weighted, ~$10–15/day, **0 conv so far** — letting it run
  3–4 weeks with tracking + Clarity before judging. High AOV (~$1,270) tolerates ~$200–300 CPA.
- **Ply + Formwork** = local, $50/day. Radius Pro is the account's real seller (mostly **direct**, not ads).
- **Cavity Battens Performance Max = PAUSED** — it was the account's main converter. **Decision pending:**
  un-pause? (demand-gen is likely the bigger lever than search for these niche products.)
- **Page CRO** = parked pending Clarity data (see `campaigns/adwords/architrave-page-cro-audit.md`).

---

## Weekly Log (fill in each Monday)
| Week (Mon) | Ads spend | Ads conv | Cost/conv | Architrave spend | Arch conv | Site CR | Arch orders (Shopify) | Clarity note | Change made |
|---|---|---|---|---|---|---|---|---|---|
| 2026-07-20 | ~$264/7d | 1 | ~$195 | ~$69 | 0 | ~1–2% | (check) | Clarity just installed | Victoria re-weight + skirting/bunnings negatives |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |

_Reference: `campaigns/adwords/craftons-change-log.md` (every ad change) · `architrave-page-cro-audit.md`
(page fixes) · `STATUS.md` (overall)._
