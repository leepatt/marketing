# Session refresh — continue building the Meta ads marketing agent

Continuing work in `/home/user/marketing` (repo `leepatt/marketing`), with code in
`leepatt/cnccut-app`. Both on branch **`claude/marketing-agents-setup-qamq2f`** — all work is
committed and pushed. Goal of this session: **continue building the Craftons Meta ads agent.**

## Where things stand

**Scope locked (Lee):** Craftons only · **Radius Pro only** to start · human approves first, autonomy
earned via a 5-rung ladder · code lives in `cnccut-app` · lightweight data layer (no Airbyte /
ClickHouse — Neon + `marketing_metrics_cache` already does it) · **AI avatars approved as presenters**
(banned as testimonial-givers, ACL s18/s29(1)(e)) · **$2,000/month ceiling** · optimise on a combined
high-intent event, score on revenue.

**Built and verified in `cnccut-app`** (Phases 1, 2, 4, 5 of the bible's plan):
- `tools/_meta-policy.mjs` — all guardrails as pure, credential-free functions
- `tools/meta-ads.mjs` — `report` · `doctor` · `evaluate` · `winners` · `research` · `check-batch` ·
  `upload-image` · `create-creative` · `propose` · `apply`
- `app/api/cron/meta-ads/route.ts` — weekly cadence (Sun 22:00 UTC), wired in `vercel.json`
- Verified 2026-08-03: **13/13 guardrail self-checks pass**, `tsc --noEmit` clean, `report` /
  `winners` / `research` all return real data from the live account.

**Key findings from the live account (these overturned earlier assumptions):**
- **Meta is NOT a cold start.** 30 days: $1,977.82 spend, 21 results, $17,285 revenue, **~8.7× ROAS**.
  Shopify's referrer attribution undercounts Meta by >10× — always read Meta from Meta.
- **July collapse diagnosed.** Spend scaled ~13× (22–28 Jul), clicks rose ~150×, results went to
  **zero**. Causes: optimised on `AddToCart` (too high in funnel), creative hand-segmented by trade
  (pre-Andromeda), budget scaled in one step. Account is **currently paused**.
- **Best ad: "Retargeting – Configurator Hero Ad D" at $6.05/result.** Worst: "AD5 Chippies" at
  $758.74. A 125× spread — independent evidence for making the configurator the creative engine.
  (Caveat: the $6.05 rests on $12 of spend. Direction is trustworthy, precision isn't.)
- **Gross margin measured at 52.4%** (Xero, Feb–Jul 2026) → break-even CAC **~$322**, break-even
  volume ~6.2 orders/month.

**Phase 0 (tracking) — essentially green:**
- ✅ Advanced Matching enabled 2026-08-03, all 11 params
- ✅ Shopify data sharing already "Optimized" (highest tier); CAPI + browser both live
- ✅ No rogue pixels — Customer events is clean
- ✅ **Duplicate-Purchase alarm was a false positive.** Two real orders in one hour produced 2 browser
  + 2 server events = exactly 1 of each per order. Meta's `/stats` endpoint reports *pre-dedup*
  counts, so 97-events-vs-36-orders was never like-for-like. **Nothing to fix.**

## Next steps

1. **Create the combined custom conversion** — `InitiateCheckout` OR `Purchase` (~53 events/week,
   clears Meta's ~50/wk learning threshold). Last Phase 0 item. Additive, reversible, nothing live.
   Lee was asked and hadn't answered yet — confirm before creating.
2. **Check Event Match Quality > 7** — Advanced Matching went on 2026-08-03, needs 24–48h to settle.
3. **Phase 3 — creative production.** The tooling exists; the assets don't. In order:
   configurator capture pipeline (Playwright over Radius Pro) → static templates → a first batch of
   15–20 through `check-batch` → one properly structured ad set.
4. **Blocked on Lee:** before/after site photography (bog-and-sanded curve vs parts arriving cut) —
   the only creative family that can't be assembled from existing assets, and likely the strongest angle.

## Files to open (read these, don't re-derive)

**In this repo (`/home/user/marketing`):**
- `campaigns/meta/META-ADS-AGENT-BIBLE.md` — **the main doc.** Design, doctrine, the Craftons
  translation, phased build plan with items ticked. Start here.
- `campaigns/meta/conversion-tracking.md` — Phase 0 step-by-step, with current status
- `campaigns/meta/step1-duplicate-purchase.md` — the resolved false alarm; record only, conclusions superseded
- `STATUS.md` — living status across the whole marketing engine
- `QUALITY-DOCTRINE.md` — the anti-slop rules that constrain all creative
- `brand/audience.md` — Radius Pro pain points, from real customer contact (beats scraped research)
- `brand/keyword-plan.md` — proven converting language ("bendy ply", "curved bench seat")

**In `cnccut-app`** — ⚠️ **not in a fresh session's scope. Run `add_repo` for `leepatt/cnccut-app`,
then `git clone --depth 1 ... /workspace/cnccut-app` and `git checkout claude/marketing-agents-setup-qamq2f`:**
- `tools/_meta-policy.mjs` — every guardrail and its reasoning
- `tools/meta-ads.mjs` — the agent
- `tools/README.md` — conventions all tools follow
- `app/api/cron/meta-ads/route.ts` — the cadence
- `content-engine/` — Remotion, Playwright capture, brand kit, real photography (Phase 3 lives here)
- `docs/marketing/APP-NOTES.md` — env var names; match these, don't invent

**In `craftons-curves-calculator`** — also needs `add_repo` + clone if touching tracking:
- `src/app/lib/meta-tracking.ts` — the configurator's pixel/CAPI code. Well built, properly
  deduplicated by `event_id`. Fires ViewContent, ConfiguratorStarted, AddToCart, InitiateCheckout.

## Carried-over data

**IDs (used constantly, not written in any single file):**
- Pixel / dataset: `677437638374055` ("Craftons Web") · Business: `1006792137511423` ("Craftons")
- Ad account: `act_1650412872259063` · Second dataset: `993965426717610` ("Craftons Ads API", app-type)
- Shopify: `5e2910-9d.myshopify.com` · Radius Pro Shopify product id `8464537125042`

**Graph API recon recipes** (these were ad-hoc scripts in an ephemeral scratchpad — they're gone, but
they're one-liners. `META_ACCESS_TOKEN` is in the session env; token type SYSTEM_USER, scopes
`ads_management`, `ads_read`, `business_management`):

```
GET /v23.0/{pixel}?fields=enable_automatic_matching,automatic_matching_fields,last_fired_time
GET /v23.0/{pixel}/stats?aggregation=event&start_time=YYYY-MM-DD
GET /v23.0/{pixel}/stats?aggregation=event_source|host&start_time=...&event=Purchase
GET /v23.0/{pixel}/da_checks            → diagnostics
GET /v23.0/{business}/system_users      → found "Conversions API System User"
```
Auth header, never the URL: `Authorization: Bearer $META_ACCESS_TOKEN`.

**Baselines to compare against:**
Radius Pro 365d: 202 orders / $124,164 / **$614.67 AOV** (60% of all orders).
Store: ~35–39 orders/month, ~5× YoY growth. Pixel 30d events: ViewContent 78,980 · AddToCart 920 ·
ConfiguratorStarted 812 · **InitiateCheckout 193** · Purchase 97. Traffic 72% iPhone.
