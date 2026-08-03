# Sabri Suby's 8 hacks — Craftons implementation

_Written 2026-08-03 at Lee's request. Source: Drive `MARKETING-BIBLE.md` §9 (from Suby's "8 hacks I
wish I knew sooner", $300M+ spend). This doc turns the hacks into what we actually build, checked
against the real account._

> **Read first:** `radius-pro-product-truth.md` (what the product is) · `radius-pro-ad-copy.md` (the
> copy). This doc is the *strategy*; those are the *facts* and the *words*.

---

## 🔴 First — the July post-mortem was wrong, and it changes the plan

Every doc in this repo has repeated a claim that does not survive contact with the account data:

> ~~"Never segment creative by trade. July ran separate ads for Chippies, Carpenters, Builders,
> Concreters and Landscapers and every trade-identity ad lost. AD5 Chippies cost $758/result."~~

**Lee challenged this. He was right.** Pulled from the Marketing API, July 2026:

### What the ad sets actually were

| Ad set | Optimisation | Promoted event | Targeting |
|---|---|---|---|
| `TOF \| Broad AU \| AddToCart` | `OFFSITE_CONVERSIONS` | **`ADD_TO_CART`** | **Broad AU, no interests** |

**All five trade ads sat in that one ad set.** July did **not** segment the audience. It ran broad
targeting with identity words in the creative — **which is exactly what hack #2 prescribes.** The
"segmentation" I objected to was creative variation, which is the entire point of the hack.

### What the creative actually did

| Ad | Spend | CTR | Link clicks | Landing page views | Cost/LPV | Reactions | Saves |
|---|---:|---:|---:|---:|---:|---:|---:|
| **AD5 Chippies** | $739.53 | **10.45%** | 9,306 | **9,244** | **$0.08** | 132 | 12 |
| AD4 Builders | $39.40 | 9.94% | 212 | 201 | $0.20 | 6 | 5 |
| AD1 Concreters | $110.41 | 9.39% | 1,200 | 1,131 | $0.10 | 19 | 1 |
| AD6 Carpenters | $71.37 | 9.18% | 795 | 824 | $0.09 | 22 | 2 |
| AD2 Landscapers | $182.77 | 7.51% | 2,026 | 1,912 | $0.10 | 39 | — |
| _Retargeting (the "winner")_ | $446.76 | _1.72%_ | 352 | 320 | _$1.40_ | 30 | 23 |

**A 10.45% CTR is exceptional.** The trade-identity creative was the best-performing hook the account
has ever run. It was not the failure.

### What actually failed

**The optimisation event had no signal to learn from.** The ad set optimised for `ADD_TO_CART`. The
account produces roughly **15 ATC and 13 purchases a month** — far under the **~50 events/week** Meta
needs to exit the learning phase. Starved of conversion signal, delivery collapses to whoever clicks
cheapest. That is exactly the observed signature: huge CTR, $0.08 traffic, almost nothing downstream
(9,244 landing page views → 15 add-to-carts).

**The "$758/result" figure divided real spend by a broken denominator.** It was evidence about event
volume, not about creative.

### The three real lessons

1. **Fix the optimisation event before blaming creative.** → The combined custom conversion
   (`InitiateCheckout` OR `Purchase`) exists precisely to pool events over the learning threshold.
   **This is now the highest-priority item in the whole build**, not a tidy-up.
2. **We had no capture mechanism.** 12,718 clicks and ~13,000 landing page views arrived, and we
   captured **zero** email addresses. That is Pillar 2's "missing middle" costing real money, and it
   is the single biggest structural gap.
3. **TOF probably did work — attribution just can't show it.** Retargeting produced **11 purchases on
   $446** in the same month. Retargeting *whom?* The audience TOF built. Last-click credits the
   retargeting ad for demand the trade ads created.

> **The corrected rule:** identity words in the creative on **broad** targeting is doctrine, and the
> account supports it. **What must never be repeated is optimising on an event we can't generate
> enough of.**

---

## The 8 hacks — status and action

| # | Hack | Status | What we do |
|---|---|---|---|
| 1 | **Statics beat video, win on volume** | ✅ Doing | `render-ads.mjs` makes statics as HTML. Batch raised to **24** |
| 2 | **Identity keyword — creative IS targeting** | 🔄 **Reinstated** | Identity variants back in the launch batch. Broad AU targeting |
| 3 | **Clone winners; zombie relaunch** | ⏳ Ready | `winners` joins performance to recipe. Needs a clean winner first |
| 4 | **Don't look like ads — run native** | 🔴 **Biggest creative gap** | Current renders are catalogue cards. See below |
| 5 | **Broad targeting + specific copy** | ✅ Doing | Already policy. July proves it works at the hook level |
| 6 | **Ad ↔ landing page scent match** | ❌ Not started | Ads point at `/products/radius-online` with no headline congruence |
| 7 | **Retarget with a different offer** | 🔴 Blocked on capture | Product spread is the engine. Nothing built |
| 8 | **Track net cash, not ROAS** | 🟡 Partial | `cac` computes true CAC ($152.15 vs $322.09 break-even) |

