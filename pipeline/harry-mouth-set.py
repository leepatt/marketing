#!/usr/bin/env python3
"""Build the mouth-training set HeyGen needs to stop inventing Harry's teeth.

    REPLICATE_API_TOKEN=... python3 harry-mouth-set.py <closeup.png> <out-dir> [attempts]

## The problem this solves

The first HeyGen render had a bad mouth: teeth as one flat white slab with no
individual teeth and no gaps, no lower teeth, no tongue, over-pink lips, and the
moustache smearing as the lips moved beneath it.

The cause is in what we supplied, not in HeyGen. Every frame we gave it had a
closed mouth, so it had never seen Harry's teeth and had to hallucinate a mouth
interior — and a beard makes the lip boundary the hardest region to inpaint.

Two things follow, and this script does both.

**Show it the real mouth.** These frames cover the shapes speech actually makes —
lips together, slightly parted, an open "ah", a wide "ee", a rounded "oo", and a
full smile — so the animator interpolates between references instead of guessing.

**Give it pixels.** In the export the head was 296px wide inside a 1920x1080
frame while the source we supplied was 776px. Working from a head-and-shoulders
crop instead of a waist-up frame roughly triples the share of the image spent on
the face, which is where all the detail that matters lives.

## On scoring these

Do not gate this set on ArcFace similarity. The metric reads facial geometry, and
an open mouth changes the lower face, so it penalises exactly the variation we
are trying to create — a real photograph of the same man mid-word scores about
0.7 against a closed-mouth reference. Judge these by eye.
"""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

TOKEN = os.environ["REPLICATE_API_TOKEN"]
MODEL = "black-forest-labs/flux-kontext-max"
SRC, OUT = sys.argv[1], sys.argv[2]
ATTEMPTS = int(sys.argv[3]) if len(sys.argv) > 3 else 2
os.makedirs(OUT, exist_ok=True)

# Identity clauses, plus the teeth description that the first render got wrong.
# "White teeth" is what produces the slab; real teeth need to be described as
# separate objects with their own colour and shadow.
KEEP = (
    "Keep this exact man's face completely unchanged — same face shape, jawline, nose, "
    "blue-grey eyes, eyebrows, hairline and dark hair. Keep his real skin: visible pores, "
    "uneven complexion, crow's feet, forehead lines, sun freckling, and the short beard "
    "with grey scattered through it. He is about forty and looks it. Do not smooth his "
    "skin or make him younger. Same room, same framing, same camera position, same "
    "head angle, looking straight into the lens. Clothing carries no logo or text. "
)
TEETH = (
    " Render the mouth realistically: individual separate teeth with visible edges and "
    "small natural gaps between them, slightly off-white and ivory rather than bleached "
    "or uniform, with natural shadow where they meet the gums and darker recession toward "
    "the back of the mouth. Lips are a natural muted colour, not bright pink or glossy. "
    "The moustache sits cleanly above the lip without smearing into it."
)

SHOTS = [
    ("m1-closed", "Change only his mouth: lips gently closed together in a neutral rest position, no smile, jaw relaxed."),
    ("m2-parted", "Change only his mouth: lips parted very slightly, a thin dark gap between them, jaw almost closed, the very edges of the upper teeth just showing."),
    ("m3-ah-open", "Change only his mouth: open in an 'ah' shape as if saying the word 'are', jaw dropped, upper and lower teeth both visible, tongue visible low in the mouth behind the lower teeth, dark recession at the back of the mouth."),
    ("m4-ee-wide", "Change only his mouth: a wide 'ee' shape as if saying the word 'see', lips stretched horizontally, upper and lower teeth close together and both clearly visible, corners of the mouth pulled back."),
    ("m5-oo-round", "Change only his mouth: lips pushed forward and rounded into a small 'oo' shape as if saying the word 'you', a small dark opening, teeth barely visible."),
    ("m6-smile-teeth", "Change only his expression: a warm genuine smile with upper teeth clearly visible and the corners of his eyes creasing naturally."),
    ("m7-mid-word", "Change only his mouth: caught mid-word in relaxed speech, jaw dropped a moderate amount, upper teeth visible and a hint of the lower teeth and tongue."),
    ("m8-f-v", "Change only his mouth: upper teeth resting lightly on the lower lip as when saying an 'f' or 'v' sound, mouth otherwise nearly closed."),
]


def api(path, data=None):
    req = urllib.request.Request(
        f"https://api.replicate.com/v1{path}",
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def upload(path):
    b = "----mouthset"
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


src_url = upload(SRC)


def run(job):
    slug, edit = job
    made = []
    for i in range(ATTEMPTS):
        seed = 700 + i * 313
        try:
            p = api(f"/models/{MODEL}/predictions", {"input": {
                "prompt": KEEP + edit + TEETH,
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
            dest = os.path.join(OUT, f"{slug}-s{seed}.png")
            urllib.request.urlretrieve(o[0] if isinstance(o, list) else o, dest)
            made.append(dest)
        except Exception as e:
            print(f"  {slug} seed {seed}: {e}", flush=True)
    print(f"  {slug}: {len(made)} made", flush=True)
    return made


with ThreadPoolExecutor(max_workers=3) as ex:
    results = list(ex.map(run, SHOTS))
print(f"\n{sum(len(r) for r in results)} frames -> {OUT}")
