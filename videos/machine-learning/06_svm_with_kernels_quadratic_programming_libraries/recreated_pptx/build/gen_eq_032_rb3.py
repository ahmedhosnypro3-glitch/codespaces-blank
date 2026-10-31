#!/usr/bin/env python3
"""Wave-3 final slide_032 equations: 24pt, colors pixel-verified on the original
(K base blue, K_1/K_2/K_3 red, alpha green), LEFT-aligned in each panel at
x=0.059 (original ink edge), vertically centered in the panel's equation band.
Writes eq_032/*.png + manifest.json (x,y = top-left inches)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_math
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_032")
os.makedirs(OUT, exist_ok=True)

W, H = 13.33, 7.5
DPI = render_math.DPI

# name -> (row, equation band [x0,y0,x1,y1] normalized — left-aligned at x0)
EQS = {
    "eq1": ("0000FF:K(a,b)||000000: = ||FF0000:K_{1}(a,b)||000000: + ||FF0000:K_{2}(a,b)",
            (0.059, 0.335, 0.69, 0.42)),
    "eq2": ("0000FF:K(a,b)||000000: = ||008000:\\alpha\\,||FF0000:K_{1}(a,b)",
            (0.059, 0.49, 0.69, 0.575)),
    "eq3": ("0000FF:K(a,b)||000000: = ||FF0000:K_{1}(a,b)||000000: \\ast ||FF0000:K_{2}(a,b)",
            (0.059, 0.645, 0.69, 0.73)),
    "eq4": ("0000FF:K(a,b)||000000: = ||FF0000:K_{1}(a,b)||000000: \\ast ||FF0000:K_{2}(a,b)||000000: + ||008000:\\alpha\\,||FF0000:K_{3}(a,b)",
            (0.059, 0.81, 0.69, 0.90)),
}

manifest = {}
for name, (row, b) in EQS.items():
    bx, by = b[0] * W, b[1] * H
    bw, bh = (b[2] - b[0]) * W, (b[3] - b[1]) * H
    canvas = render_math.render_row(row, 24.0)
    pt = 24.0
    w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
    if w_in > 0.95 * bw or h_in > 0.9 * bh:
        canvas, pt = render_math.fit_row(row, 24.0, 0.95 * bw, 0.9 * bh)
        w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    x = bx  # left-aligned per original
    y = by + (bh - h_in) / 2
    manifest[name] = {"file": name + ".png", "x": round(x, 4), "y": round(y, 4),
                      "w_in": round(w_in, 5), "h_in": round(h_in, 5), "pt": round(pt, 2)}
    with open(os.path.join(OUT, name + ".json"), "w") as fh:
        json.dump({"path": "eq_032/" + name + ".png", "w_px": int(canvas.shape[1]),
                   "h_px": int(canvas.shape[0]), "w_in": round(w_in, 5),
                   "h_in": round(h_in, 5), "dpi": DPI, "fontsize_pt": pt, "row": row},
                  fh, indent=2)
    print(name, "x=%.3f y=%.3f w_in=%.3f h_in=%.3f pt=%.1f" % (x, y, w_in, h_in, pt))

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
