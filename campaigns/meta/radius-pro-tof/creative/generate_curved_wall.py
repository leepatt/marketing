#!/usr/bin/env python3
"""Generate the AD4/AD5 curved-wall carousel pair (BEFORE frame / AFTER finished).

Governed by CURVED-WALL-BUILD-SPEC.md. Prompts here restate that spec; if the spec
changes, fix the spec first, then update the prompts to match.

Usage:
  python3 generate_curved_wall.py after   # flux-kontext-pro rework of IMG_5539
  python3 generate_curved_wall.py before  # nano-banana frame build from refs
  python3 generate_curved_wall.py export <in.png> <slug>  # 4:5 + 1:1 crops

Reference images are expected in REF_DIR (session-scoped uploads, copied there
by hand). They are gitignored; keep copies in the Drive brain.

Requires: REPLICATE_API_TOKEN in env, pillow, requests (stdlib urllib used to
avoid extra deps).
"""

import base64
import json
import mimetypes
import os
import sys
import time
import urllib.request
import urllib.error

REF_DIR = os.environ.get("REF_DIR", os.path.join(os.path.dirname(__file__), "refs"))
OUT_DIR = os.environ.get("OUT_DIR", os.path.join(os.path.dirname(__file__), "out"))
API = "https://api.replicate.com/v1"
TOKEN = os.environ["REPLICATE_API_TOKEN"]

# ---------------------------------------------------------------- prompts ----

# The construction facts, shared by both prompts (from CURVED-WALL-BUILD-SPEC.md).
SPEC_FRAME = (
    "A curved timber stud wall under construction on a real Australian building site. "
    "The wall is ONE soft CONVEX curve that joins two straight wall runs, bulging toward "
    "the camera. It is NOT a cylinder, NOT a drum, NOT a pod, NOT concave. Full height, "
    "from the concrete slab up to the underside of exposed timber roof trusses. "
    "Top and bottom plates are curved 34mm black Formply: two 17mm sheets laminated "
    "together, flat faces matte black phenolic, edges showing pale plywood grain layers. "
    "The plates are 90mm wide, exactly the same width as the studs, flush with the stud "
    "faces on both sides, no overhang. The black curved bottom plate sits directly on the "
    "bare pale concrete slab and contrasts dark against it. "
    "Studs are 90x35mm pine, plumb, evenly spaced at 125mm centres, close together, with "
    "the narrow 35mm face toward the camera, following the curve. "
    "One single row of solid timber noggin blocks at mid height, each about 150mm high, "
    "grain running vertical, the row slightly uneven: two or three blocks sit roughly 5mm "
    "above or below the line, hand-built not laser perfect. "
    "Genuine mid-build scene with ZERO finished work: bare swept concrete slab with light "
    "dust, exposed roof trusses overhead, no plasterboard, no ceiling lining, no doors, "
    "no door jambs, no architraves, no skirting, no finished flooring anywhere. Any "
    "openings are raw timber framed. No steel strapping, no text, no logos, no people. "
    "Natural daylight, phone-photo realism, shot like a tradie's photo on site."
)

PROMPT_AFTER = (
    "Rework this photo into a different, original interior while keeping the exact same "
    "camera viewpoint and the exact same curved wall geometry: a smooth full-height "
    "CONVEX plastered curved feature wall that joins two straight walls, bulging toward "
    "the camera. Keep the curve line identical. Change everything else enough to make it "
    "a different home: replace the herringbone timber floor with wide-board pale oak "
    "flooring laid straight, change the lighting to warm late-afternoon sun with soft "
    "shadows raking across the curved wall, and change the room visible beyond the "
    "opening to a simple neutral living space with different furniture. Crisp white "
    "painted plaster on the curved wall, clean modern Australian residential finish. "
    "No text, no logos, no people. Photorealistic, natural, like a real estate photo "
    "taken on a phone."
)

# BEFORE: refine the best frame render so it fully matches the spec.
PROMPT_BEFORE = (
    "Using the finished curved wall photo as the shape and viewpoint reference, and the "
    "site framing photos as the build-detail reference, produce the SAME curved wall at "
    "the SAME camera viewpoint, but as a bare timber frame mid-construction. "
    + SPEC_FRAME
    + " Behind the studs there is only open air and the rest of the building site, no "
    "grey backing board, no lining behind the frame. Through any framed opening you see "
    "more raw site: bare slab and framing, never a finished room."
)

# ------------------------------------------------------------- replicate ----


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def api(method, url, payload=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    body = json.dumps(payload).encode() if payload is not None else None
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, body) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 2 ** (attempt + 1)
                print(f"429 rate limited, retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            print(e.read().decode(), file=sys.stderr)
            raise
    raise RuntimeError("gave up after repeated 429s")


def run_model(model, inputs, out_path):
    pred = api("POST", f"{API}/models/{model}/predictions", {"input": inputs})
    url = pred["urls"]["get"]
    while pred["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(3)
        pred = api("GET", url)
    if pred["status"] != "succeeded":
        raise RuntimeError(f"{model} {pred['status']}: {pred.get('error')}")
    out = pred["output"]
    if isinstance(out, list):
        out = out[0]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    urllib.request.urlretrieve(out, out_path)
    print(f"saved {out_path}")
    return out_path


# --------------------------------------------------------------- exports ----


def export(src, slug):
    from PIL import Image

    img = Image.open(src).convert("RGB")
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, (tw, th) in {"4x5": (1080, 1350), "1x1": (1080, 1080)}.items():
        w, h = img.size
        scale = max(tw / w, th / h)
        r = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        left = (r.width - tw) // 2
        top = (r.height - th) // 2
        crop = r.crop((left, top, left + tw, top + th))
        path = os.path.join(OUT_DIR, f"{slug}_{name}_{tw}x{th}.png")
        crop.save(path)
        print(f"saved {path}")


# ------------------------------------------------------------------ main ----


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "after":
        run_model(
            "black-forest-labs/flux-kontext-pro",
            {
                "prompt": PROMPT_AFTER,
                "input_image": data_uri(os.path.join(REF_DIR, "IMG_5539.jpg")),
                "aspect_ratio": "4:5",
                "output_format": "png",
                "safety_tolerance": 2,
            },
            os.path.join(OUT_DIR, "raw_after_finished.png"),
        )
    elif cmd == "before":
        refs = [
            os.path.join(REF_DIR, "IMG_5539.jpg"),  # shape + viewpoint (MAIN)
            os.path.join(REF_DIR, "IMG_5548.png"),  # best frame so far
            os.path.join(REF_DIR, "IMG_5545.jpg"),  # real framing detail
        ]
        run_model(
            "google/nano-banana",
            {
                "prompt": PROMPT_BEFORE,
                "image_input": [data_uri(p) for p in refs if os.path.exists(p)],
                "output_format": "png",
            },
            os.path.join(OUT_DIR, "raw_before_frame.png"),
        )
    elif cmd == "export" and len(sys.argv) == 4:
        export(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
