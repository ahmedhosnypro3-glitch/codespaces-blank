#!/usr/bin/env python3
"""Densest-content region picker for deck-03 rejudge crop pairs.

Frame px (960x540, 1px=1pt). Scans 288x192 windows (stride = cell 24px) over an
ink-range (local max-min) integral image and picks the window with the most
local contrast, excluding house-chrome zones (panel edges, badge). Prints
"x0 y0 x1 y1" with 8px padding, clamped inside the panel.
"""
import sys

import numpy as np
from PIL import Image

N = sys.argv[1]
NS = "videos/machine-learning/03_ridger_regression_gradient_descent"
o = Image.open(f"{NS}/unique_slides/slide_{N}.jpg").convert("L")
a = np.asarray(o).astype(np.int32)
H, W = a.shape

CELL = 24
WW, WH = 288, 192
wc, hc = WW // CELL, WH // CELL
Hc, Wc = H // CELL, W // CELL

rng = np.zeros((Hc, Wc), dtype=np.int64)
for i in range(Hc):
    for j in range(Wc):
        b = a[i * CELL:(i + 1) * CELL, j * CELL:(j + 1) * CELL]
        rng[i, j] = int(b.max()) - int(b.min())
S = rng.cumsum(0).cumsum(1)

def boxsum(i0, j0):
    i1, j1 = i0 + hc - 1, j0 + wc - 1
    s = S[i1, j1]
    if i0 > 0:
        s -= S[i0 - 1, j1]
    if j0 > 0:
        s -= S[i1, j0 - 1]
    if i0 > 0 and j0 > 0:
        s += S[i0 - 1, j0 - 1]
    return int(s)

best = (-1, (60, 47, 348, 239))
for i in range(Hc - hc + 1):
    for j in range(Wc - wc + 1):
        x0, y0 = j * CELL, i * CELL
        x1, y1 = x0 + WW, y0 + WH
        if x1 > 902 or y0 < 46:      # outside panel / above panel top
            continue
        if x0 < 860 and y0 < 95:     # badge zone top-right handled separately
            continue
        if x0 >= 860 and y0 < 95:    # over the badge itself
            continue
        s = boxsum(i, j)
        if s > best[0]:
            best = (s, (x0, y0, x1, y1))

x0, y0, x1, y1 = best[1]
x0 = max(60, x0 - 8)
y0 = max(47, y0 - 8)
x1 = min(901, x1 + 8)
y1 = min(539, y1 + 8)
print(x0, y0, x1, y1)
