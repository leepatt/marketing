# Aug26 campaign — post-mortem, salvage verdict, and the plan to actual sales

_Written 2026-08-17 07:54 UTC, 83h after go-live, from live account + Shopify data plus current (2026)
Meta guidance. Companion to the reading log in `monitoring-and-reward-plan.md`._

---

## VERDICT: SALVAGE. One component is broken, and it is a two-minute edit.

The campaign structure is right — objective, targeting, budget discipline and creative all verified
working. **The single failure is that the ad set optimises toward a custom conversion that has never
fired**, which starved the optimiser and is now collapsing delivery. Rebuilding from scratch would
discard nothing broken and fix nothing the edit doesn't.

**The fix, today, in Ads Manager (~2 min):**
Ad set `RadiusPro | TOF | Broad AU | SalesIntent | Aug26` → Edit → Conversion → change the conversion
event from the custom conversion (*Sales Intent — Checkout or Purchase*) to the **standard
`InitiateCheckout` pixel event** → Publish. Learning resets — which costs nothing, because with zero
attributed conversions there is no learning to lose.

This is also exactly what current guidance prescribes for accounts our size: *"for low-volume accounts,
temporarily optimise for a more frequent micro-conversion (like Initiate Checkout) until you hit 50+
weekly conversions."* ([Modern Marketing Institute 2026](https://www.modernmarketinginstitute.com/blog/how-to-exit-the-meta-ads-learning-phase-fast-and-start-scaling-profitably-in-2026))

---

## 1. The campaign to date (read live 2026-08-17 07:54)

| | |
|---|---|
| Spend since go-live (13 Aug 20:50) | **$192.08** |
| Link clicks / LPVs | 600 / 578 (96.9% load rate) |
| Real link CTR | 3.58% · $0.32 per LPV |
| ATC / IC / Purchases (Meta-attributed) | 6 / 1 / **0** |
| Custom-conversion attributions | **zero, ever** |
| Delivery trend (daily spend) | $63 → $66 → $48 → **$15** (−86% impressions in 3 days; $75/day budget never once hit) |
| Month-to-date account spend | $655.85 of the $2,000 ceiling |

---

## 2. What went wrong — ranked

### 🔴 Cause 1 (root): the ad set optimises on a conversion Meta has never recorded

The custom conversion `27686282527680441` looks correct on inspection — not archived, rule
`{or:[InitiateCheckout, Purchase]}`, pixel data source — but it has **no `first_fired_time`**, zero
attributed actions on any campaign, and an empty `conversions` field on the ad set, while **the pixel
itself recorded dozens of IC and Purchase events in the same window**. The events flow; the conversion
built on them registers nothing.

