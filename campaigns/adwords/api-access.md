# Google Ads API — get out of Test access + run it from the engine

_Plan for moving from manual AdWords to engine-run (Claude reports + proposes, Lee approves)._

## Step 1 (Lee) — apply for Basic access
The dev token is **Test access** (can't touch the live account). Apply for **Basic** (15,000 ops/day):
1. Sign into the **manager (MCC)**: Craftons Marketing **275-347-3695**.
2. Wrench (**Tools & Settings**) → **Setup → API Center** (MCC-only).
3. Find the developer token → **Apply for Basic access**.
4. Form: company `craftons.com.au`; use case = "internal tool to manage our own Google Ads account —
   reporting + campaign management"; accept API Terms + Required Minimum Functionality.
5. Submit → Google reviews ~**1–3 business days** (may ask a follow-up).
6. When granted, the **rotated creds work against the live advertiser account** (310-491-2421 under MCC).

## Step 2 (Claude) — build the engine's Google Ads tool
Once Basic access lands, build `tools/google-ads.mjs` here (official Google Ads API + rotated creds
from env, never committed):
- **Report mode (read-only, default, safe):** last-7-days performance, search terms, wasted spend,
  cost-per-lead by ad group/keyword → the weekly report + advice.
- **Change mode (behind a CONFIRM gate):** add negatives, pause losing keywords, adjust bids/budget,
  create/edit ads — only on explicit approval.

**Dependency:** the Google Ads creds must be in **this engine's environment variables** for the tool
to run here (the "mirror to the cloud environment" item still open from the 2026-06-23 rotation —
they're currently in Vercel). Env vars needed: `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`,
`GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID`,
`GOOGLE_ADS_LOGIN_CUSTOMER_ID`.

## Control model (real money — guardrail)
- Claude **reports + recommends automatically** (read-only).
- **Changes need Lee's approval** before they're pushed (CONFIRM=1 guardrail, like `meta-ads.mjs`).
  Claude proposes → Lee approves → tool applies. Loosen later once proven.

## Step 3 — wire the weekly routine
Post-launch routine runs the report tool weekly → summary + recommended changes → Lee approves →
Claude applies.

## Status
- ☑ **Basic access GRANTED 2026-06-30** — Developer Token approved on MCC **275-347-3695**
  (15,000 ops/day). Engine verified it can reach the Google Ads API endpoint from the cloud.
- ☑ **`tools/google-ads.mjs` built (read-only)** — `accounts` + `report` commands; `google-ads-api`
  dep added. Writes (deploy/negatives/bids) to be added behind CONFIRM=1 after we connect.
- ☐ **Google Ads creds mirrored into this engine's env vars** (Lee — into the environment's secret
  store, persists across sessions; not repo/chat). Vars: see `## Env vars needed` below.
- ☐ **Confirm the Craftons advertiser customer id** — docs conflict (design doc says 310-491-2421;
  STATUS labelled that CNC Cut). Resolve empirically: `node tools/google-ads.mjs accounts` lists
  accounts by name + 30-day conversions; pick the one with Craftons' ~23 purchases + 443 leads.
- ☐ Weekly routine wired (after launch + access)

## Env vars needed (set in the environment's secret store)
`GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`,
`GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_LOGIN_CUSTOMER_ID` (=2753473695),
`GOOGLE_ADS_CUSTOMER_ID` (=3104912421, the Craftons advertiser — confirm via `accounts` first).

> **⚠️ Source of truth = Vercel** (cnccut-app project → Settings → Environment Variables), holding the
> **post-2026-06-23 rotation** values. The local cnccut-app `.env` is **STALE/revoked — do NOT copy
> creds from it** (you'd grab the revoked client secret + refresh token and auth would fail). Copy the
> 4 secrets from Vercel straight into this environment's variable settings (dashboard → dashboard,
> never via chat). Confirmed by the old session's `creds-mirror-handoff.md`.
