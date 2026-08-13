#!/usr/bin/env python3
"""Generate ONE Harry frame at a time, as an edit of the approved hero.

    REPLICATE_API_TOKEN=... python3 harry-shoot.py <hero.png> <out-dir> <shot-number> [attempts] [seed-offset]

Shot numbers follow HARRY-SHOT-LIST.md (1-30). Default 4 attempts.

## Why best-of-N, and why the score alone cannot pick the winner

The same prompt at different seeds swings hard on likeness — one boxy-polo brief
scored 0.909, 0.892 and 0.640 across three seeds. A single roll is therefore a
coin toss, and re-rolling by hand until it looks right is exactly the judgement
that drifts over thirty frames. So each shot generates several candidates and
scores every one against the hero.

But picking purely on score is a trap: similarity is highest when the edit did
the least, so the top scorer is often the candidate that quietly ignored half
the brief. The first best-of-4 run proved it — the 0.907 winner had changed the
polo and left the room exactly as the hero's.

So a candidate must clear two gates, not one: the face has to match AND the
scene has to have actually changed. Room changes are verified by measuring how
much the background moved away from the hero, with the centre of frame masked
out so the subject himself does not count toward it.

## Why this is an edit, not a generation

Measured on this hero, against ArcFace similarity to the hero itself:

    kontext, clothes + room, everything else held           0.952
    kontext, framing only                                   0.921
    kontext, clothes + room, pose held                      0.893
    kontext, clothes + room + framing + expression          0.833
    nano-banana-pro, fresh scene, one reference             0.820
    nano-banana-pro, fresh scene, three references          0.775
    kontext, rotate to three-quarter                        0.693

Two findings, and the second matters more than the first.

nano-banana-pro rebuilds the scene from scratch, so it reconstructs the face
every time and drifts. flux-kontext-max edits the source, so the face survives.

But the bigger lever is how much each edit changes at once. Every axis you move
costs identity and the costs stack: two axes lands at 0.95, four at 0.83, and
0.83 is where a viewer stops seeing the same man. So shots change one or two
things, never four, and the set carries the variety rather than each frame.

Big camera rotations are out. Asked to turn him, the model either ignores it or
swings his head away and loses the face (0.693). That is the right trade for a
HeyGen avatar: it is trained on a talking head facing camera, so a consistent
front-facing face is worth more than a dramatic angle that is not him.
"""
import json, os, sys, time, urllib.request

TOKEN = os.environ["REPLICATE_API_TOKEN"]
MODEL = "black-forest-labs/flux-kontext-max"
HERO, OUT, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
ATTEMPTS = int(sys.argv[4]) if len(sys.argv) > 4 else 4
# Seeds are deterministic so a re-run reproduces the same candidates. Pass an
# offset to explore fresh ones without paying to regenerate the known ones.
SEED_OFFSET = int(sys.argv[5]) if len(sys.argv) > 5 else 0
os.makedirs(OUT, exist_ok=True)

# Prepended to every edit. The face clauses do the work; the texture clauses stop
# it quietly re-polishing him back into a stranger.
KEEP = (
    "Keep this exact man's face completely unchanged — same face shape, jawline, nose, "
    "mouth, blue-grey eyes, eyebrows, hairline and dark hair swept back the same way. "
    "Keep his real skin exactly as it is: visible pores, uneven complexion, crow's feet, "
    "forehead lines, sun freckling, small blemishes, and the short beard with grey "
    "scattered through it and at the temples. He is about forty and looks it. Do not "
    "smooth his skin, do not darken the grey, do not make him younger or better looking. "
    "He keeps looking toward the camera. His clothing carries no logo, wordmark, print "
    "or text of any kind. "
)

# Rooms, described as edits rather than scenes.
IN_LIVING = ("the room is a large open living area in a near-finished high-end Australian "
             "home, plastered walls, big windows, cardboard floor protection")
IN_KITCHEN = ("the room is the kitchen of a near-finished high-end home, stone benchtop and "
              "new timber cabinetry behind him, cardboard floor protection")
IN_HALL = ("he is in a wide hallway of a near-finished high-end home, doorways either side "
           "receding behind him, cardboard floor protection")
IN_STAIR = ("he is at the foot of a timber staircase in a near-finished high-end home, "
            "cardboard protection on the treads")
STUDIO = ("the room is a clean modern office with matte white walls, a warm timber desk and "
          "a few plants, no camera equipment anywhere")
OUT_FORM = ("he is outdoors on a residential building site, and clearly behind him is a "
            "curved concrete bench seat formed up ready to pour — bent plywood formwork held "
            "by timber stakes, steel reinforcement mesh inside the form, compacted ground")

VEST = "a black puffer vest over a short-sleeved khaki work shirt"
POLO = ("a plain black short-sleeved polo shirt in a boxy relaxed cut — roomy through "
        "the chest and body, square at the shoulder, sleeves loose on the upper arm, "
        "hanging straight rather than clinging. Not fitted, not tight, not muscle-fit")
