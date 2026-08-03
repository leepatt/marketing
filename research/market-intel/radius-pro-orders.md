# Radius Pro — what customers actually order

_First-party intel, pulled from the Shopify Admin API 2026-08-03. Sample: the 15 most recent
Radius Pro orders (product `8464537125042`), read from `lineItems.customAttributes` — the
configurator writes every curve spec into the order._

**This is the highest-value research done so far, and it contradicts the ad creative already
rendered.** The ads show a decorative quarter-arc. The product is something else.

---

## 🔴 The headline: this is a curved WALL PLATE product

**Width is 90mm on the overwhelming majority of parts ordered.**

90mm is a **stud width**. These are **top and bottom plates for curved stud walls** — structural
framing components, not decorative curves. Confirmed by an enquiry in the same period:

> *"We have included all curved 90mm stud walls. Double top and double bottom…"*
> — Craftons Plan Scan quote, Pleasant St

Widths seen across the sample: **90mm** (dominant) · 150 · 250 · 100 · 170 · 40.

## The radii are building-scale, not furniture-scale

| Order | Radii ordered (mm) |
|---|---|
| #1275 | 1725 · **10182** · 1749 |
| #1274 | **5073 · 3714 · 2710 · 3897 · 4895** · 1808 · 3624 · 2620 · 3807 · 1704 |
| #1258 | 888 · **6160 · 9100 · 9260 · 13750** · 500 · 610 · 1000 |
| #1259 | **3509 · 5009** |

**Multi-metre radii are normal.** A 900mm radius — what my ads show — is at the *small* end.

## Material

`form-17` (17mm formply) dominates, then `BC-25` (25mm BC structural ply). **Formply is the
workhorse**, which fits the formwork/structural use.

## Quantities are production runs, not one-offs

`Qty:16` · `Qty:20` · `Qty:25` · `Qty:60`. Someone ordering 60 parts is framing a building, not
making a bench seat.

## Order values run well above the headline AOV

Sample range **$196 → $5,465**, mean ≈ **$1,090** — against the trailing-365-day AOV of $614.67.
Recent orders are materially bigger. Worth re-checking the AOV that feeds break-even CAC.

---

## ✅ Claims VERIFIED by order data

These were unverified in `radius-pro-interview.md` §1. The order attributes settle three of them:

| Claim | Verdict | Evidence |
|---|---|---|
| **Part IDs engraved** | ✅ **TRUE** | `_part_id_engraving: "Included"` on every order |
| **Turnaround** | ⚠️ **We're under-promising** | `_total_turnaround` is **"2 days"** on most orders, 3 on some, 5 on a 27-sheet job. It **scales with size**. "Three business days" is conservative but imprecise |
| **"Nothing to fill at the join"** | ❌ **FALSE — and the truth is better** | `_joiner_blocks: "Included"`, quantities 4–95. Splits are joined with **supplied joiner blocks**, not filler |

**The joiner-block finding kills the misleading ad and replaces it with a stronger, true claim.**
The honest line isn't "nothing to fill" — it's *"splits come with joiner blocks, so it goes back
together on your line."* That's a real product feature I was papering over with a false one.

## Splits are routine, not exceptional

`Split:2` through `Split:10` appear constantly. My ad framed splitting as a special feature; it's an
everyday part of how the product works — which makes the joiner blocks more important, not less.

---

## Other findings

- **Plan Scanner is already producing orders.** #1271 carries `_source: "plan-scanner"` and a
  `_plan_scan_id`. It is live, not "coming soon".
- **Tangent legs are common** — `SL:`/`EL:` (start/end leg) on many parts.
- **Attribution is mostly `direct`**, some Google, **one from `facebook.com`** (#1273, $371) — a real
  Meta-attributed order in the sample.
- **Projects are named by address** — "6 Avalon Road, Armadale — Basement", "FF Retreat". Residential
  construction, often multiple orders per site (#1274 and #1275 are the same address, different rooms).

---

## What this means for the ads

**Every rendered ad is aimed at the wrong picture of the product.**

| My ad assumed | Reality |
|---|---|
| Decorative quarter-arc, 900mm radius, 150mm wide | **Curved wall plates, 90mm wide, multi-metre radii** |
| One part | **Qty 4–60, production runs** |
| Splitting is a notable feature | Splitting is routine — **the joiner blocks** are the feature |
| "Nothing to fill at the join" | **Joiner blocks supplied** |
| Buyer designs a curve online | Many send plans; **Plan Scan** exists for exactly that |

### The angle this suggests, which nobody has written yet

Not *"design your curve online"* and not *"stop bog-and-sanding"* — but something closer to:

> **"Curved stud walls, set out and cut. 90mm plates, any radius, with joiner blocks and Part IDs
> engraved."**

That is specific (Suby's U-U-S-U), it's true, it uses the trade's own frame (stud walls, plates,
set-out), and it describes what people are actually buying.

### Still to verify with Lee

- Is "curved wall plates for stud walls" genuinely the primary use, or just the highest-volume one?
- What are joiner blocks, exactly — and do they solve the join, or just locate it?
- Is the recent higher AOV a trend or a few big jobs?
- Is Plan Scan ready to be pointed at in ads, or still soft-launch?
