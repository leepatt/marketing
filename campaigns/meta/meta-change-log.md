# Meta Ads — change log

_Account: `act_1650412872259063` (Craftons, AUD) · Pixel: `677437638374055`_

Every change made to the live Meta ad account gets recorded here, with the API response that
confirmed it.

**Correction (2026-08-02):** an earlier version of this note said the Jul 22 build "was never written
down." That was wrong. It **was** documented — in Drive at
`02 Strategy/META-ADS-BRIEF.md`, dated 2026-07-21, the day before launch. What was missing was a
**pointer from the repo to it**, so a repo-side session found the campaign only by querying the API.
The two homes are now cross-linked. Log account changes here *and* keep Drive in step.

---

## 2026-08-02 — Emergency stop after audit

Context: `meta-ads-audit-2026-08-02.md`. Sales fell after the Jul 22 launch (orders/day −42%,
conversion rate 1.49% → 0.066%) and the TOF campaign was poisoning the retargeting audience.

Authorised by Lee in-session. Both changes verified against the API after execution.

| # | Change | Object | Before | After |
|---|---|---|---|---|
| 1 | Paused campaign | `RadiusPro \| TOF \| Ardreagh \| Jul26` (`120247183657950186`) | ACTIVE, $70.00/day | **PAUSED** |
| 2 | Cut daily budget | ad set `Retargeting — BOF - Add To Cart` (`120232888615720186`) | $60.00/day | **$15.00/day** |

**Daily exposure: ~$130/day → $15.00/day.**

Verified account-wide after the changes — exactly one ad set still delivering:

```
Retargeting Campaign - Bottom Of Funnel | ...- Add To Cart   $15.00/day
TOTAL DAILY EXPOSURE: $15.00/day
```

TOF ad set `TOF | Broad AU | AddToCart` reads `effective_status: CAMPAIGN_PAUSED` — nothing beneath
the paused campaign is delivering. Final TOF spend on its last day (Aug 2): $85.97, 1,281 clicks,
15 add-to-carts, **0 purchases**. Campaign lifetime: $1,277 → 0 purchases.

---

## 2026-08-02 (later) — Creative fix + switch to Purchase optimisation

Authorised by Lee. Triggered by a finding that **invalidated audit recommendation §5.2**: that
recommendation was made from ad-set settings without checking the creative inside them.

### The finding that changed the plan

Ad-level performance, retargeting campaign, Jul 8 – Aug 2:

| Ad | Spend | Purchases | Revenue | ROAS | Was |
|---|---|---|---|---|---|
| Ad 2 | $351.55 | **8** | $13,091 | 37.2 | ACTIVE (in ATC ad set) |
| Configurator Hero Ad D | $11.62 | 2 | $2,972 | 255.8 | **PAUSED** |
| Radius Pro boss video | $234.68 | 1 | $371 | 1.6 | ACTIVE |
| Ad 1 (only ad in Purchase ad set) | $125.03 lifetime | **0** | $0 | 0 | idle since Oct 2025 |

