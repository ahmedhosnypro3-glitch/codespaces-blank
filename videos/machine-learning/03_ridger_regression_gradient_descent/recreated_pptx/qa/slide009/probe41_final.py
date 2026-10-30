#!/usr/bin/env python3
"""Probe 41: final geometry — blue fitted-line exact endpoints, grid-line exact
spans, annotation-box exact border rects, orange point exact centroids/diameters.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

BLU = (b > 120) & ((b - r) > 40) & ((b - g) > 30)
ORA = (r >= 160) & (g >= 85) & (g <= 155) & (b <= 125) & ((r - b) >= 70)
GRID = (r > 225) & (r < 250) & (np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b) < 12)
NAVY = (b > 90) & ((b - r) > 40) & ((b - g) > 30)
PALE = (b > 240) & ((b - r) > 6) & (g >= r - 4)

def runs_of(vals, gap=1):
    vals = sorted(int(v) for v in vals)
    if not vals: return []
    out, s, p = [], vals[0], vals[0]
    for v in vals[1:]:
        if v <= p + gap: p = v; continue
        out.append((s, p)); s = p = v
    out.append((s, p)); return out

print("=== BLUE fitted line: first/last column with >=3 blue px (rows 195..415) ===")
for nm, x0, x1 in (("LEFT", 100, 460), ("RIGHT", 495, 860)):
    cols = [(x, len(np.nonzero(BLU[195:415, x])[0])) for x in range(x0, x1+1)]
    good = [c for c, n in cols if n >= 3]
    print(f"  {nm}: x {min(good)}..{max(good)}")
    for xx in (min(good), max(good)):
        rr = runs_of(np.nonzero(BLU[195:415, xx])[0] + 195)
        print(f"    x{xx}: " + "  ".join(f"y{p}..{q}" for p, q in rr))

print("\n=== GRID line spans (first/last row/col with >=200 grid px) ===")
for nm, x0, x1, y0, y1 in (("LEFT", 98, 463, 111, 470), ("RIGHT", 489, 867, 111, 470)):
    m = GRID[y0:y1+1, x0:x1+1]
    rr = runs_of(np.where(m.sum(axis=1) > 150)[0] + y0)
    cc = runs_of(np.where(m.sum(axis=0) > 150)[0] + x0)
    print(f"  {nm} ROWS(>150): {rr}")
    print(f"  {nm} COLS(>150): {cc}")

print("\n=== ANNOTATION BOX exact border (navy) ===")
for nm, x0, x1, y0, y1 in (("LEFT", 96, 320, 143, 178), ("RIGHT", 628, 738, 143, 178)):
    m = NAVY[y0:y1+1, x0:x1+1]
    if not m.any():
        print(f"  {nm}: no navy"); continue
    ys, xs = np.nonzero(m)
    print(f"  {nm}: navy bbox x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()}")
    print(f"    rows>10: {runs_of(np.where(m.sum(axis=1)>10)[0]+y0)}")
    print(f"    cols>10: {runs_of(np.where(m.sum(axis=0)>10)[0]+x0)}")
    # pale fill extent
    m2 = PALE[y0:y1+1, x0:x1+1]
    ys2, xs2 = np.nonzero(m2)
    print(f"    pale fill bbox x{x0+xs2.min()}..{x0+xs2.max()} y{y0+ys2.min()}..{y0+ys2.max()}")

print("\n=== ORANGE points (exact centroid + diameter) ===")
from scipy import ndimage
for nm, x0, x1 in (("LEFT", 98, 463), ("RIGHT", 489, 867)):
    m = ORA[111:471, x0:x1+1].copy()
    m[:, 124:131] = False if nm == "LEFT" else m[:, 124:131]
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    pts = []
    for i, sl in enumerate(objs, 1):
        sz = int((lab[sl] == i).sum())
        if sz < 25: continue
        X0, X1 = sl[1].start, sl[1].stop-1
        Y0, Y1 = sl[0].start, sl[0].stop-1
        pts.append(((X0+X1)/2+x0, (Y0+Y1)/2+111, X1-X0+1, Y1-Y0+1, sz))
    pts.sort()
    print(f"  {nm}: {len(pts)} points")
    for cx, cy, w, h, sz in pts:
        print(f"    c=({cx:6.1f},{cy:6.1f}) d={w}x{h} n={sz}")
