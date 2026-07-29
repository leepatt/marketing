# Radius Pro TOF. LAUNCHED (record)

**Went live: 2026-07-22.** First native TOF batch off the real Ardreagh job. Built via the Meta
Marketing API. This file is the record of exactly what is running.

## Campaign
- **Name:** `RadiusPro | TOF | Ardreagh | Jul26`
- **Campaign ID:** `120247183657950186`
- **Ad account:** `act_1650412872259063` (Craftons, AUD, Australia/Melbourne)
- **Objective:** Traffic (OUTCOME_TRAFFIC)
- **Budget:** $130/day AUD, campaign budget (CBO), lowest cost. Launched at $100/day, raised to $130
  (+30%) on 2026-07-25 as the first scale step.
- **Status:** ACTIVE

## Ad set
- **Name:** `TOF | Broad AU | LPV` · **ID:** `120247183658270186`
- **Optimisation:** Landing Page Views · billing on impressions
- **Audience:** Australia, age 25+, broad (Advantage+ audience on, no interests). The copy targets.
- **Placements:** automatic (Advantage+ placements)

## Ads (carousel, 3 slides, 1:1, real Ardreagh photos)
- **AD1 Concreters** · ad ID `120247183658860186` · utm_content `ad1_concreters`
- **AD2 Landscapers** · ad ID `120247183659780186` · utm_content `ad2_landscapers`
- Slides: formwork (dramatic), formwork (wide), finished courtyard.
- **Card headlines (in order):** "Curves cut to the exact radius." / "Designed online. Machined.
  Delivered." / "Every curve, exactly to plan."
- **CTA:** Learn more. **Destination:** `craftons.com.au/products/radius-online` + per-ad UTMs.
- Copy: the locked long-form concreter + landscaper captions (see `AD-CONCEPTS.md`). Identity clone,
  one word swapped (hack 2).

## Added since launch
- **AD2b Landscapers (finished-first)** · ad ID `120247190951340186` · same Ardreagh photos as AD2 but
  led with the finished shot. **PAUSED** on 2026-07-25 (finished-first lost decisively to formwork-first).
- **Curved-wall-frame creative (Lawless customer photo)**, three identity clones (hack 2) on the same
  real curved-wall-frame shot, all ACTIVE. This is the curved-wall-plate ad that `PHOTO-BRIEF.md` AD4
  was waiting on, now that the photo arrived:
  - **AD4 Builders** · ad ID `120247222879340186`
  - **AD5 Chippies** · ad ID `120247222879990186`
  - **AD6 Carpenters** · ad ID `120247222880330186`

## Verified pre-flight
- Pixel "Craftons Web" (`677437638374055`) firing. GREEN.
- Landing-page scent OK: page title "Custom Radius & Curves, Cut to Size" is congruent with the ad.
- No music auto-add (declined the Opportunity Score prompt: keeps it native, we do not control the track).

## Watch / next
- Day 1 to 2: gut-check CTR + cost per landing page view. If clearly failing, pause. Otherwise do not touch.
- 3 to 4 days: read concreter vs landscaper. Scale the winner (raise campaign budget <=30% every 2 to 3
  days), then clone the winner to Formworkers and to the AD4/AD5 job types once we have those photos.
- Judge on net cash, not ROAS % or Meta's Opportunity Score.

## Retargeting (BOF) video A/B, live 2026-07-27

The boss-avatar config video went live in the existing BOF retargeting ad set to run head to head against
the incumbent video ad (hack 7: same warm pool, different angle. Do not kill the producer, test against it).

- **Campaign:** `120232888615730186` Retargeting Campaign - Bottom Of Funnel (OUTCOME_SALES)
- **Ad set:** `120232888615720186` "- Add To Cart", optimising OFFSITE_CONVERSIONS (Add To Cart).
  **Budget raised $15 to $30/day** on 2026-07-27.
- **New ad:** `120247285566810186` "Retargeting - Radius Pro boss video (highlights)", video
  `2576437746132450`, creative `1379110744170312`. CTA Shop Now to
  `products/radius-online` with `utm_content=boss_video_highlights`. Caption reworked to the first-person
  version on 2026-07-27 (creative `1729446611812943`, replacing `1379110744170312`, because the cold
  problem-story copy was the wrong temperature for a warm retarget pool). Preview:
  https://fb.me/37jXDrCtbEfoEi7
- **Competing against:** `120233970244410186` "Bottom Of Funnel - Ad 2" (the incumbent, 45 add-to-carts
  and $5,092 value over the last 30 days) and `120245221715860186` "Configurator Hero Ad D".
- **The creative:** 9:16 10s. Top panel is a real screen recording of the Radius Pro configurator
  (radius 1200, width 90, angle 90, qty 8, Add Part, scroll to the $367 order summary and Add to Cart).
  Bottom panel is the AI boss avatar on a high-end job speaking the approved first-person VO. Highlight
  captions in Aeonik Regular.
