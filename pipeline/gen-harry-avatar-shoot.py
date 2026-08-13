#!/usr/bin/env python3
"""Harry (Craftons head of marketing) — HeyGen photo-avatar training set.

Identity is locked verbatim on every prompt so the face cannot drift between
frames; only wardrobe, set, angle and framing move. That consistency is the
whole point of the set.

    REPLICATE_API_TOKEN=... python3 gen-harry-avatar-shoot.py \
        <face-ref.png> <lockup-2col.png> <lockup-white.png> <exemplar.png> <out-dir>

<exemplar.png> is an approved frame showing the logo at the correct size and
placement. Branded shots receive it as a third reference and are told to copy
its scale — description alone did not hold it steady across runs.

Branded garments carry the real Craftons lockup, passed in as a reference image
rather than left to the model to invent — render it from the app repo's
craftons-logo.svg (see build_logo_refs.py alongside this file).

Two workers: a five-wide fan-out 429s on this account. Slugs already written to
the out-dir are skipped, so a killed or credit-starved run resumes by
re-invoking the same command.
"""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

TOKEN = os.environ["REPLICATE_API_TOKEN"]
MODEL = "google/nano-banana-pro"
FACE, LOCKUP_2COL, LOCKUP_WHITE, EXEMPLAR, OUT = sys.argv[1:6]
os.makedirs(OUT, exist_ok=True)

LOCK = (
    "This is the exact same man as in the first reference photo. Preserve his identity "
    "precisely: same face shape, same jawline and cheekbones, same nose, same blue-grey "
    "eyes, same eyebrows, same hairline and same dark brown side-swept hair, same age "
    "(late 30s), same skin tone. He keeps the same short, naturally kept dark beard in "
    "every shot. Do not restyle his face or his beard. "
    "Carry over his skin and beard exactly as they are in the reference: visible pores and "
    "uneven complexion, crow's feet at the eyes, forehead lines, sun freckling on the "
    "cheekbones, small natural blemishes, and grey hairs scattered through the beard and "
    "temples. He is about forty and looks it. Do NOT smooth his skin, do NOT even out his "
    "complexion, do NOT darken the grey out of his beard, do NOT make him younger or more "
    "handsome than the reference. "
    "Photorealistic, shot on a full-frame camera with a 50mm lens, sharp focus on the eyes, "
    "no beauty retouching, no skin smoothing, no plastic skin, not CGI, not illustrated. "
    "Absolutely no suit, no blazer, no sport coat, no tie."
)

# --- the logo brief -------------------------------------------------------
# Two colourways. Two-colour (green mark + white wordmark) is the house
# treatment and goes on black and khaki. On the Craftons-green jumper the green
# mark would sit green-on-green and vanish, so that one runs all-white.
# Scale is the part prompt adjectives could not hold — successive runs swung from
# a discreet badge to a chest-wide print off the same words. So the brief carries
# a worked example: an approved frame goes in as a third reference and the model
# is told to copy its scale and placement rather than interpret a description.
_SIZE = (
    "Embroider the complete lockup on his left breast, high on the chest just below the "
    "collarbone, offset to his left — never centred across the middle of the chest. "
    "LAYOUT IS CRITICAL: the lockup is HORIZONTAL — the four-lobe mark sits to the LEFT "
    "of the word 'Craftons', side by side on one single line, sharing a baseline. Never "
    "stack the mark above the word. Never show the mark on its own without the word. "
    "SIZE IS CRITICAL: the THIRD reference image shows this same man wearing the logo at "
    "exactly the correct size and position. Copy that scale and placement precisely. The "
    "whole lockup spans about one sixth of the image width and the mark alone is about "
    "one thirty-fifth of it — a modest chest badge, roughly 10cm wide on the real garment. "
    "It must not be a large print spanning the chest. "
    "Spell it exactly 'Craftons' and reproduce the letterforms and the mark faithfully. "
    "No other branding anywhere on the garment."
)
LOGO_2COL = ("\n\nThe second reference image is the Craftons logo artwork. " + _SIZE +
             " The mark is Craftons green and the word 'Craftons' is white.")
LOGO_WHITE = ("\n\nThe second reference image is the Craftons logo artwork. " + _SIZE +
              " Render the mark and the word both in white, so they read against the "
              "dark green fabric. Match the third reference for size and placement only, "
              "not for colour.")

# --- garments -------------------------------------------------------------
VEST = ("a black quilted puffer vest, unzipped, over a short-sleeved khaki work shirt "
        "with the collar open")
POLO = "a plain black short-sleeved polo shirt, no logo or branding of any kind"
JUMPER_BLACK = "a plain black crew-neck jumper"
JUMPER_BLACK_PLAIN = ("a plain black crew-neck jumper with no logo, no print and no branding of any kind")
JUMPER_GREEN = ("a crew-neck jumper in deep Craftons forest green (hex #194431), worn with "
                "plain trousers")
JUMPER_GREEN_PLAIN = ("a crew-neck jumper in deep Craftons forest green (hex #194431) with no logo, "
                      "no print and no branding of any kind, worn with plain trousers")
