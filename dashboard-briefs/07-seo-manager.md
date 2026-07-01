# Brief 07 — SEO Manager

_Depends on Brief 01. Feeds content into Briefs 05/06. Complements the Google Ads module._

---

## 1. Goal

An SEO module that manages Craftons' organic search: **tracks** keyword coverage and rankings, **audits**
on-page/technical SEO for the Shopify site, and **generates SEO content briefs + drafts** from the
existing keyword plan — so organic capture grows alongside paid. It turns `brand/keyword-plan.md` and
the `keyword-research`/`seo-content` skills into a living, in-cockpit workflow.

## 2. Why it exists

We already did the keyword research (7 pillars + 6 ad groups, 90-day calendar; confirmed converters
"bendy ply", "curved bench seat"; product = Radius Pro). That plan shouldn't rot in a doc — it should
drive a pipeline: identify gaps → brief → draft → publish → track rank → refresh. Organic is the
compounding, un-rented counterpart to Google/Meta ads.

## 3. Users & control model

Internal. The tool proposes briefs, drafts, and technical fixes; a human approves before anything is
published to the live Shopify site. Content drafts follow the human-in-loop gate; **no auto-publish to
the storefront**.

## 4. Inputs

**Synced brand docs (`docs/marketing/`):**
- `brand/keyword-plan.md` — the 7 pillars + 6 ad groups, paid + SEO split, 90-day calendar, converters.
- `.claude/skills/keyword-research/SKILL.md`, `.claude/skills/seo-content/SKILL.md` — the 6-circles
  method, clustering, SERP-aware content generation, Article + FAQ JSON-LD schema.
- `brand/competitors.md`, `brand/audience.md`, `brand/voice-profile.md` — landscape + who we write for.
- `CONTENT-PILLARS.md` — align SEO topics with content lanes.

**Live data / APIs:**
- **Shopify** (connected) — product/collection pages to audit + optimise (titles, meta, alt text,
  structured data); verified product URLs (Radius Pro `/products/radius-online`, formwork, architraves).
- **Perplexity** (`PERPLEXITY_API_KEY`) — SERP/topic research, People-Also-Ask, competitor content.
- **Firecrawl** (`FIRECRAWL_API_KEY`) — scrape competitor pages/SERPs for gap analysis.
- **(Optional) Google Search Console** — real impressions/clicks/positions. Needs OAuth setup (see
  Open Questions); without it, MVP uses the keyword plan + Perplexity/Firecrawl signals.

## 5. MVP vertical slice

**Keyword plan → a coverage/gap dashboard + one SEO content brief generated end-to-end.**

1. Load `keyword-plan.md` into a **keyword table**: pillar, term, intent, paid/SEO, target URL, status
   (no-page / thin / published / ranking-unknown). Map each term to an existing Shopify page if one
   exists (flag gaps = terms with no page).
2. `tools/seo.mjs audit` checks mapped Shopify pages: title/meta length, H1, missing alt text, JSON-LD
   presence, internal links → a per-page score + fixes.
3. `tools/seo.mjs brief --keyword <term>` generates an SEO content brief (SERP analysis via
   Perplexity/Firecrawl, PAA questions, outline, target word count, entities, internal-link targets,
   Article + FAQ JSON-LD stub) using the `seo-content` skill logic.
4. Brief + optional draft land as an `asset`/document `needs-approval`; Approval drawer; approved
   briefs flow to the writer (or straight to a draft via `seo-content`). Drafts hand off to the
   Newsletter/Social modules for distribution.

## 6. Backend — `tools/seo.mjs`

- `coverage` — reconcile keyword plan vs. live Shopify pages; output gaps + a coverage table (read-only).
- `audit [--url <u>]` — on-page/technical audit of Shopify pages (titles/meta/alt/schema/links).
- `brief --keyword <term>` — SERP-aware content brief (Perplexity + Firecrawl + seo-content logic).
- `draft --brief <id>` — (post-MVP) generate the full article draft + JSON-LD.
- `apply-meta --url <u>` — (post-MVP) push approved title/meta/schema fixes to Shopify; `CONFIRM=1`.
All writes to the live store are `CONFIRM=1` + approval gated.

## 7. Frontend — SEO page

- Keyword table (pillar/intent/URL/status/gap flag) with filters; coverage % per pillar.
- Page audit view: per-URL score + issue list + suggested fixes (approve to apply, post-MVP).
- Brief generator: enter/select a keyword → generated brief preview → approve → hand to writer.
- (With GSC) a rankings/impressions trend panel per keyword/URL.

## 8. Data model additions

`seo_keywords` (term, pillar, intent, channel, target_url, status, position, updated_at),
`seo_audits` (url, score, issues json, checked_at), `seo_briefs` (keyword, brief json, status).
Reuse `assets`, `approvals`, `runs`, `metrics_cache`.

## 9. Post-MVP backlog

- Google Search Console integration → real rankings/CTR/impressions trends + "striking distance"
  (positions 5–15) opportunities.
- Full article drafting (`seo-content`) + JSON-LD + refresh mode (update stale pages on SERP change).
- Push approved on-page fixes (title/meta/alt/schema) to Shopify via Admin API.
- Internal-linking recommender across the storefront; content-decay alerts.
- Merge with Google Ads keyword data (shared terms, paid↔organic cannibalisation view).

## 10. Guardrails, safety

No auto-publish to the live storefront; every content draft + on-page change is human-approved and
`CONFIRM=1`-gated. Content follows brand voice + anti-slop (human-verified, not generic AI filler).
Respect Perplexity/Firecrawl rate limits + costs.

## 11. MVP acceptance criteria

- [ ] `keyword-plan.md` renders as a coverage table mapped to live Shopify pages, with gaps flagged.
- [ ] `audit` scores at least the key product pages with actionable fixes.
- [ ] `brief` generates a real SERP-aware content brief (with PAA + JSON-LD stub) for a target keyword.
- [ ] Brief lands `needs-approval` and can be approved; no writes hit the live store without approval.

## 12. Open questions

- Set up **Google Search Console** access now (real rankings) or defer and use plan + Perplexity/
  Firecrawl signals for the MVP? (GSC needs an OAuth property connection.)
- Should approved on-page fixes push to Shopify automatically (gated), or export for manual application?
- Priority: product/collection page optimisation first, or new blog/pillar content first?

---

## Kickoff prompt (paste into a fresh cnccut.app session)

> Build the **SEO Manager module** following brief `07-seo-manager.md` and the shared conventions in
> `01-foundation-cockpit-shell.md`. Foundation shell + `docs/marketing/` should exist. Ship the MVP on
> `/marketing/seo`: load `docs/marketing/brand/keyword-plan.md` into a **coverage table** mapped to live
> Shopify pages (flag gaps), a `tools/seo.mjs audit` that scores the key product pages
> (title/meta/alt/JSON-LD/links) with fixes, and a `tools/seo.mjs brief --keyword <term>` that produces
> a SERP-aware content brief (Perplexity + Firecrawl + the `seo-content` skill logic, with PAA + Article/
> FAQ JSON-LD stub). Briefs land `needs-approval` via the shared Approval drawer. No writes to the live
> Shopify store without approval + `CONFIRM=1`. Decide with me whether to wire Google Search Console now
> or defer (see Open Questions). New branch, logical commits.
