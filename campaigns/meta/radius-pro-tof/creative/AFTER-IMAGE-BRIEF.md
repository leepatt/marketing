# AFTER image brief. The finished curved wall (AD4/AD5 swipe pair)

> 2026-07-23. Drafted for Lee's approval after the BEFORE crops were locked (see
> `CURVED-WALL-CREATIVE-LOG.md`). The AFTER is generated FROM our own real photo
> (`refs/real-frame-A-side-on.jpeg`, full 1320x1760 master), so there is no third-party rights issue
> on this image. Generate full frame first, then apply the LOCKED crop windows from the log so the
> before/after swipe aligns pixel-perfect in both ratios.

## The one-line idea

The exact same camera position as the frame photo, months later: the house is finished and handed
over, and the framed curve is now a fair, crisp white plastered feature wall.

## Locked (not up for interpretation)

- Same viewpoint, same lens feel, same curve geometry and position as the master photo. The convex
  curve joining two straight runs must line up with the frame shot when swiped.
- Full height curve, floor to ceiling. No bulkheads, no half walls.
- Native, not ad-looking: no text, no logos, no people, no staging props that read as a furniture ad.
- Photorealistic. It must read as a phone or real estate photo of a real finished build.

## Creative choices (recommended, Lee to confirm or amend)

- **The curved wall:** smooth set plasterboard, painted crisp white, square set (no cornice reveal
  drama). The curve reads perfectly fair, which is the whole product story.
- **Floor:** pale oak engineered boards, laid straight down the hallway line. (Not herringbone: keeps
  it clearly distinct from the old client inspiration photo and suits a new build.)
- **Ceiling:** flat white plasterboard where the sky currently is, a few recessed downlights, square
  set junction to the curve.
- **Surroundings:** the neighbouring site framing becomes the same home finished. Left of the curve, a
  doorway into a daylit room. Right, the hallway continuing along the straight run. Windows out of
  frame supply the light.
- **Furnishing:** empty, just-completed handover look. No furniture clutter. The curve is the subject.
- **Light:** warm natural afternoon daylight, soft shadows, bright and airy. Same general light
  direction as the site photo so the pair feels like the same place.

## Process

1. flux-kontext-pro on the FULL 1320x1760 master (aspect_ratio match_input_image).
2. Inspect against this brief, iterate the prompt if the curve drifts or anything reads finished-fake.
3. Apply the locked crop windows (4:5: 0,110,1320,1760 and 1:1: 0,160,1320,1480), export 1080x1350
   and 1080x1080.
4. Lee approves the pair. Nothing goes live from this session.

## Status 2026-07-23: v1 and v2 REJECTED. Restarting from a Lee-authored brief

Lee rejected both flux-kontext drafts: the generated curve was a totally different shape from the
framed wall. The model smoothed the real plate line into a generic rounded pod and changed the wall
proportions instead of plastering over the actual frame. **Creative decisions are back with Lee.**
The "Creative choices (recommended)" section below no longer stands; a new brief will be written by
Lee from scratch.

