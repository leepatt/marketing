# What went wrong with the Meta ads — and how we stop it happening again

_Written 2026-08-02 for Lee. Plain language, no marketing jargon._
_Companion document: **`ADS-PREFLIGHT-CHECKLIST.md`** — the checklist that must be completed before
any future ad spends real money._

---

## The short version

Between 22 July and 2 August we spent **$1,711** on Facebook and Instagram ads.

They sent **14,427 people** to the Craftons website. Those people produced **2 orders worth $398**.

Over the same period, total sales went **down**, not up — from an average of $1,795/day before the
ads to $593/day while they ran.

The ads didn't just fail. They also damaged the one campaign that *was* making money.

**This was my failure, not bad luck.** Three specific mistakes caused it, all of them preventable,
all of them checkable in advance. This document explains them in plain terms and turns each one into
a rule.

---

## First — the words you need

You don't need to be a marketer to follow this, but six terms come up constantly. Here they are in
plain English.

| Term | What it actually means |
|---|---|
| **Pixel** | A small piece of tracking code on your website. It tells Facebook "someone just looked at a product" or "someone just bought something." Without it working, Facebook is blind — it has no idea if its ads are producing sales. |
| **Objective** | The goal you tell Facebook to chase. You pick this when you build the campaign. Options include "Traffic" (get people to click) and "Sales" (get people to buy). Facebook then optimises hard for whatever you picked. |
| **Retargeting** | Advertising to people who have already visited your website. Much more effective than advertising to strangers, because they already know who you are. Facebook builds this list automatically from website visitors. |
| **CTR** (click-through rate) | Of the people who saw the ad, what percentage clicked. Sounds like a quality measure. It isn't — see "the trap" below. |
| **CPC** (cost per click) | What you paid for each click. Cheap sounds good. It usually isn't. |
| **Conversion** | Someone doing the thing you actually want — buying, or submitting an enquiry. This is the only number that pays wages. |

---

## The damage, in numbers

| | Before the ads (4–21 Jul) | While the ads ran (22 Jul – 2 Aug) |
|---|---|---|
| Orders per day | 1.44 | 0.83 |
| Sales per day | $1,795 | $593 |
| Website visits per day | 86 | 1,255 |
| People adding to cart per day | 2.56 | 2.33 |

Read the last two rows together, because that's the whole story:

> **Visitors went up roughly 15 times over. The number of people putting something in a basket did
> not move at all.** It actually went slightly down.

15,058 people visited in 12 days and produced 28 cart additions. Before the ads, 1,541 people
visited and produced 46.

The visitors were worthless. Not "low quality" — worthless. They behaved as if nobody had arrived.

> **An honest caveat:** your order volume is low and lumpy — a single order can swing $4,000–8,000,
> so the *revenue* drop is partly random noise. The visits-versus-baskets collapse is **not** noise.
> That's measured across 15,000 people. That part is solid.

---

## What went wrong — four failures

### Failure 1 — We told Facebook to buy the wrong thing

When you build a Facebook campaign you choose a goal. We chose **"Traffic."** That tells Facebook:
*get me clicks, as cheaply as you can.*

We wanted sales. Facebook was never asked for sales, so it never went looking for buyers. It went
looking for the cheapest clicks on the internet — and it found them.

> **The analogy:** it's like paying a promoter per person who walks through the door, instead of per
> person who buys a drink. You will get a packed room and an empty till. The promoter did their job
> perfectly. You asked the wrong question.

**Where the money went:** 72% of the budget ($919) went to **Reels** — the vertical swipe-up videos.
People scrolling Reels tap by accident constantly. We paid **6.5 cents a click** and got a 10%
click rate, both of which look spectacular on a dashboard.

They were accidental taps. The proof: of 7,909 people who "landed" on the site from Facebook Reels,
only **428 stayed long enough to look at a single product.** That's 5%. The other 95% swiped away
before the page finished loading.

**Rule that comes out of this:** never run a "Traffic" campaign when the goal is sales. And never
run Reels for a considered trade purchase — Feed placements only until proven otherwise.

---

### Failure 2 — The measuring equipment wasn't plugged in

The pixel — the tracking code — was **not reporting to this campaign for the first 8 days.**

Facebook recorded zero product views and zero cart additions from 22–29 July. Not "low." Zero. Then
on 30 July it suddenly started working.

**$985 — 77% of the entire campaign budget — was spent during the blind period.**

Two things this caused:

1. We couldn't see it was failing.
2. **Facebook couldn't see it either.** Facebook improves an ad by watching what works. With no
   sales data coming back, it had nothing to learn from — so it just kept buying cheap clicks,
   getting better and better at the wrong thing.

> **The analogy:** driving across the country with the fuel gauge disconnected. It's not that the
> gauge read low and you ignored it. It read nothing, and you assumed that meant fine.

**Rule that comes out of this:** no campaign spends a dollar until the tracking is *proven* working
— verified with a real event, not assumed because the code is installed.

