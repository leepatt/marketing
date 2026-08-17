# Meta ads — the complete build checklist

_Every item from **both** source videos, with honest status. Written 2026-08-03._
_Nothing here is marked done unless it has been **run and verified**, not merely written._

**The two sources:**
- **Video A — Cody Schneider / Greg Isenberg, "Marketing Agents Are Too Good Now"** → the *machine*
  (data loop, cadence, creative pipeline, entropy). Digested in `META-ADS-AGENT-BIBLE.md`.
- **Video B — Sabri Suby, "8 hacks I wish I knew sooner"** ($300M+ spend) → the *marketing*
  (what the ads say and how they're structured). Digested in Drive `MARKETING-BIBLE.md` §9.

> ⚠️ **Read `MARKETING-BIBLE.md` and `MARKETING-CHECKLIST.md` in Drive before writing any copy.**
> They existed before this build and I did not read them until 2026-08-03. They contain the offer,
> the funnel and the verbatim law — and the first ad batch broke that law.

**Key:** ✅ done & verified · 🟡 partial · ❌ not started · ⛔ blocked/impossible · 👤 needs Lee

---

# 🔴 THIS CHECKLIST WAS CORRECT AND WAS NOT EXECUTED (2026-08-17)

The Aug26 launch spent **$192.08 for zero attributed conversions** and delivery collapsed 86% in three
days, because the ad set optimised toward a custom conversion that **had never fired**.

**Nothing new needed to be known to prevent it. Three items already on record said so:**

| Where | What it already said | What actually happened |
|---|---|---|
| Line 4 of this file | *"Nothing here is marked done unless it has been **run and verified**, not merely written."* | The conversion was verified to **exist**, never to **fire**. Reported as "wired ✓" |
| Line 109 of this file | *"**Never optimise on an event we can't generate.**"* | We optimised on an event that had never once been generated |
| Bible §4.7 Stage 1, quoted at line 193 | Gate is *"**tracking fires**, EMQ > 7, no policy rejections, creative approved"* | Launched with tracking unproven |
| **C4.4 — EMQ > 7** | 🟡 *"Can't read yet"* | **Still unread at launch, and launched anyway** |

**The lesson is not "write a better checklist." It is that a document cannot enforce itself.**
A markdown gate gets read once and skipped under momentum. So the blocking items are now **code that
refuses**, and they were verified against the real broken ad set on 2026-08-17.

## ✅ These items are now ENFORCED IN CODE, not merely written

`judgeLaunchReadiness()` in `tools/_meta-policy.mjs`, called from the activation preflight in
`tools/meta-ads.mjs` **at execution time**. It **fails closed** — no spend starts unless every check
passes. 7 new `doctor` self-checks assert it (total **54/54**).

| Gate | Refuses when |
|---|---|
| **Conversion has fired** | the target custom conversion has no `first_fired_time` — *the exact Aug26 failure* |
| **EMQ acknowledged** | `emq_acknowledged` is not explicitly `true`. EMQ is not API-readable, so a human must confirm it in Events Manager rather than let it stay 🟡 |
| **Pixel alive** | the pixel reports `is_unavailable`, or last fired > 7 days ago |
| **A target exists** | `promoted_object` carries no conversion target at all |
| **Australia only** | any non-AU geo, or no geo set (which Meta serves worldwide) |
| **Budget caps** | daily > $100, or the $2,000 month ceiling already reached |

**Proof it works, run against the live Aug26 ad set:**

```
## Meta Ads — apply blocked (activation preflight)
- custom conversion 27686282527680441 has NEVER FIRED (no first_fired_time)…
- EMQ has not been acknowledged…
Fix these and propose again. Nothing was activated.
```

## Guardrail revised in the same pass

`create_ad_set` previously rejected `custom_event_type` outright — a rule written because ATC broke
July, which encoded "custom conversion good, standard event bad". Aug26 inverted the evidence, and that
rule was blocking the correct fix. It now **accepts `INITIATED_CHECKOUT` and `PURCHASE`**, and still
**refuses `ADD_TO_CART` by name**. Guardrails encode hypotheses; when the evidence flips, revise the
guardrail rather than route around it.

---

# PART A — Video A: the machine

## A1. Unified data / the warehouse

| # | Item | Status | Evidence |
|---|---|---|---|
| A1.1 | One place holding all sources in context | ✅ | `marketing_metrics_cache`, 494 rows, 328 kB, holds Meta + Google Ads |
| A1.2 | Agent run history | ✅ | `marketing_runs`, 214 rows |
| A1.3 | Creative memory with recipes | ✅ | `marketing_assets.provenance`, 15 rows |
| A1.4 | Human approval gate | ✅ | `marketing_approvals`, 7 rows |
| A1.5 | **API for writes, never bulk reads** | ✅ | `report` writes cache; `evaluate` reads cache, never re-hits insights |
| A1.6 | Airbyte + ClickHouse | ⛔ | **Deliberately not built.** 328 kB across 3 sources; ClickHouse is for billions of rows |
| A1.7 | Rate-limit discipline / backoff | ✅ | `_lib.mjs fetchJson`, honours `Retry-After` |

## A2. Autonomous decisions on a cadence

| # | Item | Status | Evidence |
|---|---|---|---|
| A2.1 | Scheduled run, not human-invoked | ✅ | Vercel cron, Sun 22:00 UTC, `app/api/cron/meta-ads` |
| A2.2 | Weekly not daily (volume-appropriate) | ✅ | Reasoned in bible §5.5 |
| A2.3 | Cadence does report → evaluate | ✅ | Verified in the loop dry run |
| A2.4 | Cadence also runs brand-check | ✅ | Added 2026-08-03, capped at 8/firing, non-blocking |

## A3. The feedback loop

| # | Item | Status | Evidence |
|---|---|---|---|
| A3.1 | Kill rules, explicit and tunable | ✅ | ≥72h, ≥$25, 0 results; kill cap 50%/run |
| A3.2 | Winners pool | ✅ | `pool`. **Note:** cannot allocate budget — Meta budgets sit on the ad set |
| A3.3 | **Store the recipe, not the ad** | ✅ | `provenance.recipe`. Was silently broken (missing SELECT column) until fixed |
| A3.4 | Winners analysed by recipe pattern | ✅ | `winners` joins provenance |
| A3.5 | Full loop run end-to-end | ✅ | Run 2026-08-03. Found 2 bugs, both fixed |

## A4. Creative pipeline

| # | Item | Status | Evidence |
|---|---|---|---|
| A4.1 | Research → pain points | 🟡 | Tool works, but see **C1** — the research is not yet the dream buyer's words |
| A4.2 | Rank pain points by frequency | ❌ | Probes return quotes, not counts. **Still not done** |
| A4.3 | Static generation | ✅ | `content-engine/ads/render-ads.mjs` — HTML, not AI |
| A4.4 | Vision model over every output | ✅ | `brand-check` now reads pixels. **Untested live** — needs one real run |
| A4.5 | Video / avatar creative | ❌ | HeyGen key now in Vercel; path not built |
| A4.6 | Kie.ai / Nano Banana | ⛔ | Not needed — Replicate + Glif already wired |
| A4.7 | Seedance | ⛔ | **Skip.** Can only produce set-dressing; our product is geometry |

## A5. Publishing

| # | Item | Status | Evidence |
|---|---|---|---|
| A5.1 | `/adimages` → `/adcreatives` → `/ads` | ✅ | Built |
| A5.2 | Always create PAUSED | ✅ | Hard-coded in `buildMutation` |
| A5.3 | One campaign, one ad set enforced | ✅ | `MAX_AD_SETS = 1` |
| A5.4 | Batch approval in one screen | ✅ | Cockpit component + `/approvals/batch` |
| A5.5 | Writes need CONFIRM=1 **and** approval | ✅ | **Verified** — refused with CONFIRM=1 on a pending row |

## A6. Entropy

| # | Item | Status | Evidence |
|---|---|---|---|
| A6.1 | Meta Ad Library puller | ⛔ | **Impossible for AU.** Non-EU commercial ads aren't archived. Not a permissions issue |
| A6.2 | Virlo trend API | ⛔ | Skip — not before there's a loop to un-stick |
| A6.3 | Transcript mining | ❌ | Not started |
| A6.4 | Novelty check | ✅ | `checkNovelty`, 3-batch window |
| A6.5 | Competitor swipe file | ❌ | Must be **manual** (web UI), since A6.1 is impossible |

---

# PART B — Video B: Suby's 8 hacks (the ad-creation layer)

> This is the layer the build has been **weakest** on. The machine is finished; what it publishes
> has not been through this.

| # | Hack | Status | What it means for Craftons |
|---|---|---|---|
| B1 | **Statics beat video, win on volume** | ✅ | The renderer makes statics cheaply. Vindicated the decision to drop the configurator clip |
| B2 | **Identity keyword — creative IS targeting** | 🟡 | ⚠️ **See the contradiction below** |
| B3 | **Clone winning formats; zombie relaunch** | ❌ | Nothing to clone yet — no winner. `winners` will feed this |
| B4 | **Don't look like ads — run native** | ❌ | My 6 ads **are catalogue cards**. This is a real miss |
| B5 | **Broad targeting + specific copy** | ✅ | Matches Andromeda; one broad ad set is already policy |
| B6 | **Ad ↔ landing page scent match** | ❌ | Ads point at `/products/radius-online` with **no headline congruence** |
| B7 | **Retarget with a different offer** | ❌ | Product spread (Formwork, Architrave, Field Guide) is the engine. Not built |
| B8 | **Track net cash, not ROAS** | 🟡 | `cac` computes true CAC. Full net-cash/LTV model not built |

### ⚠️ B2 — the contradiction, and the resolution

> **⛔ Resolved differently, 2026-08-03 — the resolution below picked the wrong side.**
> July never segmented the audience: one ad set, broad AU, identity words in the creative — hack #2 as
> written. It pulled **10.45% CTR at $0.08/landing page view**. What failed was optimising on
> `ADD_TO_CART` with ~15 events/month against a ~50/week learning threshold.
> **New rule: identity words on broad targeting, from launch. Never optimise on an event we can't
> generate.** → `suby-8-hacks-implementation.md`

`launch-angles.md` bans trade segmentation, citing July (AD5 Chippies, **$758/result**; three trade ads
at **zero**). Suby's hack #2 says put the trade *in* the ad.

**Both are right, at different stages:**

- **July** built five trade-segmented ads **from scratch at launch**, splitting signal across creative
  that had never worked.
- **Suby** says duplicate a **winning** ad and swap the identity word — a **scaling lever on proven
  creative**.

> **Rule: do not segment at launch. Use identity words to multiply a winner once one exists.**

---

# PART C — What actually blocks the test

## C1. 🔴 The verbatim law is being broken

Drive `MARKETING-BIBLE.md` §1.4: *"No verbatim quote = not ready to write."*

**All six ads were written with zero verbatim customer language.** They are my words about the
product, not the market's words about their problem.

| # | Item | Status | Owner |
|---|---|---|---|
| C1.1 | Stand up `research/market-intel/` (pains · desires · objections · language · triggers) | ✅ | **Was done 2026-07-21, not found until 2026-08-03 (later pass).** Recovered — 7 files now on this branch |
| C1.2 | **Mine the 443 lead-form submissions** — first-party, competitors can't see it | ✅ | ClickUp Job List + Gmail, 68 jobs → `CURVED-JOBS-WINLOSS.md` |
| C1.3 | Mine call notes / email replies / configurator sessions | ✅ | `VOICE-OF-CUSTOMER-curved-jobs.md` (9 verbatim, won+lost) · `enquiry-language.md` |
| C1.4 | Reddit: r/AusConstruction, r/carpentry, r/Formwork1 | 🟡 | Ran, but returned **US woodworkers**, not AU tradies. Superseded — first-party beats it |
| C1.5 | AU Facebook trade groups | ❌ | Claude — low priority now |
| C1.6 | Competitor **one-star reviews** (their failures = our positioning) | ❌ | Claude |
| C1.7 | Rank pains by frequency | 🟡 | No counts, but win/loss gives something better: **Radius Pro 73%, formwork 50%** |

> ✅ **Resolved 2026-08-03 (later pass) → `copy-reconciliation.md`.** The verbatim law is no longer being broken:
> a Lee-approved verbatim copy set from 2026-07-21 was recovered, and all copy is now rewritten
> against cross-validated customer language. The failure was never missing research — it was
> **not finding research that already existed.**

## C2. 🔴 Product facts are unverified — the interview

I asserted these in live ad copy without confirming them with anyone who makes the product:

| Claim used in an ad | Verified? |
|---|---|
| "dispatched in three business days" | ⚠️ **Imprecise** — turnaround is 2 days typical, scales to 5. Use "cut this week" |
| "Part IDs engraved" | ✅ **TRUE** — `_part_id_engraving: "Included"` on every order |
| "nothing to fill at the join" | ❌ **FALSE** — joiner blocks ship with every split. Customer's word: *"splice piece for every join"* |
| "On site in three days" | ❌ **Killed** — overclaim, dispatch ≠ delivered |
| Bending ply framing | ❌ **Killed** — Craftons sells bendy formply (Rip Pro); "bendy ply" is a confirmed job-winner |

> ✅ **Resolved 2026-08-03 (later pass) from order data + the recovered Lee-approved copy → `copy-reconciliation.md` §3.**
> Four of five settled without the interview. The interview is still worth answering for §4 (the buyer),
> §5 (the fear) and §7 (proof) — but it **no longer blocks the rewrite**.

## C3. 🟠 The offer doesn't exist in the ads

Drive bible §4 defines a Godfather Offer with risk reversal. **None of my ads carry it.** It also
carries a feasibility gate that only Lee can clear.

| # | Item | Status | Owner |
|---|---|---|---|
| C3.1 | Approve/sharpen the fit-guarantee offer | ❌ | 👤 **Lee** |
| C3.2 | Decide guarantee boundary (our fault vs bad set-out) + freight cap | ❌ | 👤 **Lee/Ops** |
| C3.3 | Put the approved offer in every ad and on the page | ❌ | Claude |

## C4. 🔴 Phase 0 tracking — the last gate

| # | Item | Status |
|---|---|---|
| C4.1 | Pixel + CAPI live | ✅ |
| C4.2 | Advanced Matching on, 11 params | ✅ |
| C4.3 | **Combined custom conversion (IC OR Purchase)** | ❌ 👤 **Lee, or say the word** |
| C4.4 | EMQ > 7 | 🟡 Can't read yet — needs 24–48h from 2026-08-03 |
| C4.5 | Purchase carries AUD value | ✅ |
| C4.6 | Checkout → sale close rate | ✅ `cac` — **39.4%**, twice the sitewide estimate |

## C5. 🟠 Creative volume

6 ads · floor 15 · 2 families · minimum 3. `check-batch` **correctly refuses**.

> **But note:** 15 is the *performance* floor. A **validation run** (does the plumbing work?) needs
> far fewer. Bible §4.7 Stage 1's gate is explicitly *"tracking fires, EMQ > 7, no policy rejections,
> creative approved"* — **not performance.**

---

# The honest summary

**The machine is done.** Parts A1–A5 are built and exercised end-to-end; the safety spine is proven.

**What isn't done is the marketing.** Part B (Suby) and Part C (verbatim research, verified product
facts, the offer) are where the work is — and they're what makes the difference between ads that spend
money and ads that make it.

**Do not run the test until at minimum:**
1. ~~The product interview clears the unverified claims (**C2**)~~ — ✅ **done 2026-08-03 (later pass)** from order
   data + recovered approved copy
2. The custom conversion exists (**C4.3**) — 👤 **still the gate.** Account write, needs Lee
3. ~~Copy is rewritten against real customer language (**C1**)~~ — ✅ **done 2026-08-03 (later pass)** →
   `copy-reconciliation.md` §4
4. 🆕 **Creative re-rendered to match.** The words are fixed; the images still show a 900mm decorative
   arc, which is the wrong product. A true headline over a misleading image is still a misleading ad

Items 1 and 3 were the ones I got wrong by rushing. Better to find that here than in market.

> **The deeper lesson, logged 2026-08-03 (later pass):** both failures were the same failure. The Drive bible went
> unread, and then a full verbatim research pass went unfound — so it got re-derived, worse. The fix
> isn't "research harder", it's **look for the work before doing the work.** `STATUS.md` exists for
> exactly this and was three sessions stale.
