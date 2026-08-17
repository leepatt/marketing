# Session refresh — fix the Meta ads

Continuing work in `/home/user/marketing` (repo `leepatt/marketing`, branch
`claude/craftons-meta-ads-launch-6m5ll0`). Goal of this session: **fix the Meta ads.**

## Setup before anything

1. **Branch:** `git checkout claude/craftons-meta-ads-launch-6m5ll0` — all work is pushed there.
2. **Env var names are wrong and must be aliased** (this has cost two sessions):
   ```
   export ANTHROPIC_API_KEY="$ANTHROPIC_KEY"   # saved as ANTHROPIC_KEY
   export META_PAGE_ID="$PAGE_ID"              # saved as PAGE_ID
   ```
   Check keys by length/prefix only. Never print a value.
3. **Pull in the code repo** (not present in a fresh session): `add_repo(leepatt, cnccut-app)` → clone →
   `register_repo_root` → `git checkout claude/craftons-real-footage-register` →
   `npm install --no-save @neondatabase/serverless playwright`. Chromium is pre-installed.
   **Branch from `main`, never from `claude/marketing-agents-setup-qamq2f`** (squash-merged, dead history).

## Where things stand

**Ads are LIVE-CAPABLE but PAUSED. Two faults were found; one is fixed, one is Lee's to fix.**

- **Fault 1 — FIXED.** The Aug26 ad set optimised on custom conversion `27686282527680441`, which has
  **never fired in 14 days** while the pixel logged events normally. Meta had no signal, so delivery
  collapsed 86% ($63 → $15/day) and $192.08 bought **0 attributed conversions**.
  A published ad set **cannot be repointed** (Meta: *"You can't edit your pixel, conversion event,
  custom conversion or optimisation for an ad set after the ad set has been published"*), so it was
  rebuilt: **v2 ad set `120247812165960186`** on the **standard `InitiateCheckout`** event, byte-identical
  to v1 otherwise. v1 retired. Both PAUSED, 6 ads each.
- **Fault 2 — OPEN, Lee's action.** Match quality is broken. 11 advanced-matching fields configured,
  **only `external_id` arriving**. `matched_entries: 0`, `match_rate_approx: -1`,
  `/da_checks` → `[failed] Pixel has low event source match rate`, and Meta's UI says
  **"$118 ad spend affected by low data quality"**. Fix is the Shopify → Meta data-sharing level.
- **The pattern behind both campaigns:** pre-launch gates were marked verified after checking that
  something was *configured*, not that it *worked* — the conversion, and Advanced Matching. Both were
  written as ✅ in the checklist.
- **Now enforced in code, not prose:** `judgeLaunchReadiness()` refuses activation when the target
  conversion has never fired, when EMQ is unacknowledged, when the pixel is stale/unavailable, when
  there is no conversion target, plus AU-only and budget caps. **Verified against the real broken ad
  set — it blocks it.** `doctor` is 54/54.
- **Creative is not the problem:** 3.58% link CTR, 96.9% click→page-load, LPV→ATC **0.9% vs July's
  0.16%**. Note `report`'s headline CTR is engagement-inflated — **always use `inline_link_clicks`**.
- **Budget $65/day** (fits the $2,000 ceiling for a full month). Retargeting is ACTIVE and produces all
  the account's attributed results — leave it, and read the test **blended at account level**.

## Next steps

1. **Confirm nothing changed while away** — run `doctor` and `report`, and re-read the v2 ad set's
   `promoted_object`. Never quote account figures from memory.
2. **If Lee says the Shopify data-sharing fix is done:** re-run the `match_keys` +
   `matched_entries` check on pixel `677437638374055`. Real identifiers (`em`, `ph`) arriving = fixed.
   This is machine-checkable — do not take it on trust.
3. **Then activate v2:** propose `activate_campaign` (already ACTIVE), `activate_ad_set` and the 6
   `activate_ad` changes **with `emq_acknowledged: true`** once Lee has confirmed EMQ. Lee approves,
   then apply. The gate refuses without the acknowledgement — by design.
4. **If match quality is NOT yet fixed:** recommend holding. Launching into a "$118 affected by low
   data quality" penalty repeats spending on weak signal. Lee's call, but that is the advice.
5. **Delete the US-targeted boosted post** — `Instagram post: CAMPBELL STREET`, spent $43.82 for 0
   results, targets the **US**. The Marketing API refuses it (*"can only be deleted on your Page"*);
   Lee must remove it from the Page. Last thing breaching Australia-only.
6. **After launch:** first readable signal ~72h; kill rule = ≥72h AND ≥$25 AND zero results (and
   **never kill while results cannot be counted**); readable CAC ~3–4 weeks. Budget ladder
   $65 → $78 → $94 → $100 cap, one step/week, only at CAC ≤ $322.

## Files to open (read these, don't re-derive)

- `campaigns/meta/RUNBOOK-lee-tasks.md` — **start here.** Lee's remaining tasks, current object states,
  and the full object-ID reference (ad account, datasets, all v2 ad + creative IDs).
- `campaigns/meta/aug26-post-mortem-and-salvage-plan.md` — both root causes, the rebuild record, the
  phased plan to sales, and a 10-point learnings ledger.
- `campaigns/meta/monitoring-and-reward-plan.md` — the reading log (16h / 72h / 83h), the cut-and-budget
  decision ladder, and why the kill rule was refused.
- `campaigns/meta/BUILD-CHECKLIST.md` — top section records that the checklist was correct and not
  executed, and which items are now code-enforced.
- `STATUS.md` — doc index, every correction, the env-key table, the two git traps.
- `campaigns/meta/radius-pro-product-truth.md` — product source of truth, Lee's words. Wins on conflict.
- `campaigns/meta/radius-pro-longform-copy.md` — LF1–LF6, the winner's proven long-form register.
- `campaigns/meta/pool-builders.md` — pool use case confirmed from orders (formwork, not set-out); LF7
  written and gated.
- In `cnccut-app`: `tools/_meta-policy.mjs` (`judgeLaunchReadiness`, `checkTargeting`,
  `DEFAULT_TARGETING`), `tools/meta-ads.mjs` (change types, activation preflight), `tools/studio.mjs`
  (`buildBrandCheckPrompt`, the footage rubric).
- Drive `MARKETING-BIBLE.md` + `META-ADS-BRIEF.md` via the Google Drive connector. **Both have been
  missed before and both times it cost days.**

## Standing rules (Lee)

- 🔒 **No ad goes live without Lee's explicit approval.** LAW 1, amended 2026-08-13 so he can approve
  *through Claude* — the mechanism moved, the requirement did not. No rung grants activation.
- 🇦🇺 **Australia only.** Enforced by `checkTargeting()`; an ad set with no geo fails too.
- Real footage leads, AI extends, a human approves every asset.
- Banned from Radius Pro copy: bog · kerf · curve bending · bendy-ply-as-the-problem · laminating ·
  wiggle wood.
- **Don't segment by trade until an ad wins.** LF4/LF5/LF7 are written and gated.
- Never paste a secret value into chat, a repo file, or the Drive brain.
- **Verify function, not configuration.** Both failed campaigns trace to marking a setting ✅ without
  proving it worked.
