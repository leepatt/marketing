# Craftons — brand rules

> Craftons makes customisable building products that remove complexity from construction:
> CNC-manufactured components, configured online, delivered ready to install.
>
> **Tagline:** Building Smarter Starts Here. We help you build better.

Australian-made, precision-engineered building products. Visual identity is **dark forest green +
black + warm off-white**, with a signature **curved-line pattern motif** (wood-grain abstracted
into a Lissajous figure) used as a watermark behind hero text. Photography is **product-on-white**
(catalogue) or **environmental portraits** of tradies on site — warm, real, unstaged.

This file is the quick-reference rule set. The **exact, complete token values** live in the
canonical `colors_and_type.css` in Drive — see `SOURCE.md`. Values below are the confirmed
anchors; pull the CSS for the full set.

## Colour (confirmed anchors)

| Token | Hex | Use |
|-------|-----|-----|
| `--craftons-green` | `#194431` | Primary deep forest green — the brand signature; live-site theme colour |
| `--craftons-green-700` | `#123022` | Darker green (hover/depth) |
| `--craftons-green-900` | `#0a1c14` | Darkest green panels |
| `--craftons-line-green` | `#2d8a5b` | Brighter line-art green — the curve patterns on dark grounds |
| `--black` | `#000000` | Black grounds |
| `--ink` | `#0e0e0c` | Near-black body text |

Plus a warm neutral ramp (ink → slate → stone → rule → paper → white) — **no blue cast** — and
semantic success/warning/danger. Fetch `colors_and_type.css` for exact neutral + semantic hexes.

**Rules:** no gradients on UI surfaces. No emoji. Always reference colours via `var(--token)`,
never raw hex (enforced by the system's lint config).

## Typography

| Role | Family | Notes |
|------|--------|-------|
| Display | **Aeonik** (geometric grotesk) | Licensed `.otf` family in Drive `fonts/` (12 weights + italics) |
| Body | **Inter** | Google Fonts; highly legible |
| Condensed | **HWT Artz** → **Big Shoulders Display** (fallback) | Compliance/spec stamps |
| Stencil | **Anton** (+ Big Shoulders Display) | Loud spec callouts |
| Mono | **JetBrains Mono** | Spec readouts / numbers |

- Type scale is **display-heavy** — builders read fast; lean on big hierarchy.
- Aeonik is the only display face. Don't substitute it when the licensed files are available.

## Voice (builder-to-builder)

- **Builder-to-builder.** Written by people who've been on site. Explains *why it matters*, not
  *what it is* (assumes the reader knows "NCC 2025", "7-star energy rating").
- **Confident, not boastful.** "We help you build better." not "World-class solutions."
- **Action-first headlines**, imperative and period-terminated: *Building Smarter Starts Here.*
  *Build Now. Add to Cart. Save and Share.*
- **No marketing jargon** ("synergy", "leverage", "ecosystem"). Use trade language: *cavity batten,
  formply, radius, chord length.*
- **"We" = Craftons, "you" = the builder.** Never "the customer".
- Testimonials use **first name + last initial** ("Samuel C.", "Tanya B.").

## Casing

- **Sentence/Title case for headlines**, periods kept tight.
- **ALL CAPS reserved for compliance + spec callouts** (*EXCEEDS NCC 2025 STANDARDS*, *ENABLES
  7-STAR ENERGY RATINGS*, *4.8M LONG STICKS*) — always paired with a condensed/stencil face.

## The motif & components

- **Curved-line motif** is the brand's signature device. Use it **big, once per page, behind hero
  text.** Pattern PNGs live in Drive `assets/` (green-on-black curve / loop, green-on-green,
  deep-green tonal variants).
- **Buttons:** ~6px radius (`--r-md`), dark green, square-ish.
- **Spacing** is a 4px scale (`--sp-1` = 4px … `--sp-13` = 128px).
- **Radii:** 0 / 2 / 4 / 6 (default) / 10 / 16 / pill.
- **Marquee strip** (all-caps, pipe-separated, scrolling) is a singular Craftons device.
- **Spec stamps / compliance block** — typographic compliance icons in the condensed/stencil face
  on a patterned green panel.

## Product & framework reference
- Products: Radius Pro, Bending Plywood, Formply, Structural Vented Cavity Batten.
- Four-feature framework: **Design & Visualize / Rapid Production / Pre-Fab Perfection / Smart Parts.**
- The **Formwork Builder** configurator is the "world-first" in-house tool (the hero product story).
