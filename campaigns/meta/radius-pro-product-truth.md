# Radius Pro — what it actually is

_From Lee, 2026-08-03, in his own words. **This is the product source of truth.** Where any other doc
in this repo disagrees with this one, this one wins._

> **Why this doc exists:** every copy failure so far traces to writing about the product without a
> description from someone who makes it. This is that description. `radius-pro-interview.md` §1–§3 is
> now largely answered by it.

---

## The one-liner

**Software Craftons built to cut curves in timber.** The customer inputs their dimensions and receives
the parts cut perfect, labelled, ready to go on site.

---

## The pain it removes — in Lee's words

This is the real pain, and it is **not** what earlier copy assumed.

Currently, on site, a builder / concreter / landscaper has to:

1. **Do some maths** — *"not everyone is able to do the maths to figure it out"*
2. **Draw it out on a sheet of plywood** — *"it's hard to actually measure a radius and mark it out on
   a piece of plywood"*
3. **Cut it with a jigsaw**

**What goes wrong, per client feedback:**

- **Mistakes** — *"the amount of mistakes that happen from their workers marking them out and cutting them"*
- **Waste** — *"the amount of waste that goes in the bin"*
- **Time** — *"this can be pretty time consuming"*

> ### 🔴 What is NOT the pain — Lee, explicitly
>
> *"I've noticed that on some ads, it talks about curve bending and bogging and all of this stuff.
> Like, that's just not related to the job at all. So we don't need to include any of that. Just stick
> to what the app is."*
>
> **Banned from all Radius Pro copy: bog-and-sand · bogging · kerfing · kerf bending · curve bending ·
> bendy-ply-as-the-problem · laminating · wiggle wood.**
>
> This **supersedes** the Lee-approved 2026-07-21 line *"No hand-templating, no bog-and-sand"* and
> retires launch Angle 2 as written. The approval was real; this instruction is later and more
> specific. **Bending ply is a complement, not a competitor** — concreters fix bendy ply *to* the
> frame Radius Pro cuts.

---

## What the software does

| Step | What happens | Why it matters |
|---|---|---|
| 1 | **Perfectly draws the radius** | Removes the maths and the marking-out |
| 2 | **Nests the parts on the sheet in the most efficient way** | **Minimal waste.** Nothing in the bin |
| 3 | **Cuts it perfect on the CNC** | Removes worker marking/cutting mistakes |
| 4 | **Labels every part with its radius measurement** | Saves set-out time on site |
| 5 | **Ships in 2–3 days** | Australia-wide via **FedEx**, interstate included |

**Nesting/waste is the biggest thing missing from every ad written so far.** It's a cost argument, it
comes straight from client feedback, and no competitor makes it.

### Parts labelling — corrected

*"It will label all of the parts for you with different radius measurements. For example, if you had
four plates that were 900 millimetres, all of those plates would engrave 900 millimetres on the plate.
Just saves set-out time."*

> ✅ **Resolved by Lee on review:** *"Sometimes it's part radius, sometimes part ID. I think saying
> part ID is safe to use in copy."*
>
> **So it's both, depending on the job — and "part ID" is the safe blanket claim.** A copy line saying
> *"every plate says its radius"* would be false on some orders. Use **part ID**.
>
> Worth noting: the original copy said "Part IDs engraved" and I *corrected* it to "radius" mid-session
> off Lee's 900mm example. That correction was wrong. The Shopify attribute `_part_id_engraving` was
> right all along.

### Joiner blocks — CONCRETERS ONLY

*"We also offer joiner blocks. This is mostly used for concrete formwork. The concreters can build
their curved wall, put studs in between the plates, put bendy ply on it. And when they join their
frames together, they put this joiner block on top. **The joiner blocks are only for concreters**, not
for carpenters or anything like that."*

⚠️ **This kills joiner blocks as general-audience copy.** Two of the fifteen ads led on it. It belongs
in concreter-targeted creative only — see the segmentation note below.

### Tails

*"You can actually add a tail to the radius. So if you have your radius that's 900mm but you want to
join it to a wall frame, you can extend that by 100, 200, 300 millimetres, whatever it is."*

✅ Confirms the `SL:` / `EL:` (start leg / end leg) attributes seen throughout the order data.

---

## Who it's for

