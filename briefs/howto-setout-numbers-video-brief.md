# How-To Series: "The set-out numbers" — HyperFrames motion-graphic (brief, script, caption)

_Made 2026-09-11 with HeyGen's HyperFrames (HTML-to-video). First Craftons video produced end-to-end
in a session: written, rendered and QA'd here, nothing recorded. Lane: **How-To Series (Teach)**.
Source composition: `pipeline/video/hyperframes/howto-setout/`. Guardrails from
`campaigns/meta/radius-pro-product-truth.md`, `SOCIAL-VOICE.md`, `CONTENT-PILLARS.md`._

---

## 1. What it is, in one paragraph

A 29-second, 9:16, silent-safe motion graphic that teaches one real thing: **how to get a curved wall
plate onto the slab from the plan using chord and rise**, so nobody has to swing a 3.7 m trammel from
a centre point they can't reach. It is the locked How-To shortlist item **"How to calculate curved wall
plates from plans"** (`CONTENT-PILLARS.md` Lane 1), done as a diagram-driven explainer rather than a
talking head. Radius Pro appears once, at the end, as a soft creation line. No hard sell.

**Why this format for HyperFrames:** HyperFrames is not an avatar tool. It renders HTML/CSS/GSAP to
video, deterministically. That makes it the right tool for exactly the content the pillars say we lack
footage for: diagrams, numbers, set-out. Everything on screen is drawn from three numbers in code, so
the drawing and the labels can never disagree.

## 2. The job on screen (real numbers)

| Input (off the plan) | Value | Derived set-out number | Value |
|---|---|---|---|
| Internal radius | **R 3714** | Chord = 2R sin(θ/2) | **1923 mm** |
| Stud width | **90** | Rise = R(1 − cos θ/2) | **127 mm** |
| Segment angle | **30°** (0.5236 rad) | Arc = Rθ | **1945 mm** |
| Material | 17 mm formply | | |

R3714 and 90/17 mm formply come from the order data in `radius-pro-howto-video-brief.md` (branch
`claude/radius-pro-video-script-gitg6u`). The 30° segment is my choice so the plate fits a 2400 sheet.
**Lee to confirm the angle reads as a typical plate segment.**

## 3. Beat sheet (what's on screen when)

| Time | Scene | On screen |
|---|---|---|
| 0.0–4.0 | Hook, dark green, curved-line motif draws in | eyebrow `HOW-TO SERIES` · **The plan says R3714.** · *It doesn't say how to set it out.* |
| 4.0–10.4 | 01 / Off the plan, paper | **Three numbers off the plan.** Plan-view plate draws; callouts pop in order: `R 3714` → `90 wide` → `30°` |
| 10.7–22.5 | 02 / The set-out numbers, paper | **Chord and rise. That's your set-out.** Chord draws + `CHORD 1923` counts up · rise tick + `RISE 127` · arc highlight + `ARC 1945` · three body lines · formula strip |
| 22.5–29.0 | Payoff, dark green | **Or type the radius into Radius Pro.** · *Arc, chord and rise come back on their own. Plates turn up cut to size.* · *Save this for your next curved job.* · wordmark + craftons.com.au |

Body lines (chapter 02):
1. **Chord** is where the plate starts and ends.
2. **Rise** is how far it bows off the string line.
3. String the chord, mark the rise at the middle. Nobody is swinging a 3.7 metre trammel on a slab.

## 4. Guardrail check (done)

- Banned Radius Pro words (bog-and-sand, bogging, kerf, kerfing, curve bending, laminating, wiggle wood,
  bendy-ply-as-problem): **none used.**
- No "send us your plan / CAD". No joiner blocks. No waste percentage. No delivery-day number (2 vs 3
  is still open in `STATUS.md`, so the video says "cut to size" and nothing about days).
- Brand presence: no brand word until 22.5 s; one product line; soft CTA; wordmark small on the end card.
  ~78 % of runtime is pure teach.
- Voice: sentence case, no emoji, no em dashes in copy, trade words (chord, rise, set-out, string line,
  formply, stud, trammel).
- Works muted (designed silent). Contrast: 38/38 text checks pass WCAG AA (`hyperframes check`).
- Brand law 1 (big company, studio-clean or rendered only): it is fully rendered.

## 5. Instagram caption (draft, per `SOCIAL-VOICE.md`)

> The plan says R3714. It doesn't say how to set it out.
>
> Chord and rise are the two numbers that put a curved wall plate on the slab. String the chord, mark
> the rise at the middle, and the curve is located without swinging a 3.7 metre trammel from a centre
> point you can't get to.
>
> Radius Pro works those out the moment you type the radius in, and the plates turn up cut and engraved
> with their part IDs.
>
> Save this for your next curved job.
>
> #curvedwalls #curvedwallframe #setout #framing #carpentryaustralia #formply #radiuspro #BuiltWithCraftons

Alt hook lines: "Curved wall on the plans? Don't mark it out." · "Two numbers set out any curved wall
plate." · "Nobody is swinging a 3.7 metre trammel on a slab."

## 6. Decisions I need from Lee

1. **Episode number.** Pilot = angled backrest, Ep 2 = off-form screen (Drive storyboards). Where does
   this sit? The eyebrow currently just says `HOW-TO SERIES`; a number is a one-line change.
2. **Keep or cut the product line at the end** ("Plates turn up cut to size")? Cutting it makes it a
   purer Teach post; keeping it matches the how-to brief's Benefit beat.
3. **The 30° / R3714 example.** Happy with it, or give me a real plate off a recent order and I'll
   re-render with those numbers (every label is derived from the three inputs).
4. **Voice-over?** It is built silent-first. HyperFrames can add TTS or a recorded track; a 25-second
   read by Lee over the top would make it a proper How-To episode. Your call.
5. **Instagram handle** for the end card. I could not confirm it from the repo or Drive, so the end
   card shows the wordmark + `craftons.com.au`. Send the handle and I'll swap it in.
6. **HyperFrames connector.** The HyperFrames MCP connector is installed on this session but **not
   authorised** (it needs a HeyGen sign-in via claude.ai → Settings → Connectors). We do **not** need
   it to render, everything here ran locally. It only matters if you want hosted preview links or
   cloud renders. Authorise it once if that sounds useful; otherwise leave it.

## 7. Where things live

- Composition + re-render instructions: `pipeline/video/hyperframes/howto-setout/README.md`
- Rendered MP4 (v1): sent in-session; **save it to Drive `Marketing/Video/How-To-Series/`** (the
  connector cannot push video from a session, per `pipeline/video/REEL-PROCESS.md`).
- Nothing auto-publishes. Lee reviews on the phone, then posts via Later.
