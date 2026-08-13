#!/usr/bin/env python3
"""Generate ONE Harry frame at a time, from the approved hero.

Deliberately one at a time. Bulk runs produce sets that look fine in a contact
sheet and fall apart on inspection — this exists so every frame is scored against
the hero and accepted or rejected on its own before the next one starts.

    REPLICATE_API_TOKEN=... python3 harry-shoot.py <hero.png> <out-dir> <shot-number>

Shot numbers follow HARRY-SHOT-LIST.md (1-30). Writes <out-dir>/NN-<slug>.png.
Pair it with face-check.py, which puts a number on the likeness.
"""
import json, os, sys, time, urllib.request

TOKEN = os.environ["REPLICATE_API_TOKEN"]
MODEL = "google/nano-banana-pro"
HERO, OUT, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
os.makedirs(OUT, exist_ok=True)

# Repeated verbatim on every frame. The texture clauses matter as much as the
# geometry ones: left alone the model smooths him back into a polished stranger.
LOCK = (
    "This is the exact same man as in the reference photograph. His face is the single "
    "most important thing in this image and it must match the reference exactly: same "
    "face shape, same jawline and cheekbones, same nose, same mouth, same blue-grey eyes "
    "set the same distance apart, same eyebrows, same hairline, same dark brown hair swept "
    "back the same way. Same man, same age, photographed on a different day. "
    "Carry his skin and beard over exactly as they are: visible pores and uneven "
    "complexion, crow's feet at the eyes, forehead lines, sun freckling on the cheekbones, "
    "small natural blemishes, short beard with grey scattered through it and at the temples. "
    "He is about forty and looks it. Do NOT smooth his skin, do NOT even out his complexion, "
    "do NOT darken the grey out of his beard, do NOT make him younger, slimmer or more "
    "handsome than the reference. "
    "Photorealistic, full-frame camera, 50mm lens, sharp focus on the eyes, no beauty "
    "retouching, no skin smoothing, no plastic skin, not CGI, not illustrated. "
    "No suit, no blazer, no sport coat, no tie. "
    "His clothing is completely unbranded: no logo, no wordmark, no embroidery, no print, "
    "no badge and no text anywhere on any garment."
)

VEST = ("a black quilted puffer vest, unzipped, over a short-sleeved khaki work shirt with "
        "the collar open")
POLO = "a plain black short-sleeved polo shirt"
JUMPER = "a plain black crew-neck jumper"
HOODIE = ("a plain black hoodie with relaxed straight-leg blue denim jeans, loose through "
          "the thigh, not skinny and not tapered")
TEE = ("a boxy relaxed white crew-neck t-shirt, roomy through the chest and square at the "
       "shoulder, hanging straight rather than clinging, with relaxed straight-leg trousers")
GREEN = ("a crew-neck jumper in deep Craftons forest green (hex #194431) with relaxed "
         "straight-leg trousers")
NAVY = ("a thick heavyweight navy overshirt, buttoned, over a plain tee, with relaxed "
        "straight-leg trousers")

IN = ("Interior of a large near-finished high-end Australian home: freshly painted plaster "
      "walls, premium joinery installed, large windows with soft daylight, floor fully "
      "covered in brown corrugated cardboard protection sheeting taped at the seams.")
ST = ("A clean modern marketing office: matte white walls, warm timber desks, a few plants "
      "and books, soft daylight from a large window. There is absolutely no camera equipment "
      "in frame — no cameras, tripods, studio lights, softboxes, stands or microphones.")
OUTS = ("An outdoor residential building site in Australia. Clearly behind him is a curved "
        "concrete bench seat formed up ready to pour: bent plywood formwork panels held by "
        "timber stakes and props, steel reinforcement mesh inside the form, compacted ground "
        "around it, part-built landscaping and a rendered house wall beyond.")

