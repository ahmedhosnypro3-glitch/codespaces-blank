#!/usr/bin/env python3
"""Probe 16: column/row ink profiles over the two caption bands, to detect any
thin vertical border lines (suspects: LEFT ~x502/x840 on the right half,
~x435..472 at y528 on the left half) and to get the true per-line text bboxes
with those border columns excluded.

Also: exact ink bbox of each caption line, excluding columns whose ink spans
> 40 rows in the band (i.e. vertical rules, not glyphs).
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)

BAND = (478, 528)
for nm, x0, x1 in (("LEFT", 100, 472), ("RIGHT", 480, 878)):
    print(f"\n########## {nm} caption band x{x0}..{x1} ##########")
    y0, y1 = BAND
    # per-column row-count of "differs from local background by >55"
    colrows = np.zeros(x1 - x0 + 1, int)
    for y in range(y0, y1 + 1):
        row = a[y, x0:x1 + 1]
        q = (row // 8) * 8
        keys, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
        bg = keys[counts.argmax()]
        colrows += (np.abs(row - bg).max(axis=1) > 55)
    tall = np.where(colrows > 40)[0]
    print("  columns with >40 inked rows (vertical rules):",
          [x0 + t for t in tall] if len(tall) else "none")
    # line bboxes excluding those columns
    good = colrows <= 40
    for (l0, l1, label) in ((486, 506, "LINE1"), (506, 528, "LINE2")):
        sub = np.zeros((l1 - l0 + 1, x1 - x0 + 1), bool)
        for y in range(l0, l1 + 1):
            row = a[y, x0:x1 + 1]
            q = (row // 8) * 8
            keys, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
            bg = keys[counts.argmax()]
            sub[y - l0] = (np.abs(row - bg).max(axis=1) > 55)
        sub[:, ~good] = False
        ys, xs = np.where(sub)
        if not len(ys):
            print(f"  {label}: no ink")
            continue
        print(f"  {label} y{l0}..{l1}: text ink x {x0+xs.min()}..{x0+xs.max()} "
              f"(w={xs.max()-xs.min()+1}) y {l0+ys.min()}..{l0+ys.max()} (h={ys.max()-ys.min()+1}) "
              f"center x {(x0+xs.min()+x0+xs.max())/2:.1f}")
