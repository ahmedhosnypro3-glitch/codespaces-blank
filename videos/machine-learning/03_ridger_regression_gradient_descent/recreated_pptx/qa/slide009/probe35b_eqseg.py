#!/usr/bin/env python3
"""Probe 35b: equation structure by segmentation at the '=' column.
The probe31 column runs already localize the '=' gap. Here we render, for each
row band, the ASCII of the LEFT-of-equals region and the RIGHT-of-equals region
so the superscript is unambiguous.
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

# probe31 runs (LEFT): (226,232)(234,240)(242,243)(246,251)(253,259)(261,261)(264,264)(266,271)(278,283)(286,291)(293,299)(301,307)
# '=' must be one of the later runs; the 1px runs at 261/264 are suspicious.
# LEFT '50.85^2' occupies 226..259 -> '=' at 266..271, then '2585' 278..307.
band("LEFT left-of-1px-runs", 224, 266, 150, 170)
band("LEFT 1px runs region", 258, 274, 150, 170)

# RIGHT runs: (643,648)(651,656)(659,659)(662,675)(678,678)(683,688)(694,699)(702,707)(710,715)(717,723)
band("RIGHT full", 641, 726, 150, 170)
