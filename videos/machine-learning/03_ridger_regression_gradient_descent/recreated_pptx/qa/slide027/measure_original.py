#!/usr/bin/env python3
"""Exploratory PIL measurement of unique_slides/slide_027.jpg (960x540, 1px = 1pt).
Finds: title band, graph box (red border), black ink (axes/curve/text), blue dots,
yellow dot, dashed line, and prints bboxes + profiles for geometry derivation."""
import numpy as np
from PIL import Image

FRAME = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_027.jpg"
im = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
print(f"frame {W}x{H}")

# color masks
dark_red_title = (r > 80) & (r < 190) & (g < 90) & (b < 90)          # 8B0000-ish title
bright_red = (r > 150) & (g < 110) & (b < 110)                        # FF0000/C00000-ish box border
black_ink = (r < 90) & (g < 90) & (b < 90)                           # curve, axes, text
blue = (b > 100) & (r < 100) & (g < 100)                            # 0000CD dots
yellow = (r > 200) & (g > 200) & (b < 160)                           # FFFF00 dot/badge

for name, mask in [("dark_red_title", dark_red_title), ("bright_red", bright_red),
                   ("black_ink", black_ink), ("blue", blue), ("yellow", yellow)]:
    n = int(mask.sum())
    print(f"\n== {name}: {n} px")
    if not n:
        continue
    ys, xs = np.where(mask)
    print(f"   bbox x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}")
    # row profile bands (row -> count) condensed into runs
    rows = np.where(mask.sum(axis=1) > 0)[0]
    if len(rows):
        runs = []
        s = p = rows[0]
        for y in rows[1:]:
            if y == p + 1:
                p = y
            else:
                runs.append((s, p)); s = p = y
        runs.append((s, p))
        print(f"   row bands: {runs[:40]}")
    cols = np.where(mask.sum(axis=0) > 0)[0]
    if len(cols):
        runs = []
        s = p = cols[0]
        for x in cols[1:]:
            if x == p + 1:
                p = x
            else:
                runs.append((s, p)); s = p = x
        runs.append((s, p))
        print(f"   col bands: {runs[:40]}")

# distinct color census over non-gray pixels
flat = im.reshape(-1, 3)
grayish = (abs(flat[:, 0] - flat[:, 1]) < 12) & (abs(flat[:, 1] - flat[:, 2]) < 14) & (flat[:, 0] > 150)
nongray = flat[~grayish]
from collections import Counter
cnt = Counter(map(tuple, nongray.tolist()))
print("\n== top 25 non-gray-ish colors:")
for c, n in cnt.most_common(25):
    print(f"   {c}: {n}")
