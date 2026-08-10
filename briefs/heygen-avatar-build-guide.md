# HeyGen avatar build — the full production guide

_Goal: one AI presenter, consistent across hundreds of videos, that doesn't read as slop._
_Written 2026-08-10. Sources: HeyGen help centre (Personal Model, Avatar V, Photo Avatars), Aug 2026._

---

## The one thing that decides quality

Everyone thinks the avatar is made when you upload a photo. It isn't. **The avatar is made by the
identity image set you train the Personal Model on.** Ten mediocre images gives you a face that
subtly changes between videos — different nose width, different jaw, different age — and viewers
clock it without being able to say why. Thirty deliberate images gives you a person.

Budget 80% of your effort on Steps 1–3. The HeyGen clicking is the easy part.

---

## Step 0 — Decide what this avatar *is* (do this before anything)

Two different products, two different pipelines. Pick one and don't hybridise.

| | **A. Synthetic presenter** (recommended for you) | **B. Digital twin of a real person** |
|---|---|---|
| Source | AI-generated images of a person who doesn't exist | Real photos + a 15s video of Lee/Jake/a hired face |
| HeyGen path | Photo Avatar → **Personal Model** → Generate Looks → Avatar IV | **Clone a Real Person** → Avatar V |
| Realism ceiling | High, but motion is generic | Highest — Avatar V learns *that person's* gestures |
| Risk | Uncanny stiffness; identity drift | Person leaves / wants out; consent admin |
| Cost to change later | Total rebuild | Total rebuild |

**You said your images are already generated → you're on Path A.** That's the right call for a
brand-owned presenter you'll use for years: nobody can quit, nobody ages, no release forms.

The one thing Path A gives up is Avatar V, which builds a fine-tuned motion model from a 15-second
reference video and is HeyGen's best realism tier. **Workaround if you want Avatar V later:** once
the character is locked, generate a 15s talking-head *video* of them (Kling / Veo / Runway,
image-to-video from your hero frame), then feed that as the Avatar V reference. Treat that as a
Phase 2 upgrade — don't block the build on it.

> ⚠️ **Decide now and write it down, because every later step is downstream of it.** Changing the
> face after you've shot 40 videos means every video before it is now a different person.

---

## Step 1 — Write the character bible (30 minutes, saves you months)

Before you look at a single image, write a fixed description you will paste into every future
prompt for the next three years. This is what stops drift when you generate new looks in 2027.

Template — fill it in and commit it:

```
NAME (internal):
AGE:                       e.g. 38–42, reads mid-late 30s
BUILD:                     e.g. solid, tradie build, broad shoulders
HAIR:                      colour, length, style, parting side, grey at temples y/n
FACIAL HAIR:               exact — "short stubble, 3-day, no moustache gap"
FACE:                      jaw shape, nose, brow, cheekbones, skin texture (pores, sun-weathered)
EYES:                      colour, shape, crow's feet y/n
DISTINGUISHING:            one memorable feature — small scar, gap tooth, freckles.
                           A face with no distinguishing feature drifts more.
SKIN TONE:                 specific, not "medium"
WARDROBE BASE:             the default outfit they're in 70% of the time
LOOK/LENS:                 e.g. 50mm, shallow depth of field, soft key from camera-left,
                           natural colour, no beauty retouching, visible skin texture
NEVER:                     no hat, no sunglasses, no hi-vis over the shoulders in close-ups,
                           no heavy grade, no glossy "AI skin"
```

Two notes that matter more than they sound:

- **Give them a flaw.** Perfectly symmetrical, poreless faces are the #1 tell of AI. Ask for visible
  pores, slight asymmetry, sun damage if they're meant to read Australian trade.
- **Decide if they're a Craftons employee or a presenter.** If viewers think they're meeting your
  actual estimator, that's a trust problem when they call and he doesn't exist. My recommendation:
  they're an unnamed presenter/host, never introduced as "I'm Dave from Craftons."

---

## Step 2 — Build the identity image set (the real work)

**Target: 30+ images. Absolute minimum: 10.** HeyGen's own guidance is that 10 trains, 30+ is
"strongest results," and the quality indicator in the training panel will push you toward 30.

### Technical specs per image

