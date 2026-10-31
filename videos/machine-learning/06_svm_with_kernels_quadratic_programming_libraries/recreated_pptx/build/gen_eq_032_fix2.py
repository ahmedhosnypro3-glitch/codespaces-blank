#!/usr/bin/env python3
"""Slide_032 fix round 2: regenerate the four kernel-closure equations from the
pixel-verified original frame (qa/rejudge2/orig_png/slide_032.png).

Verified on the original (960x540): equations are LEFT-aligned starting x~0.15,
K(a,b) and operators are black, K_1/K_2/K_3 terms red, alpha green; glyph rows
sit in the lower half of each panel. Panels span x 0.08-0.696.
Writes eq_032_fix2/*.png + manifest.json with exact placement (inches)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_math
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_032_fix2")
os.makedirs(OUT, exist_ok=True)

W, H = 13.33, 7.5
DPI = render_math.DPI

# name -> (row, [x0, x1, y_center] normalized fractions measured on the original)
EQS = {
    "eq1": ("000000:K(a,b)||000000: = ||FF0000:K_{1}(a,b)||000000: + ||FF0000:K_{2}(a,b)",
            (0.149, 0.408, 0.3845)),
    "eq2": ("000000:K(a,b)||000000: = ||008000:\\alpha\\,||FF0000:K_{1}(a,b)",
            (0.151, 0.314, 0.5510)),
    "eq3": ("000000:K(a,b)||000000: = ||FF0000:K_{1}(a,b)||000000: \\ast ||FF0000:K_{2}(a,b)",
            (0.155, 0.412, 0.7095)),
    "eq4": ("000000:K(a,b)||000000: = ||FF0000:K_{1}(a,b)||000000: \\ast ||FF0000:K_{2}(a,b)||000000: + ||008000:\\alpha\\,||FF0000:K_{3}(a,b)",
            (0.153, 0.535, 0.8740)),
}

manifest = {}
for name, (row, (x0, x1, yc)) in EQS.items():
    target_w = (x1 - x0) * W * 1.03
    canvas, pt = render_math.fit_row(row, 22.0, target_w, 0.42)
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
    x = x0 * W
    y = yc * H - h_in / 2
    manifest[name] = {"file": name + ".png", "x": round(x, 4), "y": round(y, 4),
                      "w_in": round(w_in, 5), "h_in": round(h_in, 5), "pt": round(pt, 2)}
    with open(os.path.join(OUT, name + ".json"), "w") as fh:
        json.dump({"path": "eq_032_fix2/" + name + ".png", "w_px": int(canvas.shape[1]),
                   "h_px": int(canvas.shape[0]), "w_in": round(w_in, 5),
                   "h_in": round(h_in, 5), "dpi": DPI, "fontsize_pt": pt, "row": row},
                  fh, indent=2)
    print(name, "x=%.3f y=%.3f w_in=%.3f h_in=%.3f pt=%.1f" % (x, y, w_in, h_in, pt))

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
