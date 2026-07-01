# Brief 01 — Foundation: the Marketing Cockpit shell

**Build this before any tool module.** It defines the shared shell, conventions, and plumbing that
all six tools slot into. Ship it as its own MVP: an empty-but-real cockpit with nav, auth, the
design system, the data layer, the doc-sync, and one working `tools/*.mjs` reference implementation.

---

## 1. Goal

Stand up a single **marketing cockpit** in cnccut.app: one authenticated dashboard area where each
marketing tool is a module/route sharing nav, auth, the Craftons design system, a data layer, and a
`tools/*.mjs` backend convention. Reuse the existing Google Ads dashboard scaffolding — don't fork a
parallel pattern. When this is done, adding a tool = adding a route + a script that follow the
conventions here.

## 2. Users & control model

- **Users:** internal only — Lee and Jake. No public access. Keep auth simple but real.
- **Control model:** every outward action (post, send, spend, publish) is **human-gated**. The UI
  proposes; a person approves; only then does the backend execute. Backend write paths require an
  explicit `CONFIRM=1` env/flag in addition to the UI approval.

## 3. First: verify the existing app (do this before writing anything)

The briefs assume but must not trust the following — confirm in the repo first and adapt:

- Framework & hosting (assumed **Next.js on Vercel** — creds were placed in Vercel env vars).
- The existing **Google Ads dashboard scaffolding** location and shape — this is the template.
- Existing **`tools/meta-ads.mjs`** and any `google-ads.mjs` — copy their structure, arg parsing,
  env handling, and `CONFIRM=1` guardrail exactly.
- Current auth (if any), styling approach (Tailwind? CSS modules?), and data layer (DB? none yet?).
- The `.env` var names already present (Meta, Google Ads, Replicate, Glif, Perplexity, Firecrawl).
  **Match existing names; do not invent new ones.** See `docs/marketing/INTEGRATIONS.md` for the
  recommended convention, but the repo wins.

Write findings into a short `docs/marketing/APP-NOTES.md` so later tool sessions start from truth.

## 4. Doc-sync: `docs/marketing/` (the answer to "how do tools read the md files")

Tools need the marketing brain's md files. A session can't read another repo, so we sync a curated
set into cnccut.app and version them with the app.

**Deliverable:** `scripts/sync-marketing-docs.mjs` + a manifest.

- **Manifest** (`scripts/marketing-docs.manifest.json`): an allowlist of files to pull from
  `leepatt/marketing`, mapped to their destination under `docs/marketing/`. Start with the full
  "Source docs" table in `00-INDEX.md`.
