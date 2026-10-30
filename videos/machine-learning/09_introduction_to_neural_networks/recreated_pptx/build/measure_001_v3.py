#!/usr/bin/env python3
"""Measure slide_001 v3: clean text bands (frame rules excluded), badge, logo structure."""
import os
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = os.path.join(V, "unique_slides/slide_001.jpg")
OUT = os.path.join(V, "recreated_pptx/build/measure_001_v3.txt")

im = Image.open(ORIG).convert("RGB")
a = np.asarray(im).astype(np.int16)
H, W = a.shape[:2]
L = (0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2])
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
out = []
def p(*x):
    s = " ".join(str(v) for v in x); out.append(s); print(s)

bgL = 232.0
ink = L < 160
# exclude frame rules and bottom bar
mask = ink.copy()
mask[:, 56:61] = False
mask[:, 899:904] = False
mask[42:46, :] = False
mask[516:, :] = False

rowink = mask.sum(axis=1)
bands = []
inb = False
for y in range(H):
    if rowink[y] > 2 and not inb:
        st = y; inb = True
    elif rowink[y] <= 2 and inb:
        bands.append([st, y - 1]); inb = False
if inb: bands.append([st, H - 1])
merged = []
for b in bands:
    if merged and b[0] - merged[-1][1] <= 8:
        merged[-1][1] = b[1]
    else:
        merged.append(b)
p("### CLEAN TEXT BANDS (frame rules + bottom bar excluded, gap<=8 merged)")
p("band        y-range   h    x-range        cap   fontsize~pt  median-colour")
for (y0, y1) in merged:
    sub = mask[y0:y1 + 1]
    xs2 = np.nonzero(sub.sum(axis=0) > 0)[0]
    if len(xs2) < 3: continue
    cols = a[y0:y1 + 1][sub]
    med = np.median(cols, axis=0).astype(int)
    h = y1 - y0 + 1
    # approximate point size: cap height ~0.7em for latin; use ink height
    p("y %4d-%4d  h=%3d  x %4d-%4d  w=%4d  inkpx=%5d  med=%s" %
      (y0, y1, h, xs2.min(), xs2.max(), xs2.max() - xs2.min() + 1, int(sub.sum()), med.tolist()))

# ---- per-line x-extent for multi-line blocks (split by column profile)
p("")
p("### per-band column clusters (split lines inside a band)")
for (y0, y1) in merged:
    sub = mask[y0:y1 + 1]
    colp = sub.sum(axis=0)
    gaps = []
    run = None
    for x in range(W):
        if colp[x] > 0:
            if run is None: run = [x, x]
            else: run[1] = x
        else:
            if run is not None:
                gaps.append(run); run = None
    if run is not None: gaps.append(run)
    if len(gaps) > 1:
        p("band y %d-%d has %d column groups:" % (y0, y1, len(gaps)))
        for g in gaps:
            p("   x %d-%d" % (g[0], g[1]))

# ---- badge: purple detection
p("")
p("### badge (purple)")
purple = (R - G > 20) & (B - G > 15) & (R > 60) & (B > 60) & (L < 200)
ys, xs = np.nonzero(purple)
if len(ys):
    p("purple bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "count", len(ys))
    p("purple median", np.median(a[purple].reshape(-1, 3), axis=0).astype(int).tolist())
    p("purple w", xs.max() - xs.min() + 1, "h", ys.max() - ys.min() + 1)
# white circle near top-right?
sub = a[20:100, 820:940]
lumsub = L[20:100, 820:940]
p("bright(>248) in 820-940 x 20-100:", int((lumsub > 248).sum()))
ys2, xs2 = np.nonzero(lumsub > 248)
if len(xs2):
    p("  bbox x", 820 + xs2.min(), 820 + xs2.max(), "y", 20 + ys2.min(), 20 + ys2.max())

# ---- logo region: teal tile + white panel
p("")
p("### logo structure")
teal = (B > 60) & (B - R > 40) & (G - R > 25) & (G > 60)
tys, txs = np.nonzero(teal)
p("teal tile bbox x", txs.min(), txs.max(), "y", tys.min(), tys.max(),
  "-> x %d-%d y %d-%d" % (txs.min(), txs.max(), tys.min(), tys.max()))
p("teal w", txs.max() - txs.min() + 1, "h", tys.max() - tys.min() + 1)
p("teal median", np.median(a[teal].reshape(-1, 3), axis=0).astype(int).tolist())
# white panel right of x=680, y>430, lum > 245 (brighter than bg 232)
wp = (L > 245)
wp[:430] = False
wp[:, :680] = False
ys3, xs3 = np.nonzero(wp)
if len(xs3):
    p("white panel bbox x", xs3.min(), xs3.max(), "y", ys3.min(), ys3.max())
    p("white panel median", np.median(a[wp].reshape(-1, 3), axis=0).astype(int).tolist())

# ---- dark ink inside logo band x>=676, y 430..515
p("")
p("### logo band text ink (x>=676, y 430-515)")
lg = np.zeros_like(ink)
lg[430:516, 676:] = ink[430:516, 676:]
rowlg = lg.sum(axis=1)
bd = []
inb = False
for y in range(430, 516):
    if rowlg[y] > 0 and not inb: st = y; inb = True
    elif rowlg[y] == 0 and inb: bd.append((st, y - 1)); inb = False
if inb: bd.append((st, 515))
for (y0, y1) in bd:
    s2 = lg[y0:y1 + 1]
    xs4 = np.nonzero(s2.sum(axis=0) > 0)[0]
    if len(xs4) < 2: continue
    cols = a[y0:y1 + 1][s2]
    med = np.median(cols, axis=0).astype(int)
    p("y %4d-%4d h=%3d x %4d-%4d w=%4d inkpx=%4d med=%s" %
      (y0, y1, y1 - y0 + 1, xs4.min(), xs4.max(), xs4.max() - xs4.min() + 1, int(s2.sum()), med.tolist()))

# ---- ASCII of the teal tile (luminance ramp)
p("")
p("### ASCII luminance map of logo tile x 580-700, y 425-515")
RAMP = "@%#*+=-:. "
x0, x1, y0, y1 = 580, 700, 425, 515
for y in range(y0, y1, 2):
    row = ""
    for x in range(x0, x1, 2):
        v = L[y, x]
        idx = min(9, int((255 - v) / 256 * 10))
        row += RAMP[idx]
    p("y%4d %s" % (y, row))

p("")
p("### ASCII luminance map of white panel x 676-910, y 430-516")
x0, x1, y0, y1 = 676, 910, 430, 516
for y in range(y0, y1, 2):
    row = ""
    for x in range(x0, x1, 2):
        v = L[y, x]
        idx = min(9, int((255 - v) / 256 * 10))
        row += RAMP[idx]
    p("y%4d %s" % (y, row))

with open(OUT, "w") as f:
    f.write("\n".join(out))
p(""); p("wrote", OUT)
