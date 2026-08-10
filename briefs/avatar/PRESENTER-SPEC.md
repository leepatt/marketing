# Craftons Presenter v1 — production state (2026-08-10)

## Status
- **Face LOCKED** (Lee approved 2026-08-10): "podcast guy" — blue-grey eyes, dark swept-back hair,
  short trimmed beard, mid-30s. Anchor = `hero-master.png` (this folder). Never regenerate the face
  independently; every new image derives from this master.
- **Training set BUILT + QC'd**: 29 frames (master + 28), delivered to Lee as
  `craftons-presenter-v1_training-set-part1.zip` (q95 JPEG). PNG masters were session-local;
  the recipe to regenerate is `genbatch.py` + `manifest.json` (identity from hero-master).
- QC: 5-reviewer workflow pass, per-image verdicts in `qc-results.json`. 8 flagged images were
  fixed (3 regens, 5 targeted edits) and re-verified.

## Wardrobe roster (locked)
work kit (black puffer vest + khaki shirt) · khaki shirt only · black hoodie · white tee ·
green crewneck (PLAIN for training) · navy wool overshirt

## Hard rules encoded in the pipeline
- NO logos/text in any training image (real Craftons SVG composited at the LOOK stage, post-training;
  logo files live in Drive: `craftons-logo-white.svg` etc.)
- NO AI-generated construction sites/formwork — real site photos as background plates only
- Base-look / non-"talking" frames: mouth closed, no teeth
- Generation: google/nano-banana (identity: hero-master as image 1) + real-esrgan 2x
  via Replicate (`REPLICATE_API_TOKEN`)

## Next steps
1. HeyGen: Avatars → New Avatar → upload base look (`craftons-presenter-v1_heygen-baselook.png`) →
   name `Craftons-Presenter-v1`
2. Generate Looks panel → Personal Model toggle → upload all 29 frames → Train (60 credits, paid plan)
3. After training: build 6-8 canonical looks; composite real logo onto look stills for branded looks
4. Voice: clone or premium AU stock; test "Craftons, architrave, CNC, MDF, formwork, Mornington, Geelong"
5. Worksite images: ON HOLD until Lee re-sends real site photos (originals never reached the
   session transcript) — use them as background plates
6. Full guide: `briefs/heygen-avatar-build-guide.md` + artifact
   https://claude.ai/code/artifact/bace1853-75f1-4ce4-91d3-0182aa99296c
