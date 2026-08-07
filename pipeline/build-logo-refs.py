#!/usr/bin/env python3
"""Render the Craftons lockup reference images the avatar shoot feeds to the model.

Two colourways, both straight from the official vector so the letterforms and the
mark are exact rather than whatever the model imagines:

  logo-lockup-2col.png   green four-lobe mark + white "Craftons" — the house
                         treatment, used on black and khaki garments
  logo-lockup-white.png  mark and wordmark both white — used on the Craftons-green
                         jumper, where a green mark would sit green-on-green

    python3 build-logo-refs.py <path-to-craftons-logo.svg> <out-dir>

The SVG lives in the cnccut-app repo at
content-engine/public/brand/logo/craftons-logo.svg.
"""
import os, sys
import cairosvg

SVG, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
src = open(SVG).read()

# In the source vector the two halves of the lockup are coloured differently:
# the mark is drawn as strokes (stroke:#42a661, fill:none), the wordmark as a
# filled group (fill:#194431). So they have to be recoloured separately —
# a blanket fill swap silently leaves the mark green.
MARK = "stroke:#42a661"
WORD = "fill:#194431"
DARK = "#141414"   # stand-in garment ground so the model reads the lockup as reversed

for name in (MARK, WORD):
    if name not in src:
        raise SystemExit(f"'{name}' not found in the SVG — the source has changed, "
                         "re-check its colour declarations before trusting this output")

# --- house treatment: green mark, white wordmark (black and khaki garments) ---
two = src.replace(WORD, "fill:#ffffff")
cairosvg.svg2png(bytestring=two.encode(), write_to=os.path.join(OUT, "logo-lockup-2col.png"),
                 output_width=1600, background_color=DARK)

# --- all white (the Craftons-green jumper, where green-on-green would vanish) ---
white = src.replace(WORD, "fill:#ffffff").replace(MARK, "stroke:#ffffff")
cairosvg.svg2png(bytestring=white.encode(), write_to=os.path.join(OUT, "logo-lockup-white.png"),
                 output_width=1600, background_color=DARK)

print(f"wrote logo-lockup-2col.png and logo-lockup-white.png -> {OUT}")
