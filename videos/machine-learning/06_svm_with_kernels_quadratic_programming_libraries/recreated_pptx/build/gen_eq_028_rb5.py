#!/usr/bin/env python3
"""Render slide_028 (rb5) equation assets via render_math.py into eq_028/.

rb5 fix (judge MAJOR: glyphs ~half size; MINOR: panels too narrow vs frame):
map the original capture's red frame [0.054,0.065,0.852,0.856] onto the house
frame [0.011,0.02,0.989,0.98] (normalized), i.e. scale content by ~1.2256 x and
~1.2136 y about the frame, so panels/glyphs match the original relative to the
house red frame. Columns still use nested \\underset (true 6-line stacks).
Writes rb5_<name>.png + manifest_rb5.json; boxes stored in SPEC coords.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from render_math import fit_row, DPI

EQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_028")
W, H = 13.33, 7.5

FX0, FY0, FX1, FY1 = 0.054, 0.065, 0.852, 0.856   # original capture frame
HX0, HY0, HX1, HY1 = 0.011, 0.020, 0.989, 0.980   # house frame, normalized
SX = (HX1 - HX0) / (FX1 - FX0)
SY = (HY1 - HY0) / (FY1 - FY0)


def tbox(box):
    x0, y0, x1, y1 = box
    nx0 = HX0 + (x0 - FX0) * SX
    nx1 = HX0 + (x1 - FX0) * SX
    ny0 = HY0 + (y0 - FY0) * SY
    ny1 = HY0 + (y1 - FY0) * SY
    return (nx0, ny0, nx1, ny1)


def col(rows):
    out = rows[0]
    for r in rows[1:]:
        out = "\\underset{%s}{%s}" % (r, out)
    return out


A = "\\alpha_{1}^{2},\\ \\alpha_{2}^{2},\\ \\sqrt{2}\\alpha_{1}\\alpha_{2},\\ \\sqrt{2}\\alpha_{1},\\ \\sqrt{2}\\alpha_{2},\\ 1"
B6 = col(["\\beta_{1}^{2}", "\\beta_{2}^{2}", "\\sqrt{2}\\beta_{1}\\beta_{2}",
          "\\sqrt{2}\\beta_{1}", "\\sqrt{2}\\beta_{2}", "1"])
P6 = col(["x_{1}^{2}", "x_{2}^{2}", "\\sqrt{2}x_{1}x_{2}",
          "\\sqrt{2}x_{1}", "\\sqrt{2}x_{2}", "1"])
N6 = col(["3^{2}", "4^{2}", "\\sqrt{2}\\,3{\\cdot}4", "3\\sqrt{2}", "4\\sqrt{2}", "1"])
M6 = col(["9", "16", "12\\sqrt{2}", "3\\sqrt{2}", "4\\sqrt{2}", "1"])
X2 = col(["x_{1}", "x_{2}"])

ASSETS = {
    "chip":   ([0.073, 0.256, 0.133, 0.300], "#FF0033:a^{T}b+1"),
    "sq":     ([0.139, 0.254, 0.154, 0.281], "#000000:^{2}="),
    "arow":   ([0.154, 0.178, 0.367, 0.207], "#FF0033:\\left(" + A + "\\right)"),
    "bcol":   ([0.371, 0.167, 0.429, 0.398], "#0000FF:\\left(" + B6 + "\\right)^{T}"),
    "eq":     ([0.443, 0.265, 0.518, 0.296], "#000000:=\\phi(a)^{T}\\phi(b)"),
    "where":  ([0.550, 0.250, 0.651, 0.302], "#000000:\\mathrm{Where:}\\ \\phi(x)=\\left(" + X2 + "\\right)^{T}"),
    "arrow":  ([0.690, 0.267, 0.704, 0.291], "#FF0033:\\Rightarrow"),
    "phicol": ([0.717, 0.167, 0.773, 0.398], "#000000:\\left(" + P6 + "\\right)"),
    "a":      ([0.073, 0.444, 0.125, 0.528], "#FF0033:\\mathbf{a}=\\left(" + col(["1", "2"]) + "\\right)^{T}"),
    "b":      ([0.146, 0.444, 0.200, 0.528], "#0000FF:\\mathbf{b}=\\left(" + col(["3", "4"]) + "\\right)^{T}"),
    "leq":    ([0.073, 0.615, 0.169, 0.652], "#000000:\\phi(a)^{T}\\phi(b)="),
    "row":    ([0.175, 0.541, 0.388, 0.574], "#FF0033:\\left(1^{2},\\ 2^{2},\\ \\sqrt{2}\\,1{\\cdot}2,\\ \\sqrt{2},\\ 2\\sqrt{2},\\ 1\\right)"),
    "bcol2":  ([0.394, 0.537, 0.460, 0.737], "#0000FF:\\left(" + N6 + "\\right)^{T}"),
    "prod":   ([0.479, 0.587, 0.627, 0.617], "#000000:= ||#FF0033:\\left(1,\\ 4,\\ 2\\sqrt{2},\\ \\sqrt{2},\\ 2\\sqrt{2},\\ 1\\right)"),
    "numcol": ([0.654, 0.533, 0.710, 0.741], "#0000FF:\\left(" + M6 + "\\right)"),
    "sum":    ([0.461, 0.746, 0.652, 0.778], "#000000:=9+64+48+6+16+1=144"),
    "bot":    ([0.073, 0.787, 0.346, 0.824], "#000000:| ||#FF0033:a^{T} ||#0000FF:b+1 ||#000000:|^{2}=(1+3+2{\\cdot}4+1)^{2}=12^{2}=144"),
}

man = {}
for name, (box, row) in ASSETS.items():
    nx0, ny0, nx1, ny1 = tbox(box)
    maxw, maxh = (nx1 - nx0) * W, (ny1 - ny0) * H
    canvas, pt = fit_row(row, 30.0, maxw, maxh)
    fn = f"rb5_{name}.png"
    Image.fromarray(canvas).save(os.path.join(EQ, fn))
    man[name] = {
        "file": fn,
        "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
        "w_in": round(canvas.shape[1] / DPI, 5), "h_in": round(canvas.shape[0] / DPI, 5),
        "pt": round(pt, 2), "box": box,
    }
    print(name, man[name]["w_in"], man[name]["h_in"], man[name]["pt"])

with open(os.path.join(EQ, "manifest_rb5.json"), "w") as fh:
    json.dump(man, fh, indent=2)
print("manifest_rb5.json written:", len(man), "assets")
