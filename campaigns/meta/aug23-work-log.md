# Session 2026-08-23 — A1 / B1 / C1 / D1

_Lee chose A1, B1, C1, D1 from the options list. This records what each turned into once checked
against live data. Two of the four were not what they looked like._

---

## ⏱ First: the 7-day read was three days stale

The read was pulled **2026-08-20**; Lee replied **2026-08-23**. TOF v2 kept spending in between.

**Corrected v2 lifetime (pulled 08-23, final):**

| | 08-20 read | **Final** |
|---|---:|---:|
| Spend | $165.66 | **$386.81** |
| Landing page views | 553 | **1,116** |
| Add to cart | 9 | **18** |
| InitiateCheckout | 0 | **1** |
| Purchases | 0 | **0** |
| Shopify orders | 0 | **0** |

Daily: 08-21 $65.51 · 08-22 $103.86 · 08-23 $51.32. The extra three days cost **$221.15** and bought
one checkout and no orders.

**TOF all time is now $1,870.27** ($1,279.94 Jul + $203.52 v1 + $386.81 v2) → still **one traceable
$362 order**.

Shopify orders since 08-20 (`#1298`, `#1299`, `#1300`): all **Google SEO / direct**. No Meta.

---

## ✅ A1 — DONE. TOF v2 paused.

Approved by Lee in chat, applied 2026-08-23, verified against the account:

| Ad set | Status |
|---|---|
| v2 TOF `120247812165960186` | **PAUSED** ✅ |
| v1 TOF `120247706822330186` | PAUSED |
| Retargeting `120233074187690186` | **ACTIVE** $15/day — the only thing spending on Meta |

Account MTD $1,142.62 against the $2,000 ceiling.

_A2 (retargeting $15 → $18) was not chosen — approval `25d9597c` stays pending._

---

## 🔴 B1 — STOPPED. It runs into a guardrail I wrote, and the guardrail is right.

**B1 was my idea and I should not have proposed it without checking the code first.**

`tools/meta-ads.mjs` refuses `ADD_TO_CART` **by name**, with this comment:

> ADD_TO_CART is refused by name — in the configurator, adding to cart is just how you see a price
> (ATC→Purchase 11% vs IC→Purchase 51%), and optimising on it is what broke July.

Fresh data agrees, and more strongly than when that was written:

| | ATC→Checkout |
|---|---:|
| Retargeting (lifetime, 304 ATC) | **41.8%** |
| TOF v2 (18 ATC) | **5.6%** |

**And the premise of B1 was wrong.** I argued Meta had "no signal to learn from" because IC was zero.
But cold TOF converts to IC at 0.02–0.17% of landing page views. At 1,116 LPV, the *expected* number
of checkouts is **0.2–1.9**. We got 1. **Zero was never evidence of a broken optimisation target — it
was the expected outcome at this traffic volume.** Reaching Meta's ~50 events/week would need roughly
$15,000/week. Switching to ATC would buy ~36 events/week of a signal that predicts purchase eight
times worse, in a configurator where "add to cart" is literally how you see a price.

**The lookalike alternative is also closed.** Checked every custom audience on the account: all 20+
lookalikes return *"The audience is too small to be used in campaign creation."* The seed audiences
are ~20 people. There is no lookalike path until there are far more purchasers.

**Recommendation: do not build v3.** Meta prospecting has now been tried five ways —

| Structure | Spend | Purchases |
|---|---:|---:|
| Advantage+ MOF | $2,964.33 | 4 ($741 each) |
| New Sales – Changed | $1,424.29 | 1 ($1,424) |
| TOF Jul26 | $1,279.94 | 0 |
| Brand Awareness TOF | $740.33 | 0 |
| TOF Aug26 v1 + v2 | $590.33 | 0 |
| **Total prospecting** | **~$7,000** | **5** |
| **Retargeting** | **$3,229.71** | **62** |

**Meta works for Craftons as retargeting. It has never worked as prospecting.**

If Lee still wants v3, the guardrail should be overridden **explicitly and narrowly** — a named
`atc_override_ack` field recording who authorised it and why — not by widening the allowed set, so a
future session cannot trip into it. Not built; awaiting Lee.

---

## 🔴 D1 — The Google campaign is ALREADY LIVE, and it is burning money on the wrong searches

**D1 was "launch the campaign that's already built". It has been running for at least 30 days.**

**Last 30 days: $1,059.42 spend → 4 conversions.** But only **2 are purchases**:

| Conversion action | Count | Value |
|---|---:|---:|
| Google Shopping App Purchase | **2** | **$1,098.00** |
| Craftons (web) form_submit | 2 | $2.00 |

**True CAC ≈ $529 per purchase, against a $322 break-even.** Google is losing money too — but unlike
Meta, the reason is specific and fixable.

### The whole problem in one table

