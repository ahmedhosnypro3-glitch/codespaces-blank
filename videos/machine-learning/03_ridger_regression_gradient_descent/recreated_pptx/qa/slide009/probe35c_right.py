#!/usr/bin/env python3
"""Probe 35c: RIGHT equation segmentation into glyph groups.
RIGHT runs: (643,648)(651,656)(659,659)(662,675)(678,678)(683,688)(694,699)(702,707)(710,715)(717,723)
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
t = a.sum(axis=2)

def band(name, x0, x1, y0, y1, thr=690):
    print(f"=== {name} x{x0}..{x1} y{y0}..{y1} ===")
    hdr = "     "
    for xx in range(x0, x1+1):
        hdr += str((xx // 10) % 10) if xx % 10 == 0 else " "
    print(hdr)
    for yy in range(y0, y1+1):
        print(f"{yy:4d} " + "".join("#" if t[yy, xx] <= thr else "." for xx in range(x0, x1+1)))

# RIGHT: '63.64' -> 643..659ish, '^2' superscript, '=', '4050'
band("RIGHT number-part", 641, 700, 150, 170)
band("RIGHT superscript+eq", 655, 700, 150, 170)
