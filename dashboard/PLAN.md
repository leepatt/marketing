# Craftons Marketing Cockpit — master plan

_Draft 2026-06-30. Planning only — nothing is built or deployed yet. Lives in `cnccut.app`._

> **The idea in one line:** a single place inside cnccut.app where Lee sees every marketing channel's
> data *and steers it* — with Claude as the "brain" that watches the numbers, proposes moves, and
> applies the ones Lee approves with a click. Think **Go High Level**, but opinionated, gamified, and
> wired to an AI that actually does the work.

---

## 1. What it is (and isn't)

- **It is a cockpit, not a dashboard.** Dashboards show you numbers. A cockpit lets you *fly the
  plane* — see the instruments **and** pull the levers, with an autopilot (Claude) that suggests the
  next move.
- **Claude is the brain.** It reads the data, spots waste/opportunity, and writes **recommendations as
  click-to-apply cards**. Lee approves; the system executes. A chat bar runs along the bottom so Lee
  can ask "why did leads drop?" or "shift more budget to architraves" in plain English — exactly like
  this conversation, but embedded in the app.
- **It is not auto-pilot-without-a-pilot.** Carries over the existing control law: **Claude proposes →
  Lee approves → the system applies.** Nothing changes the live account (or posts anything) without an
  explicit human click. Every change is logged.

## 2. The core loop (this is the whole product)

```
        ┌──────────── DATA ───────────┐
        │ Pull from each channel's API │  Google Ads, Meta/IG, email, etc.
        │ → cache in a DB → show in UI │
        └───────────────┬──────────────┘
                        │
        ┌───────────────▼──────────────┐
        │           BRAIN (Claude)      │  reads the data via the same tools
        │ spots waste / opportunity →   │  we already built (google-ads.mjs …)
        │ writes structured ACTION CARDS│  + a conversational chat
        └───────────────┬──────────────┘
                        │  "Add negative 'guitar'"  [Apply] [Dismiss]
        ┌───────────────▼──────────────┐
        │        SURFACE (the UI)       │  KPI tiles, charts, tables,
        │ Lee reads + clicks Apply      │  recommendation feed, chat bar,
        └───────────────┬──────────────┘  gamification layer
                        │  click = approved
        ┌───────────────▼──────────────┐
        │     EXECUTE (gated writes)    │  the CONFIRM-gated tools run the
        │ tool runs → channel API →     │  change against the live account,
        │ result logged to audit trail  │  then the loop refreshes
        └──────────────────────────────┘
```

Everything below is just this loop, repeated per channel and dressed up well.

## 3. Three layers (the architecture)

**A. Data layer — connectors + store**
- One **connector per channel** that pulls metrics on a schedule and on demand, normalises them, and
  writes to a small database (snapshots + current state). The Google Ads connector is essentially
  `tools/google-ads.mjs` promoted to a server service.
- Store daily snapshots so we get **trends** (and so the gamification streaks/history work) without
  hammering each API.
- Creds stay **server-side only** (already rotated + in Vercel env). Never shipped to the browser.

**B. Brain layer — Claude + the engine**
- The recommendation engine and the chat are both **Claude (Agent SDK / Claude API)** with the
  marketing tools available to it — the same tools we've been running from this session.
- Two modes: **(1) scheduled** (the daily/weekly monitor already running → writes cards to the feed)
  and **(2) interactive** (Lee chats → Claude answers + proposes).
- Output is **structured actions**, not just prose, so the UI can render a button. (Schema in the
  module spec.)

**C. Surface layer — the UI**
- A shared **shell**: top KPI row, a channel switcher, a main panel, a **recommendations feed**, a
  persistent **chat bar**, and the **gamification** chrome (score, streak, quests).
- Each channel plugs into the shell as a **module** with the same shape (see §5). Build the pattern
  once on Google Ads, then every later channel is a repeat, not a rebuild.

## 4. Control & safety (non-negotiable)

- **Propose → approve → apply.** Every write is a human click. No silent changes.
- **Auth + audit.** Only Lee's authenticated session can apply. Every applied action is written to an
  audit log (what, when, who, before/after, result).
- **Guardrails on money.** Budget/bid changes have caps and a confirm step; spend can't be raised
  beyond a ceiling without an extra confirmation.
- **Secrets server-side.** API keys never reach the frontend; all channel calls go through the backend.

### Autonomy — graduated (decided 2026-06-30: "auto low-risk later")
- **Start strict:** every change is a click Lee approves. (Phases 1–4.)
- **Then graduate:** once Claude has a track record, let it **auto-apply only clearly-safe, low-risk
  actions** — e.g. adding obvious junk negatives ("guitar", "skateboard") — while **everything with
  money or reach still asks** (budget/bid changes, pausing keywords/ads/campaigns, creating/editing
  ads). Each action already carries a `risk` field (`low`/`med`/`high`) and a type — autonomy is just a
  per-type allow-list gated on `risk: "low"`.
