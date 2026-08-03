# Copy reconciliation — resolving three intel sources into one corrected ad set

_Written 2026-08-03 (later pass). Closes the "rewrite all ad copy from verbatim language" blocker in
`BUILD-CHECKLIST.md` Part C1/C2, as far as it can be closed without Lee._

> **The short version:** the ad copy problem was never a shortage of research. A full verbatim pass
> **already existed** — done 2026-07-21, Lee-approved, sitting in Drive and on a branch nobody
> reopened. The 2026-08-03 batch was written without it, and re-derived a worse version of it.

---

## 1. What was actually missing

`META-ADS-BRIEF.md` (Drive) was listed as "unread" in the handoff. Reading it turned up a complete
research corpus that this branch did not have:

| Artefact | Where it was | What it contains |
|---|---|---|
| `META-ADS-BRIEF.md` | Drive `01 Craftons/Marketing/` | Golden rule · dream buyer · **Lee-approved copy (§5)** · static-ad rules |
| `customer-voice-ad-copy.md` | branch `marketing-video-transcript-cy49qx` | **"Lee-approved 2026-07-21"** — headlines + descriptions, all three products |
| `VOICE-OF-CUSTOMER-curved-jobs.md` | same branch | 9 verbatim enquiries, won **and** lost, with outcomes |
| `CURVED-JOBS-WINLOSS.md` | same branch | 68 jobs, win rate by product — **Radius Pro 73%** |
| `CURVED-JOBS-DOLLARS-AND-BOTTLENECK.md` | same branch | $ sizing + the quoting-bottleneck finding |
| `DREAM-BUYER-AVATAR.md` · `QUOTE-BANK.md` | same branch | Buyer profile + quote bank |

