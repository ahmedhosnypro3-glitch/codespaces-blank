#!/usr/bin/env python3
"""Slide 020: per-line ink widths in ORIGINAL vs RENDER for the multi-line
text blocks, so fonts can be scaled to the original's typography."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
S = 960 / 13.3333
IN = 2001 / 13.3333
O = np.array(Image.open(f"{NS}/unique_slides/slide_020.jpg").convert("L")).astype(int)
R = np.array(Image.open(f"{NS}/qa/slide020/b10wave2/render-1.png").convert("L")).astype(int)


def lines(a, sc, x0, x1, y0, y1, gap):
    """split a block into lines by horizontal zero-runs"""
    X0, X1, Y0, Y1 = (int(v * sc) for v in (x0, x1, y0, y1))
    sub = a[Y0:Y1, X0:X1] < 200
    rows = sub.sum(axis=1)
    out, s, none_since = [], None, 0
    h = Y1 - Y0
    gp = gap * sc
    for y, v in enumerate(rows):
        if v > 0:
            if s is None:
                s = y
            none_since = 0
        elif s is not None:
            none_since += 1
            if none_since > gp:
                out.append((s, y - none_since))
                s = None
    if s is not None:
        out.append((s, len(rows)))
    res = []
    for (a_, b_) in out:
        band = sub[a_:b_ + 1]
        cols = band.sum(axis=0)
        xs = np.where(cols > 0)[0]
        if len(xs) == 0:
            continue
        res.append(((a_ + Y0) / sc, (b_ + Y0) / sc, (xs.min() + X0) / sc,
                    (xs.max() + X0) / sc, (xs.max() - xs.min()) / sc))
    return res


print("=== CYAN CHAIN BOX (declared text x 0.78, y 0.96/1.57/2.18/2.79) ===")
for tag, a, sc in (("ORIG", O, S), ("REND", R, IN)):
    ls = lines(a, sc, 0.7, 5.45, 0.80, 3.25, 0.10)
    print(f"--- {tag}: {len(ls)} lines")
    for y0, y1, x0, x1, w in ls:
        print(f"   y {y0:.3f}-{y1:.3f}  x {x0:.3f}-{x1:.3f}  w={w:.3f} in")

print("\n=== CREAM DERIV PANEL (x 9.15-12.60) ===")
for tag, a, sc in (("ORIG", O, S), ("REND", R, IN)):
    ls = lines(a, sc, 9.10, 12.65, 3.35, 6.50, 0.08)
    print(f"--- {tag}: {len(ls)} lines")
    for y0, y1, x0, x1, w in ls:
        print(f"   y {y0:.3f}-{y1:.3f}  x {x0:.3f}-{x1:.3f}  w={w:.3f} in")

print("\n=== NODE MODE caption (x 5.6-7.2, y 2.80-3.25) ===")
for tag, a, sc in (("ORIG", O, S), ("REND", R, IN)):
    ls = lines(a, sc, 5.55, 7.30, 2.75, 3.25, 0.04)
    print(f"--- {tag}: {len(ls)} lines")
    for y0, y1, x0, x1, w in ls:
        print(f"   y {y0:.3f}-{y1:.3f}  x {x0:.3f}-{x1:.3f}  w={w:.3f} in")
