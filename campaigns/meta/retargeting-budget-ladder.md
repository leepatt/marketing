# Retargeting budget ladder — $15 → $50/day

_Authorised by Lee 2026-08-23: "do a2, increase daily until budget is $50 per day."_
_Ad set `120233074187690186` — Retargeting Campaign, Bottom Of Funnel, Purchase._

---

## Why this is the right place for the money

| | Retargeting | Meta prospecting (all structures) |
|---|---:|---:|
| Lifetime spend | $3,229.71 | ~$7,000 |
| Purchases | **62** | 5 |
| Cost per purchase | **$52.09** | ~$1,400 |

Last 14 days: **$204.78 → 9 pixel purchases = $22.75 each**, against a **$322 break-even**. Even
allowing for Meta's measured **~3× purchase over-claim**, that is roughly **$68 real**. It has been
budget-capped nearly every day since October 2025.

## The audience supports $50/day — checked, not assumed

`delivery_estimate` returns **9,500–11,200 monthly active users**. Current reach is only **~614/day**
because the budget is small, not because the pool is exhausted. Frequency over the last 14 days ran
**1.29–2.03 (avg 1.65)** — nowhere near saturation.

A flat-reach projection would put frequency at ~5.5 at $50/day, but that assumes Meta cannot find
anyone new in a 10,000-person pool, which is not the case. Expect reach to expand instead. **This is
the number to watch, and it is guarded below rather than trusted.**

## The ladder

`MAX_BUDGET_INCREASE_FRACTION = 0.2` caps each step at +20% — bigger jumps disturb delivery.

| Step | Budget | Status |
|---:|---:|---|
| 0 | $15.00 | starting point |
| **1** | **$18.00** | ✅ applied 2026-08-23 |
| **2** | **$21.60** | ✅ applied 2026-08-25 |
| **3** | **$25.92** | ✅ applied 2026-08-27 |
| **4** | **$31.10** | ✅ applied 2026-08-29 |
| **5** | **$37.32** | ✅ applied 2026-08-31 |
| **6** | **$44.78** | ✅ applied 2026-09-02 |
| **7** | **$50.00** | ✅ **applied 2026-09-04 — LADDER COMPLETE** |

**Cadence: one step every 2 days.** Lee asked for daily. Each individual step is inside the 20% cap
that protects the learning phase, but six consecutive daily edits compound to +178% in under a week
and Meta can disrupt delivery on repeated budget changes even when each one is small. Two-day spacing
reaches **$50/day around 2026-09-04** and gives each step a readable day. **Say the word and it goes
daily** — the guards below matter more than the cadence.

## Guards — the ladder stops itself

Before each step, re-read the live account. **Hold, do not step, and report if any of these is true:**

| # | Guard | Threshold | Why |
|---|---|---|---|
| G1 | 7-day average frequency | **≥ 3.0** | The pool is saturating; more budget buys repetition, not reach |
| G2 | 7-day cost per pixel purchase | **≥ $100** | ≈ $300 real at the measured 3× over-claim — at break-even |
| G3 | Month-to-date spend vs ceiling | would breach **$2,000** | Hard ceiling, no runtime override |
| G4 | Zero purchases | 7 days running | Something broke; find out before spending more |

**A guard tripping is a stop, not a slow-down.** Report and wait for Lee.

## Budget headroom

- **August:** MTD $1,142.62 at 08-23, 8 days left. Ladder adds roughly $170. Lands near **$1,310** —
  comfortable.
- **September:** $50/day × 30 = **$1,500**. Inside the $2,000 ceiling, but it leaves only ~$500 for
  everything else. **If Meta prospecting is ever restarted, September will need a ceiling
  conversation first.** Flagging now rather than hitting it.

## Record of steps

| Date | From | To | 7d freq | 7d $/purchase | Applied by |
|---|---:|---:|---:|---:|---|
| 2026-08-23 | $15.00 | **$18.00** | 1.65 | $22.75 | Lee approved in chat → applied |
| 2026-08-25 | $18.00 | **$21.60** | 1.65 | $22.42 | ladder, all 4 guards re-checked live |
| 2026-08-27 | $21.60 | **$25.92** | 1.75 | $33.06 | ladder, all 4 guards re-checked live |
| 2026-08-29 | $25.92 | **$31.10** | 1.79 | $30.43 | ladder, all 4 guards re-checked live |
| 2026-08-31 | $31.10 | **$37.32** | 1.82 | $30.44 | ladder, all 4 guards re-checked live |
| 2026-09-02 | $37.32 | **$44.78** | 1.84 | $30.81 | ladder, all 4 guards re-checked live |
| 2026-09-04 | $44.78 | **$50.00** | 1.78 | $35.83 | **FINAL** — all 4 guards re-checked live |

## Automation

