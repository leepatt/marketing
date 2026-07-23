# Handoff: generate the curved-wall ad images (paste into the new session)

## Your job this session
Generate the TWO carousel images for the curved-wall ad (builders + carpenters, Radius Pro TOF):
- **BEFORE = the timber FRAME** of a curved wall.
- **AFTER = the FINISHED curved wall.**
Same wall, same viewpoint, so they work as a before/after swipe. The ad copy is already locked (do not
rewrite it). This session is only about producing the two images to spec, for Lee to approve.

## THE BIBLE (read first, in this order)
Everything is governed by Sabri Suby's 8 hacks. Do not freelance away from it.
1. `playbooks/SABRI-8-HACKS-TRANSCRIPT.md` (verbatim source of truth, read first)
2. `playbooks/META-ADS-SABRI-8-HACKS.md` (the distilled method)
Then the campaign files:
3. `campaigns/meta/radius-pro-tof/AD4-AD5-BRIEF.md` (why/what for this ad)
4. `campaigns/meta/radius-pro-tof/CURVED-WALL-BUILD-SPEC.md` (HOW the wall is built. The source of truth
   for the render. Follow it exactly.)
5. `campaigns/meta/radius-pro-tof/AD-CONCEPTS.md` (the locked copy + the test matrix)

Repo `leepatt/marketing`, branch `claude/radius-pro-tof-meta-ads-0fwzlj`. Start with
`git checkout claude/radius-pro-tof-meta-ads-0fwzlj`.

## Reference images to RE-UPLOAD (they are session-scoped, so re-attach them here)
- **IMG_5539** finished curved wall (Lawless "Casa Sol"). The SHAPE + viewpoint reference for both
  slides, and the base for the AFTER. NOTE: we do NOT have rights to this photo, so the AFTER slide must
  be an AI-reworked version, changed enough to be ours (different floor, light, room beyond).
- **IMG_5548** the refined timber-frame render (current best BEFORE). Good starting point.
- **IMG_5543 / IMG_5544 / IMG_5545** real curved-wall framing on site (build-detail reference). IGNORE
  the steel strapping in them.
- **IMG_5540** conventional curved-wall framing (extra reference).

## The construction spec (from CURVED-WALL-BUILD-SPEC.md, summarised. That file wins if there is any doubt)
- **Geometry:** a single soft curve that JOINS TWO STRAIGHT WALLS, CONVEX (bulging toward the camera),
  matching IMG_5539. Not a cylinder, drum or pod. Full height, floor to trusses.
- **Plates (our product):** 17mm Formply, top and bottom, DOUBLED to 34mm. Flat faces matte BLACK
  (phenolic), edges show pale ply grain. Same 90mm width as the studs, flush both sides, no overhang.
  The black curved BOTTOM plate sits on the concrete slab and contrasts dark against it.
- **Studs:** 90x35 pine, plumb, evenly spaced at **125mm centres**, narrow 35mm face to the room.
- **Noggins:** single row at mid height, ~150mm blocks, grain vertical, slightly UNEVEN (nudge 2 or 3
  off the line) so it is not laser-perfect.
- **Scene:** genuine mid-build, ZERO finished work. Bare concrete slab (swept but a bit dusty), EXPOSED
  roof trusses overhead (no plasterboard), no doors, jambs, architraves, skirting or finished floor.
  Openings are raw timber-framed.

## What "done" looks like
Two clean, NATIVE images (no on-image text, no logos, no CTA. The photo IS the content, hack 4):
- **Frame (before):** matches IMG_5539 shape + the spec above.
- **Finished (after):** the same wall finished, AI-reworked from IMG_5539 so it is ours, matched to the
  frame's viewpoint.
Export each at **4:5 (1080x1350)** primary and **1:1 (1080x1080)**. Same ratio across the pair.
Deliver to Lee for approval (a human approves every asset). Nothing goes live from this session.

## Image-gen tooling that worked (this environment)
- Use **Replicate** (`REPLICATE_API_TOKEN` is set in env). The Glif API the ai-image-generation skill
  wants is DEPRECATED (410), so call Replicate directly with curl.
- **Best for a same-viewpoint transform** (finished photo -> its frame, or reworking the finished):
  `black-forest-labs/flux-kontext-pro` (single `input_image` + prompt, preserves geometry).
- **Best for build-accurate framing from references:** `google/nano-banana` (Gemini 2.5 Flash Image,
  takes an `image_input` array. Feed IMG_5539 for shape + IMG_5545 for build detail). This produced the
  best frame so far. Do NOT feed the drum photo (IMG_5543) as the main ref or it drifts to a cylinder.
- Pass images as base64 data URIs. Poll the prediction get-url until `succeeded`, then download the
  output. Watch for a 429 (rate limit) and retry.
- Learnings: text-to-image invents the wrong curve; nano can copy junk from a screenshot (it once copied
  an "Add comment" bar, crop it); force CONVEX and "joins two straight walls, not a cylinder".

## Guardrails (non-negotiable)
- The 8 hacks are the bible. Native, not ad-looking. Real approves AI.
- Product truth: we supply ONLY the doubled 34mm Formply plates, cut to the exact radius. We CUT, we
  never bend. Do not imply we build the wall.
- No em dashes, no en dashes, ever.

## Already locked (do NOT redo)
- The copy (builder + chippy versions) and the test matrix are locked in `AD-CONCEPTS.md`.
- Identity: builder vs chippy (one-word clone, run both). Slide order A/B: frame-first vs finished-first.

## After the images are approved (next session, not this one)
Wire AD4 (builder) + AD5 (chippy), each with the frame-first and finished-first slide orders, into the
live ad set `120247183658270186` (campaign `120247183657950186`), built PAUSED for a real Meta preview,
destination `craftons.com.au/products/radius-online` with the utm_content tags in `AD-CONCEPTS.md`.
Then Lee approves and flips to active. Judge on net cash + phone volume (hack 8), not CTR alone.
