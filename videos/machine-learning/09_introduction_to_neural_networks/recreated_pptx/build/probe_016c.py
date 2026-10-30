#!/usr/bin/env python3
"""slide_016 original: exact structure scans + per-letter metrics."""
from PIL import Image
import numpy as np

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_016.jpg"
a = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
H, W = a.shape[:2]
print(f"image {W}x{H}")


def scanrow(y, x0, x1, step=1, label=""):
    print(f"\n-- row {y} {label} x[{x0},{x1}] --")
    out = []
    prev = None
    start = x0
    for x in range(x0, x1, step):
        c = tuple(a[y, x])
        if c != prev:
            if prev is not None:
                out.append((start, x - 1, prev))
            prev = c
            start = x
    out.append((start, x1 - 1, prev))
    for (s, e, c) in out:
        if e - s >= 0:
            print(f"   x {s}-{e}: {c}")


def scancol(x, y0, y1, step=1, label=""):
    print(f"\n-- col {x} {label} y[{y0},{y1}] --")
    out = []
    prev = None
    start = y0
    for y in range(y0, y1, step):
        c = tuple(a[y, x])
        if c != prev:
            if prev is not None:
                out.append((start, y - 1, prev))
            prev = c
            start = y
    out.append((start, y1 - 1, prev))
    for (s, e, c) in out:
        print(f"   y {s}-{e}: {c}")


scanrow(300, 40, 80, label="(left edge at title-subtitle mid)")
scanrow(120, 40, 80, label="(left edge upper)")
scanrow(300, 890, 930, label="(right edge)")
scanrow(45, 40, 90, label="(top-left corner region)")
scancol(480, 36, 56, label="(top edge center)")
scancol(480, 500, 540, label="(bottom edge center)")
scanrow(525, 20, 960, step=4, label="(bottom strip row)")

# structure extents
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mx = a.max(axis=2)
gray = (abs(r - 234) < 14) & (abs(g - 234) < 14) & (abs(b - 234) < 14)
white = a.min(axis=2) > 242
dark = mx < 120
print("\n-- structural extents --")
ys, xs = np.where(gray)
print(f"  gray panel bbox: x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} (in: x {xs.min()/W*13.33:.2f}-{xs.max()/W*13.33:.2f}, y {ys.min()/H*7.5:.2f}-{ys.max()/H*7.5:.2f})")
print(f"  gray px count {int(gray.sum())}")
# rows near bottom: black counts
for y in range(500, 540):
    c = int(dark[y].sum())
    if c:
        cols = np.where(dark[y])[0]
        print(f"  row {y}: dark={c} x {cols.min()}-{cols.max()}")
print()
for x in (48, 50, 52, 60, 62, 64, 66, 900, 902, 904, 906, 908, 910):
    col = np.where(dark[:, x])[0]
    col = col[(col > 40) & (col < 520)]
    print(f"  col {x}: dark rows {col.min() if len(col) else '-'}..{col.max() if len(col) else '-'} count {len(col)}")
