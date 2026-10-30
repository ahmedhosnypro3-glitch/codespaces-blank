#!/usr/bin/env python3
"""Geometry probe of ORIGINAL slide_008: plot rect, red border, bottom bar, title ink, badge."""
import numpy as np
from PIL import Image

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
im = Image.open(ORIG).convert("RGB").resize((960, 540), Image.LANCZOS)
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = a.max(axis=2); mn = a.min(axis=2)

print("=== outer red frame? check 6px inset ring ===")
for yy in [4, 6, 8, 10, 12, 14]:
    row = a[yy, :, :]
    print(f"  y={yy:3d}  x=20:{tuple(row[20])}  x=480:{tuple(row[480])}  x=940:{tuple(row[940])}")
for xx in [4, 6, 8, 10, 12, 14]:
    col = a[:, xx, :]
    print(f"  x={xx:3d}  y=20:{tuple(col[20])}  y=270:{tuple(col[270])}  y=520:{tuple(col[520])}")

print("\n=== black bottom bar ===")
dark = (mx < 60)
rowfrac = dark.mean(axis=1)
for i in range(500, 540):
    print(f"  y={i}  darkfrac={rowfrac[i]:.3f}")
darkrows = np.nonzero(rowfrac > 0.85)[0]
print("  fully-dark rows:", darkrows.min() if len(darkrows) else None, "..", darkrows.max() if len(darkrows) else None)

print("\n=== white plot vs gray background map (row/col profiles) ===")
whiteish = (mn > 245)
grayish = (np.abs(r - g) < 6) & (np.abs(g - b) < 6) & (r > 215) & (r < 245)
for i in range(0, 540, 20):
    print(f"  y={i:3d} white={whiteish[i].mean():.2f} gray={grayish[i].mean():.2f} dark={rowfrac[i]:.2f}")
print("  column profile:")
colw = whiteish.mean(axis=0)
colg = grayish.mean(axis=0)
for i in range(0, 960, 20):
    print(f"  x={i:3d} white={colw[i]:.2f} gray={colg[i]:.2f}")

print("\n=== plot border hunt: rows/cols with pinkish/red tint (r>g,b) ===")
pink = (r > g + 6) & (r > b + 4) & (r > 150)
rp = pink.mean(axis=1)
cp = pink.mean(axis=0)
cand_rows = [(i, round(float(rp[i]), 3)) for i in range(540) if rp[i] > 0.25]
cand_cols = [(i, round(float(cp[i]), 3)) for i in range(960) if cp[i] > 0.25]
print("  rows with >25% pink:", cand_rows[:30])
print("  cols with >25% pink:", cand_cols[:30])

print("\n=== badge (top-right circle) ===")
for x in range(880, 960, 8):
    print(f"  x={x} y=40:{tuple(a[40,x])} y=55:{tuple(a[55,x])}")

print("\n=== title ink rows (y 30..110) ===")
bg = a[95:115, 30:200].reshape(-1, 3).mean(axis=0)
ink = (np.abs(a - bg).sum(axis=2) > 70)
for i in range(25, 115, 5):
    print(f"  y={i:3d} inkfrac={ink[i].mean():.3f}")
