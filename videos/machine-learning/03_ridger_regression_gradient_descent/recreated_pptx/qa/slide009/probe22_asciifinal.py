#!/usr/bin/env python3
"""Probe 22: final clean ASCII of all remaining text elements using the robust
'differs from per-row background mode by > 60' predicate, at the CORRECT
y-windows (the 'mm' labels live beside the y-axis arrowheads at y~140..182,
NOT down in the caption band).
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
RED = (r - g > 30) & (r - b > 30) & (r > 90)


def mask_of(y0, y1, x0, x1, thr=60):
    m = np.zeros((y1 - y0 + 1, x1 - x0 + 1), bool)
    for i, y in enumerate(range(y0, y1 + 1)):
        row = a[y, x0:x1 + 1]
        q = (row // 8) * 8
        keys, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
        bg = keys[counts.argmax()]
        m[i] = np.abs(row - bg).max(axis=1) > thr
    return m


def dump(nm, x0, x1, y0, y1, thr=60):
    m = mask_of(y0, y1, x0, x1, thr)
    rm = RED[y0:y1 + 1, x0:x1 + 1] & m
    ys, xs = np.where(m)
    print(f"\n===== {nm} x{x0}..{x1} y{y0}..{y1} thr={thr} =====")
    if not len(ys):
        print("  no ink")
        return
    print(f"  INK x {x0+xs.min()}..{x0+xs.max()} (w={xs.max()-xs.min()+1}) "
          f"y {y0+ys.min()}..{y0+ys.max()} (h={ys.max()-ys.min()+1})")
    X0, X1 = x0 + xs.min() - 1, x0 + xs.max() + 1
    step = 2 if (X1 - X0) > 260 else 1
    print("      " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(X0, X1 + 1, step)))
    for y in range(y0 + ys.min(), y0 + ys.max() + 1):
        print(f"  {y:4d} " + "".join(
            "R" if rm[y - y0, x - x0] else ("#" if m[y - y0, x - x0] else " ")
            for x in range(X0, X1 + 1, step)))


dump("RCAP line1 'Generalized (Residuals are not minimized)'", 495, 838, 486, 506)
dump("RCAP line2 'Successes to detect the Pattern'", 495, 838, 506, 528)
dump("LEQ '50.85^2 = 2585'", 140, 462, 138, 182)
dump("REQ '63.64^2 = 4050'", 510, 866, 138, 186)
dump("LMM '50.85 mm'", 96, 160, 138, 186)
dump("RMM '63.64 mm'", 492, 560, 138, 186)
dump("BADGE numeral '9'", 858, 896, 55, 92)
