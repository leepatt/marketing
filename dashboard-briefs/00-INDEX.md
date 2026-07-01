# Craftons Marketing Cockpit — build briefs (index)

_The plan for building the marketing tools dashboard on **cnccut.app**. One brief per tool. Each is
written to be handed to a **fresh cnccut.app repo session** as its kickoff spec. Last updated 2026-07-01._

---

## What we're building

A **unified marketing cockpit** inside cnccut.app: one dashboard (shared shell, nav, auth, design
system, data layer) where each marketing tool is a module/route. The Google Ads dashboard scaffolding
already in the repo is the first module and the pattern to mirror.

Every tool is **hybrid**: a dashboard UI (view + approve + trigger) backed by a `tools/<name>.mjs`
script that Claude or a cron job runs — mirroring the existing `meta-ads.mjs` / `google-ads.mjs`
pattern (read-only by default, writes gated behind `CONFIRM=1` + a human approval step).

**Control model (non-negotiable, inherited from the marketing repo):** Claude drafts → Lee/Jake
approve → then it posts/sends/spends. Nothing auto-publishes.

## Build order

1. **`01-foundation-cockpit-shell.md`** — build this FIRST. Shared shell, auth, design system,
   data layer, the `docs/marketing/` doc-sync mechanism, and the `tools/*.mjs` conventions every
   other tool depends on.
2. Then the six tools, in any order (each is an MVP vertical slice, independently shippable):
   - `02-meta-ads.md` — Meta (FB/IG) ads: insights + human-approved campaign drafting
   - `03-image-video-generator.md` — on-brand image/video generation (Replicate/Glif + render pipeline)
   - `04-config-asset-creator.md` — turn a Craftons product configuration into on-brand marketing assets
   - `05-social-media-organiser.md` — FB/IG/LinkedIn content calendar + draft→approve→schedule pipeline
   - `06-newsletter-generator.md` — fortnightly newsletter draft + Shopify Email send
   - `07-seo-manager.md` — keyword/content/technical SEO tracking + brief generation
3. **`08-execution-order.md`** — dependency map, recommended build sequence, parallelisation, and the
   cross-session guardrails. Read this to decide *what to build when* and *what to build in parallel*.

## How to use a brief

Open a new session in the **cnccut.app** repo, on a new branch, and paste that brief's
**"Kickoff prompt"** (bottom of each file) as your first message. The prompt tells the session to
read the Foundation brief, respect the shared conventions, and build the MVP slice.

## The recurring answer: how tools read the marketing md files

A cnccut.app session **cannot** reach into the `leepatt/marketing` repo on its own — a web session is
scoped to one repo. So we **sync** the needed md files into cnccut.app under `docs/marketing/`
(mechanism specified in the Foundation brief). Each tool brief lists exactly which synced docs it
consumes. This keeps the app self-contained and versioned, with a repeatable refresh script.

## Source docs each tool draws on (in this repo, to be synced)

| Concern | Source file(s) |
|---|---|
| Brand rules / design tokens | `.claude/skills/craftons-design/BRAND.md`, `SOURCE.md`, `pipeline/tokens.css` |
| Brand voice / audience | `brand/voice-profile.md`, `brand/audience.md`, `brand/competitors.md` |
| Social voice | `SOCIAL-VOICE.md` |
| Content strategy | `CONTENT-PILLARS.md` |
| Quality / anti-slop law | `QUALITY-DOCTRINE.md` |
| Keyword / SEO plan | `brand/keyword-plan.md` |
| Ads assets & tracking | `campaigns/adwords/*` |
| Integrations & env vars | `INTEGRATIONS.md`, `SETUP.md` |
| Production pipeline | `pipeline/README.md`, `pipeline/templates/*`, `pipeline/tokens.css` |
| Status / decisions log | `STATUS.md` |

## Cross-cutting decisions already made (don't relitigate per session)

- **Docs access:** sync into cnccut.app `docs/marketing/` (not live cross-repo reads).
- **Tool nature:** hybrid UI + `tools/*.mjs` backend.
- **Architecture:** one unified cockpit, shared shell.
- **Depth per session:** ship an MVP vertical slice first, then iterate against the backlog.
- **Secrets:** live in cnccut.app `.env` + Vercel env vars. Never in the Drive brain, never in git.
- **Posting/sending/spending:** always human-gated (`CONFIRM=1` + UI approval).