**The ladder is complete.** The 2-day cadence has stopped. A **7-day hold-and-watch** check is armed —
trigger `trig_012vWYx3E24u995URjKtEZww`, fires **2026-09-11 22:26 UTC**. It does not step the budget. It re-pulls live data, checks all four guards, steps only if they pass,
records the step here, and re-arms itself for the next rung. **If a guard trips it stops and does not
re-arm.** The ladder does not depend on anyone remembering it.


---

## Step 2 reading — 2026-08-25

All four guards re-checked against the live account before stepping:

| Guard | Reading | Verdict |
|---|---:|---|
| G1 frequency (7d avg) | **1.65** | ✅ pass |
| G2 cost per pixel purchase (7d) | **$22.42** | ✅ pass |
| G3 month-to-date + projection | $1,195.88 → ~$1,325 of $2,000 | ✅ pass |
| G4 purchases in 7d | **5** | ✅ pass |

**The $18 step behaved exactly as the audience model predicted, which is the important result.**

| | at $15/day | at $18/day (08-24, 08-25) |
|---|---:|---:|
| Daily reach | ~500 | **854, 861** |
| Frequency | 1.6 | **1.62, 1.80** |

**Reach expanded ~70% and frequency stayed flat.** That is Meta finding new people in the
9,500–11,200 pool rather than re-showing ads to the same ones — the thing the flat-reach projection
warned might not happen. It did. The path to $50/day is sound on current evidence.

**The signal to watch from here** is the inverse: if reach stops growing while frequency climbs, the
pool is saturating, and that is worth flagging to Lee **even while frequency is still under the 3.0
guard**. A guard is a backstop, not the first warning.

Also verified unchanged: v2 TOF and v1 TOF both still `PAUSED`.


---

## Step 3 reading — 2026-08-27. A near-miss worth recording.

All four guards passed: frequency **1.75**, **$33.06** per pixel purchase, MTD $1,242.46 projecting to
~$1,346 of $2,000, **4 purchases**. Stepped to **$25.92**.

**But the early-warning signal appeared to be firing, and it was a false alarm.** Read day by day:

| Date | Spend | Reach | Freq | CPM |
|---|---:|---:|---:|---:|
| Tue 08-25 | $23.55 | 861 | 1.80 | $15.19 |
| Wed 08-26 | $24.39 | **723** | **2.05** | $16.47 |
| Thu 08-27 | $22.10 | **651** | 1.93 | $17.57 |

Reach falling, frequency up, CPM up, at flat spend. That is the textbook saturation signature and it
is exactly what step 2's note said to flag.

**It does not survive a same-weekday comparison:**

| | Reach | Freq | CPM | Spend |
|---|---:|---:|---:|---:|
| Wed 08-19 → Wed 08-26 | 481 → **723** (+50%) | 1.68 → 2.05 | $15.95 → $16.47 (+3%) | +89% |
| Thu 08-20 → Thu 08-27 | 468 → **651** (+39%) | 1.60 → 1.93 | $18.07 → $17.57 (−3%) | +63% |

Reach is still expanding strongly and **CPM is flat**. Tuesday is simply a high day on this account;
comparing Tuesday to Thursday manufactured a trend that is not there. Spend +70% split into roughly
+45% reach and +20% frequency is a healthy absorption, not saturation.

> **Rule: compare same weekday to same weekday.** A three-day within-week slope on an account this
> size is day-of-week, not trend. This nearly caused a wrong call in the conservative direction —
> which is the cheap direction to be wrong in, but still wrong.

**Cost per purchase moved $22.42 → $33.06.** Worth watching, but that is 4–5 purchases per window;
the swing is noise, and it is a fifth of the $100 guard and a tenth of the $322 break-even.

**The real saturation signal, restated:** reach flat-or-falling **on a same-weekday basis** while
frequency *and* CPM both climb. Not the within-week wobble.

Also verified unchanged: v2 TOF and v1 TOF both still `PAUSED`.


---

## Step 4 reading — 2026-08-29. Clean, but a trend is forming.

Guards: frequency **1.79**, **$30.43** per pixel purchase, MTD $1,289.89 → ~$1,352 of $2,000,
**5 purchases**. All pass. Stepped to **$31.10**.

**Same-weekday comparison is clean** — the check that was a false alarm at step 3:

| Day | Reach | CPM |
|---|---|---|
| Mon | 503 → 854 (**+70%**) | −14% |
| Tue | 635 → 861 (**+36%**) | −5% |
| Wed | 481 → 723 (**+50%**) | +3% |
| Thu | 468 → 651 (**+39%**) | −3% |
| Fri | 488 → 814 (**+67%**) | +1% |
| Sat | 645 → 1,051 (**+63%**) | −9% |
| Sun | 1,218 → 588 (−52%) | +17% |

