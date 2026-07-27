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

## Generating the presenter with Veo 3

Veo 3 does native dialogue and lip-sync, so it can speak the VO. Clips are short (about 8 seconds), so the
~12s leaner cut is two clips, the ~18s primary is three. Keep the same character across clips (reuse the
description word for word, and use the last frame of clip 1 as the reference image for clip 2).

**Reusable scene + character block (put this in every clip prompt):**

> A rugged Australian carpenter in his 30s, hi-vis work shirt, standing in a bright timber workshop with
> curved plywood offcuts on the bench behind him. Natural daylight. He talks straight to camera like he is
> telling a mate, relaxed and genuine, light Australian accent. Framed in the lower two thirds of a 9:16
> vertical frame, with a plain wall and workshop space in the upper third above his head (leave that space
> clear for a graphic overlay). Handheld, natural, unpolished. No subtitles, no on-screen text, no captions.

**Then append the spoken line per clip, in quotes, e.g.:**
- Clip 1: `He says: "Radius Pro is dead simple. I just add every curved plate off my plans to the parts list."`
- Clip 2: `He says: "Set the angle, the width, the quantity, check out, and they turn up cut to size, two days later."`

**Veo 3 notes:**
- The upper-third framing leaves room for the Radius Pro screen grab to sit in the top third in edit.
- Keep it looking unpolished. If Veo makes him too glossy or corporate, regenerate. Native is the point.
- No burned-in captions from Veo (we add our own for silent autoplay).
- Vertical 9:16. Generate a few takes and pick the most natural, human one.

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
