# Formwork Builder soft launch — reel (2026-09-11)

**Lane:** Sell (Formwork Builder Showcase). **Format:** 9:16, 1080×1920, 30 fps, 99 s (17.5 s Lee to camera →
78 s builder demo under Lee's voiceover → end card). Captions burned in. IG + FB use the same file.
**Source:** Lee's take `IMG_5910.MOV` (Drive), jump-cut from 2:36 to 1:36. Builder footage captured live from
`builder.craftons.com.au/apps/formwork` building Lee's own design (share `fw-FTSclLEA`: Circle 220°, R2750,
550 high, 1030 seat, backrest 450/300/15°, cantilever, plates + shutters both sides, end caps).
**Build:** `pipeline/video/hyperframes/fw-reel/` (composition) · `pipeline/video/builder-capture/` (footage) ·
`pipeline/video/README.md` (the whole pipeline).


## v2 (2026-10-12) — Lee's feedback applied

**Structure:** Lee full-screen → on the words "Formwork Builder" the hero image from the website comes in as a
title card on the brand green (slow pan, about 2.5 s) → the builder with Lee's head and shoulders as a PIP top-right
(3D model nudged left in the capture so the PIP never covers it) → end card. The "New · Formwork Builder" tag is gone;
the hero card is the title now. About 68 s total (64 s of speech + end card), down from 99 s.

**Beats kept (Lee's words, in order):** 1 hook · 2 trimmed to "So we built this product, we're finally launching it,
we're happy with it, the Formwork Builder" · 3 "click into it" · 4 wall shape, circle and U-shape · 6 edit your
dimensions · 10 the backrest half only · 11 backrest height and width (taper cut) · 12 cantilever and kickers ·
13 scroll down to formwork, choose what you want cut · 14 plates · 15 shutters, bendy ply and 17mm ply · 16 end caps ·
17 five minutes on the website · 18 "you don't need to do any maths" (rest of the sentence cut) ·
19 "add to cart, or share quote for a client" (trailing words cut).
**Beats removed:** 5 L-shape · 7 straights · 8 "designing the concrete structure" · 9 "cool features" · 10 rounded
ends · 11 taper · 18 "the software works out everything" · 20 "delivered in three to four days" (the builder now shows
**5 to 7 business days** on screen for this design; the site has changed since September, so re-check before any
delivery claim in a caption).

**How it was made (reproducible):** `pipeline/video/recut.py` applies `builder-capture/keeps-formwork-v2.json` on
top of the jump cut; `pipeline/video/map-words.py` maps the corrected source transcript onto the cut (re-transcribing a
spliced cut makes Whisper drop words, so don't); `builder-capture/capture-fw-v2.mjs` is the shorter walkthrough;
`hyperframes/fw-reel/make-v2.py` derives every timing from the cut's words and fills `index.template.html`;
`finish-v2.sh` runs demo → check → render → captions → preview.

## Decisions for Lee

1. **The delivery line.** The take ends on "cut and delivered in three to four days". The builder itself shows
   **7 to 9 business days** for this design (4 to 5 with plates only), and that number is on screen in the video.
   Options: (a) cut the take after "share quote for a client or something like that" so the reel ends there, or
   (b) re-record that one sentence with the right number and I'll drop it in. v1 keeps the line so you can hear it.
2. **Length.** 99 s is a full walkthrough. Say the word and I'll cut a 35 to 40 s lean version from the same
   assets (intro, shape, dimensions, backrest, plates and shutters, price, end card).
3. **End card copy.** "Design it. Price it. Order it." + "Curved formwork, cut to your set-out. Link in bio."
   Swap in a handle if you want one.
4. **Caption style.** Same as the Radius Pro reel (green Inter Bold, live word in line green, no box).

## Caption (three variants, per SOCIAL-VOICE.md: sentence case, no emoji, soft CTA, ≤8 hashtags)

**A. Overview**
> Concreters kept asking for the full package for curved formwork. So we built it.
>
> The Formwork Builder is live. Pick the wall shape, punch in the dimensions, add a backrest or a cantilever if
> the job needs one, then tick the plates, shutters and end caps you want cut. The price sits there the whole
> time and the software does the maths.
>
> Design yours in the Formwork Builder. Link in bio.
>
> #curvedformwork #formwork #concreteformwork #concreters #curvedbenchseat #formply #formworkbuilder #BuiltWithCraftons

**B. Short**
> Curved formwork, designed in five minutes. No maths.
>
> Shape, dimensions, backrest, cantilever, then tick the plates and shutters you want cut. The Formwork
> Builder is live.
>
> Link in bio.

**C. Numbered**
> The Formwork Builder is live. The whole job in four moves.
>
> 1. Pick the shape. Circle, U, L or straight.
> 2. Punch in the dimensions off the plans.
> 3. Add the backrest, or a cantilever kicker, if the job has one.
> 4. Tick the plates, shutters and end caps. The price is right there.
>
> Design yours. Link in bio.

Every claim above is said or shown in the video. No delivery-day claim in the caption until decision 1 is made.

## Lee's final caption
_(record Lee's edit here)_
