#!/usr/bin/env python3
"""PIL measurement of slide_007 original frame: structure, colors, geometry."""
import numpy as np
from PIL import Image
from collections import Counter

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"

im = Image.open(SRC).convert("RGB")
print("SIZE", im.size)
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

# --- dominant colors ---
cnt = Counter(map(tuple, a.reshape(-1, 3)))
print("\nTOP 18 COLORS:")
for c, n in cnt.most_common(18):
    print(f"  {c} #{c[0]:02X}{c[1]:02X}{c[2]:02X}  n={n} ({100*n/(H*W):.2f}%)")

# --- column/row profile of "non-white" ink (plot area is white panel) ---
def is_whiteish(px):
    return px[0] > 240 and px[1] > 240 and px[2] > 240

nonwhite = ~np.all(a > 240, axis=2)
print("\nNON-WHITE bbox (whole frame):")
ys, xs = np.where(nonwhite)
print("  x", xs.min(), xs.max(), " y", ys.min(), ys.max())

# find red-ish frame pixels
red = (a[:,:,0] > 120) & (a[:,:,0] - a[:,:,1] > 60) & (a[:,:,0] - a[:,:,2] > 60)
ys, xs = np.where(red)
print("\nRED-ISH bbox: x", xs.min(), xs.max(), " y", ys.min(), ys.max())

# --- title region: top 80px, look for blue text ---
blue = (a[:,:,2] > 110) & (a[:,:,2] - a[:,:,0] > 60) & (a[:,:,2] - a[:,:,1] > 60)
ys, xs = np.where(blue)
if len(xs):
    print("BLUE-ISH bbox: x", xs.min(), xs.max(), " y", ys.min(), ys.max())
    # blue connected row bands
    rows = sorted(set(ys.tolist()))
    bands = []
    s = rows[0]; p = rows[0]
    for r in rows[1:]:
        if r - p > 3:
            bands.append((s, p)); s = r
        p = r
    bands.append((s, p))
    print("  blue row bands:", bands)

# red row bands in title region y<120
m = red.copy(); m[120:, :] = False
ys2, xs2 = np.where(m)
if len(ys2):
    rows = sorted(set(ys2.tolist()))
    bands = []
    s = rows[0]; p = rows[0]
    for r in rows[1:]:
        if r - p > 3:
            bands.append((s, p)); s = r
        p = r
    bands.append((s, p))
    print("RED title row bands (y<120):", bands)
    for (b0, b1) in bands:
        sel = (ys2 >= b0) & (ys2 <= b1)
        print(f"    band y {b0}-{b1}: x {xs2[sel].min()}-{xs2[sel].max()}")

# yellow pixels (badge + C boxes)
yellow = (a[:,:,0] > 190) & (a[:,:,1] > 170) & (a[:,:,2] < 160) & (a[:,:,0] - a[:,:,2] > 60)
ys3, xs3 = np.where(yellow)
print("\nYELLOW bbox: x", xs3.min(), xs3.max(), " y", ys3.min(), ys3.max())
# cluster yellow into boxes via simple grid labeling
from scipy import ndimage
lab, n = ndimage.label(yellow)
print("  yellow components:", n)
for i in range(1, n+1):
    yy, xx = np.where(lab == i)
    if len(yy) < 30:
        continue
    print(f"    comp {i}: x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()} area={len(yy)}")
