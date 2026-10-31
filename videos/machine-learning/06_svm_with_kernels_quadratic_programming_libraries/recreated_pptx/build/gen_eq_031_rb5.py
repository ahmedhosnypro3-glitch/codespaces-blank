#!/usr/bin/env python3
"""Slide 031 eq assets, round 5: fixed large point size (no shrink-to-fit).

Same mathtext rows as rb4 (correct a,b variables, attached superscripts), but
every equation renders at a fixed 26 pt so exponents stay legible at 150 dpi;
placement in slide_031.js uses the natural PNG size. Writes eq_031/*.png +
manifest.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_math
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_031")
os.makedirs(OUT, exist_ok=True)

W, H = 13.33, 7.5
DPI = render_math.DPI
PT = 26.0


def box(x0, y0, x1, y1):
    return (x0 * W, y0 * H, (x1 - x0) * W, (y1 - y0) * H)


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

manifest = {}
for name, (row, b) in EQS.items():
    x, y, box_w, box_h = box(*b)
    canvas = render_math.render_row(row, PT)
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
    manifest[name] = {"file": name + ".png", "x": round(x, 4), "y": round(y, 4),
                      "w_in": round(w_in, 5), "h_in": round(h_in, 5), "pt": PT}
    print(name, "w_in=%.3f h_in=%.3f pt=%.1f" % (w_in, h_in, PT))

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
