# brand/ — brand memory for the marketing skill suite

This folder is the **brand memory** the marketing skills read on every run
(`keyword-research`, `seo-content`, `positioning-angles`, `direct-response-copy`,
`content-atomizer`). It mirrors/distills our canonical docs so the skills auto-load
Craftons context instead of asking each time.

## Canonical sources (edit these first, then mirror here)
- `../BRAND.md` (in `.claude/skills/craftons-design/`) — brand + visual voice
- `../SOCIAL-VOICE.md` — the caption/online voice → `voice-profile.md`
- `../CONTENT-PILLARS.md` — the content model
- `../inspiration/SWIPE-FILE.md` — brand teardowns → `competitors.md`

## Files here
| File | Feeds | Source |
|------|-------|--------|
| `voice-profile.md` | tone of all copy/content | SOCIAL-VOICE.md + BRAND.md |
| `audience.md` | who we write for, depth, language | this project |
| `competitors.md` | positioning + SERP seeds | SWIPE-FILE.md + building competitors |
| `positioning.md` | *(written by `positioning-angles`)* | — |
| `keyword-plan.md` | *(written by `keyword-research`)* | — |
| `assets.md` / `learnings.md` | content registry + performance | appended by skills |

> Note: the skill suite also references `_system/` and `references/` folders that aren't
> installed — the skills degrade gracefully without them.