The consequence is textbook and documented in current guidance: *"if conversions are happening but not
being tracked, Meta thinks your campaign isn't working and will throttle delivery"*
([admanage 2026](https://admanage.ai/blog/fix-facebook-ads-not-spending)). The optimiser had no signal
for four days, could build no model, lost confidence, and cut delivery 86%. It is compounded by Meta's
**March 2026 shift to outcome-based delivery**, under which accounts below ~50 conversion events/week
are the most sensitive to signal quality
([Digital Applied](https://www.digitalapplied.com/blog/meta-ads-performance-dropped-march-2026-ai-algorithm-changes)).

**Leading hypothesis for WHY it never fired** (not proven; stated with the evidence): the conversion was
created via API, where the documented rule key `event` was rejected and `event_name` was accepted
(`STATUS.md`, 2026-08-03). **Acceptance at write time is not proof the evaluation engine matches on that
key.** A rule the matcher silently ignores would produce precisely this signature: object valid, events
flowing, zero fires ever. Definitive test: recreate the conversion **in the Events Manager UI** (UI-built
rules are guaranteed well-formed) and watch whether it accrues activity within 48h. But don't block on
that — the standard-event fix doesn't need it answered.

### 🟠 Cause 2 (process): the fault was flagged at 16h and acted on by nobody for 3 days

The 16h check-in identified "custom conversion not attributing" as the #1 thing to watch — and then,
by design, deferred action to the 72h check. That cadence is right for *performance* noise and wrong
for *measurement* faults. **New rule: a measurement fault is acted on immediately; only performance
readings wait for statistical patience.** ~$130 of the spend happened inside that gap.

### 🟡 Cause 3 (instruments): three measurement traps found and documented on the way

1. **Engagement-inflated CTR** — `report`'s headline "12.13% CTR" counts likes/saves/expands; only 575
   of 1,947 clicks were link clicks. All CTR/CPC comparisons must use `inline_link_clicks`. July's
   celebrated "10.45% CTR" carries the same inflation.
2. **`/{pixel}/stats` does not window reliably** — one day returned *more* IC than four days. No weekly
   event rate may be quoted from it. Trustworthy sources: Shopify orders and ad-level `actions`.
3. **Pixel purchase inflation re-confirmed at 2.33×** (7 pixel purchases vs 3 real orders, 08-17).

### Context, not a cause: this product's funnel closes late

Today's three orders ($3,592) were all **Google SEO first-touch**; the biggest ($2,736) closed via the
**Trade Program email** after 7 touchpoints. A concreter bought $521 of Radius Pro landing straight on
the product page in one touch. Meaning: **capture and follow-up close; cold ads fill the pool.** The
July finding stands — ~13,000 LPVs produced zero captured emails, and that structural hole is still
open while 578 new visitors have flowed through it this week.

---

## 3. What went right — the salvage case

- **The objective fix worked.** LPV→ATC is **0.9% vs July's 0.16%** — 5.6× better traffic quality from
  the same creative bones. `OUTCOME_SALES` is finding real tradespeople, not cheap clicks.
- **Creative is performing**: 3.58% link CTR, 96.9% click→page-load, $0.32/LPV.
- **The guardrails earned their keep twice**: the kill rule was correctly *refused* at 72h when it
  would have deleted AD5/AD4/AD6 on a broken "zero results" counter; AU-only auditing caught six rogue
  ad sets earlier in the week.
- **Monitoring caught this fault at 16 hours and ~$63 spent.** July's equivalent lesson cost $1,280.
- **The $192 was not burnt**: 578 verified humans hit the product page and now seed the retargeting
  pool, which is live and producing all the account's attributed results.

---

## 4. The salvage plan

### Phase 0 — restore the signal (today)
1. **Lee: the 2-minute conversion-event edit** (top of this doc). Manual, because of the irony below.
2. **Lee: 30 seconds in Events Manager** — confirm EMQ (target >7 per 2026 guidance) and glance at
   whether the custom conversion shows any activity (settles the root-cause hypothesis).
3. No other touches. No kills while the results counter is broken.

> ### ⚠️ The guardrail irony, worth recording
> `create_ad_set` **hard-rejects `custom_event_type`** — a rule I wrote because optimising on the raw
> ATC event broke July, encoding "custom conversion good, standard event bad". The evidence has now
> inverted: the custom conversion is the broken part and the standard event is the fix — and my own
> guardrail blocks the tool from applying it. **Guardrails encode hypotheses; when the evidence flips,
> revise the guardrail rather than obey it.** Code change spec: allow
> `custom_event_type: "INITIATED_CHECKOUT"` explicitly (still reject `ADD_TO_CART`), or add an
> `update_ad_set` change type; plus an activation-preflight rule that **refuses to point spend at any
> custom conversion with no `first_fired_time`** — the check that would have caught this before launch.

### Phase 1 — re-learn and judge honestly (weeks 1–4)
- After the event change, **hands off for 7 days** (fresh learning phase; per 2026 guidance the fastest
  exit is consolidated structure + no edits).
- Judge on **blended account CAC vs $322**, secondary on cost/IC and the LPV→ATC→IC funnel. ~10
  conversions ≈ 3–4 weeks at $75/day. Retargeting stays on.
- Kill rule re-arms **only once results attribute** — then 72h/$25/zero-results as coded.

### Phase 2 — reward winners and widen the entity set (when results attribute)
- **Andromeda reads our 6 ads as roughly 3.** Current guidance: Andromeda collapses visually similar
  creatives into a single Entity ID and makes them compete internally rather than expanding reach
  ([Billo](https://billo.app/blog/meta-andromeda-update/), [Segwise](https://segwise.ai/blog/meta-andromeda-update-creative-strategy-2026)).
  AD4/AD5/AD6 share one photograph — one entity. The 2026 target is **8–12 conceptually distinct
  creatives** ([PixelFlow checklist](https://pixelflow.so/blog/meta-ads-checklist-2026)). We can get
  there **without violating the no-segmentation rule**, because concept diversity ≠ trade targeting:
  the 33 brand-checked static cards and the configurator proof cards are visually distinct entities
  sitting unused. Add the best 3–5 once measurement is stable.
- Identity clones (LF4 concreters / LF5 landscapers / LF7 pool builders — all written) stay gated until
  an ad has real attributed conversions, then multiply the winner.
- **Photography remains the single biggest lever** — one real photo still beats everything, and it also
  breaks the entity-collapse problem. Shot list in `creative-strategy.md` §4.1; ask Lawless + Cronulla.
- Budget ladder unchanged: $75 → $90 → $100 (cap), one step/week, only at CAC ≤ $322.

### Phase 3 — structural (this month, parallel)
- **Lead capture on `/products/radius-online`.** Today's biggest order closed via email. The July gap
  (13k LPVs, zero emails) is still the most expensive hole in the funnel.
- **CAPI + EMQ hygiene** — pixel+CAPI running together with EMQ >7 is table stakes in every 2026
  checklist; ours is unread since 2026-08-04.
- Creative refresh cadence ~monthly (Andromeda-era guidance: refresh every 2–3 weeks; our
  `check-batch`/novelty gates already enforce diversity on new batches).
- Revisit Advantage+ Sales structure only after conversion history exists; a single broad ad set is
  already 90% of that shape.

### 📅 September budget decision (needs Lee before 1 Sep)
$75/day × 30 = **$2,250 > the $2,000/month code ceiling**. August fits only because launch was mid-month
($656 MTD). Options: raise `MONTHLY_CEILING_AUD` (code change + review), or run September at $65/day
($1,950). Do nothing and the ceiling guard will start blocking budget-affecting writes mid-September.

---

## 5. Learnings ledger — carried to every future campaign

1. **Never point spend at a conversion that has never fired.** Check `first_fired_time` / Events
   Manager activity *before* launch. (Encode as activation-preflight — spec above.)
2. **Creation success ≠ semantic validity.** The API accepted an `event_name` rule and
   `validate_only` passed the payload; neither proves the matcher works. UI-created objects, or a
   48h fire-test, are the proof.
3. **Measurement faults are acted on immediately; performance readings wait.** The 16h→72h deferral
   cost ~$130.
4. **Never kill on "zero results" when results cannot be counted.** The kill rule would have deleted
   the account's best creative twice this week.
5. **Delivery collapse with empty `learning_stage_info` and empty `issues_info` = starved optimiser.**
   It is a signal-side fault, not creative/budget/targeting.
6. **Use `inline_link_clicks` for every CTR/CPC claim.** Engagement-inflated CTR misread July and
   nearly misread August.
7. **Distrust `/{pixel}/stats` windows; trust Shopify counts and ad-level `actions`.** Pixel purchases
   run ~2.3× real orders.
8. **One photograph = one Andromeda entity, however many ads wear it.** Visual diversity is the real
   diversity; another reason photography is the lever.
9. **Guardrails encode hypotheses.** When evidence inverts (custom conversion vs standard event),
   revise the rule — don't route around it, don't obey it.
10. **This product closes late, via capture + retargeting + search.** Judge TOF blended, build the
    email capture, and remember the concreter who bought $521 in one touch from Google.

---

## Sources (2026)

- [admanage — Facebook Ads Not Spending? 9 Fixes (2026)](https://admanage.ai/blog/fix-facebook-ads-not-spending)
- [Digital Applied — Why Meta Ads Performance Dropped in March 2026](https://www.digitalapplied.com/blog/meta-ads-performance-dropped-march-2026-ai-algorithm-changes)
- [Modern Marketing Institute — Exit the Learning Phase in 2026](https://www.modernmarketinginstitute.com/blog/how-to-exit-the-meta-ads-learning-phase-fast-and-start-scaling-profitably-in-2026)
- [PixelFlow — Meta Ads Checklist 2026 (Andromeda era)](https://pixelflow.so/blog/meta-ads-checklist-2026)
- [Segwise — Meta Andromeda Creative Strategy 2026](https://segwise.ai/blog/meta-andromeda-update-creative-strategy-2026)
- [Billo — Meta Andromeda Update: Creative Volume & AI Ranking](https://billo.app/blog/meta-andromeda-update/)
- [Cropink — Optimization for Ad Delivery on Meta, 2026](https://cropink.com/optimization-for-ad-delivery-meta)
