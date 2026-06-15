# Desktop to-do — pick up here

_Created 2026-06-15 from a mobile session. Everything below is saved + pushed; nothing is blocked._

## 🔴 Do first — security
- [ ] **Rotate the Google Ads credentials** (client secret + refresh token appeared in a setup screenshot).
  1. [myaccount.google.com/permissions](https://myaccount.google.com/permissions) → "Craftons Ads" → **Remove access**.
  2. Google Cloud Console → **Clients → craftons-ads-client → Reset secret**.
  3. Re-run the OAuth Playground (offline + force-consent) → new refresh token.
  4. Update the 2 values in **both** places: cnccut-app `.env` **and** the Jake cloud environment.

## 🟠 Finish the design-system wiring
- [ ] **Paste `colors_and_type.css` into the repo** for an in-repo token copy.
      Open `G:\…\00 Brain\Design-system\colors_and_type.css`, copy the plain text, paste to Claude →
      it commits to `.claude/skills/craftons-design/`. (Until then the Drive copy is canonical and fetched on demand.)
- [ ] (Optional) Same for the small text extras if wanted: `_ds_manifest.json`, `_adherence.oxlintrc.json`,
      and the `ui_kits/web/` HTML/CSS/JS. Fonts/PNGs/PDF stay in Drive.

## 🟡 Production pipeline (B9 + compositing)
- [x] **Pipeline built + working** → `pipeline/` (HTML/CSS template → PNG via Playwright + sharp).
      Proven render: `post-hero-1080x1350` IG portrait. `npm run render`.
- [ ] **Add the media tooling setup script to the Jake cloud environment** — paste
      `pipeline/setup-media-tooling.sh` body into the env's *Setup script* field (so mobile sessions have ffmpeg/Playwright cached).
- [ ] **Swap interim `pipeline/tokens.css` for the canonical `colors_and_type.css`** (from Drive) + drop
      **Aeonik `.otf`s** into `pipeline/fonts/` so headlines render in the real face (currently a fallback).
- [ ] **Pull the real curve-motif PNG + logo** from Drive `assets/` (template uses an SVG placeholder).
- [ ] **More templates:** carousel slides, quote/testimonial card, compliance block, story 1080×1920.
- [ ] **Video:** ffmpeg assembly of Tia's footage → Reels export.
- [ ] **Social/illustration style layer** (anti-slop rules) feeding AI gen (Replicate/Glif).

## ✅ Verify
- [ ] Confirm the cnccut-app `.env` loads all 12 keys (quick check from inside the repo).
- [ ] Confirm a new session reads the keys from the Jake cloud environment.

## 🅿️ Parked decisions (yours to make, not blocking)
- [ ] Ad budget $ + per-platform split.
- [ ] LinkedIn activation timing (founder-led).
- [ ] Whether/when to add TikTok + YouTube.
- [ ] A5 — sync the Drive-side `CLAUDE.md` system map (was pending desktop).

---

### Done this session (for reference)
- 12 API keys collected → cnccut-app `.env` + Jake cloud environment.
- Decisions: Later = manual (no API); email = Shopify Email (not Klaviyo).
- `craftons-design` skill installed in the marketing repo (rules in-repo; exact tokens/assets canonical in Drive).
- `SETUP.md` / `INTEGRATIONS.md` updated (B1–B8).
