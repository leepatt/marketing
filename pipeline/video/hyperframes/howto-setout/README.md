# How-To Series: "The set-out numbers" — HyperFrames composition

The first Craftons video made entirely in a session with **HyperFrames by HeyGen** (an open-source
HTML/CSS/GSAP → MP4 renderer; the "HyperFrames" connector in Claude is the hosted front-end for it).
9:16 · 1080×1920 · 30 fps · 29 s · silent-safe. Brief, beat sheet, caption and open decisions:
`briefs/howto-setout-numbers-video-brief.md`.

## Files

| File | What |
|---|---|
| `index.html` | The whole video: three timed scenes, the plan-view drawing (generated from `JOB = {R:3714, W:90, deg:30}`), the curved-line motif, and the GSAP timeline. Change the numbers in `JOB` and every label, dimension and count-up follows. |
| `tokens-root.css` | The `:root` block of the canonical `colors_and_type.css` from the Drive design system (file id `1KMBH74vo-tSqim_7WnI9dFaee3aWuo9M`). Only `var(--token)` colours are used. |
| `fonts/` | Self-hosted webfonts: Inter 400/500/600 + JetBrains Mono 500 (open licence, committed). **Aeonik-Medium.otf is licensed and git-ignored** — pull it from Drive `00 Brain/Design-system/fonts/` (file id `1udF8_o2UOmnOi5lhi1PDQxDYYRjesIQv`) into `fonts/` before rendering. `render.sh` writes `fonts/aeonik.css` (also ignored) declaring it when present; without it the display face falls back to Inter and the check still passes. |
| `vendor/gsap.min.js` | GSAP 3.14.2, vendored so renders never touch the network. |
| `render.sh` | One-shot local render (installs the pinned CLI + static FFmpeg/FFprobe on first run). `./render.sh check` runs the lint/runtime/layout/contrast gate; `./render.sh snapshot` writes QA frames. |
| `hyperframes.json`, `meta.json`, `package.json` | HyperFrames project scaffolding (`hyperframes init --example blank --resolution portrait`). |

## Rendering (local, no account needed)

```bash
cd pipeline/video/hyperframes/howto-setout
./render.sh check        # must be 0 errors before rendering
./render.sh              # → out/craftons-howto-setout.mp4
```

Needs Node 22+. Chrome/FFmpeg/FFprobe are auto-resolved: in the Claude web sandbox Chrome is
Playwright's bundle at `/opt/pw-browsers/`, and FFmpeg/FFprobe come from the `@ffmpeg-installer` /
`@ffprobe-installer` npm packages (Playwright's own ffmpeg is a stripped build with no H.264, which is
why the CLI's default fails there). Google Fonts are unreachable from headless Chrome in the sandbox,
hence the self-hosted `fonts/`. A 29 s render takes about 3 minutes on 4 cores.

## The HyperFrames MCP connector (optional)

Installed on the session but **needs a one-time HeyGen sign-in**: claude.ai → Settings → Connectors →
HyperFrames by HeyGen → authorise. It renders on HeyGen's cloud and returns hosted preview links, which is
handy for phone review, but everything in this folder renders locally without it. Authorise it only if
hosted links / cloud renders are wanted.

## Editing rules of thumb

- Timing lives in the `tl.*(…, atSeconds)` calls at the bottom of `index.html`; scenes are the three
  `<section class="clip">` elements with `data-start` / `data-duration`.
- Keep copy inside the guardrails in the brief (Radius Pro banned words, no delivery-day number, no
  "send us your plan", soft CTA only, no emoji, no em dashes).
- Run `./render.sh check` after every edit. Contrast is checked against WCAG AA automatically.
- Nothing auto-publishes: render → Lee reviews the MP4 on the phone → save to Drive
  `Marketing/Video/How-To-Series/` → post via Later.
