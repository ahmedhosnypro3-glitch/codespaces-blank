#!/usr/bin/env python3
"""Precise measurement of slide_028.jpg original — axes, curve, dots.

960x540, 1px = 1pt. Every geometry/colour claim below is measured, not guessed.
"""
import numpy as np
from collections import Counter
from PIL import Image

o = np.asarray(Image.open(
    '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg'
).convert('RGB')).astype(int)
H, W = o.shape[:2]

def hexc(c): return '#%02X%02X%02X' % tuple(int(round(v)) for v in c)

# ---------- background map ----------
panel = (np.abs(o[:, :, 0] - 233) < 14) & (np.abs(o[:, :, 1] - 233) < 14) & (np.abs(o[:, :, 2] - 231) < 16)
white = (o[:, :, 0] > 240) & (o[:, :, 1] > 240) & (o[:, :, 2] > 240)
print("=== BACKGROUND MAP ===")
print("  gray E9E9E7 px:", panel.sum(), " white px:", white.sum())
# where is the white region?  (the inner chart area is white, the outer band is gray)
ys, xs = np.where(white)
print("  white bbox x%d-%d y%d-%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
# per-row white count to find the boundary
for y in range(40, 545, 40):
    print(f"    row y={y}: gray={panel[y].sum():4d} white={white[y].sum():4d}")

# ---------- vertical axis strokes ----------
print("\n=== VERTICAL AXIS STROKES (dark ink columns inside chart area) ===")
darkish = (o.sum(axis=2) < 500)
for x in range(85, 200):
    col = darkish[:, x]
    ys = np.where(col[130:508])[0]
    if len(ys) > 60:
        c = Counter(tuple(p) for p in o[130:508, x][col[130:508]])
        print(f"  x={x}: n={len(ys)} y{ys.min()+130}-{ys.max()+130} top={c.most_common(2)}")
print("  --- right panel ---")
for x in range(468, 560):
    col = darkish[:, x]
    ys = np.where(col[130:508])[0]
    if len(ys) > 60:
        c = Counter(tuple(p) for p in o[130:508, x][col[130:508]])
        print(f"  x={x}: n={len(ys)} y{ys.min()+130}-{ys.max()+130} top={c.most_common(2)}")

# ---------- horizontal axis strokes ----------
print("\n=== HORIZONTAL AXIS STROKES (dark ink rows) ===")
for y in range(420, 512):
    row = darkish[y]
    xs = np.where(row[85:900])[0] + 85
    if len(xs) > 60:
        c = Counter(tuple(p) for p in o[y, 85:900][row[85:900]])
        print(f"  y={y}: n={len(xs)} x{xs.min()}-{xs.max()} top={c.most_common(2)}")

# ---------- red mask: which axes are red ----------
print("\n=== RED MASK (r>150, g<110, b<110) inside chart ===")
red = (o[:, :, 0] > 150) & (o[:, :, 1] < 110) & (o[:, :, 2] < 110)
rm = red.copy(); rm[:115, :] = False; rm[515:, :] = False
rm[:, :95] = False; rm[:, 885:] = False
ys, xs = np.where(rm)
print(f"  red px={len(ys)} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}")
# column histogram
colsum = rm.sum(axis=0)
print("  cols with >=20 red px:", [(x, int(colsum[x])) for x in np.where(colsum >= 20)[0]])
rowsum = rm.sum(axis=1)
print("  rows with >=20 red px:", [(y, int(rowsum[y])) for y in np.where(rowsum >= 20)[0]])

# ---------- dark-blue (1F4E79 / 1B1263) mask ----------
print("\n=== DARK-BLUE SHAFT MASK ===")
db = (np.abs(o[:, :, 0] - 31) < 40) & (np.abs(o[:, :, 1] - 78) < 40) & (np.abs(o[:, :, 2] - 121) < 45)
dm = db.copy(); dm[:115, :] = False; dm[515:, :] = False
ys, xs = np.where(dm)
print(f"  px={len(ys)} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}")
colsum = dm.sum(axis=0)
print("  cols with >=40 db px:", [(x, int(colsum[x])) for x in np.where(colsum >= 40)[0]])
rowsum = dm.sum(axis=1)
print("  rows with >=40 db px:", [(y, int(rowsum[y])) for y in np.where(rowsum >= 40)[0]])
