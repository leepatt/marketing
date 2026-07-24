# Radius Pro TOF. LAUNCHED (record)

**Went live: 2026-07-22.** First native TOF batch off the real Ardreagh job. Built via the Meta
Marketing API. This file is the record of exactly what is running.

## Campaign
- **Name:** `RadiusPro | TOF | Ardreagh | Jul26`
- **Campaign ID:** `120247183657950186`
- **Ad account:** `act_1650412872259063` (Craftons, AUD, Australia/Melbourne)
- **Objective:** Traffic (OUTCOME_TRAFFIC)
- **Budget:** $130/day AUD, campaign budget (CBO), lowest cost (raised from $100 on 2026-07-24,
  +30%, single safe step; Friday into the weekend + phone at 3x justified feeding it. Read net cash
  Monday, step again <=30% every 2 to 3 days only while net cash holds.)
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

## ~24h read (pulled 2026-07-23, spend $98.09, 956 LPV, blended $0.103/LPV)
| Ad | Spend | Link CTR | LPVs | Cost/LPV |
|---|---|---|---|---|
| AD2 Landscapers | $76.10 | 9.1% | 785 | $0.097 |
| AD1 Concreters | $19.78 | 7.9% | 163 | $0.121 |
| AD2b Landscapers finished-first | $2.21 | 3.9% | 8 | $0.276 |

- Meta has chosen: ~78% of spend on AD2 Landscapers (best CTR, cheapest LPV). Landscaper beats
  Concreter; process-first beats finished-first (Meta all but paused AD2b at 3.9% CTR). Strong signal
  for the day-3 read: scale AD2, clone the winner to Formworkers + the curved-wall builder/chippy ads.
- Held per doctrine: day 1 to 2 is gut-check only, learning phase left alone.
- Tracking now flowing: pixel AddToCart 25, InitiateCheckout 9, Purchase 3 in the ~24h window (up from
  9 ATC the morning before). The fix is live.
- Net cash (hack 8, judged honestly): 2 new Craftons orders since launch, #1264 Formwork Builder $881
  and #1265 Bendy Formply $640, but NEITHER is a radius-online order and #1265 is a repeat customer, so
  not attributable to these ads. No direct Radius Pro sale yet. Fine at ~1 day for TOF.

## OFFLINE SIGNAL: phone ringing non-stop since launch (2026-07-23)
Lee reports the phone has been ringing non-stop since the ads went live. This is the metric that
matters (hack 8: net cash at the business level, not ROAS %). Tradies call rather than self-serve, so
phone volume is likely the real conversion path and the online pixel numbers are undercounting true
response. Implication: performance is better than the online-only read, which strengthens the case to
scale the winner at the day-3 read.
- TO CAPTURE (so we can attribute): ask every caller "how did you hear about us?" and tally.
- CONSIDER: a call-tracking number on the radius-online page to attribute calls per-ad (this audience
  phones, so it is worth the setup).

**Refined read (2026-07-23, per Lee):** calls are about ALL things Craftons, not just radius, and
running about **3x normal volume**. So the ad is a top-of-funnel driver for the WHOLE business: it lands
tradies on the site, they browse the range, and convert (often by phone) on whatever fits. This is the
blended net-cash win (hack 8), judged at the business level, not per-product ROAS. It also means the two
orders above (#1264 Formwork Builder, #1265 Bendy Formply) are credibly part of this lift after all.
Implications: (1) online pixel undercounts true return, real performance is stronger; (2) phone is the
conversion path, so the phone number / click-to-call must be prominent on radius-online and site-wide
(hack 6 congruence) or we leak calls; (3) raises confidence to scale AD2 Landscapers at the day-3 read
and to clone the winner across more trades AND products, since the whole range benefits.

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

## ⚠️ ATTRIBUTION IS UNDER-COUNTING (2026-07-24). Do NOT judge configurator conversion on Meta's number
The Radius Pro configurator runs in a cross-origin iframe (craftons-curves-calculator.vercel.app) on
the Shopify page. The Meta click ID (`_fbc` from `fbclid`) lives on craftons.com.au and frequently
does NOT reach the configurator's AddToCart event, so Meta files ad-driven adds as unattributed.

- Pixel TOTAL AddToCart (all traffic): ~55 in 24h and growing. Configurator works and is used.
- Meta AD-ATTRIBUTED AddToCart: ~2. This is a measurement artefact, NOT low usage.
- The ads are almost certainly driving many more configurator adds than the report shows.

**Implication for decisions:** judge these ads on CTR, cost/LPV, net cash and PHONE volume (hack 8),
NOT on ad-attributed AddToCart, until the tracking is fixed. Do not pause an ad for "low AddToCart".
Fix + full diagnosis: bug-and-fix brief for the craftons-curves-calculator repo (root cause = click
ID lost across the iframe boundary; fix = forward fbclid into the iframe src). Verify via Meta Events
Manager AddToCart match quality (share of events carrying `fbc`).

## Curved-wall ads ACTIVE (2026-07-24, Lee approved, flipped live)
Built paused, previewed, then set ACTIVE by Lee on 2026-07-24 (effective_status IN_PROCESS at flip,
i.e. Meta ad review, then delivers). Now competing for spend in the CBO alongside the Ardreagh ads.
Three single-image identity clones off the real Lawless Construction curved-wall frame photo, built
via the Meta Marketing API into the SAME live ad set `120247183658270186` (one CBO, Meta distributes).
All **PAUSED**. Copy locked in `AD-CONCEPTS.md` (architect-vs-builder hook, @lawlessconstruction
credited). Image `creative/refs/IMG_5566-clean-BASE.jpeg` (real job, permission granted), image_hash
`923c0b632935f8af124c792e1b56d3f9`.

- **AD4 Builders** · ad ID `120247222879340186` · creative `883978048104405` · utm_content `ad4_curvedwall_builder`
- **AD5 Chippies** · ad ID `120247222879990186` · creative `1347855387557688` · utm_content `ad5_curvedwall_chippy`
- **AD6 Carpenters** · ad ID `120247222880330186` · creative `1030098886572890` · utm_content `ad6_curvedwall_carpenter`
- (Headline swapped 2026-07-24, creatives repointed; superseded creatives `1728285318422905` /
  `1793453378453651` / `3276441942527863` are orphaned, ignore.)

- **Format:** single image 4:5 (1080x1350), not carousel. Headline `Curved walls, without the
  guesswork`. Description `Curved Formply wall plates, cut to size. Priced online.` CTA Learn more.
  Destination `craftons.com.au/products/radius-online` + per-ad UTMs.
- **The @lawlessconstruction tag is a written credit only** in a dark-post ad (does not hotlink or
  notify). To honour the tag promise, post the photo organically tagging them (by hand, IG app),
  separate from these ads.
- **Before activating (Lee):** review each ad's real Meta preview, confirm the tradie photo reads
  native and the caption renders clean, then flip to Active. Standard-enhancements not opted out at
  build (deprecated field); toggle per-ad in the preview if you want it off to stay native.
- **Read:** builder vs chippy vs carpenter on net cash + phone volume (hack 8), which also settles
  whether "chippy" reaches carpenters as well as the formal word.

## Watch / next
- Day 1 to 2: gut-check CTR + cost per landing page view. If clearly failing, pause. Otherwise do not touch.
- 3 to 4 days: read concreter vs landscaper. Scale the winner (raise campaign budget <=30% every 2 to 3
  days), then clone the winner to Formworkers and to the AD4/AD5 job types once we have those photos.
- Judge on net cash, not ROAS % or Meta's Opportunity Score.
