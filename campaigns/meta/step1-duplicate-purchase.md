# Step 1 — The duplicate Purchase question: RESOLVED, no fault

> ## ✅ CLOSED 2026-08-03 — there was no duplication. Measurement artefact.
>
> **Settled with a live production test.** Two real orders landed in the same hour:
> `#1274` 04:43:02 UTC ($2,336) and `#1275` 04:44:40 UTC ($1,048).
>
> The pixel recorded, in that hour: **2 BROWSER + 2 SERVER**, all on `craftons.com.au`.
>
> **That is exactly one browser and one server event per order — correct behaviour.**
>
> ### What went wrong in the analysis
>
> Meta's `/{pixel_id}/stats` endpoint reports events **before deduplication**. Browser and server
> each get counted, then collapse by shared `event_id` for actual attribution. The original finding
> (97 pixel Purchase events vs 36 Shopify orders) compared a **raw pre-dedup event count** against an
> **order count** — not a like-for-like comparison, and not evidence of a fault.
>
> The signal that should have caught this sooner: **Meta's own Actions tab never flagged duplicate
> events.** Meta detects genuine duplication reliably. That absence was noted and under-weighted.
>
> ### One loose end, not a blocker
>
> Historically the daily split showed server ≈ 2× orders while browser ≈ 1× (e.g. 21 Jul: 3 orders,
> 3 browser, 6 server). Today's orders produced 1 server each. The difference: today's two orders
> were both on `craftons.com.au` with **no `shop.app`** involvement, whereas 24 of the 30-day Purchase
> events came from `shop.app` (Shop Pay).
>
> **Hypothesis: Shop Pay checkouts fire an additional server-side Purchase.** Worth confirming on a
> future Shop Pay order, but it is not a blocker and nothing should be removed over it.
>
> ### Conclusion
>
> **No action required. Nothing to remove. Phase 0's blocker does not exist.**
> The sections below are retained as the diagnostic record only — **their conclusions are superseded
> by this box.**

---

_The single highest-value fix in Phase 0. Diagnosed 2026-08-03 from the pixel's own data._
_Parent doc: `conversion-tracking.md`._

---

## The diagnosis (this is not guesswork — it's the daily data)

I pulled Purchase events split by source, day by day, and lined them up against Shopify's actual orders.

| Date | **Shopify orders** | Meta **browser** | Meta **server** | Meta total |
|---|---|---|---|---|
| 20 Jul | 1 | 1 | 2 | 3 |
| 21 Jul | 3 | 3 | 6 | 9 |
| 23 Jul | 2 | 2 | 4 | 6 |
| 24 Jul | 1 | 1 | 2 | 3 |
| 29 Jul | 2 | 1 | 2 | 3 |
| 1 Aug | 1 | 1 | 2 | 3 |
| 2 Aug | 1 | 1 | 2 | 3 |
| **14-day total** | **14** | **13** | **27** | **40** |

**Read the columns:**

- ✅ **Browser is correct.** 13 browser events against 14 real orders. The browser pixel is behaving.
- 🔴 **Server fires exactly twice per order.** 27 against 14 orders — and it's `2×` on *every single
  day*, not an average. That regularity means **two server-side integrations are both sending
  Purchase**, not a flaky one firing intermittently.
- 🔴 **Browser and server aren't deduplicating.** They add (1 + 2 = 3) instead of collapsing. Properly
  deduplicated, one order should produce **one** counted Purchase.

**Net effect: every order is counted three times.** 14 orders → 40 events. Over 30 days: 36 orders →
97 events. That's the 2.7× from the parent doc, now fully explained.

**Also seen:** by host, Purchase splits `craftons.com.au` 73 / `shop.app` 24. `shop.app` is Shop Pay's
domain — those are real checkouts, not a third bug, but they're subject to the same double-fire.

---

## What this means

There are **two separate faults**, and fixing only one won't get you to parity:

| Fault | Symptom | Fix |
|---|---|---|
| **A. Two CAPI sources** | server = 2× orders | Find and remove one (§ below) |
| **B. No browser↔server dedup** | browser + server add instead of collapsing | Shared `event_id` |

Fix A and you go from 3× to 2×. Fix B as well and you land on 1×.

---

## The fix — in order of likelihood

### 1️⃣ Most likely: a Meta-side Shopify integration *and* the Shopify-side channel

This is the classic cause of "server fires exactly twice", because both are doing their job correctly
— nobody told either that the other exists.

