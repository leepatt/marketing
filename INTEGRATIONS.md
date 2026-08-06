# Integrations & API Keys — Setup Runbook

The per-integration "how to actually wire it" companion to `SETUP.md` Part B. One section per
integration: what it unlocks, exactly how to get the key, the env var name, where it lives, and
cost. Work top-down by priority.

## 🔑 How to add an API key to the session environment (verified 2026-08-03)

Keys live on the **environment**, not the session, so they persist across sessions.

> ⚠️ **There is no settings page and no direct URL for this.** An earlier version of this doc said
> "claude.ai/code → Environments", which does not exist — that's why it couldn't be found.

1. On **claude.ai/code**, click the **cloud icon in the row directly above the message box** — it shows
   the current environment's name (e.g. `Default`). That is the only way in.
2. **Hover the environment in the list → a gear icon appears on the right → click it.** The dialog has
   Name, Network access, **Environment variables**, and Setup script.
3. Enter variables in **`.env` format, one `KEY=value` per line**. No quotes needed for plain values.
   Quote anything containing `#`, or the rest of the line is treated as a comment and dropped.
4. Two environments exist (`Default`, `Default Cloud Environment`). Use whichever already holds
   `META_ACCESS_TOKEN` — that's the one these sessions run in.
5. Values come from **vercel.com/craftons/cnccut-app → Settings → Environment Variables → reveal**.
6. ⚠️ **Start a NEW session.** Per Anthropic's docs: *"editing or adding variables affects sessions you
   start afterward; sessions already running keep the values they started with."*

### ⚠️ On putting secrets here at all

Anthropic's docs are explicit: *"cloud environments have no dedicated secrets store, so don't add API
keys or other credentials"*, and the dialog warns values are readable by **anyone using the
environment**.

**Why we do it anyway, knowingly:** these environments are *personal to Lee's account*, so "anyone
using the environment" is Lee. `META_ACCESS_TOKEN`, `DATABASE_URL`, `PERPLEXITY_API_KEY`,
`REPLICATE_API_TOKEN` and `GLIF_API_TOKEN` are already there on that basis.

**Where this stops being acceptable:** an **organisation-shared** environment (admin settings), where
the values reach every member's sessions. Don't put Craftons credentials in a shared environment.

`META_PAGE_ID` is not a secret — it's a public Facebook page ID — so it carries no such tradeoff.

**Never paste secret values into chat, into a repo file, or into the Drive brain.**

### Current state — what's actually missing, and whether it matters

| Key | In session env? | What it unlocks | Priority |
|---|---|---|---|
| `META_ACCESS_TOKEN` | ✅ | Everything Meta reads/writes. SYSTEM_USER, never expires | — |
| `PERPLEXITY_API_KEY` · `REPLICATE_API_TOKEN` · `GLIF_API_TOKEN` · `DATABASE_URL` | ✅ | Research, image gen, warehouse | — |
| **`PAGE_ID`** | ✅ **(renamed)** | **Publishing ads at all** — `create-creative` fails without it | ⚠️ **Arrived as `PAGE_ID`, but the code reads `META_PAGE_ID`.** See below |
| **`HEYGEN_API_KEY`** | ✅ | AI avatar video creative | ✅ **Verified working 2026-08-04** — HTTP 200, 1,264 avatars, test render completed |
| **`ANTHROPIC_API_KEY`** | ❌ **still missing** | `brand-check` vision, avatar scripts, agent copy generation | 🔴 **Blocks the quality gate.** Was believed added 2026-08-04; it is not in session env |
| `META_APP_ID` · `META_APP_SECRET` | ❌ | Long-lived token refresh only | ⬜ **Skip.** The token is SYSTEM_USER and never expires — these buy nothing |

### ⚠️ Corrections verified in session env, 2026-08-04

Three keys were recorded as added on 2026-08-04. Checked by length/prefix in the first session able to
see them:

