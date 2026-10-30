#!/usr/bin/env python3
"""Measure slide_001 original frame v2: frame rule, bg, text lines, colors, logo."""
import os
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = os.path.join(V, "unique_slides/slide_001.jpg")
OUT = os.path.join(V, "recreated_pptx/build/measure_001_v2.txt")

im = Image.open(ORIG).convert("RGB")
a = np.asarray(im).astype(np.int16)
H, W = a.shape[:2]
L = (0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2])
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
out = []
def p(*a_):
    s = " ".join(str(x) for x in a_)
    out.append(s); print(s)

p("### background histogram")
vals, cnts = np.unique(L.astype(np.uint8), return_counts=True)
top = sorted(zip(cnts, vals), reverse=True)[:8]
for c, v in top:
    p("lum %3d count %d" % (v, c))

# sample interior empty points
for (x, y) in [(480, 60), (480, 300), (100, 300), (200, 100), (700, 100)]:
    p("sample px", x, y, a[y, x].tolist(), "lum", round(float(L[y, x]), 1))

# --- frame rule detection: dark-ish thin long lines
p("")
p("### long thin lines (rows/cols where a consistent line colour repeats)")
darkline = L < 200
rowfrac = darkline.mean(axis=1)
colfrac = darkline.mean(axis=0)
p("rows with >60% dark:", [int(y) for y in range(H) if rowfrac[y] > 0.6])
p("cols with >60% dark:", [int(x) for x in range(W) if colfrac[x] > 0.6])
p("rows with >30% dark:", [int(y) for y in range(H) if rowfrac[y] > 0.3])
p("cols with >30% dark:", [int(x) for x in range(W) if colfrac[x] > 0.3])

# red rule specifically (coloured C00000-ish, anti-aliased)
redish = (R - L > 25) & (R - G > 45) & (R - B > 45) & (R > 110)
rowr = redish.mean(axis=1); colr = redish.mean(axis=0)
p("cols with red >20%:", [int(x) for x in range(W) if colr[x] > 0.2])
p("rows with red >20%:", [int(y) for y in range(H) if rowr[y] > 0.2])
p("cols with red >5%:", [int(x) for x in range(W) if colr[x] > 0.05])
p("rows with red >5%:", [int(y) for y in range(H) if rowr[y] > 0.05])

# --- text ink: darker than local bg
ink = L < 150
p("")
p("### dark ink (<150 lum) bbox")
ys, xs = np.nonzero(ink)
p("bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "count", len(ys))

# --- text line bands using dark ink, excluding the bottom bar and frame rules
band_src = ink.copy()
band_src[517:, :] = False  # exclude bottom black bar
# exclude frame rule columns if any
rowink = band_src.sum(axis=1)
thr = 4
bands = []
inb = False
for y in range(H):
    if rowink[y] > thr and not inb:
        st = y; inb = True
    elif rowink[y] <= thr and inb:
        bands.append((st, y - 1)); inb = False
if inb: bands.append((st, H - 1))
p("")
p("### text bands (dark ink, bottom bar excluded)")
for (y0, y1) in bands:
    sub = band_src[y0:y1 + 1]
    xs2 = np.nonzero(sub.sum(axis=0) > 0)[0]
    if len(xs2) == 0: continue
    # colour of ink
    cols = a[y0:y1 + 1][sub]
    med = np.median(cols, axis=0).astype(int)
    darkmask = sub & (L[y0:y1+1] < 150)
    h = y1 - y0 + 1
    p("band y %4d-%4d (h=%2d)  x %4d-%4d  inkpx %5d  median colour %s" %
      (y0, y1, h, xs2.min(), xs2.max(), int(sub.sum()), med.tolist()))

# finer bands: lower threshold to separate lines with small gaps
band_src2 = ink.copy(); band_src2[517:, :] = False
r2 = band_src2.sum(axis=1)
bands2 = []
inb = False
for y in range(H):
    if r2[y] > 1 and not inb:
        st = y; inb = True
    elif r2[y] <= 1 and inb:
        bands2.append((st, y - 1)); inb = False
if inb: bands2.append((st, H - 1))
# merge bands separated by < 6 px
merged = []
for b in bands2:
    if merged and b[0] - merged[-1][1] <= 6:
        merged[-1] = (merged[-1][0], b[1])
    else:
        merged.append(list(b))
p("")
p("### text bands (gap<=6 merged)")
for (y0, y1) in merged:
    sub = band_src2[y0:y1 + 1]
    xs2 = np.nonzero(sub.sum(axis=0) > 0)[0]
    if len(xs2) == 0: continue
    cols = a[y0:y1 + 1][sub]
    med = np.median(cols, axis=0).astype(int)
    p("band y %4d-%4d (h=%2d)  x %4d-%4d  inkpx %5d  median %s" %
      (y0, y1, y1 - y0 + 1, xs2.min(), xs2.max(), int(sub.sum()), med.tolist()))

# --- logo teal tile
p("")
p("### logo")
teal = (B > 60) & (B - R > 40) & (G - R > 25) & (G > 60)
tys, txs = np.nonzero(teal)
p("teal bbox x", txs.min(), txs.max(), "y", tys.min(), tys.max(), "count", len(tys))
p("teal median", np.median(a[teal].reshape(-1, 3), axis=0).tolist())
# teal column extent per row, and row extent per col to find tile bbox
colt = teal.sum(axis=0); rowt = teal.sum(axis=1)
p("teal cols >5:", [int(x) for x in range(W) if colt[x] > 5][:1], [int(x) for x in range(W) if colt[x] > 5][-1:])
p("teal rows >5:", [int(y) for y in range(H) if rowt[y] > 5][:1], [int(y) for y in range(H) if rowt[y] > 5][-1:])

# white panel to the right of teal: look for bright region x>700, y>430
sub = a[430:520, 600:960]
lumsub = L[430:520, 600:960]
bright = lumsub > 200
p("bright pixels in 600-960 x 430-520:", int(bright.sum()))
ysb, xsb = np.nonzero(bright)
if len(xsb):
    p("bright bbox in that sub: x", 600+xsb.min(), 600+xsb.max(), "y", 430+ysb.min(), 430+ysb.max())

# --- Arabic + english text ink in the logo band (x>690, y>430)
p("")
p("### logo band text ink (x>=684)")
band = ink[:, 684:]
yy, xx = np.nonzero(band)
if len(yy):
    p("ink bbox x", 684+xx.min(), 684+xx.max(), "y", yy.min(), yy.max(), "count", len(yy))
    sub2 = ink[:, 684:]
    r3 = sub2.sum(axis=1)
    bd = []
    inb = False
    for y in range(H):
        if r3[y] > 1 and not inb: st = y; inb = True
        elif r3[y] <= 1 and inb: bd.append((st, y-1)); inb = False
    if inb: bd.append((st, H-1))
    for (y0, y1) in bd:
        s2 = ink[y0:y1+1, 684:]
        x2 = np.nonzero(s2.sum(axis=0) > 0)[0]
        if len(x2) == 0: continue
        cols = a[y0:y1+1, 684:][s2]
        med = np.median(cols, axis=0).astype(int)
        p("logo-band band y %4d-%4d x %4d-%4d inkpx %5d median %s" %
          (y0, y1, 684+x2.min(), 684+x2.max(), int(s2.sum()), med.tolist()))

with open(OUT, "w") as f:
    f.write("\n".join(out))
p("")
p("wrote", OUT)
