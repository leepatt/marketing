# Craftons Marketing Engine — Setup & Build Steps

The ordered, do-this-now checklist for standing up the marketing engine. This is the
**execution layer**: the sequence, the integrations, and the API keys. It complements —
doesn't replace — the strategy docs in Drive:

- Strategy / the *why* and *what*: Drive `02 Strategy/Craftons-Marketing-Engine-Plan.md` (phases 0–6) and `…-Notes.md` (decisions, targets, Gozney playbook).
- This doc: the *how to set it up and in what order*, plus every integration/key the engine needs.

_Drafted: 2026-06-13._

---

## Guiding principle — this is an ongoing project, so invest now

This is a **long-term, repeating build, not a one-off campaign.** Where an API key or
integration would make the work repeatable, **set it up properly now** rather than working
around it each time. We pay the setup cost once and get compounding efficiency for every
future session — on desktop *and* mobile.

Concretely:
- If a task will recur (trend radar, image/video gen, posting, pulling insights), wire the
  integration rather than doing it by hand.
- Prefer durable plumbing — MCP connectors enabled in the session environment, or scripts in
  the code repo that read keys from `.env` — over copy-paste workarounds.
- A new mobile/web Claude session should be able to do the work with the connectors and keys
  already in place. Setup friction is a one-time cost; manual workarounds are a forever cost.

## Where secrets live (non-negotiable)

- **API keys and tokens live in the cnccut.app code repo's `.env`** (and/or this repo's env
  if tooling is added here later). They are also configured as environment variables on the
  remote/web session environment so mobile sessions can use them.
- **Never** put keys, tokens, or `.env` files in the Google Drive brain. The brain is content
  and media only. (`.gitignore` here already excludes `.env*`.)
- MCP connector config and the Meta Ads CLI (`tools/meta-ads.mjs`) stay in the code repo, not
  the brain.

---

## Part A — Foundations (status)

| Step | What | Status |
|------|------|--------|
| A1 | `marketing-engine` repo created as the workspace + mobile entry point | ✅ Done |
| A2 | `CLAUDE.md`, `README.md`, `.gitignore` in repo | ✅ Done |
| A3 | Google Drive brain structure (`00 Brain` … `04 Newsletter`, `Campaigns`, `Video`, `Channels`) | ✅ Exists |
| A4 | Google Drive connector confirmed working in mobile repo-sessions | ✅ Confirmed 2026-06-13 |
| A5 | Repo ↔ Drive system map consistent across both `CLAUDE.md` files | ⏳ Drive-side edit pending (desktop) |

---

## Part B — Integrations & API keys (set these up now)

The core of the "invest now" principle. Grouped by priority. For each: what it unlocks, what's
needed, and where it lives.

### Already connected (Claude session connectors — usable now, incl. mobile)

| Integration | Unlocks | Status |
|-------------|---------|--------|
| Google Drive | The brain — read/write content & media | ✅ Connected |
| Gmail | Outreach, drafts, list/label triage | ✅ Connected |
| Google Calendar | Scheduling, reminders, content calendar entries | ✅ Connected |
| ClickUp | Task/reminder tracking, calendar precursor | ✅ Connected |
| Shopify | Product/sales data, store management | ✅ Connected |
| Xero | Financials (ROI / spend context) | ✅ Connected |
| GitHub | This repo + cnccut.app code | ✅ Connected |

### To set up for the engine (priority order)

| # | Integration | Unlocks | What's needed | Where key lives | Status |
|---|-------------|---------|---------------|-----------------|--------|
| B1 | **Replicate** | AI image + video gen (b-roll, extension, touch-up) | API token; ~$50–150/mo | code repo `.env` | ☐ To do |
| B2 | **Glif** | Templated image gen / ad-creative variants | API key / credits; ~$20–40/mo | code repo `.env` | ☐ To do |
| B3 | **Perplexity** | Trend Radar + market research | API key (already used for research 2026-06-12) | code repo `.env` | ☐ Confirm/persist |
| B4 | **Firecrawl** | Scrape inspo brands & competitor content for teardowns | API key | code repo `.env` | ☐ To do |
| B5 | **Later.com** | Scheduling/posting approved drafts | Account + API access | code repo `.env` | ☐ To do |
| B6 | **Meta / Instagram Graph API** | IG insights → dashboard; Meta ad creative + draft campaigns | Meta app, access token, IG business account linked; `tools/meta-ads.mjs` (CONFIRM=1 guardrail exists) | code repo `.env` | ☐ Wire token |
| B7 | **Google Ads API** | Draft search/awareness campaigns programmatically | Account exists; need API + developer token | code repo `.env` | ☐ To do (manual first OK) |
| B8 | **Klaviyo** (provisional) | Newsletter send + list off the calculator lead magnet | API key (confirm platform first) | code repo `.env` | ☐ Decide + set up |
| B9 | **Local media tooling** | Video/image assembly (`ffmpeg`, `sharp`/Pillow/OpenCV) | Install in env / setup script | n/a (no key) | ☐ Add to setup script |

