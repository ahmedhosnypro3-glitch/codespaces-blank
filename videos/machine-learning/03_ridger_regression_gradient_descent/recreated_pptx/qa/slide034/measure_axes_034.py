#!/usr/bin/env python3
"""Locate slide_034's original plot axes: x-axis line, y-axis line, tick labels."""
import numpy as np
from PIL import Image

ROOT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
im = np.asarray(Image.open(ROOT + "/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
X0, X1, Y0, Y1 = 608, 847, 60, 312
box = im[Y0:Y1, X0:X1]
r, g, b = box[:, :, 0], box[:, :, 1], box[:, :, 2]
lum = box.sum(axis=2)

# Non-cyan, non-red, non-pink, non-white ink = axis lines + tick labels
ink = (lum < 480)
# exclude the pink callout region (frame y 270..306)
ink[270 - Y0:, :] = False
# exclude the red border rows/cols
ink[:4, :] = False; ink[-4:, :] = False
ink[:, :4] = False; ink[:, -4:] = False

rowcnt = ink.sum(axis=1)
print("rows with >40 ink px:", [(Y0 + int(i), int(c)) for i, c in enumerate(rowcnt) if c > 40])
colcnt = ink.sum(axis=0)
print("cols with >40 ink px:", [(X0 + int(i), int(c)) for i, c in enumerate(colcnt) if c > 40])

# Text blobs below the x-axis (y=172): tick labels
below = box[172 - Y0:250 - Y0, :]
lb = below.sum(axis=2) < 450
rows = lb.sum(axis=1)
print("\nbelow-axis ink rows:", [(172 + int(i), int(c)) for i, c in enumerate(rows) if c > 5][:40])

# group into blobs by x to find tick label groups
lab = lb[5:22, :] if lb.shape[0] > 22 else lb
colsum = lab.sum(axis=0)
groups = []
cur = None
for i, c in enumerate(colsum):
    if c > 0:
        if cur is None:
            cur = [i, i]
        else:
            cur[1] = i
    else:
        if cur and cur[1] - cur[0] >= 1:
            groups.append((X0 + cur[0], X0 + cur[1]))
        cur = None
if cur:
    groups.append((X0 + cur[0], X0 + cur[1]))
print("x tick label groups (frame x):", groups)

# Left of the curve: y tick labels (x < 617?) check a strip inside box left edge
print("\n--- strip x 608..640 ---")
strip = box[:, 0:32]
ls = strip.sum(axis=2) < 450
cc = ls.sum(axis=0)
print("cols:", [(X0 + int(i), int(c)) for i, c in enumerate(cc) if c > 3])
rr = ls.sum(axis=1)
print("rows:", [(Y0 + int(i), int(c)) for i, c in enumerate(rr) if c > 3][:40])
