#!/usr/bin/env python3
"""Re-render slide_003 equation PNGs with the stix mathtext fontset.

The cm fontset renders some bold glyphs (h) as wrong shapes; stix was the
validated fix in other slides' fix-passes (e.g. gen_eq_021_fix.py).
Writes eq_003/<name>.png + <name>.json (same schema render_math emits).
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_math as rm

matplotlib.rcParams["mathtext.fontset"] = "stix"
matplotlib.rcParams["mathtext.default"] = "it"

OUT = os.path.join(HERE, "eq_003")
os.makedirs(OUT, exist_ok=True)

OBJ = ("#000000:\\frac{1}{2}||#000000:[||#0000FF:\\mathbf{X}^{T}||"
       "#FF0000:\\mathbf{P}||#0000FF:\\mathbf{X}||#000000:]||#000000:+||"
       "#FF0000:\\mathbf{q}^{T}||#0000FF:\\mathbf{X}")
GXH = "#FF0000:\\mathbf{G}||#0000FF:\\mathbf{x}||#000000:\\leq||#0000FF:\\mathbf{h}"
AXB = "#FF0000:\\mathbf{A}||#0000FF:\\mathbf{x}||#000000:=||#0000FF:\\mathbf{b}"

ASSETS = [
    ("eq_obj", 26, 2.40, 0.80, [OBJ]),
    ("eq_gxleh", 24, 1.00, 0.42, [GXH]),
    ("eq_axeqb", 24, 1.00, 0.42, [AXB]),
]

for name, size, maxw, maxh, rows in ASSETS:
    png = os.path.join(OUT, name + ".png")
    canvases, sizes = [], []
    for row in rows:
        c, pt = rm.fit_row(row, size, maxw, maxh)
        canvases.append(c)
        sizes.append(pt)
    w = max(c.shape[1] for c in canvases)
    h = sum(c.shape[0] for c in canvases)
    import numpy as np
    from PIL import Image
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    y = 0
    for c in canvases:
        x = (w - c.shape[1]) // 2
        canvas[y:y + c.shape[0], x:x + c.shape[1]] = c
        y += c.shape[0]
    Image.fromarray(canvas).save(png)
    info = {"path": "eq_003/" + name + ".png", "w_px": int(w), "h_px": int(h),
            "w_in": round(w / rm.DPI, 5), "h_in": round(h / rm.DPI, 5),
            "dpi": rm.DPI, "fontsize_pt": sizes, "rows": rows}
    with open(os.path.join(OUT, name + ".json"), "w") as fh:
        json.dump(info, fh, indent=2)
    print(json.dumps(info))
