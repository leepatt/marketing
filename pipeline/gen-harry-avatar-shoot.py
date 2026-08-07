#!/usr/bin/env python3
"""Harry (Craftons head of marketing) — HeyGen photo-avatar training set.

Ten 4:5 / 2K frames off one reference photo. Identity is locked verbatim on
every prompt so the face cannot drift; only wardrobe, set, angle and framing
move. Wardrobe is Harry's real rotation — no suits, no blazers, no ties.

    REPLICATE_API_TOKEN=... python3 gen_harry.py <face-ref.png> <logo-mark.png> <out-dir>

Serial: a five-wide fan-out 429s on this account. Slugs already on disk are
skipped, so a killed run resumes by re-invoking the same command.
"""
import json, os, sys, time, urllib.request

TOKEN = os.environ["REPLICATE_API_TOKEN"]
MODEL = "google/nano-banana-pro"
FACE_REF, LOGO_REF, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)

# Repeated verbatim on every prompt — this is what makes the set trainable.
LOCK = (
    "This is the exact same man as in the first reference photo. Preserve his identity "
    "precisely: same face shape, same jawline and cheekbones, same nose, same blue-grey "
    "eyes, same eyebrows, same hairline and same dark brown side-swept hair, same age "
    "(late 30s), same skin tone. He keeps the same short, naturally kept dark beard in "
    "every shot. Do not restyle his face or his beard. "
    "Photorealistic, shot on a full-frame camera with a 50mm lens, natural skin texture "
    "with visible pores, sharp focus on the eyes, no beauty retouching, no plastic skin, "
    "not CGI, not illustrated. He is a marketing person, not a corporate executive — "
    "absolutely no suit, no blazer, no sport coat, no tie."
)

SITE = (
    "The setting is the interior of a large near-finished high-end Australian home: "
    "freshly painted plaster walls, premium joinery installed, large windows with soft "
    "daylight, and the floor fully covered in brown protective cardboard sheeting taped "
    "at the seams."
)
STUDIO = (
    "The setting is a Craftons content studio / marketing office: clean modern space, "
    "matte white and warm timber surfaces, a little video kit around the edges of frame, "
    "soft even daylight. Relaxed creative workspace, not a corporate boardroom."
)

# Wardrobe — Harry's actual rotation.
VEST = ("a black quilted puffer vest, unzipped, over a short-sleeved khaki work shirt "
        "with the collar open")
POLO = "a plain black short-sleeved polo shirt, no logo"
BLACK_JUMPER = ("a plain black crew-neck jumper with one small embroidered logo on the "
                "left breast, matching the logo in the second reference image exactly — "
                "green, small, subtle, roughly 5cm wide, no other branding anywhere")
HOODIE = "a plain black hoodie with blue denim jeans"
TEE = "a plain white crew-neck t-shirt with straight-leg trousers"
GREEN_JUMPER = ("a deep forest green crew-neck jumper in Craftons green (hex #194431) with "
                "one small embroidered logo on the left breast, matching the logo in the "
                "second reference image exactly — small and subtle, roughly 5cm wide, no "
                "other branding anywhere, worn with plain trousers")
NAVY_SHIRT = ("a thick heavyweight navy overshirt worn buttoned over a plain tee, with "
              "plain trousers")

