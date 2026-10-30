#!/usr/bin/env python3
"""Geometry + color measurement of slide_012.jpg (NN output-layer slide)."""
import numpy as np
from PIL import Image

P = "videos/machine-learning/10_nn_training_and_example/unique_slides/slide_012.jpg"
o = np.asarray(Image.open(P).convert("RGB")).astype(int)
H, W = 540, 960
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]
IN = 13.33 / W   # px -> inch
print("in/px =", round(IN, 6))


def regions(mask, name, min_px=200, band=5):
    ys, xs = np.where(mask)
    if not len(ys):
        print(f"  {name}: none")
        return
    print(f"  {name}: {len(ys)} px, rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")


print("\n=== color masks ===")
green = (g - r > 25) & (g - b > 25) & (g > 110)
orange = (r > 200) & (g > 120) & (g < 215) & (b < 110) & (r - b > 90)
lightblue = (b - r > 25) & (g > 120) & (g - r > 5) & (b > 180)
strongred = (r > 150) & (r - g > 60) & (r - b > 60)
yellow = (r > 225) & (g > 210) & (b < 165)
pale_green_strip = (r > 185) & (r < 235) & (g > 220) & (b > 185) & (g - r > 8)
for m, n in [(green, "green circles"), (orange, "orange circles"),
             (lightblue, "light-blue rects"), (strongred, "strong red"),
             (yellow, "yellow badge"), (pale_green_strip, "pale-green strip")]:
    regions(m, n)

print("\n=== connected components on each fill color ===")
from scipy import ndimage
for m, n in [(green & ~pale_green_strip, "green"), (orange, "orange"),
             (lightblue, "lightblue"), (yellow, "yellow")]:
    lbl, k = ndimage.label(m)
    print(f" {n}: {k} components")
    for i in range(1, k + 1):
        ys, xs = np.where(lbl == i)
        if len(ys) >= 150:
            print(f"   c{i}: n={len(ys)} rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()} "
                  f"wh=({xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}) "
                  f"in=({ (xs.max()-xs.min()+1)*IN:.2f}x{(ys.max()-ys.min()+1)*IN:.2f}) "
                  f"ctr_in=({ (xs.min()+xs.max())/2*IN:.2f},{(ys.min()+ys.max())/2*IN:.2f})")

print("\n=== dark ink (text/lines) ===")
dark = (r < 110) & (g < 110) & (b < 110)
rowsum = dark.sum(axis=1)
for y in range(H):
    if rowsum[y] > 40:
        xs = np.where(dark[y])[0]
        pass
print(" dark rows with >40 px:", [int(y) for y in np.where(rowsum > 40)[0][:60]])
colsum = dark.sum(axis=0)
print(" dark cols with >30 px:", [int(x) for x in np.where(colsum > 30)[0][:60]])

print("\n=== horizontal rule candidates (long dark rows) ===")
for y in range(H):
    xs = np.where(dark[y, 60:930])[0]
    if len(xs) > 120:
        print(f"  row {y}: cols {xs.min()+60}-{xs.max()+60} ({len(xs)} px)")

print("\n=== vertical rule candidates (long dark cols) ===")
for x in range(W):
    ys = np.where(dark[60:500, x])[0]
    if len(ys) > 90:
        print(f"  col {x}: rows {ys.min()+60}-{ys.max()+60} ({len(ys)} px)")

print("\n=== title ink (red text top-left, rows 40-110) ===")
sub = (r > 120) & (r - g > 60) & (r - b > 60)
ys, xs = np.where(sub[30:115])
if len(ys):
    print(f"  red title ink: rows {ys.min()+30}-{ys.max()+30} cols {xs.min()}-{xs.max()}")

print("\n=== row profile: fraction non-background per row ===")
bg = (np.abs(r - 242) < 12) & (np.abs(g - 242) < 12) & (np.abs(b - 242) < 12)
for y0 in range(0, H, 20):
    nb = (~bg[y0:y0 + 20]).sum()
    print(f"  rows {y0:>3}-{y0+19:>3}: non-bg {nb/ (20*W):.2f}")
