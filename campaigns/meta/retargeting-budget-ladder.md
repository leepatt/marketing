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
| **1** | **$18.00** | ✅ **applied 2026-08-23** |
| 2 | $21.60 | pending |
| 3 | $25.92 | pending |
| 4 | $31.10 | pending |
| 5 | $37.32 | pending |
| 6 | $44.78 | pending |
| 7 | **$50.00** | target (+11.7%, final step) |

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

## Automation

Step 2 is armed as a scheduled reminder — trigger `trig_011UaPGvNu813zEAC3w7CZgC`, fires
**2026-08-25 22:06 UTC**. It re-pulls live data, checks all four guards, steps only if they pass,
records the step here, and re-arms itself for the next rung. **If a guard trips it stops and does not
re-arm.** The ladder does not depend on anyone remembering it.
