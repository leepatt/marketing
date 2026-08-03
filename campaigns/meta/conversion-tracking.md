# Phase 0 — Meta conversion tracking (the gate)

_Step-by-step. Nothing else in the Meta agent build starts until this is green._
_Written 2026-08-03 from live recon of the pixel, the ad account and Shopify — not from a template._

> **Companion docs:** `META-ADS-AGENT-BIBLE.md` (§4.6 for why we optimise on a combined lead event) ·
> `../adwords/conversion-tracking.md` (the Google equivalent, already done).

---

## What the recon actually found

I queried the pixel and the ad account directly. **The good news: tracking is far more built out than
our notes assumed.** The bad news is in the next section.

**Pixel `677437638374055` — "Craftons Web"** · last fired 2026-08-02 · healthy, not unavailable.

**Events firing, last 30 days:**

| Event | Count |
|---|---|
| ViewContent | 78,980 |
| PageView | 60,581 |
| AddToCart | 920 |
| **ConfiguratorStarted** (custom) | **812** |
| InitiateCheckout | 193 |
| **Purchase** | **97** |
| AddPaymentInfo | 45 |
| Search | 28 |

**Traffic is 72% iPhone** (101,449 of ~140k events), which makes CAPI more important here than for a
typical store, not less — iOS is exactly where browser-only tracking loses signal.

Two things already exist that we assumed didn't:
- A **`ConfiguratorStarted` custom event** is already instrumented and firing 812×/month.
- The pixel already fires the full standard ecommerce funnel.

---

## 🔴 The headline problem: the Purchase signal is inflated ~2.7×

| Source | Purchases, last 30 days |
|---|---|
| **Meta pixel** | **97** |
| **Shopify (actual orders)** | **36** |

**Meta thinks Craftons made 97 sales last month. Craftons made 36.**

This is not a rounding difference and it is not the sessions-vs-events distinction that explains the
AddToCart gap. A Purchase event should fire once per order.

**Why it matters more than it looks.** Andromeda decides who sees your ads by correlating *creative*
against *conversion signal*. If ~61 of every 97 conversions it learns from never happened, it is
optimising toward whatever pattern produces **duplicate firing**, not toward what produces sales.
This is a plausible contributor to the July collapse in §4.5 of the bible — the account scaled into a
signal that was partly phantom.

**Two likely causes**, and Step 1 distinguishes them:
1. **Double installation** — the Shopify Facebook & Instagram channel *and* a manual pixel snippet in
   the theme (and possibly the separate configurator app) each firing Purchase.
2. **Missing deduplication** — browser and server (CAPI) events both firing without a shared
   `event_id`, so Meta counts them as two.

> **Do not skip to the fun parts.** Fixing this is worth more than any creative work in Phase 3.

---

## 🔴 Second problem: Advanced Matching is OFF

The pixel reports `enable_automatic_matching: false`.

Advanced Matching sends hashed customer details (email, phone, name) with events so Meta can match
them to real accounts. With it off, **Event Match Quality is capped low** — and EMQ > 7 is the
prerequisite for Andromeda reading creative properly. This is a two-click fix with outsized impact.

## 🔴 Third gap: zero custom conversions exist

`customconversions` returns an empty array. **The combined high-intent event specified in bible §4.6
does not exist yet.** It has to be built before any campaign can optimise toward it.

Also note: `ConfiguratorStarted` is the *top* of the configurator funnel. What §4.6 needs is the
*bottom* — a configured quote request or submission. That event does not appear in the list, so it
either isn't instrumented or is named something not firing.

---

# The steps

Each step has an action and a **verification**. Don't tick a step you haven't verified.

## Step 1 — Find the duplicate Purchase source 🔴

**Do this first. Everything downstream is polluted until it's fixed.**

