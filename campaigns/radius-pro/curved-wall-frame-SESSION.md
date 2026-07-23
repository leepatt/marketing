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

## Combine pass — v4/v5/v6 (2026-07-23)

Took the pros from each first-round variant and fed them back in. This is the strongest lever we
have: Nano Banana Pro accepts multiple `image_input` images, so we combined our own attempts.

- **Method:** three inputs — `image_input: [frame_v2.png (base look), IMG_5539 (viewpoint/curve
  ground truth), frame_v3.png (doubled-plate + hangered-joist detail donor)]`, same settings as
  before (2K, match_input_image, block_only_high). Prompt in `scratchpad/gen_frame2.py`.
- **Result:** the doubled 34mm black-Formply plate now reads **unmistakably** (thick black band +
  pale ply-grain edge sweeping around the base on the slab) — the main first-round gap is fixed.
  Kept v2's elegant convex curve + even slender studs, gained v3's realistic exposed joists with
  galv hangers.
- **v5 — new front-runner.** Best balance: elegant curve, clearest doubled black plate money shot,
  hangered joists, and the hero curve still reads OPEN (see-through).
- **v4 — close second.** Same strengths, plate slightly less pronounced.
- **v6 — third.** Beautiful plate + joists, but the curved wall has a solid tan backing (less
  see-through), the one recurring con.
- **Residual nitpick (all):** some grey/tan sheet lining lingers between studs on the flanking
  walls — reads faintly like backing behind the frame. Fixable with a masked inpaint if we want it
  fully open, without disturbing the rest.

## Round 3 — Lee's element sourcing + corrections (v7–v9, 2026-07-23)

Lee reviewed v1–v3 and directed the combine by element, plus three build corrections. Method:
four inputs `image_input: [IMG_5539 (viewpoint), frame_v2 (studs+noggins + clean through-door
wall + open frame + neutral light), frame_v1 (door opening + radius plate & stud-to-plate
connection), frame_v3 (ceiling/upper-floor joist structure)]`. Prompt in `scratchpad/gen_frame3.py`.

Lee's element sourcing: studs+noggins = V2; door opening = V1; radius plate + stud connection =
V1; ceiling/second-floor = V3.

