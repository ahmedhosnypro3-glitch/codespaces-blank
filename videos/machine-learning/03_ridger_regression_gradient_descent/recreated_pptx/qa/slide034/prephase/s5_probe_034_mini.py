#!/usr/bin/env python3
"""S5 carrier mini-probe — last 034 details."""
from PIL import Image
import numpy as np

F = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_034.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)

def scanrow(y, x0, x1, label):
    print(f"--- {label} y={y} x{x0}..{x1}")
    prev = None
    for x in range(x0, x1):
        c = tuple(int(v) for v in im[y, x]); k = tuple(v // 20 * 20 for v in c)
        if k != prev: print("  x=", x, c); prev = k

def scancol(x, y0, y1, label):
    print(f"--- {label} x={x} y{y0}..{y1}")
    prev = None
    for y in range(y0, y1):
        c = tuple(int(v) for v in im[y, x]); k = tuple(v // 20 * 20 for v in c)
        if k != prev: print("  y=", y, c); prev = k

# 1. c15 yellow slope cell border (c15 = x707..747.5)
scanrow(468, 703, 752, "slope c15 row")
scancol(727, 456, 482, "slope c15 col")
# 2. insert text color: x-row text inside insert (y332..350, x670..788)
s = im[334:349, 670:788].reshape(-1, 3)
ink = s[s.max(axis=1) < 150]
print("insert x-row text ink: n=", len(ink), "median", np.median(ink, axis=0) if len(ink) else None)
s = im[352:367, 670:788].reshape(-1, 3)
ink = s[s.max(axis=1) < 150]
print("insert f-row text ink: n=", len(ink), "median", np.median(ink, axis=0) if len(ink) else None)
# 3. param cell x-extent at y256 (green row) and y290 (yellow row)
scanrow(258, 76, 100, "param green left edge")
scanrow(258, 155, 176, "param green right edge")
scanrow(292, 76, 100, "param yellow left edge")
# divider
scanrow(262, 120, 140, "param divider")
# 4. pink box border + text ink
s2 = im[266:308, 740:848]
mg = (s2[:, :, 0] > 130) & (s2[:, :, 2] > 100) & (s2[:, :, 1] < 100)
print("pink border-ish n=", int(mg.sum()), "median", np.median(s2[mg], axis=0) if mg.sum() else None)
s3 = im[274:302, 748:838].reshape(-1, 3)
ink = s3[(s3.max(axis=1) < 160)]
print("pink text ink n=", len(ink), "median", np.median(ink, axis=0) if len(ink) else None)
scanrow(281, 744, 842, "pink box mid-row")
scancol(760, 266, 306, "pink box col")
# 5. dashed guide
w = im[145:175, 775:795]
redm = (w[:, :, 0] > 130) & (w[:, :, 1] < 80) & (w[:, :, 2] < 80)
print("dashed guide red cols x775..795:", sorted(set((np.where(redm)[1] + 775).tolist())))
# 6. data text colors: x-row "7.2" (c2 = 179..219.5, text y~336..347), delta row (y~379..390)
s = im[335:348, 182:218].reshape(-1, 3)
ink = s[s.max(axis=1) < 140]
print("x-row text ink n=", len(ink), "median", np.median(ink, axis=0) if len(ink) else None)
s = im[378:391, 182:218].reshape(-1, 3)
ink = s[s.max(axis=1) < 140]
print("x-delta row text ink n=", len(ink), "median", np.median(ink, axis=0) if len(ink) else None)
s = im[422:435, 182:218].reshape(-1, 3)
ink = s[s.max(axis=1) < 140]
print("x+delta row text ink n=", len(ink), "median", np.median(ink, axis=0) if len(ink) else None)
s = im[488:500, 182:218].reshape(-1, 3)
ink = s[s.max(axis=1) < 140]
print("next-x text ink n=", len(ink), "median", np.median(ink, axis=0) if len(ink) else None)
# 7. label col text ink
s = im[335:348, 88:136].reshape(-1, 3)
ink = s[s.max(axis=1) < 140]
print("label col text ink n=", len(ink), "median", np.median(ink, axis=0) if len(ink) else None)
# 8. eq box: bar + numerator/denominator rows for mathtext sizing
scanrow(191, 500, 560, "eq fraction bar")
