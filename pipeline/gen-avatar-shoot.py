#!/usr/bin/env python3
"""Generate a HeyGen avatar-training set from one reference photo, via Replicate.

Two wardrobes x five scenes. Identity is locked to the reference on every call;
only framing, angle, wardrobe and set change.

    REPLICATE_API_TOKEN=... python3 gen-avatar-shoot.py <reference.png> <out-dir>

Runs serially — Replicate 429s a five-wide fan-out on this account. Already-written
slugs are skipped, so a killed run resumes by re-invoking the same command.
Output is 4:5 / 2K PNG, which is the framing HeyGen photo-avatar training wants.
"""
import json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

TOKEN = os.environ["REPLICATE_API_TOKEN"]
MODEL = "google/nano-banana-pro"
REF = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# Repeated verbatim on every prompt so the face cannot drift between scenes.
LOCK = (
    "This is the exact same man as in the reference photo. Preserve his identity "
    "precisely: same face shape, same jawline and cheekbones, same nose, same "
    "blue-grey eyes, same eyebrows, same hairline and same dark brown side-swept "
    "hair, same age (late 30s), same skin tone and complexion. Do not restyle his "
    "face. Photorealistic, shot on a full-frame camera with a 50mm lens, natural "
    "skin texture with visible pores, sharp focus on the eyes, no beauty retouching, "
    "no plastic skin, not CGI, not illustrated."
)

OFFICE = (
    "He is clean and corporate: beard trimmed short, neat and sharply edged, hair "
    "combed and tidy."
)
SITE = (
    "He wears a navy quilted puffer jacket, zipped part-way, over a short-sleeved "
    "work shirt with the collar visible. Beard is natural and slightly fuller. "
    "The setting is the interior of a large near-finished high-end Australian home: "
    "plastered walls freshly painted, premium joinery installed, large windows with "
    "soft daylight, and the floor fully covered in brown protective cardboard sheeting "
    "taped at the seams."
)

SHOTS = [
    # --- 5 x office, smart attire ---
    ("01-office-front-desk",
     f"{OFFICE} Waist-up portrait, straight-on to camera at eye level, looking directly "
     "into the lens with a calm confident expression. He is seated at a desk in a modern "
     "office, wearing a crisp white shirt under an unbuttoned navy wool blazer. Blurred "
     "office depth behind him. Soft even daylight from a large window to camera-left."),

    ("02-office-three-quarter-standing",
     f"{OFFICE} Waist-up, body turned about 30 degrees to his right in a three-quarter "
     "view, head turned back toward the lens, slight smile. Standing in front of a "
     "glass-walled meeting room. Light blue business shirt, no jacket, sleeves rolled to "
     "the forearm. Bright diffused overhead office lighting."),

    ("03-office-profile-lean",
     f"{OFFICE} Chest-up, near profile, head turned roughly 60 degrees away from the lens, "
     "looking off camera to the side, neutral thoughtful expression. Leaning against the "
     "edge of a desk. Charcoal fine-knit polo. Directional side light from the right, soft "
     "shadow falling across the far cheek."),

    ("04-office-window-wide",
     f"{OFFICE} Wider waist-up with room around him, standing beside a floor-to-ceiling "
     "office window, body angled slightly to camera-left, looking to the lens. Navy suit "
     "jacket over an open-collar white shirt. Backlit by bright city daylight with soft "
     "fill on the face, gentle rim light on the shoulders."),

    ("05-office-low-angle-walking",
     f"{OFFICE} Three-quarter length, camera slightly below eye level looking up at him, "
     "mid-stride walking through an open-plan office, carrying a tablet, glancing toward "
     "the lens. Light grey blazer over a white shirt. Bright modern office, shallow depth "
     "of field, motion feels natural not posed."),

    # --- 5 x on site, navy puffer + short sleeves ---
    ("06-site-front-living",
     f"{SITE} Waist-up, straight-on to camera at eye level, looking directly into the lens, "
     "speaking to camera with an open friendly expression. Standing in the middle of a "
     "large open living area, cardboard-covered floor stretching behind him. Soft natural "
     "daylight from tall windows."),

    ("07-site-three-quarter-glazing",
     f"{SITE} Chest-up, body turned about 40 degrees to his left in three-quarter view, head "
     "turned back to the lens. Standing near a full-height glazed wall with bright daylight "
     "coming through, cardboard floor protection visible. Soft window light wrapping the "
     "face, cool daylight tone."),

    ("08-site-kitchen-island",
     f"{SITE} Wider waist-up, standing behind a large stone-topped kitchen island with a "
     "hand resting on the benchtop, angled slightly to camera-right, looking to the lens. "
     "New cabinetry behind, protective cardboard on the floor. Even overhead daylight."),

    ("09-site-staircase-side",
     f"{SITE} Three-quarter length from a side angle, roughly 70 degrees off-axis, standing "
     "at the bottom of a timber staircase, looking up and away from the lens. Cardboard "
     "sheeting running up the stair treads and across the floor. Directional light from a "
     "stairwell window above, soft shadow on the near side."),

    ("10-site-hallway-depth",
     f"{SITE} Waist-up, straight-on at eye level, hands in jacket pockets, relaxed half "
     "smile toward the lens. Standing in a wide hallway with long receding depth behind him, "
     "doorways either side, cardboard floor protection running the length of the hall. "
     "Shallow depth of field so the hallway falls soft behind him."),
]


