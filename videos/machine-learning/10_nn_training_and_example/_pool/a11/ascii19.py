#!/usr/bin/env python3
"""ASCII map of the slide-019 diagram band (a11). 1 char = 0.05in."""
import sys
import numpy as np
from PIL import Image

img = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(img).astype(int)
H, W, _ = a.shape
sc = W / 13.333
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
istam = (r > 168) & (g > 150) & (b < r) & ((r - b) < 100)
iswh = (r > 226) & (g > 226) & (b > 216)
ink = ~(istam | iswh)

STEP = 0.05
X0, X1 = float(sys.argv[2]), float(sys.argv[3])
Y0, Y1 = float(sys.argv[4]), float(sys.argv[5])


def cls(r_, g_, b_):
    if r_ > 200 and g_ > 200 and b_ > 200:
        return "."
    if r_ > 140 and g_ > 140 and b_ > 140:
        return "."
    if b_ > 140 and r_ < 130 and g_ < 160:
        return "D"   # dark blue (Net_k rects)
    mx, mn = max(r_, g_, b_), min(r_, g_, b_)
    if r_ > 170 and g_ < 105 and b_ < 110:
        return "R"
    if mx - mn > 55 and r_ > 150 and g_ > 90 and b_ < 110:
        return "O"
    if g_ > 150 and r_ < 160 and b_ < 140:
        return "G"
    if b_ > 150 and r_ < 170:
        return "B"
    if r_ > 150 and b_ > 150 and g_ < 140:
        return "M"
    if mx - mn > 45:
        return "*"
    if r_ < 110 and g_ < 110 and b_ < 110:
        return "#"
    return "-"


print(f"== {sys.argv[1]} x {X0}..{X1}in y {Y0}..{Y1}in  (col={STEP}in)")
ny = int((Y1 - Y0) / STEP)
nx = int((X1 - X0) / STEP)
print("RULER (| marks every 0.25in):")
ruler = []
for i in range(nx):
    xin = X0 + i * STEP
    if i % 5 == 0:
        ruler.append("|" if (round(xin * 4) % 2 == 0) else ":")
    else:
        ruler.append(" ")
print("      " + "".join(ruler))
for j in range(ny):
    yin = Y0 + j * STEP
    y = min(H - 1, int(yin * sc))
    line = []
    for i in range(nx):
        xin = X0 + i * STEP
        x = min(W - 1, int(xin * sc))
        if not ink[y, x]:
            line.append(" ")
        else:
            line.append(cls(r[y, x], g[y, x], b[y, x]))
    print(f"{yin:5.2f}|" + "".join(line) + "|")
print("      " + "".join(str(int((X0 + i * STEP) % 10)) for i in range(nx)))
