# Marketing engine — status & plan (READ THIS FIRST)

_Living handoff doc. Last updated 2026-09-04 (video pipeline + first reel, branch `claude/radius-pro-instagram-edit-62mac9`). Previous: 2026-08-03 on `claude/craftons-meta-ads-marketing-qif4cl`._
_Check items off as they're done so we never repeat work. Doc index at the bottom._

---

## 🚨 BEFORE YOU RESEARCH ANYTHING — check it isn't already done

**This repo has now lost the same work twice.** Both times the cost was days of re-derivation and, once,
six misleading live-ready ads. Both were preventable in about ninety seconds:

1. **Drive `MARKETING-BIBLE.md` went unread** until 2026-08-03 — it contains the verbatim law that the
   first Meta ad batch broke.
2. **A complete Lee-approved verbatim research pass (2026-07-21) went unfound** until 2026-08-03 (later pass). It was
   in Drive `META-ADS-BRIEF.md` and on branch `claude/marketing-video-transcript-cy49qx`. A session
   re-derived a *worse* version of it from the wrong inbox and drew an angle the brief forbids.

**So, first three moves of any session:**

```
1. Read this file, then Drive MARKETING-BIBLE.md + META-ADS-BRIEF.md
2. git fetch origin --prune && git branch -r          # work hides on other branches
3. Search before writing:  for b in $(git branch -r); do git ls-tree -r --name-only $b | grep -i <topic>; done
```

**Work is spread across ~25 branches and Drive. Nothing is authoritative just because it's on your branch.**

---

## ✅ Achieved (locked — do NOT redo)

### Content engine (the brain)
- [x] **Content pillars** locked — value-first, 4 lanes + flagship → `CONTENT-PILLARS.md`
  - Teach → **How-To Series** (5 episodes locked) · Inspire → **Built with Craftons** · **Craft Macro** ·
    Sell → **Formwork Builder Showcase** · Flagship → **How This Curve Was Built** (animated, build-toward)
- [x] **Social voice** locked (some dry humour, no emoji, a little slang; value-first, brand barely there) → `SOCIAL-VOICE.md`
- [x] **Brand teardowns / swipe file** (6 brands w/ receipts) → `inspiration/SWIPE-FILE.md`
- [x] **Craft Macro shoot brief** (6 shots for Tia) → `briefs/craft-macro-shoot-brief.md`
- [x] How-To Episode 2 storyboard exists in Drive (`Marketing/Video/How-To-Series/`)

### Brand rules
- [x] Value-first law encoded: ~85% adds value & mentions brand barely/not at all; visual carries a
  subtle logo; soft CTAs only; **no hard sell**. (in `CONTENT-PILLARS.md` + `SOCIAL-VOICE.md`)

### Marketing skill suite (installed in `.claude/skills/`)
- [x] `keyword-research`, `seo-content`, `positioning-angles`, `direct-response-copy`, `content-atomizer`
- [x] **brand memory** mapped for the suite → `brand/` (voice-profile, audience, competitors, keyword-plan)

### Keyword research
- [x] **Keyword plan** done → `brand/keyword-plan.md` — 7 pillars + 6 ad groups (paid + SEO), 90-day calendar
  - Confirmed converters: **"bendy ply"**, **"curved bench seat"**. Product = Radius Pro (not flat bendy sheets).

### Craftons AdWords — campaign BUILT (assets ready to deploy)
- [x] 3 RSAs → `campaigns/adwords/ads/` (Radius Pro · Curved Bench Seat/Formwork · Curved Architraves)
- [x] Keywords (phrase+exact) → `campaigns/adwords/keywords.md`
- [x] Negative keywords → `campaigns/adwords/negative-keywords.md`
- [x] Ad extensions → `campaigns/adwords/ad-extensions.md`
- [x] Campaign settings + weekly mgmt + activation checklist → `campaigns/adwords/campaign-setup.md`
  - Name: **Craftons – Customised Building Products** · $50/day · Melbourne 50km + Geelong + Surf Coast + Mornington