**The new workflow (Lee's):** Lee will annotate the timber frame photo, highlighting the bottom
plate line where the wall junction meets the floor, and the same for the ceiling junction at the
top. The annotated image then drives generation so the model knows exactly where the wall junctions
sit and holds the true geometry. Nothing gets generated until Lee's annotated image and brief are in.

Technical notes kept for the next round: flux-kontext-pro outputs 880x1184 from this master (1080
exports need a 1.23x upscale, run a proper upscaler on the approved final); nano-banana accepts
multiple reference images, so the annotated guide plus the clean frame photo can be fed together.

## Lee's annotated junction guide (2026-07-23, `refs/IMG_5566-markup-junctions.jpeg`, 1080x1350)

The colour legend, from Lee (the geometry authority for the AFTER; do not let the model invent):
- **PURPLE:** the curved wall's top and bottom plates, the HIGH-level wall junctions. Purple top =
  ceiling junction at the higher ceiling, purple bottom = floor junction at the upper floor level.
- **YELLOW:** top and bottom plate lines of the straight corridor run, the LOWER level. Lower floor
  and lower ceiling; a bulkhead (or similar) takes up the ceiling change where purple meets yellow.
- **GREEN:** the step down to the lower level, across the corridor floor.
- **RED box** (left wall): walk-in robe opening. Gets a door, potentially a sliding door.
- **BLUE box** (corridor end): the front door. A nice timber front door.

Process (Lee's): lock the LAYOUT first from this legend, then a second pass on furnishings, soft
furnishings and materials, THEN write the Replicate prompt. Questions to Lee before generating.

## LAYOUT v1 (Lee's answers, 2026-07-23. Workshopping until right, THEN textures)

- **Base photo: the IMG_5566 shot** (the photo under the markup), NOT photo A. Lee: the whole feature
  is the curve, the photo-A crops cut it off, so the photo-A crop windows in
  `CURVED-WALL-CREATIVE-LOG.md` are RETIRED. **Still needed from Lee: the CLEAN unmarked IMG_5566**
  (for the BEFORE slide and as the generation base).
- **Ratio:** the markup is native 4:5 (1080x1350) with the full curve in frame. Run BOTH carousel
  cards at 4:5; DROP the 1:1 square (it cannot hold both curves). Pending Lee's OK.
- **Camera space:** living/dining area, the high-ceiling purple zone. Not really visible in frame;
  the finished foreground treatment is Claude's to propose, Lee approves.
- **The curve:** plastered exactly on the purple junction lines, high ceiling above, upper floor
  level below.
- **The corridor (yellow):** lower level. Floor drops at the green line by TWO RISERS (one step with
  two rises, "maybe just two for now"). Lower ceiling on the yellow top line, with a bulkhead taking
  the height change where purple meets yellow.
- **Corridor right wall + light:** approved direction from the options: timber front door at the end
  (blue box) with a sidelight beside it throwing daylight down the corridor. Confirm exact glazing in
  the next workshop round.
- **Left wall (red box):** the walk-in robe opening, sliding door. Door style and material decided at
  the materials pass.

Open before generation: clean IMG_5566 upload, sidelight confirmation, 1:1-drop confirmation, then
the furnishings/soft-furnishings/materials pass, then the prompt draft for sign-off.

## LAYOUT v2 additions (Lee, 2026-07-23). Layout now closed, style pass next

- Front door: CLOSED. The timber door is the feature, the sidelight does the light work.
- WIR sliding door: CLOSED, flush and calm so nothing competes with the curve.
- Foreground: empty edges, clean floor, no furniture creeping into frame. Any furnishing hints come
  in the furnishings pass under Lee's direction.
- Step: straight across the corridor, full width, two equal risers at the green line.
- Next: the interior STYLE pass. Lee supplying sample/reference images of interiors he likes; feed
  them alongside the geometry refs at generation (nano-banana takes multiple image inputs).

## Base + style refs received (2026-07-23, staged in `refs/`)

- **`IMG_5566-clean-BASE.jpeg` (1080x1350):** the clean unmarked base photo. Native 4:5 with the
  full curve in frame. THE BEFORE SLIDE IS THIS FILE AS-IS, no crop. The AFTER generates from it at
  the same frame. (Supersedes all photo-A crop work.)
- **`style-ref-IMG_5568-ply-interior.jpeg`:** interior style sample. Pale birch plywood lined walls,
  wide pale oak boards laid straight, white ceiling, big skylight, warm light, mid-century furniture
  (black leather safari chair, round timber coffee table, terracotta accents).
- **`style-ref-IMG_5539-finished-curve.jpeg`:** the finished-curve reference (tight crop). Crisp
  white/warm plastered curve, a curved skirting following the base of the curve, pale oak
  herringbone floor, warm light washing the curve. STYLE GUIDANCE ONLY, not ours to reproduce.

## STYLE LOCKED (Lee, 2026-07-23)

- Floor: wide pale oak boards, laid STRAIGHT, both levels.
- Walls: plasterboard throughout (no ply lining). White. The 5568 ref stands for mood, floor and
  warmth only.
- The curve: crisp white set plaster, curved skirting following the base (5539 as the read).
- Front door: Claude's to detail. Solid timber, vertical boards, a warm tone that does not contrast
  the floor too much (sits close to the pale oak).
- Everything else per LAYOUT v1 + v2 above.

## THE GENERATION PLAN + PROMPT (draft, for Lee's sign-off BEFORE running)

Model: google/nano-banana on Replicate, multi-image input, in this order:
1. `IMG_5566-clean-BASE.jpeg` (the photo to transform)
2. `IMG_5566-markup-junctions.jpeg` (the geometry authority)
3. `style-ref-IMG_5539-finished-curve.jpeg` (how the plastered curve reads)
4. `style-ref-IMG_5568-ply-interior.jpeg` (floor + light + warmth mood)

Output must hold the base photo's exact framing (native 4:5). Export 1080x1350. The BEFORE slide is
the clean base as-is.

### Prompt (v3 draft)

The first image is a construction photo of a timber framed curved wall in a house being built. The
second image is the identical photo with coloured markup lines showing exactly where the finished
wall junctions sit. Transform the first photo into the exact same house completely finished, from
the exact same camera position with the exact same framing. Follow the marked junctions precisely.
The purple lines are the curved wall's junctions: the wall becomes smooth white set plasterboard
following that exact curve, meeting a flat white plasterboard ceiling exactly along the upper purple
line, and meeting the floor exactly along the lower purple line, finished with a low white skirting
board that follows the curve, like the third image. The camera side is the upper level: wide pale
oak floorboards laid straight. The yellow lines are the corridor's wall junctions: the corridor is a
lower level, its white plasterboard ceiling lower than the main ceiling, with a clean white
plasterboard bulkhead taking up the height change where the two ceilings meet. At the green line the
floor steps down to the corridor level: one straight full-width step of two equal risers, the same
oak boards continuing over both levels. The red marked opening becomes a closed flush white sliding
door to a walk in robe. The blue marked opening at the end of the corridor becomes a closed solid
timber front door with vertical boards in a warm pale oak tone close to the floor colour, with a
narrow full height sidelight window beside it letting daylight down the corridor. All other framing
becomes finished flat white plasterboard walls with white skirting. The concrete slab becomes the
oak floor. The sky becomes the ceilings. Empty just-completed home, no furniture, warm natural
daylight like the fourth image, soft shadows, bright and airy, photorealistic real estate
photography, no people, no text, no watermarks, no logos, no markup lines in the output.

- The curve and ceilings: crisp white set plaster, warm light washing the curve, and the curved
  skirting detail following the curve base (per 5539).
- Floor: wide pale oak boards laid straight (per 5568). OPEN: Lee to pick straight boards vs 5539's
  herringbone.
- OPEN, the big style question: are the other walls white plaster throughout (5568 read as mood,
  floor and furniture ref only), or is the pale ply wall lining from 5568 wanted as a literal
  feature (say the corridor or WIR wall in ply)?
- Front door: no ref supplied yet. Proposal: solid timber, vertical boards, warm oak tone. OPEN for
  a ref or a yes.
- Furniture: foreground locked empty; 5568's furniture palette noted in case Lee wants a subtle hint
  at the living/dining frame edge later.

## The generation prompt (v1, keep in sync with what is actually run)

Transform this construction site photo into the exact same house completely finished, photographed
from the exact same position. Keep the curved wall's exact geometry and position: a full height
convex curved wall sweeping between two straight wall runs, bulging toward the camera. The timber
stud frame becomes a smooth plastered curved wall painted crisp white, a perfectly fair curve,
square set. All other framing becomes finished white plasterboard walls of the same rooms. The bare
concrete slab becomes pale oak engineered floorboards laid straight along the hallway. Where open sky
shows, a flat white plasterboard ceiling with a few recessed downlights. The building site background
becomes the finished interior of the same home: on the left a doorway into a bright daylit room, on
the right the hallway continuing along the straight wall. Empty just-completed home with no
furniture, warm natural afternoon daylight, soft shadows, bright and airy, photorealistic real
estate photography, no people, no text, no logos.