All six are now recovered onto this branch. **`BUILD-CHECKLIST.md` C1.1 ("stand up
`research/market-intel/`") was marked ❌ and re-done from scratch on 2026-08-03. It had been done on
2026-07-21.** That is the second time this repo has lost work by not finding it — the same failure
mode as the unread Drive bible, one layer up.

---

## 2. The two-funnel model — this explains every apparent contradiction

The intel docs look like they contradict each other. They don't. **They describe two different
businesses that share a phone number.**

| | **CNC Cut** (bespoke) | **Craftons** (self-serve) |
|---|---|---|
| How work arrives | Email a drawing, ask for a price | Configurator → instant price → checkout |
| Data source | Gmail `cnc@cnccut.melbourne`, ClickUp Job List, Quotient | Shopify orders, `_source` attributes |
| Buyer seen | PMs, site engineers, contracts admins, directors | Builders ordering plates by qty, projects named by address |
| Lead time quoted | 3–4 weeks (a decline reason in the inbox) | `_total_turnaround` **2 days**, 3 on some, 5 on a 27-sheet job |
| Closed by | A conversation. "Spoke on the phone" is in nearly every thread | Nobody. It's a checkout |

**This is the single most important thing to hold onto**, and it resolves the contradictions:

- **The Drive golden rule** — *"ads sell the self-serve online builders. NEVER 'send us your CAD' —
  that's the bespoke CNC Cut service, our intel source, not what we advertise."*
- **`enquiry-language.md` (2026-08-03)** concluded the winning angle is *"Send us the plan. We'll snap
  to the architect's lines and cut the plates."* — **that is the forbidden framing.** It was mined
  from the CNC Cut inbox, which is exactly the funnel the brief says not to advertise.
- **The audience "correction"** in the same doc (buyer is a PM, not a chippie) describes the **CNC Cut**
  buyer. It is real, and it is not the Radius Pro buyer. `brand/audience.md` was not as wrong as
  flagged — it was being marked against the wrong funnel.
- **The lead-time tension** it flagged resolves cleanly: 2 days is Radius Pro, 3–4 weeks is bespoke
  CNC. Never blur them in an ad — that part of the warning was right.

**What does transfer across both funnels is the language.** "Top and bottom plates" appears in the
Shopify order attributes, the Gmail inbox, the ClickUp enquiries and the Lee-approved copy. Four
independent sources, one phrase. That is the anchor.

### The one genuine open question this creates

**Plan Scan.** Order #1271 carries `_source: "plan-scanner"` — send-us-your-plan is now a *live,
productised, self-serve* mechanism. The golden rule was written 2026-07-21, before that. So "send us
the plan" may no longer violate it — it may now *be* a self-serve builder.

**This is a Lee call, and it is worth asking**, because the inbox says file-friction is the biggest
unwritten pain in the market and Plan Scan is the answer to it. Until Lee rules: **Plan Scan does not
lead the launch batch.** (See §5.)

---

## 3. The five unverified claims — now settled

`radius-pro-interview.md` §1 listed five claims sitting in rendered ads. **Four are now answered from
data, without needing the interview.**

| # | Claim as written | Verdict | Evidence |
|---|---|---|---|
| 1 | "Dispatched in three business days" | ⚠️ **Imprecise — don't say it** | `_total_turnaround` is **2 days** typical, 3 some, 5 on a 27-sheet job. It scales with size. Use the Lee-approved *"cut this week"* instead — true across the range |
| 2 | "On site in three days" | ❌ **Kill.** Overclaim | Its own sub-line said *dispatched*. Dispatch ≠ delivered. No delivery data supports it |
| 3 | "Part IDs engraved" | ✅ **TRUE — use it** | `_part_id_engraving: "Included"` on every order in the sample |
| 4 | "Nothing to fill at the join" | ❌ **FALSE — and the truth is better** | `_joiner_blocks: "Included"`, qty 4–95. And the customer's own word for it is in the corpus: **"splice piece for every join"** |
| 5 | "Bendy ply is the slow way round" | ❌ **Kill. Attacks our own product** | Rip Pro *sells* bendy formply. "Bendy ply" is a confirmed job-winning search term. Lee-approved copy instead says *"no hand-templating, no bog-and-sand"* |

**Claim 4 is the best outcome here.** The false claim gets replaced by a true one that is *stronger*,
and the market already has a word for it — **"splice piece for every join"** (`CURVED-JOBS-DOLLARS`
verbatim adds). We were papering over a real feature with a fake one.

### On "bog-and-sand"

`enquiry-language.md` flagged that it never appears in the inbox and questioned Angle 2. Half right:

- It is **not** enquiry language. Nobody emails asking to stop bog-and-sanding. Correct.
- It **is** Lee-approved ad copy (*"No hand-templating, no bog-and-sand"*) and documented brand slang
  in `SOCIAL-VOICE.md`.

So it is not banned — it's *positioning* language, not *transactional* language. Keep it, but it can't
carry an ad on its own, and it shouldn't have been the #2 launch angle's headline.

---

## 4. The corrected copy

Anchored on the **Lee-approved 2026-07-21 set**, corrected by the Shopify order data, and extended for
Meta (which allows longer copy than the Google set was written for).

**Every line traces to a source.** No line asserts anything the data doesn't carry.

### Verbatim anchors (the phrases doing the work)

| Phrase | Sources agreeing |
|---|---|
| **top and bottom plates** | Shopify (90mm dominant) · Gmail (Matt P., Sean C.) · ClickUp (Perfetto, Oxbuilt) · approved copy |
| **cut to size / cut to your radius** | Approved copy · every enquiry |
| **the radius is to the outside of the wall** | `CURVED-JOBS-DOLLARS` verbatim · approved headline "Radius to the Outside? Done" |
| **splice piece for every join** | `CURVED-JOBS-DOLLARS` verbatim · matches `_joiner_blocks: Included` |
| **curves cut perfectly** | Khosh Constructions · approved headline |
| **16 plates… need them asap** | AC Building · matches order qty 16/20/25/60 |
| **whatever ply you normally use** | AC Building · "happy to use the 17mm form ply" Oxbuilt · matches `form-17` dominant |

### The batch — 15 creatives, 3 angles × 4 families

Format: **headline** (~27–40 chars) · **primary text** (front-load ~125 chars).
Family tags match `render-ads.mjs`. All point at `/products/radius-online`.

#### Angle 1 — "Design it. We cut it." (demo) — ranked 1, account evidence

| # | Family | Headline | Primary text |
|---|---|---|---|
| 1 | `configurator` | Price Your Curved Plates Online | Draw the radius. Get the price on the spot. Top and bottom plates cut to size, delivered this week. |
| 2 | `configurator` | Top & Bottom Plates, Any Radius | Type in your radius, pick your ply, see the price. No waiting on a quote to find out if it's worth it. |
| 3 | `configurator` | Radius to the Outside? Done | Set it out the way you'd set it out on site — radius to the outside of the wall. Priced online. |
| 4 | `configurator` | Curved Ply, Formply or MDF | 17mm formply, structural ply or MDF, cut to your radius. Price it online, no sales call. |
| 5 | `cad_render` | Curves Cut Perfectly | Machine-cut to your radius, not templated by hand. Design it online and see the price before you commit. |

#### Angle 2 — the problem — ranked 2, customer evidence

| # | Family | Headline | Primary text |
|---|---|---|---|
| 6 | `static_craft` | 16 Plates. Cut. This Week. | Whatever ply you normally use, cut to your radius. Order the run, not one part at a time. |
| 7 | `static_craft` | No Hand-Templating | Curved top and bottom plates, machine-cut to size. No hand-templating, no bog-and-sand. |
| 8 | `static_craft` | Curved Wall Plates, Cut to Size | The curve is the part of the job you're least sure about. It doesn't have to be the part you make twice. |
| 9 | `avatar` | Stop Making the Curve Twice | Top and bottom plates for curved walls, cut to your radius and labelled. Priced online. |
| 10 | `avatar` | Yes, We Cut That Curve | Multi-metre radii, 90mm plates, production quantities. Design it online and see what it costs. |

#### Angle 3 — the outcome — ranked 3, reassurance/retargeting

| # | Family | Headline | Primary text |
|---|---|---|---|
| 11 | `cad_render` | A Splice Piece for Every Join | Big curves ship split — with joiner blocks included, so it goes back together on your line. |
| 12 | `cad_render` | Every Part ID Engraved | Part IDs cut into the face, not stickered on. You'll know what goes where when the pack lands. |
| 13 | `static_craft` | Curved Plates Cut This Week | Cut to your radius, labelled, ready to fix. Order it online and check the lead time before you commit. |
| 14 | `avatar` | Labelled Before It Ships | Curved plates arrive cut to size with Part IDs engraved and joiner blocks for every split. |
| 15 | `configurator` | Any Radius, Any Quantity | From one plate to sixty. Multi-metre radii, cut to size, priced online in front of you. |

### What changed, and why

| Was | Now | Why |
|---|---|---|
| "On site in three days" | "Cut this week" | Dispatch ≠ delivery. "This week" is Lee-approved and true across the 2–5 day range |
| "Nothing to fill at the join" | "A splice piece for every join" | The old line was false. The new one is true, verbatim, and a better feature |
| "Bendy ply is the slow way round" | "No hand-templating, no bog-and-sand" | Stops attacking Rip Pro; uses Lee-approved phrasing |
| Decorative 900mm arc framing | 90mm plates, multi-metre radii, qty 16–60 | Order data. The creative was aimed at the wrong product |
| "Dispatched in three business days" | Dropped as a headline claim | Imprecise. Turnaround scales with size |

⚠️ **The creative still needs re-rendering.** This fixes the *words*. The rendered images still show a
900mm decorative quarter-arc, which `radius-pro-orders.md` established is the wrong product. Copy and
image have to move together — a true headline over a misleading image is still a misleading ad.

---

## 5. What still needs Lee

Narrowed from thirty-one interview questions to **four decisions**. Everything else is either answered
above or not blocking.

| # | Decision | Why it's blocking | Default if no answer |
|---|---|---|---|
| 1 | **Is Plan Scan advertisable yet?** Live and producing orders, but the golden rule predates it | Decides whether the strongest evidenced pain (file friction) can be used at all | Hold it back. Launch on the configurator |
| 2 | **The fit guarantee** — approve/sharpen, and set the boundary between our error and a bad set-out, plus freight cap | Drive bible §4: every ad is supposed to carry the same offer + risk reversal. None currently do | Launch without it. Weaker, not blocked |
| 3 | **Combined custom conversion (IC OR Purchase)** — account write | Last Phase 0 gate | Blocked. Needs the say-so |
| 4 | **Before/after photography** | Unblocks the strongest execution of Angle 2 | `before_after` family stays at 0 |

**No longer blocking:** the five §1 interview claims (settled in §3 above), the audience question
(two-funnel model), turnaround (order data), joins (order data), bending ply (approved copy).

`radius-pro-interview.md` is still worth answering — §4 (the buyer), §5 (the fear) and §7 (proof) are
where the next real gains are. But **it no longer blocks the rewrite**, and shouldn't hold the batch.

---

## 6. Ledger

- ✅ Drive bible, checklist and brief read — the standing rule that was skipped
- ✅ Lost intel corpus recovered onto this branch (6 files)
- ✅ Two-funnel model resolves the audience/angle/lead-time contradictions
- ✅ Four of five unverified claims settled from data
- ✅ 15 corrected creatives written from cross-validated verbatim
- ⬜ Re-render creative to match (blocked on the `cnccut-app` repo)
- ⬜ Re-run `ingest` → `check-batch` → `brand-check` on the corrected batch
- ⬜ Lee's four decisions above
