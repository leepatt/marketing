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
- ☐ Basic access applied for (Lee)
- ◑ Google Ads creds mirrored into this engine's env vars — **all six present**, but the
  **refresh token is expired/revoked** (see blocker below). Other five are correct.
- ☐ `tools/google-ads.mjs` built (Claude, after access)
- ☐ Weekly routine wired (after launch + access)

## ⛔ BLOCKER (found 2026-06-30) — refresh token expired after 7 days
> **Progress 2026-06-30:** OAuth app **published to "In production"** ✅ (kills the 7-day expiry going
> forward). Still outstanding: re-mint the refresh token *after* publishing (a token minted pre-publish
> keeps the 7-day clock), put it in the env, and start a fresh session. Runbook below.

All six creds are now in this engine's env. Five verified correct: `GOOGLE_ADS_CLIENT_ID`
(well-formed), `GOOGLE_ADS_CLIENT_SECRET` (GOCSPX- prefix), `GOOGLE_ADS_CUSTOMER_ID=3104912421`,
`GOOGLE_ADS_LOGIN_CUSTOMER_ID=2753473695`, `GOOGLE_ADS_DEVELOPER_TOKEN`.

**`GOOGLE_ADS_REFRESH_TOKEN` is dead.** Minting an access token returns
`invalid_grant` / "Token has been expired or revoked."

**Root cause:** Google expires refresh tokens **7 days after issuance** when the OAuth app's
**consent screen is in "Testing" publishing status** (the `adwords` scope is a sensitive scope, so
this applies). The token was re-minted on **2026-06-23**; today is **2026-06-30** = exactly 7 days.
It died on schedule. Re-minting now without changing publishing status will just expire again next
week.

**Permanent fix (Lee):**
1. Google Cloud Console → **Google Auth Platform → Audience** (a.k.a. the old "OAuth consent screen")
   → **Publish app** so publishing status = **"In production."** This stops the 7-day refresh-token expiry.
2. Re-mint the refresh token via **OAuth Playground** (see runbook below). **Order matters — see gotcha.**
3. Drop the new `GOOGLE_ADS_REFRESH_TOKEN` into this engine's env (and Vercel, to keep them in sync).
4. **Start a fresh Claude session** (env vars only load at session start — a running session keeps the
   old value), then tell Claude "refresh token re-minted" → Claude re-verifies the live API call.

(Claude can't do steps 1–2: they need Lee's Google login + consent.)

### ⚠️ Ordering gotcha — PUBLISH *before* you mint
A refresh token's expiry is locked in **at mint time**, based on the app's publishing status *then*:
- Minted while the app is **"Testing"** → still gets the **7-day expiry**, even if you publish 1 minute later.
- Minted **after** the app is **"In production"** → durable, no 7-day clock.

So: **Publish first, then mint.** If you minted before publishing, throw that token away and mint again.

### Runbook — mint a fresh refresh token (OAuth Playground)
**Need first:** the OAuth **Client ID** + **Client secret** (Cloud Console → **Google Auth Platform →
Clients** → click the OAuth client → shown on the right). The Web-app client's redirect URI must include
`https://developers.google.com/oauthplayground`.

1. Open **https://developers.google.com/oauthplayground**
2. **⚙️ gear (top-right)** → tick **"Use your own OAuth credentials"** → paste **Client ID** + **Client secret**.
3. In that same gear panel set **Force prompt = Consent screen** (forces a *new* refresh token instead of
   handing back the old one).
4. Close the gear. In **Step 1 — Select & authorize APIs**, use the **"Input your own scopes"** box and enter
   exactly:  `https://www.googleapis.com/auth/adwords`  → click **Authorize APIs**.
5. Sign in with the **Google account that owns the Craftons / MCC accounts**. Click through consent
   (own unverified app → **Advanced → Go to … (unsafe)** is fine). Approve.
6. **Step 2** → click **Exchange authorization code for tokens**.
7. Copy the **Refresh token** (starts with `1//`). That's the new secret → into the env (not into chat).

**Trip-ups:** if the response has *no* refresh token (only an access token), force-consent didn't take —
redo step 3 and re-authorise. And use the right Google account, or the token won't see the Craftons accounts.
