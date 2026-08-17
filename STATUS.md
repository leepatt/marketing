# Marketing engine — status & plan (READ THIS FIRST)

_Living handoff doc. Last updated 2026-08-04. Branch: `claude/craftons-meta-ads-marketing-qif4cl`._
_Check items off as they're done so we never repeat work. Doc index at the bottom._

---

## 🟢 META ADS ARE LIVE — v2 launched 2026-08-17

**v2 ad set `120247812165960186` is `ACTIVE` at $65/day**, optimising on standard `INITIATED_CHECKOUT`
(pixel `677437638374055`), AU-only, with all 6 `aug26 v2` ads `ACTIVE`. v1 stayed `PAUSED`. Verified by
reading state back from the Graph API, not from the mutation responses. Blended spend ~$80/day with
retargeting.

Lee approved after reading EMQ: **`InitiateCheckout` 6.4/10, `Purchase` 8.3/10** — the 6.4 accepted
knowingly as an attribution drag, since Bible §4.7 sets the bar at >7. Applied through the
propose/approve/apply path with an audit trail; approval IDs in `campaigns/meta/RUNBOOK-lee-tasks.md`.

**Next action: a reading at ~72h (≈ Aug 20). Not before.** Kill rule needs ≥72h AND ≥$25 AND zero
results, and never fires while results can't be counted. Readable CAC 3–4 weeks. Ladder
$65 → $78 → $94 → $100, one step/week, only at CAC ≤ $322. **Always read `inline_link_clicks`** — the
headline CTR runs ~3.5× inflated on these ads.

---

## 🔴 CORRECTION — Meta match quality was MISDIAGNOSED (2026-08-17)

**Advanced Matching was never broken. Do not "fix" it.** The Aug26 post-mortem's second root cause is
withdrawn. Verified against the live API this session:

- `email` (332) and `phone` (212) arrive in the last 7d, plus `fn`, `ln`, `ct`, `st`, `zip`, `country`.
  They have arrived **every day for 14+ days** — including before the claim was written.
- `had_pii`: **100% of `Purchase` events (39/39)** carry PII. `InitiateCheckout` 51 with / 79 without.
- `event_source`: 7831 SERVER vs 4028 BROWSER — CAPI is live.

**The error:** `/stats?aggregation=match_keys` returns **hourly buckets**. The first bucket held 6 events
carrying only `external_id`, and that fragment was read as the whole window.

**On the corroborating "sources" — each one checked individually:**

