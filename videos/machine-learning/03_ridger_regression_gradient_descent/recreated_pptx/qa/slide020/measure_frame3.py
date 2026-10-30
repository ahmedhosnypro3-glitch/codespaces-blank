#!/usr/bin/env python3
"""Underline band + glyph x-extent precision measurement for slide_020.jpg."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_020.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)

# underline-only: rows 337..342, count columns with red in each row and extents
print("== per-row underline extents (rows 336..343) ==")
for y in range(336, 344):
    cols = np.where(red[y, :])[0]
    if len(cols):
        print(f"  y={y}: px={len(cols)} x {cols.min()}..{cols.max()}")
    else:
        print(f"  y={y}: 0")

# glyphs-only x extent of line 2 (rows 310..336, excl underline core)
cols2 = np.where(red[310:337, :].any(axis=0))[0]
print("line-2 glyph x extent (rows 310-336):", cols2.min(), "..", cols2.max(), " width:", cols2.max()-cols2.min()+1)

# line-1 x extent
cols1 = np.where(red[228:266, :].any(axis=0))[0]
print("line-1 glyph x extent (rows 228-266):", cols1.min(), "..", cols1.max(), " width:", cols1.max()-cols1.min()+1)

# underline: columns where rows 338-340 are ALL red (solid core)
core = red[338:341, :].all(axis=0)
c = np.where(core)[0]
print("underline solid-core columns:", c.min(), "..", c.max(), " width:", c.max()-c.min()+1, " count:", len(c))

# 'i' stem width test (bold vs regular): 'i' in "Ridge" — Ridge starts at ~209
# stem = contiguous red run at mid-x-height row through 'i'
print("== stem-width probe: row 248 (mid x-height line1), runs of 3+ px, x 200..320 ==")
row = red[248, 200:320]
runs = []
start = None
for i, v in enumerate(row):
    if v and start is None: start = i
    if not v and start is not None:
        runs.append((start+200, i-1+200, i-start)); start = None
if start is not None: runs.append((start+200, len(row)-1+200, len(row)-start))
print("  runs:", runs)
# row through cap band of 'I' in Inverse (line 2, x~183-190), row 322
row2 = red[322, 175:200]
print("== 'I' stem row 322, x 175..200:", list(row2.astype(int)))
