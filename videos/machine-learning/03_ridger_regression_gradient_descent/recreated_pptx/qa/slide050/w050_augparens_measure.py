#!/usr/bin/env python3
"""Measure the 050 augmented-table tall-paren columns + digit bands (orig frame).
Paren strokes span the full table height, so scanning the row-GAP bands isolates
paren ink from digit ink."""
import numpy as np
from PIL import Image

NS = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(NS + "/unique_slides/slide_050.jpg").convert("RGB")).astype(int)

panel = o[136:250, 66:250]
lum = panel.mean(axis=2)
ink = lum < 190

def clusters(cols, gap=3):
    if len(cols) == 0:
        return []
    out, s, p = [], cols[0], cols[0]
    for c in cols[1:]:
        if c - p > gap:
            out.append((s, p)); s = c
        p = c
    out.append((s, p))
    return out

# row-gap bands (no digit ink there if parens are continuous)
for band, lo, hi in [("gap1", 191, 197), ("gap2", 208, 212), ("above", 176, 182), ("below", 223, 229)]:
    cols = np.where(ink[lo-136:hi-136].any(axis=0))[0]
    cl = clusters(cols)
    print("%s (y%d..%d) ink cols:" % (band, lo, hi), [(66+a, 66+b) for a, b in cl])

# vertical runs: columns with >=25 continuous ink rows in y178..224
runs = []
for xx in range(panel.shape[1]):
    col = ink[178-136:225-136, xx]
    # longest run
    best = cur = 0
    for v in col:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    if best >= 20:
        runs.append((66+xx, best))
print("cols with runs>=20 in y178..224:", runs)

# digit bands: per-row ink inside the table (x66..250), excluding paren columns
print("\nrow profile y178..228 (ink px per row, full panel width):")
for yy in range(178, 229):
    print("  y%d n=%d" % (yy, int(ink[yy-136].sum())))

# digit column x-extents per row band (exclude paren columns found above)
paren_cols = [c for c, _ in runs]
mask = ink.copy()
for c in paren_cols:
    cc = c - 66
    for d in (-1, 0, 1):
        if 0 <= cc+d < mask.shape[1]:
            mask[:, cc+d] = False
for lo, hi, tag in [(183, 191, "row1"), (198, 208, "row2"), (213, 223, "row3"), (231, 240, "clsrow")]:
    cols = np.where(mask[lo-136:hi-136].any(axis=0))[0]
    cl = clusters(cols, gap=4)
    print("%s digit clusters:" % tag, [(66+a, 66+b) for a, b in cl])