| Spec | Requirement |
|---|---|
| Resolution | ≥1024px short side. Aim 1500–2048px. |
| Format | PNG or high-quality JPG. **No screenshots, no re-saves, no WhatsApp/phone-share copies** — recompression artifacts poison training. |
| Face size in frame | Face occupies roughly 25–60% of the frame height. Not a tiny figure in a wide scene. |
| Focus | Eyes tack sharp. Any motion blur or soft focus = reject. |
| Subject | One person only. No second face anywhere in frame, even blurred in the background. |
| Face coverage | Eyes, mouth and lips clearly visible and unobstructed. |

### The coverage matrix — don't upload 30 near-identical images

Thirty variations of the same shot teaches the model one pose, not a person. Spread them:

| Dimension | Aim for |
|---|---|
| **Angle** | ~12 straight-on, ~10 slight turn (15–20°), ~6 three-quarter (30–45°), ~2 slight up/down tilt |
| **Framing** | ~15 close-up (chest up), ~10 half-body (waist up, hands sometimes visible), ~5 wider |
| **Expression** | Neutral, warm smile, mid-sentence talking, listening/attentive, serious/explaining. Get all five. |
| **Wardrobe** | 4–6 distinct outfits. This is how the model learns *the face* is you and the shirt isn't. |
| **Lighting** | Soft studio, natural window light, warm workshop, slightly overcast outdoor. Vary it — but keep all of it *flattering and clean*. |
| **Background** | Vary. Plain, workshop, site, office. Prevents the model baking a background into the identity. |

### Hard reject list (HeyGen's + mine)

- Group photos, or anyone else in frame
- Hats, caps, hard hats, sunglasses, safety glasses, anything covering the face
- Heavy filters, heavy grading, beauty smoothing, obvious retouching
- Low res, blurry, noisy, compressed
- Extreme angles, extreme expressions, mouth wide open mid-shout
- Hands over the face, phone in front of face, mic covering the mouth
- Inconsistent age/weight across the set — pick one version of this person

### Getting consistency out of an image generator (Path A specific)

This is where most synthetic avatars fall over. The set drifts and the Personal Model averages a
blurry composite of four slightly different people. Tactics, in order of effectiveness:

1. **One hero frame first.** Generate until you have a single, undeniable, perfect image. That's
   your reference. Everything else is derived from it, never generated independently.
2. **Use character-reference / identity locking**, not just text prompts. Whatever tool you're on —
   Midjourney `--cref`, FLUX with an IP-Adapter or a trained LoRA, Nano Banana / Gemini image
   editing with the hero attached, Higgsfield Soul-type character features. Text alone will drift.
3. **Better: train a LoRA on your best 10–15 images**, then generate the remaining 20 from it. Two
   rounds. This is the same "locked style" logic already in `QUALITY-DOCTRINE.md` §3, applied to a
   face. It's the single biggest quality jump available.
4. **Same model, same settings, same seed family** for the whole set. Don't mix Midjourney output
   with FLUX output — different renderers have different "skin physics" and the model sees two people.
5. **Change one variable at a time.** Same prompt, swap only the outfit. Then only the angle. Then
   only the lighting. Drift compounds when you change three things at once.
6. **Cull hard.** Generate 100+, keep 30. Any image where you hesitate for even a second on "is that
   the same guy?" — bin it. One bad image in thirty measurably degrades the model.

---

## Step 3 — QC gate (send me the images here)

Send them and I'll run every one against this rubric. Anything scoring a fail on a **blocker** gets
cut, no discussion.

