# Brief 08 — Execution order & dependencies

_How the tools depend on each other, and the order to build them in. Read alongside `00-INDEX.md`._

---

## The one hard rule

**Build the Foundation (Brief 01) first.** Everything else assumes the shared shell, `docs/marketing/`
doc-sync, data layer (`runs` / `approvals` / `assets` / `metrics_cache`), design system, and the
`tools/*.mjs` + `CONFIRM=1` convention already exist. Don't start a tool session until Foundation is
merged, or the tool session will reinvent the plumbing and drift.

## Dependency map

```
                        ┌─────────────────────────────┐
                        │  01 FOUNDATION (shell,       │
                        │  doc-sync, data layer,       │  ← build first, blocks all
                        │  design system, tools/*.mjs) │
                        └──────────────┬──────────────┘
                                       │
        ┌──────────────┬───────────────┼───────────────┬──────────────┐
        ▼              ▼               ▼               ▼              ▼
   03 STUDIO       07 SEO         02 META ADS      (Google Ads     06 NEWSLETTER
   (image/video)   (keyword/      (insights +       module,        (Shopify Email)
        │           content)       drafting)        already          ▲   ▲   ▲
        │              │              ▲             scaffolded)      │   │   │
        ▼              │              │                              │   │   │
   04 CONFIG           │              │  creative from ───────┐      │   │   │
   ASSET CREATOR       │              │  03 / 04              │      │   │   │
   (config → assets)   │              │                        │     │   │   │
        │              │              │                        │     │   │   │
        └──────┬───────┴──────────────┴────────────────────────┘     │   │   │
               ▼                                                      │   │   │
          05 SOCIAL ORGANISER  ────────────────────────────────────┘   │   │
          (calendar + pipeline) ──── top posts feed newsletter ─────────┘   │
                    ▲                                                        │
                    └──── consumes assets from 03 & 04 ─────────────────────┘
   07 SEO ──── drafts/briefs feed 05 (social) and 06 (newsletter) ──────────┘
```

**Read the arrows as "produces input for":** Studio (03) and Config Assets (04) produce media the
Social (05), Meta (02), and Newsletter (06) modules consume. SEO (07) produces content that Social and
Newsletter distribute. None of these are *hard* build blockers — each tool ships its MVP standalone —
but building an upstream tool first means the downstream one has real inputs to wire against instead of
stubs.

## Hard vs. soft dependencies

| Tool | Hard deps (must exist) | Soft deps (nicer if built first) |
|---|---|---|
| 01 Foundation | — | — |
| 02 Meta Ads | 01 | 03/04 (for creative to attach) |
| 03 Studio | 01 (render pipeline ported) | — |
| 04 Config Assets | 01, **03's render pipeline** | — |
| 05 Social | 01 | 03 + 04 (assets to post), 07 (content) |
| 06 Newsletter | 01 | 03/04 (images), 05 (top posts), 07 (articles) |
| 07 SEO | 01 | — |

Only genuinely hard chain: **01 → 03 → 04** (Config Assets reuses Studio's render pipeline). Everything
else can be built with stubbed inputs and back-filled.

## Recommended sequence (value-first)

Ordered to get something usable fast and to build upstream producers before downstream consumers:

1. **01 Foundation** — unblocks everything. _(blocking)_
2. **03 Studio** — the asset engine; the most-reused producer. Also proves the anti-slop/Gate-1 flow.
3. **07 SEO** — independent, high-leverage, turns the finished keyword plan into a live pipeline. Can
   run in parallel with 03 (no shared code).
4. **05 Social Organiser** — the operating loop; now has Studio assets to post. The daily-driver UI.
5. **02 Meta Ads** — insights first (read-only, low risk), then approved drafting; can attach Studio
   creative. Pairs with the existing Google Ads module.
6. **04 Config Assets** — builds on Studio; turns real configurations into assets that feed 05/02.
7. **06 Newsletter** — last: it's the aggregator, best once 03/04/05/07 are producing content to pull.

**If you want to parallelise across sessions:** after Foundation merges, run **03 + 07** at the same
time (no overlap). Then **05 + 02**. Keep **04** after 03, and **06** last.

**If you want fastest single win instead:** 01 → 07 (SEO). It's fully independent, needs no media
pipeline, and turns work you've already done (`keyword-plan.md`) into a live dashboard.

## Cross-session guardrails (so parallel builds don't collide)

- **Shared code is owned by Foundation.** Tool sessions extend the shell/data layer/UI primitives; they
  don't rewrite them. If a tool needs a new shared primitive, add it in the shared location, not inside
  the module.
- **One branch per tool**, each off the merged Foundation branch. Merge Foundation before branching a
  tool, or rebase the tool onto it before merging.
- **Data-layer migrations are additive.** Each tool adds its own tables (`meta_*`, `social_*`,
  `seo_*`, `newsletter_*`); no tool alters another's schema.
- **`tools/*.mjs` naming is stable:** `meta-ads.mjs`, `studio.mjs`, `config-assets.mjs`, `social.mjs`,
  `newsletter.mjs`, `seo.mjs`. Reuse, don't duplicate (e.g. Config Assets imports Studio's render core).
- **`docs/marketing/APP-NOTES.md` is the shared truth.** Every session reads it first and appends what
  it learns (stack quirks, env var names, where configs/list live) so the next session starts ahead.

## Blockers to clear before the relevant session (from the per-tool Open Questions)

| Blocks | Decision needed | Default if undecided |
|---|---|---|
| 02 Meta Ads (purchase-optimised spend) | Meta Pixel/CAPI verified on site? | Insights + lead-gen only until verified |
| 04 Config Assets | Scope confirm; where configs live; permission to use customer jobs | Start Radius Pro, anonymised, spec-only |
| 05 Social | LinkedIn API vs. manual; Later manual vs. API scheduler | IG end-to-end; FB/LinkedIn stubbed |
| 06 Newsletter | Shopify Email API send vs. manual click; where the list lives | Draft + test-send; hand final send to admin |
| 07 SEO | Google Search Console now or later | Defer GSC; use plan + Perplexity/Firecrawl |

None of these block **starting** their session — each has a safe default — but deciding them upfront
avoids a mid-build stall.
