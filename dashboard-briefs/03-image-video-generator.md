# Brief 03 — Image / Video Generator (the Studio)

_Depends on Brief 01. Wraps the existing `pipeline/` render system + Replicate/Glif._

---

## 1. Goal

A **Studio** module that produces on-brand images and videos through the cockpit: render deterministic
brand assets from templates (the existing `pipeline/`), and generate/extend media with AI
(Replicate/Glif) under the anti-slop constraints. Output flows into an asset library, brand-checked,
awaiting human approval, ready for the Social organiser (Brief 05) and Meta/Google ads.

## 2. Why it exists

We need volume without slop. `QUALITY-DOCTRINE.md` is the law: **render real things, constrain the AI,
a human curates.** Heroes (product shots, the Formwork Builder reel) are rendered pixel-exact from
real data; AI only fills the edges (b-roll, backgrounds, extension). This tool operationalises that
system so every session produces consistent, on-brand media instead of one-off looks.

## 3. Users & control model

Internal. AI **proposes**, a human **disposes** — nothing enters the "approved" library or ships
without Gate 2 (human pick). Gate 1 is an automated brand/adherence self-check before a human ever sees
it. Generation costs money (Replicate/Glif) — show estimated cost before a run; draft on cheap models,
spend on finals.

## 4. Inputs

**Synced brand docs (`docs/marketing/`):**
- `QUALITY-DOCTRINE.md` — the anti-slop stack + the pre-ship checklist (encode as Gate 1).
- `craftons-design/BRAND.md` + `pipeline/tokens.css` (interim) / canonical `colors_and_type.css` —
  colours, type (Aeonik/Inter), curve motif, spacing, "no gradients/emoji".
- `pipeline/README.md` + `pipeline/templates/*` + `pipeline/content/*.json` — the render system:
  content JSON + HTML template → PNG via headless browser + sharp.
- `research/2026-motion-design.md`, `research/2026-production-stack.md` — motion rules + tooling.
- `briefs/craft-macro-shoot-brief.md`, `CONTENT-PILLARS.md` — what we're producing and for which lane.

**Live APIs / tooling:**
- **Replicate** (`REPLICATE_API_TOKEN`) — AI image/video gen, b-roll, extension, touch-up.
- **Glif** (`GLIF_API_TOKEN`) — templated image gen / ad-creative variants.
- **Local media tooling** — Playwright (already in env), sharp, `ffmpeg` (needs adding to the
  cnccut.app build/setup — see `INTEGRATIONS.md` B9).

## 5. MVP vertical slice

**Render a brand template to a finished PNG from the cockpit, brand-checked, into the asset library.**

1. Studio page lists available templates (from `pipeline/templates/`) and a content-JSON form.
2. User fills the form (headline, product, spec) → `tools/studio.mjs render` runs the existing
   `render.mjs` (template + content JSON → PNG via Playwright + sharp).
3. **Gate 1 auto-check:** adherence lint (no raw hex/px/off-system fonts; on-brand tokens) + the
   `QUALITY-DOCTRINE` checklist surfaced as pass/flag items.
4. Output lands in the **asset library** with status `needs-approval`; the Approval drawer lets a
   human approve/reject. Approved assets store a Drive + Vercel Blob ref on the `assets` row.
5. Then wire **one AI path** as the second slice: an image via Glif/Replicate from a locked style,
   through the same Gate 1 → library → approval flow, with a pre-run cost estimate.

## 6. Backend — `tools/studio.mjs`

- `render --template <t> --content <json>` — deterministic template render (wraps `pipeline/render.mjs`).
- `gen-image --prompt <p> [--style <lockedStyle>] [--model draft|final]` — Replicate/Glif; prints a
  cost estimate; `CONFIRM=1` to actually spend on final models.
- `gen-video / extend` — (post-MVP) ffmpeg assembly of real footage + AI b-roll/extension.
- `brand-check <file>` — run the Gate 1 adherence + checklist, return pass/flags.
Every run writes a `runs` row (model, cost, prompt/provenance) and an `assets` row.

## 7. Frontend — Studio page

- Template gallery + content form (live preview if feasible via the render endpoint).
- AI-gen panel: prompt, locked-style selector, draft/final toggle, **cost estimate before run**.
- Asset library grid: thumbnail, type, brand-check badges, status, provenance, source refs; filter by
  pillar/status. Approval drawer on each. "Send to Social/Meta" action (hands off to Briefs 05/02).

## 8. Data model additions

Reuse shared `assets` + `runs`. Add `styles` (locked Craftons AI styles: Recraft style / FLUX LoRA
id, sample refs) so AI gen always draws from an approved look, per `QUALITY-DOCTRINE` layer 3.

## 9. Post-MVP backlog

- Video: ffmpeg assembly of Tia's footage → Reels/cuts; AI b-roll/extension; motion rules from research.
- Carousel/story/testimonial/compliance-block templates (pipeline "next" list).
- Train + register a locked Craftons AI style (Recraft/FLUX LoRA) on ~10–30 approved pieces.
- Swap interim `tokens.css` for canonical `colors_and_type.css`; add licensed Aeonik `.otf`s; pull real
  curve-motif PNG + logo from Drive.
- Auto-atomise one Tia shoot into multiple outputs (stills + reel cuts + carousel frames).

## 10. Guardrails, safety, cost

Hero geometry/dimensions are **rendered from real data, never AI-imagined**. In-image text is
human-verified (AI text fails ~20%). Cost estimate before every paid run; draft cheap, spend on
finals; `CONFIRM=1` for final-model spend. Nothing ships without Gate 2.

## 11. MVP acceptance criteria

- [ ] A template renders to a finished on-brand PNG from the cockpit.
- [ ] Gate 1 adherence check runs and reports pass/flags.
- [ ] Asset lands in the library `needs-approval` and can be approved with stored provenance + refs.
- [ ] One AI-gen path works through the same flow with a pre-run cost estimate.

## 12. Open questions

- Is `ffmpeg` available in the cnccut.app build/runtime, or do we add it (B9)?
- Are the canonical design CSS + Aeonik `.otf`s + motif PNGs synced from Drive yet, or still interim?
- Do we train a locked AI style now (needs ~10–30 approved pieces) or start template-only?

---

## Kickoff prompt (paste into a fresh cnccut.app session)

> Build the **Studio (image/video generator) module** following brief `03-image-video-generator.md`
> and the shared conventions in `01-foundation-cockpit-shell.md`. The Foundation shell +
> `docs/marketing/` must exist. Port the existing `pipeline/` render system (content JSON + HTML
> template → PNG via Playwright + sharp) into a `tools/studio.mjs` backend and a `/marketing/studio`
> page. Ship the MVP: render a brand template to a finished PNG, run the `QUALITY-DOCTRINE` Gate-1
> adherence check, and land it in an asset library as `needs-approval` with provenance, approvable via
> the shared Approval drawer. Then wire one AI-gen path (Glif/Replicate from a locked style) through
> the same flow with a pre-run cost estimate and `CONFIRM=1` for final-model spend. Hero
> geometry/dimensions are rendered from real data, never AI-imagined; nothing ships without human
> approval. New branch, logical commits.
