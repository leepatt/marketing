# Session refresh — continue with the marketing agent

Continuing work in `/home/user/marketing` (repo `leepatt/marketing`, branch
`claude/craftons-meta-ads-agent-sbgh3r`). Goal of this session: continue building the Craftons Meta
ads agent.

## Where things stand

**The machine is finished. The marketing is not.** That split is the whole picture.

**Scaffolding — complete and verified (2026-08-03).** 22/22 guardrail self-checks, `tsc` + `eslint`
clean. The full loop was run end-to-end for the first time — `report → evaluate → pool → entropy →
ingest → check-batch → propose → apply` — against the live account at autonomy rung 0. **The safety
spine held:** `apply` dry-ran without `CONFIRM=1`, and *refused outright* with `CONFIRM=1` against a
pending row. `check-batch` correctly failed the 6-ad batch. **No writes reached the ad account.**

Built this session: `ingest` (creative → assets with recipes), `pool` (winners), `entropy` (novelty),
`cac` (true CAC), Cockpit batch approval, image-based `brand-check` wired into the weekly cron.

**Bugs found and fixed by actually running things** — worth knowing the pattern, it recurred:
- `recentAssets` never selected `provenance`, so the recipe-learning loop had *always* been dead.
  Its failure mode is silence, not an exception.
