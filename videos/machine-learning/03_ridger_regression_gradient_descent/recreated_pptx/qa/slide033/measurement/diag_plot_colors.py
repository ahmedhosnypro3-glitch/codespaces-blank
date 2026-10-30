#!/usr/bin/env python3
"""Diagnose the ORIGINAL plot region colors precisely."""
import numpy as np
from PIL import Image
from collections import Counter

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)

# Plot region frame px
X0, Y0, X1, Y1 = 615, 120, 930, 330
sub = o[Y0:Y1, X0:X1].reshape(-1, 3)
cnt = Counter(map(tuple, sub))
print("Top 30 colors in ORIGINAL plot region (615-930, 120-330):")
for c, n in cnt.most_common(30):
    print(f"  {c}  x{n}")

print(f"\ntotal px: {len(sub)}, distinct colors: {len(cnt)}")

# Now find pixels that are "greenish": g is max channel
r, g, b = sub[:, 0], sub[:, 1], sub[:, 2]
greenish = (g >= r) & (g >= b) & (g > 60) & ((g - r) + (g - b) > 20)
print(f"\ngreenish px: {greenish.sum()}")
if greenish.sum():
    gs = sub[greenish]
    ys = np.where(greenish)[0] // (X1 - X0) + Y0
    xs = np.where(greenish)[0] % (X1 - X0) + X0
    print(f"  extent rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")
    print("  top colors:", Counter(map(tuple, gs)).most_common(8))

# Pixels where B is max (blue/purple)
bluish = (b >= r) & (b >= g) & (b > 60) & ((b - r) + (b - g) > 25)
print(f"\nbluish px: {bluish.sum()}")
if bluish.sum():
    bs = sub[bluish]
    ys = np.where(bluish)[0] // (X1 - X0) + Y0
    xs = np.where(bluish)[0] % (X1 - X0) + X0
    print(f"  extent rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")
    print("  top colors:", Counter(map(tuple, bs)).most_common(8))

# Pixels where R is max (red/orange)
reddish = (r >= g) & (r >= b) & (r > 100) & ((r - g) + (r - b) > 40)
print(f"\nreddish px: {reddish.sum()}")
if reddish.sum():
    rs = sub[reddish]
    ys = np.where(reddish)[0] // (X1 - X0) + Y0
    xs = np.where(reddish)[0] % (X1 - X0) + X0
    print(f"  extent rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")
    print("  top colors:", Counter(map(tuple, rs)).most_common(8))

# Row-by-row colour summary of the plot region (which colours appear per row band)
print("\nRow-band colour census (10px bands):")
for y in range(Y0, Y1, 10):
    band = o[y:y + 10, X0:X1].reshape(-1, 3)
    cnt2 = Counter(map(tuple, band))
    top = cnt2.most_common(3)
    nonwhite = sum(n for c, n in cnt2.items() if sum(c) < 720)
    print(f"  rows {y:>3}-{y+9:>3}: nonwhite={nonwhite:>5}  top={top}")
