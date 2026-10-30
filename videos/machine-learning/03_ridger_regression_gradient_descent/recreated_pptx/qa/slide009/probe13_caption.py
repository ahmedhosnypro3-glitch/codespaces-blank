#!/usr/bin/env python3
"""Probe 13: raw color census of the caption band (y 478..532) on both halves,
so the caption text color and its true ink bbox are settled from pixels.

Prints, per row, the distinct colors with counts (top 6), plus a fine ASCII of
the LEFT caption using a permissive "anything != local background" predicate.
"""
import numpy as np
from PIL import Image
from collections import Counter

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)


def census(name, x0, x1, y0, y1):
    print(f"\n===== {name} x{x0}..{x1} y{y0}..{y1} =====")
    for y in range(y0, y1 + 1):
        cc = Counter(map(tuple, a[y, x0:x1 + 1]))
        top = cc.most_common(4)
        s = " | ".join(f"{c}x{n}" for c, n in top)
        print(f"  y={y:3d} n={len(cc):4d} {s}")


census("LEFT caption band", 100, 470, 484, 504)
census("RIGHT caption band", 480, 875, 484, 504)

# Now: what is the darkest ink per row in the caption band, and its bbox?
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
print("\n===== caption ink via 'sum < 500' (any dark) =====")
for nm, x0, x1 in (("LEFT", 100, 472), ("RIGHT", 480, 875)):
    m = (r + g + b < 500)[484:505, x0:x1 + 1]
    ys, xs = np.where(m)
    if not len(ys):
        print(f"  {nm}: none")
        continue
    print(f"  {nm}: x {x0+xs.min()}..{x0+xs.max()}  y {484+ys.min()}..{484+ys.max()}")
    # per-row spans
    for i in range(m.shape[0]):
        if m[i].sum() == 0:
            continue
        xs2 = np.where(m[i])[0]
        print(f"    y={484+i}: x {x0+xs2.min()}..{x0+xs2.max()} n={m[i].sum()}")
