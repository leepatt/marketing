#!/usr/bin/env python3
"""Harry (Craftons head of marketing) — HeyGen photo-avatar training set, batch 3.

30 frames: 10 site interior, 10 studio/office, 10 outdoor building site with a
concrete bench seat formed up ready to pour. Identity locked verbatim on every
prompt; only wardrobe, set, angle and framing move.

    REPLICATE_API_TOKEN=... python3 gen_harry_v3.py <face> <lockup-dark> <lockup-light> <out>

Branded garments carry the full Craftons lockup (mark + "Craftons" wordmark in
Aeonik), passed in as a reference image rather than left to the model to invent.
Two workers — five 429s, one is needlessly slow. Existing slugs are skipped.
"""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

TOKEN = os.environ["REPLICATE_API_TOKEN"]
MODEL = "google/nano-banana-pro"
FACE, LOCKUP_ON_DARK, LOCKUP_ON_LIGHT, OUT = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)

LOCK = (
    "This is the exact same man as in the first reference photo. Preserve his identity "
    "precisely: same face shape, same jawline and cheekbones, same nose, same blue-grey "
    "eyes, same eyebrows, same hairline and same dark brown side-swept hair, same age "
    "(late 30s), same skin tone. He keeps the same short, naturally kept dark beard in "
    "every shot. Do not restyle his face or his beard. "
    "Photorealistic, shot on a full-frame camera with a 50mm lens, natural skin texture "
    "with visible pores, sharp focus on the eyes, no beauty retouching, no plastic skin, "
    "not CGI, not illustrated. Absolutely no suit, no blazer, no sport coat, no tie."
)

# Garments
VEST = ("a black quilted puffer vest, unzipped, over a short-sleeved khaki work shirt "
        "with the collar open")
POLO = "a plain black short-sleeved polo shirt, no logo or branding of any kind"
JUMPER_BLACK = "a plain black crew-neck jumper"
HOODIE = "a plain black hoodie with blue denim jeans, no logo or branding of any kind"
TEE = "a plain white crew-neck t-shirt with straight-leg trousers, no logo or print"
JUMPER_GREEN = ("a crew-neck jumper in deep Craftons forest green (hex #194431), worn with "
                "plain trousers")
NAVY = ("a thick heavyweight navy overshirt, buttoned, over a plain tee, with plain "
        "trousers, no logo or branding")

# Sets
SITE_IN = (
    "The setting is the interior of a large near-finished high-end Australian home: "
    "freshly painted plaster walls, premium joinery installed, large windows with soft "
    "daylight, and the floor fully covered in brown corrugated cardboard protection "
    "sheeting, clearly cardboard, taped at the seams."
)
STUDIO = (
    "The setting is a clean modern Craftons marketing office: matte white walls, warm "
    "timber desk surfaces, a few plants and some books, soft even daylight from a large "
    "window. IMPORTANT: there is absolutely no camera equipment anywhere in the frame — "
    "no cameras, no tripods, no studio lights, no softboxes, no light stands, no boom "
    "arms, no microphones, no video gear of any kind. An ordinary quiet office."
)
SITE_OUT = (
    "The setting is an outdoor residential building site in Australia on a bright day. "
    "Clearly visible behind him is a curved concrete bench seat that has been formed up "
    "and is ready to pour: smooth plywood formwork panels bent to a curve, held by timber "
    "stakes and props, steel reinforcement mesh sitting inside the form, clean compacted "
    "ground around it. Part-built landscaping and a rendered house wall further behind."
)

LOGO_NOTE_DARK = (
    "\n\nThe second reference image is the Craftons logo lockup: the green four-lobe mark "
    "followed by the word 'Craftons' set in the brand's geometric sans-serif. Embroider "
    "that complete lockup — mark AND the word 'Craftons' beside it — small on his left "
    "breast, about 9cm wide, wordmark in white with the mark in green, spelled exactly "
    "'Craftons'. Reproduce the letterforms and the mark faithfully. No other branding "
    "anywhere on the garment."
)
LOGO_NOTE_LIGHT = LOGO_NOTE_DARK.replace(
    "wordmark in white with the mark in green", "wordmark and mark both in white")

