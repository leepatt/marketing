# How to create the launch ad set — step by step

_For Lee. Written 2026-08-05. Do this in Ads Manager by hand; the agent cannot do it (see §Why)._

**Time: about 5 minutes.** Nothing here makes an ad go live. You are building an empty container.

---

## Before you start

- Ad account: **`act_1650412872259063`** (Craftons)
- Leave **`Retargeting Campaign - Bottom Of Funnel`** running. It is making money — 18 of the
  account's last 20 results came from it on $660.90. Do not switch it off to tidy the test.
- You are creating a **new** campaign, not editing an existing one.

---

## Step 1 — New campaign

1. Ads Manager → **Campaigns** tab → green **+ Create**
2. Buying type: **Auction**
3. Objective: **Sales**
4. Click **Continue**

## Step 2 — Campaign settings

1. Campaign name: **`RadiusPro | TOF | Aug26`**
2. **Special ad categories: leave EMPTY.** Not credit, employment, housing, social issues.
3. **Advantage campaign budget: OFF.** Budget goes on the ad set so the $2k/mo ceiling in code stays
   meaningful.
4. A/B test: **off**
5. Click **Next**

## Step 3 — Ad set: the conversion (⚠️ the step that matters most)

1. Ad set name: **`RadiusPro | TOF | Broad AU | SalesIntent | Aug26`**
2. Conversion location: **Website**
3. Performance goal: **Maximise number of conversions**
4. **Pixel / Dataset: `Craftons Web`** (`677437638374055`)
5. **Conversion event: `Sales Intent — Checkout or Purchase`**

> 🔴 **This is the whole point of the exercise.** The dropdown lists standard events
> (Purchase, Add to Cart, Initiate Checkout) *and* custom conversions. You want the **custom
> conversion** named **`Sales Intent — Checkout or Purchase`** (ID `27686282527680441`).
>
> **Do NOT pick "Purchase".** Purchase alone runs at ~9 events/week. The custom conversion pools
> InitiateCheckout OR Purchase and roughly triples that. Pooling events is the fix for what actually
> broke in July.
>
> **Do NOT pick "Add to Cart"** either. It has the volume but IC→Purchase converts at 51% while
> ATC→Purchase converts at 11% — in the configurator, adding to cart is just how you see a price.
> Optimising on it buys attention, not sales.

## Step 4 — Budget and schedule

1. Daily budget: **$50** (start here; the code ceiling is $2,000/month)
2. Start date: today. **No end date.**
3. Leave the bid strategy on the default (**Highest volume**). No bid cap.

## Step 5 — Audience 🇦🇺

1. **Location: Australia.** Country level — not Melbourne, not a radius.
2. Under the location box set the dropdown to **"People living in this location"**
3. Age: **18 – 65+**
4. Gender: **All**
5. **Detailed targeting: LEAVE COMPLETELY EMPTY.** No interests, no behaviours, no job titles.
6. **Detailed targeting expansion / Advantage+ audience: OFF** if the toggle is offered.
7. Languages: leave empty.

> **Why broad and empty.** July's ad set reads back from the API as `geo=["AU"]`, `interests: 0` —
> broad with no interests was the one thing July got right, and the "trade segmentation failed" story
> was wrong. Segmenting from scratch splits signal across creative that has never won. Identity words
> are for multiplying a proven winner, and LF4/LF5 are already written and waiting for that moment.

> 🇦🇺 **Australia only is now enforced in code.** `checkTargeting()` in `_meta-policy.mjs` fails any
> ad set outside AU, `doctor` asserts it on every run, and `report` audits every live ad set and
> prints offenders.

## Step 6 — Placements

1. **Advantage+ placements (automatic).** Do not hand-pick.
2. ⚠️ Note: **no Instagram account is linked to the ad account**, so this will run Facebook-only and
   you lose roughly half the inventory. Worth connecting Instagram first — see §Also worth doing.

## Step 7 — Attribution

1. Attribution setting: **7-day click, 1-day view** (the default)
2. Click **Next**

## Step 8 — Stop at the ad level

**Do not build an ad here. Click away or save as draft.**

