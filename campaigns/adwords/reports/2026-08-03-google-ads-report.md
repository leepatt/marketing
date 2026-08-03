# Google Ads report — Craftons

_Account: **Craftons Google Ads account** (310-491-2421) · AUD · Australia/Melbourne_
_Pulled live from the Google Ads API on 2026-08-03 via `tools/google-ads.mjs`._
_Windows: **since launch = 1 Jul – 2 Aug 2026** (33 days) · **last 30 days = 4 Jul – 2 Aug**._

---

## TL;DR

1. **The campaigns are live and spending.** They went live 1 July (not "built, awaiting deploy" as
   `STATUS.md` said). $1,601.71 spent since launch, ~$48.54/day.
2. **They're not paying for themselves yet:** 4 conversions total — 3 lead forms + 1 purchase
   ($1,265 revenue). That's **0.79x ROAS** and **$400 per conversion**.
3. **The bigger issue: the account's revenue engine was switched off the day before.** The Cavity
   Battens Performance Max campaign last spent **29 June**. In June it turned $1,171 into **$9,044
   of tracked revenue (7.7x ROAS)** plus 78 lead forms — and its ROAS had climbed five months
   straight. Since 1 July it has spent $0 and returned $0.
4. **Root cause of the high CPCs is Quality Score.** 69% of spend sits on keywords scoring **1–3/10**.
   That's what's holding CPCs at ~$5.80 while the one QS-7 keyword clicks at $2.98.
5. **Radius Pro is the single worst line item** — $555.44, 97 clicks, **zero** conversions.

---

## 1. Since launch (1 Jul – 2 Aug 2026)

| Metric | Value |
|---|---|
| Spend | **$1,601.71** |
| Impressions | 3,974 |
| Clicks | 316 |
| CTR | 7.95% |
| Avg CPC | $5.07 |
| Conversions | **4** (3 lead forms + 1 purchase) |
| Tracked revenue | $1,265.00 |
| ROAS | **0.79x** |
| Cost per conversion | $400.43 |
| Daily run rate | $48.54/day (~$1,476/mo) |

**By campaign**

| Campaign | Started | Budget/day | Spend | Clicks | Avg CPC | Conv | Revenue |
|---|---|---|---|---|---|---|---|
| Craftons – Customised Building Products | 1 Jul | $50 | $1,177.55 | 209 | $5.63 | 3 | $1,265 |
| Craftons – Curved Architraves | 8 Jul | $100 | $424.16 | 107 | $3.96 | 1 | $0 |
| Cavity Battens – Performance Max | (paused) | $40 | $0.00 | 0 | — | 0 | $0 |

**By ad group**

| Ad group | Spend | Clicks | Conv | Verdict |
|---|---|---|---|---|
| Radius Pro | $555.44 | 97 | **0** | Worst performer — biggest spend, no return |
| Curved Bench Seat / Formwork | $429.68 | 75 | 2 | Best converter |
| Curved Architraves (own campaign) | $424.16 | 107 | 1 | OK, cheapest clicks |
| Curved Architraves (in main campaign, now paused) | $192.44 | 37 | 1 | Duplicate — correctly paused |

Week on week is flat: 20–26 Jul $304.17 / 66 clicks / 1 conv → 27 Jul–2 Aug $310.00 / 65 clicks /
**0 conv**. No trend improvement yet.

---

## 1a. How the month actually played out

| Date | Event |
|---|---|
| 29 Jun | Cavity Battens PMax spends for the last time |
| 1 Jul | "Customised Building Products" goes live, $50/day |
| 2 Jul | The single purchase — $1,265 |
| 8 Jul | "Curved Architraves" built (campaign + budget + ad group + ad + 47 keywords + 27 negatives); duplicate Architraves ad group in the main campaign paused |
| 11 Jul | 2 negatives added — **last change made to the account** |
| 13 / 15 / 23 Jul | Three lead-form submissions |
| 23 Jul → 3 Aug | No conversions for 11 days |

**Nobody has touched the account since 11 July** — 23 days of unattended spend (per `change_event`).

**Weekly trend**

| Week | Spend | Clicks | Avg CPC | Conv |
|---|---|---|---|---|
| 6 Jul | $421.35 | 73 | $5.77 | 0 |
| 13 Jul | $304.45 | 61 | $4.99 | 2 |
| 20 Jul | $304.17 | 66 | $4.61 | 1 |
| 27 Jul | $310.00 | 65 | $4.77 | 0 |

Blended CPC improved only because Architraves warmed up ($5.72 → $3.04). The main campaign is pinned
at **$5.13 / $5.80 / $5.74 / $5.84 / $5.82** — dead flat, i.e. Manual CPC paying its maximum bid on
essentially every click. That's the signature of weak Ad Rank being topped up with money.

