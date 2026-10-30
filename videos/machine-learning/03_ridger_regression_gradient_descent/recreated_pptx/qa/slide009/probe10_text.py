#!/usr/bin/env python3
"""Probe 10: ASCII dumps of all text regions on slide_009.jpg so the glyph
layout is read directly from pixels (not inferred from spec prose).

Regions (frame px, 960x540, 1px = 1pt):
  LEFT equation box   x 88..475  y 100..190   (white fill, navy border)
  RIGHT equation box  x 478..880 y 100..190
  LEFT mm label       x 96..150  y 480..535
  RIGHT mm label      x 490..545 y 480..535
  LEFT captions       x 88..475  y 480..535
  RIGHT captions      x 478..880 y 480..535
Legend: ' ' white fill | '.' panel gray | 'R' red family | 'U' blue family |
        'O' orange | '#' dark ink / border
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def dump(name, x0, x1, y0, y1):
    print(f"\n===== {name} x{x0}..{x1} y{y0}..{y1} =====")
    print("      " + "".join(str((x // 100) % 10) if x % 10 == 0 else " " for x in range(x0, x1 + 1)))
    print("      " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x0, x1 + 1)))
    for y in range(y0, y1 + 1):
        row = []
        for x in range(x0, x1 + 1):
            R, G, B = r[y, x], g[y, x], b[y, x]
            if R > 245 and G > 245 and B > 245:
                row.append(" ")          # white fill
            elif abs(R - 233) < 14 and abs(G - 233) < 14 and abs(B - 231) < 16:
                row.append(".")          # panel gray
            elif R - G > 60 and R - B > 60:
                row.append("R")          # red family
            elif B - R > 60 and B - G > 30:
                row.append("U")          # blue family
            elif R > 200 and G > 150 and B < 130:
                row.append("O")          # orange
            else:
                row.append("#")          # dark ink / border
        print(f"  {y:4d} " + "".join(row))


# equation boxes: interior only (skip navy border cols 88..97 / 464..474)
dump("LEQ interior (navy border clipped)", 98, 464, 100, 190)
dump("REQ interior (navy border clipped)", 488, 868, 100, 190)
dump("LEFT mm label", 96, 150, 478, 535)
dump("RIGHT mm label", 490, 545, 478, 535)
dump("LEFT captions", 100, 470, 482, 532)
dump("RIGHT captions", 480, 875, 482, 532)
