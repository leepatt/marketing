# Craftons motion graphics (Remotion)

Brand overlays rendered from code, dropped into CapCut as clips. **Code generates the asset;
CapCut does the edit.** This does not replace the CapCut bridge — it feeds it.

> ✅ **Verified working.** Every composition here was rendered and visually checked.

## Compositions

| ID | What | Output |
|---|---|---|
| `SpecStamp` | **The signature move.** Real job specs on real footage — `R900 · 2400mm · 17mm formply` | transparent .mov |
| `LowerThird` | Customer name + trade | transparent .mov |
| `TitleCard` | Section marker. Number it only if it's genuinely a sequence | transparent .mov |
| `Endcard` | 1.5s sign-off, curved-line motif, soft CTA | opaque .mp4 |

## Render

```bash
npm install
npm run spec        # renders with alpha
npm run endcard
npm run studio      # live preview in a browser
```

**Real job numbers, via props:**

```bash
npx remotion render SpecStamp out/job-1450.mov \
  --codec=prores --prores-profile=4444 --pixel-format=yuva444p10le \
  --props='{"radius":"R1450","specs":["3600mm","19mm bendy ply"],"label":"SET OUT"}'
```

Then drop the `.mov` onto a track above your footage in CapCut. Transparency is preserved.

## Two things that will bite you

**`--pixel-format=yuva444p10le` is required for transparency.** Without it, `--prores-profile=4444`
still renders `yuv422p12le` — no alpha — and the overlay composites as a **solid black box**. The
npm scripts already include it; if you write a render command by hand, don't drop it.

**Fonts are bundled in `public/fonts`, not fetched.** Declaring a font-family isn't enough in
Remotion — it silently falls back to a generic and the render looks nothing like the brand. `fonts.ts`
loads the files and blocks the render until they're ready. **Always set an explicit `fontWeight`**
that matches a loaded file (700 or 900 for condensed), or the browser mixes faces mid-word.

## Files

| File | |
|---|---|
| `src/brand.ts` | Colours, canvas, the 2026 safe zone |
| `src/fonts.ts` | Local font loading + render blocking |
| `src/SpecStamp.tsx` etc. | The compositions |
| `src/Root.tsx` | Registry + default props |
| `public/fonts/` | Bundled woff2 — Big Shoulders Display, JetBrains Mono, Inter |
