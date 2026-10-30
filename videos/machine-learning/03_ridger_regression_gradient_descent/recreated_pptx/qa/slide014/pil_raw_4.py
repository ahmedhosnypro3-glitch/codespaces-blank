#!/usr/bin/env python3
"""Raw pixel dumps: lower blue region rows + mid band text colors; plus render comparison."""
from PIL import Image
import numpy as np
from collections import Counter

def dump_row(a, y, xs, label):
    print(f"{label} y={y}:")
    seen = []
    for x in xs:
        r, g, b = a[y, x]
        seen.append((x, int(r), int(g), int(b)))
    print("   ", seen)

def color_runs(a, y, x0, x1, tol=30):
    """Print contiguous color runs along a row."""
    runs = []
    cur = tuple(a[y, x0]); s = x0
    for x in range(x0 + 1, x1 + 1):
        c = tuple(a[y, x])
        if sum(abs(int(c[i]) - int(cur[i])) for i in range(3)) > tol:
            runs.append((s, x - 1, cur)); cur = c; s = x
    runs.append((s, x1, cur))
    return runs

im = Image.open("unique_slides/slide_014.jpg").convert("RGB")
a = np.asarray(im).astype(int)

print("=== LOWER BLUE REGION — color runs per row (x60..905) ===")
for y in (468, 470, 475, 480, 485, 490, 495, 500, 505, 510, 515, 520, 525, 528):
    runs = color_runs(a, y, 60, 905, tol=40)
    # compress: only runs wider than 8px
    big = [(s, e, c) for (s, e, c) in runs if e - s > 8]
    print(f"y={y}: {big}")

print("\n=== MID BAND 1 (peach) — text ink colors y355..390 ===")
for y in (355, 360, 365, 370, 375, 380, 385):
    sub = a[y, 90:665]
    d = np.abs(sub - np.array([249, 222, 193])).sum(axis=1)
    w = np.abs(sub - np.array([255, 255, 255])).sum(axis=1)
    mask = (d > 90) & (w > 90)
    cols = [tuple(sub[i]) for i in range(len(sub)) if mask[i]]
    cc = Counter(cols)
    print(f"y={y}: n={len(cols)} top={cc.most_common(3)}")

print("\n=== MID BAND 2 (peach) — text ink colors y405..444 ===")
for y in (410, 415, 420, 425, 430, 435, 440):
    sub = a[y, 89:471]
    d = np.abs(sub - np.array([248, 223, 193])).sum(axis=1)
    w = np.abs(sub - np.array([255, 255, 255])).sum(axis=1)
    mask = (d > 90) & (w > 90)
    cols = [tuple(sub[i]) for i in range(len(sub)) if mask[i]]
    cc = Counter(cols)
    print(f"y={y}: n={len(cols)} top={cc.most_common(3)}")

print("\n=== MID BAND 3 (yellow) — text ink colors y405..444 ===")
for y in (410, 415, 420, 425, 430, 435, 440):
    sub = a[y, 533:880]
    d = np.abs(sub - np.array([251, 252, 218])).sum(axis=1)
    w = np.abs(sub - np.array([255, 255, 255])).sum(axis=1)
    mask = (d > 90) & (w > 90)
    cols = [tuple(sub[i]) for i in range(len(sub)) if mask[i]]
    cc = Counter(cols)
    print(f"y={y}: n={len(cols)} top={cc.most_common(3)}")

print("\n=== MID BAND 1 — x extents of text line by row ===")
for y in range(348, 393):
    sub = a[y, 90:665]
    d = np.abs(sub - np.array([249, 222, 193])).sum(axis=1)
    w = np.abs(sub - np.array([255, 255, 255])).sum(axis=1)
    mask = (d > 90) & (w > 90)
    n = int(mask.sum())
    xs = [90 + i for i in range(len(sub)) if mask[i]]
    if n:
        print(f"y={y}: n={n} x{min(xs)}..{max(xs)}")
    else:
        print(f"y={y}: n=0")
