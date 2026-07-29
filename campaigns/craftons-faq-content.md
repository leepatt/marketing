# Craftons FAQ — content + placement

_Drafted 2026-07-27. Facts supplied by Lee; materials pulled live from the configurator's
`/api/materials.json`. Voice per `SOCIAL-VOICE.md` / `brand/voice-profile.md`._

---

## Placement: two jobs, one set of answers

Write each answer once. Publish it in two places.

| Where | Blocks shown | Job |
|---|---|---|
| **Product pages** (Radius Pro first) | Core + that product's block | **Conversion.** 11,288 sessions land on `/products/radius-online`. Kills objections mid-configurator. |
| **`/pages/avada-faqs`** | Core + every product block | **Support + SEO.** Currently 0 landing sessions. One link to send customers; catches long-tail search. |

Put the product-page block **directly under the configurator**, before the contact form. That's where
someone stalls — mid set-out, wondering if it'll fit on the truck.

> ### ⚠️ Do this first
> `/pages/avada-faqs` is currently live with untouched Avada demo copy — a `17track.net` link and
> **"call us at hotline: 123456XXX"** — wrapped in `FAQPage` schema. Delete those six entries before
> publishing anything else.

---

## Core FAQ — Craftons-wide

Applies to every product: Radius Pro, Formwork Builder, Architrave Builder, Rip Pro.

**Where are Craftons parts made?**
In our own facility in Fairfield, Victoria. Every part is cut here — nothing is outsourced and nothing
is sitting in a container somewhere. That's how we hold the lead time.

**How long until I get my parts?**
Dispatched within 3 business days of checkout. No quote to wait on, no back-and-forth — you order, we
cut, it ships.

**What does delivery cost?**
Calculated at checkout once you've entered your address. You'll see the exact figure before you pay.

**Do you deliver interstate?**
Yes, through FedEx. Two things worth knowing before you order: someone needs to be on site to take
delivery, and if FedEx charges extra for a manual unload, that gets passed on to you. Have a hand
available and it's a non-issue.

**Can I return a custom part?**
No. Every Craftons part is made to your dimensions, so there's nothing to put back on a shelf — it's
your curve, cut to your set-out. Check your numbers before you check out.

**What if I get my dimensions wrong?**
You're responsible for the set-out you enter. But if you spot it early, tell us straight away — if the
job hasn't hit the machine yet, we can adjust it. Once it's cut, it's cut.

---

## Radius Pro block

Shown on `/products/radius-online` (and the material-specific Radius Pro pages).

**How accurate is the cut?**
±0.5mm. That's CNC tolerance, not chippy-with-a-jigsaw tolerance. It's why the parts land on your
set-out instead of near it.

**What materials and thicknesses can I get?**

| Material | Thickness |
|---|---|
| Formply | 17mm |
| BC structural plywood | 15mm, 18mm, 25mm |
| MDF standard | 12mm, 18mm |

All cut from 2400 × 1200mm sheets. Pick your material in the configurator and the price updates as you go.

**Do I need CAD files or drawings?**
No. Enter your radius, width and angle in the configurator and it does the rest. If you can read a
set-out, you can order a curve — no drafting, no DWG, no waiting on someone else's file.

**What's the biggest part you can make?**
Any radius you like. Parts longer than 2300mm get split automatically so they nest on a standard sheet
— see the next question.

**Why has my curve arrived in pieces?**
Because a 6-metre curve doesn't come off a 2.4m sheet, and it wouldn't fit on the truck if it did.
Anything over 2300mm is split automatically at the design stage. The joins are cut to the same ±0.5mm,
so they close up clean on site.

**What are the numbers engraved on my parts?**
Unique part IDs. Every piece is engraved so you know exactly what goes where and in what order —
no laying eleven near-identical segments on the slab and guessing. Follow the numbers.

---

## FAQPage schema

Replace the existing boilerplate JSON-LD on `/pages/avada-faqs` with this. Avada generates schema from
whatever entries you save, so getting the entries right should regenerate it — verify with Google's
Rich Results Test afterwards.

