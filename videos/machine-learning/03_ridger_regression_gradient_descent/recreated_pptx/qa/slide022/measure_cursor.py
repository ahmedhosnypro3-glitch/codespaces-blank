#!/usr/bin/env python3
"""Locate the mouse-cursor artifact precisely (video artifact, OMITTED from the
build; ground rules (c)) — and confirm nothing else lives between the title lines."""
import numpy as np
from PIL import Image

IM = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_022.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
BG = np.array([233, 233, 231])

print("per-row non-red, non-background ink for rows y300..326 (cursor hunt):")
for y in range(300, 327):
    row = im[y, 100:900]
    # sensitive: differs from panel by >15 on any channel AND not red text
    d = np.abs(row - BG).max(axis=1)
    red = (row[:, 0] > 90) & ((row[:, 0] - row[:, 1]) > 40) & ((row[:, 0] - row[:, 2]) > 10)
    m = (d > 15) & ~red
    n = int(m.sum())
    if n:
        xs = np.where(m)[0]
        # contiguous runs
        runs = np.split(xs, np.where(np.diff(xs) > 4)[0] + 1) if len(xs) else []
        rs = ", ".join(f"x {100+r.min()}..{100+r.max()}" for r in runs)
        print(f"  y={y}: n={n:3d}  {rs}")

# strongest cursor rows: print min/max channel values in the y305..325 band
print("\ncursor band sample colors (y305..325):")
band = im[305:326, 400:600]
d = np.abs(band - BG).max(axis=2)
mask = d > 15
ys, xs = np.where(mask)
if len(ys):
    pxs = band[mask]
    print(f"  n={mask.sum()}, x-extent {400+xs.min()}..{400+xs.max()}, y-extent {305+ys.min()}..{305+ys.max()}")
    print(f"  darkest px = {pxs[pxs.sum(axis=1).argmin()]}, brightest px = {pxs[pxs.sum(axis=1).argmax()]}")
    print(f"  mean = {pxs.mean(axis=0).round(1)}")

# also confirm the whole frame has no other ink between y95..230 and y366..530
for (ya, yb, lbl) in ((95, 230, "between badge and L1"), (366, 530, "below L2")):
    reg = im[ya:yb, 66:894]
    d = np.abs(reg - BG).max(axis=2)
    m = d > 18
    print(f"\n{lbl} (y{ya}..{yb}): sensitive ink px = {m.sum()}")
    if m.sum():
        ys, xs = np.where(m)
        print(f"  extent x {66+xs.min()}..{66+xs.max()} y {ya+ys.min()}..{ya+ys.max()}")