The ad set is the container. Ads get published into it by the agent, always **PAUSED**, and you turn
them on. That is the approval gate — see below.

## Step 9 — Send me the ad set ID

Open the ad set, copy the ID from the URL or the ID column, and paste it to me. It looks like
`120233074187690186`. I will verify via the API that:

- `promoted_object` really contains `custom_conversion_id: 27686282527680441` (not
  `custom_event_type`, which is a different thing that looks identical in the UI)
- `geo_locations.countries` is exactly `["AU"]`
- `interests` is empty
- the budget and optimisation goal are what you intended

---

## 🔒 How I'm making sure no ad goes live without you

You asked for this explicitly. Here is what actually enforces it, verified in code this session:

| Layer | What it does | Where |
|---|---|---|
| **Autonomy rung 0** | The agent may report and propose. Nothing else. Verified: *"Rung 0 permits nothing unattended"* passes in `doctor` | `_meta-policy.mjs` |
| **Ads created PAUSED, always** | `publish_ad` hard-codes `status: "PAUSED"`. There is no code path that creates an active ad | `meta-ads.mjs` |
| **`create_ad_set` always needs a human** | In `ALWAYS_REQUIRES_APPROVAL` at *every* rung, including the highest | `_meta-policy.mjs` |
| **Writes need CONFIRM=1 *and* an approved row** | `apply` without both is a dry run | `meta-ads.mjs` |
| **The cron cannot spend** | Weekly job runs `report` then `evaluate --file_proposals`. It files proposals; it does not apply them | `app/api/cron/meta-ads` |
| **Only 3 write types exist at all** | `pause_ad`, `set_budget`, `publish_ad` (paused). There is no "activate ad" mutation in the codebase | `meta-ads.mjs` |

**In plain terms: the only way an ad goes live is you clicking the toggle in Ads Manager.** The worst
the agent can do unattended is file a proposal in the Cockpit for you to read.

I have not touched the account this session. Everything I ran was a read, except the HeyGen test
render, which went to HeyGen and not to Meta.

---

## 🇦🇺 Australia only — four ad sets need your attention

The new live audit found these. **All are `CAMPAIGN_PAUSED`, so nothing is spending right now**, but a
paused ad set is one un-pause away:

| Ad set | Problem |
|---|---|
| `Instagram post: CAMPBELL STREET \| Ground floor...` | Targets **US**. Spent **$43.82 for 0 results** |
| `Wed 23/7` | **No country targeting at all** — runs worldwide |
| `Adset 1` | **No country targeting at all** |
| `Adset 1` (second one) | **No country targeting at all** |

**Recommendation: delete them.** They are old boosted-post ad sets, they have no role in the plan, and
deleting removes the risk permanently. If you would rather keep the history, set each one's location to
Australia so an accidental un-pause cannot leak spend offshore.

I have not changed them — that is an account write and you have asked that nothing move without your
say-so. Say the word and I will propose it through the normal approval path.

---

## Also worth doing before you launch

1. **Link an Instagram account** to the ad account. `instagram_accounts` is empty, so you are
   Facebook-only, which roughly halves the inventory for a test that is already low-volume.
2. **Read EMQ by eye** — see below. It cannot be read via the API.
3. **Rotate `META_ACCESS_TOKEN`.** Meta's own `stats` endpoint returns the token inside its paging URL
   and a diagnostic printed it into a session transcript. Not committed anywhere. Cheap to fix.

---

## Why the agent cannot do this itself

Verified in `leepatt/cnccut-app` @ `main`:

- `promoted_object` appears **nowhere** in `tools/` — zero occurrences
- `apply` implements exactly three change types: `pause_ad`, `set_budget`, `publish_ad`
- there is **no `create_ad_set` executor**, though the guardrail requiring human approval for one exists

So the guard was built and the thing it guards was not. Building it is correct eventually, but it is a
new **spend-capable** outward-write path and it wants your explicit sign-off plus its own review —
not something to add unattended. The ad set is created once. Doing it by hand costs five minutes and
keeps that path out of the codebase until it earns its place.