| Buyer | What they use it for | Detail |
|---|---|---|
| **Carpenters & builders** | Curved timber **wall frames** | Top and bottom plates. *"Curved walls are getting really popular in houses in Australia at the moment."* Measurements come **off the plans** → into Radius Pro → cut to site. Some **double them up** — two at top, two at bottom, to strengthen the wall |
| **Concreters** | Curved **concrete walls** | Build the frame, add **bendy ply** to form the curved former, pour concrete inside. The joiner-block user |
| **Landscapers** | Similar method to concreters | |
| **Pool designers / builders** | Enquiries received; Lee thinks **set-out**, unconfirmed | Don't write copy for this until confirmed |

✅ **"Double top and double bottom"** independently confirms the Plan Scan quote in
`enquiry-language.md` (*"all curved 90mm stud walls. Double top and double bottom"*) and the 90mm
dominance in the Shopify order data. Three sources agree.

---

## ⚠️ Lee's segmentation suggestion — and the evidence against it

Lee: *"Maybe if we just do targeted copy for concreters, landscapers."*

**That is the right instinct and the wrong time.** July ran exactly this — creative hand-segmented by
trade — and it was the worst money the account has spent:

| Ad | Spend | Results | Cost/result |
|---|---|---|---|
| AD5 **Chippies** | $758.74 | 1 | **$758.74** |
| AD1/AD2/AD6 (Concreters, Landscapers, Carpenters) | $370.48 | **0** | — |
| Retargeting — **Configurator** (not segmented) | $12.10 | 2 | **$6.05** |

**The rule already agreed** (`BUILD-CHECKLIST.md` B2): *don't segment at launch; use identity words to
multiply a winner once one exists.* Suby's identity hack is a **scaling lever on proven creative** —
duplicate a winner and swap the trade word. July segmented from scratch, splitting signal across
creative that had never worked.

**So:** launch broad and problem-led. The moment one ad wins, clone it into concreter and landscaper
variants — and *that* is where the joiner-block copy goes, because it's true for exactly that audience.

---

## Claims — status after this briefing

| Claim | Status | Note |
|---|---|---|
| **2–3 days, delivered, Australia-wide via FedEx** | ✅ Lee's own framing | Reverses my earlier kill of "on site in three days". I flagged it unverified; it's now verified — though see the open question on big jobs |
| **Parts labelled/engraved with the radius** | ✅ True | But it's the *radius*, not a part ID |
| **Efficient nesting → minimal waste** | ✅ True | **New. Unused in any ad so far** |
| **Cut perfect on the CNC** | ✅ True | |
| **Tails / leg extensions** | ✅ True | |
| **Joiner blocks included** | ✅ True — **concreters only** | Not general copy |
| **Bendy ply is the slow way round** | ❌ Dead | It's a complement. Concreters fix it to our frame |
| **Bog-and-sand / kerfing framing** | ❌ Dead | *"Not related to the job at all"* |

---

## ✅ Answered by Lee, 2026-08-03

| Q | Answer | Effect on copy |
|---|---|---|
| **Engraving** — radius or part ID? | **Both, job-dependent. "Part ID" is safe to use** | Copy says *"engraved with its part ID"*. A blanket "says its radius" would be false on some jobs |
| **2–3 days on big jobs?** | ~~Hedge it~~ → **REVERSED on review: "Safe to say orders delivered in 3 day. Not most orders."** | **Flat claim: "Delivered in 3 days."** No hedge, in every ad. Lee saw the hedged version rendered and overrode it — 3 days is the safe upper bound, so hedging bought nothing and cost the punch |
| **Radius limits?** | **No practical limit in normal use** | *"Any radius"* is fair. Used in #13. Multi-metre radii are normal and worth showing |

## Still open

1. **Waste — is there a number?** *"Minimal waste"* is vague, and this is now the strongest unused
   argument we have. A figure would make it far stronger — *"most jobs come off a sheet fewer"* or a
   percentage. Even a rough comparison from two or three real jobs (sheets nested vs sheets if marked
   out by hand) would do. **Highest-value outstanding answer.**
2. **Materials:** order data shows 17mm formply dominant, then 25mm BC structural ply. Is the full
   list formply / structural ply / MDF? Anything we should *not* name?
3. **Pool builders:** confirm what they use it for, or park it? No copy until confirmed.
