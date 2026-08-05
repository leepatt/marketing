# Session refresh — run brand-check live, then finish launch prep

Continuing work in `/home/user/marketing` (repo `leepatt/marketing`). Goal of this session: **run
`brand-check` live on the 36-ad batch — the one built-and-never-run path — then finish launch prep.**

## Setup before anything else

1. **The Anthropic key is saved as `ANTHROPIC_KEY`, not `ANTHROPIC_API_KEY`.** Every tool reads the
   latter, so brand-check will report it missing unless you either rename the env var (preferred) or
   prefix each command. Same for the page ID: it is `PAGE_ID`, not `META_PAGE_ID`.
   ```
   export ANTHROPIC_API_KEY="$ANTHROPIC_KEY"
   export META_PAGE_ID="$PAGE_ID"
   ```
   Check keys by length/prefix only — never print a value.
2. **Branch:** `git checkout claude/craftons-meta-ads-launch-6m5ll0` (all work below is pushed there).
3. **Pull in the code repo** — not present in a fresh session:
   `add_repo(leepatt, cnccut-app)` → clone → `register_repo_root`, then
   `git checkout claude/craftons-real-footage-register`. **Branch from `main`, never from
   `claude/marketing-agents-setup-qamq2f`** (squash-merged, reads as unmerged, dead history).
   Deps: `npm install --no-save @neondatabase/serverless playwright` (Chromium is pre-installed).

## Where things stand

**The machine is verified working against the live account. The launch is gated on photography.**

- `doctor` **29/29** guardrails pass · `report` reads the account cleanly · `check-batch` **PASSES**
  at 3 families (36 creatives).
- 🆕 **The account's best-ever creative was recovered** — AD5's bare site photo (10.45% CTR, 9,244 LPVs
  at $0.08) was not in the repo at all. Pulled back by image hash; now
  `content-engine/sandbox/real/site-lawless-curved-stud-wall.jpg`. A new `bare` render template emits
  it with no overlay, which is what made it work.
- **AD4/AD5/AD6 all shared the identical image hash** and differed only by the identity word. That is
  the account's own proof that identity words multiply a proven winner rather than find one.
- **Long-form copy set written** (LF1–LF6) in the winner's six-paragraph register — the proven template
  that nothing in the 33-ad batch uses.
- **LAW 1 is now in the bible and asserted in code:** no ad goes live without Lee's approval. There is
  no mutation anywhere that sets an ad ACTIVE, and no autonomy rung grants one.
- **Australia-only** is enforced in `_meta-policy.mjs` and audited live by `report`.

**Three traps that have each cost a session:** don't research before searching (~25 branches; this repo
has lost the same work twice) · don't trust `git branch --contains` on cnccut-app (squash merges) ·
don't quote account figures from memory, run `report`.

## Next steps

1. **Run `brand-check` live on the 36-ad batch.** The whole point of this session. It sweeps every
   pending asset for a module, so no asset IDs needed:
   `node tools/studio.mjs brand-check` (see `--module`/`--asset_id` usage in the file header).
   ⚠️ **Do the duplicate cleanup FIRST (step 2) or it scores everything twice.**
2. 🔴 **Clean up 36 duplicate `pending` rows** — `marketing_assets` holds 72 rows for 36 creatives.
   The `ingest` bug is fixed; the existing rows are not. Scoped: `module='meta-ads' AND
   brand_check_status='pending'`, keep newest per title, never touch `pass`/`fail`/`skipped`.
   **Lee must approve — a previous DELETE attempt was blocked by the permission classifier.**
3. **Four non-AU ad sets** — one targets the US ($43.82, 0 results), three have no geo at all
   (= worldwide). All paused. Recommend deleting; **Lee's call**, it is an account write.
4. **Create the launch ad set** — Lee's 5-minute job, step-by-step already written. Then verify via API
   that `promoted_object` holds `custom_conversion_id: 27686282527680441` (not `custom_event_type`).
5. **Read EMQ by eye** in Events Manager → Craftons Web. Not exposed on the API.
6. **Rotate `META_ACCESS_TOKEN`** — Meta's `stats` endpoint embeds it in its own paging URL.
7. **The real lever: photography.** One phone photo beat a designed batch of 33 and there is still
   exactly one. Nothing an agent does unattended competes with this.

## Files to open (read these, don't re-derive)

- `STATUS.md` — read first. Doc index, every correction, the env-key table, the two git traps.
- `campaigns/meta/HOW-TO-create-the-ad-set.md` — the 5-minute ad-set build, the conversion-dropdown
  trap, and the full table of what stops an ad going live.
- `campaigns/meta/radius-pro-longform-copy.md` — LF1–LF6 in the winner's register. LF1 is the July
  winner with one word corrected ("laminate" is banned; "double them up" is the approved phrasing).
- `campaigns/meta/creative-strategy.md` — teardown of the one ad that worked; shot list at §4.1.
- `campaigns/meta/radius-pro-product-truth.md` — product source of truth in Lee's words. Wins on conflict.
- `campaigns/meta/ad-set-wiring.md` — why the agent cannot wire the conversion itself, and the EMQ finding.
- `campaigns/meta/META-ADS-AGENT-BIBLE.md` — **LAW 1 at the top**, autonomy ladder, architecture.
- `INTEGRATIONS.md` — env-var runbook, including the two misnamed keys.
- In `cnccut-app`: `tools/_meta-policy.mjs`, `tools/meta-ads.mjs`, `tools/studio.mjs`,
  `content-engine/ads/ads.config.mjs`, `content-engine/public/ads/static/_contact-sheet.png`
- Drive `MARKETING-BIBLE.md` + `META-ADS-BRIEF.md` via the Google Drive connector. **Both have been
  missed before and both times it cost days.**

## Standing rules (Lee)

- 🔒 **No ad goes live without Lee's explicit approval.** No exceptions, no rung.
- 🇦🇺 **Australia only.**
- Real footage leads, AI extends, a human approves every asset.
- Banned from Radius Pro copy: bog, kerf, curve bending, bendy-ply-as-the-problem, laminating, wiggle wood.
- Don't segment by trade at launch — identity words multiply a proven winner, they don't find one.
- Never paste a secret value into chat, a repo file, or the Drive brain.
