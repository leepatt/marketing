# Lee's tasks — step by step (updated 2026-08-17, second pass)

> # 🔴 THE 7-DAY READ IS IN — 2026-08-20. TOF DOES NOT WORK.
>
> The reading this banner was waiting for has been done, against the live Meta and Shopify APIs.
>
> **v2 ran 3.5 days: $165.66 · 553 landing page views · 9 add-to-carts · 0 checkouts · 0 orders.**
> **TOF all time: $1,649.12 across three campaigns and two months → one traceable $362 order.**
>
> Meanwhile **retargeting returns roughly ten times its cost and runs out of money every single day**
> at $15/day, frequency 1.6 — nowhere near saturated. The money is in the wrong place.
>
> **Two changes proposed. Nothing has touched the account.**
>
> | Change | approval_id |
> |---|---|
> | **Pause TOF v2** `120247812165960186` | `d8391efe-4388-4b9e-9c5e-fb2e027dc5da` |
> | **Retargeting `120233074187690186` $15 → $18/day** | `25d9597c-3363-4e23-8e95-f933ead563a6` |
>
> Full working, including why 3.5 days is enough this time: **`aug20-seven-day-read.md`**.
>
> **Match quality is not implicated.** The 08-17 correction stands — Advanced Matching was never
> broken, EMQ is IC 6.4 / Purchase 8.3, and none of that explains 553 landing page views producing
> zero checkouts. Do not reopen it.

<details><summary>Launch banner and task history (kept for the record)</summary>

> # 🟢 LAUNCHED 2026-08-17 — Lee's task list is EMPTY
>
> All three tasks are closed and **v2 is live at $65/day**. Task 1 (EMQ) read: IC 6.4 / Purchase 8.3.
> Task 2 cancelled — misdiagnosis, nothing to fix. Task 3 done — US post archived.

> # ✅ ONE TASK LEFT, AND IT IS A 60-SECOND READ
>
> Re-verified against the live API this session. **Tasks 2 and 3 are off the list:**
>
> - **Task 2 (Shopify match quality) — NOT NEEDED. The fault was misdiagnosed.** Email and phone have
>   been arriving for at least 14 days straight (`email` 332, `phone` 212 in the last 7d; 100% of
>   `Purchase` events carry PII; CAPI is live at 7831 server events). The earlier "only `external_id`
>   arrives" reading came from one hourly bucket of a paginated endpoint. **Do not change any Shopify
>   setting on account of this** — there is nothing to fix. Full detail in
>   `aug26-post-mortem-and-salvage-plan.md`.
> - **Task 3 (US boosted post) — DONE.** The CAMPBELL STREET ad set is now `ARCHIVED` (was `PAUSED`) and
>   its ad is gone from the account. Every one of the 7 live/pausable ad sets is AU-only.
>
> **The only remaining blocker is the EMQ read below** — a number the API genuinely cannot return, which
> is why the launch gate demands a human state it. Everything else the gate checks now passes.

_Everything Claude can do is already done: v2 ad set built, 6 ads published, v1 retired, all PAUSED._

---

## ⭐ TASK 1 — Read the EMQ score — **REINSTATED, and now the only task**

**This is the whole remaining gate.** The v2 ad set passes every machine-checkable launch condition;
`judgeLaunchReadiness()` was run against the real object this session and returns exactly one problem:
EMQ is unacknowledged. Meta does not expose EMQ through the Marketing API, so a human has to read it.

### Where EMQ actually lives

**It is only in the Events Manager UI.** Confirmed this session by probing the Graph API as a node field
(`event_match_quality`, `match_quality`, `data_quality`, `emq`), as an edge, and as a stats aggregation —
every one rejected. There is no API route to it, which is exactly why the gate asks a human.

