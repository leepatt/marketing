# Curved Wall Frame Image — session record (2026-07-22)

Working log for the AD4/AD5 Radius Pro "frame-stage" hero image. Source of truth for the build
detail is `CURVEDWALLBUILDSPEC.md` (same folder). This file records what we actually did this
session so we never re-derive the approach, the prompt, or the settings again.

> Media (the reference photo + generated frames) lives in the Google Drive brain, NOT in this repo
> (`.gitignore` excludes `*.png/*.jpg/*.jpeg`). This doc is the durable record; images are archived
> in Drive.

## Goal

One accurate **frame-stage** image of the `IMG_5539` curved feature wall — same camera position and
viewpoint as the finished photo, shown as bare timber frame on a concrete slab, zero finished work.
(The finished→frame reveal pair is deferred per the spec.)

## Winning method (do this again)

**Image-to-image / reference-conditioned**, deriving from `IMG_5539` so the shape + viewpoint are
locked from the photo, with the build detail driven by the prompt. Text-to-image alone gets the
curve wrong (logged in the spec's failure list) — always condition on the reference file.

- **Model:** `google/nano-banana-pro` on Replicate (Nano Banana Pro / Gemini image).
- **Key inputs:** `image_input: [IMG_5539]`, `aspect_ratio: "match_input_image"` (locks the portrait
  viewpoint), `resolution: "2K"`, `output_format: "png"`, `safety_filter_level: "block_only_high"`.
- **Token:** `REPLICATE_API_TOKEN` is live in the web-session env. Script: `scratchpad/gen_frame.py`
  (run `python3 gen_frame.py 3` for 3 variants). ~30–50s per generation.
- Run 3× on the identical locked prompt; run-to-run variance gives the spread to choose from.

## Creative decisions locked this session (the finished photo hides all of this)

1. **Behind/through the frame:** more raw stud framing + further raw framed openings visible through
   the curve (studs at 125mm are mostly air — you see through).
2. **Overhead:** exposed timber floor joists of the level above (no plasterboard; reads true for this
   flat-ceilinged unit — not pitched roof trusses).
3. **Lighting:** flat, neutral, even site light — NOT the warm sun-pooling of the finished photo.
4. **Scene scope:** whole scene raw-framed; the left doorway becomes a bare stud opening too.

## The locked prompt

See `gen_frame.py` (`PROMPT`). Summary of what it enforces: same camera/perspective/curve; bare
90×35 pine studs plumb at 125mm centres showing the 35mm face; doubled ~34mm black-faced Formply
plates (black faces, ply-grain edges) top + bottom, 90mm wide flush both faces, black bottom plate
on pale concrete; single imperfect mid-height noggin row (~150mm blocks); bare dusty concrete slab;
no plasterboard, exposed floor joists; left doorway a raw stud opening; more framing beyond; no
skirting/architraves/paint/furniture/steel strapping; flat neutral site light; photoreal.

## Results (variants v1/v2/v3)

All three hit the previously-failing hard parts: correct convex curve + viewpoint, bare slab, no
plasterboard, exposed joists, left doorway as raw opening, framing visible beyond, slender studs
(not chunky), single mid noggin row, and a dark plate contrasting on the pale slab (money shot).

- **v2 — recommended.** Clearest "see-through open frame" read (best for the reveal concept),
  slender even studs, strong black bottom plate, believable joists.
- **v3 — premium alt.** Most photoreal, boldest black-plate money shot, best joists; backing behind
  the curve reads slightly solid (a touch less "open frame").
- **v1 — third.** Solid but studs slightly chunkier/less even, plate less pronounced.

**Known residual gap (all variants):** plates read as a solid black band rather than *unmistakably
doubled* (two 17mm sheets = 34mm, black faces + pale ply-grain edges). Refinement target for the
next pass — emphasise the visible lamination line / ply edge on the plate.

## Next steps

- [ ] Lee picks the winning variant.
- [ ] Upload the winner (and archive all three) to the Drive brain; link it here.
- [ ] Optional refinement pass to make the doubled-34mm black-Formply plate unmistakable.
- [ ] Later: decide the finished→frame reveal pair (deferred).
