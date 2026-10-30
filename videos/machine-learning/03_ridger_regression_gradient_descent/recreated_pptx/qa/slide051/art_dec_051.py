#!/usr/bin/env python3
"""Zoomed ASCII art of the original DEC row 1 regions (frame px, 1 char per px)."""
import sys
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_051.jpg"

img = Image.open(ORIG).convert("RGB")
px = img.load()


def cls(r, g, b):
    mx, mn = max(r, g, b), min(r, g, b)
    if b > r + 40 and b > g + 40:
        return "B"
    if g > r + 25 and g > b + 25:
        return "G"
    if r > g + 50 and r > b + 50:
        return "R"
    return "#"


def art(x0, x1, y0, y1, title):
    print("\n### %s  (x%d..%d y%d..%d)" % (title, x0, x1 - 1, y0, y1 - 1))
    print("     " + "".join(str((x // 10) % 10) for x in range(x0, x1)))
    print("     " + "".join(str(x % 10) for x in range(x0, x1)))
    for y in range(y0, y1):
        row = []
        for x in range(x0, x1):
            r, g, b = px[x, y]
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            row.append("." if lum >= 200 else cls(r, g, b))
        print("%3d  %s" % (y, "".join(row)))


art(278, 330, 156, 180, "d(Z1) label + '=' region")
art(330, 412, 144, 196, "blue (0 0) + green vector")
art(408, 440, 158, 176, "'= 5' region")
art(490, 600, 158, 176, "arrow + condition")
art(645, 700, 158, 176, "class tag")
