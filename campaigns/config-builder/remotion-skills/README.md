# Remotion Agent Skills (downloaded 2026-07-12)

The official Remotion agent skills, saved here for the content-engine build. Source:
https://www.remotion.dev/docs/ai/skills · repo `github.com/remotion-dev/skills`.

## The 8 skills
| Skill | What it covers |
|-------|----------------|
| `remotion-best-practices` | Umbrella — use when unsure which specific skill applies |
| `remotion-create` | Starting new projects / compositions (incl. Tailwind, video layout) |
| `remotion-markup` | Compositions, animations, layout, typography, media, effects, maps, audio, fonts, timing, transitions |
| `remotion-render` | Rendering video/stills (incl. transparent videos) |
| `remotion-captions` | Subtitles/captions (import SRT, transcribe, display) |
| `remotion-saas` | Architecture for Remotion-powered apps + product integrations (player, framework, rendering) |
| `remotion-interactivity` | Editable elements in Remotion Studio |
| `mediabunny` | Browser-based multimedia — video/audio metadata (dimensions, duration) |

## Install (into the repo that builds the content engine, e.g. cnccut-app)
```bash
npx skills add remotion-dev/skills   # installs to ./.agents/skills + symlinks into ./.claude/skills
```
Each skill is a folder with a `SKILL.md` plus supporting `.md` references. To use in Claude Code, they must be
under `.claude/skills/` in the target repo (the installer symlinks them; this saved copy is the raw files).

## Why we have these
The content engine's compositing/render layer is **Remotion** (see `../CONTENT-ENGINE-SPEC.md`). These skills
teach an agent to author Remotion video code — the stage that adds the synthetic cursor/auto-zoom, captions,
real-footage compositing, and audio on top of the real-app capture. Copy them into the build repo when we start.
