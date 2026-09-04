# Reel process — phone clip + screen recording → Instagram + Facebook

_Written after the first Radius Pro reel (2026-09-04). This is the process; `pipeline/video/` is the tooling.
Read this first, then run the steps. Rough time: 45–60 min of session time for a 3–4 min take, most of it renders._

**Control model (unchanged):** Claude cuts and drafts → Lee reviews on the phone → Lee posts. Nothing auto-publishes.

---

## 0. Before you record (Lee, 5 min) — this is where most of the effort is saved

- [ ] **Record the screen in a portrait browser window.** Drag Chrome to roughly 720×1280 before hitting record.
      The app reflows to one column and the recording is already 9:16, so Instagram and Facebook get the same
      full-frame file and there are no bands to hide. (The first reel used a 902×1128 landscape-ish window,
      which forced a 4:5 edit and a padded 9:16 for Facebook.)
- [ ] **Start the screen recording first, then the phone.** Any order works — the sync is found from audio —
      but both must be rolling for the whole take, and the screen recording must have its mic on.
- [ ] **One clap or desk tap** at the start, in view of both. Not required (the cross-correlation locked at
      0.94 without it) but it makes the sync check trivial.
- [ ] **Phone framing:** 1080×1920, you in the lower two-thirds, plain wall. Headroom gets cropped anyway.
      Keep the shirt logo in frame — it does the branding.
- [ ] **Talk in sentences.** The cut removes every pause over 0.6 s and every "um". Restarts stay in unless
      asked for, so if you fluff a line, pause, then say the whole sentence again — the pause becomes the cut point.
- [ ] **Say the numbers the way you want them captioned.** Captions are the transcript. "Two point four metre
      sheet", "form ply", "accept quote" all came out wrong first time and were fixed by hand.
- [ ] **Keep the take under ~2:30.** Instagram is fine longer; Facebook Reels limits vary by account.

## 1. Hand-over (Lee, 2 min)

1. Upload both files to Drive `Peninsula Studio/01 Craftons/Marketing/Video/` (phone `.MOV` + screen `.mp4`).
2. Set **both** to *Anyone with the link → Viewer*. Without this the session gets a Google sign-in page.
   The Drive connector can read the file list but cannot pull video (it base64-encodes through the chat).
3. Tell the session: the two filenames, the layout you want, and anything to snip.

## 2. Pull + cut (Claude, ~10 min)

```bash
# scratchpad, not the repo
ID=<drive file id>   # from the Drive connector's search_files
curl -sSL -o phone.MOV "https://drive.usercontent.google.com/download?id=$ID&export=download&confirm=t"
pip install imageio-ffmpeg faster-whisper fonttools    # ffmpeg ships in the wheel; no apt needed
python3 pipeline/video/jumpcut.py phone.MOV cut/phone-cut.mp4 --preview
```
- `jumpcut.py` = ffmpeg `silencedetect` (−35 dB, ≥0.6 s, 0.12 s handles) + faster-whisper **medium** with a
  filler prompt → cut list → render + `phone-cut.cut-sheet.txt` (keep-list in source seconds).
- Send Lee the `--preview` file (540×960, ~6 MB) straight away. Don't wait for the composite.
- **Proofread the transcript now** (`phone-cut.words.json`): Australian spelling, trade words, product names.
  Fix in the JSON before captions are built. Known misses: metre/millimetre, form ply, accept/except, "2 .4".

## 3. Sync the screen recording (Claude, ~5 min)

Cross-correlate the two audio envelopes (100 Hz log-envelope, FFT) — the one-liner is in `STATUS.md`
history / the 2026-09-04 session; a score ≥0.9 means locked. Then apply the same keep-list shifted by the
offset to the screen recording (`select=between(t,in+OFF,out+OFF)` per segment, `-r 30`).

Check for **page-loading flashes** (a new tab opening shows a dark grey frame for ~1.5 s). Find them with
`signalstats` YAVG per frame; hold the previous frame over them with `FREEZE=first:last:replace` in
`compose-reel.sh`.

## 4. Compose (Claude, ~5 min per render)

