#!/usr/bin/env python3
"""Probe 1 — structural map of slide_010.jpg (960x540, 1px=1pt).

Coarse ASCII downsample + row/column ink profiles so the panels, grids,
fitted lines, points, caption bands and badge can be located before any
geometry decisions.
"""
from PIL import Image
import collections

IMG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_010.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
print("size:", im.size)
px = im.load()

# ---- color cores (quantize to /16 buckets) ----
cnt = collections.Counter()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        cnt[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
print("top colors (bucket, pct):")
tot = W * H
for c, n in cnt.most_common(18):
    print("  ", c, f"{100.0*n/tot:5.2f}%")

# ---- ASCII luminance map: 120x54 (each cell 8x10 px) ----
print("\nASCII luminance map (120x54 cells, 8x10 px each):")
chars = " .:-=+*#%@"
for cy in range(54):
    row = []
    for cx in range(120):
        s = 0
        for yy in range(cy * 10, cy * 10 + 10, 2):
            for xx in range(cx * 8, cx * 8 + 8, 2):
                r, g, b = px[xx, yy]
                s += (r + g + b) / 3
        v = s / 40
        row.append(chars[min(9, int((255 - v) / 25.6))])
    print("".join(row))

# ---- red-ish ink columns (find vertical structures) ----
def is_red(c):
    r, g, b = c
    return r > 120 and r - g > 60 and r - b > 60
print("\nred x-profile (x: count of red px in column):")
for x in range(0, W, 4):
    n = sum(1 for y in range(H) if is_red(px[x, y]))
    if n > 40:
        print(f"  x={x}: {n}")

print("\nred y-profile (y: count of red px in row):")
for y in range(0, H, 4):
    n = sum(1 for x in range(W) if is_red(px[x, y]))
    if n > 40:
        print(f"  y={y}: {n}")
