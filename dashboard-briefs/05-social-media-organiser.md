# Brief 05 — Social Media Organiser (FB · IG · LinkedIn)

_Depends on Brief 01. Consumes assets from Briefs 03/04. This is the "Cockpit" content pipeline._

---

## 1. Goal

A social command centre: a **content calendar** + a **status pipeline** (idea → draft → approved →
scheduled → posted) across **Facebook, Instagram, and LinkedIn**, balanced across the content pillars,
with performance pulled back in. Claude drafts captions + attaches assets against a pillar; Lee
approves; approved items get scheduled/posted. This is the operating loop from `SETUP.md` Part D made
into a tool.

## 2. Why it exists

Cadence is ~3 Reels + 1–2 carousels/week (~12–20 posts/mo) but Tia supplies only ~2–3 hero pieces/mo,
so the calendar must be deliberately balanced (hero footage + in-workshop + site spotlight + configure
screen-recordings + carousels + AI b-roll). Doing that in spreadsheets/Later alone loses the thread.
This tool holds the plan, the drafts, the approvals, and the scorecard in one place.

## 3. Users & control model

Internal. **Claude produces → Lee approves → then it posts. Nothing auto-publishes.** Two gates:
Gate 1 = Claude self-checks each draft vs `SOCIAL-VOICE.md` + brand rules; Gate 2 = Lee approves in
the UI. Value-first law: ~85% of posts add value / mention brand barely; soft CTAs only.

## 4. Inputs

**Synced brand docs (`docs/marketing/`):**
- `CONTENT-PILLARS.md` — the pillars/lanes (How-To, Built with Craftons, Craft Macro, Formwork
  Showcase, flagship "How This Curve Was Built") — the calendar balances across these.
- `SOCIAL-VOICE.md` — the caption voice (dry humour, no emoji, value-first, brand barely there).
- `craftons-design/BRAND.md` — visual rules for attached assets.
- `.claude/skills/content-atomizer/SKILL.md` — repurpose one piece into per-platform variants
  (IG vs LinkedIn tone/format).
- `SETUP.md` Part D — the operating loop + the weekly scorecard metrics (optimise for saves + shares).

**Live data / APIs:**
- **Meta/IG Graph API** (`tools/meta-ads.mjs` insights, or a sibling `tools/social.mjs`) — publish
  to FB/IG + pull organic insights. Env: `META_ACCESS_TOKEN`, `IG_BUSINESS_ACCOUNT_ID`, page id.
- **LinkedIn** — needs an API decision (see Open Questions); founder-led, activates later.
- **Later.com** — **no public API (confirmed)**. Default = **manual**: approved drafts export to load
  into Later. Optionally add an API-first scheduler (Postproxy/Ayrshare) later if manual is the
  bottleneck.
- **Google Calendar / ClickUp** (connected) — mirror the calendar / reminders if useful.
- Assets come from the Studio (Brief 03) + Config Asset Creator (Brief 04) asset library.

## 5. MVP vertical slice

**A working content calendar + draft→approve→export pipeline for IG (one platform end-to-end).**

1. Calendar view (week/month) with slots; each slot = a post with pillar, platform, caption, asset,
   and a status (idea/draft/approved/scheduled/posted).
2. Create a draft: pick a pillar + attach a library asset → `tools/social.mjs draft` generates a
   caption in `SOCIAL-VOICE` (via content-atomizer logic) + Gate 1 self-check flags.
3. Approval drawer → approve → item moves to `approved`.
4. **Publish path:** since Later has no API, MVP = **export an approved post** (caption + asset +
   suggested time) as a ready-to-load package for Later, and mark `scheduled`. (If a scheduler API is
   chosen, wire direct scheduling instead.)
5. Pull IG insights back onto posted items (reach, saves, shares, profile visits) via the Meta API.

## 6. Backend — `tools/social.mjs`

- `draft --pillar <p> --asset <id> [--platform ig|fb|li]` — caption + platform variants; Gate 1 check.
- `export --post <id>` — package approved post for Later (or `schedule` if a scheduler API exists;
  `CONFIRM=1` for any direct publish).
- `insights [--days 7]` — pull organic performance → `metrics_cache` → scorecard.
Direct publishing (if enabled) is `CONFIRM=1`-gated and only for approved posts.

## 7. Frontend — Social page

- Calendar (week/month) + Kanban status board (idea→…→posted) — two views of the same posts.
- Post editor: pillar, platform tabs (IG/FB/LinkedIn variants), caption, asset picker (from library),
  Gate 1 flags, schedule slot. Approval drawer.
- Scorecard: reach/post, saves, shares, profile visits, link clicks, follower growth % — optimise for
  saves + shares. Pillar-balance widget (are we over/under-weight on a lane this fortnight?).

## 8. Data model additions

`social_posts` (pillar, platform, caption(s), asset_id, status, scheduled_at, posted_at, external_id),
`social_metrics` (post_id, platform, metric, value, pulled_at). Reuse `approvals`, `assets`, `runs`.

## 9. Post-MVP backlog

- Direct IG/FB scheduling (if we adopt Postproxy/Ayrshare) instead of manual Later export.
- LinkedIn founder-led activation (Jake/Lee) once the API path is decided.
- Auto-fill the rolling 2-week calendar balanced across pillars from the asset backlog.
- Repurpose flows: one hero piece → multi-platform variants in one action (content-atomizer).
- TikTok/YouTube if IG data justifies (Phase 6).

## 10. Guardrails, safety

Nothing auto-posts; every post is Gate 1 + Gate 2 gated. No emoji, value-first, soft CTAs (enforced in
the draft check). Respect platform rate limits.

## 11. MVP acceptance criteria

- [ ] Calendar + status pipeline works for IG posts end-to-end.
- [ ] A draft caption generates in `SOCIAL-VOICE` with Gate 1 flags, attaches a library asset.
- [ ] Approve → export a Later-ready package (or schedule via API) → status updates.
- [ ] IG insights pull back onto posted items into a scorecard.

## 12. Open questions

- **LinkedIn:** use the LinkedIn Marketing API (app + review needed), or manual-export like Later to
  start? Founder-led timing?
- Stay **manual via Later**, or adopt an API scheduler (Postproxy/Ayrshare) now?
- Is a Facebook Page publish token available alongside IG, or IG-only to start?

---

## Kickoff prompt (paste into a fresh cnccut.app session)

> Build the **Social Media Organiser module** following brief `05-social-media-organiser.md` and the
> shared conventions in `01-foundation-cockpit-shell.md`. Foundation shell + `docs/marketing/` +
> the asset library (Brief 03) should exist. Ship the MVP for **Instagram** end-to-end: a content
> **calendar + status pipeline** (idea→draft→approved→scheduled→posted) on `/marketing/social`, a
> `tools/social.mjs draft` that writes captions in `SOCIAL-VOICE` (value-first, no emoji) with a Gate-1
> self-check and attaches a library asset, the shared Approval drawer for Gate 2, and — since Later has
> no API — an **export** step that packages an approved post for Later and marks it scheduled. Pull IG
> organic insights back into a scorecard (optimise for saves + shares). Nothing auto-posts. Leave
> FB/LinkedIn as stubs pending the API decisions in the brief. New branch, logical commits.
