# Brief 06 — Newsletter Generator

_Depends on Brief 01. Sends via Shopify Email (decided). Consumes assets from Briefs 03/04/05/07._

---

## 1. Goal

A tool that drafts the **fortnightly Craftons newsletter** — copy + layout + images — in brand voice,
assembled from recent content (social wins, new configs, SEO/blog pieces, product news), and sends it
via **Shopify Email** to the list built off the calculator lead magnet. Claude drafts; Lee approves;
then it sends.

## 2. Why it exists

The newsletter is the owned-audience channel (Phase 3). Email platform is **decided: Shopify Email** —
already connected, free for the first 10k sends/mo, same admin as store/customer data. We just need a
repeatable draft→approve→send loop that reuses everything the cockpit already produces instead of
writing each issue from scratch.

## 3. Users & control model

Internal. **Draft → human approval → send.** A send is the highest-stakes outward action here:
`CONFIRM=1` + explicit UI approval, and a mandatory **test-send to self** before the real send. Never
send to the list without Lee approving the final rendered email.

## 4. Inputs

**Synced brand docs (`docs/marketing/`):**
- `brand/voice-profile.md`, `craftons-design/BRAND.md` — email voice + visual system (note: brand tone,
  not the punchy social caption tone; but still builder-to-builder, no jargon, no emoji).
- `.claude/skills/direct-response-copy/SKILL.md`, `.claude/skills/seo-content/SKILL.md` — subject
  lines, structure, CTAs.
- `CONTENT-PILLARS.md` — themes; recurring sections mapped to pillars.

**Live data / sources:**
- **Shopify** (connected) — the **customer/email list** + product data + **Shopify Email** send.
  Reads via the Shopify MCP/Admin API; sends via Shopify Email (Marketing → Campaigns). Env: existing
  Shopify connection (no new key). `KLAVIYO_API_KEY` only if we ever switch back.
- **Cockpit content:** top social posts (Brief 05), new config assets (Brief 04), new SEO/blog pieces
  (Brief 07), new products — the newsletter auto-suggests an issue from these.

## 5. MVP vertical slice

**Assemble a draft issue → render an on-brand email → approve → test-send via Shopify Email.**

1. Newsletter page: "New issue" pulls candidate items (recent approved assets, top posts, new
   products/configs, latest blog) into a suggested outline.
2. `tools/newsletter.mjs draft --issue <date>` generates: subject line variants, preview text,
   sections (hero + 2–3 blocks + soft CTA) in brand voice, with images from the asset library.
3. Render to an **email-safe HTML** layout (Shopify Email-compatible: inline styles, table layout,
   brand tokens) + a plain-text fallback. Gate 1 brand-check.
4. Approval drawer (preview the rendered email) → approve → **test-send to self** via Shopify Email →
   then a `CONFIRM=1` real send to the list (or hand the built campaign to Shopify admin for the final
   click, whichever the Shopify Email API supports).
5. Record the issue + send in `runs`; pull open/click stats back afterward if available.

## 6. Backend — `tools/newsletter.mjs`

- `suggest --issue <date>` — gather candidate content into an outline (read-only).
- `draft --issue <date>` — generate copy + assemble sections + render email HTML.
- `test-send --to <email>` — send a test via Shopify Email (`CONFIRM=1`).
- `send --issue <date>` — real send to the list; requires `CONFIRM=1` + prior approval + a completed
  test-send. (If the Shopify Email API doesn't allow programmatic list-send, this step *builds* the
  campaign in Shopify and leaves the final send button to a human — document which path applies.)

## 7. Frontend — Newsletter page

- Issue builder: suggested outline + drag/reorder sections + per-section copy/image edit.
- Subject-line A/B options; preview text.
- Rendered email preview (desktop + mobile) + Gate 1 flags.
- Approval drawer; Test-send; Send (guarded). Past issues list with open/click stats.

## 8. Data model additions

`newsletter_issues` (date, subject options, sections json, status, sent_at, shopify_campaign_id,
stats). Reuse `assets`, `approvals`, `runs`.

## 9. Post-MVP backlog

- Automated cadence reminder (every 2 weeks) → pre-drafted issue awaiting approval.
- Segment sends off Shopify customer data (buyers vs. lead-magnet subscribers) — note Shopify Email's
  weak automation; revisit Klaviyo only if lifecycle flows are needed.
- Reuse winning newsletter blocks → social (content-atomizer) and vice-versa.
- Lead-magnet/calculator signup → list growth tracking on the Overview.

## 10. Guardrails, safety

A real send is irreversible — mandatory approval + test-send + `CONFIRM=1`. Verify unsubscribe/compliance
footer is present. Confirm list source/consent (lead-magnet opt-ins). No emoji; brand voice.

## 11. MVP acceptance criteria

- [ ] "New issue" assembles a suggested outline from real recent cockpit content + Shopify products.
- [ ] A full draft renders as an on-brand, email-safe HTML preview (desktop + mobile) with Gate 1.
- [ ] Approve → **test-send to self via Shopify Email** succeeds.
- [ ] Real send is blocked without approval + test-send + `CONFIRM=1`.

## 12. Open questions

- Does the **Shopify Email API/MCP** support programmatic campaign create + send, or must the final
  send be a human click in Shopify admin? (Determines whether `send` fully automates or hands off.)
- Where does the newsletter **list** currently live — Shopify customers with a marketing-consent tag,
  or a separate lead-magnet list? Is the calculator lead magnet live yet?
- Confirmed fortnightly cadence + a default section structure?

---

## Kickoff prompt (paste into a fresh cnccut.app session)

> Build the **Newsletter Generator module** following brief `06-newsletter-generator.md` and the
> shared conventions in `01-foundation-cockpit-shell.md`. Foundation shell + `docs/marketing/` should
> exist. Email platform is **Shopify Email** (already connected — no new key). First confirm whether the
> Shopify Email API/MCP supports programmatic campaign create+send or requires a human click, and note
> it in `docs/marketing/APP-NOTES.md`. Ship the MVP on `/marketing/newsletter`: a `tools/newsletter.mjs`
> that assembles a suggested issue from recent approved assets/posts/products, drafts subject +
> sections in brand voice, renders an **email-safe HTML** preview (desktop + mobile) with a Gate-1
> brand-check, goes through the shared Approval drawer, and does a **test-send to self** via Shopify
> Email. Block the real list-send behind approval + test-send + `CONFIRM=1` (or hand off to Shopify
> admin if the API can't send). No emoji; brand voice, not social-caption tone. New branch, logical
> commits.
