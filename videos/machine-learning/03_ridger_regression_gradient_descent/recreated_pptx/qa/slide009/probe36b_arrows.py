#!/usr/bin/env python3
"""Probe 36b: residual-arrow census with probe4's exact red predicate
(r>90 & r-g>40 & r-b>10), axes excluded, plus ASCII art of the largest
components so arrow geometry (shaft + head) is unambiguous.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
RED = (r > 90) & ((r - g) > 40) & ((r - b) > 10)

# exclude stroked axes
RED2 = RED.copy()
RED2[:, 124:129] = False   # LEFT red y-axis cols 125..127 +/-1
RED2[:, 538:543] = False   # RIGHT red y-axis cols 539..541 +/-1
RED2[432:437, :] = False   # red x-axis rows 433..435 +/-1
# restrict to chart panel rows (above captions) to drop caption keyword ink
RED3 = RED2.copy()
RED3[480:, :] = False

lab, n = ndimage.label(RED3, structure=np.ones((3, 3)))
sizes = ndimage.sum(RED3, lab, range(1, n + 1))
objs = ndimage.find_objects(lab)
print(f"total red comps (panel rows only): {n}")
rows = []
for i, (sl, sz) in enumerate(zip(objs, sizes), 1):
    if sz < 8:
        continue
    y0, y1 = sl[0].start, sl[0].stop - 1
    x0, x1 = sl[1].start, sl[1].stop - 1
    side = "L" if x1 < 470 else ("R" if x0 > 480 else "?")
    rows.append((side, x0, x1, y0, y1, int(sz), i))
rows.sort(key=lambda t: (t[0], t[1]))
for side, x0, x1, y0, y1, sz, i in rows:
    print(f"  {side} comp{i:3d}: x {x0:4d}..{x1:4d} y {y0:4d}..{y1:4d} w={x1-x0+1:3d} h={y1-y0+1:3d} n={sz:5d}")

print("\n########## ASCII of the 4 largest comps ##########")
big = sorted(rows, key=lambda t: -t[5])[:4]
for side, x0, x1, y0, y1, sz, i in big:
    print(f"--- {side} comp{i}: x{x0}..{x1} y{y0}..{y1} n={sz}")
    sub = RED3[y0:y1+1, x0:x1+1]
    for rr in range(sub.shape[0]):
        print("    " + "".join("#" if v else "." for v in sub[rr]))
