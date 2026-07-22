# Radius Pro TOF. LAUNCHED (record)

**Went live: 2026-07-22.** First native TOF batch off the real Ardreagh job. Built via the Meta
Marketing API. This file is the record of exactly what is running.

## Campaign
- **Name:** `RadiusPro | TOF | Ardreagh | Jul26`
- **Campaign ID:** `120247183657950186`
- **Ad account:** `act_1650412872259063` (Craftons, AUD, Australia/Melbourne)
- **Objective:** Traffic (OUTCOME_TRAFFIC)
- **Budget:** $100/day AUD, campaign budget (CBO), lowest cost
- **Status:** ACTIVE

## Ad set
- **Name:** `TOF | Broad AU | LPV` · **ID:** `120247183658270186`
- **Optimisation:** Landing Page Views · billing on impressions
- **Audience:** Australia, age 25+, broad (Advantage+ audience on, no interests). The copy targets.
- **Placements:** automatic (Advantage+ placements)

## Ads (carousel, 3 slides, 1:1, real Ardreagh photos)
- **AD1 Concreters** · ad ID `120247183658860186` · utm_content `ad1_concreters`
- **AD2 Landscapers** · ad ID `120247183659780186` · utm_content `ad2_landscapers`
- **AD2b Landscapers (finished-first)** · ad ID `120247190951340186` · added later on launch day
  (22:20 AEST): same landscaper ad with the slide order reversed, finished courtyard first. Tests
  payoff-first vs process-first inside the same CBO.
- Slides (AD1/AD2): formwork (dramatic), formwork (wide), finished courtyard. AD2b runs the reverse.
- **Card headlines (in order):** "Curves cut to the exact radius." / "Designed online. Machined.
  Delivered." / "Every curve, exactly to plan."
- **CTA:** Learn more. **Destination:** `craftons.com.au/products/radius-online` + per-ad UTMs.
- Copy: the locked long-form concreter + landscaper captions (see `AD-CONCEPTS.md`). Identity clone,
  one word swapped (hack 2).

## Verified pre-flight
- Pixel "Craftons Web" (`677437638374055`) firing. GREEN.
- Landing-page scent OK: page title "Custom Radius & Curves, Cut to Size" is congruent with the ad.
- No music auto-add (declined the Opportunity Score prompt: keeps it native, we do not control the track).

## Day-0 read (pulled 2026-07-23 ~05:30 AEST, spend $80.79 total)
| Ad | Spend | Impr | Link CTR | LPVs | Cost/LPV |
|---|---|---|---|---|---|
| AD1 Concreters | $13.21 | 1,558 | 5.5% | 98 | $0.135 |
| AD2 Landscapers | $66.85 | 8,148 | 9.3% | 709 | $0.094 |
| AD2b Landscapers finished-first | $0.73 | 103 | 2.9% | 3 | $0.243 |

- Meta is pouring spend into AD2 (83% of budget). AD2b only entered the auction at 22:20 so its
  numbers mean nothing yet. Per doctrine: day 1 to 2 is gut-check only, nothing touched, learning
  phase left alone. Numbers are healthy (all well under the $1/LPV worry line).
- No orders attributable yet (last Shopify order predates launch). Judge on net cash at the day-3 read.

## Tracking status (2026-07-23 morning)
- **AddToCart and InitiateCheckout hit the pixel for the first time**: 9 ATC + 3 IC, all in the
  19:00 UTC hour (about 5am AEST Jul 23), none before, no Purchase after. Pattern matches the go-live
  test walk-through from `TRACKING-VERIFICATION.md` (or a single real abandoner). Server events are
  flowing (4,259 SERVER vs 1,976 BROWSER in the window), but Shopify Maximum sharing also sends
  server events, so this is strong evidence, not formal confirmation. **Waiting on the calculator
  session's REPORT BACK** (dedup check, one-Purchase check, test code removed) before trusting it.
- **Retargeting audience created (hack 7 seed):** `Radius Pro | Added part, no purchase | 30d`,
  audience ID `120247198803570186` (pixel AddToCart last 30d excluding Purchase). It accumulates from
  now; no ads point at it yet.
- **Still optimising Landing Page Views.** Do NOT switch to AddToCart until the walk-through is
  confirmed and volume holds around 15 to 25 per week of real (non-test) events.

## Watch / next
- Day 1 to 2: gut-check CTR + cost per landing page view. If clearly failing, pause. Otherwise do not touch.
- 3 to 4 days: read concreter vs landscaper. Scale the winner (raise campaign budget <=30% every 2 to 3
  days), then clone the winner to Formworkers and to the AD4/AD5 job types once we have those photos.
- Judge on net cash, not ROAS % or Meta's Opportunity Score.
