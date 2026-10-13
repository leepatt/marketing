# Video captions: one style and font for every Craftons video

_Research + options, 2026-10-13. For Lee to pick from. Mockups in `research/assets/2026-10-video-captions/`._
_Companions: `research/2026-caption-styles.md` (on branch `claude/radius-pro-instagram-edit-62mac9`),
`.claude/skills/craftons-design/BRAND.md`, `SOCIAL-VOICE.md`._

![Options side by side](assets/2026-10-video-captions/options-contact-sheet.jpg)

---

## 1. The problem: three caption styles are in use, and none of them uses the brand font

Every branch was searched before writing this. Craftons videos currently run three different caption styles:

| Where | Caption style | Font |
|---|---|---|
| Radius Pro reel 01 + Formwork Builder reel v2 (`pipeline/video/captions-highlight.py`) | Craftons green text, paper outline, 2×2 word blocks, live word in line green | **Inter Bold** 84px |
| Desktop CapCut pipeline (`pipeline/video-edit/CLAUDE.md` §3, branch `claude/dreamy-fermi-gfqbdj`) | White text, dark shadow, one highlighted term per card | **Inter SemiBold** + **Big Shoulders Display** for emphasis |
| Meta ad statics (`cnccut-app` `content-engine/ads/`) | Social guide layout | **Aeonik Regular** + **Akkurat Mono Bold** (JetBrains Mono stand-in) |

The brand sources disagree with the first two:

- **Brand Guidelines May 26** (official PDF): *Logo & display* = **Aeonik Regular / Medium**. *Body & webfont* = Inter.
  *Secondary & contrast* = HWT Artz, Anton ("these can be changed"). Headlines are sentence case with a full stop
  (*Building Smarter Starts Here.*).
- **Residency Studios social guide** (`Craftons_BrandGuide_SocialLayouts01.pdf`, 27.07.2026): headlines are
  **Aeonik Regular, not Bold**, labels are **Akkurat Mono Bold in caps**, and the palette adds **sage `#dae6d2`**.
  Logo bottom-left, URL bottom-right in mono. This guide is for **organic posting**, which is where most of the videos go.
- Captions are display type laid over the image, so Aeonik is the right face. Inter is the web/body face. The
  "Inter everywhere" decision (2026-07-08, `FONTS.md`) was made for **web documents**, because Aeonik is licensed and
  not deployed on the site. A burned-in caption is pixels in a video, not a web font, so that reason doesn't apply here.
- Big Shoulders Display isn't a brand font. It's the fallback for HWT Artz on compliance stamps only.

The social guide arrived on 2026-08-03 and was applied to the ad statics only. The video pipeline was built
separately in September on Inter and never picked it up. The video captions are now the only Craftons surface that
still shouts in Inter Bold.

## 2. What is NOT being re-pitched

On 2026-09-04 Lee rejected five caption add-ons as "really bad": hook title card + step counter, UI callouts,
editorial lower-third, knockout opener, black live-word highlight. **None of those come back here.** This doc only
changes the **base caption**: font, colour and how it sits on the footage. The approved mechanics stay:
word-synced timing, colour-only live word, sentence case, no box *behind the live word*.

## 3. What the research says (short version)

