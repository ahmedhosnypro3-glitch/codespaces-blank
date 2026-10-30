#!/usr/bin/env python3
"""att9 pre-build measurement: 048 rows 2-6 right-side W-column anatomy at thr<200.

Per row (y-windows from the calc-panel boxes), full x-census of x690..775:
per-column-run x-runs + y-bands + mean color -> pins W= x, bar xs, digit xs.
Plus: Initial-W '=' check (x440..470 y55..80, expect none) and row-1
semicolons (x660..668 / x715..721, y160..182).
"""
from PIL import Image
import numpy as np

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
O48 = np.array(Image.open(f"{DECK}/unique_slides/slide_048.jpg").convert("RGB")).astype(int)
H, W = O48.shape[:2]
print(f"orig size {W}x{H}")
SUM = O48.sum(axis=2)

# ink bands: row windows minus the calc-panel rule rows (measured: rules at
# 140/197/206/263/272/330/338/395/404/461/470/528, att9_meas2 §7 + meas4 §4)
ROWS = [(2, 207, 262), (3, 273, 328), (4, 339, 394), (5, 405, 460), (6, 471, 527)]

for r, y0, y1 in ROWS:
    print(f"\n===== row {r} (y{y0}..{y1}) right side x690..775 thr<200 =====")
    zone = SUM[y0:y1, 690:776] < 600
    colmask = zone.any(axis=0)
    runs, s = [], None
    for i, v in enumerate(colmask):
        if v and s is None: s = i
        elif not v and s is not None: runs.append((s, i - 1)); s = None
    if s is not None: runs.append((s, len(colmask) - 1))
    for a, b in runs:
        xs, xe = 690 + a, 690 + b
        sub = zone[:, a:b + 1]
        rows_ink = sub.any(axis=1)
        yb, s2 = [], None
        for j, v in enumerate(rows_ink):
            if v and s2 is None: s2 = j
            elif not v and s2 is not None: yb.append((y0 + s2, y0 + j - 1)); s2 = None
        if s2 is not None: yb.append((y0 + s2, y0 + len(rows_ink) - 1))
        mean = O48[y0:y1, xs:xe + 1][sub].mean(axis=0).astype(int)
        npx = int(sub.sum())
        print(f"  x{xs}..{xe} yb={yb} mean={tuple(mean)} npx={npx}")

print("\n===== Initial-W '=' check (x440..470, y55..80) thr<200 =====")
zone = SUM[55:81, 440:471] < 600
print(f"  ink px={int(zone.sum())} (expect 0 or near-0; runs below if any)")
colmask = zone.any(axis=0)
runs, s = [], None
for i, v in enumerate(colmask):
    if v and s is None: s = i
    elif not v and s is not None: runs.append((440 + s, 440 + i - 1)); s = None
if s is not None: runs.append((440 + s, 470))
for a, b in runs:
    rows_ink = zone[:, a - 440:b - 440 + 1].any(axis=1)
    ys = [55 + j for j, v in enumerate(rows_ink) if v]
    print(f"  x{a}..{b} y{min(ys)}..{max(ys)} npx={int(zone[:, a-440:b-440+1].sum())}")

print("\n===== row-1 semicolons thr<200 =====")
for x0, x1, tag in [(660, 669, "vec1"), (715, 722, "vec2")]:
    zone = SUM[160:183, x0:x1 + 1] < 600
    colmask = zone.any(axis=0)
    runs, s = [], None
    for i, v in enumerate(colmask):
        if v and s is None: s = i
        elif not v and s is not None: runs.append((x0 + s, x0 + i - 1)); s = None
    if s is not None: runs.append((x0 + s, x1))
    print(f"  {tag} x{x0}..{x1}:")
    for a, b in runs:
        sub = zone[:, a - x0:b - x0 + 1]
        rows_ink = sub.any(axis=1)
        yb, s2 = [], None
        for j, v in enumerate(rows_ink):
            if v and s2 is None: s2 = j
            elif not v and s2 is not None: yb.append((160 + s2, 160 + j - 1)); s2 = None
        if s2 is not None: yb.append((160 + s2, 182))
        mean = O48[160:183, a:b + 1][sub].mean(axis=0).astype(int)
        print(f"    x{a}..{b} yb={yb} mean={tuple(mean)} npx={int(sub.sum())}")
