# Brief 02 — Meta Ads (Facebook / Instagram)

_Depends on Brief 01 (Foundation). Mirrors the Google Ads module's pattern._

---

## 1. Goal

A Meta Ads module in the cockpit that (a) **reports** Facebook + Instagram ad and organic-insight
performance, and (b) **drafts campaigns/ad sets/creatives for human approval** — never spending or
launching without Lee/Jake approving. This is the Meta counterpart to the Google Ads dashboard, and
it reuses the existing `tools/meta-ads.mjs` (which already exists with a `CONFIRM=1` guardrail).

## 2. Why it exists

We're about to run paid on Meta (retargeting configurator visitors first, then awareness). Manual
Ads Manager review is slow and we spent blind on Google before tracking existed — the lesson is
**instrumented, human-gated, in-cockpit**. This tool catches wasted spend fast and keeps creative +
targeting in sync with our content/keyword plan.

## 3. Users & control model

Internal (Lee/Jake). **Read by default.** Any write (create/edit campaign, ad set, creative, budget,
pause/enable) is proposed in the UI Approval drawer and only executes with `CONFIRM=1` after approval.
A daily budget cap is enforced; no autonomous spend increases.

## 4. Inputs

**Synced brand docs (`docs/marketing/`):**
- `brand/keyword-plan.md` — the paid + SEO plan; confirmed converters ("bendy ply", "curved bench
  seat"); Radius Pro is the product, not flat sheets.
- `brand/audience.md`, `brand/competitors.md` — targeting + positioning.
- `SOCIAL-VOICE.md` + `craftons-design/BRAND.md` — creative voice/visual rules (note: **ad tone ≠
  brand-caption tone** — ads use direct CTAs).
- `campaigns/adwords/conversion-tracking.md` — Craftons Shopify tracking is verified solid (Purchases
  + lead forms). Mirror that instrumentation thinking for Meta (Pixel/CAPI).
- `campaigns/adwords/ads/*`, `negative-keywords.md` — existing ad copy + exclusions to reuse.

**Live data / APIs:**
- **Meta Graph + Marketing API** via `tools/meta-ads.mjs`. Env: `META_ACCESS_TOKEN`,
  `META_AD_ACCOUNT_ID`, `META_APP_ID`, `META_APP_SECRET`, `IG_BUSINESS_ACCOUNT_ID` (verify which the
  existing script actually uses — reuse those names).
- **Shopify** (connected) for purchase/lead attribution context (ROAS sanity vs. Xero).

## 5. MVP vertical slice

**A weekly Meta performance report in the cockpit, plus one human-approved draft action.**

1. `tools/meta-ads.mjs report` pulls last 7/30 days: spend, impressions, reach, clicks, CTR, CPC,
   conversions/leads, cost-per-result, ROAS, by campaign → ad set → ad. Also IG organic insights
   (reach, saves, shares, profile visits) if the token allows.
2. Report writes a `runs` row + a Markdown/JSON summary; the Meta Ads page renders KPI tiles + a
   drill-down table, with "top wasted audiences/placements" and "underperforming creatives" flagged.
3. One write path wired end-to-end as the approval proof: **pause an underperforming ad** (or add an
   audience exclusion). The UI proposes it → Approval drawer → `CONFIRM=1` executes → logs the change.

## 6. Backend — `tools/meta-ads.mjs`

Extend the existing script (don't rewrite). Subcommands:
- `report [--days 7|30]` — read-only performance + insights (default).
- `draft-campaign --brief <file>` — generate a campaign/ad set/creative spec (objective, audience,
  placements, budget, copy from voice docs) → outputs a proposed payload, **does not create**.
- `apply --change <id>` — execute an approved change; requires `CONFIRM=1`. Covers create/edit/pause.
Guardrails: budget cap check before any spend change; dry-run prints the diff without `CONFIRM=1`.

## 7. Frontend — Meta Ads page

- KPI header (spend, results, cost/result, ROAS, CTR) with 7/30 toggle.
- Campaign → ad set → ad table with sort + status; flags for wasted spend / weak creative.
- Creative preview cards (image/video + primary text + headline) pulled from the account.
- Approval drawer for every proposed change; Run panel to trigger a fresh `report`.
- "Draft new campaign" flow: pick objective + audience + product → preview spec → send to approval.

## 8. Data model additions

`meta_campaigns_cache`, `meta_creatives`, plus reuse shared `runs`, `approvals`, `metrics_cache`.

## 9. Post-MVP backlog

- Retargeting audiences off configurator visitors (the priority-1 paid play) + Pixel/CAPI check.
- Creative variants pulled from the Image/Video Studio (Brief 03) and Config Asset Creator (Brief 04).
- A/B test tracking; budget-shift recommendations; weekly auto-digest via cron → Overview card.
- Cross-channel view: Meta + Google Ads spend/ROAS side by side (shared with Google module).

## 10. Guardrails, safety, cost

Read-only default; `CONFIRM=1` for writes; daily budget cap; every change logged to `approvals`.
Never launch spend without verified conversion tracking on the destination (Shopify is instrumented;
confirm Meta Pixel/CAPI before enabling purchase-optimised campaigns).

## 11. MVP acceptance criteria

- [ ] `report` renders real last-7/30-day Meta numbers in the cockpit.
- [ ] Wasted-spend / weak-creative flags appear.
- [ ] One change (pause ad / add exclusion) goes proposal → approval → `CONFIRM=1` → logged.
- [ ] No secrets in logs; brand/voice pulled from `docs/marketing/`.

## 12. Open questions

- Is Meta Pixel/CAPI verified on the Craftons site yet (gate for purchase-optimised spend)?
- Confirm which env vars `meta-ads.mjs` currently expects.
- Starting budget + per-platform split vs. Google Ads?

---

## Kickoff prompt (paste into a fresh cnccut.app session)

> Foundation (Brief 01) must already be built and merged — if `docs/marketing/` doesn't exist, stop
> and flag it. Open and read the full brief `docs/marketing/dashboard-briefs/02-meta-ads.md` plus the
> shared conventions in `docs/marketing/dashboard-briefs/01-foundation-cockpit-shell.md` and
> `docs/marketing/APP-NOTES.md`, then build the **Meta Ads module** in the marketing cockpit.
> Extend the existing `tools/meta-ads.mjs` (keep its `CONFIRM=1` guardrail); do not rewrite it. Ship
> the MVP slice: a weekly Meta report (spend/results/ROAS/CTR by campaign→ad set→ad + IG insights)
> rendered on a `/marketing/meta` page with wasted-spend flags, plus ONE write path (pause ad / add
> exclusion) going through the shared Approval drawer → `CONFIRM=1` → logged. Pull voice/targeting
> from `docs/marketing/`. Read-only by default; never spend or launch without approval. New branch,
> logical commits.
