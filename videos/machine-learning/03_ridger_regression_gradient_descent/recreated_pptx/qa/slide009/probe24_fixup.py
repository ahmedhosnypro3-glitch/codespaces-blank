#!/usr/bin/env python3
"""Probe 24: FIX-UP of probe 23's failed predicates.
  * BLK must exclude saturated red/blue (their channel sum is also < 430)
  * ORANGE: relax to catch JPEG-softened orange points
  * GRID: sample the true grid-line color first, then threshold on it
"""
import numpy as np
from PIL import Image
from collections import deque

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
SAT = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)


def runs(vals):
    out = []
    for v in vals:
        if out and v - out[-1][1] <= 2:
            out[-1][1] = v
        else:
            out.append([v, v])
    return [(s, e) for s, e in out]


print("############ GRID / ORANGE COLOR SAMPLES ############")
print("  row y=143 x300..320:", [tuple(a[143, x]) for x in (300, 305, 310, 315)])
print("  row y=255 x300..320:", [tuple(a[255, x]) for x in (300, 305, 310, 315)])
print("  row y=120 x300..320:", [tuple(a[120, x]) for x in (300, 305, 310, 315)])
print("  col x=240 y150..160:", [tuple(a[y, 240]) for y in (150, 152, 154, 156, 158)])
print("  col x=240 y200..210:", [tuple(a[y, 240]) for y in (200, 202, 204, 206, 208)])
print("  orange pt ~(176,380):", [tuple(a[378 + dy, 175 + dx]) for dy in (-1, 0, 1) for dx in (-1, 0, 1)])
print("  orange pt ~(260,333):", [tuple(a[331 + dy, 259 + dx]) for dy in (-1, 0, 1) for dx in (-1, 0, 1)])

# --- corrected masks -------------------------------------------------------
ORA = (r > 190) & (g > 120) & (b < 150) & (r - b > 60) & (r - g > 40)
BLK = ((r + g + b) < 450) & (SAT <= 45)
GRID = (SAT <= 16) & (r >= 180) & (r < 246)

print("\n############ ORANGE POINT BLOBS ############")
for nm, x0, x1 in (("LEFT", 98, 463), ("RIGHT", 489, 867)):
    sub = ORA[113:468, x0:x1]
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
                if len(pts) >= 12:
                    ys = [p[0] for p in pts]
                    xss = [p[1] for p in pts]
                    comps.append((len(pts), x0 + sum(xss) / len(pts), 113 + sum(ys) / len(ys),
                                  x0 + min(xss), x0 + max(xss), 113 + min(ys), 113 + max(ys)))
    comps.sort(key=lambda c: c[1])
    print(f"  {nm}: {len(comps)} blobs (orange px {sub.sum()})")
    for n, cx, cy, xa, xb, ya, yb in comps:
        print(f"    n={n:4d} c=({cx:6.1f},{cy:6.1f}) bbox x{xa}..{xb} y{ya}..{yb} d~{xb-xa+1}x{yb-ya+1}")

print("\n############ GRID LINES (gray, achromatic, 180..246) ############")
for nm, x0, x1 in (("LEFT", 98, 463), ("RIGHT", 489, 867)):
    sub = GRID[113:468, x0:x1]
    rowsum = sub.sum(axis=0)
    colsum = sub.sum(axis=1)
    print(f"  {nm} grid ROWS (gray px > 100): {runs(np.where(colsum > 100)[0] + 113)}")
    print(f"  {nm} grid COLS (gray px > 100): {runs(np.where(rowsum > 100)[0] + x0)}")

print("\n############ EQUATION / mm LABEL TEXT (achromatic black) ############")
for nm, x0, x1, y0, y1 in (
        ("LEQ", 140, 462, 148, 172), ("REQ", 510, 866, 148, 172),
        ("LMM", 160, 260, 145, 172), ("RMM", 495, 605, 145, 172)):
    sub = BLK[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(sub)
    if not len(ys):
        print(f"  {nm}: <none>")
        continue
    print(f"  {nm}: x {x0+xs.min()}..{x0+xs.max()} (w={xs.max()-xs.min()+1}) "
          f"y {y0+ys.min()}..{y0+ys.max()} (h={ys.max()-ys.min()+1})")
    colsum = sub.sum(axis=0)
    print(f"      col runs (>=3): {runs(np.where(colsum >= 3)[0] + x0)}")
