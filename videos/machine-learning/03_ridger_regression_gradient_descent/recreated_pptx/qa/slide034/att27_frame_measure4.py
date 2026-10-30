#!/usr/bin/env python3
"""att27 frame measure 4 — addendum: band edges, column separators, next-x
verticals, tick-label size, gridline core color, plot border right col."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("unique_slides/slide_034.jpg").convert("RGB")).astype(int)
out = []
def w(s=""): out.append(s)

# --- 1. band fill x-extent (row scans) ---
w("### 1. band fill x-extents")
for nm, yy, test in (
    ("band1 y340", 340, lambda p: p[2] < 190 and p[0] > 180 and p[1] > 190),
    ("band2 y395", 395, lambda p: p[2] > 200 and p[0] < 230 and p[1] < 200),
    ("band3 y430", 430, lambda p: p[0] > 200 and p[1] > 180 and p[2] < 215),
    ("slopebg y475", 475, lambda p: p[1] > 200 and p[0] > 180 and p[2] < 230),
    ("nextx y497", 497, lambda p: p[0] > 200 and p[1] < 215 and p[2] < 225),
):
    row = im[yy]
    xs = [x for x in range(60, 900) if test(row[x])]
    if xs:
        w(" %s: fill x%d..%d n=%d" % (nm, min(xs), max(xs), len(xs)))
    else:
        w(" %s: none" % nm)
# detailed left-edge + right-edge pixel runs
w(" band1 y340 x66..90: %s" % [(x, tuple(int(v) for v in im[340, x])) for x in range(66, 90)])
w(" band1 y340 x858..884: %s" % [(x, tuple(int(v) for v in im[340, x])) for x in range(858, 884)])
w(" nextx y497 x66..90: %s" % [(x, tuple(int(v) for v in im[497, x])) for x in range(66, 90)])
w(" nextx y497 x858..884: %s" % [(x, tuple(int(v) for v in im[497, x])) for x in range(858, 884)])

# --- 2. column separators via B-channel profile (bands 1-3) ---
w("### 2. column separator candidates (B-channel bumps)")
for nm, (ya, yb) in (("band1", (334, 366)), ("band2", (377, 408)), ("band3", (420, 452))):
    seg = im[ya:yb, 140:885]
    bmean = seg[..., 2].mean(axis=0)
    fill_b = np.median(bmean)
    bumps = [140 + i for i in range(1, len(bmean) - 1)
             if bmean[i] > fill_b + 25 and bmean[i] >= bmean[i - 1] and bmean[i] >= bmean[i + 1]]
    # cluster
    cl = []
    for x in bumps:
        if cl and x - cl[-1][-1] <= 2: cl[-1].append(x)
        else: cl.append([x])
    w(" %s fillB=%.0f bump cols: %s" % (nm, fill_b, [round(sum(c) / len(c), 1) for c in cl]))

# --- 3. next-x strong red verticals ---
w("### 3. next-x strong-red cols (y486..500)")
seg = im[486:500, 70:880]
r, g, b = seg[..., 0], seg[..., 1], seg[..., 2]
red = (r > 140) & (r - g > 100) & (r - b > 90)
coln = red.sum(axis=0)
cand = [70 + i for i in np.nonzero(coln >= 6)[0]]
cl = []
for x in cand:
    if cl and x - cl[-1][-1] <= 2: cl[-1].append(x)
    else: cl.append([x])
w(" strong-red col clusters: %s" % [f"({c[0]},{c[-1]})" for c in cl])

# --- 4. tick label ink heights ---
w("### 4. tick-label ink")
def inkbbox(x0, x1, y0, y1, thr=140):
    seg = im[y0:y1, x0:x1]
    m = seg.mean(axis=2)
    ys, xs = np.nonzero(m < thr)
    if len(xs) == 0: return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max(), len(xs))
w(" xlabel '-10' zone x618..650 y172..192: %s" % (inkbbox(618, 650, 172, 192),))
w(" xlabel '2' zone x736..752 y172..192: %s" % (inkbbox(736, 752, 172, 192),))
w(" xlabel '10' zone x806..830 y172..192: %s" % (inkbbox(806, 830, 172, 192),))
w(" ylabel '-12' zone x694..716 y276..294: %s" % (inkbbox(694, 716, 276, 294),))
w(" ylabel '8' zone x700..718 y92..108: %s" % (inkbbox(700, 718, 92, 108),))

# --- 5. gridline core color ---
w("### 5. gridline core")
for nm, x, y0, y1 in (("vgrid x668", 668, 240, 300), ("vgrid x775", 775, 220, 270),
                      ("hgrid y190", 190, 620, 700)):
    if nm.startswith("h"):
        seg = im[y - 1:y + 2, 620:700] if False else im[189:192, 620:700]
        m = seg.mean(axis=2)
        i = np.unravel_index(np.argmin(m), m.shape)
        w(" %s: darkest %s at (%d,%d)" % (nm, tuple(int(v) for v in seg[i]), 620 + i[1], 189 + i[0]))
    else:
        seg = im[y0:y1, x - 1:x + 2]
        m = seg.mean(axis=2)
        i = np.unravel_index(np.argmin(m), m.shape)
        w(" %s: darkest %s at (%d,%d)" % (nm, tuple(int(v) for v in seg[i]), x - 1 + i[1], y0 + i[0]))

# --- 6. plot border right column ---
w("### 6. plot border cols x840..852 (y100..300)")
seg = im[100:300, 840:853]
r, g, b = seg[..., 0], seg[..., 1], seg[..., 2]
dr = (r > 90) & (r < 215) & (g < 90) & (b < 90)
coln = dr.sum(axis=0)
w(" dark-red counts: %s" % {840 + i: int(coln[i]) for i in range(len(coln)) if coln[i] > 10})
w(" x846 sample rows: %s" % [(y, tuple(int(v) for v in im[y, 846])) for y in (80, 150, 250, 300)])

# --- 7. insert dashed border rows at x700 ---
w("### 7. insert border rows x700 y324..330 / y366..374")
w(" top: %s" % [(y, tuple(int(v) for v in im[y, 700])) for y in range(324, 331)])
w(" bot: %s" % [(y, tuple(int(v) for v in im[y, 700])) for y in range(366, 374)])

# --- 8. band2/3 left+right border strokes ---
w("### 8. band border verticals")
for nm, yy in (("band2 y395", 395), ("band3 y430", 430)):
    w(" %s x64..92: %s" % (nm, [(x, tuple(int(v) for v in im[yy, x])) for x in range(64, 92)]))
    w(" %s x856..884: %s" % (nm, [(x, tuple(int(v) for v in im[yy, x])) for x in range(856, 884)]))

txt = "\n".join(out)
with open("recreated_pptx/qa/slide034/att27_frame_measure4.txt", "w") as f:
    f.write(txt + "\n")
print(txt)
