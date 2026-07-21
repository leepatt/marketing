# Radius Pro TOF — creative assets index

> The rendered ad images (`*.png`) are **gitignored** per repo policy (media lives in Google Drive,
> not in git). This file is the tracked index of what the creative set is. Binaries are delivered to
> Lee directly and belong in the Drive brain under `…/Marketing/03 Content/` (or the campaign folder).

## Status: v1 DRAFT — imagery under review (2026-07-21)

The photo-based concepts (AD1, AD2, AD4) were rendered with **AI-generated placeholder imagery**
(Replicate `flux-1.1-pro`) to prove out layout + copy. **Per the bible rule "real footage leads; AI
extends," these are being workshopped** — the plan is to swap in **real Craftons curved-job photos**
(and/or Craft Macro stills) before launch. AD3 + AD5 are pure brand-graphic / configurator renders
and are launch-ready as-is.

## The set (each concept → 3 sizes)

| File stem | Concept | Segment | Imagery (v1) | Launch-ready? |
|-----------|---------|---------|--------------|---------------|
| `ad1-builder-pain_*` | Pain-first native photo | Builder | AI (→ swap real) | pending photo |
| `ad2-builder-spec_*` | Spec-stamp macro | Builder | AI (→ swap Craft Macro) | pending photo |
| `ad3-builder-number_*` | Number card / configurator | Builder | vector, no photo | ✅ ready |
| `ad4-concretor-question_*` | Question hook native photo | Concreter | AI (→ swap real) | pending photo |
| `ad5-concretor-pour_*` | Identity card | Concreter | graphic + faint texture | ✅ ready |

Sizes per concept: `_1080x1350.png` (4:5 feed), `_1080x1080.png` (1:1 square),
`_1080x1920.png` (9:16 stories/reels).

## Reproduce / re-render

The render pipeline (design system + templates + Playwright/sharp render) lives in the session
scratchpad (`design.mjs`, `render.mjs`, `gen_images*.sh`). Fonts: Manrope (Aeonik stand-in — swap
licensed Aeonik from Drive for final), Inter, Anton, JetBrains Mono. Wordmark is a typeset stand-in —
swap the Drive `logo-wordmark.svg` before final.

## Copy → see `../AD-CONCEPTS.md`. Launch plan → see `../LAUNCH-GUIDE.md`.
