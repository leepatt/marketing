# Monitoring and "rewarding the winner" — the plan, and the honest arithmetic

_Written 2026-08-05 on Lee's instruction: "monitor performance and reward winning ad after 16 hours."_

---

## 🔴 First: at 16 hours you cannot pick a winner on sales. Here is the arithmetic.

| | |
|---|---|
| Daily budget | **$50/day** |
| Spend in 16 hours | **≈ $33** |
| Break-even CAC | **$322** · target CAC ~$179 |
| Expected purchases from $33 | **≈ 0.1 — 0.2** |
| Expected sales-intent events (IC or Purchase) from $33 | **well under 1** |

**Split across 6 ads, that is a fraction of one conversion per ad.** Any "winner" ranked on sales at
16 hours is noise, and acting on it is precisely what went wrong in July: budget scaled ~13× off an
early read, clicks rose ~150×, results went to **zero**.

**The coded kill rule already refuses this**: an ad needs **≥72h AND ≥$25 AND zero results** before it
can be killed, capped at 50% of the batch per pass. 16 hours fails that gate deliberately, and the
`doctor` self-checks assert it (*"Ad younger than 72h is never killed"*).

### What 16 hours genuinely IS good for

Early **hook** signal, at the creative level, as information — not as an action:

- **CTR** and **CPC** per ad — is the image/hook stopping the scroll?
- **Landing page views** and cost per LPV — is the click cheap and intentional?
- **Any** InitiateCheckout at all — a single IC in 16h is a good sign, zero is not a bad one.
- Delivery sanity: is Meta actually serving all 6 ads, or has it concentrated on one or two already?

⚠️ **The trap, stated plainly.** July's ads showed **8.35% CTR at $0.09 CPC** — spectacular at 16
hours — and produced **zero** conversions. AD5 hit **10.45% CTR and 9,244 landing page views at $0.08**.
Cheap clicks look like a winner early and are the single most misleading metric this account has. **A
high CTR at 16 hours is a reason to keep watching, never a reason to spend more.**

---

## What "reward the winner" can actually mean here

There is **one ad set**, and on Meta the budget lives on the **ad set**, not the ad. So there is no
per-ad budget to shift — "give the winner more money" is not implementable as an allocation. This is
already documented in `_meta-policy.mjs` (`WINNERS_POOL_SIZE`).

Three things "reward" *can* mean, in increasing order of commitment:

| # | Action | Effect | When it is safe |
|---|---|---|---|
| 1 | **Leave it alone** | Meta's own delivery optimisation concentrates the ad set's budget on whatever performs. It does this better than we can from outside | Immediately. This is the default and it is doing the work |
| 2 | **Pause the clear losers** | Shrinks the pool Meta chooses from, so spend concentrates on survivors | **≥72h AND ≥$25 AND zero results** per ad (the coded rule) |
| 3 | **Clone the winner with identity variants** | Multiplies a proven ad — Suby's identity hack. LF4 (concreters) and LF5 (landscapers) are already written and gated for exactly this | Once one ad has **real conversions**, not clicks |

**Option 3 is the actual "reward", and it is what the account's own data supports:** AD4/AD5/AD6 shared
an identical image hash and differed only by the trade word, and AD5 won. Identity words multiply a
proven winner; they do not find one.

---

## 📊 READING 1 — 20.5h after go-live (2026-08-14 17:21 UTC)

Live 2026-08-13 20:50 UTC at $75/day. **No actions taken — report only, per the plan.**

`RadiusPro | TOF | Aug26`, since go-live:

| Ad | Spend | Link CTR | $/link click | LPV | $/LPV | ATC | IC | Purch |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AD5 Chippies (Lawless) | $39.33 | — | — | 142 | $0.28 | 0 | 0 | 0 |
| **AD4 Builders (Lawless)** | $18.60 | — | — | 58 | $0.32 | **2** | **1** | 0 |
| AD6 Carpenters (Lawless) | $4.65 | — | — | 21 | $0.22 | 0 | 0 | 0 |
| AD2b / AD2 / AD1 carousels | $0.17 total | — | — | 1 | — | 0 | 0 | 0 |
| **TOTAL** | **$62.75** | **~3.3%** | **$0.27** | **222** | **$0.28** | **2** | **1** | **0** |

