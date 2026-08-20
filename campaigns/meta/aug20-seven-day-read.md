# The 7-day read — 2026-08-20

_Every figure below was pulled live from the Meta API and the Shopify Admin API on 2026-08-20.
Nothing is quoted from memory or from an earlier session's notes._

---

## First, a correction to the last handoff

The previous session's handoff said **"v2 is PAUSED, nothing is spending on the test."** That was
wrong by the time it was written. The record:

- **Lee approved activation on 2026-08-17 at 10:43 UTC** — seven `marketing_approvals` rows,
  `approver = "Lee Patterson"`: one `activate_ad_set` and six `activate_ad`.
- v2 started delivering at **2026-08-17 19:54 Melbourne** and **has been live ever since**.
- LAW 1 was honoured exactly as designed. The approval trail is clean. The handoff note was stale,
  not the account.

**v1 was retired the same evening** and has spent $0 since 08-17.

---

## What the test actually did

**v2 ad set `120247812165960186`, live 2026-08-17 → now (~3.5 days):**

| | |
|---|---:|
| Spend | **$165.66** |
| Impressions | 17,056 |
| Link clicks (`inline_link_clicks`) | 574 |
| Link CTR | **3.36%** |
| Landing page views | 553 |
| Click → page load | **96.3%** |
| Add to cart | **9** |
| **InitiateCheckout** (the optimisation event) | **0** |
| Purchases | **0** |

**Per ad** — Meta has already picked a winner and starved the rest:

| Ad | Spend | LPV | ATC |
|---|---:|---:|---:|
| AD5 Chippies (Lawless photo) | $84.12 | 294 | 7 |
| AD4 Builders (Lawless photo) | $44.02 | 139 | 2 |
| AD6 Carpenters (Lawless photo) | $25.62 | 91 | 0 |
| AD1 Concreters (carousel) | $5.63 | 11 | 0 |
| AD2b Landscapers (carousel) | $4.12 | 8 | 0 |
| AD2 Landscapers (carousel) | $2.15 | 10 | 0 |

The three carousels never got a real audition — under 3% of spend between them. The three Lawless
photo ads are near-identical, which is exactly the Andromeda entity-collapse case: they competed
with each other and AD5 won.

---

## The number that decides this: TOF, all time

| Campaign | Spend | LPV | ATC | IC | Pixel purchases |
|---|---:|---:|---:|---:|---:|
| RadiusPro \| TOF \| Ardreagh \| Jul26 | $1,279.94 | 13,954 | 56 | 3 | **0** |
| RadiusPro \| TOF \| Aug26 (v1 + v2) | $369.18 | 1,159 | 17 | 1 | **0** |
| **Total** | **$1,649.12** | **15,113** | **73** | **4** | **0** |

**Shopify-traceable revenue from all TOF spend, ever: one order.** `#1280`, **$362**, 2026-08-10 —
first visit carried `utm_campaign=radiuspro_tof_jul26`, and even that order's *last* click was
retargeting.

$1,649 in, $362 out. That is not a noisy read any more. Three separate TOF campaigns across two
months agree with each other.

---

## The finding that matters more than the failure

The account already has a working machine, and it is being starved.

| Ad set | Lifetime spend | LPV | ATC | LPV→ATC | IC | ATC→IC | Purchases |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Retargeting — BOF** | $3,229.71 | 2,681 | 304 | **11.3%** | 127 | **41.8%** | **62** |
| TOF Jul26 | $1,279.94 | 13,954 | 56 | 0.40% | 3 | 5.4% | 0 |
| TOF Aug26 v1 | $203.52 | 606 | 8 | 1.32% | 1 | 12.5% | 0 |
| TOF Aug26 v2 | $165.66 | 553 | 9 | 1.63% | 0 | — | 0 |

Read the two right-hand columns. Cold traffic adds to cart at roughly a seventh of the rate warm
traffic does, and then **does not check out at all**. Warm traffic checks out 42% of the time.

**Retargeting is capped, not saturated:**

- Daily budget **$15**. It spends it, every day, and has since October 2025.
- **Frequency 1.6** over the last fortnight (range 1.29–2.03). A saturated audience runs 4–5+.
  At 1.6 there is real headroom.
- August 1–20: **$266.37 spend → 8 pixel purchases** ($33.30 each). Lifetime: **$52.09 per purchase**
  against a **$322 break-even**.
- Shopify agrees: three August orders carry `source=meta` UTMs — `#1286` $3,168, `#1280` $362,
  `#1273` $371 = **$3,901 traceable revenue on $266 of spend.**

So the account is spending **$65/day on the thing that returns $0.22 per dollar** and **$15/day on
the thing that returns roughly ten times its cost**, and the second one runs out of money every day.

---

## Two corrections to what I told you before

**1. Match quality — I nearly re-asserted an error that had already been withdrawn.**

Drafting this read, I pulled `match_rate_approx: -1` and `matched_entries: 0` off the pixel node and
started writing that match quality was "broken but not the cause". Before pushing, I found a parallel
session had already **withdrawn that root cause on 2026-08-17**, with better evidence than I had:

- `email` (332) and `phone` (212) arrive every day and have for 14+ days. 100% of `Purchase` events
  carry PII. CAPI is live at 7,831 server events.
