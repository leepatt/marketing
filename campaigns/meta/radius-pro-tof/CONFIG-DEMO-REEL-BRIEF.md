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
- **Hook: identity, matching the winner.** "Now any chippy can frame a curve." Carries the winning ad's
  angle straight into the demo (hack 2 identity trigger, hack 6 scent match).
- **Audio: silent + kinetic captions.** Feed and Reels autoplay muted, so the captions carry it.
- **Scent (hack 6):** captions and CTA echo the live winning language ("cut to the exact radius",
  "priced online", "punch in your radius") so the ad, the reel and the page all say the same thing.
- **House rules:** we cut, we do not bend. No em or en dashes anywhere.

## The reel-spec (paste into `content-engine/specs/radius-pro-wall-plates.json`)

```json
{
  "slug": "radius-pro-wall-plates",
  "meta": {
    "title": "Curved wall plates",
    "product": "curves",
    "dims": { "radius": 900, "width": 140, "angle": 135 },
    "material": "form-17",
    "aspect": "9:16",
    "fps": 30
  },
  "capture": {
    "url": "http://localhost:3000/",
    "fields": [
      { "beat": "radius", "id": "specifiedRadius", "from": 1200, "to": 900, "dur": 1.1 },
      { "beat": "width",  "id": "width",           "from": 100,  "to": 140, "dur": 1.0 },
      { "beat": "angle",  "id": "angle",           "from": 90,   "to": 135, "dur": 1.2 }
    ],
    "click": { "text": "Add Part" },
    "summaryHeading": "Order Summary",
    "beats": { "settle": 1.0, "hold": 1.6 }
  },
  "shots": [
    { "type": "hook", "headline": "Now any chippy can frame a curve." },
    {
      "type": "ui-capture",
      "autozoom": true,
      "captions": [
        { "beat": "radius",  "text": "Set your radius." },
        { "beat": "width",   "text": "Plate width." },
        { "beat": "angle",   "text": "Sweep the wall." },
        { "beat": "summary", "text": "Cut to the exact radius." },
        { "beat": "hold",    "text": "Priced online. Ready to order.", "pos": "top" }
      ]
    },
    { "type": "cta", "line": "Punch in your radius", "url": "craftons.com.au" }
  ],
  "audio": { "musicMood": null, "vo": null },
  "captions": { "on": true, "style": "kinetic-word", "font": "Aeonik" },
  "brand": { "motif": true, "look": "stylized" }
}
```

## Run it

```bash
# 1) real configurator running once (separate repo)
cd /workspace/craftons-curves-calculator && npm install && npm run build && PORT=3000 npm start &
# 2) from content-engine/
npm install
npm run render -- specs/radius-pro-wall-plates.json
```

## Confirm before rendering (no guessing, verify against the live configurator)

1. **Dimensions read as a wall plate.** The from/to values sit inside the ranges the bench-seat and
   formwork specs already use, so they are safe, but open the configurator and check the built shape
   reads as a feature-wall arc. If the tool allows a bigger radius, a larger, gentler curve looks more
   like a wall. Nudge radius up for drama if it is in range.
2. **Field IDs, click text, material.** `#specifiedRadius`, `#width`, `#angle`, the "Add Part" button,
   the "Order Summary" heading, and material `form-17` (17mm Formply) all match the bench-seat spec, but
   confirm they are current on the curves product before the run.
3. **Hook alt for maximum scent match.** If you want the reel to mirror the live ad word for word, swap
   the hook headline to the full winning line: "Any architect can draw a curve. Now any chippy can frame
   one." Kept the shorter version above per the workshop pick.

## Where it goes once rendered

- **BOF retarget challenger:** add it as a second creative in the existing Add To Cart ad set, head to
  head with the current static config image. Keep the winner (do not just swap out a producer).
- **Product page:** radius-online hero, muted autoplay in a contained 9:16 player. Tightens scent.
- **Optional feed cut:** a 1:1 or 4:5 crop later if we want it in feed as well as Reels and Stories.