JUMPER = "a plain black crew-neck jumper"
HOODIE = "a plain black hoodie with relaxed straight-leg blue jeans"
TEE = "a boxy relaxed plain white crew-neck t-shirt, roomy and square at the shoulder"
GREEN = "a deep forest green crew-neck jumper"
NAVY = "a thick navy overshirt, buttoned, over a plain tee"

# (slug, base, edit) — base is "hero" or the slug of an earlier shot.
#
# Every entry changes ONE or TWO axes from its base and no more. That is the whole
# design: measured on this hero, a two-axis edit scores 0.95 and a four-axis edit
# scores 0.83, and 0.83 is where it stops looking like the same man.
#
# Tier A (1-10) edits the hero directly, changing wardrobe and room together.
# Tier B (11-30) edits an approved Tier A frame, changing a single axis — framing,
# expression, camera height or light — so the variety compounds while each
# individual step stays small. Every frame is still scored against the hero, not
# against its base, so chained drift cannot creep past the gate.
SHOTS = [
    ("in-polo-kitchen", "hero", f"He now wears {POLO}, and {IN_KITCHEN}. Same framing, same camera position, same expression."),
    ("in-jumper-hall", "hero", f"He now wears {JUMPER}, and {IN_HALL}. Same framing, same camera position, same expression."),
    ("in-vest-stair", "hero", f"{IN_STAIR}. Same clothing, same framing, same camera position, same expression."),
    ("st-tee", "hero", f"He now wears {TEE}, and {STUDIO}. Same framing, same camera position, same expression."),
    ("st-hoodie", "hero", f"He now wears {HOODIE}, and {STUDIO}. Same framing, same camera position, same expression."),
    ("st-green", "hero", f"He now wears {GREEN}, and {STUDIO}. Same framing, same camera position, same expression."),
    ("st-navy", "hero", f"He now wears {NAVY}, and {STUDIO}. Same framing, same camera position, same expression."),
    ("out-vest-form", "hero", f"{OUT_FORM}. Same clothing, same framing, same camera position, same expression."),
    ("out-polo-form", "hero", f"He now wears {POLO}, and {OUT_FORM}. Same framing, same camera position, same expression."),
    ("out-jumper-form", "hero", f"He now wears {JUMPER}, and {OUT_FORM}. Same framing, same camera position, same expression."),

    ("in-polo-kitchen-speaking", "in-polo-kitchen", "Change only his expression: he is speaking to camera mid-sentence with his mouth open. Everything else identical."),
    ("in-polo-kitchen-close", "in-polo-kitchen", "Change only the framing: crop tighter to head and shoulders. Everything else identical."),
    ("in-jumper-hall-smile", "in-jumper-hall", "Change only his expression: a relaxed genuine smile. Everything else identical."),
    ("in-jumper-hall-low", "in-jumper-hall", "Change only the camera height: it sits a little lower, looking slightly up at him. Everything else identical."),
    ("in-vest-stair-listening", "in-vest-stair", "Change only his expression: attentive and listening, mouth closed. Everything else identical."),
    ("in-vest-stair-wide", "in-vest-stair", "Change only the framing: pull back wider with more room around him. Everything else identical."),
    ("st-tee-speaking", "st-tee", "Change only his expression: speaking to camera mid-sentence with his mouth open. Everything else identical."),
    ("st-tee-close", "st-tee", "Change only the framing: crop tighter to head and shoulders. Everything else identical."),
    ("st-hoodie-seated", "st-hoodie", "Change only his posture: he is now seated at the desk leaning slightly forward on his forearms. Everything else identical."),
    ("st-hoodie-smile", "st-hoodie", "Change only his expression: a warm open smile. Everything else identical."),
    ("st-green-close", "st-green", "Change only the framing: crop tighter to head and shoulders. Everything else identical."),
    ("st-green-high", "st-green", "Change only the camera height: it sits a little higher, looking slightly down at him as he looks up into the lens. Everything else identical."),
    ("st-navy-seated", "st-navy", "Change only his posture: he is now seated with his hands resting on the desk. Everything else identical."),
    ("st-navy-turned", "st-navy", "Change only his posture: his shoulders turn very slightly to his left while his face stays square to the lens. Everything else identical."),
    ("out-vest-form-speaking", "out-vest-form", "Change only his expression: speaking to camera mid-sentence with his mouth open. Everything else identical."),
    ("out-vest-form-wide", "out-vest-form", "Change only the framing: pull back wider so the whole formed-up bench seat is visible behind him. Everything else identical."),
    ("out-polo-form-low", "out-polo-form", "Change only the camera height: it sits a little lower, looking slightly up at him. Everything else identical."),
    ("out-polo-form-smile", "out-polo-form", "Change only his expression: an easy half smile. Everything else identical."),
    ("out-jumper-form-golden", "out-jumper-form", "Change only the light: warm golden-hour side light with long soft shadows. The jumper still reads clearly black, not brown. Everything else identical."),
    ("out-jumper-form-close", "out-jumper-form", "Change only the framing: crop tighter to head and shoulders. Everything else identical."),
]

if not 1 <= N <= len(SHOTS):
    raise SystemExit(f"shot number must be 1-{len(SHOTS)}")
