# Harry — HeyGen avatar shot list

_Harry is the Craftons head of marketing. He shoots content on site and works from
the studio. No suits, no blazers, no ties, and **no branding on any garment** — the
logo comes later, composited from the real vector rather than drawn by a model._

**Hero reference:** `hero-reference-LOCKED.png` — the approved weathered frame.
Every shot is generated from it and scored against it before it counts.

## The rule this list is built around

The face is the deliverable. Everything else — wardrobe, set, angle — exists to give
HeyGen variety around a face that never changes. So the list is weighted toward the
angles that keep the face square-ish to camera, where identity is easiest to hold and
most useful to train on. Extreme profiles are capped at four of thirty: they are worth
having for range, they score lower by nature, and a set full of them trains badly.

Every frame is checked with `face-check.py` against the hero before it is accepted.

## Angle spread across the 30

| Angle | Count | Why |
|---|---|---|
| Front-on, eye level | 10 | The workhorse — what HeyGen leans on most |
| Three-quarter (5 each way) | 10 | Range without losing the face |
| Near-profile (2 each way) | 4 | Edge of usable; looser similarity bar |
| Low angle | 3 | Looking up at him, as on site |
| High angle | 3 | Looking down, seated or in close |

Expressions rotate through neutral, mid-sentence speaking, slight smile and
listening, so the avatar has more than one resting face to work from.

## Wardrobe

**On site** — puffer vest over short-sleeve khaki · black polo · black jumper
**Studio** — black hoodie + straight-leg jeans · boxy white tee · Craftons-green
jumper · thick navy overshirt

All plain. No logo, wordmark, embroidery, print or badge.

## Sets

- **Site interior** — near-finished high-end home, cardboard floor protection
- **Studio** — plain marketing office, no camera gear in frame
- **Outdoor site** — curved concrete bench seat formed up ready to pour

## The 30

### Site interior (1–10)

| # | Wardrobe | Angle | Beat |
|---|---|---|---|
| 01 | Vest + khaki | Front-on, eye level | Speaking to camera, open living area |
| 02 | Vest + khaki | Three-quarter right | Slight smile, beside a tall window |
| 03 | Vest + khaki | Low angle | Neutral, standing in a wide doorway |
| 04 | Vest + khaki | Near-profile right | Looking off camera, plain plastered wall |
| 05 | Black polo | Front-on, eye level | Half smile, hand on stone benchtop |
| 06 | Black polo | Three-quarter left | Listening, wide hallway |
| 07 | Black polo | High angle | Looking up to lens, base of the stairs |
| 08 | Black jumper | Front-on, eye level | Calm and direct, large open room |
| 09 | Black jumper | Three-quarter right | Mid-sentence, near full-height glazing |
| 10 | Black jumper | Near-profile left | Thoughtful, hallway depth behind |

### Studio (11–20)

| # | Wardrobe | Angle | Beat |
|---|---|---|---|
| 11 | Hoodie + jeans | Front-on, eye level | Seated at desk, leaning on forearms |
| 12 | Hoodie + jeans | Three-quarter left | Slight smile against a plain white wall |
| 13 | Hoodie + jeans | Low angle | Mid-stride, glancing to lens |
| 14 | White tee | Front-on, eye level | Warm and open, clean background |
| 15 | White tee | Three-quarter right | Listening, soft daylight |
| 16 | White tee | High angle | Seated at a table with a notebook |
| 17 | Green jumper | Front-on, eye level | Relaxed, even key light |
| 18 | Green jumper | Three-quarter left | Mid-sentence speaking |
| 19 | Navy overshirt | Front-on, eye level | Seated, attentive, hands on desk |
| 20 | Navy overshirt | Near-profile right | Leaning on a desk edge, directional light |

### Outdoor site (21–30)

| # | Wardrobe | Angle | Beat |
|---|---|---|---|
| 21 | Vest + khaki | Front-on, eye level | Speaking to camera, formwork behind |
| 22 | Vest + khaki | Three-quarter right | Slight smile, warm morning light |
| 23 | Vest + khaki | Low angle | Hand on the top edge of the form |
| 24 | Vest + khaki | Three-quarter left | Neutral, overcast even light |
| 25 | Black polo | Front-on, eye level | Calm and direct, bright daylight |
| 26 | Black polo | Near-profile left | Looking along the line of the formwork |
| 27 | Black polo | High angle | Looking up to lens, form in frame |
| 28 | Black jumper | Front-on, eye level | Half smile, hands in pockets |
| 29 | Black jumper | Three-quarter right | Mid-sentence, golden hour side light |
| 30 | Black jumper | Three-quarter left | Listening, reinforcement mesh behind |

## Working method

One at a time. Generate, score against Harry, show the pair side by side, get a
verdict, then move on. Nothing is generated in bulk and nothing is accepted on the
strength of looking roughly right in a contact sheet — which is how the last set
passed review and then fell apart on inspection.
