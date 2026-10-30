#!/usr/bin/env python3
"""Probe 57: precise equation ink bbox (luminance-difference mask, catches the
antialiased superscript that strict achromatic masks miss)."""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
lum = a.mean(axis=2)

BOXES = {"LEFT": (216, 317, 147, 175), "RIGHT": (631, 735, 146, 176)}
for nm, (x0, x1, y0, y1) in BOXES.items():
    sub = lum[y0:y1 + 1, x0:x1 + 1]
    # fill median from the border-free rows/cols
    med = np.median(sub)
    ink = sub < (med - 25)
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    print(f"=== {nm} box x{x0}..{x1} y{y0}..{y1} (fill lum median {med:.0f}) ===")
    print(f"  ink bbox: x {cols.min()+x0}..{cols.max()+x0} (w={cols.max()-cols.min()+1}) "
          f"y {rows.min()+y0}..{rows.max()+y0} (h={rows.max()-rows.min()+1}) n={int(ink.sum())}")
    # per-row ink extents
    for y in range(rows.min() + y0, rows.max() + y0 + 1):
        xs = np.where(ink[y - y0])[0]
        if len(xs):
            print(f"    y={y}: x {xs.min()+x0}..{xs.max()+x0} n={len(xs)}")
    # split main line vs superscript: find the widest contiguous horizontal band
    rh = ink.sum(axis=1)
    print("  row ink counts:", {int(y + y0): int(rh[y]) for y in range(len(rh)) if rh[y] > 0})
