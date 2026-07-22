# Radius Pro configurator. Meta Pixel + Conversions API tracking spec

**For:** the developer who built the Radius Pro configurator / the Craftons Shopify theme.
**Goal:** make the Meta (Facebook) pixel see the configurator funnel, so we can measure real intent,
build retargeting audiences, and later optimise ad campaigns toward the money actions.

## Why this is needed (the gap we found)

The Radius Pro page (`craftons.com.au/products/radius-online`, custom template `radius-pro`, a
custom-priced product) currently only fires the base **PageView**. Meta sees the landing page view and
nothing after it. The reason: the configurator is bespoke, and its key action, **"add part to list"**
(where the user has built a part and a real price appears), is a custom in-app action, not a standard
Shopify add-to-cart, so the pixel never sees it. The most valuable intent signal in the whole funnel
is invisible. This spec fixes that.

Confirmed working: the full flow (build, add to list, cart, checkout, payment) works on mobile. This
is a tracking task, not a UX change.

## The event map

Fire these events at these moments. Use the Meta Pixel (`fbq`) in the browser AND the Conversions API
server-side, deduplicated by a shared `event_id` (see below). All monetary values in **AUD**.

| Funnel moment | Meta event | Fire when |
|---|---|---|
| Land on the Radius Pro page | `ViewContent` | page load |
| User starts building (first meaningful input, e.g. enters a radius or picks material) | `ConfiguratorStarted` (custom) | first configurator interaction, once per session |
| **User clicks "add part to list" and the price is shown** | **`AddToCart`** | on that click, after the price is computed |
| User proceeds to the Shopify checkout | `InitiateCheckout` | checkout page load |
| Order placed | `Purchase` | order confirmation / thank-you page |

**`AddToCart` on "add part to list" is the important one.** That is the priced-part intent signal we
are missing today.

## Exact calls (browser pixel)

The base pixel (`fbq('init', ...)`) is already present on the template (that is why PageView fires), so
you only need to add these `fbq('track', ...)` calls at the hook points.

```js
// 1. On Radius Pro page load
fbq('track', 'ViewContent', {
  content_ids: ['8464537125042'],      // match the id used in your Meta product catalog feed
  content_name: 'Radius Pro',
  content_type: 'product',
  currency: 'AUD'
});

// 2. First configurator interaction (once per session) - optional but useful
fbq('trackCustom', 'ConfiguratorStarted', { content_name: 'Radius Pro' });

// 3. On "add part to list", AFTER the price is calculated  <-- the key event
const eventId = crypto.randomUUID();  // reuse this same id for the server-side CAPI call
fbq('track', 'AddToCart', {
  content_ids: ['8464537125042'],
  content_name: 'Radius Pro',
  content_type: 'product',
  contents: [{ id: '8464537125042', quantity: 1, item_price: PART_PRICE }],  // PART_PRICE = the price shown
  value: PART_PRICE,                   // number, AUD, the price the user just saw
  currency: 'AUD'
}, { eventID: eventId });

// 4. On checkout page
fbq('track', 'InitiateCheckout', {
  value: CART_TOTAL,
  currency: 'AUD',
  num_items: NUM_ITEMS,
  content_ids: ['8464537125042']
});

// 5. Purchase - normally fired by Shopify's native Meta integration on the order page.
// Verify it fires for these custom-priced orders with the correct order value; if not, fire it manually:
fbq('track', 'Purchase', {
  value: ORDER_TOTAL, currency: 'AUD', content_ids: ['8464537125042'], content_type: 'product'
});
```

## Value and currency rules

- `value` = the **price the user sees** for that part / cart / order, as a number (e.g. `1450.00`), in
  **AUD**. Be consistent: use the same basis (ex-GST or inc-GST) across all events. Recommend the
  customer-facing price (inc-GST), ex-shipping.
- `currency` = `'AUD'` on every event.
- `content_ids` must match whatever id Radius Pro uses in the **Meta product catalog feed** (likely the
  product id `8464537125042` or the variant id). If unsure, use the product id and we will confirm the
  catalog matches.

## Conversions API (server-side) and deduplication

94% of this traffic is the **Facebook in-app browser on iOS**, where the browser pixel is unreliable
and events get dropped. So the key events (`AddToCart`, `InitiateCheckout`, `Purchase`) should also be
sent **server-side via the Meta Conversions API**, using the **same `event_id`** as the browser event
so Meta deduplicates them. Shopify's Meta channel may already send CAPI for the standard Shopify
events; the custom `AddToCart` on "add to list" is the one that needs to be sent from your side (browser
`eventID` + a matching server event, or via the Conversions API with the same `event_id`).

If server-side is not feasible immediately, ship the browser events first. They are still a big
improvement over the current PageView-only state.

## Acceptance criteria (how we verify)

In Meta **Events Manager, Test Events**, walk the flow on a phone and confirm:
1. `ViewContent` fires once on page load.
2. `AddToCart` fires once when you add a part to the list, with the correct `value` in AUD.
3. Adding a second part fires a second `AddToCart`.
4. `InitiateCheckout` fires once at checkout with the cart total.
5. `Purchase` fires once on order completion with the order total.
6. **No duplicate `AddToCart`** from the later Shopify cart step (if Shopify's native pixel also fires
   one when the list pushes to the cart, tell us so we adjust the mapping to avoid double counting).

## Out of scope

- No UX or flow changes. The two-step "add to list then checkout" stays as is.
- No pricing logic changes.
