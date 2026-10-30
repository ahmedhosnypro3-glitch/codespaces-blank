#!/usr/bin/env python3
"""Determine slide_034's plot: curve color, axis lines/ticks, callout box, arrows."""
import numpy as np
from PIL import Image

ROOT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
im = np.asarray(Image.open(ROOT + "/unique_slides/slide_034.jpg").convert("RGB")).astype(int)

# We now know the plot frame is x607..847, y59..313 (red border).
X0, X1, Y0, Y1 = 608, 847, 60, 313
box = im[Y0:Y1, X0:X1]
r, g, b = box[:, :, 0], box[:, :, 1], box[:, :, 2]

# Tight cyan curve mask (curve mean rgb ~ (137,206,209) — desaturated cyan)
cyan = (b - r > 55) & (g - r > 30) & (b > 140)
ys, xs = np.where(cyan)
print("curve px:", len(xs), "bbox x %d..%d y %d..%d"
      % (X0+xs.min(), X0+xs.max(), Y0+ys.min(), Y0+ys.max()))
if len(xs):
    print("curve mean rgb:", box[cyan].mean(axis=0).round(1))

# Per-column topmost/bottommost curve pixel -> rough curve y-profile
for cx in [640, 660, 700, 740, 760, 780, 800, 820, 835]:
    col = np.where(cyan[:, cx - X0])[0]
    if len(col):
        print("x=%d: curve y %d..%d center %.0f" % (cx, Y0+col.min(), Y0+col.max(), Y0+col.mean()))

# axis ticks: look for dark short vertical lines inside the box (left spine?)
dark = (r + g + b) < 300
colcnt = dark.sum(axis=0)
print("vertical dark cols (rel):", [(X0+int(i), int(c)) for i, c in enumerate(colcnt) if c > 100])
rowcnt = dark.sum(axis=1)
print("horizontal dark rows (rel):", [(Y0+int(i), int(c)) for i, c in enumerate(rowcnt) if c > 150])

# red markers on the curve
redm = (r > 150) & (r - g > 60) & (r - b > 60)
ys2, xs2 = np.where(redm)
print("red-ish px in box:", len(xs2), end=" ")
if len(xs2):
    print("bbox x %d..%d y %d..%d" % (X0+xs2.min(), X0+xs2.max(), Y0+ys2.min(), Y0+ys2.max()))
    # cluster markers
    from scipy import ndimage
    lbl, n = ndimage.label(redm)
    sizes = ndimage.sum(redm, lbl, range(1, n+1))
    big = [i+1 for i, s in enumerate(sizes) if s >= 6]
    cents = ndimage.center_of_mass(redm, lbl, big)
    print("marker clusters (n=%d):" % len(big),
          [(X0+int(c[1]), Y0+int(c[0])) for c in cents])

# orange arrow region detail
orange = (r > 200) & (g > 100) & (g < 190) & (b < 90)
ys3, xs3 = np.where(orange)
if len(xs3):
    print("orange bbox x %d..%d y %d..%d" % (X0+xs3.min(), X0+xs3.max(), Y0+ys3.min(), Y0+ys3.max()))

# pink callout: find the pink FILL box (not text). Look for broad pink band rows.
pink = (r > 210) & (g > 150) & (g < 215) & (b > 180) & (b - g > 30)
ys4, xs4 = np.where(pink)
if len(xs4):
    print("pink-fill bbox x %d..%d y %d..%d (n=%d)"
          % (X0+xs4.min(), X0+xs4.max(), Y0+ys4.min(), Y0+ys4.max(), len(xs4)))
    rowcnt = pink.sum(axis=1)
    print("pink rows >60px wide (rel):", [(Y0+int(i), int(c)) for i, c in enumerate(rowcnt) if c > 60])
