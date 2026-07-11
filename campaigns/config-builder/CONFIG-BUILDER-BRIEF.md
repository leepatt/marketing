# Craftons Config Builder — consolidated brief (recovered from prior chat)

_Last updated 2026-07-11. Branch: `claude/craftons-config-builder-live-yes248`._
_Purpose: gather everything discussed about the Craftons config builder ("configurator") so we can get it live. This repo is docs-only; the live app lives in a separate code repo (below)._

---

## TL;DR — where things actually stand

- The config builder is **real and already built**: a Next.js "Calculator Suite" in repo **`leepatt/craftons-curves-calculator`**.
- It is **already deployed** to Vercel at **`https://craftons-curves-calculator.vercel.app`** (region `syd1`), auto-deploying on push to `main`.
- It **embeds into the Craftons Shopify store** (`craftons-au.myshopify.com` / craftons.com.au) via Liquid `section-*.liquid` files in an iframe, with cart accumulation over `postMessage` → `/cart/add.js`.
- So "get it running live on the cnccut app" = **finish/verify the production deploy + the Shopify embed**, not build from scratch.

## The builders in the suite (routes)

| App | Route | Shopify section | Status (per DEPLOYMENT_GUIDE) |
|-----|-------|-----------------|------|
| Curves | `/` | `CORRECTED_FULL_SECTION.liquid` | Ready |
| Radius Pro | `/apps/radius-pro` | (shared with Curves) | Ready |
| Ripping | `/apps/ripping` | `section-ripping.liquid` | Ready |
| Formwork | `/apps/formwork` | `section-formwork.liquid` | Ready |
| Box Builder | `/apps/box-builder` | needs section | App ready |
| Stair Builder | `/apps/stair-builder` | needs section | App ready |
| Pelmet Pro | `/apps/pelmet-pro` | needs section | App ready |
| Cut Studio | `/apps/cut-studio` | needs section | App ready |
| Curved Architraves | — | `section-curved-architraves.liquid` | in repo |
| Concrete Stair Formwork | `/apps/concrete-stair-formwork` | `section-concrete-stair-formwork.liquid` | in repo |
| 3D Letters | `/apps/3d-letters` | `section-3d-letters.liquid` | in repo |

Tech: Next.js 15 (App Router), TypeScript, Tailwind, Three.js/R3F for 3D, SVG export for CNC. Also hosts a remote **MCP endpoint** (`/api/mcp`) so LLMs can quote + return a checkout link.

## Deploy path (from DEPLOYMENT_GUIDE.md)

1. Push to `main` → Vercel auto-builds (`npm run build`, output `.next`).
2. Required env vars in Vercel: `NEXT_PUBLIC_SHOP_DOMAIN`, `NEXT_PUBLIC_DOLLAR_VARIANT_ID`, `SHOPIFY_ADMIN_ACCESS_TOKEN`, `SHOPIFY_WEBHOOK_SECRET`, `MCP_API_KEY`, `BLOB_READ_WRITE_TOKEN` (for share links), optional per-app `*_DOLLAR_VARIANT_ID`.
3. Add each `section-*.liquid` into the Shopify theme, place on the product page, ensure the cart handler is present (accumulate, don't replace).
4. `$1` hidden product provides the price-by-quantity variant.
5. Formwork: register `orders/paid` webhook → `/api/webhooks/order-paid` to append production-file download links to order notes.

---

## The concept (from Lee & Jake call, 2026-06-11 — Drive vault)

- Customer punches in dimensions → live preview → live price → Add to Cart / Save & Share, with **shop drawings auto-generated**.
- Two headline flavours: **Radius Pro** (curved parts) and **Formwork Builder** (curved formwork for concrete pours).
- Go-to-market: productise onto the site for customers; hand an **early-access beta** to Jed (tier-2 builder) and spec the tool (incl. fixing system) with his estimator.
- Pricing = Jake's "Mario's pricing" spreadsheet handed to Claude as a **live, auto-updating** source; extra fees for angle/difficult cuts.
- Positioning: **Australian-made, local, short lead time** — do not compete on price. Not chasing mass market / T1 stadium jobs.
- Insight: the configurator is also a **design-comprehension tool** — Peter (Cartform) ran Craftons on one screen + plans on the other and it "helped me figure out a lot about this project."
- Radius Pro plan-reading MVP: DXF/DWG first (offline, no LLM); PDF/image-vision wall-detection later.

## Content assets already produced (Drive, 2026-06-14)

- `ConfiguratorScreen.jsx` — working React prototype (radius/width/angle + material, live SVG curve preview, arc/chord derivation, `calcPrice()`, Add to Cart).
- `Craftons Meta Ad - Radius Configurator.html` — 1080×1350 Meta ad, phone mockup of the configurator UI.
- `Craftons Radius Pro Ad D Configurator.html` — 1080×1350 ad using a real screenshot.
- `phone-configurator-v3.png` — screenshot of the live configurator.
- `Craftons-formwork-builder-promo.md` — 25-sec vertical promo video script (shot-by-shot + AI-gen prompts + CapCut edit plan).

## Flags to fix before content ships

- **"Kraftons" / kraftons.com.au** appears in the promo doc — brand is **Craftons / craftons.com.au**. Placeholder typo; correct before publishing.

## Open routing note

- `leepatt/cnccut-app` (the dashboard repo) exists but was **not** added to this session; `leepatt/craftons-curves-calculator` (the config builder) **was**. Confirm whether "live on the cnccut app" means (a) this suite's own Vercel+Shopify deploy (current design) or (b) embedding it inside `cnccut-app`.