- [x] Verified product URLs: Radius Pro `/products/radius-online` · Formwork `/products/craftons-formwork-builder-custom-online-formwork` · Architraves `/products/curved-architraves`

### Conversion tracking
- [x] **Craftons (Shopify) tracking VERIFIED SOLID** — Google & YouTube app + GA4 already live:
  - **Purchases** = Primary, healthy, 23/$17.3k tracked · **Submit lead forms** = Primary, Active, 443 tracked
  - Purchase "no recent conversions" = just low volume (tag healthy, consent mode active). Nothing to fix.
- [x] Guide written (Shopify + custom-app paths) → `campaigns/adwords/conversion-tracking.md`

### CNC Cut account (existing, separate spend) — TIGHTENED
- [x] Paused $19/click "Industry Specific"; capped CPC ~$3.50; Search Partners/Display off; negatives added;
  match types already exact; Brand bidding reined in → baseline + checklist in `campaigns/adwords/cnc-cut-review-log.md`

### Infrastructure / security
- [x] **Google Ads creds rotated** (2026-06-23), placed in Vercel → `INTEGRATIONS.md` / `DESKTOP-TODO.md`
- [x] **Drive connector permission fix** — tracked `.claude/settings.json` allow-lists Drive tools
  (`mcp__*__*`). NOTE: permission changes only take effect on a **NEW session** (loaded at startup).

---

### Meta Ads agent — designed (2026-08-03)
- [x] **Meta Ads Agent Bible** written → `campaigns/meta/META-ADS-AGENT-BIBLE.md`
  - Digested from the Isenberg × Cody Schneider "marketing agents" episode; translated to Craftons.
  - **Scope locked:** Craftons only · **Radius Pro only** to start · human-approves first, autonomy
    earned via a 5-rung ladder · code lives in `leepatt/cnccut-app` · lightweight data layer (no
    Airbyte/ClickHouse — Neon + `marketing_metrics_cache` already does the job).
- [x] **Recon of `leepatt/cnccut-app` done** (HEAD `01f69e3`) — **resolves the "blocked on repo scope"
  TODO in `INTEGRATIONS.md`.** Env var names confirmed against `docs/marketing/APP-NOTES.md`.
  - ⚠️ **Our notes were badly out of date.** Far more is built than this repo assumed: the four
    `marketing_*` tables (runs/approvals/assets/metrics_cache) on Neon, a **live** `meta-ads.mjs report`,
    `google-ads.mjs` with a full propose→approve→apply pattern, `studio.mjs generate` + **`brand-check`**,
    and the `/marketing` Cockpit with all 8 modules `status: "built"`.
  - **Most of the video's architecture already exists** under different names. The build is *extend*, not *create*.
- [x] **Meta ads agent BUILT** in `leepatt/cnccut-app` on branch `claude/marketing-agents-setup-qamq2f`
  - `tools/_meta-policy.mjs` (new) — all guardrails as pure, credential-free functions
  - `tools/meta-ads.mjs` (rewritten) — `report` · `doctor` · `evaluate` · `check-batch` · `propose` · `apply`
  - Verified live: **13/13 guardrail self-checks pass**, `report` returns real account data,
    `evaluate` closes the loop, `tsc --noEmit` clean.
  - Enforced in code: $2k/mo ceiling · one ad set · +20% max budget step · kill needs no-results
    AND 72h AND $25 · ads always created PAUSED · autonomy rung 0 (propose only) by default.
  - **Full subcommand set:** `report` · `doctor` · `evaluate` · `winners` · `research` ·
    `check-batch` · `upload-image` · `create-creative` · `propose` · `apply`
  - **Cadence live:** `app/api/cron/meta-ads` weekly (Sun 22:00 UTC) → runs `report` then
    `evaluate --file_proposals`. Cannot spend or change the account; only files proposals.
  - **Recipe memory:** `create-creative` stores the generation spec in `marketing_assets.provenance`;
    `winners` joins performance back to it and aggregates by creative family. This is the compounding step.
  - **Remaining:** Phase 0 (Meta pixel + CAPI + EMQ>7) is the gate · Phase 3 (creative production).
    Needs `META_PAGE_ID` for `create-creative`; `META_APP_ID`/`SECRET` only for long-lived token refresh.

