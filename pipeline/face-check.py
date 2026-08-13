#!/usr/bin/env python3
"""Score a candidate frame's face against Harry, and build a side-by-side to eyeball.

Face consistency is the one thing that has to be right, and eyeballing it across
thirty frames is exactly the kind of judgement that drifts. This puts a number on
it: ArcFace (buffalo_l) embeddings, cosine similarity against the approved hero.

    python3 face-check.py <hero.png> <candidate.png> <compare-out.jpg>

Prints PASS/BORDERLINE/FAIL and the score, and writes a side-by-side face crop.
Exit code is 0 on pass, 1 otherwise, so a generate loop can gate on it.

Thresholds are calibrated on this reference, not universal. Same-person pairs
score high when the head is square to camera and drop as it turns — pose costs
similarity even when the identity is identical — so a profile is judged against a
looser bar than a front-on shot rather than being failed for being a profile.
"""
import sys, os, warnings
warnings.filterwarnings("ignore")
os.environ.setdefault("ORT_LOGGING_LEVEL", "3")

import numpy as np, cv2, insightface
from PIL import Image

HERO, CAND, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

# Front-on and three-quarter frames should land high; near-profiles legitimately
# sit lower because the far side of the face is hidden from the embedder.
PASS_FRONT, PASS_PROFILE = 0.75, 0.62
YAW_PROFILE = 25.0  # degrees of head turn beyond which the looser bar applies

_app = insightface.app.FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
_app.prepare(ctx_id=-1, det_size=(640, 640))


def biggest_face(path):
    img = cv2.imread(path)
    if img is None:
        raise SystemExit(f"could not read {path}")
    faces = _app.get(img)
    if not faces:
        return None, None, img
    f = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
    return f.normed_embedding, f, img


def face_crop(img, face, size=520):
    """Square crop around the face with headroom, so both sides compare like for like."""
    x1, y1, x2, y2 = face.bbox
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    half = max(x2 - x1, y2 - y1) * 0.95
    l, t = int(max(0, cx - half)), int(max(0, cy - half))
    r, b = int(min(img.shape[1], cx + half)), int(min(img.shape[0], cy + half))
    rgb = cv2.cvtColor(img[t:b, l:r], cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb).resize((size, size), Image.LANCZOS)


he, hf, himg = biggest_face(HERO)
ce, cf, cimg = biggest_face(CAND)
if he is None:
    raise SystemExit("no face found in the hero — wrong file?")
if ce is None:
    print("FAIL  no face detected in the candidate")
    sys.exit(1)

score = float(np.dot(he, ce))
yaw = abs(float(cf.pose[1])) if getattr(cf, "pose", None) is not None else 0.0
bar = PASS_PROFILE if yaw >= YAW_PROFILE else PASS_FRONT
verdict = "PASS" if score >= bar else ("BORDERLINE" if score >= bar - 0.05 else "FAIL")

sheet = Image.new("RGB", (1060, 560), "white")
sheet.paste(face_crop(himg, hf), (10, 30))
sheet.paste(face_crop(cimg, cf), (530, 30))
sheet.save(OUT, quality=94)

print(f"{verdict}  score {score:.3f}  (bar {bar:.2f}, head turn {yaw:.0f}deg)  -> {OUT}")
sys.exit(0 if verdict == "PASS" else 1)
