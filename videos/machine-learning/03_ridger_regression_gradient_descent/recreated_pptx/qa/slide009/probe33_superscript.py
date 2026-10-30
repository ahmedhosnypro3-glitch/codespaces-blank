#!/usr/bin/env python3
"""Probe 33: the inter-glyph gap x256..276 in both equation boxes, with a LOOSE
predicate (anything darker than the E0F0FF box fill) to catch a faint
superscript or thin separator that the dark mask missed.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)

def gap(name, x0, x1, y0, y1):
    w = a[y0:y1+1, x0:x1+1]
    r, g, b = w[:, :, 0], w[:, :, 1], w[:, :, 2]
    # box fill measures around (224,240,255) -> total 719. anything < 690 is ink-ish
    ink = (r + g + b) <= 690
    print(f"=== {name}  x{x0}..{x1} y{y0}..{y1} (loose) ===")
    hdr = "     "
    for xx in range(x0, x1+1):
        hdr += str((xx // 10) % 10) if xx % 10 == 0 else " "
    print(hdr)
    for i, yy in enumerate(range(y0, y1+1)):
        chars = []
        for j in range(x1-x0+1):
            t = r[i, j] + g[i, j] + b[i, j]
            chars.append("#" if t <= 690 else ("+" if t <= 730 else "."))
        print(f"{yy:4d} " + "".join(chars))

gap("LEFT gap+eq", 256, 276, 148, 168)
gap("RIGHT gap+eq", 660, 690, 148, 168)

# also: faint ink anywhere in the full equation boxes (loose)
for nm, x0, x1, y0, y1 in [("LEFT full", 218, 315, 148, 173), ("RIGHT full", 637, 730, 152, 170)]:
    w = a[y0:y1+1, x0:x1+1]
    r, g, b = w[:, :, 0], w[:, :, 1], w[:, :, 2]
    ink = (r + g + b) <= 690
    ys, xs = np.nonzero(ink)
    print(f"[{nm}] loose ink x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(xs)}")