- **Always auditable + reversible:** auto-applied actions still hit the audit log and surface in the
  feed as "auto-applied (undo)", so nothing happens invisibly and Lee can roll any of them back.

## 5. The module pattern (so it scales to everything)

Every channel is a **module** implementing the same contract:

| Part | What it provides |
|------|------------------|
| **Connector** | pull(): fetch + normalise metrics & entities; snapshot to DB |
| **KPIs** | the 4–6 headline numbers for the top tiles |
| **Views** | the detail tables/charts for that channel |
| **Actions** | the list of changes Claude can propose + the gated tool that applies each |
| **Brain prompt** | what "good/bad" looks like for this channel (so recommendations are smart) |
| **Game hooks** | how this channel feeds the score, streaks, and quests |

Build modules in this order (value + readiness):
1. **Google Ads** ← start here (engine already built, data already flowing). *Spec: `google-ads-module.md`.*
2. **Conversion/sales overview** (Shopify purchases + leads — already tracked).
3. **Meta / Instagram** (insights + ads) — token half-collected.
4. **Email / newsletter** (Shopify Email sends + opens/clicks).
5. **Social posting + content pipeline** (drafts → approve → schedule; LinkedIn, IG, etc.).
6. **Content/SEO** (the keyword plan + article performance).

## 6. Gamification — **LIGHT** (decided 2026-06-30)

Decision: keep it light — useful signals, not a full game. **Two mechanics only:**
- **Per-channel Health (0–100, traffic-light):** a quick "is this channel ok" read, blended from real
  outcomes (cost-per-lead vs target, CTR, % budget not wasted, ads approved, has conversions). Green/
  amber/red. Honest — tracks business results, not vanity.
- **Leak meter 💧:** a live "wasted spend" gauge — money going to 0-conversion search terms. Applying
  negatives visibly drops it, which gives instant, satisfying feedback without dressing it up as a game.

_Deliberately **out of scope** for now (can revisit later): the 0–1000 Marketing Score, streaks, XP,
quests/missions, badges/levels. We can add any of these later if the light version proves it wants more._

## 7. Tech stack (recommendation — confirm against cnccut.app)

> ⚠ This repo's scope doesn't include the `cnccut.app` code, so the stack below is a **recommendation
> to confirm** once we open that repo. The Vercel hints suggest a Next.js/React app already.

- **Frontend:** Next.js (React) — KPI tiles, charts (Recharts/Tremor), the feed, the chat bar.
- **Backend:** Next.js API routes / server actions (or a small service) holding the connectors, the
  gated write tools, and the Claude calls. Runs on Vercel alongside the app.
- **Brain:** Claude via the **Agent SDK / Claude API** (latest model), given the marketing tools.
- **Store:** a Postgres (e.g. Supabase/Neon) for snapshots, recommendations, audit log, game state.
- **Auth:** the app's existing auth, scoped so only Lee can apply actions.
- **Reuse:** the logic in `tools/google-ads.mjs` + `google-ads-launch.mjs` ports almost directly into
  the Google Ads connector + action handlers — we're not starting from zero.

## 8. Roadmap (phased; deploy nothing until a phase is locked)

- **Phase 0 — this plan** ✅ (you're reading it).
- **Phase 1 — Google Ads, read-only:** connector + KPI tiles + charts + tables. Just *see* the data
  beautifully. (Detailed in `google-ads-module.md`.)
- **Phase 2 — Recommendations feed:** Claude writes action cards (still read-only — cards are advice).
- **Phase 3 — Click-to-apply:** wire the gated writes behind the Apply buttons + audit log.
- **Phase 4 — Chat bar:** the embedded conversational brain (ask + propose inline).
- **Phase 5 — Gamification:** score, streaks, quests, leak meter.
- **Phase 6 — Next modules:** repeat the pattern for sales, Meta, email, social, content.

## 9. Open questions (to unblock the build later)

- **cnccut.app stack** — confirm framework/DB/auth so the plan's stack section is real, not assumed.
- **Repo access** — when we build, add the `cnccut.app` repo to a session (it's outside this repo's
  current scope).
- **Hosting of the brain** — Claude calls run server-side on Vercel? Or a separate worker for the
  scheduled monitor? (Vercel functions have time limits; the monitor may want a small worker/cron.)
- ~~How much autonomy~~ **DECIDED:** start strict; later auto-apply only `risk:low` actions, ask for
  everything with money/reach (see §4 "Autonomy — graduated").
- ~~Gamification appetite~~ **DECIDED:** light — Health score + Leak meter only (see §6).

---

### Where this connects to what's already running
- `tools/google-ads.mjs` / `tools/google-ads-launch.mjs` → become the Google Ads **connector + action
  handlers**.
- The **daily monitor** (scheduled Claude routine) → becomes the engine that **fills the
  recommendations feed**.
- The **propose→approve** control model → becomes the **Apply/Dismiss** buttons.
- So the dashboard isn't a new system — it's a **face on the engine we already built.**
