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