- `pool` counted paused ads as live (filtered "not DELETED" vs `evaluate`'s "ACTIVE").
- `brand-check` scored a text prompt, not the image — it could pass an asset it had never seen.
- The no-key path marked assets `skipped`, which then dropped out of the `--pending` queue forever.

**🔴 The ad copy is not usable.** Lee flagged it; the audit was worse than tone. Three of six ads carry
claims that are wrong or overclaimed, and three more were asserted without verification. Root cause: I
never read `MARKETING-BIBLE.md` in Drive, which forbids exactly this — *"No verbatim quote = not ready
to write."* All six were written with zero verbatim customer language.

**Research done late but decisive** — three intel docs now exist, and they overturn the creative:
- Real orders are **90mm-wide curved stud-wall plates at multi-metre radii in 17mm formply**, qty 4–60
  — not the 900mm decorative arc the ads show.
- Part ID engraving **confirmed true**; turnaround is **2 days** not 3; *"nothing to fill at the join"*
  is **false** — **joiner blocks ship with every split**.
- The buyers are largely **PMs, site engineers and contracts administrators** at commercial
  contractors, not only people on the tools.
- **The unwritten pain: getting curved geometry into a cuttable file.** Plan views, Revit and IFC all
  arrive uncuttable. One job was lost to it. **Plan Scan solves this and is already live.**
- Nobody in the inbox says *"bog-and-sand"*, *"kerfing"* or *"bendy ply"* — all three are in my ads.

## Next steps

1. **Lee is supplying a Radius Pro description (what it does, who it's for) plus customer pain
   points.** Reconcile it against the three intel docs, then **rewrite all ad copy** from verbatim
   language. This is the blocker on everything creative.
2. **Get the product interview answered** — `campaigns/meta/radius-pro-interview.md` §1 lists the five
   claims currently sitting in rendered ads. Nothing goes live until those are cleared.
3. **Create the combined custom conversion** (`InitiateCheckout` OR `Purchase`, ~53/wk) — the last
   Phase 0 gate. Lee can do it in Events Manager, or Claude can create it via the API **on his
   explicit say-so** (it's an account write).
4. **Check EMQ > 7** — Advanced Matching went on 2026-08-03 and needs 24–48h. Not readable before then
   (`match_rate_approx` returns `-1`).
5. **Verify `brand-check`'s vision path.** Built but never run live — `ANTHROPIC_API_KEY` is in Vercel,
   not in the session env. The Sunday 22:00 UTC cron will be its first real run against the 6 ads.
6. Optional, only once copy is fixed: add a `--validation` escape hatch to `check-batch` so a 6-ad
   plumbing test can run without meeting the 15-ad *performance* floor.

## Files to open (read these, don't re-derive)

**In `/home/user/marketing` (this repo — already cloned):**
- `campaigns/meta/BUILD-CHECKLIST.md` — **start here.** Every item from both source videos with
  evidence, split into the machine (done) vs the marketing (not).
- `campaigns/meta/radius-pro-interview.md` — the questions blocking the copy rewrite.
- `research/market-intel/radius-pro-orders.md` — what customers actually order; overturns the creative.
- `research/market-intel/enquiry-language.md` — the market's own words; the file-format pain.
- `campaigns/meta/META-ADS-AGENT-BIBLE.md` — the agent design doc, with corrections inline.
- `campaigns/meta/launch-angles.md` — the three angles. ⚠️ Angle 2's headline uses language the inbox
  never uses; Angle 1 assumes a self-service buyer the inbox contradicts.
- `campaigns/meta/conversion-tracking.md` — Phase 0 step-by-step.
- `QUALITY-DOCTRINE.md` · `brand/audience.md` (⚠️ audience needs correcting per the intel).

**In Google Drive — READ BEFORE WRITING ANY COPY.** Folder `Peninsula Studio/01 Craftons/Marketing/`,
reachable via the Google Drive connector:
- `MARKETING-BIBLE.md` — the Sabri Suby doctrine, the Godfather Offer, the **verbatim law**, and the
  **8 hacks** in §9. This predates the build and was missed.
- `MARKETING-CHECKLIST.md` — the phased action list that pairs with it.
- `META-ADS-BRIEF.md` — not yet read.

**Other repos — ephemeral, must be re-added with `add_repo` then cloned:**
- `leepatt/cnccut-app` → branch **`claude/marketing-agents-setup-qamq2f`**. All agent code:
  `tools/meta-ads.mjs`, `tools/_meta-policy.mjs`, `tools/studio.mjs`, `content-engine/ads/`,
  `app/api/cron/meta-ads/route.ts`.
- `leepatt/animations` → branch **`claude/radius-pro-motion-graphic`**. The
  `craftons-motion-graphic-radius` skill (front-on 2D capture). ⚠️ Configurator video was **dropped by
  Lee** — do not resume it without being asked.
- `leepatt/craftons-curves-calculator` → the configurator. Run locally with
  `npx next dev -p 3210`; Radius Pro is at `/apps/radius-pro`.

## Carried-over data

**Branches (all pushed, all clean):** marketing → `claude/craftons-meta-ads-agent-sbgh3r` ·
cnccut-app → `claude/marketing-agents-setup-qamq2f` · animations → `claude/radius-pro-motion-graphic`

**IDs:** Pixel `677437638374055` · Business `1006792137511423` · Ad account `act_1650412872259063` ·
**Meta app `993965426717610` ("Craftons Ads API")** · Shopify `5e2910-9d.myshopify.com` ·
Radius Pro product `8464537125042` · Vercel team `Craftons`, project `cnccut-app`

**Token:** `META_ACCESS_TOKEN` is SYSTEM_USER and **never expires** (`expires_at: 0`, verified via
`/debug_token`). Scopes `ads_management, ads_read, business_management`. There is no refresh to build.

**Env split that keeps catching people out:** `ANTHROPIC_API_KEY`, `HEYGEN_API_KEY`, `META_APP_ID`,
`META_APP_SECRET` are **in Vercel but NOT in the session env**. Present in session:
`META_ACCESS_TOKEN`, `PERPLEXITY_API_KEY`, `REPLICATE_API_TOKEN`, `GLIF_API_TOKEN`, `DATABASE_URL`.
Replicate account is `cncjake`.

**Live numbers (30d, from `cac`):** spend $1,977.92 · revenue $17,285 · **ROAS 8.7×** · 33 checkouts →
13 purchases · **close rate 39.4%** (not the ~19% the tracking doc estimated) · cost/checkout $59.94 ·
**true CAC $152.15** — healthy, under the $178.94 target, half of $322.09 break-even.

**Warehouse:** `marketing_metrics_cache` 494 rows / 328 kB on Neon. **No Airbyte, no ClickHouse** —
deliberate, and correct at this size.

## Avoid repeating

- **Meta Ad Library API is impossible for AU**, not merely unapproved. Meta's own docs: ads that never
  reached the EU only return if political. An approved app returns an empty set. Do not apply.
- **Perplexity research needs `search_domain_filter` + ONE focused question per call.** A compound
  prompt returns vendor pages and looks like the seam doesn't exist. It does.
- **Reddit blocks Anthropic's crawler** — that's why research routes through Perplexity.
- **Chromium has no egress in this container.** Run apps locally and drive `127.0.0.1`.
- **Playwright's bundled ffmpeg is a stripped build** — no MJPEG decoder, no libx264. Use system
  ffmpeg (`apt-get install -y ffmpeg`).
- **Don't rebuild the configurator video.** Lee dropped it: the 2D set-out is right for a customer
  setting out a job and wrong for a stranger scrolling.
- **Don't segment ads by trade at launch** — July did and it cost $758/result. Suby's identity-keyword
  hack is a scaling lever on a *proven winner*, not a launch structure.
- **Don't write copy before reading the Drive bible.** That single miss caused the misleading ads.
