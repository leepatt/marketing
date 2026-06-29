# Conversion tracking setup (Shopify → Google Ads)

_Without this you're spending blind (see the CNC Cut account: ~$2k/mo, 0 tracked conversions). Set
this up for **each store** (Craftons + CNC Cut), each linked to its own Google Ads account. Do the
steps in order — Step 1 alone gets you purchase tracking fast._

## What counts as a conversion (and rough value)
Assigning a value lets Google optimise toward *valuable* leads, not just any click.

| Conversion | Type | Count | Suggested value |
|------------|------|-------|-----------------|
| **Online order / checkout** (configurator + products) | Purchase | Every | Actual order value (dynamic) |
| **Quote / contact form submit** | Lead | One | Est. lead value (e.g. avg job × close rate, even rough) — **primary** |
| **Phone call** (from ad + from website) | Lead | One | Est. lead value |
| **Email click** (mailto) | Lead | One | Low / secondary (observe only) |

Mark **orders + form submits** as **Primary** (used for bidding). Calls/emails can be **Secondary**
(tracked, not optimised on) until you trust them.

---

## Step 1 — Shopify "Google & YouTube" app (fastest — handles purchases)
1. Shopify admin → **Settings → Apps and sales channels** (or **Sales channels → +**) → add
   **Google & YouTube**.
2. Connect the **Google account** that owns the right Google Ads account; **link the Google Ads account**.
3. It auto-sets-up **purchase conversion tracking** (and can sync products to Merchant Center later).
4. Turn on **Enhanced Conversions** when prompted (sends hashed email/phone → more accurate matching).

This gets *sales* tracked with almost no effort. Leads (forms/calls) come next.

## Step 2 — GA4 for the full funnel (leads + checkout steps)
1. Make sure **GA4 is installed** on the store (the Google & YouTube app can set this up, or
   Shopify → **Online Store → Preferences → Google Analytics**).
2. In **GA4 → Admin → Events / Key events**, mark these as **key events (conversions)**:
   `purchase`, `generate_lead` or `form_submit` (quote/contact), `begin_checkout` (configurator
   checkout started).
3. **Link GA4 → Google Ads:** GA4 → Admin → **Product links → Google Ads → Link**.
4. **Import into Google Ads:** Google Ads → **Goals → Conversions → + New → Import → GA4** → select
   the key events above.

## Step 3 — Lead conversions in Google Ads (forms, calls)
For tighter lead tracking, create these directly: Google Ads → **Goals → Conversions → + New action → Website**.
- **Submit lead form** (quote/contact):
  - Easiest if your form redirects to a **thank-you page** → track that page-load as the conversion.
  - If it's an AJAX form (no redirect) → use the GA4 `form_submit` event from Step 2 instead.
- **Phone calls:**
  - **Calls from ads** → from the call extension/asset (track calls ≥ a sensible length, e.g. 30s).
  - **Clicks on your phone number** on the website (mobile).
- **Email clicks** (mailto) → a click conversion, set as **Secondary**.
- Turn on **Enhanced Conversions for leads** in the conversion settings.

## Step 4 — Verify (don't trust it until you've tested)
- **Test a real form submit** and a **test order** → check Google Ads → Conversions shows status
  **"Recording conversions"** (not "No recent conversions" / "Inactive").
- Use **Google Tag Assistant** to confirm tags fire on the thank-you/checkout pages.
- Give it 24–48h, then the campaign data starts showing real conversions + cost-per-lead.

## After it's live
- Once you have **~15–30 conversions**, switch bidding from *Maximise clicks* to **Maximise
  Conversions** (or Target CPA) so Google optimises for *leads*, not clicks.
- Then the weekly review (`campaign-setup.md`) finally has a real scoreboard: **cost-per-lead vs.
  job value.**

> Note for the CNC Cut account specifically: it's spending ~$2k/mo on *Maximise clicks* with 0 tracked
> conversions — do this setup there first/too, and reconsider the $19/click "Industry Specific" campaign
> once you can see which spend actually produces leads.
