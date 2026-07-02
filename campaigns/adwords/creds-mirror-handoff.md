# Handoff prompt — mirror Google Ads API creds (paste into a new session)

> Paste this whole file as your first message in a new session. It briefs you to help me mirror the
> Google Ads API credentials into another environment.
> **NEVER print, echo, or ask me to paste any secret values into the chat.**

## Task
Help me copy the **current (post-2026-06-23 rotation)** Google Ads API credentials from their source
of truth into a target environment (the marketing engine's env vars / wherever `tools/google-ads.mjs`
will run), so the engine can manage the Craftons Google Ads account once **Basic API access** is granted.

## Hard rules
- **Do NOT print, echo, or request any secret values** in chat — developer token, client secret,
  refresh token. Those get pasted **directly into the environment-variable UI only.**
- Account IDs (customer IDs / MCC) are **not** secrets and may be discussed.

## Known facts (from the prior session + committed docs — verify where flagged)

**Source of truth = Vercel.** The rotated `GOOGLE_ADS_CLIENT_SECRET` and `GOOGLE_ADS_REFRESH_TOKEN`
were placed in the **cnccut-app Vercel project → Settings → Environment Variables** on 2026-06-23 and
redeployed. The **local `cnccut-app` `.env` is STALE** (old/revoked values or none) — **do not copy
from it.** This marketing engine's env does **not** have them yet.

**Env-var names (the 6 the tooling uses — match EXACTLY what's in Vercel):**
```
GOOGLE_ADS_DEVELOPER_TOKEN
GOOGLE_ADS_CLIENT_ID
GOOGLE_ADS_CLIENT_SECRET
GOOGLE_ADS_REFRESH_TOKEN
GOOGLE_ADS_CUSTOMER_ID         # advertiser, digits only (no dashes)
GOOGLE_ADS_LOGIN_CUSTOMER_ID   # MCC, digits only (no dashes)
```
(These are the documented convention — confirm against the actual names shown in Vercel and copy them verbatim.)

**Account mapping (VERIFY step 1 before copying CUSTOMER_ID):**
- MCC "Craftons Marketing" = **275-347-3695** → `GOOGLE_ADS_LOGIN_CUSTOMER_ID = 2753473695`
- Craftons advertiser = **310-491-2421** → `GOOGLE_ADS_CUSTOMER_ID = 3104912421`
  - *Documented mapping. The account holding the Shopify purchases + Craftons-named GA4 conversion
    actions (23 purchases + 443 lead forms) is clearly Craftons — but the exact ID and whether the
    CNC Cut campaigns share this same account vs a separate one was NOT confirmed last session.*

## Steps (guide me through these)
1. **Verify the account:** open the Google Ads account with the conversion tracking (23 purchases +
   443 lead forms) → confirm its ID is `310-491-2421`, and check whether the **CNC Cut campaigns** sit
   in the **same** account (shared) or a **different** one. Use whichever ID is correct for the account
   the engine should manage.
2. **Confirm the 6 variable names** present in the cnccut-app Vercel project.
3. **Mirror to the target env:** create the **same 6 names** there; paste each value directly in that
   env's UI (never via chat). Use the **verified** advertiser ID for `GOOGLE_ADS_CUSTOMER_ID` and
   `2753473695` for `GOOGLE_ADS_LOGIN_CUSTOMER_ID`.
4. **Verify** with a **read-only** Google Ads API call — only **after Basic access is granted** (Test
   access cannot hit the live account).

## Context docs (marketing repo, branch `claude/peninsula-studio-marketing-access-3uwvoz`)
- `STATUS.md` — overall project status & plan
- `campaigns/adwords/api-access.md` — API access plan + control model (Claude reports, Lee approves)
- `campaigns/adwords/api-tool-design.md` — the `google-ads.mjs` design (for the Basic-access app)
- `INTEGRATIONS.md` — integration runbook (notes the env-var-name verification TODO)
