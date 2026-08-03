# Phase 0 — Meta conversion tracking (the gate)

_Step-by-step. Nothing else in the Meta agent build starts until this is green._
_Written 2026-08-03 from live recon of the pixel, the ad account, Shopify **and the configurator
source code** — not from a template. Revised after tracing the configurator's tracking._

> **Companion docs:** `META-ADS-AGENT-BIBLE.md` (§4.6, optimisation event) ·
> `../adwords/conversion-tracking.md` (the Google equivalent, already done).

---

## What the recon found

**Pixel `677437638374055` — "Craftons Web"** · last fired 2026-08-02 · healthy.

**Events firing, last 30 days:**

| Event | Count | Per week | What it means |
|---|---|---|---|
| ViewContent | 78,980 | — | Configurator mount, once per page load |
| PageView | 60,581 | — | Standard |
| **AddToCart** | **920** | ~215 | **Once per part added** — see below, this is by design |
| ConfiguratorStarted (custom) | 812 | ~190 | First meaningful interaction, once per session |
| **InitiateCheckout** | **193** | **~45** | **Handoff to the Shopify cart — the real high-intent event** |
| Purchase | 97 | ~23 | ⚠️ but Shopify records only 36 orders |
| AddPaymentInfo | 45 | — | |
| Search | 28 | — | |

**Traffic is 72% iPhone.** The configurator's own code comments put ad traffic at ~94% iOS Facebook
in-app browser — which drops browser pixel events. This is why CAPI matters here more than usual.

### The configurator tracking is genuinely well built

I read `craftons-curves-calculator/src/app/lib/meta-tracking.ts` and the CAPI relay. It is careful work
and **it is not the problem**:

- The calculator runs in a **cross-origin iframe** on the Shopify product page, so it `postMessage`s
  browser events to the parent, where `CORRECTED_FULL_SECTION.liquid` calls the page's `fbq`.
- **Server-side CAPI events carry the same `event_id`** as the browser event, which is exactly how
  deduplication is supposed to work. Most people get this wrong; this doesn't.
- `_fbp` / `_fbc` cookies are fetched from the parent via a handshake and attached to CAPI sends.
- It fires **only** `ViewContent`, `ConfiguratorStarted`, `AddToCart`, `InitiateCheckout`.

### ✅ Two things I flagged earlier that are NOT problems

**1. AddToCart at 920/month is by design, not inflation.** It fires **once per "add part to list"
click**, with that part's price. Someone configuring a staircase adds many parts. My earlier
comparison against Shopify's *sessions with cart additions* was comparing events to sessions —
not a like-for-like. Nothing to fix.

**2. The configurator does not fire Purchase.** `meta-tracking.ts` has no Purchase function at all.
(The CAPI route's allow-list *permits* Purchase, but nothing client-side ever sends it — a permissive
allow-list, not an active source.) **The configurator is cleared as a duplicate suspect.**

---

## 🔴 The one real problem: Purchase is inflated ~2.7×

| Source | Purchases, last 30 days |
|---|---|
| **Meta pixel** | **97** |
| **Shopify (actual orders)** | **36** |

A Purchase should fire once per order. Andromeda decides who sees your ads by correlating creative
against conversion signal — if ~61 of every 97 conversions it learned from never happened, it has been
optimising toward whatever produces **duplicate firing** rather than sales. **This is a plausible
contributor to the July collapse** (bible §4.5).

**The suspect list is now short.** The configurator is cleared, so Purchase can only be coming from
the Shopify side:

1. **The Shopify Facebook & Instagram channel** (fires Purchase automatically), **and**
2. **A manual `fbq('track','Purchase')` snippet** in the theme or in Settings → Customer events.

Both firing = exactly the ~2× you'd expect. That's Step 1.

## 🔴 Advanced Matching is OFF

`enable_automatic_matching: false`. This caps Event Match Quality, and **EMQ > 7 is the prerequisite**
for Andromeda reading creative properly. Two clicks.

Related: the configurator's CAPI relay sends `client_ip_address`, `client_user_agent`, `fbp` and `fbc`
— but **no hashed email or phone**. For AddToCart that's largely unavoidable (no email yet), but it
does mean those events will never score highly on match quality.

## 🔴 Zero custom conversions exist

`customconversions` returns empty. The event the campaign will optimise toward has to be built.

---

# The steps

Each has an action and a **verification**. Don't tick one you haven't verified.

## Step 1 — Kill the duplicate Purchase 🔴

**Do this first.** Everything downstream is polluted until it's fixed. The configurator is cleared, so
look only at Shopify:

1. **Events Manager → Data sources → Craftons Web → Purchase → View details.** Check the
   **connection method** breakdown (Browser / Server / both) and the **Diagnostics** tab — Meta
   usually names duplicate sources directly.
2. **Shopify admin → Settings → Apps and sales channels** — is **Facebook & Instagram** installed?
   If yes, it fires Purchase automatically. **This is the one to keep.**
3. **Shopify admin → Settings → Customer events** — look for a manually added Meta custom pixel
   firing Purchase. **This is the most likely culprit.**
4. **Shopify admin → Online Store → Themes → Edit code** — search `theme.liquid` and any checkout /
   order-status templates for `fbq(` or `677437638374055`. Note the configurator's section file
   (`CORRECTED_FULL_SECTION.liquid`) legitimately contains `fbq` — **that one relays configurator
   events and must stay.** You're looking for a *Purchase* call, which it does not contain.

**Fix:** keep exactly one Purchase source — the Facebook & Instagram channel, which handles dedup and
CAPI natively. Remove the other.

