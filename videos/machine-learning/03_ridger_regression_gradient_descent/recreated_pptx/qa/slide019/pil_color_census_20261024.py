#!/usr/bin/env python3
"""Colour of the ink in each text role of the ORIGINAL: W values, y values, x values."""
import numpy as np
from PIL import Image

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"
A = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)

# Text-line bands (frame px) from the census:
#   header      y181..197
#   TestN line  y210..218 (g1) / y318..326 (g2) / y426..435 (g3)
#   W line      y231..240 (g1) / y339..355 (g2) / y448..457 (g3)
#   y line      y~258..266 (g1) / y~365..373 (g2) / y~474..482 (g3)
REGIONS = [
    ("header",        181, 198, 124, 900),
    ("NOREG g1 Test", 208, 220, 206, 377),
    ("NOREG g1 W",    229, 242, 124, 206),
    ("NOREG g1 y",    256, 268, 206, 377),
    ("NOREG g2 W",    337, 356, 124, 206),
    ("NOREG g2 y",    363, 376, 206, 377),
    ("NOREG g3 W",    446, 458, 124, 206),
    ("NOREG g3 y",    472, 484, 206, 377),
    ("R3 g1 W",       229, 242, 384, 466),
    ("R3 g1 y",       256, 268, 466, 638),
    ("R3 g2 y",       363, 376, 466, 638),
    ("R3 g3 y",       472, 484, 466, 638),
    ("R10 g1 y",      256, 268, 726, 893),
    ("R10 g2 y",      363, 376, 726, 893),
    ("R10 g3 y",      472, 484, 726, 893),
    ("outlier g1",    198, 212, 66, 116),
    ("outlier g2",    325, 342, 66, 116),
    ("outlier g3",    428, 444, 66, 116),
    ("refline",        80, 100, 430, 896),
]

print(f"{'region':16s} {'n_ink':>6s}  mean RGB of ink (darkest 12% px)   classify")
for name, y0, y1, x0, x1 in REGIONS:
    reg = A[y0:y1, x0:x1]
    lum = reg.mean(axis=2)
    thr = np.percentile(lum, 12)
    m = lum <= max(thr, lum.min() + 12)
    if m.sum() < 8:
        print(f"{name:16s} {m.sum():6d}  (too few ink px)")
        continue
    px = reg[m]
    mr, mg, mb = px[:, 0].mean(), px[:, 1].mean(), px[:, 2].mean()
    # classify
    if mb - mr > 25 and mb > 90:
        cls = "BLUE"
    elif mr - mg > 45 and mr - mb > 45:
        cls = "RED"
    elif mg - mr > 25 and mg - mb > 10:
        cls = "GREEN"
    elif mr > 200 and mg > 200 and mb < 200:
        cls = "YELLOW-fill"
    else:
        cls = "BLACK/neutral"
    print(f"{name:16s} {m.sum():6d}  rgb({mr:5.1f},{mg:5.1f},{mb:5.1f})   {cls}")

# Also: whole-frame colour inventory of DARK text ink (lum<120) by hue class
print("\n=== whole-frame dark-ink (lum<120) colour inventory ===")
lum = A.mean(axis=2)
m = lum < 120
px = A[m]
print("  ink px:", m.sum())
r, g, b = px[:, 0], px[:, 1], px[:, 2]
blue = ((b - r > 25) & (b > 80)).sum()
red = ((r - g > 45) & (r - b > 45)).sum()
green = ((g - r > 20) & (g - b > 10)).sum()
print(f"  BLUE-ish {blue}  RED-ish {red}  GREEN-ish {green}  neutral {m.sum()-blue-red-green}")
