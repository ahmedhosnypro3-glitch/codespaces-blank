#!/usr/bin/env python3
"""Wave-3 fix for slide_032 equations: smaller fitted size (was oversized, collided
with panel headers) and original-faithful colors (K base blue, K_1/K_2/K_3 red,
alpha green — verified by pixel counts on the original frame). Writes eq_032/*.png
plus manifest.json with centered placement inside the spec equation boxes."""
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

# name -> (row, spec eq box [x0,y0,x1,y1] normalized)
EQS = {
    "eq1": ("0000FF:K(a,b)||000000: = ||FF0000:K_{1}(a,b)||000000: + ||FF0000:K_{2}(a,b)",
            (0.10, 0.29, 0.90, 0.41)),
    "eq2": ("0000FF:K(a,b)||000000: = ||008000:\\alpha\\,||FF0000:K_{1}(a,b)",
            (0.10, 0.51, 0.75, 0.58)),
    "eq3": ("0000FF:K(a,b)||000000: = ||FF0000:K_{1}(a,b)||000000: \\ast ||FF0000:K_{2}(a,b)",
            (0.10, 0.67, 0.85, 0.75)),
    "eq4": ("0000FF:K(a,b)||000000: = ||FF0000:K_{1}(a,b)||000000: \\ast ||FF0000:K_{2}(a,b)||000000: + ||008000:\\alpha\\,||FF0000:K_{3}(a,b)",
            (0.10, 0.84, 0.92, 0.92)),
}

manifest = {}
for name, (row, b) in EQS.items():
    bx, by = b[0] * W, b[1] * H
    bw, bh = (b[2] - b[0]) * W, (b[3] - b[1]) * H
    canvas = render_math.render_row(row, 24.0)
    pt = 24.0
    w_in0, h_in0 = canvas.shape[1] / DPI, canvas.shape[0] / DPI
    if w_in0 > 0.92 * bw or h_in0 > 0.85 * bh:
        canvas, pt = render_math.fit_row(row, 24.0, 0.92 * bw, 0.85 * bh)
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
    x = bx + (bw - w_in) / 2
    y = by + (bh - h_in) / 2
    manifest[name] = {"file": name + ".png", "x": round(x, 4), "y": round(y, 4),
                      "w_in": round(w_in, 5), "h_in": round(h_in, 5), "pt": round(pt, 2)}
    with open(os.path.join(OUT, name + ".json"), "w") as fh:
        json.dump({"path": "eq_032/" + name + ".png", "w_px": int(canvas.shape[1]),
                   "h_px": int(canvas.shape[0]), "w_in": round(w_in, 5),
                   "h_in": round(h_in, 5), "dpi": DPI, "fontsize_pt": pt, "row": row},
                  fh, indent=2)
    print(name, "w_in=%.3f h_in=%.3f pt=%.1f" % (w_in, h_in, pt))

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