**✅ Verify:** after 48h, pixel Purchase for a given day should match Shopify orders ±1.
**I can check this for you** — I have both data sources.

---

## Step 2 — Turn on Advanced Matching 🔴

1. **Events Manager → Data sources → Craftons Web → Settings**.
2. Enable **Automatic Advanced Matching**; tick every parameter (email, phone, name, city, state, zip,
   country, external ID).
3. **Shopify admin → Facebook & Instagram → Settings → Data sharing** — set to **Maximum**.

**✅ Verify:** Events Manager → Overview → **Event Match Quality > 7**, within ~24–48h.

---

## Step 3 — Confirm CAPI on the Purchase path 🔴

**Partly done already.** The configurator already runs CAPI for `AddToCart` and `InitiateCheckout`
with proper dedup. What's missing is the **Purchase** path, which lives on Shopify.

1. Setting data sharing to **Maximum** in Step 2 enables CAPI for Shopify's own events.
2. Confirm the channel points at pixel **677437638374055** and not a second one.
3. Confirm `META_CAPI_ACCESS_TOKEN` is still set in the configurator's Vercel project — without it the
   relay silently skips (by design), and you'd lose iOS AddToCart/InitiateCheckout signal without any
   error showing.

**✅ Verify:** Purchase shows **both Browser and Server** with a **deduplicated** count, and the net
matches Shopify orders.

---

## Step 4 — Pick the optimisation event ✅ (probably no code needed)

**Good news: the event we need already exists.** I'd planned a new `QuoteRequested` event. On reading
the configurator, **`InitiateCheckout` already is it** — it fires on handoff to the Shopify cart with
the real cart total, only after someone has configured parts. That is genuinely high intent.

And the volume works, which is the thing that kills most accounts at this budget:

| Candidate | Per week | vs Meta's ~50/wk learning threshold |
|---|---|---|
| Purchase (real) | ~8 | ❌ 6× short |
| **InitiateCheckout** | **~45** | ✅ **essentially at threshold** |
| **InitiateCheckout + Purchase** | **~53** | ✅ **clears it** |
| AddToCart | ~215 | ❌ too loose — fires per part, and is what failed in July |
| ConfiguratorStarted | ~190 | ❌ top of funnel |

**Recommendation: optimise on `InitiateCheckout` + `Purchase` combined** (~53/week). That clears the
learning threshold with margin, and both events mean someone with a configured cart. Nothing to build.

> This supersedes the `QuoteRequested` plan in earlier drafts. **One caveat:** a buyer fires both IC
> and Purchase, so "results" isn't a clean count of people. That's fine for optimisation — it's a
> stronger signal, not a corrupted one — but read revenue, not result count, as the scoreboard.

---

## Step 5 — Build the combined custom conversion 🟠

1. **Events Manager → Custom conversions → Create custom conversion**.
2. **Data source:** Craftons Web.
3. **Name:** `Craftons — High Intent (Checkout + Purchase)`.
4. **Rules:** `InitiateCheckout` **OR** `Purchase`.
   - **Do NOT include** `AddToCart`, `ViewContent`, `PageView` or `ConfiguratorStarted`. July's
     campaign optimised on `AddToCart` and bought 2,476 clicks/day for zero results (bible §4.5).
     This step exists to prevent exactly that.
5. **Optimisation category:** Lead. **Value:** use the event value.

**✅ Verify:** accruing within 24h at roughly 53/week.

---

## Step 6 — Purchase carries real AUD value 🟠

Needed so the later switch to value optimisation is a step change, not a cold start (bible §4.6).
Shopify's native integration does this once Step 3 is done — verify rather than assume.

**✅ Verify:** 30-day Purchase value ≈ Shopify gross sales (~$39,420 last 30 days).

---

## Step 7 — Close the checkout → sale loop 🟡

We optimise on InitiateCheckout, so we need to know what fraction becomes a paid order.
Right now: **193 InitiateCheckout → 36 orders ≈ 19%.** Worth confirming that's a real drop-off and not
an attribution artefact — a 19% checkout-to-order rate is low enough to be worth investigating on its
own merits, independent of ads.

**I can build this** into `meta-ads.mjs` as a `cac` subcommand.

---

## Step 8 — Confirm the gross margin 🟡

Kill criteria and ramp trigger both key off break-even CAC, currently assuming ~45% margin → ~$277.
If it's really 30%, break-even is ~$184 and the current rules are too permissive.
**Xero is connected — I can derive this.**

---

# Definition of done

- [ ] **Pixel Purchase matches Shopify orders ±1** over 7 days
- [ ] **Event Match Quality > 7**
- [ ] **Purchase shows Browser + Server**, deduplicated
- [ ] `META_CAPI_ACCESS_TOKEN` confirmed live in Vercel
- [ ] **Combined custom conversion exists** and accrues ~53/week
- [ ] **Purchase carries AUD value**, 30-day total ≈ Shopify gross sales
- [ ] Checkout → sale rate known
- [ ] Gross margin confirmed, break-even CAC recalculated

---

# Who does what

**Only Lee** (needs Shopify admin / Events Manager): Steps 1, 2, 3, 5.

**I can do:** Step 7's `cac` subcommand · Step 8 from Xero · **verification of every step** — I can
query the pixel and Shopify directly and tell you whether a fix landed.

**Fastest path: Steps 1 and 2 today.** Step 1 is actively corrupting the signal your ads optimise on;
Step 2 is two clicks. Tell me when they're done and I'll re-run the recon.

> **Step 4 needing no work is the good news here** — the high-intent event already exists, at a volume
> that clears Meta's learning threshold. Phase 0 is smaller than it looked.
