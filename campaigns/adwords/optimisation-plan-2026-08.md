# Google Ads optimisation plan — August 2026

_Written 2026-08-03 off live API data. Companion to `reports/2026-08-03-google-ads-report.md`._
_Context: Cavity Battens is **discontinued** (confirmed by Lee), so PMax stays off permanently and
paid search is now the entire acquisition channel. Everything here matters more than it did._

---

## The root cause: it's the landing pages, not the ads

Quality Score breaks into three components. Pulled for every enabled keyword, 1 Jul – 2 Aug:

| Ad group | Ad relevance | **Landing page experience** | Expected CTR |
|---|---|---|---|
| Radius Pro | 6 above / 1 avg / 7 below | **14 of 14 BELOW AVERAGE** | 13 below / 1 avg |
| Curved Bench Seat / Formwork | 4 above / 5 avg / 0 below | **9 of 9 BELOW AVERAGE** | 7 below / 2 avg |
| Curved Architraves | 17 above / 5 avg / 9 below | **29 of 31 BELOW AVERAGE** | 13 below / 16 avg / 2 above |

**Landing page experience is BELOW AVERAGE on 52 of 54 scored keywords.** Ad relevance is broadly
fine — Architraves is *above average* on 17 of 31. So the instinct to rewrite ads was only half right:
the ads are mostly doing their job, and the pages are dragging every keyword down to QS 1–3.

### Why the pages score badly

Fetched all three live pages:

| Page | HTML | Visible words | Load |
|---|---|---|---|
| `/products/radius-online` | 238 KB | **489** | 1.45s |
| `/products/curved-architraves` | 237 KB | **515** | 0.95s |
| `/products/craftons-formwork-builder-custom-online-formwork` | 237 KB | **502** | 1.03s |

~500 words of readable text inside 237 KB of JavaScript. These are configurator app shells, not
landing pages. Two consequences: there's little for Google to read, and mobile — **61% of spend,
converting at a third the rate of desktop** — gets the heaviest version of that.

### The pages don't contain the words being bid on

| Page | Bids on | Occurrences on page |
|---|---|---|
| `radius-online` | bendy ply, bendable plywood, flexible plywood, curved mdf | "curved" **×1** · bendable, flexible, bending, mdf **×0** |
| `curved-architraves` | arched mouldings, archway moulding, arch moulding, curved trim | **"moulding" ×0** · "trim" ×0 · "archway" ×0 · "arched" ×1 |
| `formwork-builder` | curved formwork, curved bench seat | "formwork" **×8** · "curved" ×4 · "bench seat" ×1 |

The correlation is hard to miss: the page with real keyword coverage (formwork) sits in the ad group
that produced **2 of the account's 4 conversions**. The page with a single instance of "curved"
(Radius Pro) has produced **zero from 97 clicks**.

### What it's worth

The account's own data prices this: `curved architrave` at **QS 7 costs $2.98/click**. `bendy ply`
and `curved mdf` at **QS 1 cost $5.90**. Same account, same day, ~2x the price for worse positions.

Lifting landing page experience from Below Average to Average across the account is the difference
between buying ~250 clicks a month and ~500 for the same money. No other lever here comes close.

---

## Page fixes (highest value work in this document)

These are Shopify/`cnccut.app` changes, not Google Ads changes. Each page needs a **readable content
block beneath the configurator** — the configurator itself can stay exactly as it is.

### `/products/radius-online` — the priority

Add a section that names the search terms directly, in Craftons voice:

> **Looking for bendy ply?**
> Bendy ply, bendable plywood, flexible plywood — they all solve the same problem: you need a curve.
> Bending it yourself means kerf cuts, laminating, springback and rework.
> Radius Pro skips that. Tell us the radius, we CNC-cut the curve, you install it.
> **No bending. No springback. No rework.**
>
> **Also cut in curved MDF and flexible MDF.**

Must appear in text: *bendy ply · bendable plywood · flexible plywood · bending plywood · curved MDF ·
flexible MDF · curved plywood · radius plywood*. Currently every one of those is absent.

### `/products/curved-architraves` — the growth unlock

The page never uses the word **"moulding"**. The campaign spends most of its money on moulding terms.

> **Curved architraves and arch mouldings, made to your radius.**
> Hallway arches, archway trim, arched doorways, curved window mouldings — cut to your set-out and
> delivered ready to fix. No scribing, no laminating, no builder's bog.

Must appear: *arch moulding · arched moulding · archway moulding · archway architrave · hallway arch ·
arched doorway · curved trim · curved timber moulding · arched architrave*.

### `/products/craftons-formwork-builder…`

Already the best of the three and already converting — leave the structure alone. Add *circular
formwork · round column formwork · curved concrete formwork · curved bench seat* to the copy, since
those are live search terms.

