# Bug + Fix Brief: Radius Pro configurator AddToCart attribution (paste into a craftons-curves-calculator session)

## Symptom
Meta ad reporting shows only ~2 ad-attributed AddToCart events, while the pixel's total
AddToCart is ~55/24h (and growing). The configurator works and people use it. The problem is
attribution, not usage: ad-driven configurator adds are firing without the Meta click ID, so Meta
files them as unattributed. We are under-measuring the ads badly.

## Root cause
Attribution depends on the Meta click ID (`_fbc`, derived from `fbclid` on the ad link) reaching
Meta WITH the AddToCart event. `_fbc` is a cookie on craftons.com.au. The configurator runs in a
cross-origin iframe (craftons-curves-calculator.vercel.app) that cannot read that cookie. The code
bridges this three ways, all fragile for exactly the users ads send:

1. **Handshake race.** `meta-tracking.ts` asks the parent (CORRECTED_FULL_SECTION.liquid) for
   `_fbp`/`_fbc` via a `META_PIXEL_CONTEXT_REQUEST` postMessage, then attaches `fbc` to the CAPI
   send. If a part is added before the handshake resolves (or it fails in the sandboxed mobile
   context), `pixelContext.fbc` is null and the event goes out with no click ID.
2. **Pixel runs in Shopify Web Pixels sandbox.** Pixel 677437638374055 is a Web Pixels Manager app
   pixel, not a classic `window.fbq`. The theme bridge does `if (typeof window.fbq === 'function')`
   and silently no-ops when absent. Some browser events slip through (why any events show), but it
   is inconsistent.
3. **iOS in-app browser drops browser events.** Per the code's own comment ~94% of ad traffic is the
   iOS Facebook in-app browser, which kills browser pixel events, so ad clickers rely almost entirely
   on the CAPI path, which only attributes if `fbc` from point 1 made it through.

Net: events fire and are counted (55), click IDs are frequently missing, ad attribution collapses (2).

## Files involved
- `src/app/lib/meta-tracking.ts` — client tracking; requests fbp/fbc from parent, fires browser +
  CAPI. `trackAddToCart()` is the key event.
- `src/app/api/meta/capi/route.ts` — server CAPI relay. Correctly sends fbc/fbp/ip/ua IF `body.fbc`
  is populated. Needs `META_CAPI_ACCESS_TOKEN` in Vercel env (skips silently if unset — verify it is
  set).
- `CORRECTED_FULL_SECTION.liquid` — the deployed Shopify theme section. Builds the iframe `src`,
  responds to the pixel-context handshake, bridges META_TRACK_REQUEST to window.fbq.

## The fix (cleanest, highest-leverage)
Stop relying on the handshake race. The parent page already has `fbclid` in its own URL. Forward it
(and `_fbp`/`_fbc`) straight into the iframe `src` in `CORRECTED_FULL_SECTION.liquid`, and have the
configurator read it on load:

1. In the liquid section, build the iframe URL with the click context as query params, e.g.
   append `fbclid` (from `window.location.search`) and the `_fbp`/`_fbc` cookies to the
   `craftons-curves-calculator.vercel.app` src before/at render. (Do it in the inline script by
   setting `iframe.src` with the params, since Liquid cannot read the visitor's cookies/fbclid.)
2. In `meta-tracking.ts`, read `fbclid`/`fbp`/`fbc` from the iframe's own `window.location.search`
   first, build `fbc` from `fbclid` per Meta's format (`fb.1.<ts>.<fbclid>`) if needed, and use that
   immediately. Keep the postMessage handshake as a fallback, but do not block on it.
3. Ensure `trackAddToCart` does not fire the CAPI send until `fbc` is known (queue it briefly), so
   the click ID is never lost to a race.

Secondary: confirm `window.fbq` availability given the Web Pixels sandbox. If it is not reliably
present, treat CAPI as the primary path (already built) and make sure it always carries `fbc`.

## Verify (do this first, and again after the fix)
- Meta Events Manager > Data Sources > pixel 677437638374055 > AddToCart: check match quality and
  the share of events carrying `fbc`. Most AddToCart events having no `fbc` confirms the diagnosis.
- Or set `META_TEST_EVENT_CODE` in Vercel temporarily, open the product page with `?fbclid=TEST123`,
  add a part, and watch Test Events for whether `fbc` is present. Remove the code after.

## Impact once fixed
Ad-attributed AddToCart should jump from ~2 toward the true number, the ads become measurable and
optimisable (potentially switch optimisation to AddToCart once attributed volume supports it), and
we stop the risk of killing ads that are actually working.

## Note
This is the same repo where the "upload your plan, detect the curve, price it" lead-magnet MVP
should be built (radius-online is served from here via the iframe). Fixing attribution first makes
that tool measurable from day one.