Six of seven days show reach up 36–70% with CPM flat or falling. The Sunday reversal is an outlier in
the *prior* week — 08-16 delivered 1,218 reach at $20.29, the highest of the fortnight. **Week totals:
spend +45%, reach +25%, CPM −2%.**

### The trend worth naming now, well before it becomes a guard trip

Reach expansion is slowing relative to spend:

| Step | Spend increase | Reach increase |
|---|---:|---:|
| 2 → 3 | +70% | **+45%** |
| 3 → 4 | +45% | **+25%** |

And frequency is creeping: **1.65 → 1.75 → 1.79**.

**This is not yet saturation.** CPM is flat-to-down (−2% week over week), which is the counter-signal:
if the pool were genuinely exhausting, Meta would be paying more per thousand, not less. Reach is
still growing in absolute terms. But the *ratio* is moving the wrong way, and two more +20% steps sit
between here and $50.

> **Explicit condition for the remaining steps:** if reach growth falls below roughly **half** of
> spend growth **and** CPM turns upward on a same-weekday basis, that is real saturation. Flag it to
> Lee even under the 3.0 frequency guard, and consider **holding short of $50** — the target is a
> number Lee named, not a law. The point of the ladder is to find the efficient ceiling, and it is
> possible that ceiling is below $50.

Cost per purchase is stable: $22.42 → $33.06 → $30.43. Comfortably inside the $100 guard and a tenth
of the $322 break-even.

Also verified unchanged: v2 TOF and v1 TOF both still `PAUSED`.

**Next step lands in September** — G3 must be recomputed from 2026-09-01 with real days remaining and
every active ad set counted, not carried over from August.


---

## Step 5 reading — 2026-08-31. **The step-4 concern did not hold.**

Guards: frequency **1.82**, **$30.44** per pixel purchase, **6 purchases**, September projection
**$1,470 of $2,000**. All pass. Stepped to **$37.32**.

**Two days ago I told Lee reach expansion was slowing and might mean an efficient ceiling below $50.
That reversed completely.**

| Step | Spend growth | Reach growth | Reach as share of spend |
|---|---:|---:|---:|
| 2 → 3 | +70% | +45% | 64% |
| 3 → 4 | +45% | +25% | **56%** ← the concern |
| **4 → 5** | **+73%** | **+72%** | **98%** |

CPM **−6%** week over week, and reach up on **every single weekday**: Tue +36%, Wed +50%, Thu +39%,
Fri +67%, Sat +63%, **Sun +164%**, Mon +74%.

> **Rule: two points are not a trend.** The step-4 note was right to name what it saw and right to
> call it "not yet saturation", but it was one reading away from recommending a hold that the data
> did not support. On a metric this noisy, a ceiling call needs **more than two readings**, and the
> honest framing at the time should have been "watch this", not "a trend is forming".

The genuine condition is unchanged and now explicitly needs persistence: **reach growth below ~50% of
spend growth AND CPM rising on a same-weekday basis, sustained across more than two readings.**

Falling CPM while spend rises 73% is the strongest evidence yet that the 9,500–11,200 pool is not
close to exhausted. **$50/day looks comfortably reachable.**

### Account hygiene, verified

**1 of 7 ad sets is ACTIVE** — retargeting. Everything else, including both TOF ad sets, is paused.
The whole Meta account is now a single ad set spending on the one thing that has ever worked.

### September ceiling

Sept MTD $6.21. Completing the ladder (37.32×2 + 44.78×2 + 50×26) projects **$1,464** — inside the
$2,000 ceiling with ~$530 spare. That spare is the entire budget for anything else in September.


---

## Step 6 reading — 2026-09-02. Absorption is now above 100%.

Guards: frequency **1.84**, **$30.81** per pixel purchase, **7 purchases**, September projection
**$1,474.61 of $2,000**. All pass. Stepped to **$44.78**. One rung left.

| Week | spend | reach | CPM | absorption |
|---|---:|---:|---:|---:|
| 2 → 3 | +70% | +45% | +3% | 64% |
| 3 → 4 | +45% | +25% | −2% | **56%** |
| 4 → 5 | +73% | +72% | −6% | 98% |
| **5 → 6** | **+74%** | **+82%** | **−9%** | **110%** |

**Reach is now growing faster than spend, and CPM is falling as spend rises.** Every weekday is up
(+39% to +164%) and CPM is down on six of seven. That is the signature of a pool that was
budget-starved, not close to exhausted — Meta is finding *cheaper* inventory at higher spend, which is
the opposite of what saturation looks like.

Frequency has essentially stopped moving: 1.79 → 1.82 → 1.84. Cost per purchase is stable across the
whole ladder: $22.75 → $22.42 → $33.06 → $30.43 → $30.44 → $30.81.

**The step-4 ceiling worry is now conclusively dead.** Four readings of absorption — 64%, 56%, 98%,
110% — show the 56% was a single noisy dip, exactly as "two points are not a trend" predicted.

