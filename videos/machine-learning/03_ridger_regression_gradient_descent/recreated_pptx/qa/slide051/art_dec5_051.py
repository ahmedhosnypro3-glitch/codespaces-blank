#!/usr/bin/env python3
"""Zoomed ASCII art of the blue augmented-vector text in all three DEC rows."""
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_051.jpg"
img = Image.open(ORIG).convert("RGB")
px = img.load()


def cls(r, g, b):
    if b > r + 40 and b > g + 40:
        return "B"
    if g > r + 25 and g > b + 25:
        return "G"
    if r > g + 50 and r > b + 50:
        return "R"
    return "#"


def art(x0, x1, y0, y1, title):
    print("\n### %s" % title)
    print("      " + "".join(str((x // 10) % 10) for x in range(x0, x1)))
    print("      " + "".join(str(x % 10) for x in range(x0, x1)))
    for y in range(y0, y1):
        row = []
        for x in range(x0, x1):
            r, g, b = px[x, y]
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            row.append("." if lum >= 200 else cls(r, g, b))
        print("%4d  %s" % (y, "".join(row)))


art(332, 382, 146, 160, "row1 blue  x332..381")
art(332, 382, 215, 230, "row2 blue  x332..381")
art(332, 382, 281, 296, "row3 blue  x332..381")
