# Marketing engine — status & plan (READ THIS FIRST)

_Living handoff doc. Last updated 2026-08-03. Branch: `claude/google-ads-report-4wzlav`._
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

### Craftons AdWords — campaigns LIVE since 1 Jul 2026 ✅
- [x] **Campaigns are running** (confirmed via API 2026-08-03): "Craftons – Customised Building
  Products" (live 1 Jul, $50/day) + "Craftons – Curved Architraves" (live 8 Jul, $100/day).
- [x] **First live report pulled** → `campaigns/adwords/reports/2026-08-03-google-ads-report.md`
  - 1 Jul–2 Aug: **$1,601.71** spend · 316 clicks · CPC $5.07 · **4 conv** (3 leads + 1 purchase
    $1,265) · **ROAS 0.79x** · $400/conv
  - ⚠️ **Cavity Battens PMax was paused 29 Jun** — it was doing **7.7x ROAS ($1,171 → $9,044)** in
    June and climbing 5 months straight. Biggest open revenue lever. **Needs a decision from Lee.**
  - ⚠️ **69% of spend on QS 1–3 keywords** — root cause of the ~$5.80 CPCs (QS-7 keyword clicks $2.98)
  - ⚠️ **Radius Pro ad group: $555, 97 clicks, 0 conversions** — buying flat-bendy-sheet intent for a
    cut-to-size product (the exact risk `keyword-plan.md` flagged)

### Google Ads API — WORKING ✅ (Basic access evidently granted)
- [x] Creds are **already mirrored into this engine's env** (all 6 vars present and valid)
- [x] **`tools/google-ads.mjs` built** — read-only GAQL reporting client (no write path exists)
  - `node tools/google-ads.mjs accounts | report --days 30 | raw "<GAQL>"`
- [x] **Account structure ANSWERED:** MCC Craftons Marketing (275-347-3695) has **no child accounts**.
  Craftons advertiser **310-491-2421** is granted **directly** — must omit `login-customer-id`
  (tool auto-handles). **CNC Cut is NOT in this account** and is unreachable with these creds.

### Craftons AdWords — campaign assets (built earlier)
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
- [ ] **Write mode for `google-ads.mjs`** — CONFIRM=1-gated ops (add negatives, pause keywords, adjust
  bids/budgets). Read side is done; no write path exists yet.
- [ ] **Delete the disabled old Google Ads secret** in Cloud Console (post-rotation tidy)

---

## ⏭ Next steps (in order)
1. 🔴 **DECIDE: restart Cavity Battens PMax?** Paused 29 Jun at 7.7x ROAS and climbing. Biggest single
   revenue lever in the account. Deliberate pause, or accidental casualty of the search launch?
2. **Cheap fixes** (~$110/mo recovered): add negatives (`banquette`, `booth`, `seating`, `beading`,
   `door`, `kit`, `circle`, `scallop`, `inch`, `formatube`); **stop bidding on competitor brand
   `intrim`** ($28.54, QS 1, 0 conv).
3. **Fix Radius Pro** — pause the POOR ad; rewrite ads/page to answer "bendy ply" intent directly
   ("we cut the curve — no bending required"). $555 / 0 conv can't continue.
4. **Rebalance budget** — Architraves has $100/day and spends $16 (68% lost to rank, 0% to budget);
   the main campaign loses 20.55% to budget. Move it. Also **cap max CPC ~$4.00** (Manual CPC at $5.63).
5. **Quality Score program** — 69% of spend on QS 1–3. Tighter ad-group → landing-page match.
6. **Set up the weekly-review routine** now that the report tool works → auto-report + advice.
7. **CNC Cut:** reassess vs baseline (`cnc-cut-review-log.md`) — note it's **not** reachable via the
   current API creds, so this stays manual for now.
8. **Content production** (independent of ads): Tia shoots Craft Macro Session A; How-To Series shot lists.

---

## ❓ Open questions / decisions needed (answer these to unblock)
- 🔴 **Was pausing Cavity Battens PMax deliberate?** (7.7x ROAS in June, then $0 from 1 Jul.)
- ~~**Account structure**~~ — ANSWERED 2026-08-03: Craftons = `310-491-2421`, granted directly (not via
  the MCC, which has no children). **CNC Cut is a separate account**, not reachable with these creds.
- **Sitelink "Get a Quote" URL** — confirm the real contact/quote page (placeholder `/pages/contact`).
- **Lead value:** what's a qualified lead worth? Forms currently carry a $1 placeholder, so bidding
  optimises for lead *count*, not quality.
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
- **Don't swap a proven campaign for an unproven one.** PMax at 7.7x ROAS went off the same week
  search went on. Overlap them next time — let the new one prove itself before killing the earner.
- **`login-customer-id` is only valid for accounts that actually sit under that MCC.** Sending it for a
  directly-granted account returns `USER_PERMISSION_DENIED` — misleading, looks like an access problem.
- **`metrics.conversions` counts whatever is Primary at the time** — historic PMax "conversions" are
  inflated by page-view actions that were primary back then. **Segment by
  `segments.conversion_action_name` and read purchases/revenue directly** for real performance.
- **Quality Score is the CPC lever, not bid caps.** QS 1 keywords cost ~$5.90; the one QS 7 costs $2.98.

---

## 📁 Document index
**Strategy / brand:** `CONTENT-PILLARS.md` · `SOCIAL-VOICE.md` · `inspiration/SWIPE-FILE.md` ·
`.claude/skills/craftons-design/BRAND.md` · `briefs/craft-macro-shoot-brief.md`
**Skill suite + memory:** `.claude/skills/{keyword-research,seo-content,positioning-angles,direct-response-copy,content-atomizer}/` ·
`brand/{voice-profile,audience,competitors,keyword-plan,assets}.md`
**AdWords:** `campaigns/adwords/` → `campaign-setup.md` · `keywords.md` · `negative-keywords.md` ·
`ad-extensions.md` · `ads/*` · `conversion-tracking.md` · `api-access.md` · `api-tool-design.md` ·
`cnc-cut-review-log.md` · **`reports/`** (live performance reports)
**Tools:** `tools/google-ads.mjs` — read-only Google Ads API reporting client
**Setup / ops:** `SETUP.md` · `INTEGRATIONS.md` · `DESKTOP-TODO.md` · `CLAUDE.md` · `QUALITY-DOCTRINE.md`
