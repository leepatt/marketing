# Radius Pro — Meta ad copy (v2, current)

_Written 2026-08-03 from Lee's product briefing. **This is the live copy set.**_
_Source of truth for the product: `radius-pro-product-truth.md`. Supersedes `copy-reconciliation.md` §4._

**All 15 point at `/products/radius-online`.** Format: **headline** (~27–40 chars) ·
**primary text** (front-load the first ~125 chars — the rest truncates behind "…more").

---

## The register these are written in

Lee: *"Just stick to what the app is."*

**Banned words:** bog · bog-and-sand · sand · kerf · kerfing · curve bending · bending ply as a problem ·
laminating · hand-templating · wiggle wood. None of it is related to the job.

**The pain, as it actually is:** you do the maths, you draw the radius on a sheet, you cut it with a
jigsaw. It takes time, not everyone can do the maths, it's hard to mark out accurately, your blokes
make mistakes, and a lot of the sheet goes in the bin.

**The answer:** the software draws it perfectly, nests it to save sheets, the CNC cuts it perfect,
every part is engraved with its radius, and it's on site in 2–3 days anywhere in Australia.

**Not in general copy:** joiner blocks (concreters only — hold for post-winner variants).

---

## The batch — 15 creatives

### Angle 1 — the maths and the marking out (the pain nobody has written yet)

| # | Family | Headline | Primary text |
|---|---|---|---|
| 1 | `static_craft` | Nobody's Marking Out Curves | Doing the maths, drawing the radius on a sheet, cutting it with a jigsaw. Or type the radius in and it turns up cut. |
| 2 | `static_craft` | The Maths, Done | Not everyone on the tools can set out a radius, and it shows. Type the dimensions in — we draw it and cut it. |
| 3 | `avatar` | Put the Jigsaw Down | Curved top and bottom plates, cut on the CNC to the radius you type in. Most orders on site in 2–3 days. |
| 4 | `static_craft` | Marked Out Wrong Again | Every curve marked out by hand is a chance to get it wrong. Cut ours on the CNC and it's right the first time. |
| 5 | `cad_render` | Straight Off the Plans | Take the radius off the plan, type it in, get the plates cut. No setting out, no templates, no guessing. |

### Angle 2 — waste and nesting (new — the cost argument)

| # | Family | Headline | Primary text |
|---|---|---|---|
| 6 | `configurator` | Less Sheet in the Bin | We nest your curves on the sheet the most efficient way there is. You pay for parts, not offcuts. |
| 7 | `cad_render` | Your Offcuts Are the Problem | Marking curves out by hand wastes most of the sheet. Nested properly, the same job takes fewer sheets. |
| 8 | `static_craft` | Nested. Not Guessed. | The software lays every curve out for minimum waste before a single cut is made. Priced online. |
| 9 | `configurator` | Price It Before You Commit | Type your radius, pick your ply, see the price on the spot. Nested for minimum waste, cut on the CNC. |

### Angle 3 — what lands on the truck

| # | Family | Headline | Primary text |
|---|---|---|---|
| 10 | `cad_render` | Nobody Measures It On Site | Every part turns up engraved with its part ID. Sort the stack, fix it to the plan, get on with the job. |
| 11 | `static_craft` | Cut Perfect. Labelled. Done. | Curved top and bottom plates, cut on the CNC and engraved with the part ID. Ready to fix when it lands. |
| 12 | `configurator` | Interstate in Days, Not Weeks | Australia-wide through FedEx. Type the radius, we cut it — most orders on your site in 2–3 days. |
| 13 | `avatar` | Curved Wall Plates, Any Radius | Top and bottom plates for curved timber frames. Double them up if you want the wall stiffer. |
| 14 | `configurator` | Add a Tail to Your Radius | Need the curve to meet a straight frame? Extend the leg 100, 200, 300mm — whatever it takes. |
| 15 | `cad_render` | Curved Walls, Cut to the Plan | Curved walls are everywhere in Aussie homes now. Take the radius off the plan and have the plates cut. |

---

## What changed from v1, and why

| v1 said | v2 says | Why |
|---|---|---|
| *"No hand-templating, no bog-and-sand"* (#7) | Cut entirely | Lee: *"that's just not related to the job at all"*. Supersedes the 2026-07-21 approval |
| *"Every Part ID Engraved"* · *"Part IDs cut into the face"* (#12) | *"engraved with its part ID"* | Lee, on review: *"sometimes it's part radius, sometimes part ID. I think saying part ID is safe to use in copy."* So **both occur** — a blanket "every plate says its radius" would be false on some jobs. **v1 was right and my mid-session correction was wrong**: part ID is the safe blanket claim |
| *"A Splice Piece for Every Join"* (#11) · joiner blocks (#14) | Removed from general copy | **Joiner blocks are concreters only.** Holds for post-winner concreter variants |
| *"Cut this week"* / dropped the day count | *"Most orders on site in 2–3 days"* | Lee confirms 2–3 days **delivered**, Australia-wide via FedEx — so my earlier kill of the three-day claim was over-cautious. **Hedged to "most orders" on Lee's call**, because order data shows 5 days on a 27-sheet job and cold traffic doesn't know what a big job is |
| Nothing on waste | Four ads on nesting and waste | **The biggest miss in v1.** It's in client feedback, it's a cost argument, and no competitor makes it |
| Nothing on tails or doubling up | #13, #14 | Both confirmed features, both in the order data (`SL:`/`EL:`) |
| Pain = rework and bog-and-sand | Pain = the maths, marking out, mistakes, waste | v1 had the wrong pain. This is Lee's, from client feedback |

---

## Guardrails (`meta-ads.mjs check-batch`)

| Requirement | This batch |
|---|---|
| ≥15 creatives | ✅ 15 |
| ≥3 distinct families | ✅ 4 — `static_craft` (6) · `configurator` (4) · `cad_render` (4) · `avatar` (2) |
| ≤40% synthetic | ⚠️ Depends on render mix — `avatar` is 2/15 (13%) |
| Avatar scripts pass the ACL first-person test | ✅ #3 and #13 make no first-person experience claim |

⚠️ **Copy only.** The images still show a 900mm decorative arc; the product is 90mm plates at
multi-metre radii in runs of 16–60. **Do not ship these words over those pictures.**

---

## Held back deliberately

- **Joiner blocks / "splice piece for every join"** — true, strong, and **concreters only**. First
  concreter variant off a proven winner.
- **File friction / "send us the plan"** — the best-evidenced pain in the market, but Plan Scan is in
  beta and the Drive golden rule stands. Revisit when beta ends.
- **Any guarantee** — deferred by Lee, reassess after month one.
- **Pool builders** — unconfirmed use case. No copy until Lee confirms.
