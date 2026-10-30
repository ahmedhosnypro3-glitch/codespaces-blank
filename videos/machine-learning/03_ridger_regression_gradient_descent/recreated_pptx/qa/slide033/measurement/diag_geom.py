#!/usr/bin/env python3
"""Comprehensive geometry extraction from slide_033.jpg."""
import numpy as np
from PIL import Image
from collections import Counter

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]

print("=== CYAN regions (b>80, g>80, r<120) ===")
cyan = (b > 80) & (g > 80) & (r < 120) & (b - r > 30)
# connected components via simple row/col clustering
ys, xs = np.where(cyan)
if len(ys):
    print(f"  total {len(ys)} px, extent rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()}")
    # row histogram
    h, e = np.histogram(ys, bins=54, range=(0, 540))
    for i, c in enumerate(h):
        if c > 60:
            # column extent for this row band
            m = (ys >= e[i]) & (ys < e[i+1])
            print(f"    rows {int(e[i]):>3}-{int(e[i+1]):>3}: n={c:>5} cols {xs[m].min()}-{xs[m].max()}")

print("\n=== GREEN regions (g>80, g-r>20, g-b>20) ===")
green = (g - r > 20) & (g - b > 20) & (g > 80)
ys, xs = np.where(green)
if len(ys):
    print(f"  total {len(ys)} px, extent rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()}")
    h, e = np.histogram(ys, bins=54, range=(0, 540))
    for i, c in enumerate(h):
        if c > 60:
            m = (ys >= e[i]) & (ys < e[i+1])
            print(f"    rows {int(e[i]):>3}-{int(e[i+1]):>3}: n={c:>5} cols {xs[m].min()}-{xs[m].max()}")

print("\n=== PURPLE-ish saturated (b-r>25, b>90, r>60) ===")
pur = (b - r > 25) & (b > 90) & (r > 60)
ys, xs = np.where(pur)
if len(ys):
    print(f"  total {len(ys)} px, extent rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()}")
    h, e = np.histogram(ys, bins=54, range=(0, 540))
    for i, c in enumerate(h):
        if c > 60:
            m = (ys >= e[i]) & (ys < e[i+1])
            print(f"    rows {int(e[i]):>3}-{int(e[i+1]):>3}: n={c:>5} cols {xs[m].min()}-{xs[m].max()}")

print("\n=== Strong RED (r>150, r-g>60, r-b>60) ===")
red = (r > 150) & (r - g > 60) & (r - b > 60)
ys, xs = np.where(red)
if len(ys):
    print(f"  total {len(ys)} px, extent rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()}")
    h, e = np.histogram(ys, bins=54, range=(0, 540))
    for i, c in enumerate(h):
        if c > 40:
            m = (ys >= e[i]) & (ys < e[i+1])
            print(f"    rows {int(e[i]):>3}-{int(e[i+1]):>3}: n={c:>5} cols {xs[m].min()}-{xs[m].max()}")

print("\n=== LONG VERTICAL dark-ish lines (axes) ===")
dark = (r < 130) & (g < 130) & (b < 130)
for col in range(50, 940):
    n = dark[45:520, col].sum()
    if n > 60:
        rows_ = np.where(dark[45:520, col])[0] + 45
        print(f"  col {col}: {n} px, rows {rows_.min()}-{rows_.max()}")

print("\n=== LONG HORIZONTAL dark-ish lines ===")
for row in range(45, 540):
    n = dark[row, 50:940].sum()
    if n > 60:
        cols_ = np.where(dark[row, 50:940])[0] + 50
        print(f"  row {row}: {n} px, cols {cols_.min()}-{cols_.max()}")

print("\n=== Parameter box vertical scan (x=80..180 step 10) y 240-315 ===")
for x in range(80, 190, 10):
    prev = None; start = None
    segs = []
    for y in range(238, 318):
        c = (int(r[y, x]), int(g[y, x]), int(b[y, x]))
        if c != prev:
            if prev is not None:
                segs.append((start, y - 1, prev))
            prev = c; start = y
    segs.append((start, 317, prev))
    print(f" x={x}: " + " | ".join(f"{s}-{e}:{c}" for s, e, c in segs if e - s >= 2))