| Ad group | Spend (30d) | Clicks | Conversions |
|---|---:|---:|---:|
| **Radius Pro** | **$567.24** | 132 | **0.0** |
| Curved Architraves | $274.30 | 112 | 3.0 |
| Curved Bench Seat / Formwork | $217.88 | 47 | 1.0 |

**$824.28 of 30-day spend sits on ENABLED keywords with zero conversions.** The four keywords that
actually converted cost **$95.98 between them** — about **$24 per conversion**.

### Why Radius Pro gets nothing

Every keyword in it buys a *substitute-product* searcher:

| Keyword | Match | Spend | Clicks | Conv |
|---|---|---:|---:|---:|
| bendy ply | EXACT | $136.53 | 33 | **0** |
| curved plywood panels | PHRASE | $79.13 | 16 | **0** |
| curved mdf | PHRASE | $75.23 | 18 | **0** |
| bendy ply | PHRASE | $61.21 | 14 | **0** |
| curved mdf | EXACT | $49.61 | 11 | **0** |
| flexible plywood | PHRASE | $35.63 | 8 | **0** |
| rounded plywood | PHRASE | $27.59 | 7 | **0** |
| bending mdf | PHRASE | $19.57 | 5 | **0** |
| curved plywood | PHRASE + EXACT | $34.47 | 9 | **0** |
| 'curved wall plates' | BROAD | $15.38 | 4 | **0** |
| **Total** | | **$434.92** | **105** | **0** |

Someone searching *"bendy ply"* wants a ~$50 sheet of the cheap substitute. Radius Pro is a $600+
engineered plate system. **We are paying $4 a click to show a premium product to people shopping for
the budget alternative it replaces** — and `bendy ply` is on Lee's own banned-words list for Radius
Pro copy. We banned the word in our ads and then bid on it.

**This is the same lesson as Meta TOF, on a second channel, for a second time: the traffic is the
problem, not the creative.**

### But Radius Pro does sell — just not to these searches

Orders `#1292` ($521) and `#1298` ($152) both landed on `/products/radius-online` from **Google
organic** and bought. The product converts on specific intent. The paid keywords are simply the wrong
queries.

### What the winners look like — all narrow, all product-name-exact

| Keyword | Spend | Conv |
|---|---:|---:|
| curved formwork (PHRASE) | $52.76 | 1 |
| curved molding (PHRASE) | $24.97 | 1 |
| arched architrave (PHRASE) | $10.15 | 1 |
| curved architraves (PHRASE) | $8.10 | 1 |

### Proposed — 20 changes, all pending Lee, nothing applied

**Pause 10 substitute-product keywords** (saves ~$435/30d, loses 0 conversions):

| Keyword | approval_id |
|---|---|
| bendy ply EXACT | `539b49db-b508-478e-b492-bf98491aebef` |
| bendy ply PHRASE | `a621a487-e0f7-425a-8b09-736706005857` |
| curved plywood panels | `a4fcc882-8130-472d-bd60-2ccf2e59b66c` |
| curved mdf PHRASE | `a5575fdb-b502-4782-9d02-8a463df7f632` |
| curved mdf EXACT | `2273613b-8ac0-45fc-82d5-10b33262c998` |
| flexible plywood | `b7e8f1ff-f2d7-458b-b872-07c5cf0b17b4` |
| rounded plywood | `d8f1deff-616d-4d56-8171-75788a27b3f9` |
| bending mdf | `3e85538b-a4a1-40e5-becc-7d7a625f0dc9` |
| curved plywood PHRASE | `1e2a461d-d7f3-4d9e-9032-455bd84bf921` |
| curved plywood EXACT | `bd3c55a1-402b-403d-83ba-e32bbc5a5654` |

**Add 10 negative keywords** (PHRASE, campaign `23983924746`) so remaining terms stop picking the
family up: `bendy ply` `78ae87ce` · `bendy plywood` `6dad707b` · `bendable plywood` `88278598` ·
`bending plywood` `714a542f` · `flexible plywood` `84003655` · `bendy mdf` `eb4ce2fe` ·
`bendable mdf` `a87286d6` · `neatform` `c584271d` · `laser cutting` `b87e03bf` ·
`bendable timber` `6d9be7aa`.

### Deliberately NOT proposed

**$389.36 of other 0-conversion keywords** — the moulding and formwork variants (`arched mouldings`
$59.57, `curved bench seat` $80.20, `arched trim` $33.30, `circular formwork` $29.17, and similar).
These sit in ad groups that **do** convert, on the same intent as the winners. Pausing them is
over-pruning a small sample. Better lever is a CPC cut, not a pause. **Flagged, not actioned — Lee's
call.** Recording this rather than silently capping coverage.

---

## ⬜ C1 — Lead capture. Spec written, build not started.

See `campaigns/meta/c1-lead-capture-spec.md`. It is a days-long build touching the Shopify theme, so
this session produced the design and the argument, not the implementation.