### Mobile

61% of spend, one-third the conversion rate, and the heaviest page. Worth a Lighthouse mobile run on
all three. If the configurator can't render fast on mobile, a lightweight above-the-fold content block
with the configurator lazy-loaded below would fix both the conversion gap and the QS component.

---

## Curved Architraves — how to actually sell more

**The constraint is not budget.** Budget lost impression share is **0.00%**; rank lost is **67.93%**.
The campaign literally cannot spend more money at its current Ad Rank — which is why the budget went
$100 → $25/day today. That's not a retreat, it's removing a number that was never real.

There are only two ways to buy more volume: better Ad Rank, or more/broader keywords.

### Finding: the demand says "arch", the campaign says "curved architrave"

Actual search terms in this campaign: `arch moulding` · `hallway arch moulding` · `archway trim` ·
`arch architrave` · `arched trim moulding` · `arch mouldings` · `decorative arch moulding` ·
`victorian arch moulding` · `moulding arch` · `arch door trim` · `arched architraves`.

The money is in **arch/archway** language. The campaign, the ad group and the page are all built
around "curved architrave" — which is the *product* name, not the *demand* name.

### The plan

1. **Split into two ad groups**, each with matching ads and page anchor:
   - *Curved Architraves* — curved architrave, arched architrave, curved window moulding
   - *Arch & Archway Mouldings* — arch moulding, archway moulding, hallway arch moulding, archway trim
   This is the single biggest ad-relevance lever available and it's free.
2. **Bid up the winner.** `curved architrave` EXACT is **QS 7**, $2.98 CPC, 12–30% CTR — the best
   keyword in the account. It only got 6 clicks. Give it room.
3. **Pause `curved molding`** — US spelling, QS 1, all three components Below Average, $53.64 for
   0 conversions. (See the statistics note below before pausing anything else.)
4. **Watch `arched trim`** — biggest single spender at $74.86 / 17 clicks / 0 conv, and it has no
   Quality Score yet. Revisit at ~30 clicks.
5. **Then, and only then, raise budget.** Once landing page experience is Average and CVR is above
   ~2%, the $25 cap becomes the constraint and lifting it will buy real volume.

---

## ⚠️ A statistics note — do not over-prune

The account has **4 conversions from 316 clicks** (~1.3%). At that rate, a keyword with 12 clicks and
zero conversions is expected to produce **0.16 conversions**. Seeing zero is completely unremarkable —
it is not evidence the keyword is bad.

To be 95% confident a keyword underperforms the account average you'd need roughly **230 clicks** on
it. **The highest-click keyword in the account has 28.**

So: no keyword-level pause is currently justified by *conversion* data. Pause only on grounds that
don't need statistics —
- **intent mismatch** (competitor brands, wrong product, wrong material) — done today
- **Quality Score / relevance** (all three components Below Average with meaningful spend)

Killing keywords on 0-conversion noise at this volume would strip the account back to nothing and
destroy the data needed to make real decisions later.

---

## Conversion values — the measurement fix

`Craftons (web) form_submit` is **Primary** with a **$1 placeholder value**. Bidding therefore
optimises for lead *count*, treating a $200 architrave enquiry and a $15,000 formwork package as
identical.

Purchases carry real revenue (the 2 Jul sale recorded $1,265), so the fix is only needed on leads.

**Blocked — needs one number from Lee:** what is a lead actually worth?

Either input works:
- **Direct:** "a qualified enquiry is worth about $X to us", or
- **Derived:** average job value × the share of enquiries that become jobs. From the account,
  historic AOV is ~$905 (25 purchases / $22,636). If roughly 1 in 5 enquiries converts, that implies
  a lead value near **$180** — but that close rate is a guess and needs to be Lee's number, not mine.

Once set, `maximise conversion value` becomes usable and bidding starts chasing revenue instead of
form fills.

---

## Status

| # | Action | State |
|---|---|---|
| 1 | Restart PMax | ❌ Closed — Cavity Battens discontinued |
| 2 | Negatives + kill competitor bidding | ✅ Applied 2026-08-03 |
| 3 | Pause POOR Radius Pro ad | ✅ Applied 2026-08-03 |
| 3b | Radius Pro v2 ad copy | 📝 Drafted → `ads/google-radius-pro-v2-bendy-intent.md`, awaiting approval |
| 4 | Architraves budget $100 → $25 | ✅ Applied 2026-08-03 |
| 4b | Architraves ad group split + growth | 📝 Planned above |
| 5 | Quality Score → landing pages | 📝 Page briefs above — needs Shopify work |
| 6 | Lead conversion values | ⛔ Blocked on Lee's lead value |
