#!/usr/bin/env python3
"""Generate slide_029 math assets (RBF kernel slide) as 600-dpi mathtext PNGs.

Each asset is one render_math.fit_row row of "color:latex" segments ("||"
separated), fitted into the spec's normalized region. PNGs land in eq_029/
with manifest.json (x/y/w_in/h_in = px/600 placement); slide_029.js places
them with addImage() at exact size, never rescaled.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_math as rm
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_029")
os.makedirs(OUT, exist_ok=True)

W, H = 13.33, 7.5


def region(x0, y0, x1, y1):
    return (x0 * W, y0 * H, (x1 - x0) * W, (y1 - y0) * H)


# name -> (row, normalized region [x0,y0,x1,y1], base pt, maxw_in, maxh_in)
EQS = {
    # E1: RBF identity in box 1; trailing factors blue-purple, final e^{ab} red
    "e1": ("000000:e^{-\\frac{1}{2}(a-b)^{2}} = e^{-\\frac{1}{2}(a^{2}+b^{2}-2ab)} = "
           "||3333CC:e^{-\\frac{a^{2}}{2}}\\,"
           "||3333CC:e^{-\\frac{b^{2}}{2}}\\,||CC0000:e^{ab}",
           (0.086, 0.170, 0.505, 0.227), 14, 5.6, 0.44),
    # E2: Taylor expansion of e^{ab} in box 2; e^{ab} and trailing infinity red
    "e2": ("CC0000:e^{ab} = "
           "||000000:1 + \\frac{ab}{1!} + \\frac{(ab)^{2}}{2!} + \\frac{(ab)^{3}}{3!} "
           "+ \\frac{(ab)^{4}}{4!} + \\frac{(ab)^{5}}{5!} + ......\\,"
           "||CC0000:\\infty",
           (0.086, 0.266, 0.505, 0.326), 14, 5.45, 0.44),
    # E3 label "e^{ab} =" (red) left of the vector product in box 3
    "e3_eq": ("CC0000:e^{ab} =", (0.090, 0.393, 0.127, 0.426), 14, 0.5, 0.25),
    # E3 row vector: bracketed row of stacked fractions
    "e3_row": ("000000:\\left[\\ \\frac{a}{\\sqrt{1!}}\\ \\frac{a^{2}}{\\sqrt{2!}}\\ "
               "\\frac{a^{3}}{\\sqrt{3!}}\\ \\frac{a^{4}}{\\sqrt{4!}}\\ ...\\ ...\\ \\infty\\ \\right]",
               (0.130, 0.389, 0.365, 0.444), 14, 3.14, 0.42),
    # E3 column vector: bracketed stack of stacked fractions (widened region)
    "e3_col": ("000000:\\left[\\overset{\\frac{1}{b}}{\\frac{\\sqrt{1!}}{b^{2}}}"
               "{\\frac{\\sqrt{2!}}{b^{3}}}{\\frac{\\sqrt{3!}}{b^{4}}}{\\frac{\\sqrt{4!}}{...}}"
               "{...}{...\\ \\infty}\\right]",
               (0.398, 0.395, 0.508, 0.785), 14, 1.45, 2.9),
    # E4: e^x series inside right panel inner box; trailing infinity red
    "e4": ("000000:e^{x} = 1 + \\frac{x}{1!} + \\frac{x^{2}}{2!} + \\frac{x^{3}}{3!} "
           "+ \\frac{x^{4}}{4!} + \\frac{x^{5}}{5!} + ......\\,||CC0000:\\infty",
           (0.533, 0.231, 0.859, 0.281), 13, 4.34, 0.37),
    # E5: e^3 series line; trailing infinity red
    "e5": ("000000:e^{3} = 1 + \\frac{3}{1!} + \\frac{3^{2}}{2!} + \\frac{3^{3}}{3!} "
           "+ \\frac{3^{4}}{4!} + \\frac{3^{5}}{5!} + ......\\,||CC0000:\\infty",
           (0.533, 0.311, 0.854, 0.365), 13, 4.27, 0.40),
    # phi labels on yellow highlights: blue phi, red superscript T
    "phi_a": ("0000CC:\\phi(a)||CC0000:^{\\mathrm{T}}", (0.182, 0.467, 0.251, 0.520), 14, 0.92, 0.40),
    "phi_b": ("0000CC:\\phi(b)", (0.332, 0.594, 0.397, 0.650), 14, 0.87, 0.42),
}

manifest = {}
for name, (row, (x0n, y0n, x1n, y1n), base_pt, maxw, maxh) in EQS.items():
    rx, ry, rw, rh = region(x0n, y0n, x1n, y1n)
    canvas, pt = rm.fit_row(row, base_pt, maxw, maxh)
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    w_in, h_in = canvas.shape[1] / rm.DPI, canvas.shape[0] / rm.DPI
    manifest[name] = {
        "file": name + ".png",
        "x": round(rx + (rw - w_in) / 2, 4),
        "y": round(ry + (rh - h_in) / 2, 4),
        "w_in": round(w_in, 5), "h_in": round(h_in, 5), "pt": round(pt, 2),
    }
    print(name, "w_in=%.3f h_in=%.3f pt=%.1f x=%.3f y=%.3f" % (w_in, h_in, pt, manifest[name]["x"], manifest[name]["y"]))

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
