# Lee's tasks — step by step (updated 2026-08-17, second pass)

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

**Where:** https://business.facebook.com/events_manager2/list/dataset/677437638374055/overview
→ confirm top-left says **Craftons Web · 677437638374055** → date range **Last 28 days** → scroll past
the "Event activities" chart to the events table → **"Event match quality"** column.

**Send Claude two numbers: EMQ for `InitiateCheckout` and EMQ for `Purchase`.**

Given what is actually arriving, expect **mid-to-high single digits**, not the 3–5 the old note
predicted. `Purchase` should read highest — every Purchase event carries PII.

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

**If EMQ comes back at 6 or above:** launch. Nothing else is outstanding.

**If EMQ comes back below 6:** it is still Lee's call, but the recommendation has changed. There is no
longer a pending fix to wait for — the Shopify theory is dead, and partial PII coverage on top-of-funnel
events is largely structural (guests browsing before they identify themselves). Waiting would mean
waiting for nothing in particular. Weigh a below-6 score as a known, priced-in drag on attribution
rather than as a blocker with a fix behind it.

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

## Current state — nothing is spending on the test

| Object | ID | Status |
|---|---|---|
| Campaign `RadiusPro \| TOF \| Aug26` | `120247706808370186` | ACTIVE (container only) |
| **v2 ad set** — standard `InitiateCheckout`, $65/day | `120247812165960186` | **PAUSED**, 6 ads PAUSED |
| v1 ad set — dead custom conversion | `120247706822330186` | **PAUSED** (retired) |
| Retargeting — BOF | `120233074187690186` | **ACTIVE** ($15/day) — leave it, it produces the account's results |
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