HOODIE = ("a plain black hoodie with straight-leg blue denim jeans — the jeans are a "
          "relaxed straight cut, loose through the thigh with a straight leg to the hem, "
          "definitely not skinny, not tapered and not tight. No logo or branding")
TEE = ("a plain white crew-neck t-shirt in a boxy relaxed cut — roomy through the chest "
       "and body, slightly wide and square at the shoulder, sleeves loose on the upper "
       "arm, hanging straight rather than clinging. Not fitted, not tight, not muscle-fit. "
       "Worn with relaxed straight-leg trousers. No logo or print")
NAVY = ("a thick heavyweight navy overshirt, buttoned, over a plain tee, with relaxed "
        "straight-leg trousers, no logo or branding")

# --- sets -----------------------------------------------------------------
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

# (slug, logo: None | '2col' | 'white', prompt)
SHOTS = [
    # ---------------- site interior: vest, now branded ----------------
    ("11-in-vest-front-living", '2col',
     f"He wears {VEST}, with the Craftons logo embroidered on the left breast of the vest. "
     f"{SITE_IN} Waist-up, straight-on to camera at eye level, looking directly into the "
     "lens, speaking with an open friendly expression. Standing in a large open living "
     "area. Soft natural daylight from tall windows."),
    ("12-in-vest-threequarter-window", '2col',
     f"He wears {VEST}, with the Craftons logo embroidered on the left breast of the vest. "
     f"{SITE_IN} Chest-up, body turned about 35 degrees to his right so his branded left breast stays toward camera, head turned back to "
     "the lens, slight smile. Standing beside a tall window, soft wrap light."),
    ("13-in-vest-low-doorway", '2col',
     f"He wears {VEST}, with the Craftons logo embroidered on the left breast of the vest. "
     f"{SITE_IN} Three-quarter length, camera slightly below eye level, standing in a wide "
     "doorway with rooms visible beyond, hands relaxed, neutral expression toward the lens."),
    ("14-in-vest-profile-wall", '2col',
     f"He wears {VEST}, with the Craftons logo embroidered on the left breast of the vest. "
     f"{SITE_IN} Chest-up, near profile, head turned roughly 60 degrees to his right away "
     "from the lens, looking off camera, thoughtful. Plain plastered wall behind, soft "
     "side light."),

    # ---------------- site interior: polo (unbranded, unchanged) ----------------
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

    # ---------------- site interior: black jumper ----------------
    ("18-in-jumper-front-open", '2col',
     f"He wears {JUMPER_BLACK}. {SITE_IN} Waist-up, straight-on at eye level, arms relaxed at "
     "his sides, calm confident expression into the lens. Large open room behind him falling "
     "soft. Soft frontal daylight."),
    ("19-in-jumper-threequarter-glazing", '2col',
     f"He wears {JUMPER_BLACK}. {SITE_IN} Chest-up, body turned about 30 degrees to his right so his branded left breast stays toward camera, "
     "head back to the lens, mid-sentence speaking expression. Standing near a full-height "
     "glazed wall, bright daylight through the glass."),
    ("20-in-jumper-high-hallway", '2col',
     f"He wears {JUMPER_BLACK}. {SITE_IN} Waist-up, camera slightly above eye level looking "
     "gently down at him, hands in pockets, relaxed half smile. Wide hallway receding behind, "
     "shallow depth of field."),

    # ---------------- studio ----------------
    ("21-st-hoodie-front-desk", None,
     f"He wears {HOODIE}. {STUDIO} Waist-up, straight-on at eye level, seated at a timber desk "
     "leaning slightly forward on his forearms, calm confident expression into the lens. Soft "
     "daylight from camera-left."),
    ("22-st-hoodie-threequarter-standing", None,
     f"He wears {HOODIE}. {STUDIO} Waist-up, body turned about 30 degrees to his right, head "
     "back toward the lens, slight smile. Standing against a plain matte white wall."),
    ("23-st-hoodie-low-walking", None,
     f"He wears {HOODIE}. {STUDIO} Three-quarter length, camera slightly below eye level, "
     "mid-stride walking through the office, glancing toward the lens, natural not posed. "
     "The straight-leg jeans hang loose and break cleanly over the shoe."),
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
    ("27-st-green-front", 'white',
     f"He wears {JUMPER_GREEN}. {STUDIO} Waist-up, straight-on at eye level, standing, relaxed "
     "and warm, looking directly into the lens. Clean background falling soft. Soft even key "
     "light from the front-left."),
    ("28-st-green-threequarter", 'white',
     f"He wears {JUMPER_GREEN}. {STUDIO} Chest-up, body turned about 35 degrees to his right so his branded left breast stays toward camera, "
     "head turned back to the lens, mid-sentence speaking expression. Bright diffused daylight."),
    ("29-st-navy-front-seated", None,
     f"He wears {NAVY}. {STUDIO} Waist-up, straight-on at eye level, seated, hands resting on "
     "the desk, attentive listening expression toward the lens. Soft even daylight."),
    ("30-st-navy-profile-lean", None,
     f"He wears {NAVY}. {STUDIO} Chest-up, near profile, head turned roughly 60 degrees to his "
     "right away from the lens, leaning against the edge of a desk. Directional side light."),

    # ---------------- outdoor building site ----------------
    ("31-out-vest-front-formwork", '2col',
     f"He wears {VEST}, with the Craftons logo embroidered on the left breast of the vest. "
     f"{SITE_OUT} Waist-up, straight-on to camera at eye level, looking into the lens, "
     "speaking to camera. The formed-up bench seat is clearly visible behind his shoulder. "
     "Bright overcast daylight, soft shadows."),
    ("32-out-vest-threequarter", '2col',
     f"He wears {VEST}, with the Craftons logo embroidered on the left breast of the vest. "
     f"{SITE_OUT} Chest-up, body turned about 35 degrees to his right, head back to the lens, "
     "slight smile. Formwork behind him, slightly soft. Warm morning sunlight from camera-left."),
    ("33-out-vest-low-beside", '2col',
     f"He wears {VEST}, with the Craftons logo embroidered on the left breast of the vest. "
     f"{SITE_OUT} Three-quarter length, camera slightly below eye level, standing beside the "
     "plywood formwork with one hand resting on the top edge of the form, looking to the lens. "
     "Bright daylight, blue sky above."),
    ("34-out-vest-profile", '2col',
     f"He wears {VEST}, with the Craftons logo embroidered on the left breast of the vest. "
     f"{SITE_OUT} Chest-up, near profile, head turned roughly 60 degrees to his left away from "
     "the lens, looking along the line of the formwork. Overcast even light."),
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
    ("38-out-jumper-front", '2col',
     f"He wears {JUMPER_BLACK}. {SITE_OUT} Waist-up, straight-on at eye level, hands in "
     "pockets, easy half smile to the lens. Formwork behind his shoulder. Soft overcast light."),
    ("39-out-jumper-threequarter", '2col',
     f"He wears {JUMPER_BLACK}. {SITE_OUT} Chest-up, body turned about 40 degrees to his right so his branded left breast stays toward camera, "
     "head back to the lens, mid-sentence speaking. Golden hour side light, long soft shadows; the jumper still reads clearly black, not brown or warm-tinted."),
    ("40-out-jumper-high", '2col',
     f"He wears {JUMPER_BLACK}. {SITE_OUT} Waist-up, camera slightly above eye level looking "
     "gently down at him, neutral open expression. Standing on the compacted ground with the "
     "formwork and reinforcement mesh behind. Bright even daylight."),
]

