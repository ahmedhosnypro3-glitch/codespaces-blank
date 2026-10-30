#!/usr/bin/env python3
"""Precise box-edge and border measurement for all three content boxes."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

print("== BLUE box border (violet ~ (186,180,224)) ==")
violet = (B > R + 15) & (B > 180) & (R > 120) & (R < 230) & (G > 120) & (G < 230)
for y in list(range(225, 236)) + list(range(416, 436)):
    xs = np.where(violet[y, :])[0]
    if len(xs):
        print(f" y={y}: x {xs.min()}..{xs.max()} n={len(xs)} runs:" , end=' ')
        # compress
        rr = []
        for x in xs:
            if rr and x == rr[-1][1] + 1: rr[-1][1] = x
            else: rr.append([x, x])
        print(rr[:6])
print("\ncolumn violet count (y232..420), borders:")
colc = violet[232:420, :].sum(axis=0)
for x in range(80, 100):
    if colc[x]: print(f"  x={x}: {colc[x]}")
for x in range(860, 880):
    if colc[x]: print(f"  x={x}: {colc[x]}")

print("\n== border core colors ==")
print(" blue top y228 x300..600:", Counter(tuple(p) for p in a[228, 300:600]).most_common(2))
print(" blue left x88 y300..400:", Counter(tuple(p) for p in a[300:400, 88]).most_common(2))
print(" blue right x867..869 y300..400:", Counter(tuple(p) for p in a[300:400, 867:870].reshape(-1,3)).most_common(3))

print("\n== GREEN box edges ==")
print(" green top rows 104..112 at x400..700:", [ (y, Counter(tuple(p) for p in a[y, 400:700]).most_common(1)[0][0]) for y in range(104, 113) ])
print(" green bottom rows 216..226 at x400..700:", [ (y, Counter(tuple(p) for p in a[y, 400:700]).most_common(1)[0][0]) for y in range(216, 227) ])
print(" green left cols 90..100 at y160..170:", [ (x, Counter(tuple(p) for p in a[160:170, x]).most_common(1)[0][0]) for x in range(90, 101) ])
print(" green right cols 750..762 at y160..170:", [ (x, Counter(tuple(p) for p in a[160:170, x]).most_common(1)[0][0]) for x in range(750, 763) ])
print(" green fill modal (y150..200 x600..740):", Counter(tuple(p) for p in a[150:200, 600:740].reshape(-1,3)).most_common(3))

print("\n== SOLUTION box edges ==")
print(" sol top rows 432..442 at x300..600:", [ (y, Counter(tuple(p) for p in a[y, 300:600]).most_common(1)[0][0]) for y in range(432, 443) ])
print(" sol bottom rows 525..536 at x300..600:", [ (y, Counter(tuple(p) for p in a[y, 300:600]).most_common(1)[0][0]) for y in range(525, 537) ])
print(" sol left cols 84..95 at y470..500:", [ (x, Counter(tuple(p) for p in a[470:500, x]).most_common(1)[0][0]) for x in range(84, 96) ])
print(" sol right cols 868..880 at y470..500:", [ (x, Counter(tuple(p) for p in a[470:500, x]).most_common(1)[0][0]) for x in range(868, 881) ])

print("\n== corner checks (rounded?) ==")
# green box top-left corner: green fill presence per row near corner
gm = (G > 240) & (G > R + 15)
for y in range(105, 120):
    xs = np.where(gm[y, 90:130])[0]
    print(f" green corner y={y}: leftmost green x={90+xs.min() if len(xs) else None}")
# solution box top-left: yellow fill presence per row
ym = (R > 240) & (G > 240) & (B < 235) & (G > B + 15)
for y in range(433, 448):
    xs = np.where(ym[y, 80:130])[0]
    print(f" sol corner y={y}: leftmost yellow x={80+xs.min() if len(xs) else None}")