> **Efficiency note:** for anything that should "just work" in future sessions, prefer enabling
> it as an MCP connector on the session environment, or add a setup/SessionStart script so the
> tooling and keys are present on every launch.

---

## Part C — Build sequence (step by step)

Sequenced so **posts flow in week one** while the bigger build happens behind it. Phase
rationale lives in the Drive Engine Plan; this is the actionable order.

### Step 1 — The Brain + first posts (Phase 0, Week 1)
1. Build the `00 Brain/` guideline docs: `brand-voice`, `social-voice` (punchier IG tone),
   `visual-style` (the anti-slop law), `content-pillars` (the 5), `trends-log`, `swipe-file`
   (seed with Gozney / July / BuildPass).
2. Finalise Drive folder conventions: `_inspo-dump/`, `_client-assets/`, `produced/` + a naming
   convention.
3. Queue 2–3 posts beyond the bench carousel so the feed is active immediately.
4. **Done when:** guidelines exist and posting has started this week.

### Step 2 — Intake + ideation loop (Phase 1, Weeks 2–3)
1. Inspo pipeline: dump → `_inspo-dump/` → Claude updates `trends-log` / `swipe-file` / `visual-style`.
2. Client pipeline: dump → `_client-assets/` → Claude returns caption + edited stills + a reel concept against a pillar.
3. Rolling 2-week calendar as a structured file, balanced across the 5 pillars.
4. Stand up the weekly **Trend Radar** (Mondays) → 3–5 Craftons-ready ideas *with example links*.
   *(Needs B3 Perplexity, B4 Firecrawl.)*

### Step 3 — Production system (Phase 2, Weeks 3–5)
1. Image: AI touch-up, design-system illustrations, Meta ad creative — Glif + Replicate; carousel templates. *(B1, B2.)*
2. Video: edit Tia's real footage into Reels + cuts; Replicate for AI b-roll/extension; ffmpeg assembly. *(B1, B9.)*
3. Wire the two-gate quality system: Gate 1 Claude self-checks vs `visual-style`+`social-voice`; Gate 2 Lee approves.

### Step 4 — Repurposing + newsletter (Phase 3, Weeks 5–7)
1. IG → LinkedIn repurposing (founder-led when LinkedIn activates).
2. Fortnightly newsletter: copy + layout + images; stand up Klaviyo; list off the calculator lead magnet. *(B8.)*

### Step 5 — The Cockpit dashboard (Phase 4, Weeks 6–9, parallel)
1. Build in **cnccut.app**: content calendar, asset library (indexes Drive), status pipeline
   (idea → draft → approved → scheduled → posted), performance (IG/Meta insights), ideas backlog. *(B6.)*

### Step 6 — Ads engine (Phase 5, Week 8+)
1. Meta: build creative + draft campaigns for approval; retarget configurator visitors first. *(B6.)*
2. Google Ads: capture existing demand (search) + awareness layer. *(B7.)*
3. Performance feeds the dashboard.

### Step 7 — Scale (Phase 6, later)
Founder-led LinkedIn (Jake/Lee); TikTok/YouTube if IG data justifies; LinkedIn ads.

---

## Part D — The operating loop (once set up)

The repeatable cycle every week:

1. **Dump** — inspo and client assets into Drive (`_inspo-dump/`, `_client-assets/`), incl. from phone.
2. **Draft** — Claude produces content against a pillar (caption + stills + reel concept), self-checked vs the brain (Gate 1).
3. **Approve** — Lee reviews; notes feed back into the brief; winners → swipe file (Gate 2).
4. **Schedule/post** — approved drafts → Later.com.
5. **Measure** — weekly scorecard: reach/post, saves, shares, profile visits, link clicks, follower growth %. Optimise for **saves + shares**.

**Control model:** Claude produces → Lee approves and posts. Nothing auto-publishes.

---

## Open items to unblock (parked, don't block setup)

- Tia's monthly capacity → sets Reels cadence.
- Ad budget $ + per-platform split.
- Email platform final call (provisional: Klaviyo).
- LinkedIn activation timing (founder-led).
- When/whether to add TikTok + YouTube.
