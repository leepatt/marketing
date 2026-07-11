# Craftons Configurator — Cinematic Content Engine (WORKSHOP — IN PROGRESS)

_Started 2026-07-11. Branch: `claude/craftons-config-builder-live-yes248`._
_This is a live workshop doc. The end product is a detailed build spec to hand to a session inside the **cnccut-app** repo. Do not treat anything here as final until the "LOCKED SPEC" section exists at the bottom._

---

## Why this exists

- Content pillar **Sell** = weekly short videos showing the Craftons configurator building real, buildable products so customers see what's possible.
- Blocker: it's **hard to get good footage of the configurator**. Screen-recording the live tool looks rough — janky 3D, browser chrome, cursor issues, wrong aspect ratio, loading states, and you can't reliably hit the same result twice.
- The live configurator instance on the cnccut-app **isn't live / doesn't work** yet.
- So we're speccing a **cinematic content engine**: a controllable system that turns the configurator + real footage into polished 9:16 reels, repeatably, every week. Quality bar is non-negotiable — this ships weekly and represents the brand.

## The vision (from Lee, Round 1)

A tool to create **clever, cinematic animations**. Ingredients, combined per clip:
1. **The Craftons website configurator** — shown building and designing products (the "software in action" beat).
2. **Real-life video** — actual products/jobs on site or in place.
3. **Signature move: the match.** Real video of, e.g., a concrete bench seat, alongside the configurator building that *exact* seat at the *exact* same dimensions. The digital twin.
4. **Compositing** — animations laid on top of real video.

## Locked so far

- **Output format:** 9:16 vertical, IG / TikTok reels. Fast, native, not agency-glossy-slow.
- **Reference register:** slick **SaaS product-demo** videos (UI motion, clean, confident). No single reference locked yet — to be gathered.
- **Tool identity:** option (D) — a combination of live-configurator capture + separate 3D/Blender animation + real-footage compositing + a "made-for-film" mode.
- **Blender:** in scope; **Claude drives Blender headless** (Python / `bpy`). Used for animating finished parts, the build process, and product-in-context / on-top-of-video work.
- **Who builds the actual tool:** a future session inside the **cnccut-app** repo, from the spec this workshop produces.

## The existing configurator (facts, for the spec)

- Repo: `leepatt/craftons-curves-calculator` — Next.js 15, TypeScript, Tailwind, **Three.js / React Three Fiber** 3D, SVG/DXF export for CNC, `/api/mcp` quote endpoint.
- Builders: Curves (`/`), Radius Pro, Ripping, Formwork, Stair, Box, Pelmet, Cut Studio, Curved Architraves, Concrete Stair Formwork, 3D Letters.
- Geometry + pricing live in code (e.g. `src/app/components/curves/pricing.ts`, per-app `manifest.ts` / `*-parts.ts`) — reusable by a renderer so animations are dimensionally-accurate to the real product/price.
- Deploys to Vercel (`craftons-curves-calculator.vercel.app`, syd1); embeds in the Craftons Shopify store via `section-*.liquid` iframes.

---

## OPEN QUESTIONS (being worked — Round 2+)

- Architecture fork: purpose-built cinematic renderer (reuse geometry, full camera control) vs. screen-capture the real app.
- Blender vs web-3D split: what renders where.
- The "match" workflow: how real footage is sourced/filmed and aligned to the configurator output.
- Output granularity: finished reels vs. clean components assembled in CapCut; who edits.
- Weekly workflow: input → output; how one-command vs hands-on.
- Which products/scenes to support first.