```bash
# avatar: tight 9:16 head-and-shoulders. 1080x1920 phone clip → crop=742:1320:249:600 worked; check a frame.
ffmpeg -i cut/phone-cut.mp4 -vf crop=742:1320:249:600 -c:a copy cut/avatar.mp4
python3 pipeline/video/captions-highlight.py cut/phone-cut.words.json cut/caps.ass      # BOX=0 HL=linegreen is the chosen look
FREEZE=4044:4086:4043 bash pipeline/video/compose-reel.sh full4x5 cut/screen-cut.mp4 cut/avatar.mp4 out/reel-ig.mp4 cut/caps.ass
FB916=1 bash pipeline/video/compose-reel.sh full4x5 cut/screen-cut.mp4 cut/avatar.mp4 out/reel-fb.mp4 cut/caps.ass
```
If the screen was recorded portrait (step 0), use / add a `full9x16` layout instead and skip `FB916`.

**Locked layout decisions (don't re-litigate):**
- 4:5 full-bleed for a landscape-ish screen recording; white pad, never green bands.
- Screen crop = full browser viewport width (Chrome tab/address/bookmark bars and side panel removed, no side
  trim). Wide pages like the quote sheet get clipped by any side trim.
- Avatar: small, bottom-left, rounded corners, no border. 260×462 on a 1080×1350 frame.
- Captions: Inter Bold 84 px, Craftons green, 2 lines × 2 words, spoken word in line green, no box, centred,
  bottom at y=1190 (above the Reels username/caption overlay). `RAISE=t:px` lifts the block over on-page
  buttons (the quote page's *Accept Quote*).
- Captions were the most-iterated part (8 rounds). Start from the locked style; only change what Lee names.

## 5. Review loop (Lee on the phone, Claude renders)

- Always send: a **contact sheet** or 3-up of stills at the changed spots, then the file. Stills first — they
  catch layout problems without a 3-minute render.
- Chat upload cap is **30 MiB**. crf 19 on this kind of content is ~16 MB for 2:30. If a file is bigger,
  2-pass at ~1250 kbps.
- Re-transcribe the finished cut and read it through — that's how clipped words are caught.
- Typical notes from the first reel, so they're anticipated: avatar overlapping a UI button → move/shrink it;
  captions covered by the platform overlay → raise them; caption spelling; a page clipped by the crop.

## 6. Deliver + file (Claude, 5 min)

1. Send the IG file (4:5 or 9:16) and the FB file (9:16). Say which is which.
2. Draft the caption from `SOCIAL-VOICE.md` + the `craftons-voice` skill: hook = the tension the video opens
   on; every claim must be something said or shown in the video; soft CTA; ≤8 hashtags below the fold;
   no emoji. Offer three (overview / short / numbered). Lee edits; record **Lee's edit** as the final.
3. Write `campaigns/social/YYYY-MM-<reel>.md`: video spec, lane, the final caption, notes.
4. Add a line to `STATUS.md` (achieved + gotchas). Commit and push.
5. **Remind Lee to save the MP4s** — the session disk is wiped. Re-running the pipeline is ~15 min if lost.

---

## Learnings from reel 01 (so they aren't relearned)

| What happened | What to do instead |
|---|---|
| Screen recorded in a landscape-ish window → 4:5 edit + padded 9:16 for FB | Record the screen in a portrait window (step 0) |
| Side trim on the screen crop clipped the quote sheet | Never trim the viewport sides; pad instead |
| Whisper spelled "form ply" as "form plier", US spellings, "2 .4" | Proofread `words.json` before captions |
| Two-word captions felt frantic | 2×2 stacked block is the locked default |
| Captions at the bottom got covered by the IG/FB overlay | Bottom of text at y=1190 on 1350 (≈ 77 % down on 9:16) |
| Green box behind the live word felt heavy | Colour-only highlight (line green), no box |
| Avatar overlapped *Add another part* | Small avatar, bottom-left |
| New-tab loading flash (grey) in the screen recording | `FREEZE=` in compose-reel.sh |
| Drive file not link-shared → sign-in page | Step 1.2 |
| `freezeframes` + `split` in one ffmpeg graph asserts | Freeze is a pre-pass (already in the script) |
| pgrep-based wait loops match themselves | Wait on the task notification or a sentinel line |
