#!/usr/bin/env python3
"""Exact ink x-lists per row for chosen windows of the original frame."""
import sys
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_051.jpg"
img = Image.open(ORIG).convert("RGB")
px = img.load()


def grid(x0, x1, y0, y1, title):
    print("\n### %s" % title)
    print("      " + "".join(str((x // 10) % 10) for x in range(x0, x1)))
    print("      " + "".join(str(x % 10) for x in range(x0, x1)))
    for y in range(y0, y1):
        row = []
        for x in range(x0, x1):
            r, g, b = px[x, y]
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            if lum >= 200:
                row.append(".")
            elif b > r + 40 and b > g + 40:
                row.append("B")
            elif g > r + 25 and g > b + 25:
                row.append("G")
            elif r > g + 50 and r > b + 50:
                row.append("R")
            else:
                row.append("#")
        print("%4d  %s" % (y, "".join(row)))


grid(496, 514, 160, 176, "arrow shape (dec1) x496..513")
grid(330, 412, 146, 160, "blue (0 0) + top of green vector")
grid(374, 410, 148, 192, "green vector interior/bars")
grid(280, 330, 158, 178, "d(Z1) + =")
grid(490, 530, 226, 246, "arrow shape (dec2)")
grid(490, 530, 292, 312, "arrow shape (dec3)")
