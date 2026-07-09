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

## Aeonik (display) — DECIDED: not used for web docs
**Decision (Lee, 2026-07-08): Inter everywhere**, matching the live site. Produced digital documents
standardise on **Inter for both body and headlines**. The guidelines PDF still lists Aeonik as the
display face, but the live craftons.com.au theme ships Inter, Aeonik is a **licensed** font not
deployed on the web, and we're keeping one consistent, licence-clean brand type. Don't re-open this
per document. (If a true-to-guidelines Aeonik piece is ever needed, render it as a **PDF** via the
pipeline using the Drive `.otf` — desktop-licence-clean — rather than embedding Aeonik on the web.)
