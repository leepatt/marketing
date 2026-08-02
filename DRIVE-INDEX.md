# Drive index — what lives in the brain, and where

_Last verified against Drive: 2026-08-02._

**Read this before starting any marketing work.** Drive is the source of truth for strategy, research
and creative. This repo holds working docs and the rules Claude sessions must enforce — it does
**not** duplicate the brain.

This file exists because in July 2026 a Meta campaign was properly briefed in Drive, but nothing in
this repo pointed at the brief. A repo-side session had no idea it existed and found the campaign
only by querying the Meta API. See `campaigns/POST-MORTEM-2026-08-02.md`.

> **If you are about to say "there's no record of X" — check Drive first.** That claim has already
> been made once and been wrong.

---

## Where things live

| Home | What it holds | Rule |
|---|---|---|
| **Drive** `Peninsula Studio/01 Craftons/Marketing/` | Strategy, research, briefs, creative, media | **Source of truth.** Don't copy into the repo — link to it |
| **This repo** | Working docs, campaign configs, and the rules sessions enforce at startup | Governance + build artefacts |
| **cnccut.app repo** | Dashboard/app code | Reads marketing data; doesn't import this repo |
| **Later.com** | Scheduling/posting | Approved drafts only |

**The split, stated plainly:**

- **Governing docs** (rules, gates, checklists Claude must obey) → **repo**, because sessions load the
  repo at startup and can't be relied on to fetch Drive first. Mirrored to Drive for humans to read.
- **Working docs** (briefs, research, strategy, creative) → **Drive only**. The repo links to them.

---

## Drive folder map