Three corrections (now LOCKED in the spec understanding):
1. **Room through the left doorway:** its right-hand wall is a clean, solid straight stud wall with
   NO door opening (V1/V3 wrongly showed a door; use V2's clean wall).
2. **Second-floor underside = chipboard**, not black: tan particleboard/chipboard flooring sheets as
   the underside of the floor above, between the joists (keep V3's joists + galv hangers).
3. **Plate material split:** the Craftons black-faced Formply doubled ~34mm plate is on the CURVED
   RADIUS ONLY (top AND bottom of the curve). ALL straight top and bottom plates are PINE, not black.

Results: all three corrections achieved in **v8 and v9** (front-runners; v8 slightly cleaner
chipboard + plate, v9 a near-twin with strong hangers). **v7 missed the chipboard** (still dark
voids in the ceiling). Residual across the set: faint grey sheet lining still lingers between studs
on the flanking side walls (reads like wrap/backing) — optional masked-inpaint cleanup.

## Round 4 — targeted edit of v9 (v10–v12, 2026-07-23)

Lee marked up v9 (`IMG_5546.png`) with three edits and "keep everything else the same". Method:
targeted image edit, inputs `image_input: [frame_v9 (clean base to preserve), IMG_5546 (annotated
location guide — red/green markup, told model NOT to render the marks)]`. Prompt in
`scratchpad/gen_frame4.py`. This is the "keep it all, change only X" pattern — feed the clean base
+ an annotated guide, whole-image edit. (For zero drift on unrelated areas, masked inpaint is the
alternative.)

The three edits:
1. **Continuous beam:** a ceiling joist read as broken where it crossed the curve top → made one
   continuous unbroken beam.
2. **Pine straight plates:** the straight-wall top & bottom plates were still rendering BLACK → now
   pine. Black Formply is on the curved radius ONLY (top + bottom). (Refines the round-3 split,
   which had left the right straight wall's plates black.)
3. **Slimmer curve top plate:** the black top plate was too thick/deep vs the bottom → slimmed to
   match.

Results: all three achieved cleanly in v10/v11/v12, no markup bleed. **v10 is the front-runner**
(tall elegant curve best preserved), **v12** a close twin, **v11** slightly more compressed at the
top. Whole-image edit drifts unrelated detail very slightly; composition + all requested elements
held.

## Round 5 — surgical removal of an added timber piece (v16–v18, 2026-07-23)

Lee marked v10 (`IMG_5547.png`, purple) to remove one horizontal timber rail added across the top
of the curve, "keep everything else the same". This is the true zero-drift case → **masked
inpaint**, not a whole-image edit. Full pipeline (scripts in scratchpad):
1. `build_mask.py`: detect the purple marker pixels in the annotated image, restrict to the
   top-right region (kills a window false-positive), morphologically CLOSE into one continuous
   band, upscale to the base resolution. Preview overlay to verify coverage before spending.
2. `crop_prep.py`: crop a tight bbox around the mask (1387×634) — kept under flux-fill-pro's
   ~1440px long-side cap so it is NOT downscaled (the full-frame call had silently shrunk 1696×2528
   → 966×1440, which loses res AND breaks pixel-preservation).
3. `gen_inpaint_crop.py`: flux-fill-pro (`black-forest-labs/flux-fill-pro`) inpaints just the crop,
   3 seeds, full-res.
4. `composite.py`: paste the fill back into the sharp v10 through a feathered mask — masked pixels =
   fill, everything else = exact v10. Verified: pixels outside the crop bbox are byte-identical to
   v10; output is full 1696×2528.

Result: the added rail is gone; studs run up to the black curved top plate with a natural dark gap
and joist hangers behind. **v17 = pick** (v18 near-twin; v16 slightly heavier shadow). Current base
for any further edits: v17.

Tooling note: for "change ONLY this spot", use the crop→flux-fill→composite pipeline (zero drift,
full res). For semantic changes across the frame, use Nano Banana Pro image edit (drifts slightly).

## Round 6 — fix the black-wedge artifact from round 5 (v19–v21, 2026-07-23)

Lee (rightly) flagged a black wedge "in front of the floor joist" in v16. Root cause (diagnosed via
v10↔v16 diff, 77.6k pixels turned near-black, all inside the round-5 strip, nothing else changed):
the round-5 removal mask was too TALL (reached up in front of the ceiling joists) AND its prompt
mentioned "black plate / dark gap" → the fill painted the band black instead of rebuilding joists.

Fix (`wedge_prep.py`, `gen_inpaint_crop2.py`, `composite2.py`): isolate the wedge precisely from the
diff (pixels that changed AND went near-black — this excludes the legit black curved arch plate,
which was black in both), tight-crop, flux-fill with a ceiling-only prompt (NO black words), feather
composite back onto v16. Verified pixels outside the crop are byte-identical to v16; full res.
Result: clean continuous timber joists/bearer + chipboard, no black. **v19 = pick** (v20/v21 leave a
thin dark gap).

LESSON (write into any future removal): keep the mask hugging ONLY the object; never let the fill
prompt mention "black" near a ceiling/joist area, or flux-fill will paint black.

## Round 7 — remove the extra bearer + dangling-hanger row (v25–v31, 2026-07-23)

Lee gave a reference (`IMG_5548`) of how the joist beam should look and flagged an "extra piece":
in v19 the top-right had a thick horizontal bearer with a ROW of ~5 dangling galvanised joist
hangers (structurally nonsense, absent from the reference).

- flux-fill (v22–v24) FAILED here: masking a structural beam mid-ceiling just makes it redraw the
  beam from surrounding context. Inpaint is good at removing *foreground clutter*, bad at removing a
  *structural member* the scene implies.
- Nano Banana Pro semantic edit worked. Gotcha: with a landscape 2nd input image and
  `aspect_ratio:"match_input_image"`, it matched the REFERENCE's landscape aspect and reframed the
  whole shot (v25–v27, junk). Fix: force `aspect_ratio:"2:3"` → v28–v30 kept v19's portrait framing
  and removed the bearer/hanger row cleanly. Whole-frame drift was tiny (~2%, no structural move).
- To honour "keep everything else the same", grafted ONLY the fixed corner from v30 onto the exact
  v19 via the feathered `mask3` band → **v31 = pick** (rest is byte-v19, corner is clean joists).
  v30 = full clean version if a graft seam ever shows.

## Next steps

- [x] R1 (v1–v3) … wedge fix (v19–v21), bearer/hanger removal (v25–v31).
- [ ] Lee confirms v31 as the locked frame.
- [ ] Upload the locked frame (and archive the set) to the Drive brain; link it here.
- [ ] Optional: strip the last grey lining panels on the side walls (fully open framing), if wanted.
- [ ] Later: decide the finished→frame reveal pair (deferred).
