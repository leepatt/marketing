# Integrations & API Keys — Setup Runbook

The per-integration "how to actually wire it" companion to `SETUP.md` Part B. One section per
integration: what it unlocks, exactly how to get the key, the env var name, where it lives, and
cost. Work top-down by priority.

## Ground rules (read once)

- **Only you can obtain the keys** (they require logins to each service). I can wire each one
  into tooling **once the key exists** in the env — and I can verify, document, and build the
  scripts around it.
- **Never paste raw keys into chat.** Put them straight into the cnccut.app `.env` and/or the
  web-session environment-variable config. Chat is not a safe place for secrets.
- **Keys live in the cnccut.app code repo `.env`** + the remote session env vars. Never in the
  Drive brain, never committed to git. (`.gitignore` here excludes `.env*`.)
- **Two ways to connect each service:**
  1. **Raw API key** → in `.env`, used by scripts/tooling. Most control.
  2. **Zapier MCP bridge** → already connected in this session. Good for posting/notifying/
     simple actions without managing raw keys. Configure actions at:
     `https://mcp.zapier.com/mcp/servers/1d8f79d5-5ec9-4104-8ff7-61fb14322f73/config`
- **TODO (blocked on repo scope):** verify the exact env var names below against cnccut.app's
  existing `.env` (especially Meta + Google Ads + Perplexity, which the notes say are already
  partly wired). The names below are the recommended convention; match the repo if it differs.

---

## Priority 1 — Production (unblocks content at volume)

