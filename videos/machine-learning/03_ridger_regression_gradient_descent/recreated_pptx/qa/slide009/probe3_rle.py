#!/usr/bin/env python3
"""Probe 3: RLE color dumps of key rows/columns + refined light-blue box."""
import numpy as np
from PIL import Image
from collections import Counter

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = a.shape[:2]

def rle_row(y, x0=0, x1=W, maxlen=200):
    row = a[y, x0:x1]
    out = []
    s = 0
    for i in range(1, len(row)):
        if not np.array_equal(row[i], row[s]):
            out.append((x0 + s, x0 + i - 1, tuple(int(v) for v in row[s])))
            s = i
    out.append((x0 + s, x1 - 1, tuple(int(v) for v in row[s])))
    print(f"  ROW y={y} ({len(out)} runs):")
    for r in out:
        print(f"    x {r[0]:4d}..{r[1]:4d}  ({r[1]-r[0]+1:3d})  {r[2]}")

def rle_col(x, y0=0, y1=H):
    col = a[y0:y1, x]
    out = []
    s = 0
    for i in range(1, len(col)):
        if not np.array_equal(col[i], col[s]):
            out.append((y0 + s, y0 + i - 1, tuple(int(v) for v in col[s])))
            s = i
    out.append((y0 + s, y1 - 1, tuple(int(v) for v in col[s])))
    print(f"  COL x={x} ({len(out)} runs):")
    for r in out:
        print(f"    y {r[0]:4d}..{r[1]:4d}  ({r[1]-r[0]+1:3d})  {r[2]}")

print("=== ROW DUMPS (x 0..959) ===")
for y in (46, 60, 100, 106, 108, 110, 120, 141, 160, 168, 170, 175, 180, 200,
          240, 300, 340, 380, 420, 433, 434, 436, 470, 478, 488, 490, 500, 510,
          519, 521, 530, 537, 538):
    rle_row(y)

print("\n=== COLUMN DUMPS (y 0..539) ===")
for x in (58, 100, 127, 150, 200, 250, 300, 350, 400, 440, 448, 484, 540, 600,
          650, 700, 750, 800, 850, 876, 901):
    rle_col(x)

print("\n=== STRONG light-blue mask (b-r>20, b>230) ===")
lb = (a[:, :, 2] - a[:, :, 0] > 20) & (a[:, :, 2] > 230)
print("  total:", int(lb.sum()))
pys, pxs = np.where(lb)
if len(pys):
    print(f"  bbox x {pxs.min()}..{pxs.max()} y {pys.min()}..{pys.max()}")
# histogram of rows
rh = lb.sum(axis=1)
print("  rows with >20 lb px:", [(y, int(rh[y])) for y in range(H) if rh[y] > 20])
# split into the two boxes by column gap
colsum = lb.sum(axis=0)
nz = np.where(colsum > 0)[0]
# find column gap
gaps = []
prev = None
for v in nz:
    if prev is not None and v > prev + 1:
        gaps.append((prev, v))
    prev = v
print("  column gaps:", gaps)

print("\n=== Distinct colors inside x 90..430, y 100..190 (annotation region L) ===")
sub = a[100:190, 90:430].reshape(-1, 3)
c = Counter(map(tuple, sub))
for col, n in c.most_common(15):
    print(f"  {col} n={n}")

print("\n=== Distinct colors inside x 560..860, y 100..190 (annotation region R) ===")
sub = a[100:190, 560:860].reshape(-1, 3)
c = Counter(map(tuple, sub))
for col, n in c.most_common(15):
    print(f"  {col} n={n}")

print("\n=== caption band colors (y 485..522) ===")
for nm, x0, x1 in (("L", 60, 460), ("R", 500, 900)):
    sub = a[485:522, x0:x1].reshape(-1, 3)
    c = Counter(map(tuple, sub))
    print(f"  {nm} x{x0}..{x1}:")
    for col, n in c.most_common(12):
        print(f"    {col} n={n}")
