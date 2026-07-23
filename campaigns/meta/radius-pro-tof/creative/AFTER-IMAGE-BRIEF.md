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