**Blockers (auto-reject)**
- [ ] Not the same person as the hero frame (the drift test — flick between them; if the nose,
      jaw or eye spacing moves, it's out)
- [ ] Face obscured / eyes or mouth not clearly visible
- [ ] Below resolution, soft, blurry, or visibly compressed
- [ ] More than one person in frame
- [ ] Six-fingered hands, melted ears, warped teeth, mangled jewellery — check the edges of every image
- [ ] Text in frame (signage, shirt logos) that's AI-garbled

**Quality marks (fixable, but note them)**
- [ ] Plastic/poreless skin — needs texture
- [ ] Over-symmetrical face
- [ ] Dead eyes / no catchlight
- [ ] Lighting that doesn't match the rest of the set's overall feel
- [ ] Whole set too similar (fails the coverage matrix above)

**Set-level checks**
- [ ] ≥30 images (or ≥10 to proceed as a test run)
- [ ] Coverage matrix satisfied across angle / framing / expression / wardrobe / lighting
- [ ] Consistent apparent age, weight, hairline across all of them
- [ ] At least 3 images that are unambiguously "the base look" candidates: clean close-up or
      half-body, neutral-to-warm expression, nothing covering the face

**What to send:** the full set as files, plus tell me which one you think is the hero. I'll come
back with keep / cut / regenerate-with-this-prompt-change per image, and a verdict on whether the
set is strong enough to train on or needs another round.

> **Don't train until this passes.** Training is 60 credits and 10–15 minutes; regenerating images
> is cheap by comparison. Fix the input, not the output.

---

## Step 4 — Create the Photo Avatar in HeyGen

1. **Avatars** tab → **New Avatar**
2. Choose **Upload Photo** (you already have images — don't use "Design with AI", you'd lose control
   of the character bible)
3. Upload your **hero frame** as the base
4. Name it with a version: `Craftons-Presenter-v1` — you will make a v2 one day, and you need to be
   able to tell renders apart

Plan note: free tier caps you at 3 photo avatars; Creator/Team/Enterprise is unlimited. Personal
Model training is **paid plans only**.

---

## Step 5 — Train the Personal Model ← the step people skip

This is what turns "a photo that talks" into "a consistent character." HeyGen's framing is exact:
*the prompt tells HeyGen what to create; the Personal Model tells HeyGen who should be in it.*
Without it, every new look you generate is a re-interpretation of one photo, and the face wanders.

1. Open your avatar → **Generate Looks** panel
2. Toggle **Personal Model** in the prompt bar
3. Select photos — you can pull from existing uploads, AI-generated looks, or upload fresh. Use the
   tabs to filter sources.
4. Watch the **progress counter** — push past 30. Watch the **quality indicator** and fix what it flags.
5. **Train** → confirm **60 credits**
6. ~10–15 minutes. It activates immediately for new generations.

**Rules for the rest of the avatar's life:**
- **Never retrain on your own AI-generated outputs.** Generational copying degrades the identity —
  same reason you don't photocopy a photocopy. Train on your curated source set only.
- If you improve the character later, train a **new model version** and keep the old one until every
  in-flight video is finished.

---

## Step 6 — Build the Looks library (do it once, properly)

A "look" = the avatar in a specific outfit/environment. Build the full set in one sitting so they
share a visual family, rather than adding one ad-hoc every month.

Three ways to generate: upload reference photos, prompt a description, or pick library inspiration.
Prompt structure that HeyGen responds to — **image type → main subject → background scene →
composition**, most important detail first (the model weights the front of the prompt heavier):

```
Photorealistic half-body portrait photograph, [character bible description],
wearing [outfit], standing in [environment], shot on 50mm, soft key light from
camera-left, shallow depth of field, natural skin texture, direct eye contact
with camera, centred composition with space at frame-right for on-screen graphics
```

**Suggested canonical set for Craftons (6–8 looks, no more):**

| Look | Use case | Notes |
|---|---|---|
| Clean studio, mid-grey backdrop | Talking-head explainers, ads | Your workhorse. Leaves room for graphics. |
| Workshop floor, machinery soft in background | How-To Series intros/outros | Background must be **blurred** — see tips |
| On-site, timber/frames behind | Builder-facing, Formwork Builder content | |
| Seated at desk, laptop edge in frame | Ordering / configurator walkthroughs | |
| Tighter close-up, plain dark background | Hooks, punchy 5-second openers | |
| Wider half-body, neutral | Anything needing lower-third graphics | |

Leave **frame-right or frame-left consistently empty** in your main looks. That's where product
renders, dimensions and captions go. Decide the side now and never flip it.

Generate 5–10 candidates per look, keep one. Human gate, per doctrine §5.

---

## Step 7 — Lock the voice (half the identity, and it's usually an afterthought)

The face gets all the attention and then people pick a stock voice that sounds like an airport
announcement. Viewers forgive an imperfect face; they don't forgive a robotic voice.

**Options, best to worst:**

1. **Clone a real voice** (Lee's, or a paid VO artist). Massively more natural. HeyGen's own Avatar V
   guidance: record a **separate, dedicated voice sample** rather than reusing audio from a video, and
   deliver it with varied emotional inflection — flat input, flat clone. Iterate until it's genuinely
   good, don't accept the first pass.
   - Recording: quiet room, soft furnishings, decent mic 15–20cm off-axis, 3–5 minutes of varied
     content (a statement, a question, an excited line, a calm explanation). No music, no room echo.
2. **A premium stock voice**, auditioned properly — Australian, mid-pace, warm. Not the default.

Then **lock the parameters**: voice ID, speed, pitch, pause behaviour. Write them into the spec card
in Step 10. A voice that's 5% faster in some videos reads as a different person.

**Pronunciation:** test "Craftons" immediately. Test "radius", "architrave", "CNC", "MDF", "formwork",
"Mornington", "Geelong". Anything it butchers goes in a pronunciation list — you'll fix them with
phonetic respelling in the script (write `CNC` as `C N C`, etc.).

---

## Step 8 — Pick the motion engine

| Engine | Credits | Best for |
|---|---|---|
| **Avatar III** | 3 / min | Cheap drafts, internal review cuts |
| **Avatar IV** | 20 / min | **Your default.** Best quality for *photo-based* avatars — which is what you have. |
| **Avatar V** | same per-min as IV | Best for *video-based* avatars / real-human clones. Needs a 15s reference video. Phase 2. |

Workflow that saves credits: **draft on Avatar III, final render on Avatar IV.** Script errors and
timing problems are visible at III quality; don't burn 20/min discovering a typo.

Note HeyGen's own split: Avatar V is better for real human avatars and video-based inputs; Avatar IV
is better for photo-based and virtual characters. You're photo-based, so IV is genuinely the right
tool, not a compromise.

---

## Step 9 — Torture-test before you commit

Do this **before** you build a content calendar around this face. One afternoon now, or thirty
inconsistent videos later.

Render the same 45-second script across **all** your locked looks, then review at 100% zoom, full
screen, sound on:

- [ ] **Identity hold** — pause on a frame from each look. Same person? Line them up side by side.
- [ ] **Lip sync on hard consonants** — plosives (p/b), f/v, and "th". Write the script with a few
      deliberately hard words.
- [ ] **Numbers and units** — "18mm", "2400 x 1200", "$1,450". These break TTS constantly.
- [ ] **Teeth** — the most common failure. Do they shimmer, change size, or merge?
- [ ] **Eyes** — blink rate natural? Or a dead stare / a rapid flutter?
- [ ] **Hands** — if visible, count fingers on multiple frames. Cut looks with hands if they misbehave.
- [ ] **Neck/shoulder seam** — a floating head on a static body is the giveaway. Half-body helps.
- [ ] **Background stability** — does anything behind them warp or breathe?
- [ ] **The 10-second test** — watch with fresh eyes. Does it feel like a person or a puppet? Trust the gut.

Fail any of these and fix it at the source: better base look, better images, retrain. Don't ship
around it.

---

## Step 10 — Lock the production spec card

This is what actually delivers consistency across "lots of videos." Not memory, not vibes — a card
you paste into every brief. Commit it to this repo once filled.

```
CRAFTONS PRESENTER — PRODUCTION SPEC v1        (locked YYYY-MM-DD)

Avatar name/ID:
Personal Model version:
Base look ID:
Approved look IDs:        1. studio ......
                          2. workshop ....
                          (etc.)
Voice ID:                 speed:        pitch:        pauses:
Motion engine:            Avatar IV (drafts: Avatar III)
Aspect ratios:            9:16 primary · 1:1 · 16:9
Avatar framing:           half-body, eyes on upper third, avatar occupies frame-LEFT
Safe zone:                frame-right 40% reserved for product/graphics
Background policy:        blurred real-workshop plate, never a busy AI scene
Caption style:            [font/size/position from design tokens]
Pronunciation overrides:  Craftons = ..., architrave = ..., CNC = "C N C"
NEVER:                    hard hat / sunglasses in close-up, avatar >20s on screen
                          without cutaway, no hard sell, no emoji
```

---

## Tips & tricks — the things that separate good from uncanny

**Structural**

1. **Never let the avatar carry the whole video.** Best-in-class AI-presenter content is
   avatar for 3–6 seconds → cut to real footage / product render → back to avatar. The avatar is
   the connective tissue, not the content. This is also exactly what `QUALITY-DOCTRINE.md` demands:
   real leads, AI extends.
2. **Hook in ≤2.5s** and open with a pattern interrupt (doctrine, motion rules). Don't open on a
   static talking head — open on the cut piece, then reveal the presenter.
3. **Micro-cuts 0.4–1.2s early, then every 3–5s.** Cutting frequently also hides any single frame
   where the avatar glitches.
4. **B-roll over every weak moment.** If a two-second stretch of lip sync is soft, that's where the
   cutaway goes. You will never be caught.

**Visual**

5. **Blur the background hard.** Shallow depth of field is your best friend — it removes the
   background-warping tell entirely and reads as a real 50mm lens.
6. **Composite over a real plate where you can.** Export the avatar on a clean/removable background
   and place them over actual Craftons workshop footage. Real background + synthetic presenter beats
   fully-synthetic every time, and it's on-doctrine.
7. **Add grain and a subtle camera move.** A dead-still frame screams AI. A 2–4% slow push-in over
   the clip plus light film grain does an absurd amount of work for how easy it is.
8. **Keep the eye-line consistent.** Same height, same angle across looks, or cuts between looks feel
   like different shoots.
9. **Consistent colour grade across every look.** One LUT, applied to all. Colour consistency reads
   as identity consistency even more than facial features do.

**Audio**

10. **Never leave pure TTS on silence.** Add room tone, a quiet music bed, and sound design on
    transitions — doctrine calls this the cheapest premium upgrade and it's true.
11. **Write for the mouth, not the eye.** Short sentences. Contractions. Commas where you want a
    breath. Read the script aloud first — if you stumble, the avatar will.
12. **Spell out anything technical.** `18 mil` not `18mm` if the TTS mangles it. Numbers as words
    where pacing matters.
13. **Vary the pace deliberately** — write in a short punchy line after a long one. Uniform pacing is
    the audio equivalent of a dead stare.

**Operational**

14. **Draft cheap, finish expensive.** Avatar III for script/timing approval, Avatar IV for the render.
15. **One person approves every output** (doctrine Gate 2). Generate 3, ship 1.
16. **Keep a rejects folder with notes.** "This prompt gave six fingers", "this look drifts at
    three-quarter angle." Compounding quality comes from writing down failures.
17. **Re-audition the avatar every ~20 videos.** Watch three old ones back to back with a new one.
    Drift is invisible day to day and obvious across months.
18. **Disclose it.** Don't present a synthetic person as a real Craftons employee. A presenter is
    fine; a fake estimator named Dave who customers think they can ring is a trust liability.

---

## What I need from you next

1. **The character bible** (Step 1) — or tell me the vibe and I'll draft it.
2. **The image set** — drop them in and I'll run the Step 3 rubric image by image: keep / cut /
   regenerate, plus the prompt change needed for each regenerate.
3. **Confirmation on Path A** (synthetic presenter) vs cloning a real face.

Don't spend credits on training until the set clears the gate.

---

## Sources

- [Personal Model — train your model to create better looks (HeyGen Help)](https://help.heygen.com/en/articles/14896977-personal-model-train-your-model-to-create-better-looks)
- [How to get started with Photo Avatars (HeyGen Help)](https://help.heygen.com/en/articles/10034438-how-to-get-started-with-photo-avatars)
- [Avatar V is now available on HeyGen (HeyGen Help)](https://help.heygen.com/en/articles/14602974-avatar-v-is-now-available-on-heygen)
- [How to get the best results with Avatar V (HeyGen Help)](https://help.heygen.com/en/articles/14602997-how-to-get-the-best-results-with-avatar-v-in-heygen)
- [Avatar Looks Explained (HeyGen Help)](https://help.heygen.com/en/articles/9964694-avatar-looks-explained)
- [Generate Looks: change your avatar's outfits and surroundings (HeyGen Community)](https://community.heygen.com/public/resources/generate-looks-photo-avatars)
- Internal: `QUALITY-DOCTRINE.md`, `CONTENT-PILLARS.md`, `SOCIAL-VOICE.md`
