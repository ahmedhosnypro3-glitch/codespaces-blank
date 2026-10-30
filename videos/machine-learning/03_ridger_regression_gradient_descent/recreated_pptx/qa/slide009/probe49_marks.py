#!/usr/bin/env python3
"""Probe 49: morphologically-closed solid-red census (JPEG-hole tolerant)."""
import numpy as np
from PIL import Image
from scipy import ndimage

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
# Broad red (catches JPEG-bleached cores of C00000-family ink)
RED = (r > 90) & ((r - g) > 45) & ((r - b) > 45)
ORANGE = (r > 180) & (g > 70) & (g < 175) & (b < 90) & ((r - g) > 60)
print("NOTE: broad-red also catches orange; used only to locate SHAPE then verified.")

close = ndimage.binary_closing(RED, structure=np.ones((7, 7)))
close = ndimage.binary_fill_holes(close)

for nm, x0, x1 in (("LEFT", 94, 466), ("RIGHT", 485, 871)):
    m = np.zeros_like(close)
    m[107:475, x0:x1] = close[107:475, x0:x1]
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    print(f"\n=== {nm} closed-red components (n>=40) ===")
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    objs = ndimage.find_objects(lab)
    for i, (sl, sz) in enumerate(zip(objs, sizes), 1):
        if sz < 40:
            continue
        y0, y1 = sl[0].start, sl[0].stop - 1
        xx0, xx1 = sl[1].start, sl[1].stop - 1
        # is this component mostly ORANGE (i.e. a data point)?
        om = ORANGE[y0:y1 + 1, xx0:xx1 + 1]
        rm = RED[y0:y1 + 1, xx0:xx1 + 1]
        print(f"  comp{i}: x {xx0}..{xx1} (w={xx1-xx0+1}) y {y0}..{y1} (h={y1-y0+1}) "
              f"n={int(sz)} orange_px={int(om.sum())} red_px={int(rm.sum())} "
              f"-> {'ORANGE-POINT' if om.sum() > rm.sum() else 'RED-MARK'}")

print("\n=== TRUE red core colour of each non-orange RED-MARK ===")
lab, n = ndimage.label(close, structure=np.ones((3, 3)))
for i, sl in enumerate(ndimage.find_objects(lab), 1):
    y0, y1 = sl[0].start, sl[0].stop - 1
    xx0, xx1 = sl[1].start, sl[1].stop - 1
    if not (94 < xx0 and xx1 < 900 and 107 < y0 and y1 < 475):
        continue
    om = ORANGE[y0:y1 + 1, xx0:xx1 + 1]
    rm = RED[y0:y1 + 1, xx0:xx1 + 1]
    if om.sum() > rm.sum():
        continue
    sub = a[y0:y1 + 1, xx0:xx1 + 1]
    sel = sub[rm]
    if len(sel):
        print(f"  x{xx0}..{xx1} y{y0}..{y1}: mean RGB = {sel.mean(axis=0).round(1)} n={len(sel)}")