### ⚠️ CORRECTION — the Meta account is NOT a cold start (2026-08-03)
Earlier notes (and Shopify's referrer attribution, which shows `social/facebook` at 3 orders / $729
all time) implied Meta was unused. **Wrong — Shopify last-click undercounts Meta by >10×.**
Read live from the Marketing API, last 30 days: **$1,977.82 spend · 21 results · $17,285 revenue ·
~8.7× ROAS.** Account `act_1650412872259063`. Currently **paused** (0 live ad sets).
- **Last campaign's lesson:** when spend scaled ~13× (22–28 Jul), clicks rose ~150× and results went
  to **zero**. 8.35% CTR at $0.09 CPC with no conversions = cheap junk traffic.
- **Causes:** optimised on `AddToCart` (too high in the funnel) · creative hand-segmented by trade
  (pre-Andromeda thinking) · budget scaled in one step (resets learning).
- **Retargeting produced 19 of 21 results on ~$657**; TOF prospecting spent ~$1,300 for ~2.
- **Best ad in the account = "Retargeting – Configurator Hero Ad D" at $6.05/result** (on $12 spend,
  so treat the precision carefully). Worst = "AD5 Chippies" at **$758.74/result**. That's 125× —
  and independent evidence for making the configurator the creative engine.
- Full post-mortem → `campaigns/meta/META-ADS-AGENT-BIBLE.md` §4.5.


### Video pipeline + first reel (2026-09-04, branch `claude/radius-pro-instagram-edit-62mac9`)
- [x] **First reel produced and approved by Lee** — Radius Pro walkthrough, 1080×1350 (4:5), 2:31. Lee's final
  caption is in `campaigns/social/2026-09-radius-pro-reel-01.md`. Source files (phone clip `IMG_5902.MOV`,
  screen recording `Radius pro 03.mp4`, cut sheet) are in Drive `Marketing/Video/`. The finished MP4 was handed
  over in chat (session disk is ephemeral) — if it's needed again, re-run the pipeline below (~15 min).
- [x] **Caption-style research** → `research/2026-caption-styles.md` (taxonomy, data, top 5 for Craftons; next reel: add hook card + step counter + UI callouts on top of the locked karaoke style).
- [x] **Reel process runbook** → `pipeline/video/REEL-PROCESS.md` (pre-shoot checklist, hand-over, pipeline, review loop, filing, learnings). **Start here for the next reel.**
- [x] **Repeatable Reel pipeline** in `pipeline/video/` (see `pipeline/README.md`, "Two-angle Reel"):
  `jumpcut.py` (silence + filler removal via ffmpeg silencedetect + faster-whisper, writes a cut sheet) →
  audio cross-correlation to sync a second angle → `compose-reel.sh` (layouts: `full4x5` chosen; `white9x16`,
  `green9x16` kept) → `captions-highlight.py` (the chosen Craftons caption look: Inter Bold 84 px in
  `--craftons-green`, 2 lines × 2 words, spoken word in line green, no box, bottom at y=1190, `RAISE=t:px`
  to lift it over on-page buttons). Inter static TTFs are vendored in `pipeline/video/fonts/`.
- **Decisions locked with Lee:** 4:5 full-bleed over 9:16 (no green bands); avatar cropped 9:16, small,
  bottom-left; captions centred at the reference height (Bluebeam reel used for placement only); no emoji;
  captions proofread for Australian spelling (metre/millimetre, "form ply", "Accept quote").
