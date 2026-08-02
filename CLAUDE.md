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

- **`DRIVE-INDEX.md` — what's in the Drive brain and where. READ BEFORE ANY MARKETING WORK.**
  Drive holds the doctrine (`MARKETING-BIBLE.md`), the execution plan (`MARKETING-CHECKLIST.md`),
  the ad briefs and the customer research. **Never conclude something "isn't documented" without
  checking Drive** — that claim has already been made once and was wrong.
- **This repo `STATUS.md` — the living status + plan. READ THIS FIRST each session** (what's done, what's next, open questions, doc index — so we never repeat work).
- This repo `SETUP.md` — the step-by-step setup sequence + the integrations/API-key checklist for standing the engine up.
- Drive `02 Strategy/Craftons-Marketing-Engine-Plan.md` — the phased build plan.
- Drive `02 Strategy/Craftons-Marketing-Engine-Notes.md` — decisions, targets, the Gozney playbook, benchmarks.
- Drive `01 Inspiration/README.md` — how we gather and tear down brands.

## ⛔ PAID ADVERTISING — HARD GATE (read before touching any ad account)

**No campaign spends real money until `campaigns/ADS-PREFLIGHT-CHECKLIST.md` is filled in with
evidence and Lee has approved it.** Not "reviewed" — filled in, pasted to Lee, approved.

This is not advisory. It exists because in July 2026 a Meta campaign spent **$1,711 and produced
2 orders** while sales *fell*, and it damaged the retargeting audience that was working. The full
account is in `campaigns/POST-MORTEM-2026-08-02.md`. Read it before proposing any ad work.

The four rules that matter most, if you read nothing else:

1. **Shopify is the scoreboard — never the ad platform.** Do not report an ad as performing without
   cross-checking actual orders in Shopify. Clicks, CTR, CPC, reach and impressions are not results.
   If asked how a campaign is doing, the answer leads with orders or it isn't an answer.
2. **No spend before tracking is proven** — a real conversion event visible in the campaign's own
   reporting, not a site-wide pixel that "looks installed." A site-wide green light is not proof.
3. **Cheap clicks and high CTR on a cold audience are red flags, not wins.** Under ~20c CPC or over
   ~3% CTR means investigate, not celebrate.
4. **Zero conversions after meaningful spend means tracking is broken until proven otherwise.**
   Never read it as "early days."

Every change made to a live ad account gets logged in `campaigns/meta/meta-change-log.md` (or the
equivalent for the channel) with the API response that confirmed it — including changes that failed.

**Check Drive before assuming something wasn't documented.** The July campaign *was* briefed —
Drive `02 Strategy/META-ADS-BRIEF.md`, dated the day before launch — but nothing in this repo pointed
to it, so a repo-side session found the campaign only by querying the API. When ad work spans both
homes, cross-link them.

## Standing rules

- Build deliberately. Don't rush. Lock each piece before moving on.
- **No guessing, especially about causes.** State what the data shows; label inference as inference.
  (A first draft of the Meta audit inferred from a campaign name that an outside agency was
  responsible and wrote it up as a finding. It was wrong, and it shifted blame off Claude.)
- No guessing. Inspiration teardowns only for brands Jake/Lee nominate; build from observed content with receipts.
- Brand tone ≠ social caption tone.
- Real footage leads; AI extends. A human approves every asset.
- **Ongoing project — invest in integrations.** This is a long-term build, not a one-off. Where an API key or integration would make recurring work repeatable, set it up properly now rather than working around it — pay the setup cost once for compounding efficiency across future sessions. Keys live in the code repo's `.env`, never in the Drive brain. See `SETUP.md` for the integrations checklist.

## Status

Confirmed (2026-06-13): the Google Drive connector works in mobile repo-sessions. So this repo stays a thin entry-point shell — the brain lives in Drive, reached via the connector on mobile and the `G:` mount on desktop.
