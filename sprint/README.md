# Launch Sprint dashboard — runbook

A **live document** for Lee & Jake tracking the 12-week sprint to the **Oct 1 2026** launch.
Built in the Craftons design system. Two data sections both pull from **ClickUp**; Extras and
targets are authored in the HTML.

- **File:** `sprint/launch-sprint.html` (self-contained, publishes as a Claude Artifact)
- **Live link:** https://claude.ai/code/artifact/e7c4a64e-0d5e-4583-993e-d457a20bb994
- **Refresh cadence:** weekly (automated routine + on demand)

## What it shows
1. **Products** — from ClickUp `Craftons ▸ Product Development` (list `901607662897`). Shown as a
   **tabbed list by the "Stage" custom field**: All · Research · Design · Development · Shopify · Live
   (pipeline order). Each product shows its stage chip + **% Done** (the "% Done" custom field);
   tap a row to expand owner / stage / build-step count / ClickUp link.
2. **Marketing** — from ClickUp `Craftons ▸ Launch Marketing` (list `901615813456`). 6 workstreams
   (parent tasks) each with subtasks. Status per item = the ClickUp task status.
3. **Extras** — scaffolded in the HTML (Website audit · Workshop additions · Updated design system).

## ClickUp IDs
- Space: Craftons `90161526396`
- Product Development list: `901607662897`
- Launch Marketing list: `901615813456`
  - Cockpit `86d3nkqer` · Ads `86d3nkqey` · Tia catalogue `86d3nkqf1` · Instagram `86d3nkqf4`
    · LinkedIn `86d3nkqf7` · Newsletter `86d3nkqfc`
- Product parents: Formwork Builder `86d1az1mj` · Concrete Stair Builder `86d2rw71v`
  · Formliners `86d22zhvy` · Foam Letters `86d240zd1` · Plastic Profiles & Moulding `86d2atkzr`

## Weekly refresh procedure (what the routine does)
1. Pull both lists from ClickUp:
   - Products: `clickup_filter_tasks({list_ids:["901607662897"], include_closed:true})` to list
     products, then `clickup_get_task(include:["custom_fields"])` on each to read **Stage** (field
     `e73762f7-1859-4de6-8ce9-d013731513ce`, dropdown → option name) and **% Done** (field
     `4eb35976-712a-445c-8d46-7c0968aa7969`, `value.percent_complete`). Use `include:["subtasks"]`
     if you also want the done/total step count.
   - Marketing: `clickup_get_task` on each Launch Marketing parent (`include:["subtasks"]`) for item statuses.
2. In `sprint/launch-sprint.html`, update the `PRODUCTS` array (`stage`, `pct`, `done`, `total`) and
   the `MARKETING` array, and set `LAST_SYNC` to today's date. New products/workstreams in ClickUp
   → add them to the arrays. New Stage options → add to the `STAGES` list in the HTML.
3. Re-publish to the **same** Artifact URL: `Artifact({file_path, url:"…e7c4a64e…"})`.
4. Commit the updated HTML to branch `claude/sprint-planning-doc-j69nxb`.

The countdown, sprint week, progress rail and readiness % are computed live in-browser from the
launch date — no need to touch them.

## Notes
- Fonts: the artifact CSP blocks the brand webfonts (Aeonik/Inter), so the page uses the brand's
  own defined system fallback stacks. If we ever host this outside the artifact sandbox, load the
  real faces from the Drive design-system `fonts/`.
- Control model: Claude drafts → Lee approves. Nothing auto-publishes.