- **2026-07-28 CROP FIX (important, do not regress).** The single 9:16 video was being centre-cropped in
  the Instagram feed (IG feed caps at 4:5), cutting the top off the configurator and pushing the captions
  under the nav bar. Fixed by building placement-specific sizes and a placement-customised creative
  `1047936567593444` (asset_feed_spec with asset_customization_rules):
  - **4:5 `1080x1350`, video `1514548613329069`** to FB feed / video feeds / marketplace / search and IG
    stream / explore / search. Config sits full width at the top (1080x608), avatar below (1080x742),
    captions over his chest clear of the feed UI.
  - **9:16 `1080x1920`, video `1228564626028777`** to FB and IG stories and reels, with the captions
    raised (MarginV 470) out of the bottom UI band.
  - **Rule for any future video ad: never ship a lone 9:16 to feed placements.** Build the 4:5 for feed
    and the 9:16 for stories/reels, and keep captions inside the safe zone.
- **2026-07-28 layout v4 (current, approved).** A first attempt shrank the config into a card on green to
  give the avatar height. Lee rejected it. The approved layout keeps the **config full width and fully
  visible** (1080x608, nothing clipped, the $367 total and Add to Cart readable) and instead **zooms into
  the avatar and crops his lower body away** so his head and shoulders fill the lower box, with captions
  moved up over his chest. Live creative `1460862622515293`, videos 4:5 `2568143297034491` and 9:16
  `1031224343103271`. Preview https://fb.me/ylV2s9P1twL1A1h
  **Lesson: to give the presenter more presence, crop INTO the presenter. Do not shrink the product demo.**
- **2026-07-29 story (9:16) rebuild, current.** The 9:16 avatar was visibly STRETCHED: a landscape crop
  (1010x700) was force-fitted into a portrait box (1080x1312), a 75% vertical stretch. **Rule: crop and
  destination box must share the same aspect ratio, always scale uniformly.**
  The approved 9:16 layout is now: **real Craftons mobile site header** (Lee supplied the screenshot,
  1080x165, background sampled at `#1E3428`, so it matches the page users land on) | **config full width
  and uncropped** (1080x608) | **avatar filling everything to the bottom edge** (1080x1147, crop 678x720,
  uniform scale 1.593, no green base). Live creative `1049483434443954`, new 9:16 video
  `1569194157904324`. Preview https://fb.me/1UVV4m8eSsWVheH
  The **4:5 feed asset and the caption were deliberately left untouched** (feed video kept as-is).
  Note: Meta re-encodes on publish, so live video ids differ from the upload ids.
- **2026-07-29 story safe-zone fix (CURRENT LIVE).** In the real IG Story render the header collided with
  Instagram's own chrome: our header sat at y0-165 while IG's progress bar, profile circle, `craftons.au`
  handle and X button occupy roughly y0-129. Worst part was the handle landing beside our Craftons
  wordmark, reading as two brand marks jammed together. Fix: **100px of header-green padding above the
  header**, pushing the whole stack down (Meta advises keeping key elements out of the top ~250px in
  Stories). Also removed a light seam line: the top row of Lee's header screenshot is a lighter edge
  artifact `(56,77,68)` vs the true header green `(29,53,40)`, so that row is trimmed and the pad uses the
  header's own interior colour.
  Final story layout: **pad 100 + header 164 | config 608 (full width, uncropped) | avatar 1048**
  (crop 742x720, uniform scale 1.455). Captions raised above the Shop Now button.
  Live creative `2277520083017723`, 9:16 video `1024781750266335`. Preview https://fb.me/2g91ixv3qdTzje6
  **The 4:5 feed video and the caption were again left untouched.**
- **Watch:** this is an AI avatar, so the hack 4 native-trust question is live. If it underperforms the
  incumbent, test a real-person cut (Lee or an actual chippy on a phone) before dropping the format.
- **2026-07-27 decisions:** Ad 2 left running untouched (it is the producer, 11.68 ROAS over 30 days).
  Ad set budget raised $15 to $30/day. **"Configurator Hero Ad D" `120245221715860186` PAUSED** (4
  add-to-carts, 0.29 ROAS) so the bigger budget concentrates on Ad 2 and the new video and the A/B stays
  clean. Reassess after 3 days (a check-in is scheduled for about 2026-07-31): compare add-to-carts,
  value, cost per add-to-cart and ROAS. Judge on net cash, not CTR.

## 2026-07-30 MAJOR CHANGE: TOF switched to AddToCart optimisation, budget cut

**Why.** Shopify data settled the question Meta could not. Since TOF launched (Jul 22) sessions went from
about 85/day to about 1,700/day (12,604 of 13,280 sessions in 9 days are "social", so it is our ads), but
**sessions with cart additions did not increase at all** (1 to 8/day before, 0 to 5/day after) and site
conversion rate fell from 1 to 3.8% down to 0.0 to 0.2%. Revenue per business day went $3,423 to $1,285 and
orders per business day 2.2 to 1.17. The revenue fall is probably lumpiness (orders are few and large, one
job swings a week) and 6 business days is a small sample, so do NOT claim the ads caused it. But the flat
cart-adds cannot be explained away: about 12,500 extra visits for $1,003 produced no measurable lift.

