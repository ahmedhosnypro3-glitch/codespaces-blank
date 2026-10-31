#!/usr/bin/env python3
"""Render the 2D math assets for slide_013 (QP formulation) into eq_013/.

Each asset is fitted to its spec box budget (inches) at 600 dpi; the build
script places PNGs at natural size (w = px/600). Manifest: eq_013/manifest.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from render_math import render_row, fit_row, PAD_PX

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "eq_013")
DPI = 600
MIN_SIZE = 7.0

A = r"\alpha"
# name -> (row spec "color:latex||color:latex", base pt, max w in, max h in)
EQS = {
    "obj": (r"#FF0000:\mathbf{+1" + A + r"_{1}^{2}+2" + A + r"_{1}" + A + r"_{2}-5.5" + A + r"_{1}" + A + r"_{3}-6" + A + r"_{1}" + A + r"_{4}+2" + A + r"_{2}" + A + r"_{3}+4" + A + r"_{2}^{2}-11" + A + r"_{2}" + A + r"_{4}-12" + A + r"_{3}" + A + r"_{4}}", 24, 5.844, 0.315),
    "constr": (r"#0000A0:-5.5" + A + r"_{1}" + A + r"_{3}-11" + A + r"_{1}" + A + r"_{4}+32.5" + A + r"_{2}^{2}+36" + A + r"_{3}" + A + r"_{2}-6" + A + r"_{3}" + A + r"_{4}-12" + A + r"_{3}" + A + r"_{2}+36" + A + r"_{3}" + A + r"_{4}+40" + A + r"_{4}^{2}\ ]||#FF0000:-\ [\ " + A + r"_{1}+" + A + r"_{2}+" + A + r"_{3}+" + A + r"_{4}\ ]", 22, 8.512, 0.3225),
    "sumbox": (r"#000000:\sum_{i}" + A + r"_{i}y_{i}=0", 20, 0.56, 0.26),
    "exp1": (r"#FF0000:" + A + r"_{1}+" + A + r"_{2}-" + A + r"_{3}-" + A + r"_{4}=0", 20, 2.896, 0.2325),
    "alphaleC": (r"#FF0000:" + A + r"_{i}\leq C", 20, 0.50, 0.25),
    "listle": (r"#FF0000:" + A + r"_{1}\leq 1,\ " + A + r"_{2}\leq 1,\ " + A + r"_{3}\leq 1,\ " + A + r"_{4}\leq 1", 20, 2.861, 0.225),
    "alphage0": (r"#FF0000:" + A + r"_{i}\geq 0", 20, 0.50, 0.25),
    "listge": (r"#FF0000:" + A + r"_{1}\geq 0,\ " + A + r"_{2}\geq 0,\ " + A + r"_{3}\geq 0,\ " + A + r"_{4}\geq 0", 20, 2.861, 0.225),
    "arrow": (r"#0000A0:\Rightarrow", 26, 0.28, 0.2475),
    "negalpha": (r"#FF0000:-" + A + r"_{1}\leq 0,\ -" + A + r"_{2}\leq 0,\ -" + A + r"_{3}\leq 0,\ -" + A + r"_{4}\leq 0", 20, 3.50, 0.32),
    "gxleh": (r"#FF0000:\mathbf{G}\ x||#000000:\ \leq\ ||#FF0000:\mathbf{h}", 22, 1.00, 0.30),
    "axeb": (r"#FF0000:\mathbf{A}\ x||#000000:\ =\ ||#FF0000:\mathbf{b}", 22, 1.00, 0.30),
    "g_row1": (r"#000000:-1\ 0\ 0\ 0", 16, 1.772, 0.26),
    "g_row2": (r"#000000:0\ -1\ 0\ 0", 16, 1.772, 0.26),
    "g_row3": (r"#000000:0\ 0\ -1\ 0", 16, 1.772, 0.26),
    "g_row4": (r"#000000:0\ 0\ 0\ -1", 16, 1.772, 0.26),
    "g_row5": (r"#000000:1\ 0\ 0\ 0", 16, 1.772, 0.26),
    "g_row6": (r"#000000:0\ 1\ 0\ 0", 16, 1.772, 0.26),
    "g_row7": (r"#000000:0\ 0\ 1\ 0", 16, 1.772, 0.26),
    "g_row8": (r"#000000:0\ 0\ 0\ 1", 16, 1.772, 0.26),
    "alphavec": (r"#FF0000:\left(\underset{" + A + r"_{4}}{\underset{" + A + r"_{3}}{\underset{" + A + r"_{2}}{" + A + r"_{1}}}}\right)", 44, 0.347, 1.2525),
    "h_row1": (r"#000000:0", 16, 0.24, 0.26),
    "h_row2": (r"#000000:0", 16, 0.24, 0.26),
    "h_row3": (r"#000000:0", 16, 0.24, 0.26),
    "h_row4": (r"#000000:0", 16, 0.24, 0.26),
    "h_row5": (r"#000000:1", 16, 0.24, 0.26),
    "h_row6": (r"#000000:1", 16, 0.24, 0.26),
    "h_row7": (r"#000000:1", 16, 0.24, 0.26),
    "h_row8": (r"#000000:1", 16, 0.24, 0.26),
    "arow": (r"#FF0000:A=\left[1\ \ 1\ \ -1\ \ -1\right]_{1\times 4}", 22, 2.519, 0.3975),
    "brow": (r"#FF0000:b=\left[0\right]_{1\times 1}", 22, 0.907, 0.345),
}

# multi-row assets: name -> (list of row specs, base pt, max w, max h, rowgap px)
MULTI = {
    "sol": ([r"#FF0000:" + A + r"_{1}=0.0000002,\ ", r"#FF0000:" + A + r"_{2}=0.06897,\ ",
             r"#FF0000:" + A + r"_{3}=0.06897,\ ", r"#FF0000:" + A + r"_{4}=0.00000008"],
            18, 1.533, 1.02, 14),
}


def fit(name, row, size, max_w, max_h):
    canvas, pt = fit_row(row, size, max_w, max_h, min_size=MIN_SIZE)
    return canvas, pt, canvas.shape[1] / DPI, canvas.shape[0] / DPI


def fit_multi(rows, size, max_w, max_h, rowgap):
    canvases, pts = [], []
    for r in rows:
        c, pt = fit_row(r, size, max_w, max_h, min_size=MIN_SIZE)
        canvases.append(c)
        pts.append(pt)
    w = max(c.shape[1] for c in canvases)
    h = sum(c.shape[0] for c in canvases) + rowgap * (len(canvases) - 1)
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    y = 0
    for c in canvases:
        canvas[y:y + c.shape[0], 0:c.shape[1]] = c
        y += c.shape[0] + rowgap
    return canvas, pts, w / DPI, h / DPI


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    manifest = {}
    for name, spec in EQS.items():
        canvas, pt, w_in, h_in = fit(name, *spec)
        path = os.path.join(OUT_DIR, f"{name}.png")
        Image.fromarray(canvas).save(path)
        manifest[name] = {"path": path, "w_in": round(w_in, 4),
                          "h_in": round(h_in, 4), "fontsize_pt": pt}
        print(f"{name}: {w_in:.2f} x {h_in:.2f} in @ {pt}pt")
    for name, (rows, size, mw, mh, rg) in MULTI.items():
        canvas, pts, w_in, h_in = fit_multi(rows, size, mw, mh, rg)
        path = os.path.join(OUT_DIR, f"{name}.png")
        Image.fromarray(canvas).save(path)
        manifest[name] = {"path": path, "w_in": round(w_in, 4),
                          "h_in": round(h_in, 4), "fontsize_pt": pts}
        print(f"{name}: {w_in:.2f} x {h_in:.2f} in @ {pts}pt")
    with open(os.path.join(OUT_DIR, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    print("wrote eq_013/manifest.json")


if __name__ == "__main__":
    main()