Executing §5.2 as written would have switched **off** Ad 2 (8 of the campaign's 10 purchases) and
switched **on** a stale ad that has never converted, pointing at `/collections/all`. §5.2 is wrong
and is corrected in the audit doc.

### Changes made

| # | Change | Object | Result |
|---|---|---|---|
| 1 | Paused weak ad | `Radius Pro boss video` (`120247285566810186`) | 1.6x ROAS, $234 for 1 purchase — off |
| 2 | Un-paused strong ad | `Configurator Hero Ad D` (`120245221715860186`) | had only ever had $11.62 of spend |
| 3 | Attempted in-place event switch on ATC ad set | `120232888615720186` | ❌ **Meta rejected** |
| 4 | Copied `Configurator Hero Ad D` → Purchase ad set | new ad `120247401861850186` | ✅ |
| 5 | Copied `Ad 2` → Purchase ad set | ❌ failed, then ✅ via workaround | see below |
| 6 | Paused stale `Ad 1` in Purchase ad set | `120233074187680186` | ✅ |
| 7 | Purchase ad set budget $12.50 → **$15.00/day** | `120233074187690186` | ✅ |
| 8 | Paused Add-To-Cart ad set | `120232888615720186` | ✅ |
| 9 | Activated Purchase ad set | `120233074187690186` | ✅ |

**Daily exposure unchanged at $15.00/day.** Verified account-wide: one ad set delivering,
`optimising for: PURCHASE`.

### Two API obstacles worth remembering

1. **You cannot change the conversion event on a published ad set.** Meta error 3260011:
   _"You can't edit your pixel, conversion event, custom conversion or optimisation for an ad set
   after the ad set has been published. To run an ad set with your desired changes, create a new ad
   set."_ Switching optimisation event **always** means moving to a different ad set.
2. **`/copies` failed on Ad 2** — error 3858504, _"Creative should not include standard enhancements
   … deprecated."_ Workaround that worked: create a **new ad referencing the existing
   `creative_id`** (`661763516798254`) via `POST /act_<id>/ads` with
   `creative={"creative_id":"…"}`, instead of copying the ad object.

### ⚠️ Caveats on reading the results

- **Both live ads are new objects → learning phase restarts from zero.** Expect unstable delivery
  and possibly little/no spend for several days. Do not judge this in week one.
- **At ~0.5 purchases/day the ad set will likely never exit learning** (needs ~50 events/week).
  Purchase optimisation here is a considered bet, not a safe default.
- **The Purchase ad set uses a more generous attribution window** than the one it replaced:
  `CLICK_THROUGH 7d + VIEW_THROUGH 1d + ENGAGED_VIDEO_VIEW 1d`, vs `CLICK_THROUGH 7d` only.
  **Reported conversions will look better even if real sales are identical.** Do not compare the
  new numbers to the July baseline without accounting for this. Cross-check Shopify.
- Targeting parity confirmed — same six custom audiences, age 18–65, AU.
- `Configurator Hero Ad D`'s 255x ROAS is off **$11.62 of spend**. That is a reason to give it
  budget, not a proven number.

### Reversal

`POST /120232888615720186 status=ACTIVE` · `POST /120233074187690186 status=PAUSED`
(then re-pause the two new ads `120247401861850186`, `120247401862380186` if unwinding fully)

### Deliberately NOT changed

- **`Retargeting — BOF – Purchase` ad set (`120233074187690186`) is still PAUSED** ($12.50/day).
  The live ad set optimises for Add-To-Cart, not Purchase. Recommended in the audit (§5.2), not yet
  authorised. **Open decision.**
- Nothing else in the account was touched. All other campaigns were already paused before today.

### Reversal

Both changes undo in seconds if wanted:
`POST /120247183657950186 status=ACTIVE` · `POST /120232888615720186 daily_budget=6000`

---

## Watch list (next review)

1. **Does retargeting recover at $15/day?** It produced 9 purchases / $12,797 on ~$15/day in
   Jul 8–21, then 1 purchase on a scaled-up budget once the pool was flooded. If it does **not**
   recover within ~2 weeks, the audience pool is the cause, not the budget — the 30-day visitor
   pool needs until roughly **2026-09-01** to clear the Jul 22 – Aug 2 junk cohort, and the
   180-day pools until **2027-01-29**.
2. **Cross-check Shopify before making any performance claim.** Meta claimed 2 purchases / $3,637
   from retargeting over Jul 22 – Aug 2; Shopify attributed 2 orders / $398 to all of
   Facebook + Instagram across 30 days. Never report on Meta's numbers alone.
3. **Before any relaunch:** confirm ViewContent *and* AddToCart are firing into the campaign in
   Events Manager on day one, before spend starts. The Jul 22–29 blind spend is exactly what that
   check prevents.
