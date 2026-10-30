#!/usr/bin/env python3
"""Measure slide 017 original geometry at 960x540.

Detects by colour class:
  pink equation-box fill + red outline
  blue graph panel borders
  dark-red title
  black graph axes / text
"""
import json
import sys
import numpy as np
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "unique_slides/slide_017.jpg"

im = Image.open(SRC).convert("RGB")
a = np.array(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def bbox(m, name, minpix=20):
    ys, xs = np.where(m)
    if len(ys) == 0:
        print(f"{name}: none")
        return None
    # keep only rows/cols with >= minpix density to drop JPEG speckle
    rowc = m.sum(axis=1)
    colc = m.sum(axis=0)
    rr = np.where(rowc >= minpix)[0]
    cc = np.where(colc >= minpix)[0]
    print(f"{name}: rows {rr.min()}-{rr.max()} cols {cc.min()}-{cc.max()} "
          f"(raw px {len(ys)})")
    return (int(cc.min()), int(rr.min()), int(cc.max()), int(rr.max()))


print(f"=== {SRC}  {W}x{H} ===")

pink = (R > 235) & (G > 190) & (G < 245) & (B > 195) & (B < 250) & (R - G > 12) & (R - B > 8)
red = (R > 120) & (G < 110) & (B < 110) & (R - G > 60) & (R - B > 60)
blue = (B > 140) & (B - R > 55) & (B - G > 45)
black = (R < 70) & (G < 70) & (B < 70)

bbox(pink, "PINK fill")
bbox(red, "RED ink/outline")
bbox(blue, "BLUE borders")
bbox(black, "BLACK ink")

# --- connected-component-ish region scan for pink boxes (bottom half) ---
print("\n--- pink fill row profile (y>=400) ---")
for y in range(395, H):
    row = pink[y]
    if row.sum() > 3:
        xs = np.where(row)[0]
        # group contiguous
        groups, s = [], xs[0]
        for i in range(1, len(xs)):
            if xs[i] != xs[i - 1] + 1:
                groups.append((s, xs[i - 1]))
                s = xs[i]
        groups.append((s, xs[-1]))
        big = [g for g in groups if g[1] - g[0] > 20]
        if big:
            print(f"  y={y}: {big}")

print("\n--- red ink column/row map in bottom half ---")
redb = red.copy()
redb[:380, :] = False
ys, xs = np.where(redb)
if len(ys):
    print(f"  red bottom rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")

print("\n--- blue border components ---")
ys, xs = np.where(blue)
if len(ys):
    # cluster by x gaps
    uxs = np.unique(xs)
    clusters, s = [], uxs[0]
    for i in range(1, len(uxs)):
        if uxs[i] - uxs[i - 1] > 15:
            clusters.append((s, uxs[i - 1]))
            s = uxs[i]
    clusters.append((s, uxs[-1]))
    for (c0, c1) in clusters:
        sel = (xs >= c0) & (xs <= c1)
        yy = ys[sel]
        print(f"  x {c0}-{c1} (w={c1-c0+1})  y {yy.min()}-{yy.max()} (h={yy.max()-yy.min()+1})  px={sel.sum()}")
