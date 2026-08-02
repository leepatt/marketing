# Meta Ads audit — Craftons — 2026-08-02

_Account: `act_1650412872259063` (Craftons, AUD) · Pixel: `677437638374055`_
_Pulled live from the Meta Marketing API + Shopify analytics on 2026-08-02. All figures AUD._

**Verdict: yes, this is concerning — but it's the fixable kind.** Sales didn't just fail to rise;
they fell. And there is a clear mechanical cause, not a market cause.

---

## 1. The weekend (Sat 1 – Sun 2 Aug)

| Campaign | Spend | Clicks | Add-to-cart | Checkouts | Purchases |
|---|---|---|---|---|---|
| RadiusPro \| TOF \| Ardreagh \| Jul26 | $129.75 | 1,974 | 21 | 0 | **0** |
| Retargeting — Bottom Of Funnel | $109.48 | 178 | 13 | 3 | 1 ($371) |
| **Total** | **$239.23** | 2,152 | 34 | 3 | **1** |

Shopify actually recorded 2 orders across those two days ($595.45 gross). One of them matches the
Meta-attributed $371 retargeting purchase.

**Weekends are structurally dead for this business.** Across the four weekends before the ads
started (Jul 4–5, 11–12, 18–19, 25–26) Shopify recorded **1 order in 8 days**. Builders, chippies and
concreters buy Tuesday–Thursday. Spending $239 over a weekend on a trade audience is poor timing
regardless of how the ads are built.

---

## 2. The bigger problem: sales went down, not flat

| | Jul 4–21 (18d, pre-ads) | Jul 22 – Aug 2 (12d, ads live) | Change |
|---|---|---|---|
| Orders | 26 | 10 | — |
| Orders / day | 1.44 | 0.83 | **−42%** |
| Gross sales | $32,308 | $7,112 | — |
| Gross / day | $1,795 | $593 | **−67%** |
| Sessions / day | 86 | 1,255 | **+1,360%** |
| Cart adds / day | 2.56 | 2.33 | **−9%** |
| Conversion rate | 1.49% | 0.066% | **−96%** |

This is the whole audit in one line: **traffic went up ~15x and cart additions did not move at all.**
15,058 sessions in 12 days produced 28 cart additions. The pre-ad site did 1,541 sessions and
produced 46.

Shopify's own order attribution over 30 days: **14,427 sessions from Facebook + Instagram →
2 orders, $398.18 gross.** Total Meta spend over the same live window: **$1,711.48.**

> Caveat, stated plainly: order volume here is low and lumpy (single orders swing $4–8k), so the
> revenue drop is partly noise. The session-to-cart collapse is *not* noise — that sample is large.

---

## 3. Root causes, ranked

### 3.1 Conversion tracking was dead for the first 8 days — $985 burned blind

Daily ViewContent / AddToCart on the RadiusPro campaign:

```
2026-07-22   spend $ 63.72   lpv   678   view_content   0   atc  0
2026-07-23   spend $ 89.45   lpv   816   view_content   0   atc  0
2026-07-24   spend $108.80   lpv 1,478   view_content   0   atc  0
2026-07-25   spend $106.38   lpv 1,698   view_content   0   atc  0
2026-07-26   spend $134.21   lpv 1,968   view_content   0   atc  0
2026-07-27   spend $151.53   lpv 1,921   view_content   0   atc  0
2026-07-28   spend $168.54   lpv 2,023   view_content   0   atc  0
2026-07-29   spend $162.06   lpv 1,826   view_content   0   atc  0
2026-07-30   spend $ 83.84   lpv   557   view_content 670   atc  8   <- tracking starts working
2026-07-31   spend $ 78.72   lpv   365   view_content 760   atc 27
2026-08-01   spend $ 43.80   lpv   198   view_content 426   atc  6
2026-08-02   spend $ 85.95   lpv   412   view_content 889   atc 15
```

**$984.69 — 77% of the campaign's total spend — ran with zero conversion signal reaching Meta.**
The pixel itself was healthy the whole time (site-wide it was firing ~16–18 ViewContent/hour on
Jul 20, before launch), so this was a campaign-level attachment problem, not a broken pixel.

The mismatch that caused it is still in place:

- **Campaign objective:** `OUTCOME_TRAFFIC` (reports as `LINK_CLICKS`, `optimization_goal: NONE`)
- **Ad set claims:** `OFFSITE_CONVERSIONS`, `promoted_object: {pixel, custom_event_type: ADD_TO_CART}`

