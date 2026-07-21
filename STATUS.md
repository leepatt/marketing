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

### Inspiration → image-gen reference pipeline (NEW 2026-06-30)
- [x] **`tools/video-frames.py`** — videos → deduped reference frames (1 frame/0.5s, perceptual-hash dedupe).
- [x] **`tools/ig-collect.mjs`** — Playwright collector: pulls a profile's images+videos via a saved login
  session. **Runs on desktop only** (cloud env + IG block headless/datacenter — verified). Reusable per brand.
  Default output = Drive `01 Inspiration` mount. Autonomous via `tools/ig-collect.bat` +
  `tools/install-schedule.cmd` (weekly Windows Task Scheduler job). Caveats: PC on, periodic IG re-login.
- [x] **SessionStart hook** (`.claude/hooks/session-start.sh`) auto-installs ffmpeg + media tooling every
  web session (fixes ffmpeg not persisting). **Activates once merged to default branch.**
- First target: **@modernconcreteco** → Drive `01 Inspiration/modernconcreteco/`. Reference/mood use only.
- See `tools/README.md` for the full loop. Open: image-engine (`pipeline/`) consumes prompts, not photos —
  inspiration feeds the `craftons-design` prompt/style layer + a manifest, not `render.mjs` directly.

### Infrastructure / security
- [x] **Google Ads creds rotated** (2026-06-23), placed in Vercel → `INTEGRATIONS.md` / `DESKTOP-TODO.md`
- [x] **Drive connector permission fix** — tracked `.claude/settings.json` allow-lists Drive tools
  (`mcp__*__*`). NOTE: permission changes only take effect on a **NEW session** (loaded at startup).

---

## ⏳ Pending / in progress
- [x] **Google Ads API Basic access GRANTED (2026-06-30)** — dev token approved on MCC **275-347-3695**
  (15k ops/day). Engine can reach the API from the cloud (verified). `tools/google-ads.mjs` built
  (read-only: `accounts` + `report`); writes pending behind CONFIRM=1 after connect.
- [x] **Creds mirrored + CONNECTED (2026-07-02)** — `google-ads.mjs accounts`/`report` verified read-only.
- [x] **Craftons account CONFIRMED = `3104912421`** ("Craftons Google Ads account", 84 conv/30d). MCC
  `2753473695` = "Craftons Marketing". ⚠️ The advertiser is reached **directly, NOT via the MCC** (not
  linked in the API) — tool now auto-falls-back login-customer-id. Optional: set
  `GOOGLE_ADS_LOGIN_CUSTOMER_ID=3104912421`, or link the account under the MCC in Google Ads.
- [x] **Engine now creates campaigns.** First writes (2026-07-02): raised CPC $3.50→$6 + added Sydney/
  Brisbane on the one campaign. Week-2 data showed ~$65/day, ~1 conv — architraves the only converter.
- [x] **Restructured into 2 campaigns + went LIVE (2026-07-08, Lee-approved)** → `craftons-change-log.md`:
  - **Craftons – Curved Architraves** (NEW hero) — **$100/day**, national (Melb+shires+Sydney+Brisbane),
    47 keywords incl. **Intrim / Australian Moulding & Door conquesting**, built PAUSED then enabled.
  - **Craftons – Customised Building Products** — now **Radius Pro + Formwork only**, **$50/day**, **local**
    (architraves ad group paused, Sydney/Brisbane removed).
  - **~$150/day total live.** `google-ads.mjs` now has CONFIRM-gated `bids` + `add-geo`; full campaign
    creation done via script (in change log).
  - **Watch:** new architrave ad approval; architraves conversions vs $100 budget; ⚠️ **Cavity Battens
    PMax is PAUSED** (was the main converter — confirm intentional).
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


## 2026-07-21 — decisions & refocus (Lee)
- **Cavity Battens DISCONTINUED** — no longer manufacturing. Do **NOT** un-pause the Cavity Battens
  Performance Max; it stays off. Wind down anything advertising cavity battens; archive the Shopify
  product once remaining inventory clears. (This was the account's former best converter — accept that
  it's gone; the account now has no active paid converter, which reinforces the demand-gen + content plan.)
- **Architraves → demand-gen, not more search.** Build a Performance Max / Demand-Gen campaign fed by
  finished-arch creative; keep the small architrave *search* campaign as a capture layer only.
- **Architrave page:** let Microsoft Clarity gather data (installed 2026-07-21), do the cheap
  image-surfacing + trust lines, retarget viewers, give it 3–4 weeks. No restructure. → `architrave-page-cro-audit.md`.
- **PRIMARY FOCUS = the 2-month build to launch (~late Sept 2026).** Deliberate build of all the engine
  tools + launch-readiness, not week-to-week ad tinkering. See the phased plan (Drive `02 Strategy/
  Craftons-Marketing-Engine-Plan.md`) — consolidate into an 8-week roadmap.