Root: [`01 Craftons/Marketing/`](https://drive.google.com/drive/folders/1YszHwi5dAIXdkN24ozLrQL3L-agm3s7w) · folder id `1YszHwi5dAIXdkN24ozLrQL3L-agm3s7w`

| Folder | id | Contents |
|---|---|---|
| `00 Brain/` | `1dS26fC7p6w7-DmiBnaNMwS1CEpAeCje7` | Design system, Fusion import |
| `01 Inspiration/` | `1v9o6s2aI0rgH2lzcoAmO4DCzRk559XfE` | Teardowns, `_inspo-dump/` |
| `02 Strategy/` | `1wxK39UHbXkzc9crFWhfnSkHFXTCBcvx4` | **The ads + strategy docs — enumerated below** |
| `03 Content/` | `1VAa6Qj_0rDKktEPT1oEv6iDrGEicyT9W` | Client assets, drafts, produced |
| `04 Newsletter/` | `1_oBATFZ-Miudj08TzJwRvJLI79jyQXe7` | Fortnightly newsletter |
| `Campaigns/` | `1R6NAP_TWRdm4Baeqpnh7eDZ5Y5jVW6AK` | Campaign material |
| `Video/` | `1szaFsOyJ574h0JFrIyo_K_lxC3Bj-M5V` | Scripts, storyboards, How-To series |
| `Channels/` | `1TbPcw841ihU0ymv0lGPCrpmgEBRkYP4L` | Per-platform material |

_Only `02 Strategy/` has been enumerated file-by-file. The other folders are listed but not indexed —
search them before assuming they're empty._

---

## `02 Strategy/` — the docs that govern ads

### ⭐ Read these before any paid-ads work

| Doc | Why it matters |
|---|---|
| [**MARKETING-BIBLE.md**](https://drive.google.com/file/d/1rBBxrm8nY2J4sZ9IFP7hlqKPJSOYdN8J/view) | 27KB — **the doctrine.** §3 attention, §6 scoreboard, §9 Meta ads playbook. The governing strategy document |
| [**MARKETING-CHECKLIST.md**](https://drive.google.com/file/d/1HyXSzlO1V-RYifKAZghtfdhRUF9SpNZj/view) | The phased execution plan (Phase 0–5) that runs the bible. **Not** a safety checklist — it's the roadmap |
| [**META-ADS-BRIEF.md**](https://drive.google.com/file/d/12GnGduQzbvLKwvD6Cf0DDGIDPhgJyhmF/view) | The brief for the Jul 22 campaign. Static ads, feed placements, approved copy. Still largely untested — the ads that ran weren't the ones it specified |
| [**DREAM-BUYER-AVATAR.md**](https://drive.google.com/file/d/1uh2oFloCVLJFkPSWmNpwuD6EtRHDMuNC/view) | Who we're targeting |

### Customer evidence (the source of ad copy)

| Doc | |
|---|---|
| [VOICE-OF-CUSTOMER-curved-jobs.md](https://drive.google.com/file/d/1aA714qgFyEgYzsNBXbKczM89pN0HGwAM/view) | Verbatim quotes from real paying customers |
| [customer-voice-ad-copy.md](https://drive.google.com/file/d/1qbn6sXKcvDW-PEls5Ec3KunPQJWFgCwp/view) | Lee-approved ad copy built from those quotes |
| [CURVED-JOBS-WINLOSS.md](https://drive.google.com/file/d/1QHTlveAFXzkh-pSMmRtlskk78oh3b2Id/view) | Win/loss on ~68 real curved jobs |
| [CURVED-JOBS-DOLLARS-AND-BOTTLENECK.md](https://drive.google.com/file/d/1Z25mNpeNMsfJEcMPlSy0Iac6BM_s264r/view) | Job values + the quoting bottleneck |

### The ads post-mortem (mirrored from this repo)

| Doc | |
|---|---|
| [Ads-PostMortem-2026-08-02-v2-CURRENT.md](https://drive.google.com/file/d/1A3DvG21tWHztJUvjHIaE7p32AIg_O8oW/view) | ⇄ `campaigns/POST-MORTEM-2026-08-02.md` |
| [Ads-PreFlight-Checklist-v2-CURRENT.md](https://drive.google.com/file/d/15mPg2S6h-QUaeasRCkTsiGTO_VrXukqS/view) | ⇄ `campaigns/ADS-PREFLIGHT-CHECKLIST.md` |

⚠️ Two superseded copies without the `-v2-CURRENT` suffix are still in that folder pending manual
deletion — the Drive connector can create files but not update or delete them.

### Voice / content (⚠️ also exist in this repo — drift risk)

| Doc | Repo counterpart |
|---|---|
| [CONTENT-PILLARS.md](https://drive.google.com/file/d/1-XA52KhHGZEtcyoCKygqgm4qr4rSvCPt/view) | `CONTENT-PILLARS.md` |
| [SOCIAL-VOICE.md](https://drive.google.com/file/d/10pleeIBM-yrPXdG4dqXZUhhGh1cLaxDT/view) | `SOCIAL-VOICE.md` |

**These are duplicated and will drift.** Reconcile them — pick one home each — before treating either
as authoritative.

### Earlier planning (Jake, 13 Jun — predates the Jul 21 body of work)

`Craftons-Marketing-Engine-Plan.md` · `Craftons-Marketing-Engine-Notes.md` · `Craftons-Marketing-Plan.md` ·
`Craftons-Meta-Ads-Plan.md` · `Craftons-Meta-Ads-Audit.md` · `Craftons-Social-Media-Strategy-Plan.md` ·
`Craftons-Content-Pillars.md` · `positioning-angle.md` · `Onsite-Tool-Smart-Feature-Concepts.md` ·
`Plan-Scanner-MVP-Build-Plan.md` · `research/` subfolder

_Superseded in places by the July docs. Check dates before relying on them._

---

## ⚠️ Open reconciliation — the rules already existed

`MARKETING-CHECKLIST.md` (21 Jul, the day before the campaign launched) already said, in Phase 4:

> "Launch the AdWords campaign … **Verify tracking is live before spend.**"
> "Demote vanity conversions … optimise toward **leads + jobs + net cash**, not downloads or ROAS."

And `META-ADS-BRIEF.md` §6 already said:

> "**Judge on net cash, not ROAS %.**"

**Both instructions predate the campaign and both were violated.** So the July failure was not caused
by missing rules. It was caused by rules that existed in Drive and were never surfaced to the session
doing the work.

That is why the paid-ads gate now lives in `CLAUDE.md` — loaded at startup, unavoidable — rather than
in another document that has to be sought out.

**Still to do:** reconcile the post-mortem's eight rules against `MARKETING-BIBLE.md` §6 and §9, so
there is one doctrine rather than two overlapping ones.