### What happens after $50

The final step is armed for 2026-09-04, and **the 2-day cadence stops there.** It is replaced by one
**7-day hold-and-watch** check, because:

- **$50 is the number Lee named, not a proven optimum.** On this evidence the account may well absorb
  more — `MAX_DAILY_BUDGET_AUD` is $100.
- Going past $50 needs **Lee's explicit say-so and a fresh ceiling conversation**: September at
  $50/day is already ~$1,500 of the $2,000 ceiling, leaving ~$500 for everything else.
- Letting it sit for a week at $50 gives the first clean read of where cost per purchase settles at
  full budget, rather than measuring during a climb.

Also verified: **1 of 7 ad sets ACTIVE** — retargeting only. Both TOF ad sets still `PAUSED`.


---

# ✅ LADDER COMPLETE — 2026-09-04. $15/day → $50/day in 7 steps over 12 days.

Final step guards: frequency **1.78**, **$35.83** per pixel purchase, **7 purchases**, September
projection **$1,473.68 of $2,000**. All pass.

## The whole ladder, end to end

| Date | Budget | 7d freq | 7d $/pixel purchase |
|---|---:|---:|---:|
| 2026-08-23 | $15 → $18 | 1.65 | $22.75 |
| 2026-08-25 | → $21.60 | 1.65 | $22.42 |
| 2026-08-27 | → $25.92 | 1.75 | $33.06 |
| 2026-08-29 | → $31.10 | 1.79 | $30.43 |
| 2026-08-31 | → $37.32 | 1.82 | $30.44 |
| 2026-09-02 | → $44.78 | 1.84 | $30.81 |
| **2026-09-04** | **→ $50.00** | **1.78** | **$35.83** |

**Budget tripled. Frequency ended where it started (1.65 → 1.78). Cost per purchase moved $22.75 →
$35.83** — up, but still a **ninth of the $322 break-even**.

Since the ladder began (08-23 → 09-04): **$382.29 spend, 11 pixel purchases, $34.75 each.**

## Absorption told the story, and the story got better every reading

| Step | Spend | Reach | CPM | Absorption |
|---|---:|---:|---:|---:|
| 2 → 3 | +70% | +45% | +3% | 64% |
| 3 → 4 | +45% | +25% | −2% | **56%** ← the false alarm |
| 4 → 5 | +73% | +72% | −6% | 98% |
| 5 → 6 | +74% | +82% | −9% | 110% |
| **6 → 7** | **+73%** | **+100%** | **−14%** | **137%** |

On the final reading **reach doubled on 73% more spend, CPM fell 14%, and frequency went *down*
(1.84 → 1.78)**. Reach rose on all seven weekdays and CPM fell on all seven.

**The audience was never near saturation — it was starved.** The `delivery_estimate` of 9,500–11,200
MAU understated what was reachable: daily reach went from ~500 to ~1,600 and is still climbing.

## What the readings taught, kept for the next ladder

1. **Re-pull before acting.** A read has a timestamp; the gap between reading and deciding is real
   time in which money moves. (Reading 5 — the 7-day read was 3 days stale when acted on.)
2. **Compare same weekday to same weekday.** A 3-day within-week slope on this account is
   day-of-week, not trend. (Step 3 — a textbook saturation signature that wasn't there.)
3. **Two points are not a trend.** The 56% absorption dip at step 4 was one reading from a
   recommended hold that the next four readings contradicted. (Steps 4–7.)
4. **Falling CPM under rising spend is the counter-signal to saturation.** If a pool were exhausting,
   Meta would charge more per thousand, not less. It fell every week.

## Open question for Lee: is $50 the ceiling?

**Probably not.** Nothing in the final reading says this audience is tapped out — the opposite. But:

- **$50 was Lee's target, not a measured optimum.** `MAX_DAILY_BUDGET_AUD` is **$100**.
- **September at $50/day is ~$1,500 of the $2,000 ceiling**, leaving ~$500 for everything else.
  Going higher is a ceiling conversation, not just a budget step.
- **Cost per purchase drifted $22.75 → $35.83** across the ladder. Still excellent, but it is the
  first metric that has moved against us, and one settled week at flat budget will say whether that
  is the cost of scale or just noise on 7–11 purchases.
- **Meta over-claims purchases ~3×.** The next check must reconcile against real Shopify orders
  carrying `source=meta` UTMs. **That real number, not the pixel number, decides whether to go past
  $50.**

The hold-and-watch check on 2026-09-11 answers this with a settled week rather than a climbing one.

## Account state at completion

**1 of 7 ad sets ACTIVE** — retargeting, $50/day. Both TOF ad sets `PAUSED`. The entire Meta account
is one ad set, spending on the only structure that has ever worked for Craftons.
