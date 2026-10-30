#!/usr/bin/env python3
"""Structural detection v2 on slide_008.jpg."""
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
lum = a.mean(axis=2)
sat = a.max(axis=2) - a.min(axis=2)

def hx(p): return "#%02X%02X%02X" % (p[0], p[1], p[2])

notwhite = lum < 235
rc = notwhite.sum(axis=1)
print("=== rows with nonwhite > 300 (excluding bottom bar) ===")
for y in range(0, 510):
    if rc[y] > 300:
        print(f"  y={y:3d} count={rc[y]:4d}")

cc = notwhite.sum(axis=0)
print("\n=== cols with nonwhite > 150 ===")
for x in range(W):
    if cc[x] > 150:
        print(f"  x={x:3d} count={cc[x]:4d}")

print("\n=== y=43 and y=517 row content (RGB segments) ===")
for y in [43, 517]:
    print(f" y={y}:")
    for x in [10, 60, 100, 200, 300, 400, 500, 600, 700, 800, 900, 940]:
        print(f"   x={x:3d} {hx(a[y,x])}")

print("\n=== x=58 and x=901 column content ===")
for x in [58, 901]:
    print(f" x={x}:")
    for y in [10, 50, 100, 150, 200, 300, 400, 470, 500]:
        print(f"   y={y:3d} {hx(a[y,x])}")

# coarse tint map
print("\n=== coarse tint map (24 cols x 14 rows, full 540) G/B/R/Y/P/./K ===")
for gy in range(14):
    y0, y1 = gy*H//14, (gy+1)*H//14
    row = ""
    for gx in range(24):
        x0, x1 = gx*W//24, (gx+1)*W//24
        blk = a[y0:y1, x0:x1].reshape(-1,3).mean(axis=0)
        s = bl.max()-bl.min()
        if bl.mean() < 120: c = "K"
        elif s < 12: c = "."
        elif bl[1] >= bl[0] and bl[1] >= bl[2]: c = "G"
        elif bl[2] >= bl[0] and bl[2] >= bl[1]: c = "B"
        elif bl[0] > bl[2] + 30 and bl[0] > bl[1] + 30: c = "Y"
        elif bl[0] >= bl[1] and bl[0] >= bl[2]: c = "R"
        else: c = "?"
        row += c
    print(f"  y{gy:2d} {row}")

# vertical band structure: find the plot rect borders by detecting thin straight colored lines
print("\n=== candidate vertical plot borders: columns where many pixels are strongly saturated ===")
strong = sat > 70
cs = strong.sum(axis=0)
found = []
for x in range(W):
    if cs[x] > 200:
        found.append((x, cs[x]))
print(" ", found)

print("=== candidate horizontal borders: rows ===")
rs = strong.sum(axis=1)
found = []
for y in range(H):
    if rs[y] > 200:
        found.append((y, rs[y]))
print(" ", found)

# Find the d1/d2/d3 lines: for each hue family, list pixel positions then fit line
print("\n=== green strong pixels (C1 dots + d3 line) ===")
g = strong & (a[:,:,1] > a[:,:,0]+40) & (a[:,:,1] > a[:,:,2]+30)
ys, xs = np.where(g)
print(f"  n={len(ys)} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
# group by y to separate the dot cluster (dense) from the line (spread)
import collections
hist = collections.Counter((ys//20)*20)
for k in sorted(hist):
    sel = ((ys//20)*20)==k
    print(f"   y[{k},{k+20}): n={sel.sum()} x[{xs[sel].min()},{xs[sel].max()}]")

print("\n=== blue strong pixels ===")
b = strong & (a[:,:,2] > a[:,:,0]+50) & (a[:,:,2] > a[:,:,1]+30)
ys, xs = np.where(b)
print(f"  n={len(ys)} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
hist = collections.Counter((ys//20)*20)
for k in sorted(hist):
    sel = ((ys//20)*20)==k
    print(f"   y[{k},{k+20}): n={sel.sum()} x[{xs[sel].min()},{xs[sel].max()}]")

print("\n=== red strong pixels ===")
r = strong & (a[:,:,0] > a[:,:,1]+60) & (a[:,:,0] > a[:,:,2]+60)
ys, xs = np.where(r)
print(f"  n={len(ys)} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
hist = collections.Counter((ys//20)*20)
for k in sorted(hist):
    sel = ((ys//20)*20)==k
    print(f"   y[{k},{k+20}): n={sel.sum()} x[{xs[sel].min()},{xs[sel].max()}]")

print("\n=== yellow strong pixels (C labels) ===")
yl = strong & (a[:,:,0] > a[:,:,1]+40) & (a[:,:,1] > a[:,:,2]+40)
ys, xs = np.where(yl)
print(f"  n={len(ys)} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")

print("\n=== purple-ish pixels (New Class) ===")
pp = (a[:,:,0] > 140) & (a[:,:,2] > 140) & (a[:,:,1] < a[:,:,0]-25) & (sat > 25)
ys, xs = np.where(pp)
if len(ys):
    print(f"  n={len(ys)} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] center=({(xs.min()+xs.max())//2},{(ys.min()+ys.max())//2})")
else:
    print("  none")
