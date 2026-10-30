#!/usr/bin/env python3
"""Probe 32: ASCII-art rendering of the two equation crops so glyph structure
(stacked fraction vs single line) is unambiguous.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)

def art(name, x0, x1, y0, y1):
    w = a[y0:y1+1, x0:x1+1]
    r, g, b = w[:, :, 0], w[:, :, 1], w[:, :, 2]
    dark = (r + g + b) <= 430
    print(f"=== {name}  x{x0}..{x1} y{y0}..{y1} ===")
    hdr = "     "
    for xx in range(x0, x1+1):
        hdr += str((xx // 10) % 10) if xx % 10 == 0 else " "
    print(hdr)
    for i, yy in enumerate(range(y0, y1+1)):
        line = "".join("#" if dark[i, j] else "." for j in range(x1-x0+1))
        print(f"{yy:4d} {line}")

art("LEFT equation", 222, 311, 152, 170)
art("RIGHT equation", 640, 727, 152, 170)
