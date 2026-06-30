# Marketing engine — status & plan (READ THIS FIRST)

_Living handoff doc. Last updated 2026-06-30. Branch: `claude/creds-status-check-fzhcli`._
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

### Craftons AdWords — campaign DEPLOYED via the engine (PAUSED, 2026-06-30) 🚀
- [x] **Engine built the live campaign via the Google Ads API** — `tools/google-ads-launch.mjs`
  (atomic, all-or-nothing, validated then created). **Campaign ID `23983924746`**, status **PAUSED**
  (zero spend until Lee flips it to ENABLED in the UI).
- [x] Built exactly to spec & **verified by reading it back**: Search-only (Search Partners + Display
  OFF), **Manual CPC**, **$50/day**, geo = Melbourne 50km + Geelong + Surf Coast + Mornington (Presence),
  English. 3 ad groups (cpc cap $3.50), **39 keywords** (phrase+exact), **3 RSAs** (15 HLs each),
  **70 campaign negatives**, extensions: **4 sitelinks + 8 callouts + 2 snippet sets + 1 call**
  (call number **0485500227**, Lee-confirmed).
- [ ] **Lee to review in the Google Ads UI → flip campaign to ENABLED to go live.** (Then verify a
  test form-submit fires a conversion within day 1.)

### Craftons AdWords — source assets (built the campaign above)
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

### Google Ads API — ENGINE-CONNECTED (verified live 2026-06-30)
- [x] **Creds mirrored into THIS engine's env** — all six `GOOGLE_ADS_*` vars present & well-formed;
  OAuth refresh works (rotated client secret + refresh token valid).
- [x] **Basic access CONFIRMED** — the API read the **non-test** advertiser account 310-491-2421
  (AUD/Melbourne) and returned real spend/conversions. Test-access tokens can't read production, so
  this proves Basic access is granted. (Resolves the "Basic access pending" item below.)
- [x] **`tools/google-ads.mjs` built** — zero-dependency, **read-only** reporter
  (`whoami` / `accounts` / `report [days]` / `terms [days]`). Write/change mode (CONFIRM=1) is a
  deliberate next step, not yet built. → `campaigns/adwords/api-tool-design.md`
- [x] **Live read sanity-check:** account "Craftons Google Ads account" (310-491-2421) is running
  **Cavity Battens — Performance Max** (PAUSED): 84 conv / $1,171 / **$13.94 per conv** over 30 days.
- ✅ **Linkage decided (Lee, 2026-06-30):** keep `310-491-2421` **standalone** (not under the MCC).
  Reached by direct access; tool correctly sends no `login-customer-id`. The MCC stays unused for now.

### Infrastructure / security
- [x] **Google Ads creds rotated** (2026-06-23), placed in Vercel → `INTEGRATIONS.md` / `DESKTOP-TODO.md`
- [x] **Drive connector permission fix** — tracked `.claude/settings.json` allow-lists Drive tools
  (`mcp__*__*`). NOTE: permission changes only take effect on a **NEW session** (loaded at startup).

---

## ⏳ Pending / in progress
- [x] ~~Google Ads API Basic access~~ — **GRANTED & verified 2026-06-30** (read a live production account).
- [x] ~~Mirror Google Ads creds into THIS engine's env vars~~ — **done & verified** (all six present, working).
- [ ] **Build the write/change mode** for `google-ads.mjs` (add negatives, pause keywords, adjust
  bids/budget) behind a `CONFIRM=1` gate — read-only is built; writes are not.
- [ ] **Delete the disabled old Google Ads secret** in Cloud Console (post-rotation tidy — desktop).

---

## ⏭ Next steps (in order)
1. **Lee: review campaign `23983924746` in the Google Ads UI and flip it to ENABLED.** It's built and
   PAUSED — review the 3 ad groups / RSAs / keywords / negatives / extensions, then enable to go live.
   (Engine can flip it on too — just say so. Real spend starts the moment it's ENABLED.)
2. **Verify conversions fire** — submit a test lead form on the site and confirm the `form_submit`
   conversion records within a day.
3. **Set up the weekly-review routine** (Claude routine, web app) → run `google-ads.mjs report` weekly
   → auto-report + advice + propose negatives. The read-only tool is ready to wire now.
4. **CNC Cut:** reassess in a week vs the baseline (`cnc-cut-review-log.md`); add GA4-linked tracking if not attributing.
5. **Content production** (independent of ads): Tia shoots Craft Macro Session A; build out How-To Series shot lists.

---

## ❓ Open questions / decisions needed (answer these to unblock)
- ~~Account structure~~ **DECIDED (Lee, 2026-06-30):** CNC Cut and Craftons are **separate accounts**.
  The engine works on the **Craftons ad account `310-491-2421` only** for now (CNC Cut is out of scope
  here). The Craftons Marketing MCC (`275-347-3695`) stays **unused/standalone** — `310-491-2421` is
  reached by direct access and that's fine; revisit linking it under the MCC only if a reason arises.
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
- **Google Ads `login-customer-id` gotcha:** the advertiser (310-491-2421) is reached by **direct
  user access**, not through the manager MCC. Sending the manager as `login-customer-id` → 403
  `USER_PERMISSION_DENIED`. Query the advertiser directly (no header) unless/until it's linked under
  the MCC. `tools/google-ads.mjs` defaults to no header; `GOOGLE_ADS_USE_LOGIN_CUSTOMER_ID=1` to send it.
- **Verifying Basic vs Test access:** Test-access dev tokens can only read **test** accounts. If
  `google-ads.mjs whoami` returns a non-test account with real data, Basic access is granted.

---

## 📁 Document index
**Strategy / brand:** `CONTENT-PILLARS.md` · `SOCIAL-VOICE.md` · `inspiration/SWIPE-FILE.md` ·
`.claude/skills/craftons-design/BRAND.md` · `briefs/craft-macro-shoot-brief.md`
**Skill suite + memory:** `.claude/skills/{keyword-research,seo-content,positioning-angles,direct-response-copy,content-atomizer}/` ·
`brand/{voice-profile,audience,competitors,keyword-plan,assets}.md`
**AdWords:** `campaigns/adwords/` → `campaign-setup.md` · `keywords.md` · `negative-keywords.md` ·
`ad-extensions.md` · `ads/*` · `conversion-tracking.md` · `api-access.md` · `api-tool-design.md` ·
`cnc-cut-review-log.md` · **`tools/google-ads.mjs`** (read-only reporter) ·
**`tools/google-ads-launch.mjs`** (campaign launcher — built the live campaign 23983924746)
**Setup / ops:** `SETUP.md` · `INTEGRATIONS.md` · `DESKTOP-TODO.md` · `CLAUDE.md` · `QUALITY-DOCTRINE.md`
