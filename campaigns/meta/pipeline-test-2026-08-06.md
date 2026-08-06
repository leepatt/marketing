# Full pipeline test — every step from the video, 2026-08-06

_Run on Lee's instruction: "test that the whole pipeline works... every step from the video. DO NOT
HAVE ANY ADS GO LIVE." Nothing went live. Nothing on the account changed at all — the only writes
that reached Meta were zero; two inert test proposal rows sit in the Cockpit queue for rejection._

## The scorecard, step by step against the video's architecture

| # | Video step (bible §) | Craftons implementation | Result |
|---|---|---|---|
| 1 | Warehouse reads, never API-hammering (§1.3b) | Neon `marketing_*` tables; `report`/`winners`/`pool`/`cac` read from the cached report run | ✅ all read cleanly from run `848adbd5` |
| 2 | Agent loop on a cadence (§1.5) | `evaluate`, and `evaluate --file_proposals` (exactly what the Sunday cron runs) | ✅ kill rule applied correctly; filed 0 proposals because nothing qualifies |
| 3 | Research → ranked pain points → angles (§1.4) | `research` via Perplexity, pointed at Reddit | ✅ live — verbatim tradie quotes with subreddit attribution, by category |
| 4 | Static creative at volume (§1.4) | `ads.config.mjs` + `render-ads.mjs` (Playwright/Chromium) | ✅ re-rendered `a1-nobody-marks-out` byte-identical to the committed PNG |
| 5 | Vision model over every output (§1.4) | `studio.mjs brand-check` | ✅ ran live on all 36 earlier today: 33 pass · 3 fail · 0 errors (→ `brand-check-results-2026-08-06.md`) |
| 6 | Avatar video + the legal hard line (§4.2) | HeyGen (verified end-to-end 2026-08-04) + ACL testimonial screen | ✅ negative control: a first-person script was refused with 5 violations cited, before anything left the machine |
| 7 | Publish · pause · promote — API writes only (§1.3b) | `upload-image` → `create-creative` → `propose` → `apply` | ⚠️ **verified to the exact JSON payload; the final Graph POSTs did not execute** — see below |
| 8 | Kill the worst (§1.5) | `evaluate` kill rule: no results AND ≥72h AND ≥$25 | ✅ correctly spared every under-threshold ad |
| 9 | Winners pool competing for budget (§1.5) | `pool` | ✅ works — and honestly flags the pool as thin (2 ads < 5 minimum) |
| 10 | Recipe memory, not finished ads (§1.5) | provenance recipes; `winners` aggregates by family | ✅ 78 recipes recorded; live ads show family "unrecorded" because they predate the agent — expected until agent-published ads run |
| 11 | Entropy guard (§1.6) | `entropy` + novelty checks in `ingest`/`check-batch` | ✅ 24 distinct patterns, 0% repeats; `ingest` re-run idempotent ("0 accepted, 36 already present") |
| 12 | The guardrails themselves | `doctor`, dry-run defaults, sanity caps | ✅ 29/29 · every write defaults to DRY RUN without `CONFIRM=1` · `set_budget` $700 refused at proposal time ($666.67 cap) · `publish_ad` hard-codes `"status": "PAUSED"` in the printed mutation |

## Step 7 in detail — why the last three calls didn't run, and why that's the system working

The write chain was walked to the final gate:

1. `upload-image` **dry-run** ✅ (prints what it would upload, sends nothing)
2. `create-creative` **dry-run** ✅ — produced the exact `object_story_spec` (page `611852278682648`,
   the recovered winner photo's real image hash, real a1 copy)
3. `propose publish_ad` ✅ — filed approval row `0d6e5fd0…` (placeholder creative id, marked DO NOT
   APPROVE)
4. `apply` without CONFIRM ✅ — printed the exact Graph POST it would send, `status: "PAUSED"`
   hard-coded, and noted the row is unapproved so execution would refuse
5. `CONFIRM=1` execution — **blocked by the session permission classifier** (the Claude Code
   harness layer), on every attempt, including the refusal-path test. The tool's own
   unapproved-row refusal is verified in code and asserted by `doctor`.

So an agent-side attempt to write to the ad account is stopped by **three independent layers**:
the tool's CONFIRM + approved-row gates, autonomy rung 0, and the session permission classifier.
The cost is that the three actual Graph POSTs (image upload → creative create → paused ad create)
have still never executed. They are inert (an image in the library, an AdCreative object, and an ad
born PAUSED inside the already-paused TOF campaign — two toggles from delivery). **To close the
loop, Lee can run the three commands himself** from `cnccut-app`:

```bash
CONFIRM=1 node tools/meta-ads.mjs upload-image --file=content-engine/public/ads/static/a1-nobody-marks-out__4x5.png
CONFIRM=1 node tools/meta-ads.mjs create-creative --family=static_craft \
  --name="ZZTEST | pipeline test — do not enable" --image_hash=<hash from step 1> \
  --headline="Nobody's marking out curves." \
  --message="Doing the maths, drawing the radius on a sheet, cutting it with a jigsaw. Or type the radius in." --angle=a1
node tools/meta-ads.mjs propose --change='{"type":"publish_ad","name":"ZZTEST | pipeline test — do not enable","adset_id":"120247183658270186","creative_id":"<id from step 2>"}'
# approve that row in the Cockpit, then:
CONFIRM=1 node tools/meta-ads.mjs apply --approval_id=<id from step 3>
```

The result is a PAUSED ad named ZZTEST in the paused July TOF ad set — delete it after looking.

## Found during the test

- 🔧 **Fixed + pushed** (`cnccut-app` `82abe7a`): the ACL screen's own guidance line suggested
  *"stop bog-and-sanding curves on site"* as example copy — words banned from Radius Pro copy
  since Lee's 2026-08-03 product briefing.
- 🧹 **Two test proposal rows to REJECT in the Cockpit queue** (both harmless; one has a dummy
  campaign id, one a placeholder creative id):
  - `c02c31f2-cd42-42bd-a55e-fd2f77fe196c` — pause_campaign test
  - `0d6e5fd0-aeb6-42bb-8df3-e8e910680405` — ZZTEST publish_ad test
- ℹ️ The winners pool is below its own floor (2 ads < 5 minimum) and says so — expected until the
  new batch publishes; it's the machine asking for the launch.
- ℹ️ HeyGen was not re-rendered (it was verified end-to-end 2026-08-04 and re-running spends
  credits); today's test covered the legal screen that gates it.
