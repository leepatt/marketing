# Craftons — Retargeting plan (2026-07-21)

_How we re-reach warm visitors who didn't buy. Prompted by the architrave sale #1263: a builder
configured, left, and came back 2 days later — the 2-day gap is exactly what retargeting fills._

## Live audience check (Google Ads account 3104912421, pulled 2026-07-21)
The **Shopify Google & YouTube app is already building remarketing audiences**, and the site-level ones
**are populating and above Google's minimums** (Display/Demand Gen needs **100**, Search RLSA needs **1,000**):

| Audience | Display size | Search size | Usable for… |
|---|---|---|---|
| All Converters | 2,600 | 3,000 | exclusions / lookalikes |
| **All visitors (AdWords)** — 30d | **360** | 430 | ✅ **Display/Demand Gen today** (>100) |
| **Product viewers (Retail)** — 30d | **190** | 130 | ✅ **Display/Demand Gen today** (>100) |
| General visitors (Retail) — 30d | 140 | 170 | ✅ Display (>100) |
| Shopping cart abandoners (Retail) | 16 | 16 | ❌ too small |
| Past buyers (Retail) | 8 | 0 | ❌ too small (use for exclusion) |

**So: site-level Display/Demand-Gen retargeting is viable NOW** (All visitors 360, Product viewers 190).
**Architrave-only and cart-abandoner retargeting are NOT** — those pools are ~16–20 people, below threshold.
**Search RLSA is not viable** either (max list 430 < 1,000 needed).

⚠️ **Broken lists to fix:** the custom GA4/tag audiences — *All Users of Craftons, Purchasers of Craftons,
Form Submit/Form Starts (30/60/180/365d)* — are **all at size 0**. They're defined but **not populating**
(GA4 audience export not linked, or the tag isn't feeding them). Worth fixing so we get form-based and
purchaser lists over time — but the Shopify-app "(Retail)" lists above already cover the basics.

## The plan (by horizon)

### 1. NOW — Display/Demand-Gen retargeting to warm site visitors ✅ viable today
One campaign, audience = **"All visitors" + "Product viewers"**, **exclude "Past buyers/All Converters"**.
- Format: **Demand Gen** (image/video, runs across YouTube + Discover + Gmail) — best for a visual product.
- Creative: best finished-arch + Radius shots (the AI in-situ images slot in here), one-line value prop,
  "Custom-cut to your sizes · Australian made · CNC-precise."
- Budget: small — **$10–15/day** is plenty for a 360-person pool; retargeting CPMs are cheap.
- Goal: stay in front of the ~360 warm visitors for the 30-day window; catch the 2-day-gap buyers.

### 2. NOW — Shopify abandoned-checkout recovery email (free) — copy below
Catches anyone who reaches checkout + enters email but doesn't pay. Only ~3 real/month, but each is
$400–$2,300, so it pays for itself. **Note: this is an admin-only setting — it's NOT exposed to the API,
so it must be switched on in-admin (see below); I can't flip it via the connector, but the copy is ready.**

**Where to switch it on:** Shopify admin → **Marketing → Automations** → "Abandoned checkout" (or
Settings → Checkout → "Abandoned checkouts") → **Turn on** → paste the copy below.

**Subject:** Your custom Craftons order is saved — ready when you are
**Preview:** Pick up right where you left off.

> Hi {{ first_name | default: "there" }},
>
> You were partway through a custom order with Craftons — it's **saved and ready to finish**.
>
> Everything's **cut to your exact sizes**, CNC-precise, **Australian made**, and dispatched fast so it's
> on site when you need it. No hand-shaping, no guesswork.
>
> **[ Finish my order → ]**  ({{ checkout_url }})
>
> Questions about sizes, finish or freight? Just reply to this email — a real person will help.
> Running regular jobs? Ask us about a **Trade Account**.
>
> — The Craftons team

_(Trade tone, no discount — these are B2B builders pricing real jobs, not deal-hunters. Add a code later
only if recovery is weak.)_

### 3. Lee is building — email capture inside the builder ⭐ biggest unlock
Anonymous config-builders (like #1263 on visit 1) can't be retargeted at all. A "Email me my quote / save
my config" step turns every builder into a reachable lead **and** feeds a real architrave audience. Dev job
on cnccut.app. This is #1 by leverage — it fixes the root cause (no identity = no retargeting).

### 4. 4–8 weeks — architrave-specific + form audiences
Once (3) ships and traffic accumulates, build an **architrave-viewer** and **quote-abandoner** audience;
by then they'll cross 100 and we can retarget architraves specifically (currently impossible at ~20 people).

## Recommended sequence
(2) turn on abandoned-checkout email today → (1) launch the small Demand-Gen retargeting campaign →
(3) Lee ships builder email capture → (4) build arch-specific audiences + fix the 0-size GA4 lists.
