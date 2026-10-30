#!/usr/bin/env python3
"""Probe 25: FINAL ASCII read of the equation text and the 'mm' labels using a
clean 'not white' predicate (the panel interior is pure white 254,254,255, so
anything else is content). Prints only the tight ink bbox with 1px pad.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

NOTW = ~((r > 250) & (g > 250) & (b > 250))
RED = (r - g > 30) & (r - b > 30) & (r > 90)
BLU = (b - r > 40) & (b - g > 25) & (b > 110)


def dump(nm, x0, x1, y0, y1, maxw=140):
    m = NOTW[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    print(f"\n===== {nm} x{x0}..{x1} y{y0}..{y1} =====")
    if not len(ys):
        print("  <no ink>")
        return
    print(f"  INK x {x0+xs.min()}..{x0+xs.max()} (w={xs.max()-xs.min()+1}) "
          f"y {y0+ys.min()}..{y0+ys.max()} (h={ys.max()-ys.min()+1})")
    X0, X1 = x0 + xs.min(), x0 + xs.max()
    Y0, Y1 = y0 + ys.min(), y0 + ys.max()
    step = 2 if (X1 - X0) > maxw else 1
    if step == 2:
        print(f"  (printing every 2nd column, {X1-X0+1} cols wide)")
    print("      " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(X0, X1 + 1, step)))
    for y in range(Y0, Y1 + 1):
        out = []
        for x in range(X0, X1 + 1, step):
            if RED[y, x]:
                out.append("R")
            elif BLU[y, x]:
                out.append("U")
            elif NOTW[y, x]:
                out.append("#")
            else:
                out.append(" ")
        print(f"  {y:4d} " + "".join(out))


# equation text + the arrowhead near it, inside the LEFT panel interior
dump("LEQ region '50.85^2 = 2585' + arrow", 165, 330, 135, 180)
dump("REQ region '63.64^2 = 4050' + arrow", 590, 745, 135, 180)
# 'mm' labels
dump("LMM '50.85 mm'", 165, 330, 135, 180)
dump("RMM '63.64 mm'", 590, 745, 135, 180)
