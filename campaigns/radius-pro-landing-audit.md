# Radius Pro landing page — conversion audit

_Audited 2026-07-27 · Page: `craftons.com.au/products/radius-online` · Data: Shopify Analytics, last 90 days_

---

## The headline finding

**The page is not the problem. The traffic is.**

Splitting the 9,162 sessions by source changes the entire diagnosis:

| Source | Sessions | Add to cart | Orders | CVR |
|---|---:|---:|---:|---:|
| Facebook | 7,359 | 2 | **0** | 0.00% |
| Instagram | 1,502 | 0 | **0** | 0.00% |
| Direct / unattributed | 193 | 15 | **9** | **4.66%** |
| Google | 114 | 0 | 0 | 0.00% |
| Bing / ChatGPT | 4 | 0 | 0 | 0.00% |

**8,861 sessions from Meta produced 2 add-to-carts and zero orders.**
**193 direct sessions produced 9 orders — a 4.66% conversion rate.**

A page that converts direct traffic at 4.66% on a ~$796 average order is not a broken page. That is a
genuinely good number for custom-manufactured product. The Meta traffic is the anomaly, and it is
dragging the blended rate to near zero.

For context, Radius Pro is the **best-selling product in the store**: 82 orders and $65,290 gross in
90 days — roughly two-thirds of all store revenue. It converts. Just not for anyone arriving from an ad.

---

## Why 8,861 social sessions produced zero orders

A 0.02% add-to-cart rate is not "wrong audience." Wrong-fit humans still add to cart occasionally.
This pattern — huge volume, near-zero engagement, zero purchases — points at one of three things,
in order of likelihood:

1. **Accidental / low-quality placements.** Audience Network and Reels auto-placements generate
   mis-taps that register as sessions. This is the classic signature.
2. **Bot or click-farm traffic.** Worth ruling out.
3. **Audience mismatch** — served to consumers scrolling, not builders sourcing.

The July trend supports this. Sessions tripled from 3,455 (June) to 11,225 (July), while store-wide
add-to-carts *fell* from 81 to 73. Tripling traffic produced fewer carts. That is the fingerprint of
volume bought at the expense of intent.

**Device split reinforces it:** store-wide, desktop converts at 1.44% and mobile at 0.31% — 4.6× worse
— and mobile is 75% of traffic. On this page specifically, 8,972 of 9,162 sessions were mobile (98%),
which is abnormal for a B2B trade product and consistent with a Meta-driven feed.

### Do this first — before touching the page

These are worth more than every page tweak below combined:

- **Turn off Audience Network and Advantage+ placements.** Restrict to Facebook and Instagram feeds
  only. Re-check add-to-cart rate after 7 days.
- **Check the placement breakdown in Ads Manager** (Placement × Landing page views × ATC). If one
  placement is eating spend with no carts, that alone is the answer.
- **Compare Meta's reported landing page views vs Shopify's 9,162 sessions.** A large gap means clicks
  that never actually loaded the page — mis-taps.
- **Watch 10 mobile session recordings in Microsoft Clarity.** Clarity is already installed and running
  on the site. Filter to mobile + Facebook referrer. Ten recordings will tell you in fifteen minutes
  whether these are real people who bounce, or taps that never engage. This is the single fastest way
  to confirm the diagnosis.
- **Add UTM tags** to all Meta ads so this analysis stops relying on referrer sniffing.

---

## Page fixes — ranked

The page still has real, fixable weaknesses. They matter most for *cold* traffic, which is exactly what
the ads are sending. Ranked by expected impact.

### 1. There is no price, anywhere — and no hint of one

Nothing on the page indicates whether a curved formply set costs $50 or $5,000. The only prices in the
HTML belong to the "You may also like" products. A cold visitor has to load a CNC configurator and
complete a multi-step set-out before learning if this is even in their budget.

**Fix:** add a price anchor above the configurator.

> Most jobs land between $200 and $900. Enter your set-out below for an exact price — no quote, no wait.

This single line qualifies out tyre-kickers and reassures serious buyers before they invest effort.

### 2. The configurator is the first thing on the page — before any context

The section order inside `<main>` is:

```
1. curves_calculator   ← the 750px iframe, first thing visitors see
2. rich_text           ← "Craftons Radius Pro: Custom Radius & Curves" + the pitch
3. text_with_icons     ← the four benefit cards
4. media_with_text     ← "Cutting Curves Onsite Is Hard"
5. contact             ← enquiry form
6. related-products
```

Warm traffic that already knows what Radius Pro is loves this — tool first, no scrolling. That is why
direct converts at 4.66%. Cold traffic from a Meta ad lands on an unexplained engineering tool.

**Fix:** insert a compact hero *above* the iframe — headline, one line of proof, the price anchor.
Keep it short so the tool stays visible. Suggested, on-brand:

> **Curves, cut to your set-out. Delivered in 3 days.**
> Enter your radius, chord and material. We CNC it, label every part, and ship it install-ready.
> Most jobs $200–$900.

Do **not** push the tool below the fold — that would hurt the direct traffic that currently converts.
A ~180px hero band is the right trade.

