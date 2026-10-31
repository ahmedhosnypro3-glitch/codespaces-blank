#!/usr/bin/env python3
"""Closed-loop check for slide_021 equation assets.

A mathtext source rendered as literal text is ONE tall-flat line with no
horizontal fraction bar; correctly stacked 2D math has a long horizontal ink
run (the bar). Report, for each asset: ink bbox, widest horizontal run, and the
row histogram shape, so stacked-fraction structure is provable without vision.
"""
import numpy as np
from PIL import Image
import os

D = "recreated_pptx/build/eq_assets/slide_021"
NAMES = ["eq1d", "eq2d", "eq3d", "eq1c", "eq2c", "eq3c"]

for n in NAMES:
    p = os.path.join(D, n + ".png")
    if not os.path.exists(p):
        print(f"{n}: MISSING")
        continue
    a = np.asarray(Image.open(p).convert("RGBA"))
    ink = a[:, :, 3] > 8
    if not ink.any():
        print(f"{n}: NO INK")
        continue
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = rows[0], rows[-1] + 1
    x0, x1 = cols[0], cols[-1] + 1
    sub = ink[y0:y1, x0:x1]
    # widest contiguous horizontal ink run per row -> the fraction bar is the max
    best_rows = []
    for i in range(sub.shape[0]):
        r = sub[i]
        if not r.any():
            continue
        # longest run of True
        d = np.diff(np.concatenate(([0], r.view(np.int8), [0])))
        starts = np.where(d == 1)[0]
        ends = np.where(d == -1)[0]
        longest = (ends - starts).max() if len(starts) else 0
        best_rows.append((int(longest), i))
    best_rows.sort(reverse=True)
    top = best_rows[0] if best_rows else (0, -1)
    # a stacked fraction: the longest bar spans a large fraction of the width
    widest, row = top
    frac = widest / sub.shape[1]
    # count distinct ink bands (text lines) vertically
    rowdens = sub.any(axis=1).view(np.int8)
    bands = int(np.sum(np.diff(np.concatenate(([0], rowdens, [0]))) == 1))
    print(f"{n}: ink {x1-x0}x{y1-y0} widest_run={widest}px "
          f"({frac:.0%} of width) @row {row} bands={bands}")
    verdict = "STACKED-OP-LIKE" if frac > 0.25 and bands >= 3 else \
              ("LITERAL-LINE-LIKE" if bands <= 2 else "AMBIGUOUS")
    print(f"      -> {verdict}")
