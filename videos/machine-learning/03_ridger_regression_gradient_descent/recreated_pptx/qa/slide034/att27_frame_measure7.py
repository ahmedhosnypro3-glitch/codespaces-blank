#!/usr/bin/env python3
"""att27 frame measure 7 — red arrow ink map + callout line ink extents."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("unique_slides/slide_034.jpg").convert("RGB")).astype(int)
out = []
def w(s=""): out.append(s)

w("### 1. red arrow ink rows (x150..195, y298..345)")
for y in range(298, 346):
    r, g, b = im[y, 150:195, 0], im[y, 150:195, 1], im[y, 150:195, 2]
    red = (r > 110) & (r - g > 55) & (r - b > 55)
    xs = np.nonzero(red)[0]
    if len(xs):
        w(" y%d: x%d..%d n=%d" % (y, 150 + xs.min(), 150 + xs.max(), len(xs)))
w(" arrow sample colors: %s" % [(y, x, tuple(int(v) for v in im[y, x])) for y, x in ((306, 173), (315, 170), (330, 168), (335, 166))])

w("### 2. callout line1 ink (y255..275, x265..600)")
seg = im[255:276, 265:600]
m = seg.mean(axis=2)
cols = np.nonzero((m < 150).any(axis=0))[0]
if len(cols):
    w(" x extent: %d..%d" % (265 + cols.min(), 265 + cols.max()))
rows = np.nonzero((m < 150).any(axis=1))[0]
w(" y extent: %d..%d" % (255 + rows.min(), 255 + rows.max()))
# per-cluster columns
xs = cols
cl, cur = [], [xs[0]]
for x in xs[1:]:
    if x - cur[-1] <= 6: cur.append(x)
    else: cl.append(cur); cur = [x]
cl.append(cur)
w(" clusters: %s" % [(265 + c[0], 265 + c[-1]) for c in cl])
w("### 3. callout line2 ink (y276..302, x265..600)")
seg = im[276:303, 265:600]
m = seg.mean(axis=2)
cols = np.nonzero((m < 150).any(axis=0))[0]
if len(cols):
    w(" x extent: %d..%d" % (265 + cols.min(), 265 + cols.max()))
rows = np.nonzero((m < 150).any(axis=1))[0]
w(" y extent: %d..%d" % (276 + rows.min(), 276 + rows.max()))
xs = cols
cl, cur = [], [xs[0]]
for x in xs[1:]:
    if x - cur[-1] <= 6: cur.append(x)
    else: cl.append(cur); cur = [x]
cl.append(cur)
w(" clusters: %s" % [(265 + c[0], 265 + c[-1]) for c in cl])
w(" line2 ink colors (f(x) region x273..293): %s" % [(x, tuple(int(v) for v in im[287, x])) for x in range(274, 294, 3)])

txt = "\n".join(out)
with open("recreated_pptx/qa/slide034/att27_frame_measure7.txt", "w") as f:
    f.write(txt + "\n")
print(txt)
