# CLAUDE.md — Craftons Marketing (workspace repo)

This repo is the entry point for working on Craftons marketing — especially from mobile, where Claude needs a GitHub repo to open a session. It orients the session and points at the brain. It is content/docs, not app code.

> The brain (guidelines, strategy, inspiration, content, media) lives in Google Drive: `Peninsula Studio/01 Craftons/Marketing/`. This repo points to it; it does not duplicate the media.

## The homes (don't mix them up)

- **This repo (`marketing-engine`)** — the marketing workspace + mobile entry point. Where you do the work: writing, planning, brand teardowns. Docs, not app code.
- **Google Drive `…/01 Craftons/Marketing/`** — the brain: media, assets, and content/strategy docs. Source of truth. Dump inspo here from your phone.
- **cnccut.app repo** — the dashboard/app code. It reads marketing data (from Drive and/or a database) to display it. It does not import this repo's files as code.
- **Later.com** — scheduling/posting. Approved drafts go here to be published.

**Control model:** Claude produces drafts → Lee approves and posts. Nothing auto-publishes.

## Accessing the brain

- Desktop: the Drive folder is mounted at `G:\.shortcut-targets-by-id\1V4uCnZGXyz6rAzmK_aJzGS2NseP9QURU\Peninsula Studio\01 Craftons\Marketing`
- Mobile: via the Google Drive connector (read/write Drive by API). Dump media from the phone's Google Drive app.

## Start here

- **This repo `STATUS.md` — the living status + plan. READ THIS FIRST each session** (what's done, what's next, open questions, doc index — so we never repeat work).
- This repo `SETUP.md` — the step-by-step setup sequence + the integrations/API-key checklist for standing the engine up.
- Drive `02 Strategy/Craftons-Marketing-Engine-Plan.md` — the phased build plan.
- Drive `02 Strategy/Craftons-Marketing-Engine-Notes.md` — decisions, targets, the Gozney playbook, benchmarks.
- Drive `01 Inspiration/README.md` — how we gather and tear down brands.

## Standing rules

- Build deliberately. Don't rush. Lock each piece before moving on.
- No guessing. Inspiration teardowns only for brands Jake/Lee nominate; build from observed content with receipts.
- Brand tone ≠ social caption tone.
- Real footage leads; AI extends. A human approves every asset.
- **Ongoing project — invest in integrations.** This is a long-term build, not a one-off. Where an API key or integration would make recurring work repeatable, set it up properly now rather than working around it — pay the setup cost once for compounding efficiency across future sessions. Keys live in the code repo's `.env`, never in the Drive brain. See `SETUP.md` for the integrations checklist.

## Status

Confirmed (2026-06-13): the Google Drive connector works in mobile repo-sessions. So this repo stays a thin entry-point shell — the brain lives in Drive, reached via the connector on mobile and the `G:` mount on desktop.
