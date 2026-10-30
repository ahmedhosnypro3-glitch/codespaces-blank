#!/usr/bin/env python3
r"""Banked box finder for slide 015 (deck 03): locates every rectangle box
(long horizontal border rows + long vertical border columns) in a row range of
unique_slides/slide_015.jpg and reports border/fill colours.

Usage: python3 boxes_015.py [y0 y1]
"""
import sys
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_015.jpg"
rgb = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
lum = rgb.mean(axis=2)
ink = lum < 200

y0 = int(sys.argv[1]) if len(sys.argv) > 1 else 260
y1 = int(sys.argv[2]) if len(sys.argv) > 2 else 530
sub = ink[y0:y1 + 1]

# vertical borders: columns whose ink rows span most of the range
colcount = sub.sum(axis=0)
rowcount = sub.sum(axis=1)
print(f"scan rows {y0}..{y1}")
print("  columns with >60% ink rows:", [int(c) for c in np.where(colcount > 0.6 * sub.shape[0])[0]])
print("  rows    with >25% ink cols:", [y0 + int(r) for r in np.where(rowcount > 0.25 * sub.shape[1])[0]])

# for each detected horizontal pair, find the vertical extent
hrows = [y0 + int(r) for r in np.where(rowcount > 0.25 * sub.shape[1])[0]]
for i in range(0, len(hrows), 2):
    pass

# explicit probe of a candidate rect
def rect(x0, y0_, x1, y1_, tag):
    top = rgb[y0_:y0_ + 2, x0 + 4:x1 - 3]
    bot = rgb[y1_ - 1:y1_ + 1, x0 + 4:x1 - 3]
    left = rgb[y0_ + 4:y1_ - 3, x0:x0 + 2]
    right = rgb[y0_ + 4:y1_ - 3, x1 - 1:x1 + 1]
    ins = rgb[y0_ + 14:y1_ - 13, x0 + 14:x1 - 13]
    for name, a in (("top", top), ("bottom", bot), ("left", left), ("right", right), ("inner", ins)):
        f = a.reshape(-1, 3)
        print(f"  {tag} {name:6s} median={tuple(int(v) for v in np.median(f, axis=0))} "
              f"#%02X%02X%02X" % tuple(int(v) for v in np.median(f, axis=0)))


for spec in sys.argv[3:]:
    parts = spec.split(":")
    x0, yy0, x1, yy1 = (int(v) for v in parts[0].split(","))
    tag = parts[1] if len(parts) > 1 else "box"
    rect(x0, yy0, x1, yy1, tag)
