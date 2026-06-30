# Marketing engine — status & plan (READ THIS FIRST)

_Living handoff doc. Last updated 2026-06-30. Branch: `claude/elegant-ramanujan-ct2p85`._
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

### CNC Cut account (existing, separate spend) — TIGHTENED
- [x] Paused $19/click "Industry Specific"; capped CPC ~$3.50; Search Partners/Display off; negatives added;
  match types already exact; Brand bidding reined in → baseline + checklist in `campaigns/adwords/cnc-cut-review-log.md`

### Infrastructure / security
- [x] **Google Ads creds rotated** (2026-06-23), placed in Vercel → `INTEGRATIONS.md` / `DESKTOP-TODO.md`
- [x] **Drive connector permission fix** — tracked `.claude/settings.json` allow-lists Drive tools
  (`mcp__*__*`). NOTE: permission changes only take effect on a **NEW session** (loaded at startup).

---

## ⏳ Pending / in progress
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

## ❓ Open questions / decisions needed

### ✅ Resolved 2026-06-30 (with receipts)
- **Sitelink "Get a Quote" URL → `/pages/contact`.** Verified live on craftons.com.au: there is **no
  dedicated quote page** — the contact page *is* the quote path. Placeholder was correct; caveat removed
  in `ad-extensions.md`.
- **CNC Cut milling/engraving → NO.** cnccut.melbourne advertises **2D & 3D router cutting only**. →
  Added `milling / mill / engraving / engrave / engraver / laser` as negatives (`cnc-cut-review-log.md`).
- **Configurators — purchase vs quote → BOTH, lead-dominant (~19:1).** The configurators support online
  checkout (Radius Pro product page: "dispatched in 3 business days from checkout"; **23 purchases /
  $17.3k** tracked) but the dominant action is **lead/quote forms (443 tracked)**. Implication for the
  engine: keep **Purchase** Primary, but **"Submit lead form" is the main optimisation signal** — bid
  toward leads, not just purchases.
- **`file_download` conversion → demote Primary → Secondary.** Confirmed correct: don't optimise toward
  PDF-downloaders. (Manual change in Google Ads UI — flagged in next-steps until API write access lands.)

### ✅ Resolved by Lee 2026-06-30
- **Account structure → SEPARATE accounts.** Craftons is **not** in the CNC Cut account (`310-491-2421`).
  → The engine builds the new Craftons campaigns in **Craftons' own Google Ads account** (the one with the
  23 purchases + 443 lead forms / Shopify Google&YouTube + GA4). CNC Cut stays separate.
- **Call extension phone → `0411 689 166`.** Use the number published live on craftons.com.au so the ad
  matches the site (supersedes the old `0466 146 744`). Finalised in `ad-extensions.md`.

> **All open questions resolved.** Engine deployment is unblocked once Google Ads API Basic access lands
> (see Pending / Next steps) — build in Craftons' own account, optimise toward "Submit lead form".

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
**Setup / ops:** `SETUP.md` · `INTEGRATIONS.md` · `DESKTOP-TODO.md` · `CLAUDE.md` · `QUALITY-DOCTRINE.md`
