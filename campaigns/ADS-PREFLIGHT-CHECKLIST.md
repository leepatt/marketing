# Ads pre-flight checklist — complete BEFORE any real money is spent

_Applies to **all** paid advertising: Meta (Facebook/Instagram), Google Ads, anything else._
_Created 2026-08-02 after the Meta ads post-mortem (`POST-MORTEM-2026-08-02.md`)._

---

## How this is used

**Claude must complete this checklist and paste the filled-in copy to Lee BEFORE any campaign is
switched on. Lee approves it. Only then does money get spent.**

Rules for filling it in:

- Every box needs **evidence**, not a tick. "Yes" is not an answer — "yes, verified, here's the
  number" is.
- **Any single ❌ in Section B or E blocks launch.** No exceptions, no "we'll fix it once it's
  running." That's exactly what cost $985 in July.
- If something can't be verified, it is a ❌. "Probably fine" is a ❌.
- Copy this file to `campaigns/<channel>/preflight-<campaign-name>.md` and fill that copy in, so
  there's a permanent record of what was checked and when.

---

## Section A — What are we actually trying to do

| # | Check | Evidence needed |
|---|---|---|
| A1 | What is the **one** outcome this campaign exists to produce? | Write it as a number: "orders of Radius Pro" — not "awareness" or "traffic" |
| A2 | What is that outcome worth? | Average order value, so we know what we can afford to pay for one |
| A3 | What's the most we'll pay to get one? | A dollar figure agreed before launch |
| A4 | What does the last 30 days look like **without** ads? | Baseline orders/day and sales/day from Shopify — otherwise we can't tell if ads changed anything |

> **Why A4 matters:** in July we had no agreed baseline, so "sales look flat" was arguable for
> two weeks. With a baseline it's a fact on day three.

---

## Section B — Tracking (⛔ ANY ❌ HERE BLOCKS LAUNCH)

**This is the section that failed in July. $985 was spent blind because nobody ran these four checks.**

| # | Check | Evidence needed |
|---|---|---|
| B1 | Is the tracking code (pixel) installed on the site? | Confirmed present on the actual landing page |
| B2 | Is it **firing right now**? | A real event seen in the last 24 hours — a number, not an assumption |
| B3 | Is it firing the **purchase** event specifically? | A real order appearing in the ad platform's event tool. Not page views — purchases |
| B4 | Is the tracking **connected to this specific campaign**? | The campaign's own reporting shows conversion columns populated, not blank |

> **B4 is the one that got us.** The pixel was healthy site-wide the entire time — firing 16–18
> events an hour. It just wasn't reporting into *that campaign*. A site-wide green light is not
> proof. Check the campaign itself.

**How to verify:** Meta Ads Manager → Events Manager → select the pixel → Test Events / Overview.
You want to see PageView, ViewContent **and Purchase** with counts against them in the last 24h.

---

## Section C — Campaign setup

| # | Check | Evidence needed |
|---|---|---|
| C1 | Is the objective **Sales / Conversions** — not Traffic, Engagement, Awareness or Reach? | The objective as shown in the platform |
| C2 | Does the ad-set-level goal **match** the campaign objective? | Both should say the same thing |
| C3 | Are placements **manual**, with Reels / Stories / Audience Network switched OFF? | The placement list |
| C4 | Is audience expansion ("Advantage Audience" / broad match) OFF for the first test? | Setting confirmed |
| C5 | Is the audience specific enough to be plausible buyers? | Age, location, interests written out |
| C6 | Does the schedule match when customers actually buy? | Weekdays for trade. Weekends produced 1 order in 8 days |

> **C1 and C2 are the July failure.** The campaign said Traffic while the ad set claimed to chase
> conversions. **You cannot change the objective after a campaign is created** — it has to be rebuilt.
> Get it right first time.

---

## Section D — Where the click lands

| # | Check | Evidence needed |
|---|---|---|
| D1 | Does the destination page load? | HTTP 200, checked today |
| D2 | Does it load fast? | Under ~3 seconds |
| D3 | Is it the **specific product page**, not a homepage or "all products" list? | The actual URL |
| D4 | Can someone actually buy or enquire on that page without hunting? | Checked on a phone, not just desktop |
| D5 | Are UTM tags on the link so Shopify can attribute the order? | The tagged URL |

> One of the ads found in the account pointed at `/collections/all` — a generic product list. It had
> spent $125 and produced zero sales in its lifetime.

---

## Section E — Money safety (⛔ ANY ❌ HERE BLOCKS LAUNCH)