1. **`HEYGEN_API_KEY` — present and working.** `sk_V2_…`, 54 chars. Avatar register is unblocked.
2. **`META_PAGE_ID` — present under the wrong name.** The variable in session env is **`PAGE_ID`**
   (value matches `611852278682648`). Every tool resolves it as `readEnv(["META_PAGE_ID"])`, so with
   `PAGE_ID` alone `doctor` reports it missing and `create-creative` cannot publish.
   **Fix: rename the env var to `META_PAGE_ID`** in the environment config and in Vercel. Until then
   every tool invocation needs `META_PAGE_ID="$PAGE_ID"` prefixed, which is how this session ran them.
3. **`ANTHROPIC_API_KEY` — RESOLVED 2026-08-05: it is saved as `ANTHROPIC_KEY`.**
   Confirmed by Lee from a session started after the key was added. The env holds:

   | Var | State |
   |---|---|
   | `ANTHROPIC_KEY` | ✅ set, `sk-ant-api03-…` |
   | `ANTHROPIC_BASE_URL` | ✅ set |
   | **`ANTHROPIC_API_KEY`** | ❌ **not set** |

   **Same failure mode as `META_PAGE_ID` → `PAGE_ID`: right value, wrong name.** Everything in this
   repo — and the Anthropic SDK/CLIs by default — reads `ANTHROPIC_API_KEY`. `studio.mjs brand-check`
   calls `readEnv(["ANTHROPIC_API_KEY"])`, so with only `ANTHROPIC_KEY` it still reports the key as
   missing and marks assets `skipped`.

   **Two fixes, either works:**
   - **Permanent (preferred):** rename the variable to `ANTHROPIC_API_KEY` in the environment config
     and in Vercel. Then everything works with no prefixes.
   - **Per-command:** `ANTHROPIC_API_KEY="$ANTHROPIC_KEY" node tools/studio.mjs brand-check …`

   ✅ **Worked around in-session 2026-08-06** — exports added to `~/.bashrc` *above* the
   `[ -z "$PS1" ] && return` guard (below it, non-interactive tool shells never reach them):
   `export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-$ANTHROPIC_KEY}"` and
   `export META_PAGE_ID="${META_PAGE_ID:-${PAGE_ID:-611852278682648}}"`. Verified: `doctor` sees
   both, `brand-check` ran 36 live vision calls. **Container-local — dies with the container.**
   The rename remains the durable fix. (Also noted 2026-08-06: `PAGE_ID` was not visible in this
   session's env either — only the recorded value made the alias possible.)

   ⚠️ **Two of three keys in that batch arrived misnamed.** When adding a key, paste the name as well
   as the value — do not retype it. This has now cost two sessions.

   🔐 **Do not print the key's value.** A session offered to; there is never a reason to. Check
   presence by length and prefix only.

### 🔐 Rotate `META_ACCESS_TOKEN`

`GET /{pixel_id}/stats` returns the access token embedded in its own `paging.next` URL. A diagnostic
script in this session printed that response, so **the token is in the session transcript.** It was not
written to any repo file, commit, or the Drive brain. Low risk, but rotate it — it costs nothing.

**Lesson for any future script:** scrub before printing. Every diagnostic in this session now runs
output through `String(s).replace(/EAA[A-Za-z0-9]+/g, "<REDACTED>")`.

### HeyGen v2 is deprecated

`POST /v2/video/generate` works but returns a sunset warning: **legacy, removed 2026-10-31, migrate to
`POST /v3/videos`.** The avatar test used v2 successfully. Anything built for production should target
v3 so it does not break in October.

---

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
- **Status:** ✅ Values collected 2026-06-15. **Basic-access approval still pending** (dev token is Test-access until granted; manual campaign building is fine meanwhile). ✅ **Rotated 2026-06-23** — leaked client secret + refresh token revoked: deleted the "Craftons Ads" OAuth grant, disabled the leaked secret in Cloud Console (added a new secret), re-minted the refresh token via OAuth Playground, placed the two new values in **Vercel** env vars + redeployed. ⏳ Remaining (desktop): mirror the two new values into the Jake cloud environment; delete the disabled old secret once verified.

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