### 🔴 The headline CTR is a lie, and it is the same lie that misread July

`report` shows **11.37% CTR at $0.08 CPC** — spectacular, and meaningless. That is computed on
**all clicks**: only **229 of 785** were link clicks. The other 556 were likes, saves, post expands and
photo views.

**Real numbers: link CTR ~3.3%, cost per link click $0.27, cost per landing page view $0.28.**

⚠️ **The repo's July figures carry the same inflation.** "8.35% CTR at $0.09 CPC" and AD5's "10.45% CTR"
are all-clicks numbers. Any future comparison must use `inline_link_clicks`. *(July's "9,244 LPV at
$0.08" is a genuine cost-per-LPV and is comparable — see below.)*

### ✅ Click quality is excellent — 96.9% of link clicks loaded the page

222 landing page views from 229 link clicks. **This is not a bounce problem.** An earlier draft of this
reading computed 28% using all-clicks and would have raised a false alarm.

### ✅ One InitiateCheckout, from AD4 Builders

Plus 2 AddToCart. Per this plan's own rule: *"a single IC in the first few days is a genuinely good sign
at this volume, and worth more than any CTR number."* **Zero purchases is expected** — $62.75 at a $322
break-even buys ~0.2 of a purchase.

### 🟠 Cost per LPV rose from $0.08 (July) to $0.28 — and that is the fix working

July's campaign was `OUTCOME_TRAFFIC`, so Meta bought the cheapest possible page views. This one is
`OUTCOME_SALES`, so it is hunting purchasers instead. **A 3.5× higher cost per page view is the expected
consequence of the objective change, not a regression.**

### ⚠️ #1 THING TO WATCH — the custom conversion is not attributing yet

The pixel fired `offsite_conversion.fb_pixel_initiate_checkout` (1). But there is **NO
`offsite_conversion.custom.27686282527680441` action on the campaign at all.** That is why `report` says
**Results: 0** while ad-level data shows 1 IC.

Most likely attribution lag on a single event. **But if IC events accumulate by 72h and the `custom.*`
action still never appears, the ad set is optimising toward something Meta cannot measure — which is
July's core failure wearing a new costume.** Flagged in the 72h check-in as the first thing to verify.

### Delivery — Meta concentrated hard and fast

**3 of 6 ads serving. AD5 alone took 63% of spend.** The three carousels got $0.01–$0.17 between them.
Meta picked the three Lawless-photo ads and, of those, favoured **AD5 — the July winner**. Its own
optimiser reached the same conclusion the July data did.

**Do not read that as the carousels failing.** They have had no meaningful chance; no data is not bad
data, and they are protected from the kill rule for exactly this reason.

### Blended account read (7 days to 08-14)

$176.55 spend · 7 results · $8,946 revenue · **$25.22 cost per result**. Flattering, and **retargeting
produced all 7** while the new TOF campaign produced 0. This is the attribution trap: retargeting takes
last-click credit for people TOF warms up. Judge the test on blended CAC over weeks, not on this.

**Next: +72h check-in armed for 2026-08-16 21:00 UTC** — the first point at which the kill rule is
eligible.

---

## 🔴 READING 2 — 72.2h after go-live (2026-08-16 21:01 UTC)

**No actions taken. The kill rule became eligible and was deliberately NOT applied — see below.**

| Ad | Spend | Link CTR | $/link | LPV | $/LPV | ATC | IC | Purch |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AD5 Chippies | $102.67 | 3.65% | $0.31 | 326 | $0.31 | 2 | 0 | 0 |
| AD4 Builders | $38.62 | 3.43% | $0.31 | 123 | $0.31 | 2 | **1** | 0 |
| AD6 Carpenters | $35.05 | 3.61% | $0.31 | 105 | $0.33 | 1 | 0 | 0 |
| 3 carousels | $0.34 | — | — | 1 | — | 0 | 0 | 0 |
| **TOTAL** | **$176.68** | **3.58%** | **$0.31** | **555** | **$0.32** | **5** | **1** | **0** |

*(all_clicks 1,947 vs link_clicks 575 — the `report` headline of "12.13% CTR" is engagement-inflated
again. Real link CTR is 3.58%.)*

### 🔴🔴 THE CUSTOM CONVERSION HAS NEVER FIRED. The test is running blind.

This was flagged as the #1 thing to check at 16h. **72 hours later it is confirmed, not lag.**

| Evidence | Finding |
|---|---|
| `offsite_conversion.custom.27686282527680441` on the campaign | **ZERO — the action type does not appear at all** |
| Ad set `conversions` field | **empty** |
| Custom conversion `first_fired_time` / `last_fired_time` | **not returned — no record of it ever firing** |
| **The pixel, same window** | **34 InitiateCheckout · 10 Purchase** ✅ |

**The underlying events are firing perfectly. The custom conversion built on them is registering
nothing.** The ad set's `promoted_object` points at a conversion Meta appears never to record, so the
optimiser has had **no conversion signal at all for three days** — it has been buying whatever it
guesses. That is precisely the July failure mechanism, in a new costume: July optimised on an event too
sparse to learn from; this optimises on an event that does not arrive.

Object looks correct on inspection — not archived, rule
`{"or":[{"event_name":{"eq":"InitiateCheckout"}},{"event_name":{"eq":"Purchase"}}]}`, data source is the
Craftons Web pixel. **Which is why this needs eyes in Events Manager, not more API poking.**

**Fallback if it is genuinely dead:** optimise on the **standard `InitiateCheckout` event** instead. The
pixel logged **34 IC in ~3.5 days ≈ 68/week raw**, and even deflated ~2.3× for pre-dedup inflation
that is ~30/week — more signal than the pooled custom conversion was ever projected to deliver, and a
standard event Meta definitely attributes. It loses the Purchase pooling; it gains actually existing.

### ⛔ Why the kill rule was NOT applied, even though it fired

At 72h the rule mechanically qualified **AD5 ($102.67), AD4 ($38.62) and AD6 ($35.05)** — all "≥72h AND
≥$25 AND zero results". That is **all three serving ads**, exactly at the 50%-per-run cap.

**Applying it would have been wrong, and the guardrail would have been the thing causing the damage.**

1. **"Zero results" is measuring nothing** while the results counter depends on a conversion that never
   attributes. The gate's third condition is unreliable, so the gate is unreliable.
2. **AD4 did produce a result** — 1 IC and 2 ATC at pixel level. It reads as "zero" only because of the
   attribution failure.
3. It would have deleted **AD5 — the account's best-ever creative** — on a measurement artifact, and
   left the ad set holding three carousels Meta has declined to serve.

> **Rule to carry forward: never kill on "zero results" when results cannot be counted.** Fix the
> measurement first. A kill rule fed a broken denominator is exactly the "$758/result" error the July
> post-mortem already retracted once.

### Signal quality — genuinely better than July, and worse than it needs to be

- **LPV → ATC is 0.9%** (5 of 555). July AD5 managed **0.16%**. **5.6× better traffic quality** — the
  objective change did improve who is arriving.
- **But IC has not moved: 1 at hour 16, still 1 at hour 72**, across $114 of additional spend. ATC went
  2 → 5. **People are adding to cart and not starting checkout.**
- 0 purchases on $176.68 is still statistically unremarkable — at a $322 break-even that spend buys
  ~0.5 of a purchase.

### Blended account read (7 days to 08-16)

$283.35 spend · 6 results · $8,946 revenue · $47.23 cost per result. **Retargeting produced all 6** on
$106.67 while the new TOF campaign produced 0 on $176.68. Attribution trap unchanged.

**Next: 7-day read armed for 2026-08-20 21:00 UTC.**

---

## 🚨 READING 3 — 83h (2026-08-17 07:44 UTC). DELIVERY IS COLLAPSING.

### Today's sales are real, and the ads did not produce them

Three orders, **$3,592**. Checked every one against Shopify's customer-journey data:

| Order | Value | First touch | Closed via | Meta UTM? |
|---|---:|---|---|---|
| #1293 | $2,736 | Google SEO — cavity battens page | **Email** (Trade Program welcome) | ❌ none |
| #1292 | $521 | Google SEO — **straight onto `/products/radius-online`** | same, 1 touchpoint | ❌ none |
| #1291 | $335 | Google SEO — homepage | same, 1 touchpoint | ❌ none |

**No `utm_campaign=radiuspro_tof_aug26` on any of them.** Meta attributes **0 purchases** and **$0 revenue**
to the campaign since launch. Today's revenue is SEO and email doing their job.

> Worth noting who #1292 is: **`paul@wollongongconcrete.com.au` — a concreter — bought $521 of Radius Pro
> landing directly on the product page from Google, in a single touchpoint.** Exactly the buyer the ads
> are chasing, arriving for free.

**Pixel inflation confirmed:** 7 pixel Purchases today vs **3 real Shopify orders** = **2.33×**, matching
the documented 2.3× factor.

### 🚨 The smoking gun: delivery has fallen 86% in three days

| Day (Melbourne) | Spend | Impressions | Link clicks | LPV | IC |
|---|---:|---:|---:|---:|---:|
| 08-14 | $63.05 | 6,934 | 230 | 222 | 1 |
| 08-15 | $65.56 | 5,671 | 227 | 217 | 0 |
| 08-16 | $48.28 | 3,458 | 118 | 116 | 0 |
| **08-17** | **$14.73** | **998** | **24** | **23** | **0** |

Budget is **$75/day** and it has **never once been hit**. Today it is spending **20% of budget** with
~75% of the day gone. `learning_stage_info` is **empty** — not LEARNING, not LEARNING_LIMITED, *nothing*
— and `issues_info` is empty too, so Meta reports no policy or setup fault.

**This is the textbook signature of an optimisation target that never converts.** The optimiser is told
to find people who will trigger conversion `27686282527680441`. That conversion has never fired, so it
cannot build a model, cannot find look-alikes, loses confidence, and throttles spend. **It is not a
budget, creative or targeting problem. It is the broken conversion starving the optimiser.**

### The creative is NOT the problem — that part is working

| Metric | This test | July AD5 |
|---|---:|---:|
| Link CTR | **3.58%** | — (July's "10.45%" was all-clicks) |
| Link click → landing page view | **96.9%** | — |
| LPV → AddToCart | **0.9%** | **0.16%** |

**5.6× better traffic quality than July.** The objective change fixed *who arrives*. What's broken is
whether Meta can *measure* what they do next.

### ⛔ Still no kills. Same reason, now stronger.

Cumulative: $191.62 · 578 LPV · 6 ATC · 1 IC · 0 purchases. AD5 ($102.67) and AD6 ($35.05) still read
"zero results" — and that reading is still measuring nothing. **Do not kill creative to fix a
measurement fault.**

### ➡️ The fix: repoint the ad set at an event Meta actually records

Change the ad set's conversion event from the custom conversion to the **standard `InitiateCheckout`**.
Two minutes in Ads Manager: Ad set → Conversion → Event. Whatever the true weekly IC volume is, it is
more than the **zero** the optimiser currently sees.

There is no `update_ad_set` change type in the tool, so this is either a manual edit or a small build.

**If it can't be fixed today, pausing the ad set is defensible** — it is buying traffic with no
optimisation behind it. The bleed is self-limiting (down to $15/day), so this is not urgent by the hour,
but every day it runs broken is a day of the test wasted.

### 🔴 CORRECTION to the 72h note above

That note said the pixel showed *"34 IC in ~3.5 days ≈ 68/week raw"* and used it to argue standard IC has
ample volume. **That figure is not sound.** The `/{pixel}/stats` endpoint does not window reliably:
`start_time=2026-08-17` (one day) returns **44 IC**, which is *more* than `start_time=2026-08-13` (four
days) returns at **34**. Those cannot both be right, so no weekly rate should be quoted from it — and the
30-day figures earlier in the project may share the flaw.

**What is trustworthy:** Shopify order counts, and Meta's own ad-level `actions`. **Use those.** The
recommendation above does not depend on the discarded number.

**Next: 7-day read armed for 2026-08-20 21:00 UTC.**

---
## ✅ READING 4 — 83h after the **v2** relaunch (2026-08-20 22:01 UTC / Aug 21 08:01 Melbourne)

**First reading of a test that is actually measurable.** Readings 1–3 measured a campaign optimising on
a conversion that never fired. This one has a live optimisation event and working attribution, so for
the first time the numbers mean what they say.

**Verdict: HOLD. Do not kill the ad set.** One ad (AD6) mechanically qualifies under the coded rule —
proposed below, not applied. LAW 1: nothing was changed.

### State — verified live, not from memory

| Object | State |
|---|---|
| v2 ad set `120247812165960186` | `ACTIVE` / effective `ACTIVE` · **$65.00/day** · `OFFSITE_CONVERSIONS` |
| `promoted_object` | `pixel 677437638374055` + `INITIATED_CHECKOUT` ✅ unchanged |
| geo | `["AU"]` ✅ |
| 6 ads | all `ACTIVE` / effective `ACTIVE` ✅ |
| Retargeting `120233074187690186` | `ACTIVE` $15.00/day ✅ left alone |

### v2 only, since activation (Aug 17 → 20)

| Day | Spend | Impr | Link clicks | Link CTR | ATC | IC | Purchase |
|---|---|---|---|---|---|---|---|
| Aug 17 *(3h)* | $9.49 | 1,199 | 53 | 4.42% | 5 | 0 | 0 |
| Aug 18 | $73.55 | 8,298 | 267 | 3.22% | 3 | 0 | 0 |
| Aug 19 | $40.54 | 3,765 | 142 | 3.77% | 1 | 0 | 0 |
| Aug 20 | $42.18 | 3,804 | 112 | 2.94% | 0 | 0 | 0 |
| **Total** | **$165.76** | **17,066** | **574** | **~3.4%** | **9** | **0** | **0** |

**Cost per link click $0.29. Cost per ATC $18.42. LPV→ATC ≈ 1.63%** (~552 LPV).
That LPV→ATC is **better than the 0.9% benchmark and ~10× July's 0.16%.** Traffic quality is not the
problem.

### Does the kill rule fire?

Rule: **≥72h AND ≥$25 AND zero results**, per ad, max half the batch, and *an ad with results is never
killed*.

| Ad | Spend | Link clicks | ATC | Qualifies? |
|---|---|---|---|---|
| AD5 Chippies | $84.14 | 308 | **7** | ❌ protected — has results |
| AD4 Builders | $44.05 | 141 | **2** | ❌ protected — has results |
| **AD6 Carpenters** | **$25.67** | 92 | **0** | ✅ **QUALIFIES** |
| AD1 Concreters | $5.63 | 14 | 0 | ❌ under $25 |
| AD2 Landscapers | $2.15 | 11 | 0 | ❌ under $25 |
| AD2b Landscapers | $4.12 | 8 | 0 | ❌ under $25 |

**Exactly one ad qualifies — AD6 Carpenters.** 1 of 6, well inside the 50% cap.

### Why the ad set is NOT killed, and why this is different from Reading 3

Reading 3's refusal was *"never kill on zero results when results cannot be counted."* **That escape no
longer applies — results can be counted now** (9 ATC attributed, EMQ Purchase 8.3). So the refusal has
to stand on the evidence, not on a measurement excuse:

1. **The ads produce attributed bottom-funnel intent.** 9 ATC in 83h at $18.42 each. A dead campaign
   does not generate ATC.
2. **Zero IC is within noise.** Site-wide ATC→IC ran 28% over Aug 18–20 (22 IC / 78 ATC). 9 ATC predicts
   **~2.5 IC**; observing 0 has probability **e^-2.5 ≈ 8%**. Unlucky, not damning. **n=9 cannot carry a
   kill decision.**
3. **Delivery is not collapsing.** Aug 18–20 ran $73.55 / $40.54 / $42.18 — underpacing the $65 budget
   at roughly 62–65%, but nothing like Reading 3's **86% collapse**. Different signature entirely.

### ⚠️ The two genuine negative signals, stated plainly

- **ATC is trending down: 5 → 3 → 1 → 0.** Four points, tiny n, and Aug 17 is a 3-hour stub, so this may
  be nothing. But it is the single thing most likely to justify a kill at day 7.
- **Delivery underpaces at ~62–65% of budget**, consistent with Meta not finding IC-likely users.

### 🔎 A hypothesis I formed and then disproved — recorded so nobody re-forms it

I was going to report that **`InitiateCheckout` is too sparse an event to optimise on** — a mild cousin
of the Aug26 error — on the basis that site IC looked like ~9/day (~63/week) against Meta's ~50/week
learning threshold. **Checked before writing it, and it is wrong.**

The 72h note warned `/{pixel}/stats` does not window reliably (*"one day returns 44, four days returns
34"*). **That flaw does not reproduce today.** Nested windows are monotonic and self-consistent:

| `start_time` | span | IC | ATC | Purchase |
|---|---|---|---|---|
| 2026-08-20 | 1d | 9 | 21 | 5 |
| 2026-08-19 | 2d | 18 | 45 | 8 |
| 2026-08-18 | 3d | 22 | 78 | 8 |
| 2026-08-17 | 4d | 81 | 252 | 21 |
| 2026-08-14 | **7d** | **116** | 386 | 25 |

Each nests correctly inside the next. **Site-wide IC is ~116/week — comfortably above the ~50/week
learning threshold.** The event has ample volume; v2 simply is not capturing it yet.
*(Aug 17 alone contributed 59 IC — a spike worth understanding, not a typo.)*

### Blended account read (7 days to Aug 20)

| Metric | Value |
|---|---|
| Spend | $469.52 |
| Results | 3 — **all from retargeting** ($100.24) |
| Revenue | $4,291.00 |
| Cost per result | $156.51 |
| MTD | $884.95, projected $1,269.95 of the $2,000 ceiling |

TOF campaign spend of $369.28 includes **v1's pre-pause spend**, since the 7-day window opens Aug 14 and
v1 was retired Aug 17. **v2's own spend is $165.76.** Do not read the campaign row as v2's performance.

⚠️ `report` warns **2 live ad sets** against policy `MAX_AD_SETS` = 1. This is the known, accepted
retargeting exception — it produces every attributed result on the account. Not an action item.

### Recommendation

1. **HOLD the ad set.** Re-read at **7 days (2026-08-24)**. Readable CAC is still 3–4 weeks out.
2. **Propose pausing AD6 Carpenters** — the one ad the coded rule qualifies. Narrow, reversible, and it
   concentrates budget on AD5/AD4, which are producing. **Honest caveat:** AD6's zero is *also* within
   noise (92 clicks at AD5's rate predicts ~2.1 ATC; P(0) ≈ 12%). The case for acting is that the rule
   exists so these calls are not re-litigated each time, not that AD6 is proven bad.
3. **Do not touch budget.** Ladder step needs CAC ≤ $322, and CAC is not yet computable for v2.
4. **At day 7, kill criteria:** if ATC stays at 0–1/day *and* IC is still 0 on >$300 cumulative, that is
   a real kill case with an adequate denominator.

**Next: 7-day read armed for 2026-08-24.**

---

## ⏱ When do we cut ads, and when do we touch budget?

All constants read from `_meta-policy.mjs`, not from memory.

| Constant | Value |
|---|---|
| `MIN_AGE_HOURS_BEFORE_KILL` | **72h** |
| `MIN_SPEND_AUD_BEFORE_KILL` | **$25** per ad |
| `MAX_KILL_FRACTION_PER_RUN` | **50%** of the batch per pass |
| `MAX_BUDGET_INCREASE_FRACTION` | **+20%** per step |
| `MAX_DAILY_BUDGET_AUD` | **$100/day** (Lee's hard cap) |
| `MONTHLY_CEILING_AUD` | **$2,000** |
| `BREAK_EVEN_CAC_AUD` | **$322.09** |
| `TARGET_CAC_AUD` | **$178.94** |

### Cutting an ad — three conditions, ALL required

**≥72 hours old** AND **≥$25 spent on that ad** AND **zero results.** Never more than half the batch
in one pass.

The third condition is the one people skip. **An ad Meta chose not to serve has told us nothing — no
data is not bad data.** At $50/day across 6 ads, Meta will concentrate quickly: two or three ads will
clear $25 within 1–2 days while the others may never get there. Those starved ads are not losers and
must not be cut on a spend figure they never had a chance to reach.

**So: first legitimate cuts land around day 3–5**, and only for ads with real spend and no results.

### Touching budget — not until CAC is known, which takes weeks

A budget decision needs a **readable CAC**, and that needs roughly **10 conversions**. The arithmetic:

| Daily | Monthly | Conversions/month at $322 CAC | at $179 CAC |
|---|---|---|---|
| $35 (coded `validation` stage) | $1,050 | ~3 | ~6 |
| **$50 (proposed)** | **$1,500** | **~4.7** | **~8.4** |
| $65 (`signal` stage) | $1,950 | ~6 | ~11 |

**So ~10 conversions is a 4–6 week sample at $50/day.** Anyone who wants a budget answer sooner is
asking for one the data cannot give.

**The ladder, once CAC is known and at or under break-even:**

```
$50 → $60 → $72 → $86 → $100 (hard cap)
```

+20% per step, **at least a week between steps.** Meta resets the learning phase on large jumps, so
four small raises beat one big one. July's 13×-in-one-step is unreachable in code now.

**Do not raise budget on a good CTR.** Raise it on CAC at or under $322, ideally under $179.

### 🔴 The one signal that justifies stopping early

There is a legitimate early kill, and it is not "low CTR". It is **July's exact signature**:

> **Lots of cheap clicks and ZERO InitiateCheckout.**

If by roughly **$300–400 of spend** the ads have produced hundreds of landing page views and **not one
IC**, the problem is downstream of the ad — the landing page, the offer, or the product match — and
spending on to 10 conversions will not find it. Pause and diagnose instead.

Conversely **a single IC in the first few days is a genuinely good sign** at this volume, and worth more
than any CTR number.

### ✅ SETTLED — $50/day, confirmed by Lee 2026-08-13

`BUDGET_STAGES.validation` is **$35/day** ("wk 1–2 — prove tracking + creative, not performance").
**Lee's call: launch at $50/day.** A deliberate override of the stage default, not a violation — it sits
under the $100 hard cap and the stage is config-driven. It buys a readable sample roughly 40% faster
than $35 would.

The +20% ladder therefore starts from $50: **$50 → $60 → $72 → $86 → $100 (hard cap)**, a week between
steps, and only once CAC is at or under $322.

---

## The schedule

| When | What happens | Actions permitted |
|---|---|---|
| **+16h** | `report` run. Per-ad CTR, CPC, LPV, cost/LPV, any IC. Delivery spread check | **None.** Report only |
| **+72h**, ads with ≥$25 | `evaluate` run. Coded kill rule becomes eligible | **Propose** pausing zero-result ads. Lee approves |
| **+7 days** | Blended account-level read | Still no scaling. A week at $50/day is ~$350 = 1–2 conversions. Noise |
| **+3–4 weeks** | The real read: **true CAC vs the $322 break-even** | Budget decisions, winner cloning |

**Read blended at account level, not per-campaign.** Retargeting is live at $15/day and will take
last-click credit for people the new TOF ads warm up — the exact attribution trap from the July
post-mortem.

**Budget increases are capped at +20% per step** in code, because Meta resets the learning phase on
large jumps. July's 13×-in-one-step is unreachable now.

---

## ⛔ Blocked: nothing is live, so the clock has not started

As of writing, **the account has no new campaign, no new ad set and no new ads.** The chain is:

1. ⬜ **Lee approves EXACTLY ONE ROW** — `9cf62557-0f55-495c-a17e-d6ed115df9fc`
   (`RadiusPro | TOF | Aug26`, OUTCOME_SALES) at **https://cnccut.app/marketing/meta-ads**

> ### 🔴 DO NOT "approve all" — there are 9 pending rows and two are landmines
>
> | # | Date | Action | |
> |---|---|---|---|
> | 1–4 | 2026-07-07/08 | `add_negative_keyword` ×4 | stale, Google Ads |
> | 5 | 2026-07-20 | `generate_asset` | stale |
> | 6 | 2026-08-06 | `pause_campaign` | stale — check what it targets before touching |
> | 7 | 2026-08-06 | `publish_ad` | ⛔ **`ZZTEST \| pipeline test — do not enable`**, creative_id `ZZTEST_PLACEHOLDER_DO_NOT_APPROVE` |
> | 8 | 2026-08-06 | `set_budget` | ⚠️ **$100/day onto ad set `120247183658270186`** — that is the OLD July ad set, inside the **OUTCOME_TRAFFIC** campaign. Approving it puts $100/day behind the exact setup we are replacing |
> | **9** | **2026-08-13** | **`create_campaign`** | ✅ **THIS is the one to approve** |
>
> The batch endpoint takes explicit IDs and is deliberately not "approve everything pending" — good.
> **Approve row 9 only.** Rows 7 and 8 should be rejected outright.
2. Claude applies it → campaign exists, PAUSED
3. Claude proposes ad set + 6 ads → Lee batch-approves → Claude applies → all PAUSED
4. 🔒 **Lee toggles it on.** LAW 1 — there is no code path that activates an ad
5. **The 16h clock starts at step 4**, not before

> **Why Claude cannot approve step 1:** it tried, and the permission layer blocked the write to
> `marketing_approvals` — correctly. An agent flipping its own proposal to "approved" is exactly what
> the human gate exists to prevent. The approval has to come from Lee.

### Ready and waiting

Six corrected creatives are built and validated against Meta:

| Creative | Ad | Correction |
|---|---|---|
| `1078072304563046` | AD5 Chippies (**the 10.45% winner**) | "Laminate two to 34mm" → **"Double them up to 34mm"** · UTM → `aug26` |
| `801056473070934` | AD4 Builders | same |
| `3695505940601153` | AD6 Carpenters | same |
| `954057387710539` | AD1 Concreters carousel | UTM → `aug26` |
| `1036744315626177` | AD2 Landscapers carousel | UTM → `aug26` |
| `1379645754375539` | AD2b Landscapers carousel | UTM → `aug26` |

**"Laminate" is on Lee's banned list and shipped in all three Lawless ads in July.** Duplicating them
unchanged would have re-shipped it.

---

## 📕 Reading 4 — +7 days (2026-08-20). The last one for this test.

**Full working: `aug20-seven-day-read.md`. This is the summary and the decision.**

v2 was activated 2026-08-17 on Lee's approval and ran 3.5 days at $65/day.

| | v2 |
|---|---:|
| Spend | $165.66 |
| Landing page views | 553 |
| Add to cart | 9 (1.63% of LPV) |
| **InitiateCheckout** | **0** |
| Shopify orders | **0** |

### The kill rule fires, and this time it is not refused

The three earlier readings all refused the kill rule under the same standing rule — *never kill on
"zero results" when results cannot be counted.* That protection no longer applies:

- v2 optimises on **standard `InitiateCheckout`**, which fired 19 times account-wide in August.
- Shopify journey attribution **demonstrably captures Meta clicks** (verified against 60 orders).

The denominator is real now. The result is genuinely zero.

**And the decision does not rest on 3.5 days.** It rests on **$1,649.12 of TOF spend across three
campaigns and two months producing one traceable $362 order.**

### What the readings got right, and the one thing they missed

Right: refusing to cut creative on a broken denominator, three times running. Had those cuts been
made, the creative would have been blamed for a measurement fault, and v2's 4× improvement in
LPV→ATC (0.40% → 1.63%) would never have been visible.

Missed: **every reading looked at the test in isolation.** None compared it to the retargeting ad set
sitting beside it — $15/day, budget-capped every single day since October 2025, frequency 1.6, 62
purchases at $52 each. The comparison is what turns "TOF is underperforming" into "the money is in
the wrong place", and it was available at reading 1.

**Rule to carry forward: read every test against the best-performing thing already in the account,
not only against its own targets.** A test that fails in isolation is a data point. A test that fails
while a proven ad set next to it runs out of money daily is a misallocation.

### Proposed, pending Lee

| Change | approval_id |
|---|---|
| Pause TOF v2 `120247812165960186` | `d8391efe-4388-4b9e-9c5e-fb2e027dc5da` |
| Retargeting `120233074187690186` $15 → $18/day | `25d9597c-3363-4e23-8e95-f933ead563a6` |

Per this plan's own escalation table — *"Propose pausing zero-result ads. Lee approves."* Rung 0.
Nothing applied.
