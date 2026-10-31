#!/usr/bin/env python3
"""Generate eq_011 math assets via render_math.py (600 dpi tight transparent PNGs)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from render_math import fit_row, DPI
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_011")
os.makedirs(OUT, exist_ok=True)


def mat(rows):
    return r"\left[\;\substack{" + r"\\".join(rows) + r"}\;\right]"


ASSETS = [
    ("eq_vecs.png", 13, 4.0, 1.5, [
        r"x_1=(1,1),\ y_1=1",
        r"x_2=(2,2),\ y_2=1",
        r"x_3=(7,4),\ y_3=-1",
        r"x_4=(8,4),\ y_4=-1",
    ]),
    ("eq_test.png", 13, 2.4, 1.0, [
        r"\substack{T_1\quad T_2\quad T_3\\ 2\quad 4\quad 6\\ 3\quad 5\quad 2}",
    ]),
    ("eq_cons.png", 12, 5.0, 1.15, [
        r"\alpha_1 y_1+\alpha_2 y_2+\alpha_3 y_3+\alpha_4 y_4=0",
        r"0\leq\alpha_1\leq C",
        r"0\leq\alpha_2\leq C",
        r"0\leq\alpha_3\leq C",
        r"0\leq\alpha_4\leq C,",
    ]),
    ("eq_dual.png", 15, 12.3, 0.62, [
        r"\text{Maximize }\mathcal{L}_p(\alpha)=\sum_{i=1}^{4}\alpha_i-\frac{1}{2}\sum_{i=1}^{4}\sum_{j=1}^{4}\alpha_i\alpha_j y_i y_j x_i^T x_j\ \Rightarrow\ "
        r"\text{Minimize }\mathcal{L}_D(\alpha)=\frac{1}{2}\sum_{i=1}^{4}\sum_{j=1}^{4}\alpha_i\alpha_j y_i y_j x_i^T x_j-\sum_{i=1}^{4}\alpha_i",
    ]),
    ("eq_X.png", 12, 3.0, 1.25, [
        r"\text{X}",
        mat([r"x_1\quad x_2\quad x_3\quad x_4",
             r"1\quad 2\quad 7\quad 8",
             r"1\quad 2\quad 4\quad 4"]),
    ]),
    ("eq_G.png", 11, 3.1, 1.35, [
        r"\text{G}=X^T X",
        mat([r"\quad x_1\quad x_2\quad x_3\quad x_4",
             r"x_1\quad 2\quad 4\quad 11\quad 12",
             r"x_2\quad 4\quad 8\quad 22\quad 24",
             r"x_3\quad 11\quad 22\quad 65\quad 72",
             r"x_4\quad 12\quad 24\quad 72\quad 80"]),
    ]),
    ("eq_Y.png", 11, 3.0, 1.35, [
        r"\text{Y}=(y_i y_j)",
        mat([r"\quad y_1\quad y_2\quad y_3\quad y_4",
             r"y_1\quad 1\quad 1\quad -1\quad -1",
             r"y_2\quad 1\quad 1\quad -1\quad -1",
             r"y_3\quad -1\quad -1\quad 1\quad 1",
             r"y_4\quad -1\quad -1\quad 1\quad 1"]),
    ]),
    ("eq_YG.png", 11, 3.1, 1.35, [
        r"\text{Y}\circ\text{G}",
        mat([r"\quad y_1\quad y_2\quad y_3\quad y_4",
             r"y_1\quad 2\quad 4\quad -11\quad -12",
             r"y_2\quad 4\quad 8\quad -22\quad -24",
             r"y_3\quad -11\quad -22\quad 65\quad 72",
             r"y_4\quad -12\quad -24\quad 72\quad 80"]),
    ]),
    ("eq_obj.png", 12, 7.4, 1.05, [
        r"[ +\alpha_1^2 +2\alpha_1\alpha_2 -5.5\alpha_1\alpha_3 -6\alpha_1\alpha_4 +2\alpha_2\alpha_1 +4\alpha_2^2 -11\alpha_2\alpha_3 -12\alpha_2\alpha_4",
        r" -5.5\alpha_3\alpha_1 -11\alpha_3\alpha_2 +32.5\alpha_3^2 +36\alpha_3\alpha_4 -6\alpha_4\alpha_1 -12\alpha_4\alpha_2 +36\alpha_4\alpha_3 +40\alpha_4^2 ]",
        r" -[ \alpha_1+\alpha_2+\alpha_3+\alpha_4 ]",
    ]),
    ("eq_bounds.png", 11, 3.6, 1.05, [
        r"0\leq\alpha_1\leq C",
        r"0\leq\alpha_2\leq C",
        r"0\leq\alpha_3\leq C",
        r"0\leq\alpha_4\leq C",
    ]),
    ("eq_subj.png", 11, 7.4, 0.62, [
        r"\sum_i\alpha_i y_i=0 \qquad \alpha_1+\alpha_2-\alpha_3-\alpha_4=0",
        r"\alpha_i\leq C:\ \alpha_1\leq1,\ \alpha_2\leq1,\ \alpha_3\leq1,\ \alpha_4\leq1 \qquad \alpha_i\geq0:\ \alpha_1\geq0,\ \alpha_2\geq0,\ \alpha_3\geq0,\ \alpha_4\geq0",
    ]),
]

manifest = {}
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
    path = os.path.join(OUT, name)
    Image.fromarray(canvas).save(path)
    manifest[name] = {"w_px": int(w), "h_px": int(h), "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5)}
    print(name, manifest[name])

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
