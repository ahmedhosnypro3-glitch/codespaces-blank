#!/usr/bin/env python3
"""Fix-iteration-1 regen of eq_011 assets: explicit +1a1^2 objective lead,
two-line subject-to equality, larger middle-band matrices. 600 dpi PNGs."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from render_math import fit_row, DPI
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_011")
RED = "#C00000"


def mat(rows):
    return r"\left[\;\substack{" + r"\\".join(rows) + r"}\;\right]"


ASSETS = [
    ("eq_obj.png", 13, 7.4, 1.10, [
        r"[ +1\alpha_1^2 +2\alpha_1\alpha_2 -5.5\alpha_1\alpha_3 -6\alpha_1\alpha_4 +2\alpha_2\alpha_1 +4\alpha_2^2 -11\alpha_2\alpha_3 -12\alpha_2\alpha_4",
        r" -5.5\alpha_3\alpha_1 -11\alpha_3\alpha_2 +32.5\alpha_3^2 +36\alpha_3\alpha_4 -6\alpha_4\alpha_1 -12\alpha_4\alpha_2 +36\alpha_4\alpha_3 +40\alpha_4^2 ]",
        r" -[ \alpha_1+\alpha_2+\alpha_3+\alpha_4 ]",
    ]),
    ("eq_subj.png", 12, 7.4, 0.62, [
        r"\sum_i \alpha_i y_i = 0",
        r"\alpha_1+\alpha_2-\alpha_3-\alpha_4 = 0",
    ]),
    ("eq_X.png", 14, 3.2, 1.35, [
        r"\text{X}",
        mat([r"x_1\quad x_2\quad x_3\quad x_4",
             r"1\quad 2\quad 7\quad 8",
             r"1\quad 2\quad 4\quad 4"]),
    ]),
    ("eq_G.png", 13, 3.3, 1.42, [
        r"\text{G}=X^T X",
        mat([r"\quad x_1\quad x_2\quad x_3\quad x_4",
             r"x_1\quad 2\quad 4\quad 11\quad 12",
             r"x_2\quad 4\quad 8\quad 22\quad 24",
             r"x_3\quad 11\quad 22\quad 65\quad 72",
             r"x_4\quad 12\quad 24\quad 72\quad 80"]),
    ]),
    ("eq_Y.png", 13, 3.2, 1.42, [
        r"\text{Y}=(y_i y_j)",
        mat([r"\quad y_1\quad y_2\quad y_3\quad y_4",
             r"y_1\quad 1\quad 1\quad -1\quad -1",
             r"y_2\quad 1\quad 1\quad -1\quad -1",
             r"y_3\quad -1\quad -1\quad 1\quad 1",
             r"y_4\quad -1\quad -1\quad 1\quad 1"]),
    ]),
    ("eq_YG.png", 13, 3.2, 1.42, [
        r"\text{Y}\circ\text{G}",
        mat([r"\quad y_1\quad y_2\quad y_3\quad y_4",
             r"y_1\quad 2\quad 4\quad -11\quad -12",
             r"y_2\quad 4\quad 8\quad -22\quad -24",
             r"y_3\quad -11\quad -22\quad 65\quad 72",
             r"y_4\quad -12\quad -24\quad 72\quad 80"]),
    ]),
    ("eq_dual.png", 15, 12.3, 0.62, [
        r"\text{Maximize }\mathcal{L}_D(\alpha)=\sum_{i=1}^{4}\alpha_i-\frac{1}{2}\sum_{i=1}^{4}\sum_{j=1}^{4}\alpha_i\alpha_j y_i y_j X_i^T X_j\ \Rightarrow\ "
        r"\text{Minimize }\mathcal{L}_D(\alpha)=\frac{1}{2}\sum_{i=1}^{4}\sum_{j=1}^{4}\alpha_i\alpha_j y_i y_j X_i^T X_j-\sum_{i=1}^{4}\alpha_i",
    ]),
]

manifest = json.load(open(os.path.join(OUT, "manifest.json")))
for name, size, maxw, maxh, rows in ASSETS:
    canvases = []
    for r in rows:
        c, pt = fit_row(r, size, maxw, maxh / len(rows))
        canvases.append(c)
    w = max(c.shape[1] for c in canvases)
    gap = 8
    h = sum(c.shape[0] for c in canvases) + gap * (len(canvases) - 1)
    canvas = np.zeros((h, w, 4), dtype="uint8")
    y = 0
    for c in canvases:
        canvas[y:y + c.shape[0], 0:c.shape[1]] = c
        y += c.shape[0] + gap
    Image.fromarray(canvas).save(os.path.join(OUT, name))
    manifest[name] = {"w_px": int(w), "h_px": int(h),
                      "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5)}
    print(name, manifest[name])

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