# (slug, needs_logo: None|'dark'|'light', prompt)
SHOTS = [
    # ---------------- site interior ----------------
    ("11-in-vest-front-living", None,
     f"He wears {VEST}. {SITE_IN} Waist-up, straight-on to camera at eye level, looking "
     "directly into the lens, speaking with an open friendly expression. Standing in a "
     "large open living area. Soft natural daylight from tall windows."),
    ("12-in-vest-threequarter-window", None,
     f"He wears {VEST}. {SITE_IN} Chest-up, body turned about 35 degrees to his left, head "
     "turned back to the lens, slight smile. Standing beside a tall window, soft wrap light."),
    ("13-in-vest-low-doorway", None,
     f"He wears {VEST}. {SITE_IN} Three-quarter length, camera slightly below eye level, "
     "standing in a wide doorway with rooms visible beyond, hands relaxed, neutral expression "
     "toward the lens."),
    ("14-in-vest-profile-wall", None,
     f"He wears {VEST}. {SITE_IN} Chest-up, near profile, head turned roughly 60 degrees to "
     "his right away from the lens, looking off camera, thoughtful. Plain plastered wall "
     "behind, soft side light."),
    ("15-in-polo-front-kitchen", None,
     f"He wears {POLO}. {SITE_IN} Waist-up, straight-on at eye level, one hand resting on a "
     "stone kitchen benchtop, easy half smile to the lens. New cabinetry behind. Even daylight."),
    ("16-in-polo-profile-hall", None,
     f"He wears {POLO}. {SITE_IN} Chest-up, near profile, head turned roughly 55 degrees to "
     "his left away from the lens. Standing in a wide hallway, doorways either side. "
     "Directional light from one end of the hall."),
    ("17-in-polo-threequarter-stairs", None,
     f"He wears {POLO}. {SITE_IN} Wider three-quarter length, body angled about 40 degrees to "
     "his right, glancing back to the lens. Standing at the bottom of a timber staircase, "
     "cardboard sheeting on the treads. Light from a stairwell window above."),
    ("18-in-jumper-front-open", 'dark',
     f"He wears {JUMPER_BLACK}. {SITE_IN} Waist-up, straight-on at eye level, arms relaxed at "
     "his sides, calm confident expression into the lens. Large open room behind him falling "
     "soft. Soft frontal daylight."),
    ("19-in-jumper-threequarter-glazing", 'dark',
     f"He wears {JUMPER_BLACK}. {SITE_IN} Chest-up, body turned about 30 degrees to his right, "
     "head back to the lens, mid-sentence speaking expression. Standing near a full-height "
     "glazed wall, bright daylight through the glass."),
    ("20-in-jumper-high-hallway", 'dark',
     f"He wears {JUMPER_BLACK}. {SITE_IN} Waist-up, camera slightly above eye level looking "
     "gently down at him, hands in pockets, relaxed half smile. Wide hallway receding behind, "
     "shallow depth of field."),

    # ---------------- studio / office ----------------
    ("21-st-hoodie-front-desk", None,
     f"He wears {HOODIE}. {STUDIO} Waist-up, straight-on at eye level, seated at a timber desk "
     "leaning slightly forward on his forearms, calm confident expression into the lens. Soft "
     "daylight from camera-left."),
    ("22-st-hoodie-threequarter-standing", None,
     f"He wears {HOODIE}. {STUDIO} Waist-up, body turned about 30 degrees to his right, head "
     "back toward the lens, slight smile. Standing against a plain matte white wall."),
    ("23-st-hoodie-low-walking", None,
     f"He wears {HOODIE}. {STUDIO} Three-quarter length, camera slightly below eye level, "
     "mid-stride walking through the office, glancing toward the lens, natural not posed."),
    ("24-st-tee-front-standing", None,
     f"He wears {TEE}. {STUDIO} Waist-up, straight-on at eye level, standing, arms loose, warm "
     "open expression directly into the lens. Clean uncluttered background. Soft frontal key light."),
    ("25-st-tee-profile", None,
     f"He wears {TEE}. {STUDIO} Chest-up, near profile, head turned roughly 55 degrees to his "
     "left away from the lens, neutral thoughtful expression. Directional side light from the "
     "right, soft shadow across the far cheek."),
    ("26-st-tee-high-seated", None,
     f"He wears {TEE}. {STUDIO} Waist-up, camera slightly above eye level looking down at him, "
     "seated at a timber table with a notebook, looking up to the lens, easy smile."),
    ("27-st-green-front", 'light',
     f"He wears {JUMPER_GREEN}. {STUDIO} Waist-up, straight-on at eye level, standing, relaxed "
     "and warm, looking directly into the lens. Clean background falling soft. Soft even key "
     "light from the front-left."),
    ("28-st-green-threequarter", 'light',
     f"He wears {JUMPER_GREEN}. {STUDIO} Chest-up, body turned about 35 degrees to his left, "
     "head turned back to the lens, mid-sentence speaking expression. Bright diffused daylight."),
    ("29-st-navy-front-seated", None,
     f"He wears {NAVY}. {STUDIO} Waist-up, straight-on at eye level, seated, hands resting on "
     "the desk, attentive listening expression toward the lens. Soft even daylight."),
    ("30-st-navy-profile-lean", None,
     f"He wears {NAVY}. {STUDIO} Chest-up, near profile, head turned roughly 60 degrees to his "
     "right away from the lens, leaning against the edge of a desk. Directional side light."),

    # ---------------- outdoor building site ----------------
    ("31-out-vest-front-formwork", None,
     f"He wears {VEST}. {SITE_OUT} Waist-up, straight-on to camera at eye level, looking into "
     "the lens, speaking to camera. The formed-up bench seat is clearly visible behind his "
     "shoulder. Bright overcast daylight, soft shadows."),
    ("32-out-vest-threequarter", None,
     f"He wears {VEST}. {SITE_OUT} Chest-up, body turned about 35 degrees to his right, head "
     "back to the lens, slight smile. Formwork behind him, slightly soft. Warm morning sunlight "
     "from camera-left."),
    ("33-out-vest-low-beside", None,
     f"He wears {VEST}. {SITE_OUT} Three-quarter length, camera slightly below eye level, "
     "standing beside the plywood formwork with one hand resting on the top edge of the form, "
     "looking to the lens. Bright daylight, blue sky above."),
    ("34-out-vest-profile", None,
     f"He wears {VEST}. {SITE_OUT} Chest-up, near profile, head turned roughly 60 degrees to "
     "his left away from the lens, looking along the line of the formwork. Overcast even light."),
    ("35-out-polo-front", None,
     f"He wears {POLO}. {SITE_OUT} Waist-up, straight-on at eye level, arms relaxed, calm "
     "confident expression into the lens. Curved formwork clearly behind him. Bright daylight."),
    ("36-out-polo-profile", None,
     f"He wears {POLO}. {SITE_OUT} Chest-up, near profile, head turned roughly 55 degrees to "
     "his right away from the lens, thoughtful. Late afternoon side light, warm tone."),
    ("37-out-polo-wide-gesture", None,
     f"He wears {POLO}. {SITE_OUT} Wider three-quarter length, body angled to his left, one "
     "hand gesturing toward the formed-up bench seat, head turned back to the lens, explaining "
     "something. Whole form visible in frame. Bright overcast light."),
    ("38-out-jumper-front", 'dark',
     f"He wears {JUMPER_BLACK}. {SITE_OUT} Waist-up, straight-on at eye level, hands in "
     "pockets, easy half smile to the lens. Formwork behind his shoulder. Soft overcast light."),
    ("39-out-jumper-threequarter", 'dark',
     f"He wears {JUMPER_BLACK}. {SITE_OUT} Chest-up, body turned about 40 degrees to his left, "
     "head back to the lens, mid-sentence speaking. Golden hour side light, long soft shadows."),
    ("40-out-jumper-high", 'dark',
     f"He wears {JUMPER_BLACK}. {SITE_OUT} Waist-up, camera slightly above eye level looking "
     "gently down at him, neutral open expression. Standing on the compacted ground with the "
     "formwork and reinforcement mesh behind. Bright even daylight."),
]