- `match_rate_approx: -1` and `matched_entries: 0` **are real** — but they are **fields on the pixel
  node, not stats aggregations** (as aggregations the API rejects them outright). They report
  **offline / customer-list upload matching**, which this pixel has never used. `-1` is Meta's
  "not applicable" sentinel. They say nothing about browser-event Advanced Matching.
  _(An earlier version of this correction wrongly claimed these fields don't exist. They do.)_
- `/da_checks` → `[failed] Pixel has low event source match rate` — **read its own `description`**:
  _"Some content_ids sent from pixel fires by this pixel do not match any catalog associated to the
  pixel…"_ That is a **product-catalog / DPA check about `content_id` alignment**. The title is
  misleading; it is not a customer-identity match check at all.
- Meta's UI warning and the `$118` figure derive from the same match-rate surface as each other.

So the "four independent sources" were: one misread fragment, two fields about a different matching
system entirely, and one check whose title does not describe what it measures.

> **Rule to add to the two existing ones.** The old failures verified *configuration instead of
> function*. This one verified *a fragment instead of the whole*. **Paginate before you conclude. A small
> sample is a reason to widen the window, never a reason to lean harder on sources that already agree.**

What remains true: match coverage is *partial* (~25–39% of TOF events carry PII, normal for guest
browsing). The one genuine open item `/da_checks` reports is a **catalog `content_id` mismatch**, which
affects dynamic/catalog ads — worth a look later, **irrelevant to this launch**. Neither is a blocker,
and **there is no pending Shopify fix behind either.**

**EMQ itself is genuinely not in the API.** Probed this session as a node field
(`event_match_quality`, `match_quality`, `data_quality`, `emq`, …), as an edge, and as a stats
aggregation — all rejected. The launch gate's demand for a human to read it is correct, not lazy.

**✅ EMQ READ 2026-08-17 (Lee, Events Manager, Jul 20 → Aug 16):**
**`InitiateCheckout` 6.4/10 · `Purchase` 8.3/10** · TOF events 6.1–6.3.
A pixel receiving only `external_id` scores 2–3, so this independently **confirms Advanced Matching
works**. Purchase clears the Bible's >7 bar; **InitiateCheckout at 6.4 does not** — launching is
therefore a knowing, recorded deviation on the optimisation event, not a satisfied gate.

**Net effect on the launch:** the only outstanding gate is Lee's EMQ read. The US boosted post is now
`ARCHIVED` (resolved). Details: `campaigns/meta/RUNBOOK-lee-tasks.md`.

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
Built in `leepatt/cnccut-app`, `content-engine/ads/`. **Now merged — see the note below for where it
actually lives.**
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
  ✅ Committed to `main` along with all 35 rendered PNGs — it survives a fresh container.

---

### 📍 WHERE THE AGENT CODE LIVES — verified 2026-08-04

**The agent is built and merged.** `leepatt/cnccut-app` **`main` @ `5cd7910`** — PR
[#97](https://github.com/leepatt/cnccut-app/pull/97), **squash-merged 2026-08-04 00:27 UTC**.

⚠️ **Two traps, both verified this session, both easy to get wrong:**

1. **`claude/marketing-agents-setup-qamq2f` is dead history.** Because #97 was *squash*-merged, the
   branch's 12 commits are **not ancestors of `main`** — `git merge-base --is-ancestor` says no, and
   `git branch -r --contains HEAD` returns nothing. It looks unmerged and isn't. The content is
   identical (`git diff origin/main HEAD -- content-engine/ads/` is empty). **Never stack new commits
   on that branch.** Start follow-up work from `main`:
   `git fetch origin main && git checkout -B <new-branch> origin/main`
2. **`cnccut-app` is NOT in a fresh session by default.** This container had it at
   `/workspace/cnccut-app`, but containers are reclaimed. A new session clones `leepatt/marketing`
   only. To get the code: `add_repo(owner="leepatt", repo="cnccut-app")` → run the clone command it
   returns → `register_repo_root`. **Do this before looking for the agent, not after concluding it's
   missing.**

**Paths inside `cnccut-app`** (the tools are at the repo root, *not* under `content-engine/`):

| What | Path |
|---|---|
| Guardrails (pure, credential-free) | `tools/_meta-policy.mjs` |
| The agent CLI — 15 subcommands | `tools/meta-ads.mjs` |
| Ad copy + layout definitions (33 ads) | `content-engine/ads/ads.config.mjs` |
| HTML→PNG renderer | `content-engine/ads/render-ads.mjs` |
| Rendered PNGs + contact sheet | `content-engine/public/ads/static/` |
| Weekly cron (report → evaluate) | `app/api/cron/meta-ads/route.ts` |
| Cockpit UI | `app/marketing/meta-ads/page.tsx` |

**Subcommands:** `report` · `doctor` · `evaluate` · `check-batch` · `winners` · `pool` · `cac` ·
`entropy` · `ingest` · `research` · `upload-image` · `create-creative` · `propose` · `apply` ·
`pause-campaign`

**Policy constants** (`_meta-policy.mjs`): `MONTHLY_CEILING_AUD = 2000` · `MAX_AD_SETS = 1` ·
`MIN_CREATIVES_PER_BATCH = 15` · `MAX_SYNTHETIC_FRACTION = 0.4` · `DEFAULT_AUTONOMY_RUNG = 0`
(propose-only; the rung reads from env `META_AUTONOMY_RUNG`, never from code).

---

## 🔑 Environment keys — state as of 2026-08-04

Lee added three vars on 2026-08-04. **Env vars load at session start only**, so they are invisible to
any session that was already open when they were added. Verified in-session with a length/prefix check
(never print a secret's value).

| Var | In env | Notes |
|---|---|---|
| `META_ACCESS_TOKEN` | ✅ | System-user token. Working all session |
| `META_AD_ACCOUNT_ID` | ✅ | `act_16…` |
| `ANTHROPIC_API_KEY` | ⬜ added, needs fresh session | **New key** — Vercel would not reveal the old one (encrypted on write), so a replacement was minted. Does not disturb the Vercel deployment. **API billing is separate from Lee's Max subscription** — if it 400s on credit balance, top up at platform.claude.com → Billing |
| `HEYGEN_API_KEY` | ⬜ added, needs fresh session | Unblocks the `avatar` family |
| `META_PAGE_ID` | ⬜ added, needs fresh session | `611852278682648`. **Not a secret** — it's a hard blocker for publishing, not a credential |

**First move of the next session:** re-run the presence check before assuming anything is live.

---

### ✅ Session 2026-08-04 — the agent run live for the first time

**The machine is verified working against the real account. The launch is still gated on photography.**

- [x] **`doctor` live: clean.** Credentials present, `missing_required` empty, **22/22 guardrail
  self-checks pass**. `META_APP_ID`/`SECRET` still absent — token-refresh only, non-blocking.
- [x] **`report` live: reads the account cleanly.** 30d (07-05 → 08-04): **$1,984.66 spend · 20 results ·
  $16,898 revenue · 8.35% CTR · $0.09 CPC**. Retargeting carries it — **18 of 20 results on $660.90**,
  while `RadiusPro | TOF | Ardreagh` spent **$1,279.94 for 2**.
- [x] **`check-batch` run live on the 33-ad batch → FAIL, one problem, exactly as documented:**
  `2 families (static_craft 28, configurator 5), min 3`.
- [x] 🆕 **THE WINNING PHOTO IS RECOVERED.** Pulled from the ad account by image hash
  `923c0b632935f8af124c792e1b56d3f9` → `content-engine/sandbox/real/site-lawless-curved-stud-wall.jpg`
  (1080×1350). The account's best-ever creative was previously **not in the repo at all**.
- [x] 🔑 **AD4, AD5 and AD6 all used the IDENTICAL image hash.** They differed only by the identity word,
  and AD5 won. **This is the account's own proof that identity words multiply a proven winner rather
  than finding one** — the rule was doctrine, it is now evidence.
- [x] **`check-batch` now PASSES — honestly.** Added a real `real_footage` family (3 creatives off the
  recovered photo) → 3 families, 36 creatives. **Nothing was relabelled.**
- [x] **New `bare` template** in `render-ads.mjs` — emits the photograph and nothing else: no overlay,
  no logo, no brand furniture, because that is what the winner was. Rendered and verified.
  Also fixed: the photo loader hardcoded `image/png` and produced a blank frame for JPEGs.
- [x] **Long-form copy set written** → `campaigns/meta/radius-pro-longform-copy.md`. LF1 is the July
  winner with one word corrected; LF2 leads on **nesting/waste** (the strongest never-used argument);
  LF3 is the marking-out pain in Lee's words; LF4/LF5 are identity clones **gated until a winner
  exists**; LF6 is the configurator.
- [x] **Avatar path verified end-to-end.** `HEYGEN_API_KEY` works (1,264 avatars); a 15.3s test video
  rendered and downloaded. The **ACL checker was tested with negative controls** and catches every
  first-person experience claim.
- [x] **Custom conversion verified live** — `27686282527680441`, rule uses `event_name`, not archived.
  **Confirmed nothing points at it:** every ad set on the account uses `custom_event_type` against the
  raw pixel; not one references `custom_conversion_id`.
- [x] **July's broad targeting independently re-confirmed** — `TOF | Broad AU | AddToCart` reads back as
  `geo=["AU"]`, **`interests: 0`**. The trade-segmentation retraction stands.

#### 🔴 Found this session — three things that were believed done and are not

1. **`ANTHROPIC_API_KEY` is NOT in session env.** So **`brand-check`'s vision path has still never run.**
   It refuses honestly (marks `skipped`, never silently passes), so nothing is mislabelled — but this
   remains untested. It was the whole point of step 3. → `INTEGRATIONS.md`
2. **`META_PAGE_ID` arrived as `PAGE_ID`.** Value is right; the name is wrong and every tool reads
   `META_PAGE_ID`. Rename it in env + Vercel. Until then, prefix `META_PAGE_ID="$PAGE_ID"`.
3. **The agent CANNOT wire the ad set to the custom conversion.** `promoted_object` appears nowhere in
   `tools/`, and `apply` implements only `pause_ad`, `set_budget`, `publish_ad` — **there is no
   `create_ad_set` executor.** The guardrail for it exists; the capability does not. Full settings spec
   + recommendation → **`campaigns/meta/ad-set-wiring.md`**
4. **EMQ is not readable via the API.** `event_match_quality` is not a permitted `stats` aggregation —
   it is an Events Manager UI metric. Must be read by eye. → `ad-set-wiring.md`
5. **An ad set targets the United States.** `Instagram post: CAMPBELL STREET` has
   `geo_locations: {countries:["US"]}` and spent **$43.82 for 0 results**. Campaign is paused. Do not
   un-pause as-is.
6. **`META_ACCESS_TOKEN` should be rotated** — Meta's `stats` endpoint embeds the token in its own
   paging URL and a diagnostic printed it into the session transcript. Not committed anywhere.

#### ⚠️ Don't misread the event volume

Raw pixel counts over 30d are **IC 163 + Purchase 88 = ~58/week**, which *looks* like it clears Meta's
~50/week learning threshold. **It doesn't.** Those are pre-dedup; ground truth is ~38 real orders vs 88
pixel Purchases (2.3× inflation). Deflated: **~25/week** — which matches the 26.3/week already recorded.
**The existing figure was right.** The test runs Learning Limited; judge on CAC vs $322 break-even.

---

### 🕐 DATE CORRECTION — this session's work happened **2026-08-13**, not 08-04/08-05

**The container clock was ~8 days behind for most of this session** and corrected itself partway
through. Verified at the end against three independent sources that all agree: network `Date:` header,
Neon `now()`, and the scheduler — **2026-08-13 19:45 UTC**.

So **every entry below labelled `2026-08-04` or `2026-08-05` for *this session's* work actually
occurred on 2026-08-13.** Earlier sessions' dates (2026-08-03, 08-05, 08-06) are genuine — they are
Neon-stamped and independently confirmed. Left in place rather than mass-edited, because a blanket
find/replace would also have rewritten legitimate statements like *"EMQ readable from 2026-08-04"*.

**Lesson: don't datestamp from `date` alone.** Cross-check against Neon `now()` or an HTTP `Date:`
header before writing a date into the record.

### 🔴 CORRECTION — `brand-check` did NOT run today. It ran 2026-08-05.

An earlier claim this session — *"the state changed under me, brand-check has already run in your other
session"* — **was wrong.** The 33 pass / 3 fail rows are Neon-stamped **2026-08-05T03:48Z, eight days
ago.** They only looked minutes-old because the container clock was 8 days behind when I read them.

What is still true and unaffected: the verdicts themselves (33 pass, 3 fail), the identical-photo
scoring spread (74 PASS / 55 FAIL / 58 FAIL), the rubric diagnosis, and the fix. Only the *when* and
the *who* were wrong. It also means **the Anthropic key was working on 2026-08-05**, which contradicts
the note that it had "never been usable".

### ⚠️ The approvals queue has 9 pending rows and two are landmines
**Do not "approve all".** → hazard table in `campaigns/meta/monitoring-and-reward-plan.md`
- ⛔ `0d6e5fd0…` — `ZZTEST | pipeline test — do not enable`, creative `ZZTEST_PLACEHOLDER_DO_NOT_APPROVE`
- ⚠️ `61eedf31…` — `set_budget` **$100/day onto ad set `120247183658270186`**, the OLD July ad set inside
  the **OUTCOME_TRAFFIC** campaign. Approving it funds the exact setup being replaced. **Reject both.**
- ✅ Approve only `9cf62557-0f55-495c-a17e-d6ed115df9fc` (`create_campaign`, 2026-08-13).

### ✅ Session 2026-08-05 (later) — launch structure buildable, account cleaned

- [x] **Duplicate asset rows resolved.** `brand-check` had already run in Lee's keyed session
  (**33 pass · 3 fail**); 36 redundant `pending` rows removed → clean 1:1 for 36 creatives.
- [x] **Non-AU ad sets deleted — it was SIX, not four** (earlier count was truncated by a `grep -A8`,
  not a tool miss). **5 deleted**, account 12 → 7 ad sets. Live retargeting untouched, still AU/ACTIVE.
  - ⬜ **`Instagram post: CAMPBELL STREET` (US) cannot be removed via API** — it is a boosted Page post;
    both DELETE (*"can only be deleted on your Page"*) and pause (*"Boosted post editing"*) are refused.
    **Lee must delete it from the Page/Business Suite.** Campaign paused, not spending.
- [x] **AU-only is now the DEFAULT, not just a check** — `DEFAULT_TARGETING` (frozen) +
  `withDefaultTargeting()`. Covers the real failure: geo omitted entirely, which Meta delivers
  **worldwide** rather than erroring.
- [x] 🔴 **`brand-check` rubric was failing the proven register — fixed.** `lf1`/`lf2`/`lf3` are the
  **identical photograph** (same file, same `bare` template, differing only in the headline string):
  **74 PASS / 55 FAIL / 58 FAIL.** Reasons given were *"no headline is present anywhere in the image"*
  and *"blue sky conflicts with the no-blue-cast palette rule"* — i.e. it penalised the defining
  features of the account's best-ever creative. Added `FOOTAGE_RUBRIC` for `real_footage`/`before_after`;
  it keeps teeth (stock/staged/AI, fake product, unusable frames, unsafe work, third-party logos).
  Extracted `buildBrandCheckPrompt()` as a pure export — **12 offline assertions, no API key needed.**
  - ⬜ **`lf2`/`lf3` still need re-checking from a keyed session.** This session has no Anthropic key.
  - ✅ The third failure, `a4-chippies-jigsaw`, is a **genuine catch** — two-thirds empty black canvas.
- [x] **`create_campaign` + `create_ad_set` executors built** (Lee's call). Both PAUSED, both require a
  human at every rung. `doctor` **44/44**. Campaign proposal filed:
  `9cf62557-0f55-495c-a17e-d6ed115df9fc` (**pending** — nothing touched the account).
  Verified `apply` refuses `CONFIRM=1` against a pending row.
- [x] 🔑 **Three payload bugs caught with `execution_options:["validate_only"]`**, all of which would
  have failed at apply time: missing `bid_strategy` · `promoted_object` must be `{custom_conversion_id}`
  **alone** (adding `pixel_id` is rejected) · campaign needs `is_adset_budget_sharing_enabled`.
  **Use `validate_only` for every new Marketing API write.** → `ad-set-wiring.md`
- [x] 🔑 **NEW ROOT CAUSE: July's campaign objective was `OUTCOME_TRAFFIC`**, with the ATC ad set inside
  it. A traffic campaign buys clicks, and it bought 19,773 of them at 10% CTR for 2 results. The ad
  set's own `OFFSITE_CONVERSIONS` goal does not rescue that. **Sits alongside the wrong-event
  diagnosis, not instead of it.** `OUTCOME_SALES` is now a locked constant.

### 🔒 Lee's standing rules — 2026-08-05

1. **Ads are AUSTRALIA ONLY.** Now enforced in code, not just written down: `ALLOWED_COUNTRIES` +
   `checkTargeting()` in `_meta-policy.mjs`, asserted by 5 `doctor` self-checks (22 → **27 passing**),
   and audited live by `report` on every run.
   - **The live audit immediately found four offenders** — `Instagram post: CAMPBELL STREET` targets
     **US** ($43.82, 0 results), and `Wed 23/7` + two `Adset 1` have **no country targeting at all**
     (= worldwide). All `CAMPAIGN_PAUSED`, nothing spending. **Awaiting Lee's call to delete or fix.**
   - Interest targeting is a *warning*, not a failure — "no interests" is a launch rule, not permanent.
2. **No ad goes live without Lee's approval.** Verified in code, not assumed:
   rung 0 permits nothing unattended · `publish_ad` hard-codes `status: "PAUSED"` · `create_ad_set` is
   in `ALWAYS_REQUIRES_APPROVAL` at every rung · `apply` needs `CONFIRM=1` **and** an approved row ·
   the weekly cron only files proposals · **there is no "activate ad" mutation in the codebase at all.**
   The only way an ad goes live is Lee toggling it in Ads Manager.

### ✅ RESOLVED — the Anthropic key is saved as `ANTHROPIC_KEY`, not `ANTHROPIC_API_KEY` (2026-08-05)

Lee confirmed from a fresh session: **`ANTHROPIC_KEY` is set** (`sk-ant-api03-…`), `ANTHROPIC_API_KEY`
is **not**. Right value, wrong name — **exactly the same failure as `META_PAGE_ID` → `PAGE_ID`.**
Every tool reads `ANTHROPIC_API_KEY`, so `brand-check` still reports it missing.
**Fix: rename the env var** (preferred), or prefix `ANTHROPIC_API_KEY="$ANTHROPIC_KEY"` per command.
→ full detail + the "paste the name, don't retype it" rule in `INTEGRATIONS.md`.

### ⚠️ OUTSTANDING — 36 duplicate `pending` asset rows (2026-08-05)

`ingest` was **not idempotent** and was run twice, so `marketing_assets` holds **72 pending rows for 36
creatives** (module `meta-ads`). One title, `a3-three-days`, has 3 — so an earlier session duplicated too.

**Consequence if not cleaned:** `brand-check` scores every asset twice (wasted API spend) and a human
reviews each one twice.

- [x] **Bug fixed** — `findAsset()` in `_lib.mjs`; `ingest` now skips already-present assets and reports
  `0 accepted, 36 already present`. It also fixed a second bug in the same place: composition/novelty
  were judged on newly-inserted rows only, so re-running an unchanged manifest judged a batch of
  **zero** and failed the family floor — a false alarm indistinguishable from the real 2-family failure.
- [ ] 🔴 **The 36 duplicate rows still exist.** Claude attempted the cleanup and the permission
  classifier **blocked the DELETE** (correctly — destructive DB write). **Needs Lee's go-ahead.**
  Scoped statement: `module='meta-ads' AND brand_check_status='pending'`, keep the newest row per
  title, never touch `pass`/`fail`/`skipped`.

### 📋 (superseded) `ANTHROPIC_API_KEY` — needed a NEW SESSION (2026-08-05)

Lee confirms he added it. **It is not visible to this session** — scanned every variable *name* and
every variable *value* for the `sk-ant-` prefix: zero matches. Only `ANTHROPIC_BASE_URL` exists.

**Env is captured when the session container starts.** This session started ~Aug 4 10:46; anything added
since is invisible regardless. **A fresh session will pick it up.**
- ⚠️ **Check the saved name first.** Two of the three keys from the same 2026-08-04 batch *did* arrive
  (`HEYGEN_API_KEY` ✅, `META_PAGE_ID` ✅ **but renamed to `PAGE_ID`**). Since one key in that batch had
  its name altered, confirm this one saved as exactly `ANTHROPIC_API_KEY` — `CLAUDE_API_KEY` or
  `ANTHROPIC_KEY` would fail the same way in a new session.
- **First thing to do in the new session:** `studio.mjs brand-check` on the 36-ad batch. Still the one
  built-and-never-run path.

### 📄 New: `campaigns/meta/HOW-TO-create-the-ad-set.md`
Step-by-step for building the launch ad set by hand (~5 min), the exact conversion-dropdown trap to
avoid, the AU-only settings, the four offending ad sets, and the full list of what stops an ad going
live. **Lee's action.**

---

## ⏭ Next steps (in order) — full detail in `campaigns/meta/launch-readiness.md`

### Now unblocked by the keys (do these first)
1. ⬜ **Verify all five vars are visible** in the fresh session.
2. ⬜ **Run `brand-check` live on the 33-ad batch** — built, never once run against a real image.
   Needs `ANTHROPIC_API_KEY`. This is also the first real test of its vision path.
3. ⬜ **AI avatar tests** — needs `HEYGEN_API_KEY`. ⚠️ **ACL constraint already enforced in
   `_meta-policy.mjs`:** a synthetic presenter may describe the product but **must never claim
   first-person experience of it** (s18 / s29(1)(e)). Scripts stay second-person about the product.
   Capped at 40% of a batch.

### The creative work that actually decides the launch
4. ⬜ **Photography — the single biggest lever.** One phone photo of a real curved wall frame
   out-performed everything the account has ever run (10.45% CTR). There is exactly one such photo.
   Unlocks the family gate **and** Suby hack #4 together. Shot list in `campaigns/meta/creative-strategy.md` §4.1.
5. ⬜ **Capture the configurator in use** — screen recording of someone typing a radius and the price
   appearing. Lee: *"our product is the configurator, is the tool."* Currently only a static screenshot
   showing unrepresentative values.
6. ⬜ **Lee to flag keepers vs bin** from the 33-ad contact sheet
   (`content-engine/public/ads/static/_contact-sheet.png`), then regenerate into the gaps.
7. ⬜ **Rewrite the long-form copy pattern from the winner.** Its copy is six paragraphs; every ad in
   the current batch is short. The proven template is unused.

### Launch mechanics
8. ⬜ **Wire the ad set to the custom conversion** (`promoted_object` → `27686282527680441`). The
   object exists and is verified; nothing points at it yet.
9. ⬜ **Check EMQ > 7** — needs 24–48h of pixel traffic from 2026-08-03. Readable from **2026-08-04**,
   safest 2026-08-05.
10. ⬜ **Obtain the Akkurat Mono licence** — JetBrains Mono Bold is substituted in every render. Get the
    real file before this goes to spend.

### Google Ads track (independent of Meta)
11. ⬜ **Submit the Basic-access application** (Lee) — answers + PDF ready (`api-access.md` / `api-tool-design.md`).
12. ⬜ **Once granted:** build `tools/google-ads.mjs` (read-only reports + human-approved writes), mirror
    creds into env, and let the engine deploy the Craftons campaigns — engine-run and tracked from day 1.
13. ⬜ **Weekly-review routine** (Claude routine, web app) once campaigns are live → auto-report + advice.
14. ⬜ **CNC Cut:** reassess vs the baseline (`cnc-cut-review-log.md`); add GA4-linked tracking if not attributing.
15. ⬜ **Content production** (independent of ads): Tia shoots Craft Macro Session A; build How-To Series shot lists.

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
anti-angle section retracted) · `conversion-tracking.md` · `radius-pro-interview.md` (mostly answered) ·
**`aug26-post-mortem-and-salvage-plan.md` (⭐ the Aug26 launch post-mortem: the custom conversion never
fired, delivery collapsed, salvage = repoint to standard InitiateCheckout. Learnings ledger at the end)** ·
`monitoring-and-reward-plan.md` (the reading log: 16h/72h/83h) · `pool-builders.md` (use case confirmed
from orders — formwork, not set-out; LF7 gated)

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