1. Open **Events Manager → Data sources → Craftons Web (`677437638374055`) → Overview**.
2. Select the **Purchase** event → **View details**.
3. Look at the **"Connection method"** breakdown. You're looking for whether Purchase arrives via
   **Browser**, **Server**, or **both**.
4. Check **Diagnostics** tab — Meta usually flags *"Duplicate events"* or *"Redundant Purchase events"*
   directly, with the offending sources named.

Then find every place the pixel is installed:

5. **Shopify admin → Settings → Apps and sales channels** — is **Facebook & Instagram** installed?
   If yes, it is firing Purchase automatically.
6. **Shopify admin → Online Store → Themes → Edit code** — search the theme (especially
   `theme.liquid` and any `checkout` templates) for `fbq(` or `677437638374055`. **A manual snippet
   here plus the Facebook channel = the duplicate.**
7. **Shopify admin → Settings → Customer events** — check for a manually added Meta pixel custom pixel.
8. **The configurator app** (`craftons-curves-calculator`, deployed on Vercel) — check whether it also
   fires Purchase. Given orders attribute to it in Shopify's referrer data, it's a strong candidate.

**The fix:** keep **exactly one** Purchase source. The Shopify Facebook & Instagram channel is the
right one to keep — it handles dedup and CAPI natively. Remove manual `fbq('track', 'Purchase')`
snippets from the theme and the configurator.

**✅ Verify:** after 48h, pixel Purchase count for a given day should match Shopify orders for that
day, ±1. I can check this for you — `node tools/meta-ads.mjs report` plus the Shopify order count.

---

## Step 2 — Turn on Advanced Matching 🔴

1. **Events Manager → Data sources → Craftons Web → Settings**.
2. Enable **Automatic Advanced Matching**.
3. Tick every available parameter: **email, phone, first name, last name, city, state, zip, country,
   external ID**.
4. If Shopify's Facebook channel is connected, also confirm **Customer data sharing** is on with
   **Enhanced** level: *Shopify admin → Facebook & Instagram → Settings → Data sharing*.

**✅ Verify:** Events Manager → Overview → the pixel's **Event Match Quality** score. Target **> 7**.
It updates within ~24–48h. If it stays below 7 after Step 3, the events aren't carrying customer data.

---

## Step 3 — Get CAPI running properly (browser + server, deduplicated) 🔴

72% iPhone traffic means browser-only tracking is losing a large share of conversions to ITP.

1. **Shopify admin → Settings → Apps and sales channels → Facebook & Instagram → Settings**.
2. Under **Data sharing**, set the level to **Maximum** — this is what enables the Conversions API
   alongside the browser pixel.
3. Confirm the pixel selected is **Craftons Web (677437638374055)** and not a second one.
4. **Deduplication is the part people get wrong.** Browser and server events must share an `event_id`.
   Shopify's native integration does this automatically. **A hand-rolled CAPI implementation will not
   unless you pass `event_id` explicitly on both sides** — this is the most common cause of exactly
   the 2.7× inflation in Step 1.

**✅ Verify:** Events Manager → Purchase → details → the connection breakdown should show **both
Browser and Server**, with a **"Deduplicated"** count. Deduplicated should be roughly half the raw
total, and the resulting net Purchase count should match Shopify orders.

---

## Step 4 — Instrument the high-intent quote event 🟠

Bible §4.6 optimises on a **configured quote request** — someone who has specified a curve — not a
generic contact form. `ConfiguratorStarted` fires 812×/month but is the wrong end of the funnel.

1. Decide the exact moment. Recommended: **the user submits a completed configuration** (a quote
   request or an add-to-cart from the configurator with real dimensions attached).
2. Fire a custom event named **`QuoteRequested`** at that moment, with:
   ```js
   fbq('trackCustom', 'QuoteRequested', {
     value: <estimated job value AUD>,
     currency: 'AUD',
     content_name: 'Radius Pro',
   }, { eventID: <same id sent server-side> });
   ```