def api(path, data=None):
    req = urllib.request.Request(
        f"https://api.replicate.com/v1{path}",
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def upload(path):
    b = "----craftonsharryv3"
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


def run(job, urls):
    slug, logo, scene = job
    dest = os.path.join(OUT, f"{slug}.png")
    if os.path.exists(dest) and os.path.getsize(dest) > 100_000:
        print(f"  skip {slug}", flush=True)
        return slug, dest, None

    refs = [urls["face"]]
    prompt = f"{LOCK}\n\n{scene}"
    if logo == "dark":
        refs.append(urls["dark"]);  prompt += LOGO_NOTE_DARK
    elif logo == "light":
        refs.append(urls["light"]); prompt += LOGO_NOTE_LIGHT

    for attempt in range(5):
        try:
            p = api(f"/models/{MODEL}/predictions", {"input": {
                "prompt": prompt, "image_input": refs, "aspect_ratio": "4:5",
                "resolution": "2K", "output_format": "png",
                "safety_filter_level": "block_only_high"}})
            while p["status"] not in ("succeeded", "failed", "canceled"):
                time.sleep(3)
                p = api(f"/predictions/{p['id']}")
            if p["status"] != "succeeded":
                raise RuntimeError(p.get("error") or p["status"])
            o = p["output"]
            urllib.request.urlretrieve(o[0] if isinstance(o, list) else o, dest)
            print(f"  ok   {slug}  ({os.path.getsize(dest)//1024} KB)", flush=True)
            return slug, dest, prompt
        except Exception as e:
            print(f"  retry {slug} #{attempt+1}: {e}", flush=True)
            time.sleep(15 * (attempt + 1))
    print(f"  FAIL {slug}", flush=True)
    return slug, None, prompt


print("uploading references...", flush=True)
urls = {"face": upload(FACE), "dark": upload(LOCKUP_ON_DARK), "light": upload(LOCKUP_ON_LIGHT)}
print(f"generating {len(SHOTS)} images...", flush=True)

with ThreadPoolExecutor(max_workers=2) as ex:
    results = list(ex.map(lambda j: run(j, urls), SHOTS))

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump({"model": MODEL, "face_reference": FACE,
               "shots": [{"slug": s, "file": f, "prompt": p} for s, f, p in results]},
              fh, indent=2)
print(f"\n{sum(1 for _, f, _ in results if f)}/{len(SHOTS)} generated -> {OUT}")