1. Go to **Events Manager → Data sources → Craftons Web (`677437638374055`)**.
2. Open the **Settings** tab, then find **Partner Integrations** (sometimes "Manage Integrations" or
   "Connected partners").
3. **Look for a Shopify integration set up from Meta's side.**
4. Now check the other end: **Shopify admin → Settings → Apps and sales channels → Facebook & Instagram**.
5. **If both exist, you've found it.** Remove the Meta-side partner integration and keep the Shopify
   channel — the channel is better maintained, handles Shop Pay, and sends richer customer data.

> ⚠️ **Remove one, not both.** If you delete the Shopify channel too you'll lose Purchase tracking
> entirely and the account goes blind.

### 2️⃣ Next: a third-party tracking app also sending CAPI

Apps like Elevar, Fueled, Trackify, Aitarget, OmegaTheme and similar all offer "server-side Meta
tracking" and will happily fire Purchase alongside the native channel.

1. **Shopify admin → Settings → Apps and sales channels → All apps.**
2. Scan for anything doing analytics, attribution, tracking or "server-side tagging".
3. For any you find, open its settings and look for a Meta/Facebook pixel ID — **especially
   `677437638374055`**.
4. If one is sending Purchase server-side, turn *that* off (not the whole app, if it does other work).

### 3️⃣ Then: a custom pixel in Customer events

1. **Shopify admin → Settings → Customer events.**
2. Look for any **custom pixel** (not the Facebook & Instagram app pixel).
3. Open it and check for `fbq('track', 'Purchase'` or a `fetch` to `graph.facebook.com/.../events`.
4. Remove the Purchase call if present.

### 4️⃣ Confirm what Meta already thinks

Meta usually detects this itself and will name the sources for you:

1. **Events Manager → Data sources → Craftons Web → Diagnostics.**
2. Look for **"Duplicate events"**, **"Multiple sources sending the same event"**, or
   **"Server and browser events not deduplicated"**.
3. This tab often points straight at the culprit — **check it first, it may save you steps 1–3.**

### 5️⃣ Then fix the dedup (Fault B)

Once there's only one CAPI source:

1. **Shopify admin → Facebook & Instagram → Settings → Data sharing** → set to **Maximum**.
   The native integration then sends browser and server events with a shared `event_id` automatically.
2. Re-check **Events Manager → Purchase → View details**. You want to see a **"Deduplicated"** figure,
   not just Browser and Server totals sitting side by side.

> **Do not touch `CORRECTED_FULL_SECTION.liquid`.** It contains `fbq` calls, but they relay the
> configurator's AddToCart / InitiateCheckout events and already dedupe correctly by `event_id`.
> It does not fire Purchase. It is not part of this problem.

---

## ✅ Verification

**Immediately after the change,** in Events Manager → Test Events, place a test order and confirm
**exactly one** Purchase is recorded.

**After 48 hours,** the real check — daily pixel Purchase should equal daily Shopify orders, ±1:

| | Now | Target |
|---|---|---|
| Events per order | **~3×** | **1×** |
| 30-day Purchase count | 97 | ≈36 |

**I can verify this for you.** I have both data sources wired — say the word and I'll re-run the
comparison and tell you whether it landed, rather than you eyeballing dashboards.

> ⏱ **Expect a ~1-day offset** between the two systems: Meta reports in UTC, Shopify in Melbourne
> time. Compare weekly totals rather than single days, or you'll chase a phantom.

---

## How to settle it properly

**Test Events has a limitation:** its test code applies to browser events. Shopify's server-side
Purchase won't carry the code, so **server events may not appear in the test panel at all** — which
is precisely the half in question.

**Better: use the real production path and count it.**

1. Note the exact time.
2. Place **one real order** (refund it afterwards).
3. Wait ~30–60 minutes for Meta to process.
4. Ask Claude to query the pixel for that window and count Purchase events by source.

**One order → one counted Purchase** means nothing is broken and Phase 0 loses its blocker.
**One order → three** confirms real duplication.

## Why this mattered enough to chase

Andromeda picks who sees your ads by correlating **creative** against **conversion signal**. Two of
every three conversions it has been learning from never happened — so it has been optimising toward
whatever pattern produces *duplicate firing*, which is noise.

It also means every performance number in the account is inflated. The **8.7× ROAS** in the bible's
§4.5 is measured on real revenue so it holds, but the **21 "results"** figure does not — the true
count is nearer 8. Cost per result is roughly **three times worse** than the dashboard says.

Fix this and every subsequent decision the agent makes rests on real numbers.
