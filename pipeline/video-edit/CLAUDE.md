# Craftons reel editing — instructions for the LOCAL Claude Code session

> **You are running on Lee's desktop, not in a cloud session.** CapCut is installed here.
> Lee does not know CapCut. He directs by prompt; you do the editing. Assume he cannot fix
> your mistakes by hand — if something needs a manual step, say so explicitly and tell him
> exactly where to click.

**Who's who:** Jake is on camera. Lee runs the edit and prompts you. Tia shoots and edits her
own site footage separately — that does not come through this pipeline.

---

## 1. Hard rules — these are not preferences

1. **No AI-generated footage or images. Ever.** Real footage leads. B-roll is CAD screengrabs
   and on-site footage only. A builder spots fake instantly, and the real workshop is Craftons'
   single biggest content advantage over competitors who can only show finished rooms.
2. **A human approves every output.** Never publish. Render, then show Lee.
3. **Never invent a fact about a product.** Radius, material, lead time, price — if it isn't in
   the transcript or Lee's prompt, ask. Wrong specs cost real money on site.
4. **Captions must match what Jake actually said.** Fix transcription errors, never "improve"
   his words.

---

## 2. The look

Pulled from `pipeline/tokens.css` and `.claude/skills/craftons-design/BRAND.md`.

| | |
|---|---|
| Primary | `#194431` deep forest green |
| Dark panels | `#0a1c14` · pure black `#000000` |
| Line accent (on dark) | `#2d8a5b` |
| Text | `#0e0e0c` near-black · `#ffffff` white |
| Neutrals | **warm ramp, no blue cast** |
| Display font | Aeonik → fallback Space Grotesk |
| Condensed / spec stamps | HWT Artz → Big Shoulders Display → Anton |
| Mono / numbers | JetBrains Mono |
| Body | Inter |
| Radius | 6px default |

**No gradients on UI surfaces. No emoji. Ever.**

---

## 3. Caption style

- **Font:** Inter SemiBold, or Big Shoulders Display for emphasis words
- **Case:** sentence case. Not all-caps — Craftons is builder-to-builder, not shouty
- **Colour:** white with a subtle dark shadow, or near-black on light footage
- **Highlight:** key term in `#2d8a5b`. **One highlighted term per caption group, maximum**
- **Position:** see safe zones below. Default is centred, sitting just above the bottom unsafe band
- **Grouping:** 3–5 words per card. Long lines kill retention
- **Timing:** captions land **on** the word, never behind it. If the transcript timing drifts, fix it

---

## 4. Safe zones — 9:16, 1080×1920

Meta consolidated Stories and Reels into one safe zone in March 2026:

| Edge | Unsafe | Pixels |
|---|---|---|
| Top | 14% | ~270px |
| Sides | 6% each | ~65px |
| Bottom | up to 35% | ~672px |

**Central safe area is roughly 950×978.** Nothing that must be read goes outside it.

In practice: **keep captions and the spec stamp out of the bottom 672px.** That band holds the
caption text, like/comment/share buttons and audio attribution. Put captions in the lower-middle
third instead — above the unsafe band, below Jake's face.

---

## 5. Trade vocabulary — Whisper gets these wrong every time

Check and correct every one of these after transcription:

`Radius Pro` · `Rip Pro` · `Craftons` · `formply` · `formwork` · `architrave` · `chord length` ·
`set-out` (not "setout" or "set out") · `bendy ply` · `MDF` · `Woodtron` · `cavity batten` ·
`perf panel` · `NCC` · `plywood` · `laminate` · `spoilboard` · `Fairfield`

**Numbers and units matter most.** "900mm radius", "17mm formply", "R900", "2400 × 1200".
Whisper mangles these constantly — mishearing a radius is worse than any other error this
pipeline can make.

---

## 6. Voice, for any text you write

From `SOCIAL-VOICE.md` and `BRAND.md`:

- **Builder-to-builder.** Written by someone who's been on site. Explain *why it matters*, not
  *what it is*
- **No em dashes.** Not in captions, not in title cards
- **Never the word "precision"**
- **Australian spelling**
- Trade language: *formply, radius, chord length, set-out* — not marketing language
- "We" = Craftons, "you" = the builder. Never "the customer"
- Dry humour is fine. Hype is not
- **Value-first:** ~85% of content teaches and barely mentions the brand. Soft CTAs only, no hard sell

---

## 7. The standard edit

Unless Lee says otherwise, every talking-head reel gets:

1. **Transcribe** — `python transcribe.py <file>`, then fix the vocabulary in §5
2. **Cut** — remove silences over 0.5s, filler words, and false starts. When Jake says a line
   twice, keep the better take (usually the second)
3. **Hook** — the first 1.7 seconds decide everything. If the opening line is weak, tell Lee and
   suggest an alternative from later in the transcript. Don't silently rearrange
4. **Captions** — §3 style, §4 placement
5. **B-roll** — cut to the CAD screengrab or site footage at the moment Jake names the thing.
   Only from the folder Lee points you at
6. **Spec stamp** — where a real radius or material is mentioned, overlay it (§8)
7. **Endcard** — 1.5s, Craftons logo on `#194431`, soft CTA
8. **Export** 1080×1920, H.264, then **show Lee and stop**

---

## 8. The spec stamp — the one thing nobody else has

When Jake names a real job spec, stamp it: `R900 · 2400mm · 17mm formply`

Condensed face, mono for the numbers, `#194431` panel or white on dark footage, sitting in the
central safe area. This is Craftons' signature move — the thing that makes the content
unmistakably theirs and is impossible for a competitor to fake, because it comes off a real job.

**Only ever use real figures.** Never a plausible-looking placeholder.

---

## 9. When to stop and ask

- The hook is weak and you'd need to restructure
- A spec is ambiguous in the transcript
- Footage is unusable — audio inaudible, badly out of focus
- An edit would change Jake's meaning
- You're about to do something that takes more than ~10 minutes of compute

**You cannot judge whether the result is good.** You can't watch the output. Render it, describe
what you did, and let Lee look. If he says it feels off, believe him — his eye beats your
reasoning about the edit, every time.
