#!/usr/bin/env python3
"""Map SATURATED ink across the whole original frame by color family."""
import numpy as np
from PIL import Image
from collections import Counter

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]
mx = np.maximum(np.maximum(r, g), b)
mn = np.minimum(np.minimum(r, g), b)
sat = mx - mn
print(f"saturation stats: mean={sat.mean():.1f}, p95={np.percentile(sat,95):.0f}, p99={np.percentile(sat,99):.0f}")

# Green family: g dominant, saturated
green = (g - np.maximum(r, b) > 30) & (g > 80)
ys, xs = np.where(green)
print(f"\nGREEN family (g-max by >30, g>80): {len(ys)} px")
if len(ys):
    print(f"  rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")
    # histogram of rows
    print("  row histogram (bins of 20):")
    h, edges = np.histogram(ys, bins=27, range=(0, 540))
    for i, c in enumerate(h):
        if c: print(f"    rows {int(edges[i]):>3}-{int(edges[i+1]):>3}: {'#'*min(60,int(c/5))} {c}")
    print("  top colors:", Counter(map(tuple, o[green])).most_common(5))

# Red family: r dominant, saturated
red = (r - np.maximum(g, b) > 30) & (r > 90)
ys, xs = np.where(red)
print(f"\nRED family (r-max by >30, r>90): {len(ys)} px")
if len(ys):
    print(f"  rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")
    h, edges = np.histogram(ys, bins=27, range=(0, 540))
    for i, c in enumerate(h):
        if c: print(f"    rows {int(edges[i]):>3}-{int(edges[i+1]):>3}: {'#'*min(60,int(c/5))} {c}")
    print("  top colors:", Counter(map(tuple, o[red])).most_common(5))

# Purple family: b dominant, r mid (b>r, b>g, r>g)
purple = (b - r > 20) & (b - g > 30) & (b > 100) & (r > 50)
ys, xs = np.where(purple)
print(f"\nPURPLE family: {len(ys)} px")
if len(ys):
    print(f"  rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")
    h, edges = np.histogram(ys, bins=27, range=(0, 540))
    for i, c in enumerate(h):
        if c: print(f"    rows {int(edges[i]):>3}-{int(edges[i+1]):>3}: {'#'*min(60,int(c/5))} {c}")
    print("  top colors:", Counter(map(tuple, o[purple])).most_common(5))

# Blue family: b dominant and r low (pure blue 0000FF)
blue = (b - r > 60) & (b - g > 40) & (b > 120)
ys, xs = np.where(blue)
print(f"\nBLUE family (0000FF-ish): {len(ys)} px")
if len(ys):
    print(f"  rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")
    h, edges = np.histogram(ys, bins=27, range=(0, 540))
    for i, c in enumerate(h):
        if c: print(f"    rows {int(edges[i]):>3}-{int(edges[i+1]):>3}: {'#'*min(60,int(c/5))} {c}")
    print("  top colors:", Counter(map(tuple, o[blue])).most_common(5))

# Orange family: r high, g mid, b low
orange = (r > 180) & (g > 60) & (g < 190) & (b < 100) & (r - g > 30)
ys, xs = np.where(orange)
print(f"\nORANGE family: {len(ys)} px")
if len(ys):
    print(f"  rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")
    print("  top colors:", Counter(map(tuple, o[orange])).most_common(5))

# Yellow family: r,g high, b low
yellow = (r > 200) & (g > 200) & (b < 150)
ys, xs = np.where(yellow)
print(f"\nYELLOW family: {len(ys)} px")
if len(ys):
    print(f"  rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")
    h, edges = np.histogram(ys, bins=27, range=(0, 540))
    for i, c in enumerate(h):
        if c: print(f"    rows {int(edges[i]):>3}-{int(edges[i+1]):>3}: {'#'*min(60,int(c/5))} {c}")
    print("  top colors:", Counter(map(tuple, o[yellow])).most_common(5))

# Where is BLACK ink (dark) - axes and labels
dark = (mx < 90)
ys, xs = np.where(dark)
print(f"\nDARK ink: {len(ys)} px; rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")
print("  row histogram (bins of 20):")
h, edges = np.histogram(ys, bins=27, range=(0, 540))
for i, c in enumerate(h):
    if c: print(f"    rows {int(edges[i]):>3}-{int(edges[i+1]):>3}: {'#'*min(60,int(c/5))} {c}")
