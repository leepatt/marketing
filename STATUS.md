# Marketing engine — status & plan (READ THIS FIRST)

_Living handoff doc. Last updated 2026-07-08. Branch: `claude/meta-ads-tracking-lihdvd`._
_Check items off as they're done so we never repeat work. Doc index at the bottom._

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

### Meta Ads (Craftons) — LIVE, tracking VERIFIED
- [x] **Account live & instrumented** — `act_1650412872259063` ("Craftons's ad account"), AUD, status ACTIVE.
  Meta pixel firing cleanly (add-to-cart, initiate-checkout, purchase w/ values) → ROAS attributing. No measurement gap.
  Creds live in this engine's env (`META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID`) — read-only API pulls work from here.
- [x] **Performance snapshot (last 30d, as of 2026-07-08):** spend **$428** · 33,270 impressions · 14,331 reach ·
  673 clicks · CTR **2.02%** · CPC **$0.64** · **11 purchases** · revenue **$10,792** · **ROAS 25.2×** · ~$39 CPA.
  (7d pace: $102 spend, 3 purchases — steady.)
- [x] **Only ONE campaign live:** `Retargeting Campaign – Bottom Of Funnel` (OUTCOME_SALES). Everything else PAUSED
  (Advantage+ traffic/MOF, Brand Awareness/TOF, and a stack of cavity-batten sales tests).
- [x] **Creative evidence — VIDEO beats STILL in-account:** the video retargeting ad = 2.10% CTR / 26.6× ROAS vs the
  static "Configurator Hero Ad D" = 0.59% CTR / 5.4× ROAS. (Small sample, retargeting not TOF — but points the same
  way as the strategy: motion is Craftons' scroll-stop. Statics = cheap support act, not the lead.)

### ⚠️ Meta read: retargeting is SUPPLY-constrained, not budget-constrained
- The 25× ROAS is a **harvester** — it only re-serves people who already visited (14k warm pool, ~$14/day). Pumping
  retargeting budget just raises frequency on the same pool → ROAS collapses. **Nothing is refilling the funnel** (all
  TOF/MOF paused). The unlock = fund **top-of-funnel** to grow the warm pool; retargeting then scales itself at high ROAS.
- **TOF plan (workshopped 2026-07-08, creative direction TBC with Lee):** launch a value-first Craft-Macro-style TOF
  video whose job is to *fill the pool*, not sell. Lead concept: **"Form-Strip Reveal"** (the money-shot). Keep
  retargeting ~as-is; put new spend into TOF (~$20/day recommended starting test). Awaiting Lee: concept + budget pick.

### CNC Cut account (existing, separate spend) — TIGHTENED
- [x] Paused $19/click "Industry Specific"; capped CPC ~$3.50; Search Partners/Display off; negatives added;
  match types already exact; Brand bidding reined in → baseline + checklist in `campaigns/adwords/cnc-cut-review-log.md`

### Infrastructure / security
- [x] **Google Ads creds rotated** (2026-06-23), placed in Vercel → `INTEGRATIONS.md` / `DESKTOP-TODO.md`
- [x] **Drive connector permission fix** — tracked `.claude/settings.json` allow-lists Drive tools
  (`mcp__*__*`). NOTE: permission changes only take effect on a **NEW session** (loaded at startup).

---

## ⏳ Pending / in progress
- [ ] **Meta TOF ad — decision + build.** Awaiting Lee: (a) concept [A Form-Strip Reveal ⭐ / B "site-bent radius is
  dead" / C number-hook / A+B test], (b) TOF budget [$10 / **$20** / $40 per day]. Then Claude writes the full brief
  (script, shot list, caption, cold-interest targeting) → Tia shoots → launch as a pool-filler beside retargeting.
- [ ] **Google Ads API Basic access** — application prepared (answers + PDF design doc sent). Lee to submit /
  awaiting Google (~3 business days). → `campaigns/adwords/api-access.md` + `api-tool-design.md`
- [ ] **Mirror Google Ads creds into THIS engine's env vars** (for `google-ads.mjs` to run here)
- [ ] **Delete the disabled old Google Ads secret** in Cloud Console (post-rotation tidy)

---

## ⏭ Next steps (in order)
1. **Submit the Basic-access application** (Lee) — answers + PDF are ready (`api-access.md` / `api-tool-design.md`).
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

---

## 📁 Document index
**Strategy / brand:** `CONTENT-PILLARS.md` · `SOCIAL-VOICE.md` · `inspiration/SWIPE-FILE.md` ·
`.claude/skills/craftons-design/BRAND.md` · `briefs/craft-macro-shoot-brief.md`
**Skill suite + memory:** `.claude/skills/{keyword-research,seo-content,positioning-angles,direct-response-copy,content-atomizer}/` ·
`brand/{voice-profile,audience,competitors,keyword-plan,assets}.md`
**AdWords:** `campaigns/adwords/` → `campaign-setup.md` · `keywords.md` · `negative-keywords.md` ·
`ad-extensions.md` · `ads/*` · `conversion-tracking.md` · `api-access.md` · `api-tool-design.md` ·
`cnc-cut-review-log.md`
**Meta Ads:** live account `act_1650412872259063` (read-only pulls via `META_ACCESS_TOKEN` in env) — state + TOF plan
tracked in the "Meta Ads (Craftons)" section above; see `INTEGRATIONS.md` B6 for creds.
**Setup / ops:** `SETUP.md` · `INTEGRATIONS.md` · `DESKTOP-TODO.md` · `CLAUDE.md` · `QUALITY-DOCTRINE.md`
