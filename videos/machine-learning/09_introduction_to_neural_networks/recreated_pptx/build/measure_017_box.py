#!/usr/bin/env python3
"""Ink-profile the interior of the two bottom equation boxes on slide 017 original.

Determines: how many text lines, their x extents, and where a brace sits.
"""
import sys
import numpy as np
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "unique_slides/slide_017.jpg"
a = np.array(Image.open(SRC).convert("RGB")).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# tight peach mask
peach = (R > 240) & (G > 225) & (G < 242) & (B > 205) & (B < 226) & (R - G > 12)
# any ink that is not peach and not background-gray/white
gray = (np.abs(a - np.array([232, 232, 232])).sum(axis=2) < 26) | \
       (np.abs(a - np.array([255, 255, 255])).sum(axis=2) < 18) | \
       (np.abs(a - np.array([231, 233, 230])).sum(axis=2) < 14)
ink = ~peach & ~gray


def profile(name, x0, x1, y0, y1):
    print(f"\n===== {name}: x {x0}-{x1}, y {y0}-{y1} =====")
    m = ink[y0:y1 + 1, x0:x1 + 1]
    print(f"  total ink px: {m.sum()}")
    print("  --- row profile ---")
    for i, v in enumerate(m.sum(axis=1)):
        if v:
            xs = np.where(m[i])[0]
            print(f"   y={y0+i}: n={v:3d}  x {x0+xs.min()}-{x0+xs.max()}")
    print("  --- col profile (ink count per column, runs) ---")
    cc = m.sum(axis=0)
    runs, s = [], None
    for i, v in enumerate(cc):
        if v:
            if s is None:
                s = i
        else:
            if s is not None:
                runs.append((x0 + s, x0 + i - 1, int(cc[s:i].sum())))
                s = None
    if s is not None:
        runs.append((x0 + s, x0 + len(cc) - 1, int(cc[s:].sum())))
    for r in runs:
        print(f"    x {r[0]}-{r[1]} (w={r[1]-r[0]+1}) ink={r[2]}")


profile("LEFT equation box", 110, 420, 450, 515)
profile("RIGHT equation box", 488, 805, 450, 515)