# (slug, wardrobe, needs_logo_ref, scene+framing)
SHOTS = [
    # ---------- on site ----------
    ("01-site-vest-front", VEST, False,
     f"He wears {VEST}. {SITE} Waist-up, straight-on to camera at eye level, looking "
     "directly into the lens, speaking to camera with an open friendly expression. "
     "Standing in the middle of a large open living area, cardboard-covered floor "
     "stretching away behind him. Soft natural daylight from tall windows."),

    ("02-site-vest-kitchen-threequarter", VEST, False,
     f"He wears {VEST}. {SITE} Wider waist-up, body turned about 35 degrees to his right "
     "in three-quarter view, head turned back to the lens, one hand resting on a stone "
     "kitchen benchtop. New cabinetry behind him, cardboard protection on the floor. "
     "Even overhead daylight."),

    ("03-site-polo-profile", POLO, False,
     f"He wears {POLO}. {SITE} Chest-up, near profile, head turned roughly 60 degrees away "
     "from the lens, looking off camera toward a full-height glazed wall. Bright daylight "
     "coming through the glazing, soft wrap light on the face, cool daylight tone."),

    ("04-site-jumper-hallway", BLACK_JUMPER, True,
     f"He wears {BLACK_JUMPER}. {SITE} Waist-up, straight-on at eye level, hands relaxed at "
     "his sides, easy half smile toward the lens. Standing in a wide hallway with long "
     "receding depth behind him, doorways either side, cardboard floor protection running "
     "the length of the hall. Shallow depth of field so the hallway falls soft."),

    ("05-site-jumper-filming-low", BLACK_JUMPER, True,
     f"He wears {BLACK_JUMPER}. {SITE} Three-quarter length, camera slightly below eye level "
     "looking up at him, standing at the bottom of a timber staircase holding a phone on a "
     "small gimbal, filming content, glancing toward the lens between takes. Cardboard "
     "sheeting on the treads and floor. Directional light from a stairwell window above."),

    # ---------- studio / office ----------
    ("06-studio-hoodie-desk-front", HOODIE, False,
     f"He wears {HOODIE}. {STUDIO} Waist-up, straight-on to camera at eye level, seated at a "
     "desk, leaning slightly forward on his forearms, calm confident expression directly "
     "into the lens. Soft daylight from a large window to camera-left."),

    ("07-studio-tee-threequarter", TEE, False,
     f"He wears {TEE}. {STUDIO} Waist-up, body turned about 30 degrees to his left in "
     "three-quarter view, head turned back toward the lens, slight smile, arms loose. "
     "Standing in the open studio space. Bright diffused daylight, clean soft shadows."),

    ("08-studio-green-jumper-front", GREEN_JUMPER, True,
     f"He wears {GREEN_JUMPER}. {STUDIO} Waist-up, straight-on at eye level, standing, "
     "relaxed and warm, looking directly into the lens. Clean uncluttered background falling "
     "soft behind him. Soft even key light from the front-left."),

    ("09-studio-navy-shirt-profile", NAVY_SHIRT, False,
     f"He wears {NAVY_SHIRT}. {STUDIO} Chest-up, near profile, head turned roughly 55 degrees "
     "away from the lens, looking off camera, neutral thoughtful expression, leaning against "
     "the edge of a desk. Directional side light from the right, soft shadow falling across "
     "the far cheek."),

    ("10-studio-hoodie-editing-wide", HOODIE, False,
     f"He wears {HOODIE}. {STUDIO} Wider three-quarter length from slightly above eye level, "
     "seated at a large monitor reviewing footage, camera gear and a tripod visible at the "
     "edge of frame, turning to glance toward the lens. Warm ambient light plus screen glow "
     "on the face."),
]


def api(path, data=None):
    req = urllib.request.Request(
        f"https://api.replicate.com/v1{path}",
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def upload(path):
    boundary = "----craftonsharryboundary"
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


def run(job, face_url, logo_url):
    slug, _wardrobe, needs_logo, scene = job
    dest = os.path.join(OUT, f"{slug}.png")
    if os.path.exists(dest) and os.path.getsize(dest) > 100_000:
        print(f"  skip {slug}", flush=True)
        return slug, dest, None

    refs = [face_url] + ([logo_url] if needs_logo else [])
    note = ("\n\nThe second reference image is the Craftons logo mark. Reproduce it exactly "
            "as shown — same shape, same proportions — small on the left breast only. Do not "
            "enlarge it, do not repeat it, do not add any text or wordmark."
            if needs_logo else "")
    prompt = f"{LOCK}\n\n{scene}{note}"

    for attempt in range(5):
        try:
            p = api(f"/models/{MODEL}/predictions", {"input": {
                "prompt": prompt,
                "image_input": refs,
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
            urllib.request.urlretrieve(out[0] if isinstance(out, list) else out, dest)
            print(f"  ok   {slug}  ({os.path.getsize(dest)//1024} KB)", flush=True)
            return slug, dest, prompt
        except Exception as e:
            print(f"  retry {slug} #{attempt+1}: {e}", flush=True)
            time.sleep(20 * (attempt + 1))
    print(f"  FAIL {slug}", flush=True)
    return slug, None, prompt


print("uploading references...", flush=True)
face_url, logo_url = upload(FACE_REF), upload(LOGO_REF)
print(f"generating {len(SHOTS)} images...", flush=True)

results = []
for j in SHOTS:
    results.append(run(j, face_url, logo_url))
    time.sleep(8)

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump({"model": MODEL, "face_reference": FACE_REF, "logo_reference": LOGO_REF,
               "shots": [{"slug": s, "file": f, "prompt": p} for s, f, p in results]},
              fh, indent=2)

print(f"\n{sum(1 for _, f, _ in results if f)}/{len(SHOTS)} generated -> {OUT}")