def api(path, data=None, method=None):
    req = urllib.request.Request(
        f"https://api.replicate.com/v1{path}",
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
        method=method or ("POST" if data else "GET"),
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def upload(path):
    """Multipart upload to Replicate's files API; returns a URL usable as image_input."""
    boundary = "----craftonsavatarboundary"
    body = b"".join([
        f'--{boundary}\r\nContent-Disposition: form-data; name="content"; '
        f'filename="{os.path.basename(path)}"\r\nContent-Type: image/png\r\n\r\n'.encode(),
        open(path, "rb").read(),
        f"\r\n--{boundary}--\r\n".encode(),
    ])
    req = urllib.request.Request(
        "https://api.replicate.com/v1/files", data=body,
        headers={"Authorization": f"Bearer {TOKEN}",
                 "Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)["urls"]["get"]


def run(job, ref_url):
    slug, scene = job
    done = os.path.join(OUT, f"{slug}.png")
    if os.path.exists(done) and os.path.getsize(done) > 100_000:
        print(f"  skip {slug} (already have it)", flush=True)
        return slug, done, scene
    prompt = f"{LOCK}\n\n{scene}"
    for attempt in range(5):
        try:
            p = api(f"/models/{MODEL}/predictions", {
                "input": {
                    "prompt": prompt,
                    "image_input": [ref_url],
                    "aspect_ratio": "4:5",
                    "resolution": "2K",
                    "output_format": "png",
                    "safety_filter_level": "block_only_high",
                }})
            while p["status"] not in ("succeeded", "failed", "canceled"):
                time.sleep(3)
                p = api(f"/predictions/{p['id']}")
            if p["status"] != "succeeded":
                raise RuntimeError(p.get("error") or p["status"])
            out = p["output"]
            url = out[0] if isinstance(out, list) else out
            dest = os.path.join(OUT, f"{slug}.png")
            urllib.request.urlretrieve(url, dest)
            print(f"  ok   {slug}  ({os.path.getsize(dest)//1024} KB)", flush=True)
            return slug, dest, prompt
        except Exception as e:
            print(f"  retry {slug} attempt {attempt+1}: {e}", flush=True)
            time.sleep(20 * (attempt + 1))
    print(f"  FAIL {slug}", flush=True)
    return slug, None, prompt


print("uploading reference...", flush=True)
ref_url = upload(REF)
print(f"  {ref_url}\ngenerating {len(SHOTS)} images...", flush=True)

results = []
for j in SHOTS:
    results.append(run(j, ref_url))
    time.sleep(8)

manifest = [{"slug": s, "file": f, "prompt": p} for s, f, p in results]
with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump({"model": MODEL, "reference": REF, "shots": manifest}, fh, indent=2)

ok = sum(1 for _, f, _ in results if f)
print(f"\n{ok}/{len(SHOTS)} generated -> {OUT}")