**Link (Meta's own, taken from the `da_checks` `action_uri`):**
https://business.facebook.com/events_manager2/list/pixel/677437638374055/overview

1. Confirm the top-left says **Craftons Web · 677437638374055** — *not* "Craftons Ads API"
   (`993965426717610`), which is a different dataset and a known red herring.
2. Set the date range, top right, to **Last 28 days**.
3. **Route A — the events table (most reliable).** Scroll down past the "Event activities" chart to the
   table listing `PageView`, `ViewContent`, `AddToCart`, `InitiateCheckout`, `Purchase`. Look for the
   **"Event match quality"** column — a score out of 10, per event.
4. **Route B — if that column isn't shown.** Click the **`InitiateCheckout`** row itself. The detail
   panel opens with the score plus the list of parameters being received.
5. **Route C — the Overview card.** The "Improve your match quality" card has a **`⌄` chevron** at its
   right edge, just past the `···`. It expands in place.

Meta moves this around between UI versions, so if none of the three match what you see, screenshot the
Overview page and send it — the score is on that page somewhere.

### ✅ READ — 2026-08-17, Jul 20 → Aug 16 window, dataset Craftons Web `677437638374055`

| Event | EMQ | Meta band | Total events (28d) |
|---|---|---|---|
| **Initiate checkout** ← the v2 optimisation event | **6.4 / 10** | Good | 255 |
| **Purchase** | **8.3 / 10** | Great | 91 |
| PageView | 6.3 | Good | 60.6K |
| View content | 6.1 | Good | 82.1K |
| Add to cart | 6.1 ⚠️ *update recommended* | Good | 1.2K |
| ConfiguratorStarted | 6.1 ⚠️ *update recommended* | Good | 1K |

**This settles it: match quality was never broken.** A pixel receiving only `external_id` scores 2–3.
Purchase at **8.3** is Meta's "Great" band and is the number that governs whether CAC can be read at
all. The gradient — Purchase 8.3 > InitiateCheckout 6.4 > TOF events 6.1 — is exactly what identity
resolution looks like: the further down the funnel, the more customers have identified themselves.
It matches `had_pii` precisely (Purchase 100% PII, IC 39%).

⚠️ **One honest deviation:** Bible §4.7 Stage 1 sets the bar at **EMQ > 7**. InitiateCheckout is **6.4**,
so the optimisation event is **below the written bar** while Purchase clears it comfortably.
See the launch decision below — this is Lee's call to make knowingly, not something to wave through.

_Note: `Initiate checkout` shows no ad set under "Used by" because the window ends **Aug 16** and the v2
ad set was created **Aug 17**. Not a wiring fault — confirmed separately that v2's `promoted_object`
carries `INITIATED_CHECKOUT`._

### Superseded reasoning, kept as the record

_The note below said to skip this task because match quality was "confirmed broken from four
independent sources". Three of those four were the same metric restated, and the fourth was a misread
of one hourly bucket. The task is back on._

| Source | Reading |
|---|---|
| `match_keys` composition | only `external_id` arrives — no `em`, `ph`, `fn`, `ln` |
| `match_rate_approx` | **`-1`** (Meta's "unavailable" sentinel) |
| `valid_entries` / `matched_entries` | **`0` / `0`** |
| `/da_checks` | **`[failed] Pixel has low event source match rate`** |
| Events Manager UI | *"$118 ad spend affected by low data quality"* · match quality **HIGH PRIORITY** |

**Go straight to Task 2.** Verification afterwards is machine-checkable — Claude re-runs `match_keys`
and `matched_entries` and confirms whether real identifiers start arriving. That is a better proof than
a UI number read once.

_If you do want the score anyway: on the Events Manager Overview, click the **⌄ chevron** at the right
of the "Improve your match quality" card (just past the `···`). It expands in place — no scrolling._

### Old instructions, kept for reference

1. Open **https://business.facebook.com/events_manager2/list/dataset/677437638374055/overview**
2. Confirm top-left says **Craftons Web · ID 677437638374055** (not *Craftons Ads API*).
3. Set the date range (top right) to **Last 28 days**.
4. **Scroll down past the "Event activities" chart** to the events table listing `PageView`,
   `ViewContent`, `AddToCart`, `InitiateCheckout`, `Purchase`.
5. Find the **"Event match quality"** column. It shows a score out of 10 per event.
   - If the column isn't visible, click the **`Purchase`** row — the detail panel shows the score plus
     which parameters are being received.
6. **Write down two numbers: EMQ for `Purchase` and EMQ for `InitiateCheckout`.**

**→ Send Claude both numbers.** Expect them to be low (roughly 3–5) since only `external_id` is
arriving. Target is **above 7**.

---

## ~~TASK 2 — Fix match quality~~ → ❌ CANCELLED. The diagnosis was wrong; nothing here needs doing.

> **Do not action any of the steps below.** Advanced Matching is working: `email` and `phone` arrive
> daily, 100% of `Purchase` events carry PII, and CAPI is live. Changing the Shopify data-sharing level
> now would be a change made on a false premise. Retained only as the record of the misdiagnosis.

**Original text follows — superseded.** Meta says **"$118 of ad spend affected by low data quality"** and lists *"Improve your match
quality by sending more parameters"* as **HIGH PRIORITY**. We have 11 matching fields configured and
**only `external_id` actually arriving** — no email, no phone, no name. This is free to fix and worth
more than any creative change.

### 2a. Let Meta guide it
1. Same Events Manager page → the **"Improve your match quality by sending more parameters"** card.
2. Click **Get Started** and follow it. Meta names the exact missing parameters for your setup.
3. Also click **"View all actions (7)"** and screenshot the list for Claude — there may be other
   quick wins in there.

### 2b. Turn on customer data sharing in Shopify
This is almost certainly where the missing parameters are blocked.

1. Shopify admin → **Settings → Apps and sales channels** → **Facebook & Instagram** → **Open app**.
2. Go to **Settings** (or *Data sharing settings*) inside the app.
3. **Customer data sharing: ON.**
4. **Data sharing level: set to `Maximum`.**
   - `Standard` sends browser events only — this is the level that produces exactly our symptom.
   - `Maximum` enables Advanced Matching, sending hashed email/phone with each event.
5. Confirm the connected pixel/dataset is **`677437638374055` (Craftons Web)**.
6. Save.

### 2c. Check consent isn't suppressing it
1. Shopify admin → **Settings → Customer privacy**.
2. If a cookie banner / consent requirement is enabled for **Australia**, data sharing is limited to
   visitors who actively consent. Australia has no GDPR-style consent mandate — if this is on for AU
   without a reason, that alone can starve the parameters.

### 2d. Verify it worked
1. Place a **test order** on the site (or wait for the next real one).
2. **Tell Claude when done.** Claude re-runs the `match_keys` check and confirms whether `em`/`ph` are
   now arriving. **This is machine-checkable — no guessing.**
3. Re-read EMQ in 24–48h (Meta recalculates it on a lag) and compare to your Task 1 baseline.

---

## ~~TASK 3 — Delete the US-targeted boosted post~~ → ✅ DONE (verified 2026-08-17)

> Re-audited this session: the CAMPBELL STREET ad set is now **`ARCHIVED`**, and no ad matching it
> remains in the account. All 7 live-or-pausable ad sets are AU-only. Archived is not the same as
> deleted, but it is two states from live rather than one, which closes the original concern.
> Nothing further needed.

**Original text follows — superseded.** The last thing on the account breaching the Australia-only rule.
It is paused and not spending, but a
paused ad set is one un-pause from live. The Marketing API refuses to touch it — Meta replies *"can only
be deleted on your Page"*.

1. Open **https://business.facebook.com/latest/home?asset_id=611852278682648**
2. Find the post **"CAMPBELL STREET | Ground floor…"** (an Instagram post that was boosted).
3. Open its **promotion / ad** and **delete the promotion** (deleting the ad, not necessarily the post).
4. Tell Claude — a re-audit will confirm the account is 100% AU.

For reference it spent **$43.82 for 0 results**, targeting the **United States**.

---

## What happens after Task 1

1. You send Claude the two EMQ numbers.
2. Claude proposes activation of **v2** (`120247812165960186`) with `emq_acknowledged=true`.
3. You approve. Claude applies. Ads go live on the **standard `InitiateCheckout`** event at **$65/day**.
4. Hands off 7 days. First readable signal ~72h; readable CAC ~3–4 weeks.

### The launch decision, with the real numbers in hand

**Recommendation: launch.** Reasoning, including the part that argues against:

**For:**
1. **Purchase EMQ 8.3 clears the >7 bar.** Purchase attribution is what determines whether CAC is
   readable — and CAC is the metric the whole budget ladder and kill rule run on. The monitoring plan's
   hard rule is *never kill while results can't be counted*; at 8.3, they can be counted.
2. **What actually killed Aug26 is fixed and verified** — a custom conversion that had never fired.
   v2 runs on standard `InitiateCheckout`, which fired **255 times** in the window and 44 times on
   Aug 17 alone.
3. **Signal volume is adequate.** 255 IC / 28d ≈ 9/day ≈ 63/week, around Meta's ~50/week guidance for
   stable ad-set optimisation.
4. **Waiting buys nothing specific.** There is no pending fix behind the 6.4. The Shopify theory is
   dead. IC sits below Purchase for a structural reason — shoppers start checkout before they identify
   themselves — and that does not resolve with time.

**Against, stated plainly:**
- **6.4 is below the Bible's >7 gate for the optimisation event.** That is a real deviation from a
  written standard, and this repo's whole failure history is standards waved through. The honest framing
  is *knowingly accepting a moderate attribution drag*, *not* *"the gate is satisfied"*.
- Expect reported CAC to read somewhat **worse than true CAC**. Judge the ladder against that.

**The lever if Lee prefers to raise it first:** the ⚠️ *update recommended* flags on `Add to cart` and
`ConfiguratorStarted` are Meta offering more parameters on those events. Neither is the optimisation
event, so this would not directly move the 6.4 — it is a genuine but slow, indirect improvement, and
holding $65/day of learning to chase it is a poor trade.

</details>

## 🟢 LAUNCHED — all 7 applied and verified live (2026-08-17)

**v2 is ACTIVE and spending.** Lee approved after reading EMQ; all 7 changes applied with `CONFIRM=1`,
each passing the live activation preflight. **State read back from the Graph API afterwards, not taken
from the success responses:**

| Object | Verified state |
|---|---|
| v2 ad set `120247812165960186` | **`ACTIVE` / effective `ACTIVE`** · **$65.00/day** |
| optimisation | `OFFSITE_CONVERSIONS` → `INITIATED_CHECKOUT` on pixel `677437638374055` ✅ |
| geo | `["AU"]` ✅ |
| 6 ads | **all `ACTIVE` / effective `ACTIVE`**, all the **`aug26 v2`** set (not v1) ✅ |
| Campaign `120247706808370186` | `ACTIVE` |
| v1 ad set `120247706822330186` | **`PAUSED`** — stayed retired ✅ |

Blended daily spend is now ~**$80/day** (v2 $65 + retargeting $15).

### ⏰ 72h+ reading is SCHEDULED — Fri 2026-08-21, 08:00 Melbourne (Aug 20 22:00 UTC)

Auto-fires into the Claude session (`trigger_id trig_0147qKAxFDujEStfERNNNYqE`), ~83h after launch —
past the 72h gate and in the morning rather than 9pm Thursday. It carries its own setup instructions
(branch, repo re-clone, env aliases), the kill rule, the ladder, and LAW 1. **Nobody has to remember.**

### What to watch, and when

- **Do not judge before ~72h** (≈ Aug 20). Kill rule needs **≥72h AND ≥$25 AND zero results** — and
  never kill while results cannot be counted.
- **Readable CAC: 3–4 weeks.** Reported CAC will read somewhat **worse than true CAC** because
  InitiateCheckout EMQ is 6.4. Judge the ladder against that, not against the raw number.
- **Ladder:** $65 → $78 → $94 → $100, one step per week, **only** at CAC ≤ $322.
- **Always read `inline_link_clicks`**, never the headline CTR — it runs ~3.5× inflated on these ads
  (12% headline vs 3.6% link).

### Original staging record

Proposed and approved through the codebase's own path so an audit trail exists, rather than calling the
Graph API directly. Each `apply` re-ran the live preflight (AU targeting, $100/day cap, monthly ceiling,
`judgeLaunchReadiness`) and fails closed.

| # | Change | Target | Approval ID |
|---|---|---|---|
| 1 | `activate_ad_set` | `120247812165960186` (v2, $65/day) | `950c66ab-c4cb-4983-a6b2-b2f6281a83a2` |
| 2 | `activate_ad` | AD5 Chippies `120247812181800186` | `a25420d8-d6f0-4d47-8485-a39e6ac263df` |
| 3 | `activate_ad` | AD4 Builders `120247812183590186` | `96381950-e769-4808-af3f-f5c4d4db7459` |
| 4 | `activate_ad` | AD6 Carpenters `120247812185720186` | `f5b09946-1c54-4fea-a5be-aaeaf439ac02` |
| 5 | `activate_ad` | AD1 Concreters `120247812187850186` | `1309bee9-35dd-4be5-bcb6-75b8f07ae9ad` |
| 6 | `activate_ad` | AD2 Landscapers `120247812190310186` | `fd11c166-30a0-430b-be7c-2b161a11e225` |
| 7 | `activate_ad` | AD2b Landscapers finished-first `120247812192110186` | `20cb2d98-07f7-40e8-a907-384b3588c85e` |

All carry `emq_acknowledged: true`. Approver recorded as **Lee Patterson**, with the EMQ numbers and the
knowingly-accepted 6.4 in the approval note. Dry-run confirms the ad-set call is
`POST 120247812165960186 {"status":"ACTIVE"}`.

**To execute:** `CONFIRM=1 node tools/meta-ads.mjs apply --approval_id=<id>` for each, ad set first.

## Verified live this session (2026-08-17) — nothing quoted from memory

| Check | Result |
|---|---|
| `doctor` | **54/54 pass, 0 fail** |
| v2 `promoted_object` | `pixel_id 677437638374055` + `custom_event_type INITIATED_CHECKOUT` ✅ |
| v2 status / budget / geo | `PAUSED` · `6500` cents = $65/day · `countries: ["AU"]` ✅ |
| v1 `promoted_object` | still the dead `custom_conversion_id 27686282527680441`, `PAUSED` ✅ |
| Campaign `120247706808370186` | `ACTIVE` (container only) |
| `InitiateCheckout` firing | **yes, daily** — 6–44/day; 44 on Aug 17. The v2 target has real signal. |
| Pixel `last_fired_time` | `2026-08-16T23:45:24+0000` — live |
| `judgeLaunchReadiness(v2)` | one problem: EMQ unacknowledged. With `emq_acknowledged=true` → **`ok: true`** |
| `judgeLaunchReadiness(v1)` | still correctly **refused** (conversion never fired) |
| Geo audit | 7 live/pausable ad sets, **0 non-AU**; the US one is `ARCHIVED` |
| Link CTR (Lawless ads, 14d) | **3.65% / 3.60% / 3.43%** — headline CTR reads ~12%, engagement-inflated |

---

## Current state — updated 2026-08-20 from the live account

| Object | ID | Status |
|---|---|---|
| Campaign `RadiusPro \| TOF \| Aug26` | `120247706808370186` | ACTIVE (container only) |
| **v2 ad set** — standard `InitiateCheckout`, $65/day | `120247812165960186` | **ACTIVE since 2026-08-17**, 6 ads ACTIVE — Lee approved activation 08-17 10:43 UTC. **Pause proposed**, see below |
| v1 ad set — dead custom conversion | `120247706822330186` | **PAUSED** (retired) |
| Retargeting — BOF | `120233074187690186` | **ACTIVE**, $15/day and budget-capped every day. 62 lifetime purchases at $52 each. **Raise to $18 proposed** |
| US boosted post — CAMPBELL STREET | (Page-owned) | **ARCHIVED** ✅ resolved |

## Object ID reference (everything a future session needs)

| Thing | ID |
|---|---|
| Ad account | `act_1650412872259063` (AUD, Australia/Melbourne) |
| Pixel / dataset **Craftons Web** | `677437638374055` |
| Second dataset **Craftons Ads API** — *not* linked to the ad account, red herring | `993965426717610` |
| Custom conversion *Sales Intent* — **DEAD, never fired, do not reuse** | `27686282527680441` |
| Facebook Page | `611852278682648` |

**v2 ads (PAUSED, in ad set `120247812165960186`) → creative:**

| Ad | Ad ID | Creative ID |
|---|---|---|
| AD5 Chippies (Lawless photo — the 10.45% CTR winner) | `120247812181800186` | `1078072304563046` |
| AD4 Builders (Lawless photo) | `120247812183590186` | `801056473070934` |
| AD6 Carpenters (Lawless photo) | `120247812185720186` | `3695505940601153` |
| AD1 Concreters (Ardreagh carousel) | `120247812187850186` | `954057387710539` |
| AD2 Landscapers (Ardreagh carousel) | `120247812190310186` | `1036744315626177` |
| AD2b Landscapers finished-first (carousel) | `120247812192110186` | `1379645754375539` |

All six creatives are the **aug26 v2** set: "laminate" corrected to "double them up" on the three Lawless
ads, UTMs on `radiuspro_tof_aug26`. The v1 ad set holds a parallel set of 6 ads — **do not confuse them**;
v1 is retired.

Winning site photo (the only real one): `content-engine/sandbox/real/site-lawless-curved-stud-wall.jpg`
in `leepatt/cnccut-app`, recovered from Meta image hash `923c0b632935f8af124c792e1b56d3f9`.
