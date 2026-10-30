#!/usr/bin/env python3
"""Measure the two vector boxes and the two term boxes precisely: their exact
top/left/right/bottom borders (where the border stroke sits), the gutter between
the left and right column, and whether the ORIGINAL boxes touch the red strokes.
"""
import numpy as np
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{DECK}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide014/render_2.png").convert("RGB")).astype(int)
SC = r.shape[0] / 540.0


def box_borders(im, y0, y1, x0, x1, scale, label):
    # find dark ink rows/cols within the search window (borders are black 1pt)
    sub = im[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)]
    ink = (sub.sum(axis=2) < 200)   # near-black/very dark
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    # a border row has MANY ink px (a horizontal line spanning the box)
    strong_rows = [int(i) for i in rows if ink[i].sum() > 0.7 * (x1 - x0) * scale]
    strong_cols = [int(i) for i in cols if ink[:, i].sum() > 0.7 * (y1 - y0) * scale]
    print(f"  {label}:")
    if strong_rows:
        print(f"    horizontal border rows frame-y: {[round(y0 + v/scale,1) for v in strong_rows]}")
    else:
        print("    horizontal border rows: NONE spanning")
    if strong_cols:
        print(f"    vertical border cols frame-x: {[round(x0 + v/scale,1) for v in strong_cols]}")
    else:
        print("    vertical border cols: NONE spanning")
    if len(strong_rows) >= 2 and len(strong_cols) >= 2:
        print(f"    => box: x {x0+strong_cols[0]/scale:.1f}..{x0+strong_cols[-1]/scale:.1f}  "
              f"y {y0+strong_rows[0]/scale:.1f}..{y0+strong_rows[-1]/scale:.1f}")
        print(f"    => box width {(strong_cols[-1]-strong_cols[0])/scale:.1f}  height {(strong_rows[-1]-strong_rows[0])/scale:.1f}")


print("=== VECTOR BOXES (upper, white with black border) ===")
print("ORIGINAL:")
box_borders(o, 100, 240, 40, 460, 1.0, "left box (search x40..460)")
box_borders(o, 100, 240, 460, 910, 1.0, "right box (search x460..910)")
print("RENDER:")
box_borders(r, 100, 240, 40, 460, SC, "left box")
box_borders(r, 100, 240, 460, 910, SC, "right box")

print()
print("=== TERM BOXES (lower, light blue, NO border in build) ===")
print("ORIGINAL — check for a border stroke around the blue region:")
box_borders(o, 465, 528, 40, 460, 1.0, "loss-term box (search x40..460)")
box_borders(o, 465, 528, 460, 910, 1.0, "reg-term box (search x460..910)")
print("RENDER:")
box_borders(r, 465, 528, 40, 460, SC, "loss-term box")
box_borders(r, 465, 528, 460, 910, SC, "reg-term box")

print()
print("=== COLUMN GUTTER: the gap between left and right column (both bands and boxes) ===")


def gutter_scan(im, y, scale, label):
    row = im[int((y + 0.5) * scale)]
    # classify: white/gray = outside box/band, colored = inside
    def cls(c):
        # colored fill detection: noticeably non-gray
        if abs(int(c[0])-int(c[1])) > 8 or abs(int(c[1])-int(c[2])) > 8:
            return "fill"
        return "plain"
    prev = None
    runs = []
    for i, c in enumerate(row):
        k = cls(c)
        if k != prev:
            runs.append([i, i, k])
            prev = k
        else:
            runs[-1][1] = i
    long_runs = [(a, b, k) for a, b, k in runs if (b - a) >= 5 * scale]
    s = "  ".join(f"{k}[{a/scale:.0f}-{b/scale:.0f}]" for a, b, k in long_runs)
    print(f"  {label} y={y}: {s}")


for y in (150, 380, 490, 515):
    gutter_scan(o, y, 1.0, "ORIG")
for y in (150, 380, 490, 515):
    gutter_scan(r, y, SC, "REND")
