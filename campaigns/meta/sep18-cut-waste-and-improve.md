# Cut the waste + what to fix next — 2026-09-18

_Lee: "lets cut the waste. Analyse the ads running and see how we can improve."_
_Everything below was pulled live. Applied changes are verified against the accounts._

---

## ✅ APPLIED TODAY — the Google waste is stopped

**10 keywords paused** in the Radius Pro ad group, all verified `PAUSED`:
`bendy ply` (EXACT + PHRASE) · `curved plywood panels` · `curved mdf` (PHRASE + EXACT) ·
`flexible plywood` · `rounded plywood` · `bending mdf` · `curved plywood` (PHRASE + EXACT).

**10 negative keywords added** to campaign `23983924746` (now 102 negatives total):
`bendy ply` `bendy plywood` `bendable plywood` `bending plywood` `flexible plywood` `bendy mdf`
`bendable mdf` `neatform` `laser cutting` `bendable timber`.

Those ten keywords had taken **$391.73 for zero conversions** since 08-24, and about **$435/month**
before that. Every one bought a searcher shopping for the cheap substitute Radius Pro replaces.

---

## 🔑 THE FINDING — Radius Pro *does* convert, on language the ad never uses

With the substitute-product keywords gone, what is left in that ad group is the part that works:

| Keyword | Match | Spend 30d | Clicks | Conversions | Cost/conv |
|---|---|---:|---:|---:|---:|
| `'radius wall plates'` | BROAD | **$283.39** | 82 | **4** | **$70.85** |
| `'curved wall plates'` | BROAD | **$165.20** | 47 | **3** | **$55.07** |

**Seven conversions at ~$64 each, against a $322 break-even.** The ad group was never broken — it was
being drained by the sheet-material keywords sitting next to these.

### But the ad answers a different question

The Radius Pro RSA is **ad strength POOR**, **CTR 5.4%** (vs 10.1% and 11.7% in the other two ad
groups), and its 15 headlines say *curved plywood / curved ply* **seven times**:

> Curved Plywood, Cut To Size · Radius Pro Curved Plywood · Curved Ply, Ready To Fix · Custom Curved
> Plywood · Australian Made Curved Ply · Install-Ready Curved Ply · Get A Curved Ply Quote

**It never once says "wall plates"** — the exact phrase in both converting keywords. We are bidding on
*wall plates* and answering with *curved plywood*, which is the same sheet-material framing that just
cost $391.73.

**This is the single highest-leverage fix available, and it is free.**

---

## What is running, and what is wrong with it

### Google — 3 ad groups

| Ad group | Ad strength | CTR | Spend 30d | Conv |
|---|---|---:|---:|---:|
| **Radius Pro** | 🔴 **POOR** | **5.4%** | $246.20 | 4 |
| Curved Architraves | AVERAGE | 10.1% | $240.09 | 2 |
| Curved Bench Seat / Formwork | GOOD | 11.7% | $218.02 | 1 |

**Also found: a duplicate ad.** `814926686840` in Curved Bench Seat / Formwork is **byte-identical**
to `814855235971` — same 15 headlines, same 4 descriptions — and has taken **$54.93 for 0
conversions** while the original returns 1. Two identical ads split the same traffic and Google rated
the copy differently on each. Curved Architraves has the same problem with two $0-spend twins.

### Meta — only 2 ads, and one has the wrong button

| Ad | Spend 30d | CTR | Freq | ATC | Purchases | CTA |
|---|---:|---:|---:|---:|---:|---|
| **BOF Ad 2 (purchase-optimised)** | $828.79 | **0.72%** | 3.72 | 140 | **22** | 🔴 **`BOOK_TRAVEL`** |
| Configurator Hero Ad D | $265.83 | **0.41%** | **5.12** | 39 | 8 | `SHOP_NOW` |

Three things wrong here:

1. **`BOOK_TRAVEL` is the call-to-action on the ad doing 80% of the work.** That is Meta's
   travel-booking button, on an ad selling CNC-cut plywood. The paused Ad 1 has it too. Nobody chose
   this deliberately.
2. **CTR is 0.72% and 0.41%.** The TOF ads we built in August ran **3.36%** link CTR. Warm retargeting
   audiences should beat cold traffic, not trail it by 5×. This is creative fatigue.
3. **Ad D is worn out** — frequency **5.12** with the *worst* CTR. It is showing the same people the
   same thing five times and converting worse for it.

**And there is no creative rotation at all** — two ads, both old. Meanwhile **six fresh creatives are
built, brand-checked and approved**, sitting unused in the paused TOF ad set, including the Lawless
site photo that ran at **10.45% CTR** — the best-performing asset this account has ever had.

---

## Short-term plan, ranked by return per hour

| # | Action | Effort | Why it is ranked here |
|---|---|---|---|
| **1** | **Rewrite the Radius Pro RSA around "wall plates"** | ~1 hr | Free. It is the language in both converting keywords, the ad never says it, and the ad is rated POOR. Fixes CTR *and* relevance on the only Radius Pro terms that make money |
| **2** | **Fix the Meta CTA** — `BOOK_TRAVEL` → `SHOP_NOW` on BOF Ad 2 | 10 min | A wrong button on the ad carrying 22 of 30 purchases. Pure defect |
| **3** | **Pause the duplicate formwork ad** `814926686840` | 5 min | $54.93 for 0 conv, identical copy to the one that converts. Stops splitting traffic |
| **4** | **Rotate fresh creative into Meta retargeting** | ~1 hr | Two fatigued ads, zero rotation, and six approved creatives already built. Retire Ad D (freq 5.12 / CTR 0.41%), promote the Lawless photo |
| **5** | **Step Meta to $31.10/day** | 1 min | The tripwire fired — two weeks, one traceable order each, ~$349 real CPA vs $322 break-even. **Blocked by a permission prompt, see below** |

**1–4 cost nothing but time and touch no budget.** They are the improvement work; the cuts are done.

---

## ⚠️ One thing I could not finish

**The Meta step-down to $31.10/day did not apply.** The approval is recorded and approved
(`8662dea4-abd3-4e44-a9a7-2c753a338409`) but the `apply` command was refused by the sandbox
permission classifier — *"Modify Shared Resources"*. Verified after the attempt: the ad set is
**still ACTIVE at $50.00/day**.

I did not attempt to route around it. Lee can either approve the command when prompted, add a Bash
permission rule, or change it in Ads Manager directly.

---

## Where the money actually is, for context

Seven days to 09-17: **13 Shopify orders, $13,339.** Sources: the builder (3), Google SEO (4),
direct (4), **Bing (1)**, **Meta (1)**.

Paid Meta is **2.4% of revenue** for $343 of spend. Google paid is small but genuinely profitable on
the *wall plates* terms. **Bing has never been looked at and produced ~$7,700 in the prior fortnight.**
