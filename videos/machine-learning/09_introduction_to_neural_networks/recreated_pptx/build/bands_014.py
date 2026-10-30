#!/usr/bin/env python3
"""Read text rows in the equation panel by finding text-row segmentation per line band."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
im = Image.open(SRC).convert("L")
a = np.asarray(im).astype(int)

bands = [(327, 344), (384, 401), (411, 429), (450, 467)]
for (y0, y1) in bands:
    sub = a[y0:y1 + 1, 82:596]
    ink = sub < 200
    rows = ink.any(axis=1)
    ys = np.where(rows)[0]
    ytop, ybot = (ys.min() + y0, ys.max() + y0) if len(ys) else (None, None)
    cols = np.where(ink.any(axis=0))[0]
    xl, xr = (cols.min() + 82, cols.max() + 82) if len(cols) else (None, None)
    print(f"\n=== band y[{y0}..{y1}]  ink rows y[{ytop}..{ybot}]  x[{xl}..{xr}] ===")
    # column gaps => word separation
    colink = ink.any(axis=0)
    runs, inrun = [], False
    for i, v in enumerate(colink):
        if v and not inrun:
            inrun, st = True, i
        elif not v and inrun:
            inrun = False
            runs.append((st + 82, i - 1 + 82))
    if inrun:
        runs.append((st + 82, 596 - 1))
    # merge runs with gap < 6 px (letters/words)
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= 6:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(list(r))
    print("  text clusters (x-ranges):")
    for m in merged:
        print(f"    x[{m[0]}..{m[1]}] w={m[1]-m[0]+1}")
