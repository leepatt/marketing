# Architrave page — conversion audit (2026-07-10)

**Page:** `/products/curved-architraves` (Craftons Architrave Builder). **Why:** ad clicks land and
**view** the product (20 view-item in 14d) but **0 add-to-cart / 0 checkout / 0 lead** (1 form-start).
Qualified traffic is arriving and bouncing at the page. This is the #1 architrave conversion lever.

_Verified from Shopify Admin (product data) + Google Ads funnel + Shopify funnel. The live configurator
interaction couldn't be screenshotted (site bot-protection reset the headless browser), so items marked
(inferred) are from the funnel data + the Radius Pro page pattern — confirm on the live page._

## 🔴 Fix first (biggest lift)

1. **Only ONE product image — no gallery.** *(verified: media = 1 image, alt empty)*
   A builder pricing a ~$1–2.5k custom architrave for a specific job needs to SEE it. One image kills
   confidence in a new, visual, high-consideration product.
   → **Add 6–10 images:** finished arched doorways, curved windows, circular/niche features, a close-up
   of the profile + MR-MDF finish, an install shot, the 3D preview, the range of shapes. *This is exactly
   where Tia's "Built with Craftons" finished-job shots plug in.*

2. **The visible price is "$1.00" (placeholder).** *(verified: variant price $1.00)*
   Real price comes from the configurator, but a $1 price reading anywhere looks broken/untrustworthy.
   → Ensure the **configurator's instant price** is what shows; hide the $1 placeholder; frame as
   "get your instant price" / "from $X".

3. **Thin content — no trust or proof.** *(verified: short description, no reviews metafield)*
   Good value prop ("configured online, delivered ready to install, no hand shaping") — but nothing else.
   → Add a trust band + sections: **Australian made · dispatched in 3 days · MR MDF spec**; a simple
   **How it works** (design → instant price → order → install); an **FAQ** (freight, finish/painting,
   max sizes, lead time); **reviews/testimonials** as they come in.

## 🟠 Then

4. **Make instant-buy the primary path.** *(inferred from funnel: 1 form-start, 0 submit, 0 add-to-cart)*
   If the main action is "request a quote / send message" rather than "get instant price → add to cart,"
   that's friction — and the data shows people start but don't finish.
   → Primary CTA = **design → instant price → add to cart / checkout**; keep "or request a quote"
   secondary; minimise form fields.

5. **Confirm it's not rendering "sold out."** *(verified: totalInventory 0 / made-to-order)*
   Ensure "continue selling when out of stock" is on so a made-to-order product never blocks checkout.

6. **Reassurance near the CTA** — dispatch time, Australian made, secure checkout, samples option.

## Priority order
1. Images/gallery (1 → 6–10 finished arches) · 2. Kill the $1 price / clear instant price ·
3. Trust content (AU made, 3-day dispatch, how-it-works, FAQ, reviews) · 4. Instant-buy as primary, less
form friction · 5. Confirm not sold-out.

## Ownership
Website/configurator job (Shopify theme + the configurator app). Claude can produce the **shot list for
Tia**, the **trust/how-it-works/FAQ copy**, and the **image alt text** — the dev wires them in. After the
images + trust land, **retarget the ~20 who already viewed** the product (warm, live arch jobs).


## 2026-07-10 (UPDATE — after Lee's mobile test + curl of the live page structure)
Corrections to the initial audit (that was based on the product's Shopify *media* field; the page renders
more via the theme):
- **There ARE 4 images** (carousel: finished arches + an install shot `curved_architrave_install_1.png`) +
  copy. My "1 image" was the Admin media count, not what the page shows. Alt text is empty (minor SEO miss).
- **Add-to-cart DOES work** — the builder posts "ADD TO CART requests from calculator iframe". So it's an
  instant-price → add-to-cart flow, not quote-only. (Corrects earlier inferred #4.)
- Trust bits exist: **"Apply for Trade Account"**, and a "Need a Solution Beyond the Standard App? → Send
  message" contact section. "You may also like" related products at the bottom.

### The REAL problem (Lee's finding, mechanism confirmed): the builder is an IFRAME, front-and-centre
The architrave builder is an **iframe-embedded calculator** (page is full of `IFRAME_HEIGHT_CHANGE` /
`IFRAME_VIEWPORT_INFO` / `IFRAME_MODAL_OPEN` postMessage plumbing). On mobile an inline iframe is the classic
cause of exactly what Lee saw: it takes the full width/height, scrolls internally (fighting the page), resizes
awkwardly, and **dominates the first screen** — so the 4 images + copy (the desire/trust) get buried below it.
A visitor from an ad lands on a *tool that demands work* before they've been given a reason to want the product.
**Effort before desire/trust = bounce.** Matches the funnel (20 view-item, 1 form-start, 0 finish).

### Fix (mostly a re-order + use the modal that already exists)
1. **On mobile, don't embed the builder inline as the hero.** Lead with a **hero image** (best finished arch)
   + headline + one-line value prop.
2. **Put the builder behind a big "Design your arch → get instant price" button that opens it as a
   full-screen modal** — the page already supports `IFRAME_MODAL_OPEN`, so the capability exists. Keeps the
   landing focused on desire/trust; tool is one tap away.
3. **Surface the images higher** (gallery of finished arches above/near the hero, not buried under the iframe).
4. **Add the "How it works" strip** (design → instant price → CNC-cut → delivered 3 days) between hero and builder.
5. **Test the iframe's mobile height/scroll** — the height-syncing can leave dead space or cut content.
6. Fix empty image **alt text**.
This is largely a theme/section re-order + a modal trigger — achievable without new tooling. The AI in-situ
images + how-it-works from the 2026-07-10 discussion slot straight into #1/#3/#4.