- The original "only `external_id` arrives" reading came from **one hourly bucket** of a paginated
  endpoint, read as the whole window.
- **`match_rate_approx` and `matched_entries` do not measure Advanced Matching at all.** They report
  offline/customer-list upload matching, which this pixel has never used, and `-1` is Meta's
  "not applicable" sentinel. Quoting them as evidence of a fault is a category error — the one I was
  about to make for the second time.
- Lee's actual EMQ read: **InitiateCheckout 6.4, Purchase 8.3.** A pixel receiving only `external_id`
  scores 2–3.

**So: Advanced Matching was never broken. There is nothing to fix in Shopify. Do not reopen this.**

The substantive point survives and is stronger than when I thought the pixel was faulty: match
quality cannot explain 553 landing page views producing zero checkouts, because the signal path is
healthy and retargeting converts on it at 42% add-to-cart→checkout.

Worth noting on the record: **InitiateCheckout's 6.4 is below the Bible's >7 bar**, and launching on
it was logged at the time as a knowing deviation rather than a satisfied gate. It is a mild drag on
optimisation. It is not a 553-to-zero drag.

**2. Meta over-claims purchases by about 3×.**

Meta's account-level MTD reports **9 purchases / $13,608**. Shopify shows **3 orders carrying Meta
UTMs / $3,901** for August. Every ROAS figure from Meta's own reporting should be divided by roughly
three before it informs a decision.

---

## Verified, not assumed

- **Shopify's journey data does record Meta when Meta genuinely drives a click.** Checked against 60
  orders back to 2026-07-07: `#1286` (Instagram, `Retargeting Campaign - Bottom Of Funnel`), `#1280`
  (`radiuspro_tof_jul26` → `retargeting_radius_pro`), `#1273` (`radiuspro_retarget_jul26`), `#1264`
  (`source=ig`, organic). The channel is trackable, so **zero Meta orders in the test window is a
  real absence, not a tracking gap.** This is the check that makes the whole read trustworthy.
- Month-to-date account spend **$880.18** against the **$2,000** ceiling — no breach.
- v2 targeting: **AU only**, `countries: ["AU"]`. Correct.
- v2 `promoted_object`: `{pixel_id: 677437638374055, custom_event_type: INITIATED_CHECKOUT}` —
  the standard event, as rebuilt. The wiring fix worked; the audience is the problem.
- Custom conversion `27686282527680441` still returns **no `first_fired_time` field at all**. Still
  dead. Still do not reuse it.

---

## What is proposed (pending Lee's approval — nothing has touched the account)

| # | Change | approval_id |
|---|---|---|
| 1 | **Pause TOF v2** ad set `120247812165960186` | `d8391efe-4388-4b9e-9c5e-fb2e027dc5da` |
| 2 | **Retargeting $15 → $18/day** ad set `120233074187690186` | `25d9597c-3363-4e23-8e95-f933ead563a6` |

Proposal 2 is +20% because that is the largest single step `MAX_BUDGET_INCREASE_FRACTION` allows —
bigger jumps reset Meta's learning. The ladder from here is $18 → $21.60 → $25.90 → $31.10, one step
per week, each one held only if cost-per-purchase stays under $322.

This is the process the monitoring plan already specifies: *"Propose pausing zero-result ads. Lee
approves."* Rung 0 is report-and-propose. Neither change has been applied.

---

## Why pausing TOF is the right call and not an over-reaction to 3.5 days

The standing rule is **never kill on "zero results" when results cannot be counted** — that is why
the kill rule was refused twice in the previous fortnight. It does not protect v2, because the
measurement now works:

- v2 optimises on **standard `InitiateCheckout`**, which fires site-wide (19 account-wide in August).
- Shopify journey attribution demonstrably captures Meta clicks.

Results *can* be counted. They are zero. And the decision does not rest on 3.5 days alone — it rests
on **$1,649 of TOF spend across three campaigns and two months producing one $362 order**.

**What is worth keeping:** v2's creative beat July's by **4× on LPV→ATC** (1.63% vs 0.40%). The
creative work was not wasted and the Lawless site photo is still the best asset in the account. The
failure is structural — there is nothing between "add to cart" and "check out" for a cold trade
buyer on a $600+ configured product — not a copy or image problem. Re-running the same structure
with new pictures would buy the same result.

---

## What to do after the pause — the actual argument

Do not simply move $65/day into retargeting. The 20% ladder means retargeting can only absorb about
$3/day more this week, and its pool is fed by *all* site traffic, most of which is Google SEO
(6 of the last 10 orders). Turning TOF off does not drain it quickly.

The open question is the one from `launch-readiness.md` that was flagged as "not blocking" and has
now become the whole problem:

> July put ~13,000 people on the page and captured **zero**.

15,113 cold visitors have now been bought across all TOF spend, and there is still no way to reach
any of them again except via a 180-day pixel window. **The next build is capture, not creative** —
something that turns a cold click into an address we own. Until that exists, TOF is renting traffic
and throwing away the part that does not buy on the first visit.

That is a decision for Lee, not a change to propose. It is the thing that would make TOF viable
rather than the thing that would make it prettier.
