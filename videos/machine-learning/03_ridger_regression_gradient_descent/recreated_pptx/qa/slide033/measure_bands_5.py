#!/usr/bin/env python3
"""Precise band-boundary measurement for slide 033 (frame px, 1px=1pt).

For each candidate band colour, find the exact y-extent AND the exact x-extent
of the fill, sampling only columns where that colour is the mode (so text and
gridline ink does not shift the answer). Also report whether the fill covers the
label column x86-121 or only the data columns x121-869.
"""
from PIL import Image
import numpy as np, collections

ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg")
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)

BANDS = {
    "D9E275": (217, 226, 119),
    "D6B2F5": (214, 178, 248),
    "F7DDC2": (247, 221, 194),
    "DEAC95": (222, 172, 149),
    "F7BEC4": (247, 190, 196),
}

for name, (R, G, B) in BANDS.items():
    m = (np.abs(o[:, :, 0] - R) < 22) & (np.abs(o[:, :, 1] - G) < 22) & (np.abs(o[:, :, 2] - B) < 34)
    ys, xs = np.where(m)
    if len(xs) == 0:
        print(f"{name}: NOT FOUND"); continue
    # per-row pixel counts, only inside the table's data area x121-869
    print(f"\n{name}  total px {len(xs)}  raw bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}")
    print("  rows (y: count in x121..869):")
    rows = []
    for y in range(ys.min(), ys.max() + 1):
        c = int(m[y, 121:869].sum())
        if c: rows.append((y, c))
    # find contiguous runs where count > 100 (a filled row)
    runs = []
    cur = None
    for y, c in rows:
        if c > 100:
            if cur is None: cur = [y, y]
            else: cur[1] = y
        else:
            if cur: runs.append(tuple(cur)); cur = None
    if cur: runs.append(tuple(cur))
    print("   contiguous full-width-ish runs:", runs)
    for r in runs:
        print(f"   -> band y{r[0]}-{r[1]} (h{r[1]-r[0]+1})")
    # x extent within the first run
    if runs:
        y0, y1 = runs[0]
        sub = m[y0:y1 + 1, :]
        xs2 = np.where(sub.any(0))[0]
        print(f"   x-extent of run y{y0}-{y1}: x{xs2.min()}-{xs2.max()}")
        print(f"   label col x86-121 px: {int(m[y0:y1+1, 86:121].sum())}"
              f"   data col x121-869 px: {int(m[y0:y1+1, 121:869].sum())}")
