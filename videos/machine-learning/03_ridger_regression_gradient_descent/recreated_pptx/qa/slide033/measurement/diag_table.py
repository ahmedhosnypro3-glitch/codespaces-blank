#!/usr/bin/env python3
"""Exact table band structure: row bands + per-band fill + column structure."""
import numpy as np
from PIL import Image
from collections import Counter

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)

# Scan a clean column inside the table (col 877 is right of data 866, inside panel)
print("=== Vertical scan at col 880 (inside panel, right of table) y 318-522 ===")
prev = None; start = None
for y in range(318, 523):
    c = tuple(o[y, 880])
    if c != prev:
        if prev is not None and y - start >= 2:
            print(f"  y {start}-{y-1} (h={y-start}): {prev}")
        prev = c; start = y
print(f"  y {start}-522: {prev}")

print("\n=== Vertical scan at col 100 (label col region) y 318-522 ===")
prev = None; start = None
for y in range(318, 523):
    c = tuple(o[y, 100])
    if c != prev:
        if prev is not None and y - start >= 2:
            print(f"  y {start}-{y-1} (h={y-start}): {prev}")
        prev = c; start = y
print(f"  y {start}-522: {prev}")

print("\n=== Row-band dominant fill (x 95-865, per row) ===")
prev = None; start = None
for y in range(318, 523):
    cnt = Counter(tuple(o[y, x]) for x in range(95, 866, 5))
    # drop text pixels (dark) by taking the mode of all samples
    dom = cnt.most_common(1)[0][0]
    if dom != prev:
        if prev is not None and y - start >= 4:
            print(f"  y {start}-{y-1} (h={y-start}): fill {prev}")
        prev = dom; start = y
print(f"  y {start}-522: fill {prev}")

print("\n=== Column boundaries at row 460 and 490 (data-free rows) ===")
for ry in [460, 490]:
    segs = []
    prev = None; start = None
    for x in range(90, 870):
        c = tuple(o[ry, x])
        # quantize
        q = (c[0] // 12, c[1] // 12, c[2] // 12)
        if q != prev:
            if prev is not None and x - start >= 6:
                segs.append(f"{start}-{x-1}:{tuple(v*12 for v in prev)}")
            prev = q; start = x
    segs.append(f"{start}-869:{tuple(v*12 for v in prev)}")
    print(f"  row {ry}: " + " ".join(se for se in segs if not se.split(':')[1].startswith('(228') and 'fill' in str(se)))

print("\n=== Plot: curve trace. For each col 615-830, find green curve y ===")
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]
green = (g - r > 18) & (g - b > 18) & (g > 80)
pts = {}
for x in range(612, 835):
    ys_ = np.where(green[110:340, x])[0]
    if len(ys_):
        pts[x] = 110 + ys_.mean()
print(f"  green curve in plot: {len(pts)} cols")
if pts:
    xs_ = sorted(pts)
    print(f"  cols {xs_[0]}..{xs_[-1]}")
    # print every 10th
    for x in xs_[::12]:
        print(f"    x={x}: y={pts[x]:.1f}")

print("\n=== Strong dark curve in plot (any saturated dark ink) ===")
mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
curv = (mx - mn) > 60
for x in range(612, 835, 4):
    ys_ = np.where(curv[110:340, x])[0]
    if len(ys_):
        # cluster
        groups = []
        cur = [ys_[0]]
        for v in ys_[1:]:
            if v - cur[-1] <= 3:
                cur.append(v)
            else:
                groups.append((cur[0] + 110, cur[-1] + 110)); cur = [v]
        groups.append((cur[0] + 110, cur[-1] + 110))
        if groups:
            print(f"  x={x}: groups y {groups}")
