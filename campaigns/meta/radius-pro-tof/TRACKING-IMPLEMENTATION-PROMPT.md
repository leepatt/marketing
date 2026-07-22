# Paste-into-new-session prompt: wire Meta tracking into the Radius Pro configurator

Copy everything below the line into a new Claude Code session opened on the `craftons-curves-calculator`
repo.

---

**Task: add Meta Pixel + Conversions API tracking to the Radius Pro configurator. Tracking only, no UX,
flow, or pricing changes.**

**Why this matters (context):**
We run Meta ads driving traffic to `craftons.com.au/products/radius-online` (Shopify template
`radius-pro`, a custom-priced product powered by this calculator). Right now Meta only sees the base
PageView. The configurator's real intent action, **"add part to list"** (where the user has built a
part and a real price appears), is a custom action the Meta pixel never sees, so we are blind to
engagement, cannot build retargeting audiences, and cannot optimise campaigns toward the money action.
About 94% of this traffic is the Facebook in-app browser on iOS, where the browser pixel drops events,
so server-side (Conversions API) matters.

**Reference values:**
- Meta Pixel ID: `677437638374055` (named "Craftons Web")
- Shopify product: handle `radius-online`, product id `8464537125042`, variant id `45300623343794`
- Currency: `AUD`
- Live page: `https://craftons.com.au/products/radius-online`

**Step 0. Understand the codebase before writing anything.**
Explore the repo and answer these first, then tell me what you found:
1. Framework and build (React, Vue, vanilla, Web Component, Shopify theme app extension, etc.) and how
   the calculator is bundled and loaded onto the Shopify product page.
2. **Critical: is the calculator rendered in the SAME document as the Shopify page, or inside an
   IFRAME?** This decides how we reach the pixel:
   - Same document: `window.fbq` is the page pixel and is already initialised by Shopify. Call it directly.
   - Iframe: `window.fbq` inside the iframe is NOT the page pixel. Do one of: (a) `postMessage` the event
     to the parent page and add a tiny listener in the Shopify theme that calls `fbq`, or (b) send the
     event server-side via the Conversions API, or (c) initialise a pixel inside the iframe. Prefer CAPI
     plus postMessage. Flag which applies.
3. The exact code locations for these hook points:
   - app init / first render on the product page (for ViewContent),
   - the handler that runs when a user **adds a part to the list and the price is known** (for AddToCart),
   - the handoff to the Shopify cart / checkout (for InitiateCheckout),
   - any backend or serverless function in this repo (for the Conversions API).

**Step 1. Events to implement (the funnel map):**

| Moment | Meta event | Fire when |
|---|---|---|
| Radius Pro page loads / calculator mounts | `ViewContent` | on load |
| User starts building (first meaningful input) | `ConfiguratorStarted` (custom) | first interaction, once per session |
| **User adds a part to the list and the price shows** | **`AddToCart`** | on that action, after price is computed |
| User proceeds to Shopify checkout | `InitiateCheckout` | on the handoff/checkout |
| Order placed | `Purchase` | order confirmation (likely already fired by the Shopify theme, verify) |

**Step 2. Browser pixel code (guard every call).** Only add `fbq('track', ...)` calls; the base
`fbq('init', ...)` already exists on the page.

```js
const track = (name, params, opts) => {
  if (typeof window !== 'undefined' && typeof window.fbq === 'function') window.fbq('track', name, params, opts);
};
const CONTENT = { content_ids: ['8464537125042'], content_name: 'Radius Pro', content_type: 'product' };

// on page load / mount
track('ViewContent', { ...CONTENT, currency: 'AUD' });

// first configurator interaction, once per session (guard with a flag)
if (typeof window.fbq === 'function') window.fbq('trackCustom', 'ConfiguratorStarted', { content_name: 'Radius Pro' });

// on "add part to list", AFTER the price is calculated. THE KEY EVENT.
const eventId = crypto.randomUUID(); // reuse this exact id for the server-side CAPI send
track('AddToCart', {
  ...CONTENT,
  contents: [{ id: '8464537125042', quantity: 1, item_price: partPrice }],
  value: partPrice,       // number, AUD, the price just shown to the user
  currency: 'AUD'
}, { eventID: eventId });

// on checkout handoff
track('InitiateCheckout', { ...CONTENT, value: cartTotal, currency: 'AUD', num_items: numItems });
```

If the calculator is in an iframe, replace the direct `fbq` calls with `window.parent.postMessage({type:'meta-track', name, params, eventId}, 'https://craftons.com.au')` and add a listener in the Shopify theme that calls `fbq` with the payload. Tell me if this is the case and I will also give you the theme-side listener.

**Step 3. Conversions API (server-side), same `event_id` for dedup.** For `AddToCart`, `InitiateCheckout`,
and `Purchase`, also send server-side so iOS in-app-browser events are not lost. If this repo has a
backend, POST to `https://graph.facebook.com/v21.0/677437638374055/events` with a CAPI access token,
sending: `event_name`, `event_time`, `action_source: 'website'`, the **same `event_id`** as the browser
event, `event_source_url`, `user_data` (pass the `_fbp` and `_fbc` cookies from the browser plus client
IP and user agent for matching), and `custom_data` (`value`, `currency`, `content_ids`). Store the CAPI
token in an env var. **Do not hardcode or commit it.** If there is no backend here, note it and we will
send CAPI from the Shopify side instead.

**Step 4. Rules:**
- `value` is the price the user sees, as a number, in AUD, consistent basis across all events (recommend inc-GST, ex-shipping).
- Guard every browser call with `typeof window.fbq === 'function'`.
- Fire `AddToCart` exactly once per "add to list" click. Do not also fire it when the list later pushes to the Shopify cart (avoid double counting).
- Do not commit any token or secret.

**Step 5. Test and report.** Use Meta Events Manager, Test Events, and walk the flow on a phone:
ViewContent on load, AddToCart with the correct AUD value on add-to-list, a second AddToCart on a second
part, InitiateCheckout at checkout, Purchase on completion, and no duplicate AddToCart. Then report which
files you changed, whether it was same-document or iframe, and whether CAPI was wired.

**Do not** change the calculator UI, the two-step add-to-list-then-checkout flow, or any pricing.

---
