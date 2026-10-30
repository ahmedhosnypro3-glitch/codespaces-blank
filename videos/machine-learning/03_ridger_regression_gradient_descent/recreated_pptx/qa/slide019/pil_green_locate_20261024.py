#!/usr/bin/env python3
"""Locate the green-ish dark ink in the original, region by region."""
import numpy as np
from PIL import Image

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"
A = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
lum = A.mean(axis=2)
m = lum < 120
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
GREEN = m & (g - r > 20) & (g - b > 10) & (g > 40)
print("green-ish dark ink px:", GREEN.sum())

ys, xs = np.where(GREEN)
if len(ys):
    print("rows:", sorted(set(ys.tolist()))[:60])
    print("row range", ys.min(), ys.max())
    # group rows
    rows = sorted(set(ys.tolist()))
    grp = []
    for y in rows:
        if grp and y - grp[-1][1] <= 3:
            grp[-1][1] = y
        else:
            grp.append([y, y])
    for a, bb in grp:
        sub = GREEN[a:bb + 1]
        xs2 = np.where(sub.any(axis=0))[0]
        print(f"  y{a}..{bb} n={sub.sum()} x{xs2.min()}..{xs2.max()} rgb="
              f"{tuple(A[a:bb+1][sub].mean(axis=0).round(1))}")

# per column
for nm, x0, x1 in [("outlier",60,130),("NOREG",124,380),("R3",384,640),("R10",644,900)]:
    print(f"  {nm}: greenish={GREEN[:, x0:x1].sum()}")
