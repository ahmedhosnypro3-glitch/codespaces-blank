#!/usr/bin/env python3
"""Column-profile measurement of slide 044's calc boxes (original frame).

For each of the 6 boxes (borders y139.5/197 | 206/263 | 272/329.5 | 338/395 |
404/461 | 470/528), print the x-clusters of ink per colour class (K black,
R red, G green, B blue) and the y-rows with ink, so band primitives can be
placed at measured positions.  Frame px, 1px=1pt.
"""
import sys
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = Image.open(f"{V}/unique_slides/slide_044.jpg").convert("RGB")
W, H = ORIG.size

def cls(p):
    r, g, b = p
    if r > 150 and g < 110 and b < 110:
        return "R"
    if g > 100 and g - r > 25 and g - b > 25:
        return "G"
    if b > 120 and b - r > 45 and b - g > 45:
        return "B"
    if r < 140 and g < 140 and b < 140:
        return "K"
    return None

BOXES = [(140, 197), (206, 263), (272, 329), (338, 395), (404, 461), (470, 528)]

def clusters(cols):
    out = []
    s = None
    for i in range(W):
        if cols[i] and s is None:
            s = i
        elif not cols[i] and s is not None:
            out.append((s, i - 1))
            s = None
    if s is not None:
        out.append((s, W - 1))
    return out

for bi, (y0, y1) in enumerate(BOXES, 1):
    print(f"=== BOX {bi}  y{y0}..{y1}")
    # y rows with any ink in x274..853
    rowink = []
    for y in range(y0, y1 + 1):
        n = sum(1 for x in range(274, 854) if cls(ORIG.getpixel((x, y))))
        if n:
            rowink.append((y, n))
    # compress rows into bands
    bands = []
    for y, n in rowink:
        if bands and y - bands[-1][1] <= 1:
            bands[-1] = (bands[-1][0], y, bands[-1][2] + n)
        else:
            bands.append((y, y, n))
    print("  y-bands:", [(a, b) for a, b, _ in bands])
    for c in ("K", "R", "G", "B"):
        cols = [False] * W
        for y in range(y0, y1 + 1):
            for x in range(274, 854):
                if cls(ORIG.getpixel((x, y))) == c:
                    cols[x] = True
        cl = clusters(cols)
        if cl:
            print(f"  {c} x-clusters: {cl}")
