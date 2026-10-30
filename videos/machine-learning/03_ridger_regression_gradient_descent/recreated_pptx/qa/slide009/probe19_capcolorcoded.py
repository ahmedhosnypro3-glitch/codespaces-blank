#!/usr/bin/env python3
"""Probe 19: color-coded ASCII of the four caption lines.
'R' = red ink, '#' = dark/black ink. Prints every 2nd column when wide.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

band = (r + g + b) <= 690
SAT = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
redish = band & (r - g > 20) & (r - b > 20) & (r > 60)
dark = band & (SAT <= 22)


def dump(nm, x0, x1, y0, y1):
    m = (redish | dark)[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    print(f"\n===== {nm} x{x0}..{x1} y{y0}..{y1} =====")
    if not len(ys):
        print("  no ink")
        return
    print(f"  ink bbox x {x0+xs.min()}..{x0+xs.max()}  y {y0+ys.min()}..{y0+ys.max()}")
    X0, X1 = x0 + xs.min(), x0 + xs.max()
    step = 2 if (X1 - X0) > 300 else 1
    print("      " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(X0, X1 + 1, step)))
    for y in range(y0 + ys.min(), y0 + ys.max() + 1):
        out = []
        for x in range(X0, X1 + 1, step):
            if redish[y, x]:
                out.append("R")
            elif dark[y, x]:
                out.append("#")
            else:
                out.append(" ")
        print(f"  {y:4d} " + "".join(out))
    # mean color of each class
    for label, mm in (("RED", redish[y0:y1 + 1, x0:x1 + 1]), ("DARK", dark[y0:y1 + 1, x0:x1 + 1])):
        if mm.sum():
            px = a[y0:y1 + 1, x0:x1 + 1][mm]
            s = px.sum(axis=1)
            core = px[s < np.percentile(s, 25)]
            print(f"  {label} core-25% mean RGB ({core[:,0].mean():.0f},{core[:,1].mean():.0f},{core[:,2].mean():.0f})")


dump("LCAP line1", 100, 468, 487, 505)
dump("LCAP line2", 100, 468, 506, 524)
dump("RCAP line1", 495, 838, 487, 505)
dump("RCAP line2", 495, 838, 506, 524)