- **Gotchas:** Drive files must be "Anyone with the link" for `curl` download (the connector's download tool
  base64-encodes through the chat — unusable for video). Chat upload cap is 30 MiB → render at crf 19 or
  2-pass ~1250 kbps. Wide pages (the quote sheet) need the full 848 px viewport crop — no side trim.
  Facebook Reels length limits vary by account (90 s / 2 min / longer); if a 2:31 reel is rejected, post as
  a standard FB video or cut a 90 s version from the same cut sheet. **Facebook Reels also refused the 4:5** —
  the FB deliverable is the same 4:5 edit padded to 1080×1920 with white (`FB916=1` in compose-reel.sh).

## ⏳ Pending / in progress
- [ ] **Google Ads API Basic access** — application prepared (answers + PDF design doc sent). Lee to submit /
  awaiting Google (~3 business days). → `campaigns/adwords/api-access.md` + `api-tool-design.md`
- [ ] **Mirror Google Ads creds into THIS engine's env vars** (for `google-ads.mjs` to run here)
- [ ] **Delete the disabled old Google Ads secret** in Cloud Console (post-rotation tidy)

---

### Meta ads copy — RECONCILED & REWRITTEN (2026-08-03 (later pass))
- [x] **Drive bible + checklist + brief all read** — the standing rule that had been skipped
- [x] **Lost intel corpus recovered** onto this branch from `claude/marketing-video-transcript-cy49qx`:
  `VOICE-OF-CUSTOMER-curved-jobs.md` · `CURVED-JOBS-WINLOSS.md` ·
  `CURVED-JOBS-DOLLARS-AND-BOTTLENECK.md` · `DREAM-BUYER-AVATAR.md` · `QUOTE-BANK.md` ·
  `campaigns/adwords/customer-voice-ad-copy.md` (**Lee-approved 2026-07-21**)
- [x] **The two-funnel model** — resolves every apparent contradiction between the intel docs.
  **Craftons self-serve** (configurator, 2-day turnaround, builders, 73% win rate) ≠ **CNC Cut bespoke**
  (email a drawing, 3–4 weeks, PMs/site engineers, closed by phone). Ads target the former; the latter
  is intel-only per the Drive golden rule. → `campaigns/meta/copy-reconciliation.md` §2