slug, base, edit = SHOTS[N - 1]
dest = os.path.join(OUT, f"{N:02d}-{slug}.png")

if base == "hero":
    src = HERO
else:
    idx = next(i for i, sh in enumerate(SHOTS) if sh[0] == base)
    name = f"{idx + 1:02d}-{base}.png"
    # Approved frames get moved out of the candidates dir, so look there too.
    for d in (OUT, os.path.join(os.path.dirname(OUT), "approved")):
        if os.path.exists(os.path.join(d, name)):
            src = os.path.join(d, name)
            break
    else:
        raise SystemExit(f"shot {N} builds on shot {idx + 1} ({base}), which has not been "
                         f"generated yet — run and approve that one first")


def api(path, data=None):
    req = urllib.request.Request(
        f"https://api.replicate.com/v1{path}",
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def upload(path):
    b = "----harryshoot"
    body = b"".join([
        f'--{b}\r\nContent-Disposition: form-data; name="content"; '
        f'filename="{os.path.basename(path)}"\r\nContent-Type: image/png\r\n\r\n'.encode(),
        open(path, "rb").read(), f"\r\n--{b}--\r\n".encode()])
    req = urllib.request.Request(
        "https://api.replicate.com/v1/files", data=body,
        headers={"Authorization": f"Bearer {TOKEN}",
                 "Content-Type": f"multipart/form-data; boundary={b}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)["urls"]["get"]


def generate(seed, path):
    p = api(f"/models/{MODEL}/predictions", {"input": {
        "prompt": KEEP + edit,
        "input_image": src_url,
        "aspect_ratio": "match_input_image",
        "output_format": "png",
        "safety_tolerance": 2,
        "seed": seed,
    }})
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(3)
        p = api(f"/predictions/{p['id']}")
    if p["status"] != "succeeded":
        raise RuntimeError(p.get("error") or p["status"])
    o = p["output"]
    urllib.request.urlretrieve(o[0] if isinstance(o, list) else o, path)


# face-check.py has a hyphen in its name, so it cannot be imported by name.
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location(
    "face_check", os.path.join(os.path.dirname(os.path.abspath(__file__)), "face-check.py"))
_fc = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_fc)
compare = _fc.compare

src_url = upload(src)
tmpdir = os.path.join(OUT, ".attempts")
os.makedirs(tmpdir, exist_ok=True)

def bg_moved(path):
    """How far the background has travelled from the hero, subject masked out.

    Guards against the top-scoring candidate being the one that ignored the
    room change — similarity rewards doing nothing, so this has to be checked
    separately rather than trusted to the score.
    """
    from PIL import Image as _I
    import numpy as _np
    a = _np.asarray(_I.open(HERO).convert("L").resize((320, 180), _I.LANCZOS)).astype(float)
    b = _np.asarray(_I.open(path).convert("L").resize((320, 180), _I.LANCZOS)).astype(float)
    mask = _np.ones_like(a, bool)
    mask[:, 100:220] = False
    return float(_np.abs(a - b)[mask].mean())


# Shots whose brief moves the room have to show it in the pixels. Measured: a
# candidate that kept the hero's room scored 16.9 here, so the bar sits above it.
NEEDS_NEW_ROOM = base == "hero" and "the room is" in edit or "he is " in edit
BG_MIN = 25.0

def attempt(i):
    seed = 1000 + (i + SEED_OFFSET) * 137
    tmp = os.path.join(tmpdir, f"{N:02d}-seed{seed}.png")
    try:
        generate(seed, tmp)
    except Exception as e:
        print(f"  seed {seed}: generation failed — {e}", flush=True)
        return None
    return seed, tmp


from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as ex:
    produced = [r for r in ex.map(attempt, range(ATTEMPTS)) if r]

best = None
for seed, tmp in produced:
    verdict, score, yaw, bar = compare(HERO, tmp)
    bg = bg_moved(tmp)
    room_ok = (not NEEDS_NEW_ROOM) or bg >= BG_MIN
    flag = "" if room_ok else "  (room unchanged — rejected)"
    print(f"  seed {seed}: face {score:.3f} {verdict}   bg {bg:.1f}{flag}", flush=True)
    if not room_ok:
        continue
    if best is None or score > best[0]:
        best = (score, tmp, verdict, yaw, bar)

if best is None:
    raise SystemExit(
        f"no candidate cleared both gates in {ATTEMPTS} attempts — "
        "either the face never matched or the room never changed. Re-run with more "
        "attempts, or reword the shot if it keeps ignoring the room.")

score, tmp, verdict, yaw, bar = best
os.replace(tmp, dest)
for leftover in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, leftover))
os.rmdir(tmpdir)

compare(HERO, dest, os.path.join(os.path.dirname(OUT), "compare", f"{N:02d}-compare.jpg")
        if os.path.isdir(os.path.join(os.path.dirname(OUT), "compare")) else None)

print(f"shot {N:02d}  {slug}  best {score:.3f} of {ATTEMPTS}  {verdict}  -> {dest}")
sys.exit(0 if verdict == "PASS" else 1)
