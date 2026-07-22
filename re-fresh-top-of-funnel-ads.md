# Session refresh. Continue top-of-funnel ads

Continuing work in the `leepatt/marketing` repo, working dir `/home/user/marketing`, on branch
`claude/radius-pro-top-funnel-ads-x2odkm` (all the work is committed there, check it out first).
Goal of this session: keep running the Radius Pro top-of-funnel Meta ads. Manage the live campaign, act
on the day-3 read, switch to the AddToCart signal once the tracking goes live, and add AD4/AD5 when Lee
sends photos.

First actions: `git checkout claude/radius-pro-top-funnel-ads-x2odkm`, then read
`campaigns/meta/radius-pro-tof/LAUNCHED.md`.

## This whole approach relies heavily on the Sabri video. Read it first.
Every decision here comes from Sabri Suby's "8 hacks I wish I knew sooner" Meta ads video. It is the
doctrine, not a nice-to-have. Before doing any ads work, read these two, in order:
- `playbooks/SABRI-8-HACKS-TRANSCRIPT.md` - the full verbatim transcript (the source of truth).
- `playbooks/META-ADS-SABRI-8-HACKS.md` - the distilled, actionable version (each hack plus the
  Craftons move, the copy template, the exact Meta build settings, the anti-patterns).
When in doubt about what to do, go back to the transcript. Do not freelance away from the method.

## Where things stand
- 5-ad native TOF set built to Sabri's 8 hacks: real-photo carousels, NOT designed ad-cards (the
  ad-card version was rejected, never go back to it). Copy is the long-form question-hook structure,
  cut-not-bend (we cut curved plates, we never bend), and no em or en dashes (house rule).
- LIVE in Meta since 2026-07-22: campaign `120247183657950186`, objective Traffic optimising Landing
  Page Views, $100/day AUD (campaign budget), broad AU (Advantage+ audience on, no interests). Three
  ads in one ad set (`120247183658270186`):
  - AD1 Concreters, formwork-first: `120247183658860186`
  - AD2 Landscapers, formwork-first: `120247183659780186`
  - AD2b Landscapers, finished-first: `120247190951340186`
- Day-0 numbers strong: about 9% link CTR, about $0.10 per landing page view, on-target AU mobile. Meta
  is favouring the Landscaper. Judge on net cash, not CTR.
- Clarity read: 94% Facebook in-app mobile, 17% scroll, about 18s active. Page and configurator work
  (Lee confirmed on phone). Root finding: the configurator's "add part to list" was invisible to the
  Meta pixel, so only PageView fired and Meta saw zero deeper events.
- Tracking fix implemented in the separate `craftons-curves-calculator` repo: ViewContent,
  ConfiguratorStarted, AddToCart on add-to-list (increment value, so values sum to the cart total),
  InitiateCheckout, Purchase, browser + Conversions API deduped by a shared event_id. Verified locally,
  PENDING go-live (paste the theme liquid, set `META_CAPI_ACCESS_TOKEN` in Vercel, merge to main,
  confirm in Events Manager).
- Still optimising for Landing Page Views because that is all Meta can currently measure. Do NOT switch
  to Purchase yet (volume and tracking both pending).
- A day-3 read was scheduled from the previous session (a send_later trigger fires about 2026-07-25 into
  that old session). In this fresh session, just run the read on demand, or re-arm a reminder.

## Next steps
1. When Lee or the dev confirms AddToCart is firing in production (outside Test Events): build a Meta
   retargeting audience "added a part but did not buy" (last 30 or 60 days) to feed the BOF engine
   (hack 7). Once there are roughly 15 to 25 AddToCarts a week, duplicate or switch the campaign to
   optimise for AddToCart instead of Landing Page Views.
2. Day-3 read (about Jul 25, or on demand): pull per-ad insights via the Graph API (impressions, link
   CTR, landing page views, cost per LPV, frequency, spend). Compare Concreters vs Landscapers and
   formwork-first vs finished-first. Scale the winner by 30% or less every 2 to 3 days. Clone the winner
   to a Formworkers ad by swapping the one identity word (hack 2). Append a line to `LAUNCHED.md`.
3. When Lee sends AD4 (curved wall plates) and AD5 (curved bench seat) real photos: build those two
   native carousels off the winning structure (shot list in `PHOTO-BRIEF.md`). Convert HEIC with
   pillow-heif, crop to 1:1 1080x1080.
4. Keep shipping fresh statics weekly (hack 1).

## Files to open (read these, do not re-derive). All under `campaigns/meta/radius-pro-tof/` unless noted.
- `LAUNCHED.md`: the live campaign record, all IDs and settings. Start here.
- `AD-CONCEPTS.md`: the 5 ads. AD1 and AD2 copy locked, AD3 to AD5 are drafts.
- `playbooks/SABRI-8-HACKS-TRANSCRIPT.md` (repo root `playbooks/`): the full Sabri video transcript.
  The source of truth. Read it first, we rely on it heavily.
- `playbooks/META-ADS-SABRI-8-HACKS.md` (repo root `playbooks/`): the reusable method and copy
  template distilled from that video. The doctrine for building any new ad.
- `PHOTO-BRIEF.md`: the exact shots needed for AD4 and AD5.
- `PIXEL-TRACKING-SPEC.md` and `TRACKING-VERIFICATION.md`: the tracking work and the Events Manager
  go-live checklist to confirm once the dev deploys.
- `LAUNCH-GUIDE.md`: budget ramp and kill/scale rules (some v1 detail is stale, the ramp and
  measurement rules still hold).

## Carried-over data (surfaced so the next session has it)
- Meta, token already in env as `META_ACCESS_TOKEN`: ad account `act_1650412872259063` (AUD,
  Australia/Melbourne), pixel `677437638374055`, Page `611852278682648`, Instagram
  `17841472259303502` (@craftons.au). Graph API `v21.0`. Manage and read the campaign with curl to the
  Graph API. The earlier build scripts lived in the sandbox scratchpad and are gone, rebuild small
  scripts or use curl as needed.
- IDs: campaign `120247183657950186`, ad set `120247183658270186`, ads AD1 `120247183658860186`, AD2
  `120247183659780186`, AD2b `120247190951340186`.
- Product `radius-online`: product id `8464537125042`, variant `45300623343794`.
- Clarity Data Export API: the token is NOT in the env yet. Add it as `CLARITY_API_TOKEN` in the session
  environment variables (Lee has it, regenerate in Clarity if needed, do not paste it in chat). Endpoint
  `https://www.clarity.ms/export-data/api/v1/project-live-insights`, Bearer token, `numOfDays` 1 to 3,
  optional dimensions (Device, Source, OS, Country), limit 10 calls per day.