**Last 10 days:** $115.70, 21 search terms, **zero conversions** — and ~35% of it on terms that could
never convert (`curved beading` $12.00, `curved banquette` $11.40, `intrim` $11.04, `scallop mdf
panel` $5.99). The real money terms `curved architrave` + `curved architraves` drew $7.07 between them.

---

## 2. The Performance Max shutdown — the headline

The "Cavity Battens" PMax campaign is **paused**, last spend **29 June 2026**. The new search
campaigns started **1 July**. In effect one was swapped for the other.

**What PMax was doing (purchases only — junk page-view conversions excluded):**

| Month | Spend | Purchases | Revenue | ROAS |
|---|---|---|---|---|
| Feb 2026 | $1,216.44 | 2.0 | $1,078 | 0.89x |
| Mar 2026 | $1,216.80 | 4.0 | $1,353 | 1.11x |
| Apr 2026 | $1,191.56 | 1.3 | $2,818 | 2.36x |
| May 2026 | $1,217.32 | 10.7 | $6,093 | 5.00x |
| **Jun 2026** | **$1,171.14** | **6.0** | **$9,044** | **7.72x** |
| **Feb–Jun total** | **$6,013.26** | **24.0** | **$20,386** | **3.39x** |

June also produced **78 lead-form submissions** at ~$15 each.

Set against the replacement: search has produced **1 purchase / $1,265 / 0.79x** in 33 days.

**Caveat, stated plainly:** these sell different things — PMax pushed Cavity Battens, search pushes
the curved range — so it isn't a like-for-like swap, and search is only a month old with tiny
conversion volume. But a campaign compounding toward 7.7x ROAS was turned off, and nothing has
replaced that revenue. Worth a deliberate decision rather than leaving it off by default.

---

## 3. Quality Score is what's making clicks expensive

Spend by Quality Score, enabled keywords, last 30 days:

| QS | Keywords | Spend | Share |
|---|---|---|---|
| 1 | 16 | $427.32 | 29% |
| 2 | 7 | $153.37 | 10% |
| 3 | 16 | $422.46 | 29% |
| 4 | 2 | $29.14 | 2% |
| 5 | 12 | $178.52 | 12% |
| 6 | 2 | $23.19 | 2% |
| 7 | 2 | $17.91 | 1% |
| (no score) | 51 | $208.75 | 14% |

**69% of spend sits on QS 1–3 keywords.** The effect is direct and visible:

- `curved architrave` (EXACT, **QS 7**) → **$2.98** CPC
- `curved mdf`, `bendy ply`, `flexible plywood`, `curved molding`, `archway moulding` (**QS 1**) →
  **$5.61–$5.96** CPC

Impression share confirms it isn't a money problem, it's a relevance problem:

| Campaign | Impr. share | Lost to budget | Lost to rank |
|---|---|---|---|
| Customised Building Products | 40.32% | 20.55% | **39.13%** |
| Curved Architraves | 32.07% | **0.00%** | **67.93%** |

The Architraves campaign has a **$100/day budget and spends $16/day** — it loses two-thirds of its
impressions purely to Ad Rank. Raising budget there would do nothing.

---

## 4. Radius Pro: buying the wrong intent

$555.44, 97 clicks, 0 conversions. The search terms show why:

`bendable plywood` · `flexible plywood` · `bendy plywood` · `bendable ply` · `3mm bendy plywood` ·
`flexible mdf` · `bending plywood near me`

`brand/keyword-plan.md` already flagged this exact risk:

> ⭐ Lead with "bendy ply". Confirmed lead-generator… But the *product* is **Radius Pro** (curved,
> cut-to-size); **we don't stock flat bendy sheets**, so ads/pages land on Radius Pro and reframe:
> "we cut the curve for you".

The reframe isn't landing. These searchers want a flat flexible sheet to bend themselves; Radius Pro
is a finished curved component. Google agrees — it scores those keywords **QS 1**, which means it
reads `/products/radius-online` as a poor answer to "bendy plywood". Ad strength on one Radius Pro
ad is **POOR**.

Note "bendy ply" is listed as a confirmed converter historically — so the term does work; it's the
current page/ad framing against it that isn't.

---

## 5. Wasted spend still live

Negatives are properly applied (84 phrase negatives on the main campaign, 23 broad on Architraves),
and the July `bunnings` / `skirting` leaks stopped after they were added. These are still leaking:

