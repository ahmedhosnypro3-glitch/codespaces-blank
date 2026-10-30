#!/usr/bin/env python3
"""Deeper measurement of slide_020.jpg: underline, cursor, numeral, colors, clusters."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_020.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

# 1. Underline check under line 2 (y 344..372, x 180..748): any non-panel ink?
gray_panel = (abs(r-233)<16) & (abs(g-233)<16) & (abs(b-231)<18)
ink = ~gray_panel
print("== underline scan rows 345..372, x 180..748 ==")
for y in range(345, 373):
    row = ink[y, 180:748]
    n = row.sum()
    if n > 0:
        cols = np.where(row)[0] + 180
        print(f"  y={y}: {n} ink px, x {cols.min()}..{cols.max()}")
print("(no output rows = no ink => NO underline)")

# 2. Row density profile of the two title lines (cap-height measurement)
print("== title red row profile (rows 226..268 and 306..348) ==")
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
for rng in ((226, 268), (306, 348)):
    prof = []
    for y in range(rng[0], rng[1]+1):
        prof.append(int(red[y, 100:800].sum()))
    print(f"  rows {rng[0]}..{rng[1]}: {prof}")

# 3. title core color (densest pixels)
ys, xs = np.where(red[230:265, 159:759])
region = im[230:265, 159:759]
m = red[230:265, 159:759]
core = region[m]
print("== title color: mean of red-core px ==", core.mean(axis=0))

# 4. cursor region detail (x 430..500, y 380..430)
print("== cursor region: non-panel ink map, x 430..500 y 380..430 ==")
sub = ink[380:430, 430:500]
ysc, xsc = np.where(sub)
if len(ysc):
    print("  cursor ink bbox x", xsc.min()+430, "-", xsc.max()+430,
          " y", ysc.min()+380, "-", ysc.max()+380, " px:", len(ysc))
    # white fill?
    wh = (r[380:430,430:500]>235)&(g[380:430,430:500]>235)&(b[380:430,430:500]>235)
    print("  near-white px in region:", int(wh.sum()))
else:
    print("  no cursor ink found")

# 5. badge numeral refined (inside yellow disc interior)
print("== badge numeral ==")
darknum = (r < 120) & (g < 120) & (b < 120)
inner = darknum[60:88, 864:890]
ysn, xsn = np.where(inner)
if len(ysn):
    print("  numeral bbox x", xsn.min()+864, "-", xsn.max()+864,
          " y", ysn.min()+60, "-", ysn.max()+60, " px:", len(ysn))

# 6. connected clusters of any ink (excluding panel/white) over the whole frame
from scipy import ndimage
anyink = ink & ~((r>235)&(g>235)&(b>235))
# exclude chrome strokes columns and bottom rows for content view
content = anyink.copy()
content[:, :64] = False; content[:, 896:] = False
content[536:, :] = False; content[:48, :] = False
lbl, n = ndimage.label(content)
print("== content ink clusters (size >= 30 px, outside chrome) ==")
for i in range(1, n+1):
    m2 = lbl == i
    if m2.sum() >= 30:
        ys6, xs6 = np.where(m2)
        mean_col = im[m2].mean(axis=0)
        print(f"  cluster {i}: px={int(m2.sum())} x {xs6.min()}-{xs6.max()} "
              f"y {ys6.min()}-{ys6.max()} mean_rgb={mean_col.round(0)}")

# 7. gap between panel and strokes? sample colors at key x columns (panel edge)
print("== pixel colors: (54,300),(58,300),(901,300),(903,300),(100,500),(100,400) ==")
for (x, y) in ((54,300),(56,300),(58,300),(59,300),(899,300),(901,300),(903,300),(100,500),(100,400),(100,180)):
    print(f"  ({x},{y}): {tuple(im[y,x])}")
