# Launch angles — Radius Pro on Meta

_The creative brief every ad in the launch batch reads from. Written 2026-08-03._
_Closes bible Phase 2.2 ("rank pain points, top 3 become the launch angles")._

> ### ⚠️ Superseded in part, 2026-08-03 (later pass) → `copy-reconciliation.md`
>
> **The three angles stand.** The ranking (demo → problem → outcome) is unchanged and still correct.
> What changed is the copy underneath them:
>
> - **Angle 3's own title is now wrong.** *"Dispatched in three days"* is imprecise — order data says
>   turnaround is **2 days typical**, scaling to 5 on big jobs. The angle is sound; the number isn't.
>   Use *"cut this week"* (Lee-approved). Its proof line now leads on **joiner blocks** and
>   **engraved Part IDs**, both confirmed in order data.
> - **⛔ Angle 2 is RETIRED, not weakened.** Lee, 2026-08-03: *"it talks about curve bending and
>   bogging and all of this stuff. That's just not related to the job at all."* Bog-and-sand, kerfing
>   and curve-bending are banned from Radius Pro copy outright. The real pain is **the maths, marking
>   the radius out on a sheet, jigsaw mistakes and waste** — see `radius-pro-product-truth.md`.
>   The replacement angle is *"nobody's marking out curves"* plus the **nesting/waste** argument.
> - **The verbatim below is US-Reddit woodworkers.** It was honestly caveated at the time, but it has
>   since been superseded by first-party AU intel: `VOICE-OF-CUSTOMER-curved-jobs.md`,
>   `CURVED-JOBS-WINLOSS.md`, `CURVED-JOBS-DOLLARS-AND-BOTTLENECK.md`, and Shopify order attributes.
>   **Write from those, not from this table.**
> - **The anti-angle (never segment by trade at launch) is confirmed** and now reconciled with Suby's
>   identity hack — see `BUILD-CHECKLIST.md` B2.
>
> The rewritten batch is `copy-reconciliation.md` §4.

> **Companion docs:** `META-ADS-AGENT-BIBLE.md` (§4.1 product, §4.3 creative families, §4.5 account
> post-mortem) · `../../brand/audience.md` (the pain points, from real customers) ·
> `../../brand/keyword-plan.md` (proven converting language) · `../../QUALITY-DOCTRINE.md`.

---

## How these were ranked (and why not the way the video says)

Cody's pipeline ranks pain points by **how often they're referenced on Reddit**.