Worth setting expectations: Google restricted FAQ rich snippets to government and health sites, so this
won't win you star-style results in search. It's still worth having — AI answer engines, Google's own
AI overviews, and site search all parse it.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "Where are Craftons parts made?",
      "acceptedAnswer": { "@type": "Answer", "text": "In our own facility in Fairfield, Victoria. Every part is cut here — nothing is outsourced." } },
    { "@type": "Question", "name": "How long until I get my parts?",
      "acceptedAnswer": { "@type": "Answer", "text": "Dispatched within 3 business days of checkout." } },
    { "@type": "Question", "name": "What does delivery cost?",
      "acceptedAnswer": { "@type": "Answer", "text": "Calculated at checkout once you've entered your address. You'll see the exact figure before you pay." } },
    { "@type": "Question", "name": "Do you deliver interstate?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes, through FedEx. Someone needs to be on site to take delivery, and any extra FedEx charge for a manual unload is passed on to the customer." } },
    { "@type": "Question", "name": "Can I return a custom part?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. Every Craftons part is made to order from your dimensions, so returns aren't available. Check your numbers before you check out." } },
    { "@type": "Question", "name": "What if I get my dimensions wrong?",
      "acceptedAnswer": { "@type": "Answer", "text": "You're responsible for the set-out you enter. If you tell us before the job goes to manufacturing, we can adjust it." } },
    { "@type": "Question", "name": "How accurate is the cut?",
      "acceptedAnswer": { "@type": "Answer", "text": "±0.5mm CNC tolerance." } },
    { "@type": "Question", "name": "What materials and thicknesses can I get for Radius Pro?",
      "acceptedAnswer": { "@type": "Answer", "text": "Formply 17mm, BC structural plywood 15mm, 18mm and 25mm, and standard MDF 12mm and 18mm. All cut from 2400 x 1200mm sheets." } },
    { "@type": "Question", "name": "Do I need CAD files to order a curve?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. Enter your radius, width and angle in the online configurator and it does the rest." } },
    { "@type": "Question", "name": "What is the biggest part Radius Pro can make?",
      "acceptedAnswer": { "@type": "Answer", "text": "Any radius. Parts longer than 2300mm are split automatically so they nest on a standard 2400 x 1200mm sheet." } },
    { "@type": "Question", "name": "Why has my curve arrived in pieces?",
      "acceptedAnswer": { "@type": "Answer", "text": "Anything over 2300mm is split automatically at the design stage so it fits a standard sheet and transports safely. Joins are cut to the same ±0.5mm tolerance." } },
    { "@type": "Question", "name": "What are the numbers engraved on my parts?",
      "acceptedAnswer": { "@type": "Answer", "text": "Unique part IDs. Every piece is engraved so you know what goes where and in what order during assembly." } }
  ]
}
```

---

## Still needed before publish

Two answers I've deliberately left out rather than guess:

- **Trade accounts.** `/pages/trade-account` exists and took 59 sessions in 90 days, but I don't know
  the terms. Worth an FAQ entry — "Do you do trade pricing?" is a question every builder asks. Send me
  the terms and I'll write it.
- **Does anyone check my file before it's cut?** Your answer to Q5 says the customer owns the set-out
  and you can adjust pre-manufacture. What I don't know is whether a human actually eyeballs each job
  first. If someone does, say so — it's the single most reassuring thing you can tell a first-time
  buyer spending $800 on parts they can't return.

---

## Rollout

1. Strip the six demo entries from Avada. **Today** — the fake hotline is the urgent bit.
2. Load core + Radius Pro into Avada, publish to `/pages/avada-faqs`.
3. Add the Avada block to `/products/radius-online`, directly under the configurator. This is the
   conversion win — the product page currently has no FAQ block at all.
4. Verify schema in Google's Rich Results Test.
5. Repeat step 3 for Formwork Builder, Architrave Builder and Rip Pro once their blocks are written.
