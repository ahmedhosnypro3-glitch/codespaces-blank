#!/usr/bin/env python3
"""Probe 34: loose-threshold ASCII art of both full equation boxes, so the faint
superscript glyph (if any) is visible alongside the main ink.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)

def art(name, x0, x1, y0, y1, thr=690):
    w = a[y0:y1+1, x0:x1+1]
    t = w.sum(axis=2)
    print(f"=== {name}  x{x0}..{x1} y{y0}..{y1} thr<={thr} ===")
    hdr = "     "
    for xx in range(x0, x1+1):
        hdr += str((xx // 10) % 10) if xx % 10 == 0 else " "
    print(hdr)
    for i, yy in enumerate(range(y0, y1+1)):
        print(f"{yy:4d} " + "".join("#" if v <= thr else "." for v in t[i]))

art("LEFT eq (loose)", 220, 312, 150, 169)
art("RIGHT eq (loose)", 639, 726, 151, 169)
