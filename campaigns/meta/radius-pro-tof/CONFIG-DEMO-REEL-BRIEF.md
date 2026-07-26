# Radius Pro config-demo reel. Brief + reel-spec (the tool prompt)

**Produced by:** the Craftons content engine in `cnccut-app/content-engine/` (Playwright drives the real
configurator, Remotion adds the cinematic layer, renders a 9:16 1080x1920 MP4).
**Asset job:** show, in motion, that a curved wall plate is designed online and priced instantly. The
purest proof of the golden rule (self-serve online builder, we never say send us your CAD).

## Decisions locked (with Lee, against Sabri's hacks)

- **Placement: retarget + product page.** A polished product demo reads as an ad to a cold scroller, so
  per hack 4 it lives where people already know the product: the BOF retargeting pool (people who saw
  the wall-plate ad) and the radius-online page hero. The real Lawless wall-frame photo stays the cold
  TOF opener.
- **Framing: curved wall plates, for chippies.** Matches the winning live ad (AD5) and the number-one
  target. Captions frame the curve as wall plates.
- **Build: 1200mm radius, 90mm wide plate, 90 degree angle, quantity 8.** A real order, so the instant
  price at the end is a meaningful number, not a single-part figure.
- **Hook: identity, matching the winner.** "Now any chippy can frame a curve." (hack 2, hack 6).
- **Audio: silent + kinetic captions** for the muted ad. Voiceover is a later optional layer for the
  sound-on product-page cut (see Runtime and VO below).
- **Scent (hack 6):** captions and CTA echo the live winning language ("cut to the radius", "priced
  online", "punch in your radius").
- **House rules:** we cut, we do not bend. No em or en dashes anywhere.

## The reel-spec (paste into `content-engine/specs/radius-pro-wall-plates.json`)

```json
{
  "slug": "radius-pro-wall-plates",
  "meta": {
    "title": "Curved wall plates",
    "product": "curves",
    "dims": { "radius": 1200, "width": 90, "angle": 90, "quantity": 8 },
    "material": "form-17",
    "aspect": "9:16",
    "fps": 30
  },
  "capture": {
    "url": "http://localhost:3000/",
    "fields": [
      { "beat": "radius",   "id": "specifiedRadius", "from": 900, "to": 1200, "dur": 0.9 },
      { "beat": "width",    "id": "width",           "from": 140, "to": 90,   "dur": 0.4 },
      { "beat": "angle",    "id": "angle",           "from": 45,  "to": 90,   "dur": 0.9 },
      { "beat": "quantity", "id": "quantity",        "from": 1,   "to": 8,    "dur": 0.7 }
    ],
    "click": { "text": "Add Part" },
    "summaryHeading": "Order Summary",
    "beats": { "settle": 0.4, "breathe": 0.5, "summary": 0.7, "hold": 1.0 }
  },
  "shots": [
    { "type": "hook", "headline": "Now any chippy can frame a curve." },
    {
      "type": "ui-capture",
      "autozoom": true,
      "captions": [
        { "beat": "radius",   "text": "Your radius." },
        { "beat": "angle",    "text": "The angle." },
        { "beat": "quantity", "text": "Eight parts." },
        { "beat": "summary",  "text": "Cut to the radius." },
        { "beat": "hold",     "text": "Priced online.", "pos": "top" }
      ]
    },
    { "type": "cta", "line": "Punch in your radius", "url": "craftons.com.au" }
  ],
  "audio": { "musicMood": null, "vo": null },
  "captions": { "on": true, "style": "kinetic-word", "font": "Aeonik" },
  "brand": { "motif": true, "look": "stylized" }
}
```

## Runtime and VO

The reel is **hook (2.2s, `HOOK_FRAMES` in `remotion/Reel.tsx`) + the capture + CTA (3.2s, `CTA_FRAMES`)**.
With the beats above the capture is roughly 7 seconds, so the **whole reel lands around 12 seconds**.

- **Under 10s is not worth forcing.** The hook and CTA alone are 5.4s, so a sub-10 total means a rushed
  capture and a rushed price reveal. About 12s is the right length for a retarget and product-page demo
  (under 15s is the threshold that matters).
- **To go tighter to about 11s:** trim `CTA_FRAMES` from 96 to about 60 in `remotion/Reel.tsx` and pull
  the `hold` beat down. That is a code change, not a copy change. Copy length does not drive runtime.
- **Voiceover:** captions are the copy for the muted ad (feed and Reels autoplay silent), so keep them
  short as above. VO is a separate optional layer for the sound-on product-page cut. Lee's instinct is
  right: render the silent reel first, read the exact runtime off the render, then script the VO to fit
  (about 12s is roughly 28 to 32 words). Do not block the ad on VO.

## Confirm before rendering (no guessing, verify against the live configurator)

1. **Quantity input.** The spec animates a `quantity` field from 1 to 8. This assumes the configurator has
   a numeric quantity INPUT with `id="quantity"`. **Confirm the real id** (could be `qty`, `partQty`, etc.).
   If quantity is a plus/minus stepper rather than a text input, the capture script needs a small tweak
   (the native setter only works on an input with an id). Tell me the id or point me at the calculator
   repo and I will lock it.
2. **Dimensions in range.** Targets radius 1200, width 90, angle 90 are Lee's. The from values (900, 140,
   45) just give a visible sweep. Confirm 90mm width and 45 degree start are inside the configurator's
   valid input ranges, adjust the from values if not (keep the to targets).
3. **Plumbing current:** `#specifiedRadius`, `#width`, `#angle`, the "Add Part" button, "Order Summary"
   heading, and material `form-17` all match the bench-seat spec, confirm they are still right.
4. **Hook alt for maximum scent:** to mirror the live ad word for word, swap the hook to "Any architect
   can draw a curve. Now any chippy can frame one." Kept the shorter version per the workshop pick.

## Where it goes once rendered

- **BOF retarget challenger:** add it as a second creative in the existing Add To Cart ad set, head to
  head with the current static config image. Keep the winner (do not just swap out a producer).
- **Product page:** radius-online hero, muted autoplay in a contained 9:16 player. Tightens scent.
- **Optional feed cut:** a 1:1 or 4:5 crop later if we want it in feed as well as Reels and Stories.
