#!/usr/bin/env python3
"""Probe 15: settle the caption text color + line count from pixels.

For both caption bands (y 478..535): report every row that has ink under a
'darker than the local background' test, the row-grouping into lines, and the
hue statistics of the ink pixels (is the caption RED like the spec claims, or
near-black like the equation text?).
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

for nm, x0, x1 in (("LEFT", 100, 472), ("RIGHT", 480, 878)):
    print(f"\n########## {nm} caption band x{x0}..{x1} ##########")
    # background = the per-row MODE color (JPEG majority). Ink = pixels that
    # differ from the row mode by > 60 in any channel.
    for y in range(478, 536):
        row = a[y, x0:x1 + 1]
        # mode: quantize to 8-step to survive JPEG noise
        q = (row // 8) * 8
        keys, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
        bg = keys[counts.argmax()]
        d = np.abs(row - bg).max(axis=1)
        m = d > 55
        if m.sum() < 2:
            continue
        xs = np.where(m)[0]
        ink = row[m]
        print(f"  y={y:3d} n={m.sum():4d} x {x0+xs.min()}..{x0+xs.max()} "
              f"ink mean RGB ({ink[:,0].mean():.0f},{ink[:,1].mean():.0f},{ink[:,2].mean():.0f}) "
              f"darkest ({ink[:,0].min()},{ink[:,1].min()},{ink[:,2].min()}) bg {tuple(bg)}")
