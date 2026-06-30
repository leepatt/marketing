# tools — inspiration collection

Reusable tools for building the Craftons image-gen **reference library** from
other brands' content. Reference/mood use only (third-party content), feeding
prompts for the `craftons-design` skill — not republished.

## The loop

```
ig-collect.mjs   →  raw images + videos   →  video-frames.py  →  deduped frames
(desktop, logged in)        │                                          │
                            └──────────── upload to Drive 01 Inspiration/<handle>/ ─┘
```

## 1. `ig-collect.mjs` — pull a profile's media (run on your DESKTOP)

The cloud session can't reach Instagram (network policy + IG blocks
headless/datacenter traffic). Run this on your own machine, logged into IG.

```bash
cd tools
npm install                       # one-time
npx playwright install chromium   # one-time

node ig-collect.mjs login         # one-time: log in, saves tools/.ig-session.json (git-ignored)
node ig-collect.mjs modernconcreteco --max 60
```

Options: `--out DIR`, `--max N`, `--headful` (show the browser if IG throws a
challenge). Output lands in `<out>/<handle>/raw/` plus a `manifest.json`.

**Default output → Google Drive.** `--out` defaults to the desktop `G:` mount of
the brain's `01 Inspiration` folder, so downloads sync straight into Drive with
no copy step. To change it without editing code (e.g. a Mac Drive path), set the
`IG_COLLECT_OUT` env var; `--out` still overrides per-run.

It downloads the real media bytes by capturing network responses (reliable for
IG's blob/streamed video), keeps the largest copy of each photo, and is
rate-limited between posts. If discovery returns 0 posts, IG changed its markup
— update the `POST_LINK` selector in the script.

### Run it autonomously (Windows desktop)

To have fresh inspiration land in Drive on a schedule with no one watching:

```bat
REM one-time, after login is set up:
install-schedule.cmd          REM registers a weekly task (Mondays 09:07)
```

- `ig-collect.bat [handle] [maxPosts]` is the wrapper the task runs (handle
  defaults to `modernconcreteco`); it logs to `tools/ig-collect.log` (git-ignored).
- `install-schedule.cmd` registers a Windows Task Scheduler job that runs the
  wrapper weekly. Re-run to change it; remove with
  `schtasks /Delete /TN "Craftons IG Inspiration" /F`.
- **Limits of "autonomous":** the PC must be on/awake at the scheduled time;
  IG sessions expire every few weeks (re-run `node ig-collect.mjs login`, ~30s);
  keep the cadence weekly so IG doesn't flag the account. It can't run in the
  cloud — IG blocks datacenter/headless traffic.

(On macOS the same `ig-collect.mjs` runs under `cron`/`launchd` instead — ask
Claude Code on the desktop to set that up.)

## 2. `video-frames.py` — videos → deduped reference frames

```bash
python3 video-frames.py collected/modernconcreteco/raw -o collected/modernconcreteco/frames
```

One frame every 0.5s, near-duplicates dropped via perceptual hash. (Deps are
auto-installed by the SessionStart hook in cloud sessions; on desktop:
`pip install Pillow imagehash imageio-ffmpeg` and have ffmpeg available.)

## 3. Into the library

Upload `collected/<handle>/` to Drive `01 Inspiration/<handle>/`. Then a teardown
(reuse `inspiration/brand-teardown-template.md`) turns the frames into reusable
prompt fragments for `craftons-design`.
