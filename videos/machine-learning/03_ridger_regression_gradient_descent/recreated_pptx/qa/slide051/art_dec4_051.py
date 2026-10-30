#!/usr/bin/env python3
"""Raw luminance / RGB dump for the arrow glyph and the d(Z1) label."""
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_051.jpg"
img = Image.open(ORIG).convert("RGB")
px = img.load()


def lumgrid(x0, x1, y0, y1, title):
    print("\n### %s  (luminance)" % title)
    print("      " + "".join(str((x // 10) % 10) for x in range(x0, x1)))
    print("      " + "".join(str(x % 10) for x in range(x0, x1)))
    for y in range(y0, y1):
        row = []
        for x in range(x0, x1):
            r, g, b = px[x, y]
            L = int(0.299 * r + 0.587 * g + 0.114 * b)
            row.append("%3d" % min(L, 999))
        print("%4d  %s" % (y, " ".join(row)))


def rgbgrid(x0, x1, y0, y1, title):
    print("\n### %s  (R,G,B)" % title)
    for y in range(y0, y1):
        parts = []
        for x in range(x0, x1):
            r, g, b = px[x, y]
            parts.append("%3d/%3d/%3d" % (r, g, b))
        print("%4d  %s" % (y, " ".join(parts)))


lumgrid(497, 513, 162, 173, "arrow dec1 luminance")
rgbgrid(281, 296, 161, 173, "d(Z1) 'd' glyph RGB")
rgbgrid(296, 314, 160, 173, "d(Z1) 'Z1)' RGB")
rgbgrid(333, 340, 148, 159, "blue paren RGB")
