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
- ☑ **Basic access GRANTED** — verified live 2026-06-30: the API read the **non-test** advertiser
  account (310-491-2421, AUD/Melbourne) and returned real spend/conversions. A Test-access token
  cannot read a production account, so this confirms Basic access. (`node tools/google-ads.mjs whoami`.)
- ☑ **Google Ads creds mirrored into this engine's env vars** — all six present, OAuth refresh works
  (rotated client secret + refresh token valid), dev token reaches the live account.
- ☑ `tools/google-ads.mjs` built (Claude) — **read-only** reporter (whoami / accounts / report / terms).
  Write/change mode (CONFIRM=1 gate) still TODO as a separate, deliberate step.
- ☐ Weekly routine wired (after launch)

### Account structure & linkage — DECIDED (Lee, 2026-06-30)
- **Separate accounts.** CNC Cut and Craftons are **not** the same account. The engine works on the
  **Craftons ad account `310-491-2421`** ("Craftons Google Ads account") **only** for now.
- **Standalone, not under the MCC.** `310-491-2421` is reached by **direct user access**; it is **not**
  linked under the Craftons Marketing manager MCC (`275-347-3695`), and the MCC stays unused for now.
  Forcing the manager as `login-customer-id` returns `USER_PERMISSION_DENIED`, so the tool sends **no**
  `login-customer-id` by default (set `GOOGLE_ADS_USE_LOGIN_CUSTOMER_ID=1` only if the account is ever
  moved under the MCC).
- Context: this account is currently running a **Cavity Battens Performance Max** campaign (Craftons
  product: 84 conv / $1,171 / $13.94 per conv over 30 days; now PAUSED).
