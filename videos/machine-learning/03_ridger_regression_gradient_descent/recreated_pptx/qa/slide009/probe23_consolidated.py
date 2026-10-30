#!/usr/bin/env python3
"""Probe 23 (FINAL consolidated measurement): every geometry value needed by
build/slide_009.js, measured in one place with predicates tailored per element.

Element predicates:
  box border   navy stroke: b>150 and r<120  (core ~ (36,24,106))
  box interior white:      r>248 and g>248 and b>248
  equation text            near-black: r+g+b < 430  (text is black; grid is
                          light gray ~700+, the red arrowhead is saturated)
  'mm' label                near-black, same predicate, beside the arrowhead
  grid lines                light gray: 170<r=g=b<225 and max-min<=12
  red axis/arrows           r-g>40 and r-b>40 and r>90
  blue fitted line          b-r>40 and b-g>25 and b>110
  orange points             r>200 and g>130 and b<130 and r-b>70
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def runs(vals):
    """collapse a sorted index list into (start,end) runs"""
    out = []
    for v in vals:
        if out and v - out[-1][1] <= 2:
            out[-1][1] = v
        else:
            out.append([v, v])
    return [(s, e) for s, e in out]


def report(nm, x0, x1, y0, y1):
    m = np.zeros((y1 - y0 + 1, x1 - x0 + 1), bool)
    for i, y in enumerate(range(y0, y1 + 1)):
        row = a[y, x0:x1 + 1]
        q = (row // 8) * 8
        keys, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
        bg = keys[counts.argmax()]
        m[i] = np.abs(row - bg).max(axis=1) > 60
    ys, xs = np.where(m)
    if not len(ys):
        print(f"  {nm}: <none>")
        return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())


NAVY = (b > 150) & (r < 120)
WHT = (r > 248) & (g > 248) & (b > 248)
BLK = (r + g + b) < 430
GRID = (abs(r - g) <= 12) & (abs(g - b) <= 12) & (abs(r - b) <= 12) & (r > 165) & (r < 226)
RED = (r - g > 40) & (r - b > 40) & (r > 90)
BLU = (b - r > 40) & (b - g > 25) & (b > 110)
ORA = (r > 200) & (g > 130) & (b < 130) & (r - b > 70)

print("############ 1. PANEL BORDERS (navy stroke cores) ############")
for side, xa, xb in (("LEFT", 85, 480), ("RIGHT", 475, 885)):
    sub = NAVY[100:480, xa:xb]
    ys, xs = np.where(sub)
    print(f"  {side} navy bbox: x {xa+xs.min()}..{xa+xs.max()} y {100+ys.min()}..{100+ys.max()}")
    # column histogram of navy -> the vertical border columns
    colsum = sub.sum(axis=0)
    print(f"    vertical border cols (navy rows>60): {runs(np.where(colsum > 60)[0] + xa)}")
    rowsum = sub.sum(axis=1)
    print(f"    horizontal border rows (navy px>200): {runs(np.where(rowsum > 200)[0] + 100)}")
    # white interior
    wi = WHT[100:480, xa:xb]
    ys2, xs2 = np.where(wi)
    print(f"    white interior bbox: x {xa+xs2.min()}..{xa+xs2.max()} y {100+ys2.min()}..{100+ys2.max()}")

print("\n############ 2. EQUATION TEXT (black ink inside the panel) ############")
for nm, x0, x1 in (("LEFT", 96, 464), ("RIGHT", 484, 868)):
    sub = BLK[145:175, x0:x1]
    ys, xs = np.where(sub)
    print(f"  {nm} equation ink: x {x0+xs.min()}..{x0+xs.max()} (w={xs.max()-xs.min()+1}) "
          f"y {145+ys.min()}..{145+ys.max()} (h={ys.max()-ys.min()+1})")
    # per-column runs so word gaps are visible
    colsum = sub.sum(axis=0)
    print(f"    col runs (>=2 inked rows): {runs(np.where(colsum >= 2)[0] + x0)}")

print("\n############ 3. 'mm' LABELS (black ink beside the y-axis arrowhead) ############")
for nm, x0, x1 in (("LEFT", 130, 240), ("RIGHT", 495, 605)):
    sub = BLK[145:180, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys):
        print(f"  {nm}: <none> in window")
        continue
    print(f"  {nm} ink: x {x0+xs.min()}..{x0+xs.max()} (w={xs.max()-xs.min()+1}) "
          f"y {145+ys.min()}..{145+ys.max()} (h={ys.max()-ys.min()+1})")

print("\n############ 4. GRID LINES (light gray inside white panels) ############")
for nm, x0, x1 in (("LEFT", 98, 463), ("RIGHT", 489, 867)):
    sub = GRID[113:468, x0:x1]
    rowsum = sub.sum(axis=0)
    colsum = sub.sum(axis=1)
    print(f"  {nm} grid rows (gray px > 120): {runs(np.where(colsum > 120)[0] + 113)}")
    print(f"  {nm} grid cols (gray px > 120): {runs(np.where(rowsum > 120)[0] + x0)}")

print("\n############ 5. RED AXES + RESIDUAL ARROW MARKERS ############")
for nm, x0, x1 in (("LEFT", 88, 475), ("RIGHT", 478, 880)):
    sub = RED[105:480, x0:x1]
    ys, xs = np.where(sub)
    colsum = sub.sum(axis=0)
    rowsum = sub.sum(axis=1)
    print(f"  {nm} red bbox x {x0+xs.min()}..{x0+xs.max()} y {105+ys.min()}..{105+ys.max()}")
    print(f"    red cols >100: {runs(np.where(colsum > 100)[0] + x0)}")
    print(f"    red rows >100: {runs(np.where(rowsum > 100)[0] + 105)}")

print("\n############ 6. BLUE FITTED LINE extremes ############")
for nm, x0, x1 in (("LEFT", 98, 463), ("RIGHT", 489, 867)):
    sub = BLU[113:468, x0:x1]
    ys, xs = np.where(sub)
    print(f"  {nm} blue bbox x {x0+xs.min()}..{x0+xs.max()} y {113+ys.min()}..{113+ys.max()}")
    # leftmost and rightmost blue column midpoints
    for xx in (x0 + xs.min(), x0 + (xs.min() + xs.max()) // 2, x0 + xs.max()):
        col = np.where(sub[:, xx - x0])[0]
        if len(col):
            print(f"    x={xx}: y {113+col.min()}..{113+col.max()} mid {(113+col.min()+113+col.max())/2:.1f}")

print("\n############ 7. ORANGE POINT CENTROIDS ############")
for nm, x0, x1 in (("LEFT", 98, 463), ("RIGHT", 489, 867)):
    sub = ORA[113:468, x0:x1]
    lab_n = sub.sum()
    print(f"  {nm} orange px total {lab_n}")
    # simple connected components via scipy-free flood on label grid
    from collections import deque
    seen = np.zeros_like(sub, bool)
    comps = []
    H, W = sub.shape
    for yy in range(H):
        for xx in range(W):
            if sub[yy, xx] and not seen[yy, xx]:
                q = deque([(yy, xx)])
                seen[yy, xx] = True
                pts = []
                while q:
                    cy, cx = q.popleft()
                    pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < H and 0 <= nx < W and sub[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True
                                q.append((ny, nx))
                if len(pts) >= 15:
                    ys = [p[0] for p in pts]
                    xss = [p[1] for p in pts]
                    comps.append((len(pts), x0 + sum(xss) / len(pts), 113 + sum(ys) / len(ys),
                                  x0 + min(xss), x0 + max(xss), 113 + min(ys), 113 + max(ys)))
    comps.sort(key=lambda c: c[1])
    print(f"    {len(comps)} blobs (n>=15):")
    for n, cx, cy, xa, xb, ya, yb in comps:
        print(f"      n={n:4d} centroid ({cx:6.1f},{cy:6.1f}) bbox x{xa}..{xb} y{ya}..{yb} d~{xb-xa+1}")
