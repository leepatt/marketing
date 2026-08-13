# Pool builders — what they actually use Radius Pro for

_Investigated 2026-08-13 from live Shopify order data. This closes the open question in
`radius-pro-product-truth.md`: **"Pool builders: confirm what they use it for, or park it? No copy until
confirmed."** It is now confirmed._

---

## 🔴 It is NOT set-out. It is concrete formwork.

Lee's standing guess was *"Lee thinks set-out, unconfirmed."* **The order data says otherwise, and the
evidence is not ambiguous.**

Every pool-builder part ever ordered is **17mm Formply**, with **joiner blocks included and used**, and
**split into segments**. Set-out templates would need none of those three things — you do not build a
set-out template from structural formwork, you do not need joiner blocks to hold a template's line, and
you do not split a template into six pieces.

Per Lee's own product briefing, joiner blocks are *"mostly used for concrete formwork — the concreters
build their curved wall, put studs in between the plates, put bendy ply on it."* **Pool builders are
using Radius Pro exactly like concreters use it.** They are building the formwork for the pool shell.

## The customers — 3 companies, 4 orders, $3,487

| Company | Orders | Revenue | What they ordered |
|---|---:|---:|---|
| **Cronulla Pools** (`mlainson@`) | **2** | **$2,302** | 7 parts at R1450–2070, W100, A180 · then 2 parts at **A360** |
| **Riviera Pools** (`accounts@`) | 1 | $804 | **7 parts, 7 different radii** (R300–2600), W150, A90/180, with tails |
| **TLC Pools** (`sean@`) | 1 | $381 | 1 part **A360**, R1750, W90, Qty 2, split 6 |

**Two signals worth more than the revenue:**

1. **Cronulla Pools came back in 17 days** (7 Jul → 24 Jul). A repeat buyer inside three weeks means the
   product worked on the first pool. That is the strongest possible product-fit signal from this data.
2. **Average order value $871.75 against a site AOV of $614.67 — 42% higher.** Pool builders are not a
   marginal segment; they are the highest-value orders in the account.

Two more pool companies have accounts but have never ordered: **Pool Power** and **Peninsula Pool
Steel** (pool reinforcement, likely a different job entirely).

## 🔑 The finding that makes the creative write itself

**All three full-circle (360°) orders in the entire account came from pool builders. Three out of three.
Nobody else has ever ordered one.**

Parsed 129 distinct part configurations from every order since 1 May. The angle distribution:

| Angle | Parts | Who |
|---|---:|---|
| 90° | 54 | the standard quarter-arc — feature walls, benches, general |
| 180° | 16 | mixed |
| **360°** | **3** | **pool builders only** |

At R1750–1790 internal, a 360° circle is a **round spa or plunge pool roughly 3.5m across**, split into
6 segments. That is a shape nobody else on this account builds.

### The two distinct pool jobs, both visible in the data

- **The round spa / plunge pool** — one radius, 360°, split into 6, ~10 joiner blocks. Cronulla and TLC.
- **The freeform pool** — Riviera's order is seven curves at seven different radii (2600, 2250, 1920,
  1800, 1450, 600, 300) with **tails** (`SL:200 EL:200`, `SL:400 EL:400`) to meet the straight runs.
  That is a kidney/freeform perimeter, set out curve by curve.

The 300mm and 600mm radii in that order are tight returns — steps, a bench, or a spa nook inside the
main shell.

---

## The ad — LF7, pool builders

**Register:** `real_footage` long-form, per `radius-pro-longform-copy.md`. Same template as the winner.

> **Primary text**
>
> A round spa is the bit of the job that eats the week.
>
> Setting out a three-and-a-half metre circle in formply is slow, and it only works if every segment
> matches the one next to it. One out by a few millimetres and you can see it in the shell for the life
> of the pool.
>
> Type the radius into Radius Pro instead. The software splits the circle into segments, nests them to
> save sheets, and the CNC cuts them right. 17mm Formply, every part engraved with its part ID, joiner
> blocks included where the segments meet.
>
> Freeform is the same job with more radii. Seven different curves on one pool is a normal order — add a
> tail where a curve has to meet a straight run and it lands ready to stand.
>
> Build the frame, stud between the plates, sheet it in bendy ply, brace it and pour.
>
> Delivered in 3 days, anywhere in Australia.

- **Headline:** Round spas, cut to the radius
- **Description:** Segments, joiner blocks and tails. Delivered in 3 days
- **CTA:** Shop Now → `/products/radius-online`
- **Family:** `real_footage`
- **Angle:** `lf`

### Why the copy says what it says

| Line | Grounded in |
|---|---|
| "three-and-a-half metre circle" | R1750–1790 × 2 = ~3.5m. Real numbers from real orders |
| "splits the circle into segments" | `Split:6` on every 360° order |
| "joiner blocks included where the segments meet" | 10 blocks on the round orders, 6 on the freeform. Legitimate here — concreter-method audience, so the concreters-only rule is satisfied |
| "17mm Formply" | `form-17` on 100% of pool parts |
| "Seven different curves on one pool" | Riviera's actual order |
| "add a tail where a curve has to meet a straight run" | `SL:`/`EL:` on Riviera's parts |
| "sheet it in bendy ply" | Bendy ply as a **complement**, never the problem — the standing rule |

**Banned words checked and absent:** bog · bogging · kerf · kerfing · curve bending · laminating ·
wiggle wood · bendy-ply-as-the-problem.

---

## ⚠️ Do NOT launch this as a paid ad yet

The standing rule (`BUILD-CHECKLIST` B2, and the reason July failed) is: **don't segment at launch —
identity words multiply a proven winner, they don't find one.** The TOF test went live 2026-08-13 and has
no winner yet. Running a pool variant now splits signal across creative that has never converted, which
is precisely what cost $1,279.94 for 2 results in July.

**Gate: hold LF7 until one of LF1–LF3 (or an Ardreagh ad) produces real conversions.** Then clone the
winner and swap in this copy — same as LF4 (concreters) and LF5 (landscapers), which are already written
and waiting behind the same gate.

### 🟢 But there IS something free to do now — organic Instagram

Lee: *"we do have some pool builders follow us on IG and buy from us."* An organic IG post costs nothing,
doesn't touch the ad test, and reaches an audience that has already self-selected. Per `SOCIAL-VOICE.md`
this is value-first with the brand barely present:

> **IG caption**
>
> A 3.5 metre spa, cut as six segments.
>
> The circle gets set out in the software, not on the slab. Every segment engraved with its part ID so
> the stack goes together in order, joiner blocks where they meet.
>
> 17mm Formply. Stud it, sheet it, brace it, pour.
>
> Freeform's the same job with more radii — seven curves on one pool is a normal week.

**Best asset for it:** a photo of a round spa formwork standing on site, segments visible. **We don't
have one.** Worth asking Cronulla Pools — they are a repeat buyer, and `@lawlessconstruction` already
said yes to exactly this ask.

---

## What would make this stronger

1. **Ask Cronulla Pools what the round ones were.** Spa, plunge pool, or water feature? One reply
   settles the single word the copy leans on. They have bought twice; they will probably answer.
2. **A photo of round pool formwork.** This is the `real_footage` gap again, and it is the only thing
   standing between LF7 and a genuinely native ad.
3. **Check the IG follower list for pool companies** — if there are materially more than three, the
   segment is bigger than the order data shows and worth its own budget once a winner exists.