# Branding is a switch, not a rewrite. CRAFTONS_LOGOS=off strips every logo from the
# set — garments go plain, the lockup references go unused — so an unbranded run and a
# branded one come off the same shot list rather than diverging into two scripts.
if os.environ.get("CRAFTONS_LOGOS", "on").lower() == "off":
    _plain = []
    for slug, _logo, scene in SHOTS:
        scene = scene.replace(
            ", with the Craftons logo embroidered on the left breast of the vest", "")
        scene = scene.replace(JUMPER_BLACK, JUMPER_BLACK_PLAIN)
        scene = scene.replace(JUMPER_GREEN, JUMPER_GREEN_PLAIN)
        scene += (" His clothing is completely unbranded: no logo, no wordmark, no embroidery, "
                  "no print, no badge and no text anywhere on any garment.")
        _plain.append((slug, None, scene))
    SHOTS = _plain
    print("CRAFTONS_LOGOS=off — generating unbranded garments", flush=True)

# Optional: pass a comma-separated slug-prefix filter as the last argument to re-shoot a subset.
if len(sys.argv) > 6:
    keep = tuple(sys.argv[6].split(","))
    SHOTS = [s for s in SHOTS if s[0].split("-")[0] in keep]


def api(path, data=None):
    req = urllib.request.Request(
        f"https://api.replicate.com/v1{path}",
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def upload(path):
    b = "----craftonsharry"
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
    if logo == "2col":
        refs += [urls["2col"], urls["exemplar"]];  prompt += LOGO_2COL
    elif logo == "white":
        refs += [urls["white"], urls["exemplar"]]; prompt += LOGO_WHITE

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
urls = {"face": upload(FACE), "2col": upload(LOCKUP_2COL),
        "white": upload(LOCKUP_WHITE), "exemplar": upload(EXEMPLAR)}
print(f"generating {len(SHOTS)} images...", flush=True)

with ThreadPoolExecutor(max_workers=2) as ex:
    results = list(ex.map(lambda j: run(j, urls), SHOTS))

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump({"model": MODEL, "face_reference": FACE,
               "shots": [{"slug": s, "file": f, "prompt": p} for s, f, p in results]},
              fh, indent=2)
print(f"\n{sum(1 for _, f, _ in results if f)}/{len(SHOTS)} generated -> {OUT}")
