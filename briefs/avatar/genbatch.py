#!/usr/bin/env python3
"""Generate the remaining 25 identity-set images. Idempotent — skips existing files."""
import base64, json, os, time, requests
from concurrent.futures import ThreadPoolExecutor

os.chdir(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.environ["REPLICATE_API_TOKEN"]
API = "https://api.replicate.com/v1"
HDR = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
MIME = {"png": "image/png", "webp": "image/webp", "jpg": "image/jpeg"}

def uri(p):
    return f"data:{MIME[p.rsplit('.',1)[1]]};base64," + base64.b64encode(open(p, "rb").read()).decode()

MASTER = uri("hero-master.png")
REFS = {"hoodie": uri("ref-03.webp"), "whitetee": uri("ref-05.webp"), "greencrew": uri("ref-07.webp")}

IDENT = ("IDENTITY LOCK: the man in image 1 is the subject. Reproduce his face exactly — same bone "
"structure, blue-grey eyes, dark brown swept-back hair, short trimmed beard, natural skin texture "
"with visible pores, mid-30s. ")
CLOTH = ("The additional image is ONLY a clothing reference — completely ignore the face, hair and "
"identity of the person in it. ")
STYLE = ("Photorealistic editorial photograph, 50mm lens, shallow depth of field, background softly "
"out of focus, natural colour grade, no beauty retouching, no logos, badges or text anywhere in the "
"image. The background is an INTERIOR or studio only — absolutely NO construction site, NO formwork, "
"NO scaffolding, NO timber structures, NO machinery in the background.")

OUTFITS = {
 "workkit":   (None, "He wears his exact outfit from image 1: plain matte black puffer vest with no "
               "logos over a plain khaki short-sleeve work shirt. "),
 "khaki":     (None, "He wears only the plain khaki short-sleeve work shirt from image 1 (no vest), "
               "buttons done up, sleeves natural. "),
 "hoodie":    ("hoodie", "Dress the subject in the plain black hooded sweatshirt and blue jeans from "
               "the clothing reference image. "),
 "whitetee":  ("whitetee", "Dress the subject in the plain white crew-neck t-shirt and olive chinos "
               "from the clothing reference image. "),
 "greencrew": ("greencrew", "Dress the subject in the dark forest-green knitted crew-neck jumper from "
               "the clothing reference image, but make the jumper COMPLETELY PLAIN — no chest logo, "
               "no text, unbroken fabric. "),
 "navy":      (None, "Dress the subject in a plain dark navy wool overshirt (shirt-jacket with two "
               "chest flap pockets and buttons, no logos) worn open over a plain dark navy t-shirt. "),
}

ANGLES = {
 "straight": "facing the camera straight-on, ",
 "slight":   "body and head turned about 15-20 degrees away from camera, eyes to camera, ",
 "threeq":   "body turned about 35 degrees, three-quarter view of the face, eyes to camera, ",
 "tiltup":   "photographed from slightly below eye level looking gently up at him, facing camera, ",
 "tiltdown": "photographed from slightly above eye level looking gently down at him, facing camera, ",
}
FRAMES = {
 "closeup": "close-up framing from the chest up, face large in frame, ",
 "half":    "half-body framing from the waist up, ",
 "wide":    "three-quarter-length framing from mid-thigh up, ",
}
EXPRS = {
 "neutral": "relaxed neutral expression, mouth fully closed, ",
 "smile":   "warm friendly smile with lips CLOSED, no teeth visible, ",
 "talking": "captured mid-sentence while speaking naturally, mouth slightly open as if talking, ",
 "listen":  "attentive listening expression, slight head tilt, mouth closed, ",
 "serious": "focused, serious explaining expression, brows slightly drawn, mouth closed, ",
}
SCENES = {
 "studio":   "standing against a seamless mid-grey studio backdrop, soft three-point studio lighting. ",
 "unfinished":"in a bright unfinished new-build interior with bare plastered walls thrown well out of "
              "focus, natural window light from camera-left. ",
 "office":   "in a warm modern timber-and-white office interior, background well out of focus, soft "
              "window light. ",
 "homeoffice":"in a bright minimal home office with plants and timber shelving far out of focus, "
              "natural daylight. ",
 "overcast": "near a large window on an overcast day, soft even diffused light, plain interior behind "
             "him out of focus. ",
 "darkwall": "against a plain deep-charcoal interior wall, single soft key light from camera-left, "
             "gentle falloff. ",
}

# 25 jobs: outfit, angle, frame, expression, scene
J = [
 ("workkit","straight","closeup","neutral","studio"),
 ("workkit","straight","closeup","talking","studio"),
 ("workkit","slight","closeup","smile","unfinished"),
 ("workkit","slight","half","serious","office"),
 ("workkit","threeq","closeup","neutral","overcast"),
 ("workkit","threeq","half","listen","unfinished"),
 ("workkit","tiltup","half","neutral","studio"),
 ("workkit","straight","wide","smile","unfinished"),
 ("khaki","straight","closeup","talking","office"),
 ("khaki","slight","half","neutral","overcast"),
 ("hoodie","straight","closeup","smile","homeoffice"),
 ("hoodie","threeq","closeup","serious","darkwall"),
 ("hoodie","slight","half","listen","homeoffice"),
 ("whitetee","straight","closeup","neutral","studio"),
 ("whitetee","slight","closeup","talking","homeoffice"),
 ("whitetee","threeq","half","smile","overcast"),
 ("whitetee","tiltdown","half","neutral","office"),
 ("greencrew","straight","closeup","smile","office"),
 ("greencrew","slight","closeup","neutral","darkwall"),
 ("greencrew","straight","half","talking","homeoffice"),
 ("greencrew","threeq","wide","listen","office"),
 ("navy","straight","closeup","neutral","overcast"),
 ("navy","slight","closeup","serious","darkwall"),
 ("navy","straight","half","smile","homeoffice"),
 ("navy","slight","wide","serious","studio"),
]

def predict(model, inp, tag, tries=6):
    for a in range(tries):
        try:
            r = requests.post(f"{API}/models/{model}/predictions", headers=HDR,
                              json={"input": inp}, timeout=180)
            if r.status_code not in (200, 201):
                print(tag, "create fail", r.status_code, flush=True); time.sleep(15); continue
            url = r.json()["urls"]["get"]
            while True:
                time.sleep(4)
                p = requests.get(url, headers=HDR, timeout=30).json()
                if p["status"] in ("succeeded", "failed", "canceled"): break
            if p["status"] == "succeeded":
                out = p["output"]; return out if isinstance(out, str) else out[0]
            err = str(p.get("error"))[:90]
            print(tag, "attempt", a + 1, err, flush=True)
            time.sleep(25 * (a + 1) if ("E003" in err or "RateLimit" in err) else 6)
        except Exception as e:
            print(tag, "exc", str(e)[:90], flush=True); time.sleep(10)
    return None

def run(i, job):
    outfit, angle, frame, expr, scene = job
    name = f"set-{i+6:02d}-{outfit}-{angle}-{expr}"
    if os.path.exists(f"{name}.png"): print(name, "exists", flush=True); return name, True
    refkey, garment = OUTFITS[outfit]
    imgs = [MASTER] + ([REFS[refkey]] if refkey else [])
    prompt = (IDENT + (CLOTH if refkey else "") + garment + "Scene: " + FRAMES[frame] +
              ANGLES[angle] + EXPRS[expr] + SCENES[scene] + STYLE)
    out = predict("google/nano-banana",
                  {"prompt": prompt, "image_input": imgs, "aspect_ratio": "3:4",
                   "output_format": "png"}, name)
    if not out: return name, False
    raw = requests.get(out, timeout=120).content
    open(f"{name}-raw.png", "wb").write(raw)
    b64 = base64.b64encode(raw).decode()
    up = predict("nightmareai/real-esrgan",
                 {"image": f"data:image/png;base64,{b64}", "scale": 2, "face_enhance": False},
                 name + "-up", tries=3)
    if up:
        open(f"{name}.png", "wb").write(requests.get(up, timeout=120).content)
        os.remove(f"{name}-raw.png")
    else:
        os.rename(f"{name}-raw.png", f"{name}.png")
    print(name, "DONE", flush=True)
    return name, True

results = []
with ThreadPoolExecutor(max_workers=3) as ex:
    futs = [ex.submit(run, i, j) for i, j in enumerate(J)]
    for f in futs: results.append(f.result())

manifest = [{"file": n + ".png", "outfit": j[0], "angle": j[1], "frame": j[2],
             "expr": j[3], "scene": j[4], "ok": ok}
            for (n, ok), j in zip(results, J)]
json.dump(manifest, open("manifest.json", "w"), indent=1)
fails = [n for n, ok in results if not ok]
print("COMPLETE. ok:", len(results) - len(fails), "failed:", fails, flush=True)