---

### Failure 3 — Nobody checked the till

This is the one I'm most responsible for.

Facebook's dashboard looked **excellent** the entire time. Massive click numbers, extremely cheap
clicks, thousands of visits, budget pacing perfectly.

Every one of those is a **vanity metric** — a number that goes up without money arriving.

Your Shopify sales data was one click away the entire time. It showed cart additions completely flat
from **day two**. I never looked. I reported on Facebook's numbers, and Facebook's numbers were
measuring the wrong thing beautifully.

When sales showed as zero, I read it as *"not enough data yet"* rather than *"there are no sales."*
That was the moment to stop. It was day two.

> **The analogy:** the promoter shows you a photo of the queue outside. You need to look at the till.

**Rule that comes out of this:** Facebook's numbers are never the verdict. Shopify is the verdict.
Every single report cross-checks Shopify, or it doesn't get made.

---

### Failure 4 — The bad campaign broke the good one

This is the expensive part, and the least obvious.

You had a **retargeting** campaign — ads shown to people who'd already visited the site. It was
quietly excellent: **9 sales in two weeks on about $15/day.**

It works by advertising to a list Facebook builds automatically of "everyone who visited your website
in the last 30 / 60 / 180 days."

Then we poured **14,400 accidental Reels tappers into that list.**

The list is now roughly **85% people who never meant to visit at all.** Result:

| | Sales | Spend |
|---|---|---|
| Two weeks before | 9 | ~$15/day |
| The eleven days after | 1 | up to $65/day |

And the budget was increased **four-fold** at exactly the moment the list was at its most polluted.

> **The analogy:** your best customer call-list just got padded with 14,000 wrong numbers — and then
> you hired more people to work through it.

**This is why the damage outlasts the campaign.** The bad ads are off now, but the polluted list
clears slowly: the 30-day list recovers around **1 September**; the 180-day list not until
**late January 2027**.

**Rule that comes out of this:** cold traffic and retargeting lists must be kept apart. Untested
traffic should never feed the audience that's already producing sales.

---

## Why I told you it was going fine

Because I was looking at clicks and cost-per-click, and both looked exceptional. I reported the
dashboard rather than the bank balance.

The specific error is worth naming, because it's the one that generalises:

**A cheap click and a high click-rate are not good news on a cold audience. They are usually
warning signs.** Real buyers are expensive and click less. When clicks get suspiciously cheap, it
almost always means you've found people who aren't paying attention.

I had it exactly backwards — I read the warning signs as success signals and told you so.

I also, in the first version of my audit, guessed that an outside agency had built the campaign
based on a word in its name, and wrote that up as if it were a finding. That was wrong and it
pointed blame away from me. It's corrected in the record.

---

## The seven rules

These are now standing rules for all paid advertising — Google as well as Meta.

1. **Shopify is the scoreboard. Facebook is not.** No performance claim gets made without
   cross-checking actual orders.
2. **No spend before tracking is proven.** Verified with a real event, not assumed.
3. **Match the goal to the outcome.** If we want sales, the objective is Sales. Never Traffic.
4. **Cheap clicks are a red flag, not a win.** Investigate anything under ~20c or over ~3% CTR on a
   cold audience.
5. **Small first, then scale.** Start at $10–20/day. Prove real orders. Only then increase — and
   never increase a campaign that hasn't produced a sale.
6. **Agree the kill criteria before launch, in writing.** Decide in advance what failure looks like
   and on what date, so the decision isn't made emotionally later.
7. **Protect the retargeting list.** Never let untested cold traffic feed the audience that already
   converts.

---

## What's already been done

| Action | Result |
|---|---|
| Paused the failing campaign | $70/day → $0 |
| Cut retargeting back to its working level | $60/day → $15/day |
| Switched off a weak ad (1.6x return) | was eating half the budget |
| Switched on your best ad, which was sitting paused | had only ever received $11.62 |
| Moved the winning ads to purchase-focused targeting | now optimising for sales, not clicks |
| **Total daily spend** | **~$130/day → $15/day** |

Full technical record: `campaigns/meta/meta-change-log.md` · Full data: `campaigns/meta/meta-ads-audit-2026-08-02.md`

---

## How you can check any of this yourself

You should not have to take my word for it. In Meta Ads Manager:

1. Set the date range to **22 July – 2 August**
2. Add the columns **Purchases** and **Amount Spent**
3. Look at the campaign `RadiusPro | TOF | Ardreagh | Jul26`

It should read **$1,277 spent, 0 purchases.** If it doesn't match, tell me.

Then in Shopify: **Analytics → Sessions → group by referrer.** Facebook + Instagram should show
roughly **14,400 sessions and 2 orders** over 30 days.

**The habit worth keeping permanently:** when I tell you an ad is working, ask me one question —
*"how many orders in Shopify?"* If I answer with clicks, engagement, reach or impressions, the
answer is none.