**Diagnosis.** The ad set was optimising for **Landing Page Views**, so Meta was hunting the people
cheapest to make click, not people who buy. A 10% CTR alongside a 0.15% cart-add rate is the signature of
that (plus accidental in-app-browser taps). TOF lifetime: $1,002.89 spend, 12,563 LPV at $0.080, zero
attributed ATC or purchases. BOF lifetime by contrast: $2,726.67 spend, 216 ATC, 53 purchases, $44,122,
**16.2 ROAS**.

**Changes made (both reversible).**
1. **Ad set `120247183658270186` optimisation LANDING_PAGE_VIEWS to OFFSITE_CONVERSIONS / ADD_TO_CART**
   (promoted_object pixel `677437638374055`, custom_event_type ADD_TO_CART). Renamed to
   `TOF | Broad AU | AddToCart`. This was only possible now because the configurator tracking is live: the
   pixel is doing 18 to 25 AddToCarts a day, about 130 to 175/week, above Meta's ~50/week threshold.
   **Note: Meta accepted conversion optimisation on an OUTCOME_TRAFFIC campaign, so no rebuild was needed.**
2. **Campaign budget $170 to $70/day.** Traffic is proven, conversion is not, so stop funding the
   experiment at full price.
3. BOF left completely untouched at $30/day (Ad 2 + the boss video running, Ad D and Ad 1 paused). AD2b
   remains PAUSED (verified status=PAUSED; ads show IN_PROCESS only while Meta re-reviews the edit).

**Expect a re-learning period.** Changing the optimisation goal resets learning, so impressions and cost
per result will look worse for a few days before Meta finds add-to-cart-likely people. Judge this on
**add-to-carts and Shopify revenue**, not CTR or cost per landing page view. Re-read in about 4 to 7 days:
if cart additions per day rise above the pre-TOF baseline of 1 to 8, the switch worked.

## Performance log

### 2026-07-25 day-3 read (lifetime Jul 22 to 25, $331.66 spend, 4,003 landing page views, blended $0.083 per LPV, frequency ~1.05 across all ads so no fatigue)
- **Winner: the curved-wall-frame creative (Lawless), on the chippies and carpenters identity.** AD5
  Chippies $0.064 per LPV at 11.1% CTR (1,612 LPV, $103.25). AD6 Carpenters $0.064 per LPV at 9.6% CTR.
  About 35% cheaper per LPV than the Ardreagh formwork creative, and Meta is now putting ~98% of daily
  spend here. This is the original brief's number-one target (curved wall plates for builders/chippies).
- **Ardreagh formwork creative, second:** AD2 Landscapers $0.099 per LPV (8.4% CTR, 1,192 LPV), AD1
  Concreters $0.107 per LPV (9.4% CTR, 714 LPV). Landscaper marginally ahead of concreter on cost, both
  now clearly behind the wall-frame ads.
- **Finished-first vs formwork-first (landscaper):** formwork-first won decisively. AD2b finished-first
  $0.209 per LPV at 3.6% CTR on 552 impressions, now paused. Lead with the process shot, not the payoff.
- **Budget:** already raised to $130/day (+30%). Holding there. The next scale step waits on the
  AddToCart tracking go-live so we scale on net cash, not on cheap landing page views alone.
- **Next:** keep feeding the wall-frame winner; add a Formworkers one-word clone (hack 2) on the
  concreter formwork creative; still need the curved bench-seat photo (`PHOTO-BRIEF.md` AD5). The
  wall-plate photo (Lawless) has landed and is the current winner.

### 2026-07-27 weekend read + tracking and funnel audit
- **Weekend (Sat 25 + Sun 26):** $240 spend, 3,666 landing page views at $0.066, ~10% CTR, frequency
  ~1.05 (no fatigue). AD5 Chippies took 80% of spend and held $0.066/LPV across 35k impressions. Daily
  trend since launch: cost per LPV fell $0.094 to $0.063 while volume rose 678 to 1,968 LPV/day.
- **Budget raised $130 to $170/day** (+30%, second scale step) on 2026-07-27.
- **Tracking CONFIRMED LIVE (correcting the earlier day-3 note).** The configurator pixel fires:
  ConfiguratorStarted 8 then 70, AddToCart 6 then 30 across Sat/Sun on pixel 677437638374055. The
  "PageView only" statement was stale, from before the fix deployed. AddToCart and ConfiguratorStarted
  now register. Note: in-app-browser matching means these do not all attribute back to the TOF ad in
  the TOF insights, but they do fire and they do build audiences.
- **BOF retargeting is already live and profitable.** Campaign `120232888615730186` (OUTCOME_SALES)
  retargets All Website Visitors (30/60/180d) and AddToCart-no-purchase (30/60/180d) off the same
  pixel. Last 7d: reach 4,052, frequency 2.05, $104 spend, 4 purchases at $26 each, 17 AddToCarts. This
  is the engine the TOF campaign feeds: every TOF visitor enters the website-visitor pool, every
  configure-and-add enters the AddToCart pool. BOF spend is capped by pool size, not budget, so the way
  to grow it is to keep feeding it with TOF, not to crank its budget (that just raises frequency).
