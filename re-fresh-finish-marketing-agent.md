# Session refresh — finish and implement the marketing agent

Continuing work in `/home/user/marketing` (repo `leepatt/marketing`, branch
`claude/craftons-meta-ads-marketing-qif4cl`). Goal of this session: **finish and implement the Craftons
Meta ads marketing agent** — get it from "built but never fired in anger" to actually running.

## Where things stand

**The machine is finished and merged. The marketing is not.** Be precise about which half you're
working on — the recurring failure in this project is treating creative problems as code problems.

- **Agent code: DONE and shipped.** `leepatt/cnccut-app` `main` @ `5cd7910` (PR #97,
  squash-merged 2026-08-04). 15 subcommands, 22/22 guardrail self-checks passing, full loop run
  end-to-end at autonomy rung 0 (propose-only), weekly cron filing proposals. It cannot spend.
- **Creative: 33 ads built, brand-guide accurate, unreviewed and not launch-ready.** They still fail
  `check-batch` on **2 families vs a minimum of 3** — not fixable by effort, because every image asset
  in the repo is a CGI product render on white.
- **Custom conversion created and verified** (`27686282527680441`). Nothing points at it yet.
- **The account is NOT a cold start and NOT paused** — retargeting has been live at $15/day and made a
  purchase. Read live figures with `meta-ads.mjs report` before quoting any number.
- **Three env keys were added 2026-08-04** (`ANTHROPIC_API_KEY`, `HEYGEN_API_KEY`, `META_PAGE_ID`) and
  have never been usable, because env vars load only at session start. **This session is the first that
  can see them.**

### Key decisions already locked (don't relitigate)

- **One broad AU ad set.** Identity words go in the *creative*, never in targeting. Enforced by
  `MAX_AD_SETS = 1`.
- **Optimise for purchases, not attention** — Lee: *"we want sales, not attention."* July's failure was
  the optimisation event, not the trade-identity creative.
- **Real footage leads, AI extends. A human approves every asset.** Autonomy rung 0 stands.
- **The Residency brand guide is a *posting* system, not an advertising system.** It's one register
  among five, not the house style for cold traffic.
- **Banned from all Radius Pro copy:** bog · bogging · kerf · kerfing · curve bending · bendy-ply-as-the-
  problem · laminating · wiggle wood. Lee: *"that's just not related to the job at all."*

## Next steps

1. **Verify the five env vars are visible.** Check presence by length/prefix — never print a secret's
   value. If `ANTHROPIC_API_KEY` 400s on credit balance, that's billing, not the key: API credit is
   separate from Lee's Max subscription.
2. **Pull in the code repo** — it is not in a fresh session. `add_repo(leepatt, cnccut-app)` → clone →
   `register_repo_root`. Branch from `main`, never from `claude/marketing-agents-setup-qamq2f`
   (squash-merged, so it reads as unmerged but is dead history — details in `STATUS.md`).
3. **Run `brand-check` live on the 33-ad batch.** Built, wired to the cron, **never once run against a
   real image.** Needs `ANTHROPIC_API_KEY`. This is the first honest test of its vision path.
4. **Run `doctor` and `report`** to confirm the agent still reads the live account cleanly.
5. **AI avatar tests** — needs `HEYGEN_API_KEY`. ⚠️ ACL constraint already enforced in
   `_meta-policy.mjs`: a synthetic presenter may *describe* the product but must **never claim
   first-person experience** of it (ACL s18 / s29(1)(e)). Scripts stay second-person about the product.
6. **Wire the ad set to the custom conversion** — `promoted_object` → `27686282527680441`.
7. **Check EMQ > 7** — needs 24–48h of pixel traffic from 2026-08-03, so readable from 2026-08-04.
8. **The creative work that actually decides the launch** — see the honest-blocker note below.

## Files to open (read these, don't re-derive)

- `STATUS.md` — **read first.** Living status; carries the doc index, the search protocol, every
  correction, the env-key table, and the "where the agent code lives" section with the two git traps.
- `campaigns/meta/creative-strategy.md` — the teardown of the one ad that actually worked, the
  five-register mix, and the precise blockers. **The most important doc for the creative half.**
- `campaigns/meta/radius-pro-product-truth.md` — product source of truth, in Lee's own words. Wins over
  every other doc on conflict. Carries the banned-words list.
- `campaigns/meta/launch-readiness.md` — verified account state, hard blockers, test expectations.
- `campaigns/meta/suby-8-hacks-implementation.md` — the 8 hacks mapped to actions, plus the retracted
  July post-mortem with corrected data.
- `campaigns/meta/META-ADS-AGENT-BIBLE.md` — scope, the 5-rung autonomy ladder, architecture.
- `INTEGRATIONS.md` — env-var runbook and which keys are actually worth having.
- Drive `MARKETING-BIBLE.md` + `META-ADS-BRIEF.md` — via the Google Drive connector. **Read them.**
  Both have been missed before and both times it cost days.

In `cnccut-app` after cloning: `tools/_meta-policy.mjs`, `tools/meta-ads.mjs`,
`content-engine/ads/ads.config.mjs`, `content-engine/public/ads/static/_contact-sheet.png`.

## The honest blocker (say this to Lee early, don't bury it)

Steps 3–7 are the ones an agent can do unattended, and they are the **smaller** lever.

The single best-performing creative the account has ever run — **10.45% CTR, 9,244 landing page views
at $0.08** — is a bare phone photo of a curved timber stud wall on a real slab. No overlay, no logo,
nothing designed on it. **There is exactly one such photo.** Everything else in the repo is a CGI
render on white, which is also precisely why `check-batch` fails the family minimum.

So: photography fixes the creative *and* the gate at the same time, and nothing else does. Shot list is
in `creative-strategy.md` §4.1. Also worth chasing: `@lawlessconstruction` already let us use one, and
the repeat buyers in `CURVED-JOBS-WINLOSS.md` are the obvious ask.

Second lever: the winner's copy runs six paragraphs in trade voice. Every ad in the current batch is
short. **The proven template is sitting there unused.**

## Avoid repeating

- **Don't research before searching.** Work is spread across ~25 branches and Drive; this repo has lost
  the same work twice. Run the three-step protocol at the top of `STATUS.md` first.
- **Don't trust `git branch --contains` on cnccut-app** — squash merges make shipped work look unmerged.
- **Don't quote account figures from memory.** A previous session reported per-ad numbers as
  account-wide and was wrong by an order of magnitude. Ground truth: ~38 Shopify orders / 30d, ~358 ATC.
- **Don't segment by trade at launch.** July did, from scratch, and it was the worst money the account
  has spent. Identity words multiply a *proven* winner; they don't find one.
- **Don't over-correct when challenged.** After Lee pushed back on the July post-mortem, a session swung
  from "creative was fine" to the opposite and had to correct twice. AD5's traffic converted to ATC at
  0.16% against a sitewide ~1.5% — the traffic genuinely underconverted *and* the event was wrong.
- **Don't relabel creative families to pass the gate.** `family` is explicit in `ads.config.mjs` for
  exactly this reason — it used to be derived from the template, which silently collapsed everything
  into two families. The gate only works on honest labels.
- **Don't paste secret values** into chat, a repo file, or the Drive brain. Check presence by
  length/prefix only.

## Skills to run

- `/claude-api` — before touching anything that calls Claude (`brand-check`'s vision path).
- `/craftons-voice` + `/direct-response-copy` — for the long-form rewrite from the winner.
- `/craftons-design` — for any new rendered asset.
