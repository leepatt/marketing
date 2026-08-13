# Ad set wiring — the exact settings for the launch TOF ad set

_Verified live against the account 2026-08-04. Everything here is read from the API, not from notes._

---

## ✅ RESOLVED 2026-08-05 — the agent CAN now do this step

Lee's call: build the executor. Done, and validated against Meta rather than assumed.

- **`create_campaign`** — objective locked to `OUTCOME_SALES`, created PAUSED.
- **`create_ad_set`** — AU-only via `DEFAULT_TARGETING`, `promoted_object` → the Sales Intent custom
  conversion, created PAUSED, $100/day hard cap.
- Both are in `ALWAYS_REQUIRES_APPROVAL` at **every** rung. `doctor` is now **44/44**.
- **Proposal already filed** for the campaign: approval `9cf62557-0f55-495c-a17e-d6ed115df9fc`,
  status **pending**. Nothing has touched the account.

**Verified the gate actually holds:** `apply` with `CONFIRM=1` against that *pending* row is refused —
*"CONFIRM=1 is set but approval … is pending … Refusing to proceed."* Both an approved row **and**
`CONFIRM=1` are required.

### 🔴 Three payload bugs found by asking Meta to validate, not by reading the code

Meta supports `execution_options: ["validate_only"]` — it type-checks a create without creating
anything. **All three of these would have failed at apply time on the real launch:**

| # | Symptom | Fix |
|---|---|---|
| 1 | *"Bid amount or bid constraints required for bid strategy"* | Set `bid_strategy: "LOWEST_COST_WITHOUT_CAP"` explicitly instead of inheriting the campaign's |
| 2 | *"The promoted object … has an invalid combination of parameters"* | **`promoted_object` must be `{custom_conversion_id}` ALONE.** Adding `pixel_id` is rejected — the custom conversion already carries its pixel |
| 3 | *"Must specify True or False in is_adset_budget_sharing_enabled"* | Set it `false` on the campaign — budget belongs on the ad set where the ceiling and daily cap can see it |

Confirmed nothing was created: 7 ad sets and 11 campaigns before and after, zero `ZZTEST` strays.
**Use `validate_only` for every new Marketing API write before trusting it.**

### 🔴 A root cause nobody had recorded: July's campaign objective was TRAFFIC

Read live from the account: **`RadiusPro | TOF | Ardreagh | Jul26` has `objective: OUTCOME_TRAFFIC`**,
and the `ADD_TO_CART` ad set sat inside it.

A traffic-objective campaign asks Meta to buy clicks — and it delivered exactly that: **19,773 clicks
at 10.03% CTR for 2 results on $1,279.94.** The ad set's own `optimization_goal` was
`OFFSITE_CONVERSIONS`, and that does **not** rescue a campaign whose objective is traffic.

This sits *alongside* the wrong-event diagnosis, it does not replace it. Both were true. `OUTCOME_SALES`
is now a locked constant and passing `OUTCOME_TRAFFIC` throws.

---

## (historical) The blocker as it stood on 2026-08-04

`campaigns/meta/launch-readiness.md` lists B3 as *"wire the ad set to the custom conversion"* and the
session plan treats it as a quick job. **It is not, because the code has no way to express it.**

Verified in `leepatt/cnccut-app` @ `main` (5cd7910):

| Thing | State |
|---|---|
| `promoted_object` anywhere in `tools/` | **absent** — zero occurrences |
| `create_ad_set` executor in `apply` | **absent** — `apply` implements only `pause_ad`, `set_budget`, `publish_ad` |
| `create_ad_set` in `ALWAYS_REQUIRES_APPROVAL` | present (the guardrail exists) |

So the guardrail for creating an ad set exists, but **the thing it guards does not.** The agent can
report, evaluate, check batches, upload images, create creatives and pause/publish ads. It cannot
create the ad set the launch needs, and it cannot point anything at the custom conversion.

**Two ways forward. This is Lee's call:**

1. **Create the ad set by hand in Ads Manager** using the settings below. ~3 minutes, no code, no risk.
   Then the agent publishes ads into it (`publish_ad` already exists and is guardrailed).
2. **Build the `create_ad_set` executor.** Correct long-term and matches the standing "invest in
   integrations" rule, but it is a new *spend-capable* outward-write path. Not something to add
   unattended — it wants explicit sign-off and its own review.

**Recommendation: option 1 now, option 2 later.** The ad set is created once. Hand-building it does not
block anything, and it keeps a spend-capable write path out of the codebase until it is genuinely needed.

---

## ✅ The custom conversion is live and correct

```
id                27686282527680441
name              Sales Intent — Checkout or Purchase
custom_event_type OTHER
rule              {"or":[{"event_name":{"eq":"InitiateCheckout"}},{"event_name":{"eq":"Purchase"}}]}
is_archived       false
```

The two `ZZTEST` objects are archived, as documented. Nothing half-built.

## ⬜ Confirmed: nothing points at it

