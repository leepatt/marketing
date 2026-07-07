# Paste blocks — one per cnccut.app session

_The copy-paste sheet. Each block below is the first message for one fresh session in the
**cnccut.app** repo. Canonical specs live in the numbered briefs; this file is the convenience
sheet (kept in sync manually — if a brief changes, refresh its block here)._

**Order:** Block 1 (v1) first, and **merge it** before any others. Then recommended:
Block 2 (Studio) + Block 3 (SEO) in parallel → Block 4 (Social) + Block 5 (Meta) → Block 6
(Config Assets, after Studio) → Block 7 (Newsletter, last). See `08-execution-order.md`.

---

## BLOCK 1 — Cockpit v1: Foundation + Google Ads dashboard + Meta KPIs + chat (Brief 09)

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
`.claude/skills/craftons-design/BRAND.md`, `pipeline/` (README, tokens.css, render.mjs,
templates/, content/ examples), `campaigns/adwords/` (all md), and `dashboard-briefs/` (all md).
If raw fetch needs auth that isn't available, stop and tell me.

**STEP 3 — Cockpit shell.** Route `/marketing`, gated behind internal auth (Lee + Jake only; reuse
existing app auth if present, else a simple email allowlist). Left nav: Overview, Google Ads, Meta
Ads, Studio, Config Assets, Social, Newsletter, SEO (unbuilt = "coming soon"). Craftons theme from
the synced BRAND.md + tokens.css: dark forest green `#194431`, black, warm off-white neutrals (no
blue cast), Aeonik display (fallback Space Grotesk/Inter) / Inter body, 4px spacing scale, 6px
radius, curved-line motif behind hero text, NO gradients on UI surfaces, NO emoji. Shared UI
primitives all modules reuse: page header, section card, data table, KPI tile, trend chart, empty +
loading states, an **Approval drawer** (proposed change → Approve/Reject/Edit), a **Run panel**
(trigger a tools job, show output), and the **chat dock** (Step 8).

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

---

## BLOCK 2 — Studio: image/video generator (Brief 03)

