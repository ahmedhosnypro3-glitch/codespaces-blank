#!/usr/bin/env python3
"""Measure the original's box/band extents by boundary detection (white box on
gray panel; blue box on gray panel), column-scanning in a text-free column and
row-scanning in a text-free row. Same measurement for the render.
"""
import numpy as np
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{DECK}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide014/render_2.png").convert("RGB")).astype(int)
SC = r.shape[0] / 540.0
GRAY = (233, 233, 232)


def col_scan(im, x, y0, y1, scale, kind, label):
    """Walk down column x; report y-runs where the pixel is NOT panel-gray."""
    ys = []
    for y in range(int(y0 * scale), int(y1 * scale)):
        c = im[y, int(x * scale)]
        isgray = abs(int(c[0]) - GRAY[0]) <= 6 and abs(int(c[1]) - GRAY[1]) <= 6 and abs(int(c[2]) - GRAY[2]) <= 6
        iswhite = int(c[0]) >= 250 and int(c[1]) >= 250 and int(c[2]) >= 250
        isblue = int(c[2]) - int(c[0]) > 6 and int(c[1]) > int(c[0])
        if kind == "white" and not iswhite:
            ys.append(y)
        elif kind == "blue" and isblue:
            ys.append(y)
    if len(ys) < 4 * scale:
        print(f"  {label}: col x={x} -> no {kind} region")
        return
    # group contiguous
    groups = []
    st = ys[0]
    prev = ys[0]
    for v in ys[1:]:
        if v - prev > 3 * scale:
            groups.append((st, prev))
            st = v
        prev = v
    groups.append((st, prev))
    real = [(a, b) for a, b in groups if (b - a) > 3 * scale]
    print(f"  {label}: col x={x} -> " + ", ".join(
        f"y {a/scale:.0f}..{b/scale:.0f} (h {(b-a)/scale:.0f})" for a, b in real))


def row_scan(im, y, x0, x1, scale, kind, label):
    xs = []
    for x in range(int(x0 * scale), int(x1 * scale)):
        c = im[int(y * scale), x]
        isgray = abs(int(c[0]) - GRAY[0]) <= 6 and abs(int(c[1]) - GRAY[1]) <= 6 and abs(int(c[2]) - GRAY[2]) <= 6
        iswhite = int(c[0]) >= 250 and int(c[1]) >= 250 and int(c[2]) >= 250
        isblue = int(c[2]) - int(c[0]) > 6 and int(c[1]) > int(c[0])
        if kind == "white" and not iswhite:
            xs.append(x)
        elif kind == "blue" and isblue:
            xs.append(x)
        elif kind == "notgray" and not isgray:
            xs.append(x)
    if len(xs) < 4 * scale:
        print(f"  {label}: row y={y} -> no {kind} region")
        return
    groups = []
    st = xs[0]
    prev = xs[0]
    for v in xs[1:]:
        if v - prev > 3 * scale:
            groups.append((st, prev))
            st = v
        prev = v
    groups.append((st, prev))
    real = [(a, b) for a, b in groups if (b - a) > 3 * scale]
    print(f"  {label}: row y={y} -> " + ", ".join(
        f"x {a/scale:.0f}..{b/scale:.0f} (w {(b-a)/scale:.0f})" for a, b in real))


print("=== ORIGINAL: white boxes (vector boxes) — column scan at x=70 (text-free left strip) ===")
col_scan(o, 70, 90, 250, 1.0, "white", "ORIG left vector box")
col_scan(o, 520, 90, 250, 1.0, "white", "ORIG right vector box")
print("=== RENDER: same column ===")
col_scan(r, 70, 90, 250, SC, "white", "REND left vector box")
col_scan(r, 520, 90, 250, SC, "white", "REND right vector box")

print()
print("=== ORIGINAL: blue boxes (term boxes + final band) — column scan at x=100 and x=560 ===")
col_scan(o, 100, 440, 540, 1.0, "blue", "ORIG x=100")
col_scan(o, 560, 440, 540, 1.0, "blue", "ORIG x=560")
print("=== RENDER: ===")
col_scan(r, 100, 440, 540, SC, "blue", "REND x=100")
col_scan(r, 560, 440, 540, SC, "blue", "REND x=560")

print()
print("=== ORIGINAL: blue region horizontal extent at text-free rows ===")
row_scan(o, 512, 40, 910, 1.0, "blue", "ORIG y=512")
row_scan(o, 518, 40, 910, 1.0, "blue", "ORIG y=518")
row_scan(o, 483, 40, 910, 1.0, "blue", "ORIG y=483")
print("=== RENDER: ===")
row_scan(r, 512, 40, 910, SC, "blue", "REND y=512")
row_scan(r, 518, 40, 910, SC, "blue", "REND y=518")
row_scan(r, 483, 40, 910, SC, "blue", "REND y=483")

print()
print("=== ORIGINAL: white vector box horizontal extent (row inside box, text-free left margin x70..200?) ===")
row_scan(o, 115, 40, 460, 1.0, "notgray", "ORIG y=115 left col")
row_scan(o, 115, 460, 910, 1.0, "notgray", "ORIG y=115 right col")
print("=== RENDER: ===")
row_scan(r, 115, 40, 460, SC, "notgray", "REND y=115 left col")
row_scan(r, 115, 460, 910, SC, "notgray", "REND y=115 right col")

print()
print("=== MIDDLE BANDS (the two the render is missing) ===")
print("ORIGINAL: not-gray scan at rows between the objective band and the define-loss band")
for y in (352, 370, 388, 405, 425, 438):
    row_scan(o, y, 40, 910, 1.0, "notgray", f"ORIG y={y}")
print("RENDER: same rows")
for y in (352, 370, 388, 405, 425, 438):
    row_scan(r, y, 40, 910, SC, "notgray", f"REND y={y}")
