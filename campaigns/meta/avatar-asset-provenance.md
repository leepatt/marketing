# Meta ad presenter — where the source file lives

_Search run 2026-08-07, chasing the uncropped high-res original of the presenter
shown in `story-realheader.mp4` (bearded man, black puffer vest over tan work shirt,
standing in an unfinished interior)._

## What was searched

| Location | Result |
|---|---|
| `leepatt/marketing` (this repo, all branches + history) | No media files at all — docs only |
| `leepatt/cnccut-app` (cloned, `21011e3`) | Full asset inventory below; no match |
| Google Drive — full-account search by title, mime type, date, owner, `fullText` | One strong candidate (below) |
| HyperFrames / HeyGen connector (`list_projects`) | Zero projects — the video was not rendered there |
| Drive search for `story-realheader.mp4` itself | Not present anywhere |

`story-realheader.mp4` is not stored in either repo, in Drive, or in HeyGen. The
screenshot's viewer chrome is the Claude app's file preview, so the composite was
almost certainly assembled inside a Claude session and never checked in.

## Ruled out — `tradie-portrait.png`

The only human still that ships in the codebase:

- `cnccut-app/content-engine/public/real/tradie-portrait.png`
- `cnccut-app/content-engine/sandbox/real/tradie-portrait.png`
- Drive mirror: `photo-tradie-portrait.png` (Craftons brand asset folder)

All three are byte-identical (1,905,515 B) at **819 × 1013**. It is a *different*
person — clean-shaven-ish, grey cap, grey polo, arms folded, outdoors against a
wrapped/battened facade. Not the presenter in the ad.

It is also already flagged ⛔ in `session-findings-2026-08-03b.md`: AI-generated
stock face, excluded from paid under §4.2 of the bible. Referenced by
`content-engine/remotion/HybridReel.tsx:26`.

## Strongest candidate — `CRAFTONS CRAIG AT HOME.png`

- Drive: `Peninsula Studio/01 Craftons/Marketing/03 Content/produced/`
- https://drive.google.com/file/d/1fzdZyL-LdaycEB1k5HMlDghrKcrX06jm/view
- 6,429,719 B PNG · created 2026-07-02 by Lee

A *named* Craftons character ("Craig"), an interior "at home" scene, and a file
large enough to be the uncropped master. Not visually confirmed from a headless
session — the Drive connector returns no preview for images and the file is too
large to pull into a session context. **Open it and confirm.**

## Fallbacks if Craig is not the one

Earlier presenter/portrait generation lives in the AI Studio prompt files in Drive
folder `18o4BGfurnJ-v8FpTC5lYKuQwszSTcKBh`. Each one embeds its generated frames at
full resolution:

| File | Size | Created |
|---|---|---|
| `Craftons Avatar in Modern Office` | 13.8 MB | 2025-09-09 |
| `Approachable Confident Male Studio Portrait` | 2.2 MB | 2025-08-30 |
| `Approachable Confident Male Portrait` | 2.3 MB | 2025-08-30 |
| `Tradies and Radius Pro` | 9.6 MB | 2025-09-05 |

Standalone outputs in the same folder: `Generated Image August 31, 2025 - 6_08AM.jpeg`,
`Generated Image September 05, 2025 - 10_38AM.jpeg`,
`Generated Image September 19, 2025 - 1_07PM.png`.

## Standing gap this exposes

There is no single home for presenter/avatar masters. Candidates are spread across
`03 Content/produced/`, the AI Studio prompt folder, and the app repo's
`content-engine/…/real/`. Per §4.2 open question 9 (pick one avatar + voice and lock
it), the locked presenter master should land in one named Drive folder with the
prompt/seed recorded beside it, so the next crop request is a one-step lookup.
