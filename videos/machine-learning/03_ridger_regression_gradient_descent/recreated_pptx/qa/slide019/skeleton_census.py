#!/usr/bin/env python3
"""Master skeleton census of the original: every colored rule by class.

Verticals: per-x per-class row counts (y165..530).  Horizontals: per-y per-class
column counts (x54..903) with x-extent.  Prints runs of >=100 px, merged with
color labels, so the table structure can be transcribed exactly.
"""
import numpy as np
from PIL import Image

VID = "videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{VID}/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]
mx = np.max(o, axis=2); mn = np.min(o, axis=2); sat = mx - mn
CLASSES = {
    "B": (b > 150) & (r < 130) & (g < 130),                      # blue
    "R": (r > 150) & (g < 110) & (b < 110),                      # red
    "G": (g > 110) & (r < 130) & (b < 130),                      # green
    "K": mx < 95,                                                # black
    "Y": (r > 170) & (g > 170) & (b < 150) & (sat > 40),         # yellow
    "g": (b > r + 8) & (b > g + 8) & (sat > 15) & (mx < 230),    # bluish gray
    "w": (mx > 235) & (sat < 20),                                # white-ish
}
Y0, Y1, X0, X1 = 165, 531, 54, 904
sub = {k: m[Y0:Y1, X0:X1] for k, m in CLASSES.items()}

print("=== VERTICAL RULES (class runs with >=100 rows) ===")
for x in range(X1 - X0):
    runs = []
    for k, m in sub.items():
        c = m[:, x].sum()
        if c >= 100:
            runs.append((k, int(c)))
    if runs:
        print(f"  x{X0+x:3d}: " + "  ".join(f"{k}={c}" for k, c in runs))

print("\n=== HORIZONTAL RULES (class runs with >=100 cols, with x-extent) ===")
for y in range(Y1 - Y0):
    runs = []
    for k, m in sub.items():
        cnt = m[y]
        if cnt.sum() >= 100:
            xs = np.where(cnt)[0]
            runs.append((k, int(cnt.sum()), X0 + xs.min(), X0 + xs.max()))
    if runs:
        print(f"  y{Y0+y:3d}: " + "  ".join(f"{k} n={n} x{a}..{c}" for k, n, a, c in runs))
