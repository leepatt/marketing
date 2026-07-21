# Craftons AdWords — change log (engine writes)

_Audit trail of changes `tools/google-ads.mjs` applied to the live Craftons account (3104912421),
each human-approved (CONFIRM=1). Read this for the weekly routine._

## 2026-07-02 — first engine writes
**Diagnosis:** "Craftons – Customised Building Products" (Search, $50/day, Manual CPC) barely serving —
7d $6.99 / 2 clicks. Impression share 36%; **0% lost to budget, 64% lost to rank** → bids/QS too low.
Compounded by low search volume on niche curved-product terms.

**Changes (Lee-approved):**
- **Max CPC $3.50 → $6.00** on all 3 ad groups (Radius Pro, Curved Bench Seat/Formwork, Curved
  Architraves) — to win more of the auctions being lost on Ad Rank.
- **Added location targets: Sydney metro (1000286) + Brisbane metro (1000339)** — alongside existing
  Melbourne radius + Geelong + Surf Coast + Mornington.

**Verified live:** bids now $6.00 ×3; campaign locations now include Sydney + Brisbane.

**Watch (next few days):**
- Spend should climb (was using only $7 of $50/day). Check daily spend vs the $50 cap.
- Impression share should rise and **rank-lost IS** should fall as bids win more auctions.
- Cost-per-lead — with $6 CPC, watch it stays sane vs job value.
- **Interstate leads:** confirm Sydney/Brisbane leads actually convert given **freight on bulky
  curved products** — if freight kills the economics, pull those geos back.

## 2026-07-08 — split out a dedicated Curved Architraves campaign (hero push)
**Why:** week-2 data showed the single campaign spending ~$65/day with ~1 conv — architraves the only
converter ("curved architrave" → 1 conv @ $9), good margins, upgraded site configurator. Budget + geo
are per-campaign, so a split was required to give architraves its own budget/geo.

**Built (Lee-approved, created PAUSED pending review):**
- **Craftons – Curved Architraves** (campaign id 24006679434): **$100/day** dedicated budget, Search only
  (Partners + Display OFF), Manual CPC, max CPC $6, presence-only geo.
- Geo: Melbourne + Geelong + Surf Coast + Mornington + **Sydney + Brisbane** (national test w/ new site).
- 1 ad group (Curved Architraves), **47 keywords** (generic + moulding synonyms + **Intrim / Australian
  Moulding & Door** Exact-match conquesting), **21 negatives**, 1 RSA (under review). See
  `architraves-keyword-expansion.md`.

**✅ Executed / LIVE 2026-07-08 (Lee approved "make ads live"):**
- New **Craftons – Curved Architraves** campaign **ENABLED** ($100/day).
- Old "Customised Building Products": **Curved Architraves ad group PAUSED**; **Sydney + Brisbane
  removed** → Radius Pro + Formwork now **local only** (Melbourne + Geelong + Surf Coast + Mornington),
  $50/day.
- Total live spend now **~$150/day** ($100 architraves + $50 ply/formwork).
- Note: **Cavity Battens Performance Max is PAUSED** ($0 spend) — that's why it dropped to $0 earlier.
  It was the account's main converter; flag to Lee whether that pause was intentional.

**Watch (next few days):**
- New architraves ad enters **review** — confirm it gets approved (was "under review" at build).
- Architraves spend/conversions vs the $100 budget; is the competitor (Intrim/AMDC) conquesting working?
- Ply/formwork now local — spend should drop and waste (interstate) should stop.


## 2026-07-10 — architrave conversion diagnosis + geo re-weight
**Corrected earlier "we're blind" assumption — tracking works:**
- Leads = "Craftons (web) form_submit" (PRIMARY, 53 in 30d). Purchases = "Google Shopping App Purchase"
  (PRIMARY, 5 in 30d, via the Shopify Google&YouTube app). Architrave campaign activity IS attributed
  (14d: 24 page views, 20 view-item, 1 form-start). Attribution is fine.
- Old "Craftons (web) purchase" is HIDDEN (superseded by the Shopify app purchase) — harmless. file_download
  already non-primary.

**The real bottleneck = the configurator/page, not tracking or the ads.** Architrave ad clicks land and
VIEW the product (20 view-item) but **0 add-to-cart, 0 checkout, 0 purchase, 0 form-submit** (only 1
form-start). Site-wide add-to-cart ~3%, CR ~1-2%. The clicks are qualified; they bounce at the configurator.

**Reframe:** architraves is lumpy/high-value — 6 orders/90d, single orders $2.5k, 7-week dry spells; 4 orders
in the last 3 weeks (since the configurator upgrade). At ~$6 CPC needing ~30-50 clicks/order, "0 conv in 20
clicks / 3 days" is statistically EXPECTED, not failure. High AOV/margin tolerates ~$200-300 CPA.

**Changes applied (Lee-approved, 3 asks):**
- (2) Re-weight to Victoria: Sydney + Brisbane **bid_modifier 0.30 (-70%)** on the architrave campaign
  (home was starved — 90% of spend interstate, 0 conv). Negatives added: **skirting, bunnings**.
- (1) Tracking audited = working (above); no blackout. Minor optional tidy only.
- (3) Funnel confirmed: leak is the **architrave configurator page** (view -> no cart).

**Next levers (where the conversions come from):**
- **Improve the architrave configurator page** (design->instant price->order friction; trust/proof;
  finished-arch gallery). Website/configurator job — the clicks are landing, the page must close them.
- **Retarget** architrave product viewers (warm; ~20 already).
- Give it 3-4 weeks with Victoria focus + tracking on before judging.
