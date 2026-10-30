#!/usr/bin/env python3
"""Probe 38: per-row x-runs of RED ink in the two chart panels, so the big
residual arrow's shaft/head geometry is exact (no ASCII column-counting).
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

def runs_of(vals, gap=2):
    vals = sorted(int(v) for v in vals)
    if not vals:
        return []
    out, s, p = [], vals[0], vals[0]
    for v in vals[1:]:
        if v <= p + gap:
            p = v; continue
        out.append((s, p)); s = p = v
    out.append((s, p))
    return out

for name, x0, x1 in (("LEFT", 95, 464), ("RIGHT", 487, 870)):
    print(f"########## {name} panel: per-row RED runs (gap<=2 merged) ##########")
    for yy in range(111, 471):
        cols = np.nonzero(M[yy, x0:x1+1])[0] + x0
        rr = runs_of(cols)
        if rr:
            print(f"  y{yy:3d}: " + "  ".join(f"x{a}..{b}(n={b-a+1})" for a, b in rr))