### B1 · Replicate — AI image + video generation
- **Unlocks:** b-roll, video extension, image touch-up, illustration gen (Phase 2/Step 3).
- **Get the key:** [replicate.com](https://replicate.com) → sign in → **Account → API tokens** → *Create token*.
- **Env var:** `REPLICATE_API_TOKEN`
- **Cost:** pay-as-you-go, ~$50–150/mo depending on volume. Draft on cheap models, spend on finals.
- **Status:** ✅ Key collected 2026-06-15 — pending placement in `.env` + verify

### B2 · Glif — templated image gen / ad-creative variants
- **Unlocks:** carousel templates, Meta ad-creative variants from a template.
- **Get the key:** [glif.app](https://glif.app) → account settings → **API**.
- **Env var:** `GLIF_API_TOKEN`
- **Cost:** credits, ~$20–40/mo.
- **Status:** ✅ Key collected 2026-06-15 — pending placement in `.env` + verify

---

## Priority 2 — Intel (unblocks Trend Radar + teardowns)

### B3 · Perplexity — research / Trend Radar
- **Unlocks:** weekly Trend Radar digest, market/competitor research.
- **Get the key:** [perplexity.ai](https://www.perplexity.ai) → **Settings → API** → buy credits → generate key.
- **Env var:** `PERPLEXITY_API_KEY`
- **Cost:** usage-based, small.
- **Status:** ✅ Key collected 2026-06-15 — pending placement in `.env` + verify

### B4 · Firecrawl — scrape inspo & competitor content
- **Unlocks:** pulling brand/competitor posts and pages for teardowns into `01 Inspiration/`.
- **Get the key:** [firecrawl.dev](https://www.firecrawl.dev) → dashboard → **API Keys**.
- **Env var:** `FIRECRAWL_API_KEY`
- **Cost:** free tier, then usage-based.
- **Status:** ✅ Key collected 2026-06-15 — pending placement in `.env` + verify

---

## Priority 3 — Distribution (unblocks posting + measurement)

### B5 · Later.com — scheduling / posting
- **Unlocks:** approved drafts → scheduled/posted (the execution end of the loop).
- **Reality (confirmed 2026-06-15):** Later has **no public API** — it's a manual visual scheduler by design. No developer endpoint for programmatic posting or analytics.
- **Decision: manual.** Claude drafts captions + assets → Lee loads them into Later → Later schedules/posts. Fits the "Lee approves and posts" control model exactly. No key, no integration.
- **Measurement:** pull performance from the **Meta/IG Graph API (B6)** directly, not from Later.
- **If automation is ever wanted:** switch to an API-first scheduler — **Postproxy** (free tier + MCP, best fit), **Ayrshare** (~$149/mo, most established), Late, or Post for Me. Only worth it once the manual load-in is the bottleneck.
- **Status:** ✅ Decided — manual (no key needed)

### B6 · Meta / Instagram Graph API — insights + ads
- **Unlocks:** IG insights → dashboard (Phase 4); Meta ad creative + draft campaigns (Phase 5).
- **Setup:** [developers.facebook.com](https://developers.facebook.com) → create app → add
  **Instagram Graph API** + **Marketing API** → link the IG business account + the Craftons FB
  page → generate a **long-lived access token**.
- **Env vars:** `META_ACCESS_TOKEN`, `META_APP_ID`, `META_APP_SECRET`, `META_AD_ACCOUNT_ID`, `IG_BUSINESS_ACCOUNT_ID`
- **Note:** `tools/meta-ads.mjs` already exists in cnccut.app with a `CONFIRM=1` guardrail —
  check which env vars it already expects and reuse those names.
- **Status:** ✅ `META_ACCESS_TOKEN` + `META_AD_ACCOUNT_ID` collected 2026-06-15 — pending placement + verify. (Still TBC: `META_APP_ID`/`META_APP_SECRET`/`IG_BUSINESS_ACCOUNT_ID` — check what `meta-ads.mjs` actually needs.)

### B7 · Google Ads API — draft search/awareness campaigns
- **Unlocks:** programmatic campaign drafting (Phase 5). Account already exists.
- **Setup:** Google Ads → **API Center** → apply for a **developer token** (approval has lead
  time — apply early) → create an OAuth2 client → generate a refresh token.
- **Env vars:** `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID`, `GOOGLE_ADS_LOGIN_CUSTOMER_ID`
- **Accounts (set up 2026-06-15):** Manager (MCC) `Craftons Marketing` = `275-347-3695` → `GOOGLE_ADS_LOGIN_CUSTOMER_ID=2753473695`; advertiser account `310-491-2421` → `GOOGLE_ADS_CUSTOMER_ID=3104912421`. OAuth client is a **Web application** with redirect URI `https://developers.google.com/oauthplayground`; refresh token minted via OAuth Playground (own creds, offline + force-consent).
- **Status:** ✅ All 5 values collected 2026-06-15 — pending placement + verify. **Basic-access approval still pending** (dev token is Test-access until granted; manual campaign building is fine meanwhile). ⚠️ Client secret + refresh token were exposed in a setup screenshot — rotate secret + re-mint refresh token before production.

---

## Priority 4 — Newsletter

### B8 · Email platform — newsletter send + list → **Shopify Email** (decided 2026-06-15)
- **Unlocks:** fortnightly newsletter; list built off the calculator lead magnet (Phase 3).
- **Decision:** use **Shopify Email**, not Klaviyo, to start. Rationale: already connected (no new account/key), free for the **first 10,000 sends/month** (a fortnightly newsletter to a small list stays free indefinitely), and lives in the same admin as the store/customer data.
- **Trade-off accepted:** Shopify Email has weak automation — no branching flows, A/B splits, or multi-step sequences. Fine for a simple fortnightly broadcast. **Revisit Klaviyo** only if/when we need real lifecycle automation (abandoned-config flows, predictive sends).
- **How:** Shopify admin → **Marketing → Campaigns → Create campaign → Shopify Email**. No API key needed for sending; the Shopify MCP connector (already live) + `customer`/`marketing` Admin API cover list reads and automation if we script it later.
- **Env var:** none (uses the existing Shopify connection). `KLAVIYO_API_KEY` only if we switch back.
- **Status:** ✅ Decided — Shopify Email (no key needed)

---

## Priority 5 — Local tooling (no keys)

### B9 · Media tooling — ffmpeg, sharp / Pillow / OpenCV
- **Unlocks:** video assembly + image processing locally (Phase 2).
- **Setup:** install in the session environment via a setup/SessionStart script so every session
  has them. No keys.
- **Status:** ☐ Add to setup script

---

## What unblocks what

```
B1 Replicate ─┐
B2 Glif       ├─► Step 3 Production (image/video at volume)
B9 ffmpeg ────┘
B3 Perplexity ─┐
B4 Firecrawl ──┴─► Step 2 Trend Radar + teardowns
B5 Later ─────────► Step posting (operating loop)
B6 Meta/IG ───────► Step 5 dashboard insights + Step 6 Meta ads
B7 Google Ads ────► Step 6 Google ads
B8 Klaviyo ───────► Step 4 newsletter
```

## Suggested order to knock out

1. **B1 + B2** (production) and **B3 + B4** (intel) — these unblock the most recurring work.
2. **B9** — quick, no key.
3. **B6** — start the Meta token now; it gates both insights and ads.
4. **B7** — apply for the Google Ads dev token early (approval lag).
5. **B8** — after the platform decision.
6. **B5** — manual to start; automate later.

> When you've put a key in the env, tell me which one and I'll wire/verify the tooling around it.