3. This is code in the **configurator app**. I can implement it once you confirm which component
   represents "configuration complete" — that's the one thing I can't determine from outside.

**✅ Verify:** submit a test configuration; `QuoteRequested` appears in Events Manager **Test Events**
within seconds, carrying a value.

---

## Step 5 — Build the combined custom conversion 🟠

This is the thing the campaign will actually optimise toward. There are currently **zero** custom
conversions, so this is a clean build.

1. **Events Manager → Custom conversions → Create custom conversion**.
2. **Data source:** Craftons Web.
3. **Name:** `Craftons — High Intent (Quote + Purchase)`.
4. **Rules:** include events **`QuoteRequested`** *OR* **`Purchase`**.
   - **Do NOT include** `AddToCart`, `ViewContent`, `PageView`, or `ConfiguratorStarted`. The July
     campaign optimised on `AddToCart` and bought 2,476 clicks a day for zero results (bible §4.5).
     That is the exact mistake this step exists to prevent.
5. **Optimisation category:** Lead.
6. **Value:** use the event value so Meta can eventually move to value optimisation.

**✅ Verify:** the custom conversion shows a healthy status and starts accruing within 24h. Expected
volume ≈ `QuoteRequested` + ~36 purchases/month.

---

## Step 6 — Send Purchase with real value via CAPI 🟠

Even though we optimise on the combined event, **Purchase must carry its true AUD value from day one**
— that's what makes the later switch to value optimisation a step change instead of a cold start
(bible §4.6, graduation).

Shopify's native integration does this automatically once Step 3 is done. Verify rather than assume.

**✅ Verify:** Events Manager → Purchase → recent events show a **value** in AUD, and the 30-day total
value approximates Shopify's gross sales (~$39,420 for the last 30 days).

---

## Step 7 — Close the lead → sale loop 🟡

Cost-per-lead is a vanity metric unless it converts to CAC. We need to know what fraction of
`QuoteRequested` becomes a paid order.

1. Decide how a quote is matched to its eventual order — email, or a quote reference carried into the
   Shopify order.
2. This is reportable from data Craftons already holds; I can build it into `meta-ads.mjs` as a
   `cac` subcommand once the matching key is decided.

**✅ Verify:** a number exists for "of N quote requests last month, M became orders."

---

## Step 8 — Confirm the gross margin 🟡

The kill criteria and ramp trigger both key off break-even CAC, currently assuming **~45% margin →
~$277**. If the real figure is 30%, break-even is ~$184 and the current rules are too permissive.

**Xero is connected — I can derive this** if you'd rather not dig it out. Say the word.

---

# Definition of done

Phase 0 is green when **all** of these are true:

- [ ] **Pixel Purchase count matches Shopify orders ±1** over a 7-day window
- [ ] **Event Match Quality > 7** in Events Manager
- [ ] **Purchase shows both Browser and Server** with deduplication working
- [ ] **`QuoteRequested` fires** on a completed configuration, with a value
- [ ] **The combined custom conversion exists** and is accruing
- [ ] **Purchase carries AUD value**, 30-day total ≈ Shopify gross sales
- [ ] Lead → sale close rate is known
- [ ] Gross margin confirmed, break-even CAC recalculated

---

# Who does what

**Only Lee can do** (needs Shopify admin / Events Manager / Business Manager logins):
Steps 1 (audit), 2, 3, 5 — and the decision in Step 4 about which moment counts as "configured".

**I can do** once unblocked:
- Step 4's implementation, in the configurator app, once you name the component
- Step 7's `cac` subcommand, once the matching key is decided
- Step 8, from Xero
- **Verification of every step** — I can query the pixel and Shopify directly and tell you whether a
  fix worked, rather than you having to eyeball dashboards

**Fastest path:** do Step 1 and Step 2 today. Step 1 is the one that's actively costing money, and
Step 2 is two clicks. Tell me when they're done and I'll re-run the recon and confirm.
