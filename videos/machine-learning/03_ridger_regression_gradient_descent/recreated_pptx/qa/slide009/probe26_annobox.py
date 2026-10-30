#!/usr/bin/env python3
"""Probe 26b: pin down the annotation-box rectangle around each equation, with
CORRECTED white predicate (the panel interior measures (250,252,249), not 255).

Reports the box edge geometry, its fill/border colors, and the equation ink
bbox inside it.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = np.maximum(np.maximum(r, g), b)
mn = np.minimum(np.minimum(r, g), b)
SAT = mx - mn

WHT = (r > 244) & (g > 244) & (b > 243)
NOTW = ~WHT


def longest_run(mask):
    best = (0, 0, 0)
    cur = 0
    start = 0
    for i, v in enumerate(mask):
        if v:
            if cur == 0:
                start = i
            cur += 1
            if cur > best[0]:
                best = (cur, start, i)
        else:
            cur = 0
    return best


for nm, x0, x1 in (("LEFT", 120, 400), ("RIGHT", 560, 800)):
    print(f"\n########## {nm} annotation box ##########")
    # find rows whose LONGEST non-white run is between 90 and 200 px (a box band)
    rows = []
    for y in range(120, 210):
        n, s, e = longest_run(NOTW[y, x0:x1 + 1])
        if 90 <= n <= 210:
            rows.append((y, n, x0 + s, x0 + e))
    if not rows:
        print("  no box-like rows")
        continue
    print(f"  box rows: {rows[0][0]}..{rows[-1][0]} ({len(rows)} rows)")
    xs0 = min(t[2] for t in rows)
    xs1 = max(t[3] for t in rows)
    ys0, ys1 = rows[0][0], rows[-1][0]
    print(f"  box extent: x {xs0}..{xs1} (w={xs1-xs0+1}) y {ys0}..{ys1} (h={ys1-ys0+1})")
    for yy in (ys0 + 3, (ys0 + ys1) // 2, ys1 - 3):
        print(f"    row y={yy}: left run {longest_run(NOTW[yy, x0:x1+1])[1]+x0}..{longest_run(NOTW[yy, x0:x1+1])[2]+x0}"
              f"  samples x{xs0+4}={tuple(a[yy, xs0+4])} x{(xs0+xs1)//2}={tuple(a[yy, (xs0+xs1)//2])}")
    # vertical extent of the box: for each candidate column, the non-white run
    print("    per-column vertical non-white runs (box columns):")
    for xx in (xs0, xs0 + 1, xs0 + 2, (xs0 + xs1) // 2, xs1 - 2, xs1 - 1, xs1):
        col = NOTW[120:210, xx]
        n, s, e = longest_run(col)
        print(f"      x={xx}: run y {120+s}..{120+e} (n={n})")
    # fill color: text-free interior
    print("    interior fill samples:",
          [tuple(a[y, x]) for y in (ys0 + 4, ys0 + 8, ys1 - 5) for x in (xs0 + 5, xs0 + 20)])
    # equation text: achromatic black inside the box
    BLK = ((r + g + b) < 460) & (SAT <= 50)
    sub = BLK[ys0 + 3:ys1 - 2, xs0 + 3:xs1 - 2]
    ys, xs = np.where(sub)
    if len(ys):
        print(f"    equation ink: x {xs0+3+xs.min()}..{xs0+3+xs.max()} (w={xs.max()-xs.min()+1}) "
              f"y {ys0+3+ys.min()}..{ys0+3+ys.max()} (h={ys.max()-ys.min()+1})")
    else:
        print("    equation ink: <none>")