| Search term | Cost | Last seen | Issue |
|---|---|---|---|
| `intrim mouldings` / `intrim` / `intrim architraves` | **$28.54** | 2 Aug | Competitor brand — **we're bidding on these on purpose** as EXACT keywords. QS 1, 0 conversions. |
| `curved banquette` | $11.40 | 2 Aug | Furniture intent |
| `curved beading for bottom of stairs` | $12.00 | 30 Jul | Wrong product |
| `curved booth seating` / `curved seating` / `curved metal bench seat` | $22.80 | Jul | Furniture / wrong material |
| `plywood circle 36 inch` / `circle plywood` / `scallop mdf panel` | $17.86 | 26 Jul | Wrong product, imperial units = likely offshore |
| `door archway kit` / `archway doors interior` | $11.88 | Jul | Doors, not architraves |
| `formatube suppliers melbourne` | $5.92 | 8 Jul | Competitor product brand |

Roughly **$110 (7% of spend)** on traffic that was never going to buy.

Geo is clean — 100% of spend in Australia, no offshore leakage.

---

## 6. Devices

| Device | Spend | Share | Clicks | CTR | Conv |
|---|---|---|---|---|---|
| Mobile | $888.16 | 61% | 182 | 7.50% | 1 |
| Desktop | $541.41 | 37% | 98 | 7.95% | **2** |
| Tablet | $31.09 | 2% | 6 | 14.29% | 0 |

Desktop converts about 3x better per dollar. Volume is too small to act on hard, but worth watching —
if it holds, a mobile bid adjustment is the lever.

---

## 7. Conversion tracking — healthy

| Action | Category | Primary? | Lifetime |
|---|---|---|---|
| Google Shopping App Purchase | PURCHASE | **Primary** | 27 |
| Craftons (web) form_submit | SUBMIT_LEAD_FORM | **Primary** | 446 |
| Craftons (web) form_start | ENGAGEMENT | secondary | 651 |
| Craftons (web) file_download | ENGAGEMENT | secondary | 73 |
| Google Shopping App Page View / View Item | PAGE_VIEW | secondary | 159,362 |

Tracking is instrumented correctly and the `file_download` demote flagged in `STATUS.md` is **already
done** (it's secondary). One gap: **lead forms carry a $1 placeholder value**, so the account can't
optimise toward lead *quality* — only lead count. Purchases do carry real revenue.

---

## 8. Recommended actions

**Decide first (needs Lee):**
1. **Restart Cavity Battens PMax?** It was at 7.7x ROAS and climbing when it stopped. If the pause was
   deliberate (stock, margin, focus), fine — but it should be a decision, not a side effect of the
   search launch. This is the single biggest revenue lever in the account.

**Fix now (low risk, ~$110/mo recovered):**
2. Add negatives: `banquette`, `booth`, `seating`, `beading`, `door`, `doors`, `kit`, `circle`,
   `circles`, `scallop`, `inch`, `formatube`.
3. **Stop bidding on `intrim`** — competitor brand, QS 1, $28.54, zero conversions. Remove
   `intrim mouldings` and `intrim architraves` as keywords, add `intrim` as a negative.

**Fix this week:**
4. **Radius Pro** — pause the POOR ad, rewrite ads to answer "bendy ply" intent head-on ("we cut the
   curve — no bending required"), or add a section to `/products/radius-online` that addresses flat
   bendy sheets directly. $555 with zero return can't continue as is.
5. **Move budget** from Architraves ($100/day, spends $16, loses 68% to rank) to the main campaign
   (loses 20.55% to budget). Budget is in the wrong place.
6. **Cap max CPC around $4.00** on the main campaign. It's Manual CPC sitting at $5.63 — the same
   uncapped-bid pattern that was fixed on CNC Cut ($6.45 → capped $3.50).

**Fix over the month:**
7. **Quality Score work** — 69% of spend on QS 1–3. Tighter ad-group-to-landing-page match; each
   ad group should point at a page that uses the searcher's words.
8. **Give lead forms a real value** (even a rough $ per qualified lead) so bidding can optimise for
   quality, not count.

---

## How this was produced

`tools/google-ads.mjs` — read-only Google Ads API client built this session (the tool sketched in
`api-tool-design.md`). API access is **working**; Basic access is evidently granted.

```bash
node tools/google-ads.mjs accounts              # list accessible accounts
node tools/google-ads.mjs report --days 30      # full markdown report
node tools/google-ads.mjs raw "SELECT ..."      # arbitrary GAQL
```

Read-only by design — no write path exists in the tool, so it cannot change the account.

**Account structure finding** (answers an open question in `STATUS.md`): MCC **Craftons Marketing
(275-347-3695)** has **no child accounts**. The Craftons advertiser account **310-491-2421** is
granted **directly** to the OAuth user, not through the MCC — so calls must omit the
`login-customer-id` header (the tool handles this automatically). **CNC Cut is not in this account
and is not reachable with these credentials** — its campaigns are elsewhere.
