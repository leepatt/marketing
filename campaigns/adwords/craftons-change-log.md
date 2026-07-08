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
