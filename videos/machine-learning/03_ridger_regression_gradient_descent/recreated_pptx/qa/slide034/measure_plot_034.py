#!/usr/bin/env python3
"""PIL-measure slide_034's plot region: frame borders, curve color, axis layout."""
import numpy as np
from PIL import Image

ROOT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
im = np.asarray(Image.open(ROOT + "/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
print("frame", W, H)

# --- find the plot's red frame rectangle: scan the upper-right quadrant ---------
sub = im[40:330, 560:880]
r, g, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
red = (r > 110) & ((r - g) > 45) & ((r - b) > 45)
ys, xs = np.where(red)
if len(xs):
    print("red ink in plot area: x %d..%d  y %d..%d (frame coords)"
          % (560 + xs.min(), 560 + xs.max(), 40 + ys.min(), 40 + ys.max()))
    # column profile -> vertical border candidates
    colcnt = red.sum(axis=0)
    vcols = np.where(colcnt > 150)[0]
    print("strong vertical red cols (rel):", [560 + int(c) for c in vcols][:20])
    rowcnt = red.sum(axis=1)
    hrows = np.where(rowcnt > 200)[0]
    print("strong horizontal red rows (rel):", [40 + int(c) for c in hrows][:20])

# --- curve color: sample distinct saturated colors inside the plot box ---------
box = im[60:315, 610:845]
r2, g2, b2 = box[:, :, 0], box[:, :, 1], box[:, :, 2]
cyanish = (b2 > 120) & (b2 - r2 > 40) & (g2 > 100) & (b2 - r2 < 120)
print("cyan-ish px in plot box:", int(cyanish.sum()))
if cyanish.sum():
    yy, xx = np.where(cyanish)
    print("cyan mean rgb:", box[cyanish].mean(axis=0).round(1))
    print("cyan bbox: x %d..%d y %d..%d"
          % (610 + xx.min(), 610 + xx.max(), 60 + yy.min(), 60 + yy.max()))
blue = (b2 > 150) & (b2 - r2 > 60) & (g2 < 100)
print("pure-blue px in plot box:", int(blue.sum()))
orange = (r2 > 200) & (g2 > 100) & (g2 < 190) & (b2 < 90)
print("orange-ish px:", int(orange.sum()))
if orange.sum():
    yy, xx = np.where(orange)
    print("orange bbox: x %d..%d y %d..%d"
          % (610 + xx.min(), 610 + xx.max(), 60 + yy.min(), 60 + yy.max()))
pinkish = (r2 > 200) & (b2 > 150) & (g2 < 180)
print("pink-ish px:", int(pinkish.sum()))
if pinkish.sum():
    yy, xx = np.where(pinkish)
    print("pink bbox: x %d..%d y %d..%d"
          % (610 + xx.min(), 610 + xx.max(), 60 + yy.min(), 60 + yy.max()))

# --- horizontal scan through the plot box: find dark axis-like rows/cols -------
dark = (r2 + g2 + b2) < 260
rowcnt = dark.sum(axis=1)
print("dark rows (rel, count>200):", [(60 + int(i), int(c)) for i, c in enumerate(rowcnt) if c > 200][:20])

# --- magenta callout box location (scan whole slide) ---------------------------
r3, g3, b3 = im[:, :, 0], im[:, :, 1], im[:, :, 2]
mag = (r3 > 200) & (b3 > 160) & (g3 < 170) & (r3 - g3 > 60)
ys, xs = np.where(mag)
if len(xs):
    print("magenta-ish ink bbox: x %d..%d y %d..%d (n=%d)"
          % (xs.min(), xs.max(), ys.min(), ys.max(), len(xs)))
    # densest cluster
    from collections import Counter
    rows = Counter(ys // 8 * 8)
    print("magenta row histogram top:", rows.most_common(8))
    cols = Counter(xs // 8 * 8)
    print("magenta col histogram top:", cols.most_common(8))
