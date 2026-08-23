# C1 — Lead capture spec

_Written 2026-08-23. Chosen by Lee from the options list. This is the design and the argument;
the build is a separate piece of work that needs Shopify theme access._

---

## The problem, stated precisely

Across all paid prospecting on both channels, Craftons has bought roughly **15,000+ cold visits and
captured almost none of them.** They arrive, price a job, and leave with nothing owed to us.

The Meta numbers make the shape obvious:

| | v2 TOF |
|---|---:|
| Landing page views | 1,116 |
| Add to cart | 18 |
| Checkout | 1 |
| Orders | 0 |

**Eighteen people configured a product, saw a price, and left.** We do not know who any of them are.

## Why they leave — and why that is normal, not a failure

Radius Pro buyers are **pricing a job they have not won yet.** A builder quoting a curved wall needs
the plate cost to finish their own quote. They will order when the job is signed — weeks later, or
never, depending on whether they win it.

The order data says exactly this:

| Order | First visit | Ordered | Gap |
|---|---|---|---|
| `#1280` $362 | Meta TOF (Jul) | 2026-08-10 | **~3 weeks** |
| `#1294` $407 | 2026-08-14 Google | 2026-08-17 | 3 days |
| `#1293` **$2,736** | 2026-08-11 Google | 2026-08-17 | **6 days — closed by an email** |

**`#1293` is the proof.** First visit Google organic on 08-11. Ordered six days later, and the last
click was `utm_source=shopify_email`, campaign *"Welcome to the Craftons Trade Program – Your
Exclusive Discount Awaits"*. **An email brought back a customer who had already left, and it was worth
$2,736.**

So the mechanism already works. It is just almost never armed — the web form produces about
**2 submissions a month** (Google's `Craftons (web) form_submit`: 2 conversions in 30 days).

## The design decision

**Do not build a generic "10% off, join our list" popup.** It interrupts a builder mid-calculation,
it is the wrong offer (they want the number, not a discount), and it trains people to close modals.

**Capture the thing they already want: the quote.**

> ### "Email me this quote"
>
> A button beside the configurator price. One field: work email. It sends a clean PDF/HTML summary —
> radius, segments, quantity, price, lead time — that the builder can paste straight into their own
> quote to the client.

Why this is the right shape:

- **It is a favour, not a toll.** They came to get a number. We help them keep it.
- **It fires at maximum intent** — after they have configured a real job, not on page load.
- **It qualifies automatically.** Someone who configures a 6-metre radius in 17mm formply and asks for
  the quote is a live job, not a browser.
- **The follow-up writes itself** — "still pricing that job?" beats any newsletter.
- **It captures the exact people we are currently losing:** the 18 who added to cart and the 132 who
  clicked the Google Radius Pro ads.

## What to build

1. **Capture point** — `/products/radius-online` and the configurator at `builder.craftons.com.au`,
   beside the calculated price. Secondary placement on `/products/craftons-formwork-builder-…` and
   `/products/curved-architraves`, which convert better than Radius Pro.
2. **Field** — work email only. No name, no phone. Every extra field costs submissions.
3. **Payload** — the saved configuration: radius, segment count, material, thickness, qty, price,
   lead time, and a link that reopens the configurator with those values.
4. **Destination** — Shopify customer record, tagged `quote-saved` + the product, so it can be
   segmented. Reuse the existing Craftons Trade Program sender rather than adding a tool.
5. **Follow-up** — a 3-email sequence, not a newsletter:
   - **T+0** the quote itself. No selling.
   - **T+3 days** "anything you want changed?" — offer to check the radius/segment split.
   - **T+14 days** "did the job go ahead?" — the only one with a CTA to order.
6. **Consent** — AU, so no GDPR-style gate, but a plain opt-in line. Note that Shopify →
   Settings → Customer privacy can suppress data sharing if a consent banner is enabled for AU.

## What it is worth

Cheap arithmetic, deliberately conservative. Of the **~1,100 Meta landing page views + 132 Google
Radius Pro clicks** in a month, suppose **8%** save a quote → **~99 addresses/month**. At a **5%**
eventual order rate and the measured **$871 Radius Pro AOV** → **~4 orders, ~$3,500/month** from
traffic already paid for.

That does not need a single extra dollar of ad spend. It is the difference between renting traffic
and keeping it.

**It also changes what the ad channels are for.** Right now every prospecting dollar is judged on
same-session purchase, which is the one thing this buyer never does. With capture in place, TOF can
be judged on cost-per-captured-quote — a metric it might actually be able to win.

## Honest caveats

- **This does not rescue Meta prospecting on its own.** Meta cold traffic produced 18 add-to-carts
  from 1,116 visits; even perfect capture on that volume is a handful of addresses. Capture is worth
  most on **Google and organic**, where intent is higher.
- **It needs Shopify theme access and configurator work** — this is the days-long item on the list,
  not an afternoon.
- **The 8% / 5% figures above are assumptions**, not measurements. They are there to size the prize,
  and the first month of real data should replace them.

## Status

**Spec only. Nothing built.** Next step is Lee confirming the "email me this quote" shape over a
discount popup, and pointing at who can touch the theme and the configurator.