Cockpit v1 (Brief 09) must already be built and merged — if `docs/marketing/` doesn't exist, stop
and flag it. Open and read the full brief `docs/marketing/dashboard-briefs/03-image-video-generator.md`
plus the shared conventions in `docs/marketing/dashboard-briefs/01-foundation-cockpit-shell.md` and
`docs/marketing/APP-NOTES.md`, then build the **Studio (image/video generator) module**. Port the
render system synced under `docs/marketing/pipeline/` (content JSON + HTML template → PNG via
Playwright + sharp; if the pipeline source isn't synced, extend the sync manifest and re-run it)
into a `tools/studio.mjs` backend and a `/marketing/studio` page. Ship the MVP: render a brand
template to a finished PNG, run the `QUALITY-DOCTRINE` Gate-1 adherence check, and land it in an
asset library as `needs-approval` with provenance, approvable via the shared Approval drawer. Then
wire one AI-gen path (Glif/Replicate from a locked style) through the same flow with a pre-run cost
estimate and `CONFIRM=1` for final-model spend. Hero geometry/dimensions are rendered from real
data, never AI-imagined; nothing ships without human approval. New branch, logical commits.

---

## BLOCK 3 — SEO Manager (Brief 07)

Cockpit v1 (Brief 09) must already be built and merged — if `docs/marketing/` doesn't exist, stop
and flag it. Open and read the full brief `docs/marketing/dashboard-briefs/07-seo-manager.md` plus
the shared conventions in `docs/marketing/dashboard-briefs/01-foundation-cockpit-shell.md` and
`docs/marketing/APP-NOTES.md`, then build the **SEO Manager module**. Ship the MVP on
`/marketing/seo`: load `docs/marketing/brand/keyword-plan.md` into a **coverage table** mapped to
live Shopify pages (flag gaps), a `tools/seo.mjs audit` that scores the key product pages
(title/meta/alt/JSON-LD/links) with fixes, and a `tools/seo.mjs brief --keyword <term>` that
produces a SERP-aware content brief (Perplexity + Firecrawl + the `seo-content` skill logic, with
PAA + Article/FAQ JSON-LD stub). Briefs land `needs-approval` via the shared Approval drawer. No
writes to the live Shopify store without approval + `CONFIRM=1`. Decide with me whether to wire
Google Search Console now or defer (see Open Questions). New branch, logical commits.

---

## BLOCK 4 — Social Media Organiser (Brief 05)

Cockpit v1 (Brief 09) must already be built and merged — if `docs/marketing/` doesn't exist, stop
and flag it. Open and read the full brief `docs/marketing/dashboard-briefs/05-social-media-organiser.md`
plus the shared conventions in `docs/marketing/dashboard-briefs/01-foundation-cockpit-shell.md` and
`docs/marketing/APP-NOTES.md`, then build the **Social Media Organiser module**. The asset library
(Brief 03) should exist. Ship the MVP for **Instagram** end-to-end: a content **calendar + status
pipeline** (idea→draft→approved→scheduled→posted) on `/marketing/social`, a `tools/social.mjs
draft` that writes captions in `SOCIAL-VOICE` (value-first, no emoji) with a Gate-1 self-check and
attaches a library asset, the shared Approval drawer for Gate 2, and — since Later has no API — an
**export** step that packages an approved post for Later and marks it scheduled. Pull IG organic
insights back into a scorecard (optimise for saves + shares). Nothing auto-posts. Leave FB/LinkedIn
as stubs pending the API decisions in the brief. New branch, logical commits.

---

## BLOCK 5 — Meta Ads full module (Brief 02)

Cockpit v1 (Brief 09) must already be built and merged — if `docs/marketing/` doesn't exist, stop
and flag it. Open and read the full brief `docs/marketing/dashboard-briefs/02-meta-ads.md` plus the
shared conventions in `docs/marketing/dashboard-briefs/01-foundation-cockpit-shell.md` and
`docs/marketing/APP-NOTES.md`, then build the **Meta Ads module** in the marketing cockpit (v1 put
Meta KPI tiles on the Overview; this builds the full `/marketing/meta` page). Extend the existing
`tools/meta-ads.mjs` (keep its `CONFIRM=1` guardrail); do not rewrite it. Ship the MVP slice: a
weekly Meta report (spend/results/ROAS/CTR by campaign→ad set→ad + IG insights) rendered on
`/marketing/meta` with wasted-spend flags, plus ONE write path (pause ad / add exclusion) going
through the shared Approval drawer → `CONFIRM=1` → logged. Pull voice/targeting from
`docs/marketing/`. Read-only by default; never spend or launch without approval. New branch,
logical commits.

---

## BLOCK 6 — Config Asset Creator (Brief 04)

Cockpit v1 (Brief 09) must already be built and merged — if `docs/marketing/` doesn't exist, stop
and flag it. Open and read the full brief `docs/marketing/dashboard-briefs/04-config-asset-creator.md`
plus the shared conventions in `docs/marketing/dashboard-briefs/01-foundation-cockpit-shell.md` and
`docs/marketing/APP-NOTES.md`, then build the **Config Asset Creator module**. The Studio render
pipeline (Brief 03) should exist — reuse it, don't duplicate it. First, find where product
**configurations/quotes** live in this repo/DB and document it in `docs/marketing/APP-NOTES.md`.
Then ship the MVP: pick a real configuration (start with Radius Pro or the Formwork Builder job),
map its real fields into a content JSON, render an on-brand **spec/proof card** (spec stamps +
ALL-CAPS compliance callouts + curve motif, specs pulled from the config, never AI-invented), run
the Gate-1 brand-check, and land it in the asset library `needs-approval` with the source config id
as provenance. Anonymise customer data. If my scope read is wrong (see the brief's Interpretation
flag), stop and ask before building. New branch, logical commits.

---

## BLOCK 7 — Newsletter Generator (Brief 06)

Cockpit v1 (Brief 09) must already be built and merged — if `docs/marketing/` doesn't exist, stop
and flag it. Open and read the full brief `docs/marketing/dashboard-briefs/06-newsletter-generator.md`
plus the shared conventions in `docs/marketing/dashboard-briefs/01-foundation-cockpit-shell.md` and
`docs/marketing/APP-NOTES.md`, then build the **Newsletter Generator module**. Email platform is
**Shopify Email** (already connected — no new key). First confirm whether the Shopify Email API/MCP
supports programmatic campaign create+send or requires a human click, and note it in
`docs/marketing/APP-NOTES.md`. Ship the MVP on `/marketing/newsletter`: a `tools/newsletter.mjs`
that assembles a suggested issue from recent approved assets/posts/products, drafts subject +
sections in brand voice, renders an **email-safe HTML** preview (desktop + mobile) with a Gate-1
brand-check, goes through the shared Approval drawer, and does a **test-send to self** via Shopify
Email. Block the real list-send behind approval + test-send + `CONFIRM=1` (or hand off to Shopify
admin if the API can't send). No emoji; brand voice, not social-caption tone. New branch, logical
commits.
