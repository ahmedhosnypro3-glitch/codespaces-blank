#!/usr/bin/env python3
"""Measure the white plot background box in the original frame for slide 033.

The build draws the house panel (E9E9E7, x54..903 y45..540) but never paints the
plot's white background, so the render shows panel gray where the original shows
white. Find the white box's exact x/y extent so the fix is measured, not guessed.
"""
from PIL import Image
import numpy as np, collections

ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg")
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)

# white / near-white mask
W = (o[:, :, 0] >= 244) & (o[:, :, 1] >= 244) & (o[:, :, 2] >= 244)
# ignore the outside-the-panel area (canvas is white there too) - only x54..903, y45..540
inside = np.zeros_like(W)
inside[45:540, 54:903] = True
W &= inside

print("=== white runs per column in the plot band y58..322 ===")
colcnt = W[58:322, :].sum(0)
cols = [x for x in range(54, 904) if colcnt[x] > 200]
if cols:
    print(f"columns with >200 white px in y58..322: x{cols[0]}..x{cols[-1]} (n={len(cols)})")
    # contiguous
    runs, cur = [], None
    for x in range(54, 904):
        if colcnt[x] > 200:
            cur = [x, x] if cur is None else [cur[0], x]
        elif cur:
            runs.append(tuple(cur)); cur = None
    if cur: runs.append(tuple(cur))
    print("contiguous column runs:", runs)

print()
print("=== white runs per row across x600..905 ===")
rowcnt = W[:, 600:905].sum(1)
rows = [y for y in range(45, 540) if rowcnt[y] > 200]
if rows:
    print(f"rows with >200 white px in x600..905: y{rows[0]}..y{rows[-1]} (n={len(rows)})")
    runs, cur = [], None
    for y in range(45, 540):
        if rowcnt[y] > 200:
            cur = [y, y] if cur is None else [cur[0], y]
        elif cur:
            runs.append(tuple(cur)); cur = None
    if cur: runs.append(tuple(cur))
    print("contiguous row runs:", runs)

print()
print("=== modal colour of the RENDER's plot interior vs ORIGINAL ===")
for lbl, (y0, y1, x0, x1) in {"orig plot": (200, 205, 760, 780),
                              "orig plot2": (240, 243, 700, 715),
                              "orig above-plot": (52, 56, 700, 760)}.items():
    c = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1): c[tuple(o[y, x])] += 1
    print(f"  {lbl}: {c.most_common(2)}")
