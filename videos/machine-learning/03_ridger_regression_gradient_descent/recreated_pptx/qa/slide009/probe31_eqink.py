#!/usr/bin/env python3
"""Probe 31: precise equation-ink bboxes inside the two pale-blue annotation
boxes. Tight predicate: within the box interior, ink is the equation glyphs
(dark) and nothing else. Reports full bbox, per-row run structure, and the
column-profile so the PNG target size is exact.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)

def box(name, x0, x1, y0, y1):
    w = a[y0:y1+1, x0:x1+1]
    r, g, b = w[:, :, 0], w[:, :, 1], w[:, :, 2]
    dark = (r + g + b) <= 430
    ys, xs = np.nonzero(dark)
    if len(xs) == 0:
        print(f"--- {name}: no dark ink")
        return
    X0, X1, Y0, Y1 = x0+xs.min(), x0+xs.max(), y0+ys.min(), y0+ys.max()
    print(f"--- {name}: box x{x0}..{x1} y{y0}..{y1}")
    print(f"    ink x{X0}..{X1} (w={X1-X0+1})  y{Y0}..{Y1} (h={Y1-Y0+1})  n={len(xs)}")
    # per-row extent
    for yy in range(Y0, Y1+1):
        cols = np.nonzero(dark[yy-y0, :])[0]
        if len(cols):
            print(f"      row {yy}: x{x0+cols.min()}..{x0+cols.max()} n={len(cols)}")
    # column runs (contiguous groups) across full ink height band
    colany = dark[Y0-y0:Y1-y0+1, :].any(axis=0)
    runs = []
    i = 0
    while i < len(colany):
        if colany[i]:
            j = i
            while j+1 < len(colany) and colany[j+1]:
                j += 1
            runs.append((x0+i, x0+j))
            i = j+1
        else:
            i += 1
    print(f"    column runs ({len(runs)}): {runs}")

box("LEFT equation box", 218, 315, 148, 173)
box("RIGHT equation box", 633, 732, 149, 173)