> ### ⚠️ Corrected 2026-08-03 — an earlier version of this section was wrong
>
> This doc originally said the Reddit seam "isn't there" and that the research pass was a dead end
> for this niche. **That conclusion was wrong, and it was drawn too fast** — from two failed calls,
> without checking whether the failure was the source or the query.
>
> It was the query. The original `research` prompt asked one compound question ("rank the pains AND
> quote them AND list outcomes AND extract jargon") with no domain filter. Retrieval had nothing
> narrow to match on. **Re-tested with `search_domain_filter: ["reddit.com"]` and one focused
> question per call, the same API returns real verbatim comments with subreddit attribution.**
>
> Separately worth knowing: **reddit.com blocks Anthropic's crawler outright**, so direct fetching
> can't reach it. Perplexity has its own access — which is the actual reason the research path is
> routed through Perplexity rather than a plain fetch.
>
> `meta-ads.mjs research` has been rewritten to four narrow probes. A probe that finds nothing now
> reports that instead of sinking the run.

**Verbatim, from the working pass** — the language tradespeople actually use:

| Quote | Source |
|---|---|
| *"Just buy bendy ply, all the grain runs the same direction."* | r/BeginnerWoodWorking |
| *"I've never liked kerf bending bc of the flats and the holes it leaves."* | r/woodworking |
| *"Kerf cuts on inside of bend and veneer over to hide cuts"* | r/BeginnerWoodWorking |
| *"Use 3/8" bender board/ply. Then 1 layer of 1/8" MDF to give a smooth surface and help with any irregularities."* | r/cabinetry |
| *"There's plywoods on the market that bend without being kerfed and are affectionately known as **wiggle wood**."* | r/woodworking |
| *"You could try kerf bending the ply, but due to the nature of the cross grain lamination, plywood is inherently stiff."* | r/woodworking |

**Two findings that matter for copy:**

1. **"bendy ply" appears organically** — the same term `keyword-plan.md` lists as a confirmed
   converter. Independent confirmation from an unrelated source.
2. **The kerfing complaint is real and specific:** *"the flats and the holes it leaves"*. That is
   Angle 2's pain in the customer's own words, and better than anything we'd have written.

Also surfaced as live trade vocabulary: **wiggle wood · wiggleboard · flexi-ply · luan**. Note these
are largely US terms — treat as evidence the *concept* is discussed, not as AU copy. Not found in
natural use: "bender board" as two words, "doorskin" for flexible ply.

**What still hasn't been done:** a genuine *frequency* ranking. The probes return quotes, not counts,
and a rigorous ranking needs more passes than one session justifies. So the ordering below remains
evidenced from **three sources we trust more than comment volume**:

1. **`brand/audience.md`** — pain points documented from actual Craftons customers
2. **The live Meta account** (bible §4.5) — 30 days of real spend telling us which framing converts
3. **`brand/keyword-plan.md`** — search terms Lee has confirmed won jobs

**The one thing the research pass did earn its keep for — jargon.** Run 1 surfaced usable trade
vocabulary, and this is worth keeping because it's the register the copy has to hit:

> kerf bend · kerfing · relief cuts · tear-out · splintering · good face · flush-trim · template ·
> registration cut · repeat accuracy · radius formwork

Cross-checked against `keyword-plan.md`'s confirmed converters: **"bendy ply"**, **"curved bench seat"**.

---

## ~~🔴 The anti-angle — do not rebuild the July campaign~~

> ### ⛔ THIS WHOLE SECTION IS WRONG — retracted 2026-08-03 → `suby-8-hacks-implementation.md`
>
> Lee challenged it and the account data proves him right.
>
> - **July never segmented the audience.** All five trade ads sat in **one ad set** —
>   `TOF | Broad AU | AddToCart`, broad Australia, no interest targeting. That *is* Suby's hack #2:
>   broad targeting, identity word in the creative. I mistook creative variation for an audience split.
> - **The creative was the best hook the account has ever run** — AD5 Chippies at **10.45% CTR** and
>   **$0.08 per landing page view**, plus 132 reactions and 12 saves.
> - **What failed was the optimisation event.** The ad set optimised for `ADD_TO_CART`; the account
>   generates ~15 ATC/month against the ~50/week Meta needs to exit learning. Starved of signal,
>   delivery collapses to cheap clicks — exactly the observed pattern.
> - **"$758/result" divided real spend by a broken denominator.** It was evidence about event volume,
>   not creative.
>
> **Identity variants are reinstated** (`radius-pro-ad-copy.md` Angle 4). The rule that replaces this
> section: *identity words on broad targeting, always — and never optimise on an event we can't
> generate enough of.*

**Never segment creative by trade.** July ran separate ads for Chippies, Carpenters, Builders,
Concreters and Landscapers. Results (bible §4.5):

| Ad | Spend | Results | Cost/result |
|---|---|---|---|
| Retargeting — **Configurator** Hero Ad D | $12.10 | 2 | **$6.05** |
| AD5 **Chippies** — curved wall frame | $758.74 | 1 | **$758.74** |
| AD1/AD2/AD6 (Concreters, Landscapers, Carpenters) | $370.48 | **0** | — |

A 125× spread, and every trade-identity ad lost. Two reasons it fails, and they compound:

1. **Andromeda makes it pointless.** The creative *is* the targeting (§1.2). Naming the trade in the
   ad does not help Meta find that trade — describing their *problem* does. Hand-segmenting just
   fragments the signal across ads that are otherwise identical.
2. **It flatters the advertiser, not the buyer.** "Chippies — curved wall frame" tells a carpenter
   nothing they don't know about themselves. It spends the hook on identity instead of on a problem.

**Encoded consequence:** an angle whose distinguishing feature is the trade named in it is not an
angle. All three below are problem- or outcome-led, and any of them reaches any trade.

---

# The three launch angles

Deliberately three *registers*, not three topics — demo, problem, outcome. That spread is what gives
Andromeda genuinely different creative to read (§4.3), and it maps cleanly onto the creative families.

---

## Angle 1 — **"Design it. We cut it."** (the demo)

**Rank: 1. The strongest evidence in the account, twice over.**

| | |
|---|---|
| **Register** | Product demonstration. Show the thing working |
| **Core line** | Draw your curve online. It arrives cut to your set-out |
| **Pain addressed** | Hard to quote · slow set-out · no way to price a curve without a supplier conversation |
| **Proof it's true** | Live configurator, real price, 3 business days |
| **Families** | `configurator` (lead), `cad_render` |
| **CTA** | Build your curve → `/products/radius-online` |

**Why it ranks first — two independent lines of evidence agree:**

- **On site:** the configurator is the top attributable conversion path — ~54 orders / ~$26,800
  (bible §4.4). It converts people who reach it.
- **In the ad account:** "Configurator Hero Ad D" is the single most efficient ad Craftons has ever
  run on Meta — **$6.05/result**, against a break-even CAC of ~$322. That is 53× inside break-even.

⚠️ **Honest caveat, carried from the bible:** the $6.05 rests on **$12.10 of spend and 2 results**.
Treat the *direction* as unambiguous and the *precision* as meaningless. This angle is ranked first
because two different systems point the same way, not because of that one number.

**Copy notes.** The product is the hook — lead with the interface, not with a claim about it. No
adjectives doing work the screen recording already does.

---

## Angle 2 — **"Stop bog-and-sanding curves on site."** (the problem)

**Rank: 2. The #1 documented pain, in the customer's own words.**

| | |
|---|---|
| **Register** | Problem naming. Say the thing they hate out loud |
| **Core line** | Kerf it, laminate it, bog it, sand it. Or open a browser |
| **Pain addressed** | Rework · waste · inconsistency · **cracks at the join** |
| **Proof it's true** | Machine-cut to the radius. No kerfing, no laminating, no filler |
| **Families** | `static_craft` (lead), `avatar`, `before_after` (when unblocked) |
| **CTA** | See what it costs → `/products/radius-online` |

**Why it ranks second.** `brand/audience.md` lists it first and it is the most *visceral* of the
documented pains — bog-and-sand is hours of a Friday nobody enjoys. Under Andromeda, a specific
problem statement is the targeting mechanism: write the problem precisely and Meta finds whoever has
it (§1.2). This is the angle that does that job.

**It ranks second, not first, only because the demo angle has account evidence behind it and this one
has customer evidence.** Both are strong; one has been measured on Meta and the other hasn't yet.

**Copy notes.** High-sophistication audience — **do not explain what kerfing is.** Naming the
technique correctly is the credential. This is also the natural home for the confirmed converter
**"bendy ply"**.

⚠️ This angle's strongest possible execution — a real before/after — is **blocked on photography**
(bible §4.3 family 6, Part 9 item 7). Until those two photos exist it runs as `static_craft` on
existing macro photography, which is weaker than it needs to be.

---

## Angle 3 — **"Cut to your set-out. Dispatched in three days."** (the outcome)

**Rank: 3. The certainty angle — narrower, but it closes.**

| | |
|---|---|
| **Register** | Outcome and certainty. What lands on the truck |
| **Core line** | Parts arrive cut, labelled and ready to fix |
| **Pain addressed** | Tight deadlines · programme risk · rework when a curve doesn't fit |
| **Proof it's true** | 3 business days · large curves auto-split with **Part IDs engraved** |
| **Families** | `cad_render` (lead), `static_craft`, `configurator` |
| **CTA** | Check your lead time → `/products/radius-online` |

**Why it ranks third.** It's true, it's differentiating, and the Part-ID detail is genuinely
persuasive to anyone who has assembled a split curve from unlabelled parts. But it's a *reassurance*
angle — it converts someone already considering the product rather than creating the consideration.
That makes it a strong retargeting angle and a weaker cold one.

**Copy notes.** The engraved Part IDs are the single most specific, least copyable detail Craftons
has. Show them. Specificity is the proof.

---

## How the angles map onto the launch batch

Per bible §4.3, diversity comes from spanning **families**, and per §4.6 everything runs in **one ad
set**. Angles cross families rather than owning them — so a batch of 15–20 covers 3 angles × 4
families without any two ads being the same idea twice.

| Family | Ads | Angle mix |
|---|---|---|
| `configurator` | ~5 | Mostly A1, some A3 |
| `static_craft` | ~4 | Mostly A2, some A3 |
| `cad_render` | ~3 | A3 lead, A1 support |
| `avatar` | ~4 | A2 lead, A1 support — **presenter only** (§4.2) |
| `before_after` | 0 | ⛔ blocked on photography |

**Guardrails this must satisfy** (enforced by `meta-ads.mjs check-batch`, not by good intentions):
≥15 creatives · ≥3 distinct families · ≤40% synthetic · every avatar script passes the ACL
first-person test.

---

## Register — how these ads sound

**Ad tone is not social tone.** STATUS.md learned this the hard way and the bible repeats it: social
is value-first with soft CTAs and the brand barely present; **paid is direct, product-forward, and
asks for the click.** Do not let `SOCIAL-VOICE.md` leak into this batch.

- Australian spelling throughout — optimise, metre, labelled
- Trade register, no explaining down. They know what a set-out is
- Second person about the product. **Never first person about experience** — an AI presenter claiming
  personal use is an ACL s18/s29(1)(e) breach (§4.2), enforced in `_meta-policy.mjs`
- No exclamation marks, no "revolutionary", no "game-changer"
- Every claim must be literally true of the product as shipped: 3 business days, Part IDs engraved,
  auto-split. Nothing aspirational

---

## Open

- **Before/after photography** — unblocks the strongest execution of Angle 2. Still the highest-value
  thing Lee can supply (bible Part 9 item 7)
- **Reference-frequency ranking is unavailable** for this niche; if Lee wants it, the practical source
  is Craftons' own inbox and phone notes, not Reddit
- **Angle 3's cold-traffic performance is untested** — it's ranked third on reasoning, not data. The
  launch batch will settle it
