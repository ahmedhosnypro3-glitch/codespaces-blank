#!/usr/bin/env python3
"""Fix slide_032 kernel-combination equations: regenerate eq_032/*.png with
render_math (single mathtext expressions, subscripts as K_{1} etc. attached
to the K base). Old PNGs rendered doubled subscripts. Manifest stores the
final centered placement (x,y = top-left inches) for slide_032.js."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import render_math
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_032")
os.makedirs(OUT, exist_ok=True)

W, H = 13.33, 7.5
DPI = render_math.DPI

# name -> (row, spec box, max width cap in inches)
EQS = {
    "eq1": ("0000FF:K(a,b)||000000: = ||008000:K_{1}(a,b)||000000: + ||FF0000:K_{2}(a,b)",
            (0.10, 0.29, 0.90, 0.41), 8.0),
    "eq2": ("0000FF:K(a,b)||000000: = ||FF0000:\\alpha\\,||008000:K_{1}(a,b)",
            (0.10, 0.51, 0.75, 0.58), 6.5),
    "eq3": ("0000FF:K(a,b)||000000: = ||008000:K_{1}(a,b)||000000: \\ast ||FF0000:K_{2}(a,b)",
            (0.10, 0.67, 0.85, 0.75), 7.5),
    "eq4": ("0000FF:K(a,b)||000000: = ||008000:K_{1}(a,b)||000000: \\ast ||FF0000:K_{2}(a,b)||000000: + ||FF0000:\\alpha\\,K_{3}(a,b)",
            (0.10, 0.84, 0.92, 0.92), 8.5),
}

PROBE_PT = 22.0
manifest = {}
for name, (row, b, cap_w) in EQS.items():
    bx, by = b[0] * W, b[1] * H
    bw, bh = (b[2] - b[0]) * W, (b[3] - b[1]) * H
    probe = render_math.render_row(row, PROBE_PT)
    ink = probe[:, :, 3] > 40
    ys, xs = np.nonzero(ink)
    ink_w = (xs.max() - xs.min() + 1) / DPI
    ink_h = (ys.max() - ys.min() + 1) / DPI
    pt_h = PROBE_PT * (0.8 * bh) / ink_h
    pt_w = PROBE_PT * min(cap_w, bw) / ink_w
    pt = min(pt_h, pt_w, 40.0)
    canvas = render_math.render_row(row, pt)
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
    x = bx + (bw - w_in) / 2
    y = by + (bh - h_in) / 2
    manifest[name] = {"file": name + ".png", "x": round(x, 4), "y": round(y, 4),
                      "w_in": round(w_in, 5), "h_in": round(h_in, 5), "pt": round(pt, 2)}
    sidecar = {"path": "eq_032/" + name + ".png", "w_px": int(canvas.shape[1]),
               "h_px": int(canvas.shape[0]), "w_in": round(w_in, 5),
               "h_in": round(h_in, 5), "dpi": DPI, "fontsize_pt": pt, "row": row}
    with open(os.path.join(OUT, name + ".json"), "w") as fh:
        json.dump(sidecar, fh, indent=2)
    print(name, "w_in=%.3f h_in=%.3f pt=%.1f" % (w_in, h_in, pt))

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