- **Mechanism (pick the simplest that works in the repo's CI/local):**
  1. **Preferred:** fetch each file via GitHub's raw content API / `git archive` for the pinned
     branch, write to `docs/marketing/<path>`. No submodule, no live dependency at runtime.
  2. **Alternative:** `git submodule` or `git subtree` pinned to `leepatt/marketing`, with a thin
     `docs/marketing/` that re-exports the needed paths.
- **Refresh:** the script is idempotent and re-runnable ("pull latest brain into the app"). Commit
  the synced files so runtime never depends on network or connector access.
- **Pin & provenance:** record the source commit SHA in `docs/marketing/SYNC.md` on each run so we
  know how fresh the brain copy is.
- **Do NOT sync secrets.** The manifest is docs-only. `.env`, keys, tokens never get synced.

Every tool module reads brand context from `docs/marketing/…` at build/generation time — never
hardcodes brand rules inline.

## 5. The cockpit shell (UI)

- **Route:** `/marketing` (or wherever the Google Ads scaffolding already lives — extend it, don't
  duplicate). Left nav lists the modules: Overview, Google Ads, Meta Ads, Studio (image/video),
  Config Assets, Social, Newsletter, SEO. Unbuilt modules show a "Coming soon" placeholder so the
  nav is complete from day one.
- **Overview page (the MVP screen):** a cockpit home that surfaces, per module, a status card
  (last run, items awaiting approval, key metric). MVP can stub cards that later tools fill in.
- **Shared layout primitives** every module reuses: page header, section card, data table,
  stat/KPI tile, empty state, loading state, an **Approval drawer/modal** (the human gate UI —
  shows a proposed change/draft, Approve / Reject / Edit), and a **Run panel** (trigger a
  `tools/*.mjs` job, stream/show its output).
- **Design system:** implement the Craftons tokens from `docs/marketing/craftons-design/BRAND.md`
  and `pipeline/tokens.css` as the app's theme — dark forest green `#194431`, black, warm off-white
  neutrals (no blue cast), Aeonik display / Inter body, 4px spacing scale, 6px default radius, the
  curved-line motif behind hero text. **No gradients on UI surfaces, no emoji.** Add an adherence
  lint (flag raw hex/px/off-system fonts) mirroring the marketing repo's rule.

## 6. Data layer (shared)

Tools need to persist drafts, approvals, schedules, run history, and cached metrics. Define one
shared store the modules reuse — don't let each tool invent its own.

- **Recommendation:** a lightweight Postgres (Vercel Postgres / Neon / Supabase) with a small shared
  schema. If the app already has a DB, use it. If a DB is overkill for the MVP, a typed
  file/JSON store committed to the repo is acceptable for the first slice — but design the interface
  so swapping to Postgres later is a one-file change.
- **Core shared tables/entities (extend per tool):**
  - `runs` — every `tools/*.mjs` execution: tool, args, status, started/finished, output blob, cost.
  - `approvals` — proposed action, payload (draft/diff), status (pending/approved/rejected),
    approver, timestamps. The spine of the control model.
  - `assets` — generated media/copy: type, brand-check status, storage ref (Drive/Vercel Blob),
    linked module, provenance.
  - `metrics_cache` — pulled platform metrics (Meta/Google/Shopify/SEO), timestamped, so the UI
    isn't hammering APIs.
- **Media storage:** finished assets live in the Drive brain (source of truth) and/or Vercel Blob
  for fast web display. Record both refs on the `assets` row.

## 7. Backend convention: `tools/*.mjs`

Every tool ships a Node ESM script in `tools/` following the existing `meta-ads.mjs` shape:

- **Reads config from env** (keys from `.env` / Vercel). Never hardcode secrets; never log them.
- **Subcommands:** at minimum `report` (read-only, default) and one or more write actions.
- **Read-only by default.** Any write/outward action requires `CONFIRM=1`; without it the script
  prints the *proposed* change and exits without doing it (dry-run).
- **Writes a `runs` row** and returns structured output (JSON + a human-readable Markdown summary)
  the UI can render.
- **Idempotent & rate-limit aware.** Handle partial failures; surface them; back off on 429s.
- **Callable two ways:** from CLI (a human/Claude in a session) and from an API route the dashboard
  invokes (behind auth). Share the core as an importable module; the CLI and route are thin wrappers.

**Reference implementation:** build/confirm one end-to-end example (reuse `meta-ads.mjs report` or
`google-ads.mjs report`) that reads env, pulls a report, writes a `runs` row, and renders in the Run
panel. That proves the whole spine before tool sessions start.

## 8. Env / secrets

- All keys in cnccut.app `.env` + Vercel env vars. Confirm the names already present and document
  them in `docs/marketing/APP-NOTES.md`. Expected set (verify against repo):
  `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID`, `META_APP_ID`, `META_APP_SECRET`,
  `IG_BUSINESS_ACCOUNT_ID`, `GOOGLE_ADS_*` (6 vars), `REPLICATE_API_TOKEN`, `GLIF_API_TOKEN`,
  `PERPLEXITY_API_KEY`, `FIRECRAWL_API_KEY`, plus the Shopify connection for email/products.
- Never commit `.env`; confirm `.gitignore` covers `.env*`.

## 9. MVP vertical slice (what "done" means for this brief)

1. `/marketing` cockpit renders with the Craftons theme and full left nav (built + "coming soon").
2. Internal auth gates the area (Lee + Jake).
3. `docs/marketing/` exists, populated by `sync-marketing-docs.mjs` from a manifest, with a recorded
   source SHA.
4. Shared data layer live with `runs` + `approvals` tables (or the typed file-store interface).
5. Shared UI primitives exist: Approval drawer, Run panel, data table, KPI tile, empty/loading.
6. One reference `tools/*.mjs` runs end-to-end (report → `runs` row → rendered in Run panel).
7. `docs/marketing/APP-NOTES.md` documents the stack, env var names, and conventions for later
   sessions.

## 10. Post-MVP backlog

- Role/audit log on approvals; notifications (email/Slack) when items await approval.
- Cron scheduling for `report` runs (weekly digests) → Overview cards.
- Cost tracking rollup across tools (Replicate/Glif/ad spend) with Xero context.
- A settings page surfacing which integrations are wired/healthy (ping each API).

## 11. Open questions to confirm with Lee

- Auth: reuse cnccut.app's existing auth, or a simple internal gate (email allowlist)?
- DB: does cnccut.app already have Postgres, or do we provision one for the cockpit?
- Where should finished media live as source of truth — Drive brain only, or mirror to Vercel Blob?

---

## Kickoff prompt (paste into a fresh cnccut.app session)

> Build the **Marketing Cockpit foundation shell** in this repo. Read `docs/marketing/` if present;
> otherwise first create the doc-sync that pulls the Craftons marketing brain into `docs/marketing/`.
> Follow the brief `01-foundation-cockpit-shell.md` (I'll paste it / it's in the marketing repo).
>
> Before writing code: scan this repo and document the stack, the existing Google Ads dashboard
> scaffolding, `tools/meta-ads.mjs`, auth, styling, data layer, and the `.env` var names in
> `docs/marketing/APP-NOTES.md`. Then build the MVP slice from §9: a themed, auth-gated `/marketing`
> cockpit with full nav, the `docs/marketing/` sync script, a shared data layer (`runs` +
> `approvals`), shared UI primitives (Approval drawer, Run panel, table, KPI tile, states), and one
> reference `tools/*.mjs` running end-to-end. Reuse the existing Google Ads scaffolding and the
> `meta-ads.mjs` `CONFIRM=1` guardrail pattern — do not fork a parallel style. Human-gate every
> outward action. Work on a new branch, commit in logical steps, and don't build tool modules yet.