# (slug, wardrobe, set, framing + angle + beat)
SHOTS = [
    ("in-vest-front", VEST, IN,
     "Waist-up, straight-on to camera at eye level, head square to the lens, looking directly "
     "into it, speaking with an open friendly expression. Large open living area behind. Soft "
     "daylight from tall windows."),
    ("in-vest-threequarter-r", VEST, IN,
     "Chest-up, body turned about 30 degrees to his right, head turned back so the face is "
     "nearly square to the lens, slight smile. Beside a tall window, soft wrap light."),
    ("in-vest-low-doorway", VEST, IN,
     "Three-quarter length, camera slightly below eye level looking up at him, standing in a "
     "wide doorway with rooms beyond, hands relaxed, neutral expression to the lens."),
    ("in-vest-profile-r", VEST, IN,
     "Chest-up, near profile, head turned about 55 degrees to his right away from the lens, "
     "looking off camera, thoughtful. Plain plastered wall behind, soft side light."),
    ("in-polo-front-kitchen", POLO, IN,
     "Waist-up, straight-on at eye level, one hand resting on a stone kitchen benchtop, easy "
     "half smile to the lens. New cabinetry behind, even daylight."),
    ("in-polo-threequarter-l", POLO, IN,
     "Chest-up, body turned about 30 degrees to his left, head turned back toward the lens, "
     "listening expression. Wide hallway, doorways either side, directional light."),
    ("in-polo-high-stairs", POLO, IN,
     "Waist-up, camera slightly above eye level looking down at him as he looks up into the "
     "lens, easy expression. At the base of a timber staircase, cardboard on the treads."),
    ("in-jumper-front-open", JUMPER, IN,
     "Waist-up, straight-on at eye level, arms relaxed at his sides, calm confident expression "
     "directly into the lens. Large open room falling soft behind. Soft frontal daylight."),
    ("in-jumper-threequarter-r", JUMPER, IN,
     "Chest-up, body turned about 30 degrees to his right, head back to the lens, mid-sentence "
     "speaking expression. Near a full-height glazed wall, bright daylight through the glass."),
    ("in-jumper-profile-l", JUMPER, IN,
     "Chest-up, near profile, head turned about 55 degrees to his left away from the lens, "
     "thoughtful. Wide hallway receding behind, shallow depth of field."),

    ("st-hoodie-front-desk", HOODIE, ST,
     "Waist-up, straight-on at eye level, seated at a timber desk leaning slightly forward on "
     "his forearms, calm confident expression into the lens. Soft daylight from camera-left."),
    ("st-hoodie-threequarter-l", HOODIE, ST,
     "Waist-up, body turned about 30 degrees to his left, head back toward the lens, slight "
     "smile. Standing against a plain matte white wall."),
    ("st-hoodie-low-walking", HOODIE, ST,
     "Three-quarter length, camera slightly below eye level, mid-stride walking through the "
     "office, glancing toward the lens, natural rather than posed."),
    ("st-tee-front", TEE, ST,
     "Waist-up, straight-on at eye level, standing, arms loose, warm open expression directly "
     "into the lens. Clean uncluttered background, soft frontal key light."),
    ("st-tee-threequarter-r", TEE, ST,
     "Chest-up, body turned about 30 degrees to his right, head back to the lens, listening "
     "expression. Soft daylight, clean soft shadows."),
    ("st-tee-high-seated", TEE, ST,
     "Waist-up, camera slightly above eye level looking down at him, seated at a timber table "
     "with a notebook, looking up into the lens, easy smile."),
    ("st-green-front", GREEN, ST,
     "Waist-up, straight-on at eye level, standing, relaxed and warm, looking directly into "
     "the lens. Clean background falling soft, soft even key light from the front-left."),
    ("st-green-threequarter-l", GREEN, ST,
     "Chest-up, body turned about 30 degrees to his left, head back to the lens, mid-sentence "
     "speaking expression. Bright diffused daylight."),
    ("st-navy-front-seated", NAVY, ST,
     "Waist-up, straight-on at eye level, seated, hands resting on the desk, attentive "
     "listening expression toward the lens. Soft even daylight."),
    ("st-navy-profile-r", NAVY, ST,
     "Chest-up, near profile, head turned about 55 degrees to his right away from the lens, "
     "leaning against the edge of a desk. Directional side light."),

    ("out-vest-front-formwork", VEST, OUTS,
     "Waist-up, straight-on to camera at eye level, looking into the lens, speaking to camera. "
     "The formed-up bench seat clearly visible behind his shoulder. Bright overcast daylight."),
    ("out-vest-threequarter-r", VEST, OUTS,
     "Chest-up, body turned about 30 degrees to his right, head back to the lens, slight smile. "
     "Formwork behind, slightly soft. Warm morning sunlight from camera-left."),
    ("out-vest-low-beside", VEST, OUTS,
     "Three-quarter length, camera slightly below eye level, standing beside the plywood "
     "formwork with one hand on the top edge of the form, looking to the lens. Bright daylight."),
    ("out-vest-threequarter-l", VEST, OUTS,
     "Chest-up, body turned about 30 degrees to his left, head back to the lens, neutral open "
     "expression. Overcast even light, formwork behind."),
    ("out-polo-front", POLO, OUTS,
     "Waist-up, straight-on at eye level, arms relaxed, calm confident expression into the "
     "lens. Curved formwork clearly behind him. Bright daylight."),
    ("out-polo-profile-l", POLO, OUTS,
     "Chest-up, near profile, head turned about 55 degrees to his left away from the lens, "
     "looking along the line of the formwork. Late afternoon side light, warm tone."),
    ("out-polo-high", POLO, OUTS,
     "Waist-up, camera slightly above eye level looking down as he looks up into the lens. "
     "The form and reinforcement mesh in frame. Bright even daylight."),
    ("out-jumper-front", JUMPER, OUTS,
     "Waist-up, straight-on at eye level, hands in pockets, easy half smile to the lens. "
     "Formwork behind his shoulder. Soft overcast light."),
    ("out-jumper-threequarter-r", JUMPER, OUTS,
     "Chest-up, body turned about 30 degrees to his right, head back to the lens, mid-sentence "
     "speaking. Golden hour side light; the jumper still reads clearly black, not brown."),
    ("out-jumper-threequarter-l", JUMPER, OUTS,
     "Chest-up, body turned about 30 degrees to his left, head back to the lens, listening "
     "expression. Reinforcement mesh and formwork behind. Bright even daylight."),
]

if not 1 <= N <= len(SHOTS):
    raise SystemExit(f"shot number must be 1-{len(SHOTS)}")
slug, wardrobe, setting, framing = SHOTS[N - 1]
dest = os.path.join(OUT, f"{N:02d}-{slug}.png")
prompt = f"{LOCK}\n\nHe wears {wardrobe}.\n\n{setting}\n\n{framing}"


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


p = api(f"/models/{MODEL}/predictions", {"input": {
    "prompt": prompt,
    "image_input": [upload(HERO)],
    "aspect_ratio": "4:5",
    "resolution": "2K",
    "output_format": "png",
    "safety_filter_level": "block_only_high",
}})
while p["status"] not in ("succeeded", "failed", "canceled"):
    time.sleep(3)
    p = api(f"/predictions/{p['id']}")
if p["status"] != "succeeded":
    raise SystemExit(f"failed: {p.get('error') or p['status']}")

o = p["output"]
urllib.request.urlretrieve(o[0] if isinstance(o, list) else o, dest)
print(f"shot {N:02d}  {slug}  -> {dest}  ({os.path.getsize(dest)//1024} KB)")