- [x] **4 of 5 unverified ad claims settled from data** — no interview needed. Part IDs engraved ✅ true ·
  "nothing to fill at the join" ❌ false (joiner blocks; the market's word is *"splice piece for every
  join"*) · "on site in three days" ❌ killed · bendy-ply attack ❌ killed (we sell it)
- [x] **15 corrected creatives written** from cross-validated verbatim → `copy-reconciliation.md` §4
- [ ] ⚠️ **Creative still needs re-rendering** — the words are fixed, the images still show a 900mm
  decorative arc, which order data says is the wrong product. Blocked on the `cnccut-app` repo

---

### ✅ Lee's four decisions — ANSWERED 2026-08-03
- ❌ **Plan Scan is NOT advertisable — in beta testing.** The Drive golden rule stands unchanged: no ad
  may say "send us your plan / your CAD / your drawing". Ads sell the self-serve configurator only.
  **File friction is the best-evidenced pain in the market and we still can't address it.** Re-ask when
  beta ends.
- ⏸ **Fit guarantee: launch without one**, reassess after the first month against CAC. Costs no rework
  (no §4 creative carries one); costs offer strength. → `copy-reconciliation.md` §5.1
- ✅ **Custom conversion gate is CLEAR** — the order Lee was waiting on landed 2026-08-03.
  `InitiateCheckout` ×2 (08-02 22:00 UTC) · `Purchase` ×6 pre-dedup (08-03 04:00 UTC) · orders #1274
  $2,336 + #1275 $1,048, both PAID. `customconversions` returns `{"data":[]}` — nothing half-built.
  **Still needs Lee's explicit word to create — it's an account write and we're at rung 0.**
- 🟡 **Before/after photography in progress** — Lee "trying to get some". `before_after` family stays
  at 0 until they exist.

### 🔴 RETRACTED: the July post-mortem was wrong — 2026-08-03 → `campaigns/meta/suby-8-hacks-implementation.md`
**Lee challenged the "trade segmentation failed" claim. The account data proves him right.** This claim
had been repeated across four docs and was shaping the whole creative strategy.
- **July never segmented the audience.** All five trade ads sat in **one ad set** —
  `TOF | Broad AU | AddToCart`, broad Australia, **no interest targeting**. That *is* Suby's hack #2.
  Creative variation was misread as an audience split.
- **The trade creative was the best hook the account has run:** AD5 Chippies **10.45% CTR**,
  **9,244 landing page views at $0.08**, 132 reactions, 12 saves. (The "winning" retargeting ad:
  1.72% CTR, $1.40/LPV.)
- **What failed was the optimisation event.** Optimised on `ADD_TO_CART`; the account makes ~15 ATC and
  ~13 purchases a month against the **~50 events/week** Meta needs to exit learning. No signal →
  delivery collapses to cheap clicks. Exactly the observed signature.
- **"$758/result" divided real spend by a broken denominator.** Evidence about event volume, not creative.
- 🔑 **This makes the combined custom conversion (IC OR Purchase) the fix for what actually broke** —
  pooling events is how you clear the learning threshold. It is now the top priority, not a tidy-up.
- 🔑 **~13,000 landing page views arrived in July and we captured zero emails.** Pillar 2's missing
  middle, costing real money. Biggest structural gap in the whole build.
- 🔑 **TOF probably did work** — retargeting made 11 purchases on $446 in the same month, off the
  audience TOF built. Last-click credits the wrong ad.
- [x] **Identity variants reinstated** — 9 added, batch now 24 → `radius-pro-ad-copy.md` Angle 4.
  Joiner-block copy finally has a home (concreters-only, #20/#21).
- **The tell I missed:** a 10.45% CTR next to "this creative failed" should never have passed. The
  engagement numbers were in the same API response as the spend numbers.

### 🔴 Lee's product briefing — 2026-08-03 → `campaigns/meta/radius-pro-product-truth.md`
Lee gave the full Radius Pro description after flagging that ad copy had "gone off track". It corrected
more than the copy:
- **The pain was wrong in every ad so far.** It is **not** bog-and-sand or kerfing — Lee: *"that's just
  not related to the job at all."* It is: **do the maths → draw the radius on a sheet → cut it with a
  jigsaw**, which is slow, not everyone can do it, workers make mistakes, and most of the sheet goes
  in the bin. **Those words are banned from Radius Pro copy now**, which retires launch Angle 2 and
  overrides the 2026-07-21 approved line "no hand-templating, no bog-and-sand".
- **🆕 The software NESTS parts for minimum waste.** Never used in any ad. Client-fed, a cost argument,
  and no competitor makes it. Probably the strongest unused asset we have.
- **Engraving is the RADIUS measurement, not a part ID.** Four 900mm plates all arrive engraved 900mm.
  The Shopify attribute `_part_id_engraving` misled the earlier reading.
- **Joiner blocks are CONCRETERS ONLY** — not carpenters. Can't carry general copy.
- **2–3 days delivered, Australia-wide via FedEx**, interstate included. Reverses the earlier
  over-cautious kill of the three-day claim.
- **Tails** (extend the leg 100–300mm to meet a straight frame) and **doubling up** plates confirmed.
- ✅ **Lee suggested trade-targeted copy for concreters/landscapers — and he was right.** I pushed back
  citing July's "$758/result"; the account data overturns that. **See below.**
- [x] **Copy rewritten from it** → `campaigns/meta/radius-pro-ad-copy.md` (15 creatives, v2)

---

### ✅ Custom conversion CREATED — 2026-08-03 (Phase 0 gate closed)
`Sales Intent — Checkout or Purchase` · ID **`27686282527680441`** · rule
`{"or":[{"event_name":{"eq":"InitiateCheckout"}},{"event_name":{"eq":"Purchase"}}]}` · category `OTHER`.
Created on Lee's go-ahead — *"we want sales, not attention."*
- ⚠️ **API gotcha worth encoding in `meta-ads.mjs`:** the rule key is **`event_name`, not `event`**.
  With `event` the API says *"A conversion rule is required at creation time"*, which reads like a
  missing param. `custom_event_type` must be **`OTHER`** for a mixed rule; the IC enum is
  `INITIATED_CHECKOUT` (past tense). **Deletes archive, not remove** — two `ZZTEST` objects are
  archived on the account.
- ⚠️ **It does NOT clear the learning threshold, and that's expected.** Ground truth: 38 real orders
  /30d, pixel counts 2.55× higher pre-dedup. Purchase 8.8/wk · IC 17.5/wk · **combined 26.3/wk** vs
  Meta's ~50/wk. It is 3× Purchase alone and the best available without dropping to browse intent.
- **Why not AddToCart** (which would clear 50/wk at 83/wk): **IC→Purchase is 51%, ATC→Purchase is 11%.**
  In the configurator, adding to cart is how you see a price. Optimising on it buys attention.
- ⬜ **Still to wire:** the ad set's `promoted_object` must point at this conversion at launch.
  Creating it changed nothing about delivery on its own.

---

### 🔴 CORRECTION — the account is NOT paused, it is spending (verified 2026-08-03)
`STATUS.md` and the agent bible both said *"currently paused, 0 live ad sets."* **Wrong.**
- **`Retargeting Campaign - Bottom Of Funnel` is ACTIVE** at $15/day — ad set `120233074187690186`.
  Spent **$15.28 yesterday, $1.10 today**; last 3 days **$124.83 → 3 IC, 1 purchase** (inside the $322
  break-even). **Don't switch it off to tidy the test** — it's making money.
- `RadiusPro | TOF | Ardreagh | Jul26` spent **$132.69 over 3 days for zero IC and zero purchases**
  before being paused. Same signature as July.
- ⚠️ **The test does not start from zero.** Live retargeting will convert people the new TOF ads warm
  up and take last-click credit — the exact trap from the July post-mortem. **Read blended at account
  level, not per-campaign.**

### ✅ `META_PAGE_ID` FOUND — `611852278682648` ("Craftons")
Was recorded as missing because `me/accounts` returns empty for this SYSTEM_USER token. It resolves via
the business: `GET /1006792137511423/owned_pages`. **Needs adding to session env + Vercel** —
`create-creative` can't publish without it. This was a genuine hard blocker.
⚠️ **No Instagram account linked to the ad account** (`instagram_accounts` empty) → Facebook-only
placements unless connected.

---

### ✅ Creative REBUILT — 33 ads, brand-guide accurate (2026-08-03)
Built in `leepatt/cnccut-app` @ `claude/marketing-agents-setup-qamq2f`, `content-engine/ads/`.
- 🆕 **Official social brand guide received** — `Craftons_BrandGuide_SocialLayouts01.pdf`
  (Residency Studios, 27.07.2026). **It corrected the type at the root:** headlines are **Aeonik
  Regular, not Bold** (previous renders were shouting), labels are **Akkurat Mono Bold** in caps
  (there was no mono voice at all), body is Aeonik Regular 25pt/130%, and the palette gains
  **sage `#dae6d2`**. Six-row grid, logo bottom-left, URL bottom-right in mono.
- **Lee's review notes applied:** flat **"Delivered in 3 days"** (hedge reversed — seeing it rendered
  changed his call) · **stat cards deleted** ("I def would not post") · **formwork/architrave imagery
  banned** — Radius Pro only for now.
- Guide's own approved lines used verbatim: **"LESS MEASURING. LESS CUTTING. MORE BUILDING."** and
  **"Measure. Specify. Build."** Both land on the pain Lee described.
- ⚠️ **Akkurat Mono is licensed and not in the repo — JetBrains Mono Bold substituted.** Get the real
  file before spend.
- ⬜ **Still fails `check-batch`: 2 families vs a minimum of 3.** Not fixable by effort — every image
  asset is a product render on white. **Lee's photography unlocks this AND hack #4 together.**
- Contact sheet at `content-engine/public/ads/static/_contact-sheet.png` for keep/bin review.

---

## ⏭ Next steps (in order) — full detail in `campaigns/meta/launch-readiness.md`
1. ⬜ **Lee to flag keepers vs bin** from the 33-ad contact sheet, then regenerate into the gaps.
2. ⬜ **Add `META_PAGE_ID=611852278682648`** to env.
3. ⬜ **Wire the ad set to the custom conversion** (`promoted_object` → `27686282527680441`). The
   object exists; nothing points at it yet.
4. ⬜ **Run `brand-check` live on the new batch** — built, never run on a real image.
2. **Re-render the creative** against the corrected copy, then re-run `ingest` → `check-batch` →
   `brand-check`. Needs `leepatt/cnccut-app` @ `claude/marketing-agents-setup-qamq2f`.
   **Still the biggest open item** — the words are fixed, the images are not.
3. **Check EMQ > 7** — needs 24–48h of pixel traffic from 2026-08-03. **Not readable yet**; earliest
   2026-08-04, safest 2026-08-05.
4. **Verify `brand-check`'s vision path live** — built, never run. Sunday's cron is its first real run.
5. **Submit the Basic-access application** (Lee) — answers + PDF are ready (`api-access.md` / `api-tool-design.md`).
2. **Once Basic access granted:** Claude builds `tools/google-ads.mjs` (read-only reports + human-approved
   writes), mirrors creds into env, and **the engine deploys the Craftons campaigns** (the goal: engine-run, tracked from day 1).
3. **Set up the weekly-review routine** (Claude routine, web app) once campaigns are live → auto-report + advice.
4. **CNC Cut:** reassess in a week vs the baseline (`cnc-cut-review-log.md`); add GA4-linked tracking if not attributing.
5. **Content production** (independent of ads): Tia shoots Craft Macro Session A; build out How-To Series shot lists.

---

## ❓ Open questions / decisions needed (answer these to unblock)
- **Account structure:** Is Craftons in the **same Google Ads account as CNC Cut (`310-491-2421`)** or separate?
  (Decides where the engine builds the new campaigns. Craftons conversion tracking lives in the account with
  23 purchases + 443 lead forms.)
- **Sitelink "Get a Quote" URL** — confirm the real contact/quote page (placeholder `/pages/contact`).
- **Call extension phone** — confirm best lead number (had `0466 146 744`).
- **CNC Cut negatives:** do they offer **milling**? **engraving**? (If no → add as negatives.)
- **Configurators:** do customers **check out & pay online**, or mostly **request a quote**? (purchase vs lead mix)
- **Tidy:** demote `file_download` conversion from **Primary → Secondary** (don't optimise toward PDF-downloaders).

---

## ⚠️ Key learnings / gotchas (so we don't relearn them)
- **Conversion tracking is THE gate for ads.** CNC Cut spent ~$2k/mo blind (0 tracked) — don't launch anything
  without it. Craftons is already instrumented (good).
- **Drive (and other connector) tools need allow-listing in tracked `.claude/settings.json`**, and permission
  changes **only apply on a new session**. `settings.local.json` is gitignored → doesn't carry to fresh sessions.
- **Engine-run ads need:** (a) Basic access, (b) creds in this env, (c) a `google-ads.mjs` tool. Basic access
  alone is NOT enough, and is NOT required to launch manually.
- **Reading file *content* from Drive** needs the connector allow-list (search works without it). PDFs in this
  env: `pip install pdfminer.six cffi` then `pdfminer.high_level.extract_text` (poppler not installed).
- **Voice:** brand-caption tone ≠ paid-search-ad tone. Ads use direct CTAs; social is value-first/soft-CTA.
- 🔑 **Two funnels, two buyers — never mix them.** **Craftons self-serve** (configurator → instant price
  → checkout; 2-day turnaround; builders ordering plates by qty) vs **CNC Cut bespoke** (email a
  drawing; quoted in Quotient; 3–4 weeks; PMs/site engineers; closed on the phone). The CNC Cut inbox
  is our richest intel source and is **explicitly not what we advertise** (Drive golden rule). Mining it
  and then writing Craftons ads from its *offer* is how the 2026-08-03 batch went wrong. The **language**
  crosses over; the **offer and lead time do not.**
- **Lead times are per-product, not per-company.** 2 days = Radius Pro. 3–4 weeks = bespoke CNC. An ad
  that blurs them is a broken promise waiting to happen.
- **"Awaiting approval" ≠ the customer said no.** On 11 of 12 stalled jobs no quote was ever sent. The
  biggest conversion lever found so far is **internal quoting speed**, not copy.

---

## 📁 Document index
**Strategy / brand:** `CONTENT-PILLARS.md` · `SOCIAL-VOICE.md` · `inspiration/SWIPE-FILE.md` ·
`.claude/skills/craftons-design/BRAND.md` · `briefs/craft-macro-shoot-brief.md`
**Skill suite + memory:** `.claude/skills/{keyword-research,seo-content,positioning-angles,direct-response-copy,content-atomizer}/` ·
`brand/{voice-profile,audience,competitors,keyword-plan,assets}.md`
**AdWords:** `campaigns/adwords/` → `campaign-setup.md` · `keywords.md` · `negative-keywords.md` ·
`ad-extensions.md` · `ads/*` · `conversion-tracking.md` · `api-access.md` · `api-tool-design.md` ·
`cnc-cut-review-log.md`
**Meta Ads:** `campaigns/meta/` → **`radius-pro-product-truth.md` (⭐ WHAT THE PRODUCT IS — Lee's own
words. Read before writing a single line of copy. Beats every other doc on product facts)** ·
**`radius-pro-ad-copy.md` (⭐ the live copy set, v2)** · `BUILD-CHECKLIST.md` (every item, machine vs
marketing) · `copy-reconciliation.md` (the two-funnel model + claim verdicts; **§4 copy superseded**) ·
**`suby-8-hacks-implementation.md` (⭐ the 8 hacks → concrete actions, + the corrected July post-mortem)** ·
`META-ADS-AGENT-BIBLE.md` (agent design + phased build) · `launch-angles.md` (⚠️ Angle 2 retired,
anti-angle section retracted) · `conversion-tracking.md` · `radius-pro-interview.md` (mostly answered)

**🔑 Market intel — the verbatim corpus. READ BEFORE WRITING ANY COPY.** `research/market-intel/` →
`VOICE-OF-CUSTOMER-curved-jobs.md` (9 verbatim enquiries, won + lost) · `CURVED-JOBS-WINLOSS.md`
(68 jobs, win rate by product) · `CURVED-JOBS-DOLLARS-AND-BOTTLENECK.md` ($ sizing + the quoting
bottleneck) · `DREAM-BUYER-AVATAR.md` · `QUOTE-BANK.md` · `radius-pro-orders.md` (what customers
actually order, from Shopify) · `enquiry-language.md` (⚠️ correct language, superseded conclusion) ·
`campaigns/adwords/customer-voice-ad-copy.md` (**Lee-approved 2026-07-21**)

**In Google Drive** `Peninsula Studio/01 Craftons/Marketing/` — **not optional reading:**
`MARKETING-BIBLE.md` (Suby doctrine · Godfather Offer · the verbatim law · the 8 hacks §9) ·
`MARKETING-CHECKLIST.md` (the phased action list) · `META-ADS-BRIEF.md` (**the golden rule** + approved copy)

**Setup / ops:** `SETUP.md` · `INTEGRATIONS.md` · `DESKTOP-TODO.md` · `CLAUDE.md` · `QUALITY-DOCTRINE.md`
