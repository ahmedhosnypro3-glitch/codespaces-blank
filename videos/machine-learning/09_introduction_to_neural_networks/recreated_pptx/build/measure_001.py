#!/usr/bin/env python3
"""Measure slide_001 original frame: ink boxes, colors, logo crop.

V = videos/machine-learning/09_introduction_to_neural_networks
Outputs: build/measure_001.txt (geometry table) + assets/slide001_logo_tile.png
"""
import os
import sys
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = os.path.join(V, "unique_slides/slide_001.jpg")
OUT_M = os.path.join(V, "recreated_pptx/build/measure_001.txt")
ASSETS = os.path.join(V, "recreated_pptx/build/assets")
os.makedirs(ASSETS, exist_ok=True)

im = Image.open(ORIG).convert("RGB")
a = np.asarray(im).astype(np.int16)
H, W = a.shape[:2]
# original 960x540 -> slide is 13.333 x 7.5 in, so px->in depends on the
# slide's own content width.  The original slide body (red rule) spans the
# slide; measure it.
out = []
def p(*a):
    s = " ".join(str(x) for x in a)
    out.append(s)
    print(s)

p("frame size", W, "x", H)
p("px per inch if full slide 13.333x7.5:", round(W / 13.3333, 3), "x", round(H / 7.5, 3))

# ---- background colour (corner sample inside frame? sample a known-empty spot)
p("--- corner pixels ---")
for (x, y) in [(2, 2), (5, 5), (W - 3, 2), (2, H - 3), (W - 3, H - 3), (W // 2, 6)]:
    p("px", x, y, a[y, x].tolist())

# ---- red frame rule: find pixels close to C00000
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R > 120) & (R - G > 60) & (R - B > 60)
ys, xs = np.nonzero(red)
if len(ys):
    p("red ink bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "count", len(ys))
    # column histogram of red to find left/right rules
    colred = red.sum(axis=0)
    rowred = red.sum(axis=1)
    left_rules = [x for x in range(W) if colred[x] > H * 0.3]
    right_rules = [x for x in range(W) if colred[x] > H * 0.3]
    top_rules = [y for y in range(H) if rowred[y] > W * 0.3]
    bot_rules = [y for y in range(H) if rowred[y] > W * 0.3]
    p("cols with >30% red (rules):", left_rules[:1], left_rules[-1:] if len(left_rules) > 1 else "", "count", len(left_rules))
    p("rows with >30% red (rules):", top_rules[:1], bot_rules[-1:] if len(bot_rules) > 1 else "", "count", len(top_rules))
    # cluster the rule columns
    def clusters(vals):
        if not vals:
            return []
        cl = [[vals[0]]]
        for v in vals[1:]:
            (cl[-1] if v - cl[-1][-1] <= 2 else cl.append([v]))
        return [(c[0], c[-1]) for c in cl]
    p("red rule col clusters:", clusters(left_rules))
    p("red rule row clusters:", clusters(top_rules))
    p("red rule row clusters bottom:", clusters(bot_rules))

# ---- black bottom bar
blackbar = (R < 60) & (G < 60) & (B < 60)
rowblack = blackbar.sum(axis=1)
brs = [y for y in range(H) if rowblack[y] > W * 0.5]
p("bottom black bar rows:", brs[0] if brs else None, "-", brs[-1] if brs else None)

# ---- ink mask (anything not near background)
bg = np.median(a.reshape(-1, 3), axis=0)
p("bg median", bg.tolist())
dist = np.abs(a - bg).sum(axis=2)
ink = dist > 60
p("total ink px", int(ink.sum()))

# ---- horizontal ink bands (rows) to find text lines
rowink = ink.sum(axis=1)
bands = []
inb = False
for y in range(H):
    if rowink[y] > 3 and not inb:
        st = y
        inb = True
    elif rowink[y] <= 3 and inb:
        bands.append((st, y - 1))
        inb = False
if inb:
    bands.append((st, H - 1))
p("--- ink bands (rows with >3 ink px) ---")
for b in bands:
    y0, y1 = b
    sub = ink[y0:y1 + 1]
    xs2 = np.nonzero(sub.sum(axis=0) > 0)[0]
    p("band y %d-%d  x %d-%d  inkpx %d" % (y0, y1, xs2.min(), xs2.max(), int(sub.sum())))

# ---- per-band dominant colour (text colour) using the ink mask
p("--- per-band ink colour ---")
for b in bands:
    y0, y1 = b
    sub = ink[y0:y1 + 1]
    cols = a[y0:y1 + 1][sub]
    if len(cols) == 0:
        continue
    med = np.median(cols, axis=0).astype(int)
    p("band y %d-%d  median ink colour %s" % (y0, y1, med.tolist()))

# ---- locate logo region: bottom-right teal
teal = (B > 60) & (B - R > 40) & (G - R > 30) & (G > 60)
tys, txs = np.nonzero(teal)
if len(tys):
    p("--- teal ---")
    p("teal bbox x", txs.min(), txs.max(), "y", tys.min(), tys.max(), "count", len(tys))
    p("teal median", np.median(a[teal].reshape(-1, 3), axis=0).tolist())
    rowt = teal.sum(axis=1)
    tb = [y for y in range(H) if rowt[y] > 5]
    p("teal rows", tb[0] if tb else None, "-", tb[-1] if tb else None)
    colt = teal.sum(axis=0)
    cb = [x for x in range(W) if colt[x] > 5]
    p("teal cols", cb[0] if cb else None, "-", cb[-1] if cb else None)

# ---- white panel right of teal
p("--- white panel (bright, not bg) ---")
white = (R > 230) & (G > 230) & (B > 230)
p("white count", int(white.sum()))

with open(OUT_M, "w") as f:
    f.write("\n".join(out))
p("wrote", OUT_M)
