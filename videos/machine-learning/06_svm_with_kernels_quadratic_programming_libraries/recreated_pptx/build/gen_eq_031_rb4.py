#!/usr/bin/env python3
"""Slide 031 eq assets, round 4: fill the spec boxes (larger, legible 2D math).

Same rows as gen_eq_031_rb3.py (correct a,b variables, attached superscripts),
but font sizing uses the full box height/width so exponents stay readable at
150 dpi renders. Writes eq_031/*.png + manifest.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import render_math
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_031")
os.makedirs(OUT, exist_ok=True)

W, H = 13.33, 7.5
DPI = render_math.DPI


def box(x0, y0, x1, y1):
    return (x0 * W, y0 * H, (x1 - x0) * W, (y1 - y0) * H)


# name -> (row, spec box)
EQS = {
    "eq1": ("CC0000:\\boldsymbol{K}||000000:(a,b)=||CC0000:a^{T}b",
            (0.121, 0.246, 0.217, 0.289)),
    "eq_phi": ("CC0000:\\text{No Mapping , }\\phi(x)=\\ x",
               (0.344, 0.250, 0.517, 0.291)),
    "eq2": ("CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:a^{T}b||000000:]^{2}",
            (0.125, 0.387, 0.235, 0.431)),
    "eq3": ("CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:a^{T}b||000000:\\ +\\ 1]^{2}",
            (0.408, 0.387, 0.535, 0.431)),
    "eq4": ("CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:a^{T}b||CC0000:]^{d}",
            (0.121, 0.533, 0.238, 0.580)),
    "eq5": ("CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:a^{T}b||000000:\\ +\\ 1||CC0000:]^{d}",
            (0.408, 0.533, 0.560, 0.580)),
    "eq6": ("CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:e^{-\\gamma\\|a-b\\|^{2}}||000000:]",
            (0.129, 0.717, 0.333, 0.770)),
}

PROBE_PT = 18.0
manifest = {}
for name, (row, b) in EQS.items():
    x, y, box_w, box_h = box(*b)
    probe = render_math.render_row(row, PROBE_PT)
    ink = probe[:, :, 3] > 40
    ys, xs = np.nonzero(ink)
    ink_w = (xs.max() - xs.min() + 1) / DPI
    ink_h = (ys.max() - ys.min() + 1) / DPI
    pt_h = PROBE_PT * (0.98 * box_h) / ink_h
    pt_w = PROBE_PT * (0.98 * box_w) / ink_w
    pt = min(pt_h, pt_w, 48.0)
    canvas = render_math.render_row(row, pt)
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
    manifest[name] = {"file": name + ".png", "x": round(x, 4), "y": round(y, 4),
                      "w_in": round(w_in, 5), "h_in": round(h_in, 5), "pt": round(pt, 2)}
    print(name, "w_in=%.3f h_in=%.3f pt=%.1f" % (w_in, h_in, pt))

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
