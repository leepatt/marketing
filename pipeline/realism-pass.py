#!/usr/bin/env python3
"""Take the plastic off a generated portrait without changing who is in it.

Generated faces skew young and airbrushed — poreless skin, an evenly dyed beard,
no lines. This pass adds back what a real forty-year-old face has, and changes
nothing else: same pose, framing, wardrobe, background, lighting and expression.

    REPLICATE_API_TOKEN=... python3 realism-pass.py <in.png> <out.png> [strength]

strength: 'subtle' | 'default' | 'strong'  (default: 'default')

Run this on the hero frame first, approve it, then use the result as the face
reference for the rest of the shoot — every downstream frame inherits the texture
instead of needing its own pass.

Two things to know about the output. It is a re-render, not a pixel edit: the
frame comes back within about 1% of the original across the background, which is
re-render noise rather than drift, but it is not byte-identical. And it tends to
drop small generator watermarks from the source image on its own — convenient,
but check the corners rather than assume, since it is not something this prompt
asks for or can guarantee.
"""
import json, os, sys, time, urllib.request

TOKEN = os.environ["REPLICATE_API_TOKEN"]
MODEL = "google/nano-banana-pro"
SRC, DEST = sys.argv[1], sys.argv[2]
STRENGTH = sys.argv[3] if len(sys.argv) > 3 else "default"

PRESERVE = (
    "Keep absolutely everything else in this photograph identical: the same man, the same "
    "face and bone structure, the same hairstyle, the same expression, the same pose and "
    "head angle, the same wardrobe, the same background, the same lighting and the same "
    "framing and crop. Do not move him, do not re-pose him, do not change the composition, "
    "do not restyle his hair or clothing. This is a texture and detail pass on the skin and "
    "beard only — it must read as the same photograph, retouched less."
)

DETAIL = {
    "subtle": (
        "Add believable skin texture: visible pores across the nose, cheeks and forehead, "
        "faint fine lines at the outer corners of the eyes, and a slightly uneven, natural "
        "complexion. A few scattered grey hairs through the beard."
    ),
    "default": (
        "Give him the skin of a real man of about forty who works outdoors in Australia. "
        "Visible pores across the nose, cheeks and forehead. Fine crow's-feet at the outer "
        "corners of both eyes and faint horizontal forehead lines that show even at rest. "
        "Soft nasolabial folds and the beginnings of lines at the neck. Mild under-eye "
        "shadowing. An uneven, slightly ruddy complexion across the cheeks and nose with "
        "light sun freckling on the cheekbones and forehead. Two or three small natural "
        "blemishes — a mole near the jaw or temple, a small mark on the cheek — nothing "
        "dramatic or medical. Lips with a little dryness and natural texture. "
        "The beard is real stubble, uneven in density, longer at the chin than the cheeks, "
        "with a scattering of grey and white hairs through it, concentrated at the chin and "
        "sideburns, plus a few greys at the temples. Individual hairs are visible rather "
        "than a smooth mass."
    ),
    "strong": (
        "Give him the weathered skin of a man of about forty-five who has spent years on "
        "site in the Australian sun. Coarse visible pores, clear crow's-feet and forehead "
        "lines, deep nasolabial folds, neck lines, pronounced under-eye shadowing, uneven "
        "ruddy patches on the cheeks and nose, visible sun damage and freckling, several "
        "small moles and blemishes, dry textured lips, and a noticeably salt-and-pepper "
        "beard with heavy grey through the chin, jaw and sideburns."
    ),
}
if STRENGTH not in DETAIL:
    raise SystemExit(f"strength must be one of {list(DETAIL)}")

PROMPT = (
    f"{DETAIL[STRENGTH]}\n\n{PRESERVE}\n\n"
    "Photorealistic, shot on a full-frame camera, natural unretouched skin, no beauty "
    "filter, no smoothing, no airbrushing, no skin softening, not CGI, not a render. "
    "He should look like a real person photographed on a normal day, not a model in a "
    "campaign. Do NOT make him look younger, do NOT make him more handsome, do NOT "
    "clean him up."
)


def api(path, data=None):
    req = urllib.request.Request(
        f"https://api.replicate.com/v1{path}",
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def upload(path):
    b = "----craftonsrealism"
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
p = api(f"/models/{MODEL}/predictions", {"input": {
    "prompt": PROMPT,
    "image_input": [src_url],
    # match_input_image keeps the original framing — anything else recrops him.
    "aspect_ratio": "match_input_image",
    "resolution": "4K",
    "output_format": "png",
    "safety_filter_level": "block_only_high",
}})
while p["status"] not in ("succeeded", "failed", "canceled"):
    time.sleep(3)
    p = api(f"/predictions/{p['id']}")
if p["status"] != "succeeded":
    raise SystemExit(f"failed: {p.get('error') or p['status']}")

o = p["output"]
urllib.request.urlretrieve(o[0] if isinstance(o, list) else o, DEST)
print(f"{STRENGTH} pass -> {DEST} ({os.path.getsize(DEST)//1024} KB)")
