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

## 🟡 Build the production pipeline (B9 + compositing)
- [ ] **Scaffold the media tooling** as a setup script on the Jake cloud environment:
      `ffmpeg`, `sharp`, `ImageMagick`, SVG tooling (librsvg), **Playwright** (headless render),
      and install the **Aeonik brand fonts** so text renders correctly.
- [ ] Wire the **HTML/CSS → image** render pipeline using `craftons-design` tokens (true brand colours/type).
- [ ] Build the **social/illustration style layer** on top of the locked brand foundation
      (line style, colour treatment, references — the "anti-slop" rules) for mass illustration output.

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
