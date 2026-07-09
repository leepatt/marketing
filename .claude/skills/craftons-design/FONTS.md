# Craftons fonts — how every document gets the real brand type

Web artifacts + the render pipeline can't reliably pull fonts from Drive at build time, so the
brand web fonts are packaged here as a **self-contained stylesheet** any asset reuses.

## `craftons-fonts.css`
Real **Inter** (400/500/600/700, Latin), embedded as `woff2` data-URIs — no network, no Drive
fetch. Inter is the brand **body** face *and* what the live craftons.com.au theme actually ships
(the site self-hosts Inter; Aeonik is not deployed there). Inter is OFL-licensed, so it's safe to
embed and commit.

**Use it:**
- HTML artifact → paste the file's contents inside your `<style>` (CSP blocks external CSS), then
  `--font-body / --font-display: "Inter", …`.
- Pipeline render (`pipeline/`) → `@import "../.claude/skills/craftons-design/craftons-fonts.css";`
  or copy it next to the template.

## Aeonik (display) — pending
The brand guidelines call for **Aeonik** on display/headlines. Aeonik is a **licensed** font
(`.otf` in Drive `fonts/`), and web-embedding it needs a **webfont licence** — it is not deployed
on the live site. Options: keep web docs on Inter (matches the live site) and use Aeonik only in
**PDF exports** (desktop-licence-clean via the pipeline); or, with a webfont licence, add Aeonik
`@font-face` blocks here too. Decision pending with Lee.
