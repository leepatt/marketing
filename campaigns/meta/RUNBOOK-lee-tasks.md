# Lee's tasks — step by step (2026-08-17)

_Three tasks. ~15 minutes total. Task 1 and 2 unblock the v2 relaunch; Task 3 is tidy-up._
_Everything Claude can do is already done: v2 ad set built, 6 ads published, v1 retired, all PAUSED._

---

## ~~TASK 1 — Read the EMQ baseline~~ → SKIP IT (updated 2026-08-17)

**Advice changed after reading more of the API.** Don't spend time hunting the score. Match quality is
already confirmed broken from **four independent sources**, and the exact number would not change what
we do next:

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

## TASK 2 — Fix match quality (10 minutes) ⭐ the important one

**Why:** Meta says **"$118 of ad spend affected by low data quality"** and lists *"Improve your match
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

## TASK 3 — Delete the US-targeted boosted post (2 minutes, tidy-up)

The last thing on the account breaching the Australia-only rule. It is paused and not spending, but a
paused ad set is one un-pause from live. The Marketing API refuses to touch it — Meta replies *"can only
be deleted on your Page"*.

1. Open **https://business.facebook.com/latest/home?asset_id=611852278682648**
2. Find the post **"CAMPBELL STREET | Ground floor…"** (an Instagram post that was boosted).
3. Open its **promotion / ad** and **delete the promotion** (deleting the ad, not necessarily the post).
4. Tell Claude — a re-audit will confirm the account is 100% AU.

For reference it spent **$43.82 for 0 results**, targeting the **United States**.

---

## What happens after Tasks 1 and 2

1. You send Claude the EMQ numbers.
2. Claude proposes activation of **v2** (`120247812165960186`) with `emq_acknowledged=true`.
3. You approve. Claude applies. Ads go live on the **standard `InitiateCheckout`** event at **$65/day**.
4. Hands off 7 days. First readable signal ~72h; readable CAC ~3–4 weeks.

**If EMQ comes back below 7:** the right call is to finish Task 2 and let EMQ recover *before* spending,
rather than launch into the penalty Meta has already costed at $118. That is Lee's call, but it is the
recommendation.

---

## Current state — nothing is spending on the test

| Object | ID | Status |
|---|---|---|
| Campaign `RadiusPro \| TOF \| Aug26` | `120247706808370186` | ACTIVE (container only) |
| **v2 ad set** — standard `InitiateCheckout`, $65/day | `120247812165960186` | **PAUSED**, 6 ads PAUSED |
| v1 ad set — dead custom conversion | `120247706822330186` | **PAUSED** (retired) |
| Retargeting — BOF | `120233074187690186` | **ACTIVE** — leave it, it produces the account's results |

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