### Hack 1 — statics on volume
Andromeda needs a constant flood of fresh creative. Statics are cheap; the renderer is HTML, not AI,
so marginal cost is near zero. **Action: the launch batch goes from 15 → 24**, and the weekly cron
should cut fresh variants from whatever is winning.

### Hack 2 — the identity keyword ⭐ reinstated
Andromeda reads the image, copy, offer and page to find the buyer, so **put the audience in the ad**.
July proved this pulls attention at 7.5–10.5% CTR. **Action: identity variants ship in the launch
batch** — Chippies, Builders, Concreters, Formworkers, Landscapers — all in **one broad AU ad set**,
never split into separate audiences.

> **This is also where the joiner-block copy finally goes.** Joiner blocks are concreters-only
> (`radius-pro-product-truth.md`), which made them unusable in general copy — but they're perfect in a
> concreter identity variant. The hack unlocks a true claim we'd had to shelve.

### Hack 3 — clone the winner, and the zombie relaunch
When one wins, don't ride it to fatigue — generate variations and let a CBO pivot spend. **The zombie
move:** high-conviction ads that got no spend get relaunched in their own ad set, worth ~20% more
winners. **We have zombies already** — AD4 Builders spent $39 at a 9.94% CTR before delivery starved
it. That ad never got a fair run.

### Hack 4 — don't look like an ad 🔴
**The weakest part of the build.** `BUILD-CHECKLIST.md` B4 already flagged the renders as catalogue
cards. Suby's test: if it reads as an ad, it's dead on arrival. Our version of native isn't clowning —
it's a real part on a real site, a plan with a radius on it, a stack of plates on a ute tray.
**Action: this is the brief for the re-render, not just "fix the arc".**

### Hack 5 — broad targeting, specific creative
Already policy and already validated: the July ad set was broad AU with no interest stacking and
returned a 10.45% CTR. Keep. **Never re-introduce interest targeting** — older ad sets in the account
used `flexible_spec` and are the ones that went nowhere.

### Hack 6 — scent match ❌
Meta is the best split-tester on earth; headlines are seen ~1000× more than the page. Run many
headline variants, then **mirror the winner on the landing page**. **Action:** once a headline wins,
the top of `/products/radius-online` must open with that line. Worth +15–20% conversion, and it's free.

### Hack 7 — retarget with a different offer 🔴
They didn't buy because *that* offer wasn't right. Craftons' product spread is the retargeting engine:
bounced off Radius Pro → Formwork Builder, Architrave Builder, Rip Pro, Arch Kit.
**Blocked on the same missing middle** — there's no capture, so there's nothing to nurture. July's
~13,000 landing page views are gone. **Fixing capture is worth more than any copy change.**

### Hack 8 — net cash, not ROAS
`cac` already computes true CAC. 30-day actuals: **$1,977.92 spend · $17,285 revenue · 8.7× ROAS ·
true CAC $152.15 vs $322.09 break-even.** We are comfortably inside break-even, which per Suby means
**scale toward it, don't cap spend on a ROAS percentage.**

---

## What this changes, in priority order

1. 🔴 **Create the combined custom conversion.** It is the fix for what actually broke July. Awaiting
   Lee's word — account write.
2. 🔴 **Re-render creative to be native, not catalogue cards** (hack 4) — and fix the wrong product
   while we're in there.
3. 🟠 **Reinstate identity variants** (hack 2) — done in `radius-pro-ad-copy.md`.
4. 🟠 **Build capture** (hacks 6+7, Pillar 2). The Field Guide lead magnet. Biggest structural gap.
5. 🟡 **Scent-match the landing page** to the winning headline (hack 6) once one exists.

## Ledger of what I got wrong

Recorded because this repo's failure mode is losing corrections, not making them:

- **Claimed trade segmentation failed.** It never happened — one broad ad set, creative variation only.
- **Repeated "$758/result" as evidence about creative.** It was a broken denominator.
- **Wrote an "anti-angle" section banning identity words**, which contradicted the bible's own hack #2,
  and reconciled the contradiction in favour of the wrong side.
- **Treated the retargeting ad as the winner and TOF as the loser** on last-click, when TOF built the
  audience retargeting converted.

**The tell I missed:** a 10.45% CTR sitting next to "this creative failed" should never have passed
without question. The engagement numbers were in the same API response as the spend numbers all along.
