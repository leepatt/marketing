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
In our own facility in Fairfield, Victoria. Nothing is outsourced — that's how we hold the lead time.

**How long until I get my parts?**
Dispatched within 3 business days of checkout. No quote to wait on.

**What does delivery cost?**
Calculated at checkout once you've entered your address. You'll see it before you pay.

**Do you deliver interstate?**
Yes, through FedEx. Someone needs to be on site to take delivery, and if FedEx charges extra to unload
by hand, that's passed on to you.

**Can I return a custom part?**
No. Every part is made to your dimensions, so there's nothing to put back on a shelf. Check your
numbers before you check out.

**Does anyone check my set-out before it's cut?**
No. What you enter is what the machine cuts — nothing gets misread, but nothing gets caught either.
The set-out is yours. Check it on the 3D preview before you pay. If you spot a mistake after ordering,
tell us quick — if it hasn't hit the machine, we can fix it.

**Do you do trade pricing?**
Yes. Apply for a trade account and we'll get your rates sorted —
[craftons.com.au/pages/trade-account](https://craftons.com.au/pages/trade-account).

---

## Radius Pro block

Shown on `/products/radius-online` (and the material-specific Radius Pro pages).

**How accurate is the cut?**
±0.5mm. That's why parts land on your set-out instead of near it.

**What materials and thicknesses can I get?**

| Material | Thickness |
|---|---|
| Formply | 17mm |
| BC structural plywood | 15mm, 18mm, 25mm |
| MDF standard | 12mm, 18mm |

All cut from 2400 × 1200mm sheets.

**Do I need CAD files or drawings?**
No. Enter your radius, width and angle in the configurator — it does the rest. No drafting, no DWG,
no waiting on someone else's file.

**What's the biggest part you can make?**
Any radius. Parts longer than 2300mm are split automatically so they nest on a standard sheet.

**Why has my curve arrived in pieces?**
Anything over 2300mm is split so it fits a 2400mm sheet and travels safely. The joins are cut to the
same ±0.5mm, so they close up clean.

**What are the numbers engraved on my parts?**
Part IDs. Every piece is engraved so you know what goes where, and in what order. Follow the numbers.

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
      "acceptedAnswer": { "@type": "Answer", "text": "In our own facility in Fairfield, Victoria. Nothing is outsourced — that's how we hold the lead time." } },
    { "@type": "Question", "name": "How long until I get my parts?",
      "acceptedAnswer": { "@type": "Answer", "text": "Dispatched within 3 business days of checkout. No quote to wait on." } },
    { "@type": "Question", "name": "What does delivery cost?",
      "acceptedAnswer": { "@type": "Answer", "text": "Calculated at checkout once you've entered your address. You'll see it before you pay." } },
    { "@type": "Question", "name": "Do you deliver interstate?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes, through FedEx. Someone needs to be on site to take delivery, and if FedEx charges extra to unload by hand, that's passed on to you." } },
    { "@type": "Question", "name": "Can I return a custom part?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. Every part is made to your dimensions, so there's nothing to put back on a shelf. Check your numbers before you check out." } },
    { "@type": "Question", "name": "Does anyone check my set-out before it's cut?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. What you enter is what the machine cuts — nothing gets misread, but nothing gets caught either. The set-out is yours. Check it on the 3D preview before you pay. If you spot a mistake after ordering, tell us quick — if it hasn't hit the machine, we can fix it." } },
    { "@type": "Question", "name": "Do you do trade pricing?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Apply for a trade account at https://craftons.com.au/pages/trade-account and we'll get your rates sorted." } },
    { "@type": "Question", "name": "How accurate is the cut?",
      "acceptedAnswer": { "@type": "Answer", "text": "±0.5mm. That's why parts land on your set-out instead of near it." } },
    { "@type": "Question", "name": "What materials and thicknesses can I get for Radius Pro?",
      "acceptedAnswer": { "@type": "Answer", "text": "Formply 17mm, BC structural plywood 15mm, 18mm and 25mm, and standard MDF 12mm and 18mm. All cut from 2400 x 1200mm sheets." } },
    { "@type": "Question", "name": "Do I need CAD files to order a curve?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. Enter your radius, width and angle in the configurator — it does the rest. No drafting, no DWG." } },
    { "@type": "Question", "name": "What is the biggest part Radius Pro can make?",
      "acceptedAnswer": { "@type": "Answer", "text": "Any radius. Parts longer than 2300mm are split automatically so they nest on a standard 2400 x 1200mm sheet." } },
    { "@type": "Question", "name": "Why has my curve arrived in pieces?",
      "acceptedAnswer": { "@type": "Answer", "text": "Anything over 2300mm is split so it fits a 2400mm sheet and travels safely. The joins are cut to the same ±0.5mm, so they close up clean." } },
    { "@type": "Question", "name": "What are the numbers engraved on my parts?",
      "acceptedAnswer": { "@type": "Answer", "text": "Part IDs. Every piece is engraved so you know what goes where, and in what order." } }
  ]
}
```

---

## Two notes on wording

**The "nobody checks it" answer.** The whole reframe sits in one clause — *nothing gets misread, but
nothing gets caught either*. It gives you the genuine upside of going straight from screen to machine
and admits the cost in the same breath, which is more convincing than either half alone.

It must not imply anyone is checking. It says the set-out is yours, points at the 3D preview as the
check, and closes with the pre-manufacture fix. If a customer ever disputes a wrong part, this wording
is what you stand on — so it stays unambiguous.

**Merged question.** "What if I get my dimensions wrong?" and "Does anyone check my set-out?" were the
same question answered twice. Now one.

**Trade pricing.** Written thin on purpose: it confirms trade pricing exists and sends people to the
application page, without inventing discount rates or thresholds. If there's a headline number worth
leading with — a percentage, a spend threshold, terms — send it and this becomes a much stronger answer.

---

## Rollout

1. Strip the six demo entries from Avada. **Today** — the fake hotline is the urgent bit.
2. Load core + Radius Pro into Avada, publish to `/pages/avada-faqs`.
3. Add the Avada block to `/products/radius-online`, directly under the configurator. This is the
   conversion win — the product page currently has no FAQ block at all.
4. Verify schema in Google's Rich Results Test.
5. Repeat step 3 for Formwork Builder, Architrave Builder and Rip Pro once their blocks are written.
