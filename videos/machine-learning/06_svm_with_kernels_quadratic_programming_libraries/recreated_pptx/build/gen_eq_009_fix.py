#!/usr/bin/env python3
"""Fix pass for slide 009: boxed quadratic form gains the leading 1/2 factor;
G and h are re-rendered as full \\left[ \\right] matrices sized to fill the
spec regions. New files only (boxed_fix/G_full/h_full); old PNGs untouched.

Usage: python3 gen_eq_009_fix.py
"""
import json, os, sys

import numpy as np
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from render_math import fit_row, DPI

OUT = os.path.join(BUILD, "eq_009")
RED = "#CC0000"
BLACK = "#000000"


def emit(name, row, size, max_w, max_h):
    canvas, pt = fit_row(row, size, max_w, max_h)
    out = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(out)
    info = {"path": out, "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
            "w_in": round(canvas.shape[1] / DPI, 5), "h_in": round(canvas.shape[0] / DPI, 5),
            "dpi": DPI, "fontsize_pt": [pt], "rows": [row]}
    with open(out + ".json", "w") as fh:
        json.dump(info, fh, indent=2)
    print(name, info["w_in"], "x", info["h_in"], "pt", round(pt, 2))


# Yellow QP box: original shows the 1/2 coefficient before the bracket.
emit("boxed_fix", "#FF0000:\\frac{1}{2}\\left[x^{T}Px\\right]+q^{T}x", 24, 3.0, 0.40)

# Full 5x2 / 5x1 bracket matrices (nested \overset stacks) filling the spec
# regions beside the vertical divider.
G_ROW = (BLACK + r":G=\left[\overset{-1\;\;0}{\overset{0\;-1}"
         r"{\overset{-1\;-3}{\overset{2\;\;5}{3\;\;4}}}}\right]")
H_ROW = (BLACK + r":h=\left[\overset{0}{\overset{0}"
         r"{\overset{-15}{\overset{100}{80}}}}\right]")
emit("G_full", G_ROW, 30, 1.30, 1.50)
emit("h_full", H_ROW, 30, 0.70, 1.50)