| # | Check | Evidence needed |
|---|---|---|
| E1 | Is the starting budget **$10–20/day**, not more? | The figure |
| E2 | Is there a **total cap** agreed for the test? | e.g. "$200 total, then stop and review" |
| E3 | Is the **kill rule written down before launch**? | e.g. "if 0 orders by $200 spent, it stops" |
| E4 | Is the **review date in the calendar**? | Day 2 and day 7, specific dates |
| E5 | Will this campaign feed the retargeting list — and is that acceptable? | If it's untested cold traffic, it must be excluded |

> **E3 is the most important line in this document.** Decide what failure looks like *before* you're
> emotionally invested and money is already gone. In July there was no kill rule, so the campaign
> ran 12 days and got its budget increased while producing nothing.

> **E5 is the one nobody thinks of.** It's how a bad campaign broke the good one. Cold traffic
> should be excluded from retargeting audiences until it's proven to contain real buyers.

---

## Section F — Go / no-go

Only after Sections A–E are complete with evidence:

- [ ] Every box in **Section B** is ✅
- [ ] Every box in **Section E** is ✅
- [ ] Baseline Shopify numbers recorded — orders/day and sales/day for the last 30 days
- [ ] Kill rule and review dates written down
- [ ] **The campaign as actually built has been checked line by line against the approved brief** —
      placements, formats, audience, destination. Every deviation justified in writing or corrected.
- [ ] **Lee has seen this filled-in checklist and said go**

> **Why the brief check is its own line:** in July there *was* an approved brief (Drive
> `02 Strategy/META-ADS-BRIEF.md`). It specified static images in feed. What ran was 72% Reels video.
> Nobody compared the built campaign to the plan, so the gap went unnoticed for twelve days.

Launched by: ............... Date: ............... Approved by: ...............

---

## Section G — After launch (this is not optional)

### Day 2 check — the "is it real" check

Do not look at clicks. Open Shopify.

| Check | What good looks like | What means STOP |
|---|---|---|
| Sessions from the ad channel | going up | — |
| **Cart additions** | going up roughly in proportion | **flat while visits climb = the traffic is worthless. Stop now.** |
| Conversion rate | roughly holding | collapsing toward zero = stop |
| Conversions showing in the ad platform | some number appearing | **still blank = tracking is broken. Pause immediately.** |

> **This exact check on 24 July would have caught everything, at a cost of about $260 instead of
> $1,711.** Visits had already gone from 86/day to 1,671/day while cart additions sat at 5.

### Day 7 check — the "is it working" check

- Orders in **Shopify** attributed to this channel — the actual number
- Cost per order = spend ÷ orders. Compare to the figure agreed in A3
- Apply the kill rule from E3 **as written**. Don't renegotiate it now

### The one question that catches everything

Whenever Claude reports that an ad is performing, Lee asks:

> ### "How many orders in Shopify?"

If the answer is clicks, reach, impressions, engagement, CTR or cost-per-click — **the answer is
none, and the campaign is not working.** No exceptions.

---

## Red flags — recognise these on sight

These all looked like success in July. Every one was a warning.

| Signal | What it feels like | What it usually means |
|---|---|---|
| CTR above 3% on a cold audience | "people love the ad" | accidental taps |
| Cost per click under 20c | "incredible value" | you've bought people who aren't paying attention |
| Huge landing page views, few product views | "loads of interest" | they bounced before the page loaded |
| Conversions showing 0 after real spend | "early days yet" | **tracking is broken — assume this until proven otherwise** |
| Website visits up, Shopify baskets flat | "top of funnel is working" | the traffic is worthless |
| A campaign doing well enough to scale | "let's push more budget in" | check it has produced actual **orders** first, not add-to-carts |

**July's numbers for reference:** 10% CTR, 6.5c CPC, 13,940 landing page views, 2,745 product views,
0 purchases, $1,277 spent. Every metric except the last two looked like a triumph.

---

## Reference numbers (update as these change)

| | Figure | Source |
|---|---|---|
| Baseline orders/day, no ads | 1.44 | Shopify, 4–21 Jul 2026 |
| Baseline sales/day, no ads | $1,795 | Shopify, 4–21 Jul 2026 |
| Baseline site visits/day, no ads | 86 | Shopify, 4–21 Jul 2026 |
| Baseline conversion rate | ~1.5% | Shopify |
| Typical order value | ~$1,200 | Shopify |
| Retargeting when healthy | 9 orders / 2 weeks on ~$15/day | Meta, 8–21 Jul 2026 |
