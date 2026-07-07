# Brief 09 — Cockpit v1: Foundation + Google Ads dashboard + Meta KPIs + chat assistant

_Decided 2026-07-07: collapse the first real build into one effort. This brief **absorbs Brief 01**
(Foundation) and adds the Google Ads dashboard as the flagship module, Meta KPI tiles on the
Overview, and a GoHighLevel-style chat assistant. The kickoff block at the bottom is **fully
self-contained** — paste it into a fresh cnccut.app session (which cannot read this repo)._

**Status changes since the earlier briefs (bake these in):**
- ✅ **Google Ads API Basic access APPROVED** (confirmed by Lee 2026-07-07). Live account data is
  pullable via the API with the rotated creds already in Vercel.
- ✅ An **LLM API key already exists in the app's Vercel env** — the session should find and use it
  for the chat assistant.
- The CNC Cut account reassessment (vs. the 2026-06-30 baseline) is due ~2026-07-07 — the new
  dashboard's first real job.

## What v1 contains

1. **Foundation shell** (everything from Brief 01): `/marketing` cockpit, auth, Craftons theme,
   doc-sync into `docs/marketing/`, shared data layer (`runs`/`approvals`/`assets`/`metrics_cache`),
   shared UI primitives, `tools/*.mjs` conventions.
2. **`tools/google-ads.mjs`** — the engine's Google Ads tool (report mode read-only by default,
   change mode behind `CONFIRM=1`), per `campaigns/adwords/api-access.md` + `api-tool-design.md`.
3. **Google Ads dashboard page** (`/marketing/google-ads`) — live KPIs, trends, campaign → ad group →
   keyword → search-terms drill-down, wasted-spend flags, for both the Craftons advertiser account
   and CNC Cut spend under the MCC.
4. **Overview page** with cross-channel KPI tiles: Google Ads live + Meta (via the existing
   `tools/meta-ads.mjs`) — GoHighLevel-style dense marketing snapshot.
5. **Chat assistant** docked at the bottom of the cockpit — server-side LLM route that can
   call the report tools and answer "how are ads going?", produce daily/weekly reports on demand.
   **Read-only**: it can draft proposals into `approvals` but can never execute a write.

## Design inspiration

GoHighLevel-style marketing command centre: dense KPI tile row up top (spend, clicks, conversions,
cost/conversion, CTR, ROAS where derivable), trend charts (7/30-day), channel cards, a campaign
table, and a persistent assistant/chat dock at the bottom. Rendered in the **Craftons design system**
(dark forest green `#194431`, warm off-white, Aeonik/Inter, no gradients, no emoji) — not GHL's look,
its **information density and workflow**.

## Account facts (from the marketing repo — treat as ground truth)

- MCC / manager: **Craftons Marketing `275-347-3695`** → `GOOGLE_ADS_LOGIN_CUSTOMER_ID=2753473695`
- Advertiser account: **`310-491-2421`** → `GOOGLE_ADS_CUSTOMER_ID=3104912421`
- Open structural question: whether the new Craftons campaigns live in the same account as CNC Cut's
  existing campaigns — the dashboard should **list accessible accounts under the MCC** and handle
  one-or-many gracefully.
- CNC Cut baseline (June 2026): A$2,069.83 spend / 321 clicks / $6.45 CPC / 9.16% CTR / 0 tracked
  conversions; tightened 2026-06-30 (Industry Specific paused, CPC capped ~$3.50, partners/display
  off, negatives added). The dashboard should make the vs-baseline comparison easy.
- Craftons Shopify conversion tracking is verified solid (Purchases + lead forms primary).

## Non-negotiables

- Read-only by default everywhere; any write (budget, bid, pause, negative) = UI approval +
  `CONFIRM=1`. Chat assistant can *propose*, never execute.
- Secrets stay in `.env`/Vercel; never logged, never committed, never echoed by the assistant.
- Later tool modules (social, newsletter, SEO, studio, config assets) still come as separate
  sessions per Briefs 02–07 — v1 must not preclude them (nav shows them as "coming soon").

---

## Kickoff block — copy everything below the line into a fresh cnccut.app session

---