A Traffic campaign buys the cheapest clicks it can find. That is exactly what it did, and it is
exactly what we got.

### 3.2 Reels ate 72% of spend and returned nothing

Placement breakdown, RadiusPro, Jul 22 – Aug 2:

| Placement | Spend | Clicks | CTR | LPV | ViewContent | ATC | Purchases |
|---|---|---|---|---|---|---|---|
| Facebook Reels | $621.81 | 8,294 | 9.53% | 7,909 | 428 | 3 | 0 |
| Instagram Reels | $297.51 | 3,437 | 8.39% | 3,367 | 163 | 4 | 0 |
| Facebook Feed | $238.09 | 6,904 | 19.38% | 1,598 | 1,693 | 40 | 0 |
| Marketplace | $82.17 | 826 | 3.65% | 822 | 307 | 9 | 0 |
| Instagram Feed | $14.44 | 59 | 4.46% | 60 | 49 | 0 | 0 |
| Search | $9.41 | 116 | 1.68% | 104 | 21 | 0 | 0 |

**Reels = $919.32 (72% of spend) → 7 add-to-carts, 0 purchases.**

A 10% CTR at a **$0.065 CPC** is not enthusiasm — that is the signature of accidental taps in a
vertical video feed. The proof is in the drop-off: on Facebook Reels only **428 of 7,909 landing page
views (5.4%)** stayed long enough to fire ViewContent. They tapped, the page began loading, they
swiped away.

Feed and Marketplace are the only placements showing real intent — $320 of spend produced 49 of the
56 add-to-carts (88%) off 12% of the clicks.

### 3.3 The junk traffic poisoned the one campaign that was making money

The Bottom-Of-Funnel retargeting campaign targets `All Website Visitors – 30/60/180 Days` and
`Add To Cart (No Purchase) – 30/60/180 Days`.

| Window | Spend | Purchases | Revenue | ROAS |
|---|---|---|---|---|
| Jul 8–21 (before TOF launch) | $207.15 | 9 | $12,797 | 61.8 |
| Jul 22 – Aug 1 (after TOF launch) | $316.64 | 1 | $3,266 | 10.3 |

Purchases fell from **0.64/day to 0.09/day (−86%)** while spend rose 50%. The mechanism is
straightforward: before the TOF campaign the 30-day visitor pool was ~2,500 genuine prospects.
The TOF campaign then poured **14,400 Reels mis-tappers** into that same pool, so the retargeting
audience is now roughly **85% junk**. We are paying to re-serve ads to people who never meant to
visit in the first place.

Worse, the budget was scaled **4x into the poisoned pool** exactly when it was at its worst
(Jul 28 $32 → Jul 30 $64 → Jul 31 $65).

> ROAS caveat: the 61.8 pre-figure is inflated by two large orders ($4,304 on Jul 10, $5,475 on
> Jul 21), and retargeting ROAS is always over-credited — 7-day click attribution on people who were
> already going to buy. The *direction and magnitude* of the fall is the signal, not the absolute number.

### 3.4 The purchase-optimised ad set is switched off

Inside the BOF campaign:

- `Retargeting — Bottom Of Funnel – Purchase` → **PAUSED** ($12.50/day)
- `Retargeting — Bottom Of Funnel – Add To Cart` → **ACTIVE** ($60/day)

The only live bottom-funnel ad set optimises for **Add To Cart**, not Purchase. On a site with a
~$1,200 AOV and a considered B2B purchase, add-to-cart is a weak proxy — and it is the event most
easily gamed by low-intent traffic.

### 3.5 Advantage Audience is leaking spend to people who will never buy

Ad set `TOF | Broad AU | AddToCart`: age 25–65, all of Australia, `advantage_audience: 1`.

| Segment | Spend | Clicks | ATC | Purchases |
|---|---|---|---|---|
| 35–44 male | $271.19 | 4,646 | 19 | 0 |
| 25–34 male | $270.96 | 4,585 | 20 | 0 |
| 45–54 male | $193.88 | 3,086 | 12 | 0 |
| 65+ male | $179.92 | 2,456 | 5 | 0 |
| 55–64 male | $166.13 | 2,453 | **0** | 0 |
| All female segments | $171.52 | 2,160 | **0** | 0 |
| 65+ female | (incl. above) $42.26 | 437 | **0** | 0 |