- **Most Reels play muted**, so captions carry the video. Sources put it between 60% and 85%. Captions are not optional.
- **Two families of style.** Word-by-word karaoke in a heavy sans suits talking heads. Clean sentence captions suit
  product and premium content, because they don't fight the picture ([Blitzcut](https://blitzcutai.com/blog/best-caption-style-instagram-reels-2026),
  [OpusClip](https://www.opus.pro/blog/instagram-reels-caption-subtitle-best-practices)). Craftons does both, so the
  system needs one look that works for both.
- **Bouncing and popping word animation hurts legibility** and reads cheap. Restraint is the premium move (also what
  July, Bellroy and Gozney do: `inspiration/SWIPE-FILE.md`).
- **Line length** around 32–42 characters, two lines max. **Text height** up to ~6% of a vertical screen. **Medium to
  bold weights** hold up on busy, moving backgrounds ([syllaby](https://syllaby.io/blog/subtitle-styling-burn-in-caption-timing-guide/),
  [subanana](https://subanana.com/en-HK/blog/four-points-to-note-when-creating-video-subtitle)). Honest caveat:
  the one peer-reviewed paper found ([Gerber-Morón et al. 2020](https://uvadoc.uva.es/bitstream/10324/48376/3/revistas_uva_es__hermeneus_article_view_1737_3726.pdf))
  says these numbers haven't been properly tested on phones. Treat them as working rules, not science.
- **Brand font + brand colour** is what separates "built" accounts from "assembled" ones. Default CapCut yellow is
  the assembled look.
- **Safe zone (Meta, 2026):** keep readable text out of the bottom ~672px and top ~270px of 1080×1920, and ≥65px
  from the sides.

## 4. The test that decided it

All options were rendered over the **Lawless curved wall photo**, which ran in the best-performing ad in the account.
Bright timber, hard shadows and blue sky make it a worst case for captions. Approximate Reels UI is drawn in so the
safe zone is visible.

![Close-up of A, C, D](assets/2026-10-video-captions/options-closeup.jpg)

What it showed:

1. **Floating text (no plate) struggles on real site footage**, even in Aeonik with a soft shadow and scrim. Bright
   timber eats it.
2. **Dimming the words not yet spoken** (a common "premium" karaoke trick) **disappears completely** on busy footage.
   Tested and dropped.
3. **A solid green plate is the most readable, and the most Craftons.** It's the same colour and 6px corner radius as
   the website buttons. Paper on green is **9.7:1 contrast** (AAA). It works on any footage without per-shot tweaking.
4. **Sage as the live-word colour is subtle** next to paper text (similar brightness, different hue). It reads as calm
   rather than flashy, which matches the line-green highlight Lee picked in September. It's easy to strengthen if wanted.

Contrast figures (WCAG): paper on green 9.7 · sage on green 8.5 · green on sage 8.5. The current style has no
plate, so its readability depends entirely on a 3px outline.

## 5. The options

| | Look | Font | Strength | Weakness |
|---|---|---|---|---|
| **Now** | Green text, paper outline, 2×2 words | Inter Bold 84 | Approved, familiar | Off-guide font and weight; outline text looks dated; muddy on timber |
| **A · Floating Aeonik** | Paper text, soft dark halo, live word sage | Aeonik Medium 76 | Most editorial; nothing covers the picture | Weakest on bright or busy footage |
| **B · Green plate** | Paper text on a Craftons-green plate, live word sage | Aeonik Regular 70 | Readable on anything; matches site buttons; guide-correct weight | A box. September's *per-word* box felt heavy, but this is a calm line plate, not a flashing box |
| **C · Plate + spec chip** ⭐ | B, plus every spoken **measurement or material** set as a mono caps chip (`R900`, `17MM`, `2400 × 1200`) | Aeonik Regular + Akkurat Mono Bold | Same as B, plus a device nobody else in the category has. The spec reads at a glance with sound off | Needs the chip rule applied consistently, which is easy to automate from the transcript |
| **D · Sage plate** | Green text on a sage plate | Aeonik Medium 70 | Lighter, softer feel; good on dark or green-heavy shots | Lighter plate stands out more on bright footage |
| **Endcard** | Social guide grid: mono label, Aeonik Regular headline, logo bottom-left, URL bottom-right in mono | Aeonik + mono | Ties every video back to the posting system | — |

## 6. Recommendation: C as the standard, A as the quiet exception

**Use C on every video that has talking or a screen demo.** Use **A** only on Craft Macro and other calm, clean shots
that carry at most one line of text. Use **D** only when the footage itself is green or very dark. Same font, same
colours and same position everywhere, so every Craftons video looks like it came from one shop.

### The spec (for `captions-highlight.py`, the CapCut instructions and Remotion)

| Setting | Value |
|---|---|
| Font | **Aeonik Regular** (Medium only in option A) |
| Size | **70px** at 1080 wide (~3.6% of frame height, ~6.5% of width) |
| Line height | 1.2 |
| Case | Sentence case. Full stop at the end of a sentence. No ALL CAPS except chips |
| Text colour | Paper `#f4f1ea` |
| Plate | Craftons green `#194431`, **6px radius** (`--r-md`), padding 8 / 26 / 12px, one plate per line |
| Live word | Sage `#dae6d2`, colour only, no box, no scale, no bounce |
| Spec chip | **Akkurat Mono Bold**, caps, 0.74× caption size, green `#194431` on sage `#dae6d2`, 6px radius. **Only numbers with units and material codes** (R900, 17MM, 2400 × 1200, 34MM). Never product names or ordinary words |
| Card length | **3–7 words**, broken at natural pauses, **max 2 lines, ~26 characters per line** |
| Position | Centred. **Bottom of the plate at y≈1230** on 1920 (clear of the bottom 672px). ≥70px side margins |
| Motion | Cut in on the first word, no entrance animation (an 80ms fade at most). Lands **on** the word, never behind it |
| Never | Emoji, em dashes, outline text, drop-shadow-only text on busy footage, Inter or Big Shoulders in captions |

### What changes in practice
1. `pipeline/video/captions-highlight.py`: swap Inter Bold for Aeonik Regular, draw a rounded green plate per line
   (the script already has `rrect()`), live word to sage, add a chip pass for number+unit tokens, raise the block to
   y≈1230 on 9:16. About an hour of work.
2. `pipeline/video-edit/CLAUDE.md` §3 (desktop CapCut): replace the Inter SemiBold / Big Shoulders spec with the table
   above, so desktop and cloud edits match.
3. Remotion `SpecStamp` and the endcard: same fonts and colours, endcard on the social guide grid.
4. Put Aeonik `.otf` in the local pipeline font folders. **Don't commit it to git**: it's licensed, and it lives in
   Drive `Design-system/fonts/`.

## 7. Decisions / checks for Lee

1. **Pick: C (recommended), B, A or D**, or say "keep Inter" and only the plate and colour changes ship.
2. **Aeonik licence for video.** Aeonik is from CoType Foundry. Their terms weren't found online. Some foundries'
   desktop licences exclude video (Klim's does) or sell social/video as an add-on. **Check the Craftons Aeonik licence
   (or email CoType) before publishing.** If video isn't covered, the fallback is the same layout in Inter Medium.
   That loses some character but stays consistent.
3. **Akkurat Mono Bold** is still unlicensed. JetBrains Mono Bold stands in for it, here and in the ad batch. Same open item as August.
4. **Live-word strength.** Sage is subtle by design. If you want more punch, the next step is the sage word *plus* a
   2px sage underline. Still no box.

## Sources
- Blitzcut, best caption style for Reels 2026: https://blitzcutai.com/blog/best-caption-style-instagram-reels-2026
- OpusClip, Reels caption best practices 2026: https://www.opus.pro/blog/instagram-reels-caption-subtitle-best-practices
- Kapwing, Instagram subtitles guide: https://www.kapwing.com/resources/a-complete-guide-to-instagram-subtitles/
- Syllaby, subtitle styling + burn-in timing: https://syllaby.io/blog/subtitle-styling-burn-in-caption-timing-guide/
- Subanana, subtitle design 2026: https://subanana.com/en-HK/blog/four-points-to-note-when-creating-video-subtitle
- Gerber-Morón et al., *Hermēneus* 2020 (subtitle layout research gap): https://uvadoc.uva.es/bitstream/10324/48376/3/revistas_uva_es__hermeneus_article_view_1737_3726.pdf
- Klim desktop font licence (example of a video exclusion): https://klim.co.nz/licences/desktop-fonts/
- Fontwerk licensing (social/video modules): https://fontwerk.com/text/font-licensing-made-even-simpler
- Internal: Craftons Brand Guidelines May 26 (Drive `Design-system/uploads/`), social guide notes in `campaigns/meta/`
  (branch `claude/brand-check-launch-prep-jiyejg`), reel 01 record + `REEL-PROCESS.md` (branch
  `claude/radius-pro-instagram-edit-62mac9`), `pipeline/video-edit/CLAUDE.md` (branch `claude/dreamy-fermi-gfqbdj`).

_Mockup source: `assets/2026-10-video-captions/mockup-frame.html` (needs the Aeonik `.otf` files from Drive and the
background photo `Radius Pro wall plates.jpg` next to it; neither is committed)._
