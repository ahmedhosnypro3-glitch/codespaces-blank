#!/usr/bin/env python3
"""Structural detection on slide_008.jpg: plot rect, axes, hatch tint map, label boxes."""
from PIL import Image
import numpy as np

im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
lum = a.mean(axis=2)
sat = a.max(axis=2) - a.min(axis=2)

def hx(p): return "#%02X%02X%02X" % (p[0], p[1], p[2])

# --- find near-white mask ---
notwhite = lum < 235
print("=== long horizontal runs (non-white count per row, top 25) ===")
rc = notwhite.sum(axis=1)
for y in np.argsort(-rc)[:25]:
    print(f"  y={y:3d} count={rc[y]:4d}")

print("\n=== long vertical runs (non-white count per col, top 25) ===")
cc = notwhite.sum(axis=0)
for x in np.argsort(-cc)[:25]:
    print(f"  x={x:3d} count={cc[x]:4d}")

# --- find strongly saturated pixels (the decision lines / dots / boxes) ---
strong = sat > 70
print("\n=== saturated color components ===")
from collections import Counter
cnt = Counter()
for y in range(H):
    for x in range(W):
        if strong[y, x]:
            cnt[hx(a[y,x])] += 1
for c, n in cnt.most_common(14):
    print(f"  {c}  {n}")

# --- green-tinted / blue-tinted / red-tinted area masks (light tints) ---
def tint_map(name, cond):
    ys, xs = np.where(cond)
    if not len(ys):
        print(f"{name}: none"); return
    print(f"{name}: n={len(ys)} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")

greenish = (a[:,:,1] - a[:,:,0] > 6) & (a[:,:,1] - a[:,:,2] > 6) & (lum > 190) & (lum < 250)
blueish  = (a[:,:,2] - a[:,:,0] > 8) & (a[:,:,2] - a[:,:,1] > 8) & (lum > 180) & (lum < 250)
reddish  = (a[:,:,0] - a[:,:,1] > 8) & (a[:,:,0] - a[:,:,2] > 8) & (lum > 180) & (lum < 252)
yellowish= (a[:,:,0] > 200) & (a[:,:,1] > 190) & (a[:,:,2] < 160) & (sat > 50)
purpleish= (a[:,:,0] > 150) & (a[:,:,2] > 150) & (a[:,:,1] < a[:,:,0]-20) & (sat > 30)

print("\n=== tint regions ===")
tint_map("green tint (hatch/dots)", greenish)
tint_map("blue tint (hatch/dots)", blueish)
tint_map("red tint (hatch/dots)", redish)
tint_map("yellow (C labels)", yellowish)
tint_map("purple (New Class)", purpleish)

# --- print a coarse hue map: 24x14 grid, dominant tint category ---
print("\n=== coarse tint map (24 cols x 14 rows), G=green B=blue R=red Y=yellow P=purple .=white K=dark ===")
for gy in range(14):
    y0, y1 = gy*H//14, (gy+1)*H//14
    row = ""
    for gx in range(24):
        x0, x1 = gx*W//24, (gx+1)*W//24
        blk = a[y0:y1, x0:x1].reshape(-1,3)
        bl = blk.mean(axis=0)
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

# --- locate the "Undefined" and "New Class" boxes: look for rectangular border of a distinct color ---
print("\n=== purple-ish pixel bbox (New Class) ===")
ys, xs = np.where(purpleish)
if len(ys):
    print(f"  x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]  center=({(xs.min()+xs.max())//2},{(ys.min()+ys.max())//2})")
    # column histogram
    import numpy as np
    cc2 = np.bincount(xs, minlength=W)
    print("  top cols:", sorted(range(W), key=lambda i: -cc2[i])[:8])
    rc2 = np.bincount(ys, minlength=H)
    print("  top rows:", sorted(range(H), key=lambda i: -rc2[i])[:8])

print("\n=== strong-sat green bbox (C1 dots + d3 line) ===")
g = strong & (a[:,:,1] > a[:,:,0]+40) & (a[:,:,1] > a[:,:,2]+30)
ys, xs = np.where(g)
if len(ys):
    print(f"  n={len(ys)} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")

print("=== strong-sat blue bbox (C2 dots + d2 line) ===")
b = strong & (a[:,:,2] > a[:,:,0]+50) & (a[:,:,2] > a[:,:,1]+30)
ys, xs = np.where(b)
if len(ys):
    print(f"  n={len(ys)} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")

print("=== strong-sat red bbox (C3 dots + d1 line) ===")
r = strong & (a[:,:,0] > a[:,:,1]+60) & (a[:,:,0] > a[:,:,2]+60)
ys, xs = np.where(r)
if len(ys):
    print(f"  n={len(ys)} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
    # separate: d1 line spans a wide diagonal; find red in top half vs bottom
    for lo, hi in [(0,180),(180,360),(360,540)]:
        sel = (ys>=lo)&(ys<hi)
        if sel.sum():
            print(f"    y[{lo},{hi}): n={sel.sum()} x[{xs[sel].min()},{xs[sel].max()}]")