Build **v1 of the Marketing Cockpit** in this repo (cnccut.app): the foundation shell + a live
**Google Ads dashboard** + Meta KPI tiles + a chat assistant. Take workflow inspiration from
GoHighLevel-style marketing command centres (dense KPIs, trends, campaign tables, assistant dock)
but render it in the Craftons design system. Work on a new branch, commit in logical steps. Ask me
before anything irreversible; nothing may spend, post, or change ad settings without my approval.

**Context / decisions already made (don't relitigate):**
- ONE unified marketing cockpit at `/marketing`; each tool is a module/route. Later modules (Meta
  Ads full page, Studio, Config Assets, Social, Newsletter, SEO) come in later sessions — show them
  in the nav as "coming soon".
- Hybrid pattern: dashboard UI + `tools/*.mjs` backend scripts. `tools/meta-ads.mjs` already exists
  with a `CONFIRM=1` guardrail — copy its conventions exactly (env handling, dry-run without
  CONFIRM, arg style).
- Control model (non-negotiable): read-only by default; ANY write (budgets, bids, pause/enable,
  negatives, campaign edits) requires a UI approval + `CONFIRM=1`. The chat assistant is
  read-only — it can draft a proposal into the approvals queue but can never execute a change.
- **Google Ads API Basic access is APPROVED** and the rotated creds are in Vercel env vars.
- Secrets live in `.env`/Vercel only. Never commit, log, or let the assistant echo them.

**STEP 1 — Recon.** Scan the repo and write `docs/marketing/APP-NOTES.md`: framework/hosting
(assumed Next.js on Vercel — confirm), any existing Google Ads dashboard scaffolding (reuse, don't
fork), `tools/meta-ads.mjs` (document its exact env var names and conventions), auth, styling
approach, data layer, and which env vars exist. Expected (verify names, don't invent):
`GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`,
`GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID` (=3104912421),
`GOOGLE_ADS_LOGIN_CUSTOMER_ID` (=2753473695), `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID`, and an
LLM key (look for `ANTHROPIC_API_KEY` or similar — one is already in Vercel; if you can't find any,
stop and ask me rather than assuming).

**STEP 2 — Doc-sync.** Brand/strategy docs live in the separate repo `leepatt/marketing`. Build
`scripts/sync-marketing-docs.mjs` + `scripts/marketing-docs.manifest.json` (allowlist of paths →
`docs/marketing/`), fetching via GitHub's raw content API for a pinned branch, committing the synced
copies, recording the source SHA in `docs/marketing/SYNC.md`. Docs only — never secrets. Seed the
manifest with: `CLAUDE.md`, `STATUS.md`, `CONTENT-PILLARS.md`, `SOCIAL-VOICE.md`,
`QUALITY-DOCTRINE.md`, `INTEGRATIONS.md`, `SETUP.md`, `brand/*.md`,
`.claude/skills/craftons-design/BRAND.md`, `pipeline/tokens.css`, `campaigns/adwords/` (all md),
and `dashboard-briefs/` (all md). If raw fetch needs auth that isn't available, stop and tell me.

**STEP 3 — Cockpit shell.** Route `/marketing`, gated behind internal auth (Lee + Jake only; reuse
existing app auth if present, else a simple email allowlist). Left nav: Overview, Google Ads, Meta
Ads, Studio, Config Assets, Social, Newsletter, SEO (unbuilt = "coming soon"). Craftons theme from
the synced BRAND.md + tokens.css: dark forest green `#194431`, black, warm off-white neutrals (no
blue cast), Aeonik display (fallback Space Grotesk/Inter) / Inter body, 4px spacing scale, 6px
radius, curved-line motif behind hero text, NO gradients on UI surfaces, NO emoji. Shared UI
primitives all modules reuse: page header, section card, data table, KPI tile, trend chart, empty +
loading states, an **Approval drawer** (proposed change → Approve/Reject/Edit), a **Run panel**
(trigger a tools job, show output), and the **chat dock** (Step 7).

**STEP 4 — Shared data layer.** Use the app's existing DB if there is one; else provision
lightweight Postgres (Vercel Postgres/Neon), or a typed JSON file-store behind an interface as a
last resort. Tables: `runs` (tool, args, status, timestamps, output, cost), `approvals` (proposed
action, payload/diff, status, approver, timestamps), `assets`, `metrics_cache` (channel, metric,
period, value, pulled_at). Additive migrations only.

**STEP 5 — `tools/google-ads.mjs`** (Node ESM, official `google-ads-api` client, creds from env,
MCC `login-customer-id` header). Subcommands:
- `accounts` — list accessible client accounts under the MCC (there may be one or several; handle
  both — CNC Cut campaigns and new Craftons campaigns may share account `3104912421` or not).
- `report [--account <id>] [--days 7|30]` (default, read-only) — GAQL pulls: campaign, ad group,
  keyword, and search-term performance (cost, clicks, impressions, CTR, avg CPC, conversions,
  cost/conversion, impression share where available). Output structured JSON + a Markdown summary;
  cache into `metrics_cache`; write a `runs` row. Flag: wasted search terms (spend, 0 conv),
  keywords ≥20 clicks 0 conv, best/worst ad group by cost/conversion.
- `propose --change <json>` — validate a proposed change (add negatives, pause keyword/ad/campaign,
  budget/bid adjust) and enqueue it into `approvals`. Does NOT touch the account.
- `apply --approval <id>` — execute an approved change; requires `CONFIRM=1`; logs everything.
  Without `CONFIRM=1`, print the exact mutation as a dry-run and exit.
Handle rate limits/partial failures; never log tokens. Callable from CLI and from an authed API
route (share the core as an importable module).

**STEP 6 — Google Ads dashboard page** (`/marketing/google-ads`). Account switcher (from
`accounts`). KPI row: spend, clicks, conversions, cost/conversion, CTR, avg CPC — with 7 vs 30-day
toggle and delta vs prior period. Trend chart (daily spend + conversions). Campaign table →
drill into ad groups → keywords; a search-terms tab with "add as negative" actions that go through
the Approval drawer (never direct). A "flags" panel surfacing the wasted-spend findings. Context
note: the CNC Cut account was tightened 2026-06-30 (Industry Specific paused, CPC capped ~$3.50,
partners/display off) with a June baseline of A$2,069.83 / 321 clicks / $6.45 CPC / 0 tracked
conversions — show a vs-baseline comparison so the tightening's effect is obvious.

**STEP 7 — Overview page + Meta KPIs.** `/marketing` Overview: GoHighLevel-style snapshot — a
cross-channel KPI row (Google Ads live from Step 5; Meta spend/results/CTR via the existing
`tools/meta-ads.mjs` report mode, extending it only if needed), per-module status cards (last run,
pending approvals), and the flags feed. If the Meta token lacks a scope, degrade gracefully and
note it in APP-NOTES rather than failing the page.

**STEP 8 — Chat assistant.** A persistent chat dock at the bottom of the cockpit (collapsible),
GoHighLevel-assistant style. Server-side API route using the LLM key found in Step 1 (if it's an
Anthropic key, use the Messages API with tool use; default to the latest Claude model, e.g.
`claude-sonnet-5`). System prompt: it is the Craftons marketing assistant; ground it in the synced
`docs/marketing/` context (brand facts, account IDs, baselines). Give it read-only tools: run
`google-ads report`, run `meta-ads report`, query `metrics_cache`, and `propose` (enqueue to
approvals only). It must answer things like "give me today's report", "how are the ads going?",
"what's wasting money?" with real numbers, and format a tight daily/weekly report on request. It
NEVER executes writes, never reveals env values, and says so if asked. Stream responses; keep chat
history per user in the data layer.

**Done when (acceptance):**
1. `/marketing` renders themed + auth-gated with full nav; Overview shows live Google Ads + Meta
   KPI tiles and module status cards.
2. `docs/marketing/` synced with SHA recorded; `APP-NOTES.md` documents stack + env names.
3. `tools/google-ads.mjs report` pulls real live data (campaigns/keywords/search terms) and the
   Google Ads page renders it with drill-down, flags, and the CNC Cut vs-baseline view.
4. A search-term → negative proposal flows through the Approval drawer and only executes with
   `CONFIRM=1` (demonstrate the dry-run).
5. The chat dock answers "give me a daily report" with real numbers from both channels.
6. No secrets in code, logs, or chat output.

Deploy the branch as a Vercel preview and give me the URL to review before anything merges.
