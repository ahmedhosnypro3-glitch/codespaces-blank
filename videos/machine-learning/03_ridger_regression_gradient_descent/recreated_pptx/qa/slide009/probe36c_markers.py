#!/usr/bin/env python3
"""Probe 36c: ASCII art of (a) a per-point 9x9 red marker, (b) the LEFT big
arrow as one unit (comp12+comp14), (c) the RIGHT arrow unit (comp13+15+19),
(d) LEFT comp7 (x129..130 y146..151) and comp11 (x183..190 y150..160) and
their RIGHT counterparts, to determine marker/arrow geometry precisely.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
RED = (r > 90) & ((r - g) > 40) & ((r - b) > 10)

def art(label, x0, x1, y0, y1, mask):
    print(f"=== {label}  x{x0}..{x1} y{y0}..{y1} ===")
    hdr = "      "
    for xx in range(x0, x1+1):
        hdr += str((xx // 10) % 10) if xx % 10 == 0 else " "
    print(hdr)
    for yy in range(y0, y1+1):
        print(f"{yy:4d}  " + "".join("#" if mask[yy, xx] else "." for xx in range(x0, x1+1)))

R = RED.copy()
R[:, 124:129] = False
R[:, 538:543] = False
R[432:437, :] = False
R[480:, :] = False

art("L per-point marker (orange pt 175.5,380)", 170, 182, 374, 387, R)
art("L per-point marker (orange pt 421,254.5)", 415, 429, 248, 261, R)
art("L comp7 near y-axis", 126, 134, 143, 155, R)
art("L big arrow unit", 196, 248, 195, 258, R)
art("R big arrow unit", 620, 654, 207, 268, R)
