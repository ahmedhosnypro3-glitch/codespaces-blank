#!/usr/bin/env python3
"""Probe 39: per-COLUMN y-runs of RED ink for the per-point markers and the two
big arrows, to determine exact glyph geometry (diamond vs arrowhead vs shaft).
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
RED = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
M = RED.copy()
M[:, 124:129] = False
M[:, 538:543] = False
M[432:437, :] = False
M[480:, :] = False

def yruns(name, x0, x1, y0, y1):
    print(f"--- {name}: per-column RED y-runs, x{x0}..{x1} y{y0}..{y1}")
    for xx in range(x0, x1+1):
        rows = np.nonzero(M[y0:y1+1, xx])[0] + y0
        rows = sorted(int(v) for v in rows)
        # merge gap<=1
        out = []
        if rows:
            s = p = rows[0]
            for v in rows[1:]:
                if v <= p+1:
                    p = v; continue
                out.append((s, p)); s = p = v
            out.append((s, p))
        if out:
            print(f"    x{xx}: " + "  ".join(f"y{a}..{b}" for a, b in out))

yruns("L marker A (pt 175.5,380)", 170, 182, 374, 387)
yruns("L arrowhead top (of big arrow)", 206, 222, 218, 240)
yruns("R arrowhead top", 620, 646, 205, 240)
