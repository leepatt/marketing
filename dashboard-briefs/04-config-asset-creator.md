# Brief 04 — Craftons Config Asset Creator

_Depends on Brief 01 and pairs with Brief 03 (Studio). Bridges the product configurator → marketing._

---

## 1. Goal

Turn a **Craftons product configuration** — a specific configured product (Radius Pro curve, a
Formwork Builder job, curved architraves, a bending-ply spec) — into a set of **on-brand marketing
assets**: a spec/proof card, a "how this curve was built" visual/animation, social-ready product
shots, and an ad creative. The configurator is Craftons' hero story ("world-first in-house tool");
this tool mines each real configuration for marketing gold, rendered pixel-exact from real data.

> **Interpretation flag for Lee:** I've read "Config asset creator" as *"generate marketing assets
> from a product configuration (the Formwork Builder / Radius Pro configurator)."* If you meant
> something else (e.g. a generic asset-template configurator, or managing config *files*), say so and
> I'll re-scope — see Open Questions.

## 2. Why it exists

Real configurations are the ultimate anti-slop input: exact geometry, real dimensions, real specs.
`QUALITY-DOCTRINE` says heroes should be *rendered from real data, not AI-imagined* — a configuration
is that data. Every quote/order can become a "Built with Craftons" or "How This Curve Was Built"
(the flagship pillar) asset with receipts, at near-zero marginal effort.

## 3. Users & control model

Internal. The tool proposes an asset set from a configuration; a human approves before it's used.
Customer-identifying details are excluded/anonymised unless we have permission (testimonials use
first name + last initial per brand rules).

## 4. Inputs

**Synced brand docs (`docs/marketing/`):**
- `craftons-design/BRAND.md` — the four-feature framework (Design & Visualize / Rapid Production /
  Pre-Fab Perfection / Smart Parts), products (Radius Pro, Bending Plywood, Formply, Cavity Batten),
  compliance-stamp styling, curve motif, spec-stamp faces.
- `CONTENT-PILLARS.md` — the flagship **"How This Curve Was Built"** + **"Built with Craftons"** lanes.
- `QUALITY-DOCTRINE.md` — render-from-real-data law; the "lead with product in interactive 3D /
  exploded view" motion note.
- `pipeline/templates/*` + `tokens.css` — the render substrate (shared with Studio, Brief 03).
- `campaigns/adwords/ads/*` — proven product angles/copy (Radius Pro, formwork, architraves).

**Live data:**
- The **configurator/product data** in cnccut.app (the actual source of truth — the session must find
  where configurations/quotes live in this repo/DB).
- **Shopify** (connected) — product info, verified product URLs (Radius Pro `/products/radius-online`,
  Formwork, Curved Architraves), pricing/specs.

## 5. MVP vertical slice

**Configuration in → an on-brand spec/proof card out.**

1. A page (or an action on an existing configuration/quote view) where a config is selected — start
   with one product (recommend **Radius Pro** or the **Formwork Builder** job, the hero story).
2. `tools/config-assets.mjs render-card --config <id>` maps the configuration's real fields (radius,
   chord length, material, dimensions, compliance flags) into a content JSON.
3. Renders a **spec/proof card** template (Studio's render pipeline) — big display type, spec stamps
   in the condensed/stencil face, compliance callouts in ALL CAPS, curve motif, product-on-white or
   the actual configured geometry visual.
4. Gate 1 brand-check → asset library `needs-approval` → Approval drawer → approved asset with the
   source config id as provenance.

## 6. Backend — `tools/config-assets.mjs`

- `list-configs [--product radius|formwork|architrave]` — read configurations/quotes from the app DB.
- `render-card --config <id>` — map config → content JSON → spec/proof card (via Studio render).
- `asset-set --config <id>` — (post-MVP) produce the full set: card + social still + ad creative +
  "how it was built" storyboard/animation.
Anonymises customer data by default; `CONFIRM=1` only needed if an outward action is added later.

## 7. Frontend — Config Assets page

- Config picker (filter by product/date/status) sourced from the app's configuration data.
- Field mapping preview (config field → asset placeholder) so a human can sanity-check before render.
- Rendered asset preview + Gate 1 badges + Approval drawer; "Send to Social/Meta" handoff.

## 8. Data model additions

Reuse `assets` (link `source_config_id`) + `runs`. Add a `config_snapshots` cache if configs aren't
already persisted in a form the tool can reference stably.

## 9. Post-MVP backlog

- **"How This Curve Was Built"** animated build-up (the flagship): drive an exploded-view/build
  animation from the real geometry (Blender/3D or the configurator's own 3D), per the motion rules.
- Full asset set per config (card + reel + carousel + ad variant) in one run.
- Auto-trigger: new completed quote/order over a threshold → draft a "Built with Craftons" asset for
  approval (with permission gating).
- Interactive 3D/exploded-view embed lead (proven to convert for manufacturers).

## 10. Guardrails, safety, cost

Geometry/specs come **from the real configuration**, never AI-invented. Customer data anonymised
unless permissioned. Human approval before any asset is used externally.

## 11. MVP acceptance criteria

- [ ] A real configuration can be selected in the cockpit.
- [ ] Its fields map into a rendered, on-brand spec/proof card (correct specs + compliance styling).
- [ ] Gate 1 brand-check runs; asset lands `needs-approval` with the source config id as provenance.

## 12. Open questions

- **Scope confirm:** is this "assets *from* a product configuration" (my read) — and if so, where do
  configurations/quotes live in cnccut.app (DB table? API?) so the tool can read them?
- Which product to start with — Radius Pro, or the Formwork Builder job (the hero story)?
- Permission model for using a real customer's job in marketing (opt-in? anonymise-only?).
- Does the configurator expose the 3D geometry we can render, or only spec fields (text/dimensions)?

---

## Kickoff prompt (paste into a fresh cnccut.app session)

> Build the **Config Asset Creator module** following brief `04-config-asset-creator.md` and the
> shared conventions in `01-foundation-cockpit-shell.md`. Foundation shell + `docs/marketing/` +
> the Studio render pipeline (Brief 03) should exist — reuse the render pipeline, don't duplicate it.
> First, find where product **configurations/quotes** live in this repo/DB and document it in
> `docs/marketing/APP-NOTES.md`. Then ship the MVP: pick a real configuration (start with Radius Pro
> or the Formwork Builder job), map its real fields into a content JSON, render an on-brand
> **spec/proof card** (spec stamps + ALL-CAPS compliance callouts + curve motif, specs pulled from the
> config, never AI-invented), run the Gate-1 brand-check, and land it in the asset library
> `needs-approval` with the source config id as provenance. Anonymise customer data. If my scope read
> is wrong (see the brief's Interpretation flag), stop and ask before building. New branch, logical
> commits.