### 3. The page has no `<h1>`

Zero `<h1>` tags in the entire document. The product name sits in a rich-text block with no heading
semantics. This costs organic ranking (Google traffic to this page: 114 sessions, 0 orders) and removes
the strongest signal of what the page is.

**Fix:** wrap the hero headline in an `<h1>`. One line of Liquid.

### 4. Mobile is 98% of this page's traffic and the tool is heavy

The configurator is a separate Next.js app (`craftons-curves-calculator.vercel.app`) embedded in an
iframe. Measured:

- **1.68 MB** of uncompressed JS/CSS across 16 files — one chunk alone is 847 KB
- **1.19s** time-to-first-byte before any of that starts downloading
- Renders `Loading Curves configuration...` until the bundle boots
- `loading="lazy"` on an **above-the-fold** iframe — the browser deprioritises the one element that
  makes money
- Fixed `height: 750px` until the app posts its real height back

Stacked on top of the Shopify theme, Facebook pixel, Clarity, GA4, Avada FAQ and Shopify Forms, a phone
on site data is waiting a long time on a blank grey box.

**Fixes, cheapest first:**
- **Remove `loading="lazy"`** from the iframe and add `fetchpriority="high"`. One-word change.
- **Add `<link rel="preconnect" href="https://craftons-curves-calculator.vercel.app">`** to the theme
  head so DNS/TLS is warm before the iframe requests it.
- **Replace the grey box with a skeleton** that shows the headline and price anchor, so the wait has
  content in it.
- **Code-split the 847 KB chunk** in the Next.js app so first paint doesn't wait on the whole bundle.

### 5. Pinch-zoom is disabled

The theme sets:

```html
<meta name="viewport" content="... minimum-scale=1.0, maximum-scale=1.0">
```

`maximum-scale=1.0` blocks pinch-zoom. On a page whose core interaction is reading and entering
millimetre dimensions on a technical diagram, on a phone, this is actively hostile — and it is a
WCAG accessibility failure.

**Fix:** delete `maximum-scale=1.0`. Theme-wide one-liner, benefits every page.

### 6. Zero social proof

No testimonials, no ratings, no project photos with attribution, no logos, no "X curves cut this year."
For a $796 custom-manufacture purchase from a brand most visitors have never heard of, this is the
biggest missing trust lever after price.

**Fix:** a single row under the configurator — three named jobs with photos, or a counter:

> Over 2,000 curves cut for Melbourne builders. Set-out checked by a human before every cut.

Use real numbers only.

### 7. The unanswered questions aren't answered

Nothing on the page states: cutting tolerance, available materials and thicknesses, max radius, delivery
cost, delivery area, what happens if the set-out is wrong, or whether anyone checks the file before
cutting. The Avada FAQ app is loaded on the page but no FAQ content renders.

**Fix:** populate the FAQ block. Six questions, answered plainly:
- What tolerance do you cut to?
- Which materials and thicknesses?
- What's the biggest radius you can do?
- What does delivery cost, and where do you deliver?
- What if my set-out is wrong?
- Does anyone check my file before it's cut?

### 8. Smaller items

- **All hero images have empty `alt=""`** — four images, no alt text. SEO and accessibility.
- **Rendering artifact:** a stray `*">` renders as visible text in the "You may also like" section.
  Broken Liquid in the related-products block.
- **Four competing Radius Pro pages** — `radius-online` (9,162 sessions), `craftons-radius-pro-formply`
  (627), `-plywood` (524), `-mdf` (380), plus `craftons-radius-pro-custom-radius-curves-cut-to-size`
  (228). They split ranking signal and make reporting muddy. Note that `-formply` converts:
  420 desktop sessions → 3 orders. Worth consolidating deliberately, with redirects.
- **Cart line item:** the variant is priced at $1.00 with quantity used to carry the real price, so the
  cart shows a large quantity against a $1.00 unit. Direct traffic converts through it at 4.66%, so it
  isn't fatal — but it looks odd at the exact moment trust matters most. Worth a line-item property
  that displays the real description.

---

## What I'd do, in order

1. **Fix the ads.** Kill Audience Network / Advantage+ placements, check the placement breakdown, add
   UTMs. This is where the money is.
2. **Watch 10 mobile Clarity recordings** filtered to Facebook referrer. Fifteen minutes, confirms
   everything above.
3. **Three one-line code fixes:** remove `loading="lazy"`, remove `maximum-scale=1.0`, add `preconnect`.
4. **Add the hero band** above the configurator with `<h1>` + price anchor.
5. **Populate the FAQ** and add social proof.
6. Then consolidate the duplicate Radius Pro pages.

Steps 3–5 are maybe half a day of theme work. Step 1 is a settings change that could plausibly recover
most of the wasted spend.

---

## One caveat on method

I could not visually render the page — browser automation is blocked by this environment's egress proxy.
Everything above about page **structure, weight, markup and configuration** is read directly from the
served HTML and the app's real asset payloads, and all traffic figures are pulled live from Shopify
Analytics. What I have **not** visually confirmed is how the configurator itself lays out inside the
iframe on a phone. Clarity recordings will close that gap immediately.
