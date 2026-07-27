# Radius Pro retarget video. Teardown + script (talking head + screen grab)

Reference: an Instagram reel by @hansloreidesign promoting Programa (interior-design software), sent by
Lee as the format to copy. We build a Craftons version for the retargeting audience, scripted against
`playbooks/META-ADS-SABRI-8-HACKS.md` (Sabri's 8 hacks. Lee called it the seven hacks file, this is it).

## Teardown

**Honest note on access:** Instagram walls the video itself, so I could pull the page metadata but could
NOT watch the footage or hear the audio. Everything below is split into confirmed vs inferred.

**Confirmed from the page:**
- Creator: @hansloreidesign, a verified interior designer.
- It is a promo for Programa (interior-design business software).
- Caption and call to action: "Comment 'Pro' and I'll send you a discount code to get started on
  Programa. #interiordesign" (a comment-to-DM lead mechanic).
- Engagement: about 620 likes, 86 comments. The comments are full of people typing "Pro" to trigger the DM.

**The format (from Lee's description, a recognisable creator-demo pattern):**
- A real person speaking to camera (talking head), native and unpolished.
- The desktop app screen recording sits in the top third of the screen, so the tool and its inputs are
  clearly visible while the person talks.
- A direct screen grab is fine. Low production is the point.

**Why this format works, mapped to the hacks:**
- **Hack 4 (do not look like an ad):** a real person talking to camera is the single most native thing
  on the platform. It reads as organic advice, not a produced ad. This is the whole reason it beats a
  slick asset, and it is the opposite of our polished config-demo reel (which is why that one is for
  warm/retarget and on-page, not cold).
- **Hack 5 (broad targeting, super-specific long copy):** a talking head can deliver a long, specific,
  in-the-trade monologue, which feeds the algorithm a rich context and builds human trust at the same time.
- **Hack 2 (identity trigger):** the creator IS the identity. An interior designer talking to interior
  designers. Ours: a builder or chippy talking to builders.
- **The top-third screen grab:** shows the product actually working (proof and the self-serve mechanism)
  without breaking the native feel. It is "here is the thing I am talking about," not an ad card.
- **The comment-to-DM CTA (hack 7 deeper funnel):** "comment a word" drives comments (a strong ranking
  signal) and captures a warm lead you then DM and follow up. It doubles as list building.

## Our version: format spec

- **Placement:** the retargeting audience (people who saw the wall-plate ad or hit the site). Warm, so a
  demo-and-talk works. Keep the real Lawless job photo as the cold opener.
- **Aspect:** 9:16 (1080x1920) for Reels and Stories.
- **Layout:** top third is a clean Radius Pro screen grab (the configurator with the input fields
  visible). Bottom two thirds is the presenter talking to camera. We can reuse the config-demo capture we
  already built for the top-third demo, or grab a fresh raw recording.
- **Presenter:** builder-to-builder voice. Works whether it is Lee or an actual chippy. Real beats polished.
- **Production:** phone camera, direct screen grab, one take. Native is the goal, not a studio look.

## The script: first-person "how I use it" (Lee's direction)

A real tradie sharing their own workflow, not a demo of "how to use our tool" and not the problem story.
This is the most native angle (hack 4): it sounds like a chippy telling a mate what he uses, so it reads
as UGC, not an ad. Keep it plain and first-person. Do NOT over-polish it, the rough voice is the point.
Every line is one on-screen action so the VO and the top-third screen grab move together. We cut, we do
not bend. No em or en dashes.

**Primary cut (about 18 seconds):**

| VO (talking head, first person) | Top-third screen grab |
|---|---|
| "Radius Pro is so simple to use." | Radius Pro open |
| "I just go through my plans and add all my curved plates to the parts list." | Adding parts, the list filling up |
| "You set the angle, the width, the quantity for each one." | Editing angle, width, quantity |
| "Then check out, and they turn up cut to size, two days later." | Order summary, then checkout |

**Leaner cut (about 12 seconds):**

| VO (talking head, first person) | Top-third screen grab |
|---|---|
| "Radius Pro is dead simple." | Radius Pro open |
| "I add every curved plate off my plans to the list, set the angle, width and quantity, and check out." | Parts list + editing fields + checkout |
| "They turn up cut to size, two days later." | Order summary |

Delivery is locked at 2 days (matches the "2 Days" turnaround on the screen grab). Fields named are real:
Width is the on-screen "Width (w)" field.

## Generating the presenter with Veo 3 (from Lee's avatar image)

We animate a specific still Lee provided: a friendly presenter at a podcast mic in a warm home studio,
landscape. Veo 3 (in Gemini) does image-to-video with native dialogue and lip-sync. Clips run about 8
seconds, so the primary VO is two clips. Feed the same still as the start frame each time. To smooth the
join, use the last frame of clip 1 as the start image for clip 2, or cut to the screen grab on the seam.

**Final layout (matches the Instagram reference):** 9:16 vertical, the landscape Radius Pro screen grab on
top, this landscape avatar below. So generate the avatar in 16:9 landscape, matching the image.

**Paste into Gemini (attach the image), swap the line per clip:**

> Animate this photo into a natural talking-head video. The man looks straight into the camera and talks to
> it like he is chatting to a mate: warm, easy, confident, relaxed Australian accent. Give him subtle life:
> small head movements and nods, natural blinking, a slight friendly smile, easy breathing and light
> shoulder movement. He stays seated at the podcast mic. Keep the background, lighting and framing exactly
> as in the image. Accurate lip-sync to the words. Clean close-mic voice with soft warm room tone, no music.
> 16:9 landscape, matching the photo. No subtitles, no captions, no on-screen text.
>
> Voice: Zubenelgenubi. Accent: Australian, casual and warm. Temperature: 1.2.
>
> He says: "[LINE]"

**Lines (our approved copy, primary cut, two clips):**
- Clip 1: `"Radius Pro is so simple to use. I just go through my plans and add all my curved plates to the parts list."`
- Clip 2: `"You set the angle, the width and the quantity, then check out, and they turn up cut to size, two days later."`

**Notes:**
- Generate a few takes per clip and pick the most natural, least stiff one.
- No burned-in captions from Gemini (we add our own for silent autoplay).
- Keep it human. If he looks too glossy or robotic, regenerate. A too-slick avatar reads as an ad.

## Stronger variant: the boss on a high-end job (fixes hack 4 + hack 2)

The polished podcast presenter reads as a professional "presenter ad". The same man as the boss on a
near-finished high-end job reads as a real person filming himself, which is the whole native advantage
(hack 4), and it makes the identity trigger visual and instant (hack 2): a builder sees one of their own
before a word is spoken. Keep the same face and framing by editing the existing V2 avatar photo, then
animate that. Decisions (with Lee): same guy, khaki shirt + plain black puffer (no logo), no hard hat,
a subtle curved feature wall behind him.

**Step 1. Image-edit the existing V2 avatar photo (Gemini), keep the man and framing:**

> Edit this photo. Keep the same man, his face, hair, pose and the camera framing exactly. Change his
> clothing to a khaki button-up work shirt with a plain black puffer vest over the top, no logos or text on
> it. He should look put-together and confident, like the boss of the job. Replace the home-studio
> background with the interior of a high-end house at finishing stage: a warm, near-finished room with a
> subtle curved feature wall visible behind him (present but not the focus), and protective cardboard sheets
> laid over the floor. Natural indoor daylight. Remove the podcast microphone. Keep it looking like a real,
> candid phone photo taken on site, natural and believable, not a glossy studio shot. 16:9 landscape.

**Step 2. Animate the edited photo (Gemini / Veo 3), same settings, swap the line per clip:**

> Animate this photo into a natural talking-head video. The man stays standing in one spot and talks
> straight to the camera like he is telling a mate on the job: warm, easy, confident. He does not walk or
> move around the room, and the camera is locked off, static, with no panning, zooming or camera movement.
> Only subtle, natural life: small head movements and nods, natural blinking, a slight friendly smile, easy
> breathing and a light shoulder or hand gesture. Keep the interior background, lighting and framing exactly
> as in the image. Accurate lip-sync. Clean voice with quiet indoor room tone, no music. 16:9 landscape. No
> subtitles, no captions, no on-screen text.
>
> Voice: Zubenelgenubi. Accent: Australian, casual and warm. Temperature: 1.2.
>
> He says: "[LINE]"

Same two lines as above. This slots straight into the composite in place of the podcast avatar (same
16:9 landscape, cropped to portrait for the bottom panel).

**Copy notes (from the hacks):**
- Native first (hack 4): a real person's workflow, unpolished. If it sounds like a voiceover artist, redo it.
- Swap one word to clone it for another trade: chippy, builder, carpenter, shopfitter, formworker (hack 2).
- Every number is true. Never invent specs.
- Scent match (hack 6): "cut to size" and "parts list" match the live ads and the tool.
- Product truth: we CUT the plates, we never bend. Self-serve only, never "send us your plans".

## Next steps
1. Lee (or a chippy) records the talking head to this script, phone camera, one take.
2. Screen grab the Radius Pro flow (or reuse the config-demo capture) for the top third.
3. Edit: screen grab top third, presenter below, burned-in captions for silent autoplay.
4. Run it in the retargeting ad set as a second creative against the static and the config-demo reel.

## The published ad caption (Sabri structure)

Used on the live retarget video ad (2026-07-27). Problem, agitate, the turn with real numbers, the
triplet, soft mechanism close. No em or en dashes.

```
The curved wall is always the bit that blows the program.

Marking it out, snapping jigsaw blades chasing the line, binning half a pack of ply, and it's still never quite true.

Radius Pro is the other way. Pull your curved plates off the plans, punch in the radius, the width and the angle, set how many you need, and check out. Every plate turns up cut to the exact radius out of 17mm formply, engraved and ready to stand. Two days.

No marking out. No jigsaw. No waste.

If the curved jobs are the ones that always cost you a day, they don't have to. Punch in your radius, we cut the plates.

Design yours online at craftons.com.au
```