**$337.65 went to 55–64 male, 65+ female and all-female segments for 0 add-to-carts.** Note the ad
set is capped at age 65 — the $222 of 65+ spend is Advantage Audience overriding the targeting.

### 3.6 The ad set never left learning phase

56 add-to-carts in 12 days ≈ 4.7/day. Meta needs ~50 optimisation events **per week** per ad set to
exit learning. It was never going to stabilise — and for 8 of those 12 days it was receiving zero
events at all.

---

## 4. What is actually working

Worth saying clearly, because not all of this is bad:

- **The creative is not the problem.** Six trade-specific ads (concreters, landscapers, builders,
  chippies, carpenters), all pointing at a correct, healthy landing page
  (`craftons.com.au/products/radius-online`, HTTP 200, 1.5s, UTMs properly tagged per-ad). Feed
  placement pulled a 19% CTR. The angle — *"Any architect can draw a curve. Now any chippy can frame
  one."* — is landing.
- **Retargeting genuinely converts** when the pool is clean. That is the engine to protect.
- **The landing page works.** Pixel present, page fast, no errors, no redirect chain.

The failure is in **campaign structure and measurement**, not in the ads themselves.

---

## 5. Recommended actions

Nothing below has been executed — these are account changes and need Lee's sign-off.

**Immediately (stop the bleeding)**

1. **Pause `RadiusPro | TOF | Ardreagh | Jul26`.** It has spent $1,277 for 0 purchases and is
   actively degrading the retargeting audience. Every extra day makes the pool worse.
2. **Un-pause the `Bottom Of Funnel – Purchase` ad set**, pause the `Add To Cart` ad set. Optimise
   for the thing we actually want.
3. **Cut BOF daily budget back to ~$15–20/day** until the audience pool recovers. It was working at
   that level; the 4x scale-up is what broke it.

**Before relaunching TOF**

4. **Rebuild it as `OUTCOME_SALES`**, not `OUTCOME_TRAFFIC`. The current objective/ad-set mismatch
   is the root cause and cannot be fixed by editing the existing campaign — the objective is locked
   after creation.
5. **Exclude Reels, Audience Network and Stories.** Manual placements: Facebook Feed, Instagram Feed,
   Marketplace only. That is where 88% of the add-to-carts came from off 12% of the clicks.
6. **Turn Advantage Audience off**, tighten to male 25–54, and layer trade interests / job titles.
7. **Verify the pixel is attached and firing *before* spend starts** — check ViewContent and
   AddToCart both register in Events Manager on day one. This audit exists because nobody checked.
8. **Optimise for a mid-funnel event** (InitiateCheckout or a Quote/Configurator submit) rather than
   Purchase — at ~1 purchase/day the account cannot feed a purchase-optimised algorithm.

**Rebuild the audiences**

9. **Rebuild retargeting off clean signals** — `ViewContent` + `AddToCart` + configurator engagement,
   not `All Website Visitors`. Ideally exclude the Jul 22–Aug 2 visitor cohort entirely.
10. **Add a dayparting schedule**: Mon–Fri, roughly 6am–6pm. Weekends have produced 3 orders in
    10 days of data. Stop paying for them.

**Measurement**

11. Match Meta's claimed conversions against Shopify weekly. Meta claimed 2 purchases / $3,637 from
    retargeting; Shopify attributes 2 orders / $398 to all of Facebook + Instagram over 30 days.
    That gap needs watching before any decision gets made on Meta's numbers alone.

---

## 6. Open questions for Lee

- **Who is Ardreagh, and who owns this account?** The campaign naming (`Ardreagh carousel`) suggests
  an external agency built the TOF campaign. If so, they launched a Traffic-objective campaign with
  no working conversion tracking and scaled it — that conversation needs having.
- **Was anything changed on Jul 30?** Tracking started working that day. Knowing what changed tells
  us whether it's actually fixed or just intermittently reporting.
- **Was the BOF budget scale-up on Jul 28–31 deliberate?** It went into the worst possible moment.
- **Is $70/day the agreed TOF budget?** It is running at $70/day against a BOF campaign that was
  producing 62x ROAS on $15/day.

---

_Data sources: Meta Marketing API v21.0 (`/insights` at campaign, ad set, ad, placement and
demographic level; `/stats` on pixel 677437638374055) · Shopify Analytics (`sales`, `sessions`,
referrer attribution) · live HTTP check of the landing page._
