#!/usr/bin/env python3
"""Probe 28: locate the 'mm' labels (dark text) anywhere in the upper part of
each panel, OUTSIDE the annotation box, with the corrected white predicate.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-life"  # placeholder replaced below
SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = np.maximum(np.maximum(r, g), b)
mn = np.minimum(np.minimum(r, g), b)
SAT = mx - mn
WHT = (r > 244) & (g > 244) & (b > 243)
NOTW = ~WHT
# dark achromatic text ink
INK = NOTW & ((r + g + b) < 470) & (SAT <= 55)
RED = (r - g > 30) & (r - b > 30) & (r > 90)
BLU = (b - r > 40) & (b - g > 25) & (b > 110)
ORA = (r > 190) & (g > 120) & (b < 150) & (r - b > 60) & (r - g > 40)


def dump(nm, x0, x1, y0, y1):
    m = INK[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    print(f"\n===== {nm} x{x0}..{x1} y{y0}..{y1} =====")
    if not len(ys):
        print("  <no dark ink>")
        return
    print(f"  INK x {x0+xs.min()}..{x0+xs.max()} (w={xs.max()-xs.min()+1}) "
          f"y {y0+ys.min()}..{y0+ys.max()} (h={ys.max()-ys.min()+1})")
    X0, X1 = x0 + xs.min() - 1, x0 + xs.max() + 1
    Y0, Y1 = max(y0 + ys.min() - 1, 0), y0 + ys.max() + 1
    print("      " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(X0, X1 + 1)))
    for y in range(Y0, Y1 + 1):
        out = []
        for x in range(X0, X1 + 1):
            if INK[y, x]:
                out.append("#")
            elif RED[y, x]:
                out.append("R")
            elif BLU[y, x]:
                out.append("U")
            elif ORA[y, x]:
                out.append("O")
            elif NOTW[y, x]:
                out.append(":")
            else:
                out.append(" ")
        print(f"  {y:4d} " + "".join(out))


# LEFT: left of the annotation box (box starts x216), right of the y-axis (x128)
dump("LEFT area right of y-axis, x 130..214", 130, 214, 132, 180)
# RIGHT: right of the y-axis (x542), left of the annotation box (x632)
dump("RIGHT area x 543..631", 543, 631, 132, 180)