Every ad set on the account uses `custom_event_type` against the raw pixel. **Not one references
`custom_conversion_id`.** Creating the conversion changed nothing about delivery, exactly as
`STATUS.md` warned.

| Ad set | Status | promoted_object |
|---|---|---|
| Retargeting — BOF – Purchase `120233074187690186` | **ACTIVE** $15/day | `custom_event_type: PURCHASE` |
| TOF \| Broad AU \| AddToCart `120247183658270186` | campaign paused | `custom_event_type: ADD_TO_CART` |
| Retargeting — BOF - Add To Cart | paused | `custom_event_type: ADD_TO_CART` |
| Advantage+ \| MOF | campaign paused | `null` |
| Brand Awareness \| TOF | campaign paused | `page_id` only |

---

## The settings for the new ad set

```
Campaign objective     Sales (OUTCOME_SALES)
Ad set name            RadiusPro | TOF | Broad AU | SalesIntent | Aug26
Daily budget           $50-100/day   (code ceiling: $2000/mo, validation stage default $35/day)
Optimisation goal      OFFSITE_CONVERSIONS
Billing event          IMPRESSIONS
promoted_object        { "pixel_id": "677437638374055",
                         "custom_conversion_id": "27686282527680441" }
Targeting              geo_locations: { countries: ["AU"] }
                       interests: NONE          <- do not add any
                       age_min 18, age_max 65
Placements             Advantage+ (automatic)
Attribution            7-day click, 1-day view
```

⚠️ **`custom_conversion_id`, not `custom_event_type`.** Setting `custom_event_type: OTHER` against the
pixel is not the same thing and will not optimise toward the pooled event.

### Why broad with no interests

The July ad set `TOF | Broad AU | AddToCart` reads back from the API as `geo=["AU"]`, **`interests: 0`**,
age 25–65. That independently re-confirms the retraction in `STATUS.md`: **July never segmented the
audience.** Broad-with-no-interests is the one setting July got right. Keep it.

Only difference worth making: **age 18–65 rather than 25–65.** Nothing in the order data justifies
excluding 18–24, and Andromeda does better with fewer hand-drawn constraints.

---

## 🟠 Two things found while verifying — worth a look

### 1. An ad set targeting the United States

`Instagram post: CAMPBELL STREET | Ground floor...` has `geo_locations: { countries: ["US"] }` and
`custom_event_type: PURCHASE`. Craftons manufactures in Fairfield and ships Australia-wide via FedEx.

It spent **$43.82 for 0 results** and shows in `report` under "ads with spend and no results". Its
campaign is paused, so it is not burning money right now. **It should not be un-paused as-is.** Likely a
boosted Instagram post that took a default audience.

### 2. Still no Instagram account on the ad account

`instagram_accounts` is empty, as recorded. Facebook-only placements unless connected — which halves the
inventory for a test that is already low-volume. Worth connecting before launch.

---

## EMQ — not readable the way the plan assumed

Step 7 of the session plan was *"check EMQ > 7 — readable from 2026-08-04."* **EMQ is not exposed on
this endpoint.** `GET /{pixel_id}/stats` rejects `event_match_quality`; the permitted aggregations are:

```
browser_type, custom_data_field, device_os, device_type, event, host, match_keys, had_pii,
pixel_fire, event_detection_method, url, event_value_count, url_by_rule, event_total_counts,
event_source, event_processing_results
```

**EMQ has to be read by eye in Events Manager → Data Sources → Craftons Web → Event Match Quality.**
That is a Lee job, or a browser-driven one.

### The proxy signal, and why it is only a proxy

`match_keys` shows which identifiers actually arrive. Over 2026-07-28 → 08-04 the only keys present are
**`external_id`** and cookies (`c_user_cookie`, `fr_cookie`, `true_fr_cookie`). **No `em`, no `ph`, no
`fn`/`ln`** — despite `automatic_matching_fields` listing all eleven and
`enable_automatic_matching: true`.

⚠️ **Do not conclude EMQ is bad from this.** The `match_keys` counts are tiny (114 PageView) against
59,935 PageViews in the same period, so the aggregation is clearly sampled or partial. The composition
is a hint worth checking in the UI, not a measurement.

### Event volume — the raw pixel number flatters us, ignore it

| Window | InitiateCheckout | Purchase | Combined |
|---|---:|---:|---:|
| 30 days (07-05 → 08-04) | 163 | 88 | 251 → **~58/week** |

**58/week looks like it clears Meta's ~50/week threshold. It does not.** These are pre-dedup pixel
counts. Ground truth is ~38 real Shopify orders/30d against 88 pixel Purchases — a 2.3× inflation.
Deflating both events by that gives **~25 sales-intent events/week**, which matches the 26.3/week
already in `STATUS.md`.

**So the existing figure was right and stands.** The test will run Learning Limited. Judge it on true
CAC against the $322 break-even, per `launch-readiness.md`.
