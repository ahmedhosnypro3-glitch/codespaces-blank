#!/usr/bin/env python3
"""ASCII map + precise structure of the logo region (x585..905, y455..535)."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)

x0, x1, y0, y1 = 585, 905, 455, 535
seg = IM[y0:y1, x0:x1]

# classify each pixel
def classify(px):
    r, g, b = px
    if g > 100 and b > 100 and r < 130 and abs(g - b) < 60:
        return 'T'  # teal
    if r > 200 and g > 200 and b > 200 and abs(r - g) < 25 and abs(g - b) < 30 and not (r > 244 and g > 244 and b > 244):
        return 'c'  # light cyan (white text AA on teal)
    if r > 244 and g > 244 and b > 244:
        return '.'  # white
    if r < 95 and g < 95 and b < 95:
        return '#'  # dark text
    if 140 < r < 235 and 80 < g < 190 and b > 105 and r >= b - 5:
        return 'P'  # pink/mauve
    if abs(r - 231) < 12 and abs(g - 233) < 12 and abs(b - 230) < 14:
        return ' '  # gray panel bg
    return '?'

# downsample 3x3 by center-pixel classification
print("Legend: T=teal  c=cyan-wash(text on teal)  .=white  #=dark  P=mauve  ' '=panel  ?=other")
print("        cols are x; each char = 3px, starting x585. Rows: each line = 2px starting y455.")
for yy in range(0, y1 - y0, 2):
    line = []
    for xx in range(0, x1 - x0, 3):
        px = seg[yy + 1, xx + 1]
        line.append(classify(px))
    print(f"{y0+yy:3d} {''.join(line)}")
print("     " + ''.join(str((x0 + i) // 100 % 10) for i in range(0, x1 - x0, 3)))
print("     " + ''.join(str((x0 + i) // 10 % 10) for i in range(0, x1 - x0, 3)))

print("\n=== mauve/pink cluster extent ===")
sub = IM[455:535, 585:905]
m = (sub[:, :, 0] > 140) & (sub[:, :, 0] < 235) & (sub[:, :, 1] > 80) & (sub[:, :, 1] < 190) & (sub[:, :, 2] > 105) & (sub[:, :, 0] >= sub[:, :, 2] - 5)
ys, xs = np.where(m)
if len(ys):
    print(f"mauve n={len(ys)}, bbox x {585+xs.min()}..{585+xs.max()}, y {455+ys.min()}..{455+ys.max()}")
    rows = np.where(m.any(axis=1))[0]
    bands = []
    s = p = rows[0]
    for y in rows[1:]:
        if y - p > 2:
            bands.append((s, p)); s = y
        p = y
    bands.append((s, p))
    for a, z in bands:
        xs2 = np.where(m[a:z + 1].any(axis=0))[0]
        print(f"  mauve band y {455+a}..{455+z}, x {585+xs2.min()}..{585+xs2.max()}, n={m[a:z+1].sum()}")
    print("  colors:", Counter(map(tuple, sub[m] // 24 * 24)).most_common(5))

print("\n=== cyan-wash text bands in teal panel (gap>0 split) ===")
sub2 = IM[460:532, 594:676]
cy = (sub2[:, :, 0] > 110) & (sub2[:, :, 0] < 235) & (sub2[:, :, 1] > 195) & (sub2[:, :, 2] > 195)
rows = np.where(cy.any(axis=1))[0]
if len(rows):
    bands = []
    s = p = rows[0]
    for y in rows[1:]:
        if y - p > 1:
            bands.append((s, p)); s = y
        p = y
    bands.append((s, p))
    for a, z in bands:
        xs2 = np.where(cy[a:z + 1].any(axis=0))[0]
        if z - a >= 0 and (a, z) not in [(b[0], b[1]) for b in bands[:bands.index((a, z))]]:
            pass
        print(f"  cyan band y {460+a}..{460+z} (h={z-a+1}), x {594+xs2.min()}..{594+xs2.max()}, n={cy[a:z+1].sum()}")

print("\n=== dark text lines in white panel (gap>0) ===")
sub3 = IM[455:535, 676:890]
dk = (sub3[:, :, 0] < 95) & (sub3[:, :, 1] < 95) & (sub3[:, :, 2] < 110)
rows = np.where(dk.any(axis=1))[0]
if len(rows):
    bands = []
    s = p = rows[0]
    for y in rows[1:]:
        if y - p > 1:
            bands.append((s, p)); s = y
        p = y
    bands.append((s, p))
    for a, z in bands:
        xs2 = np.where(dk[a:z + 1].any(axis=0))[0]
        print(f"  dark band y {455+a}..{455+z} (h={z-a+1}), x {676+xs2.min()}..{676+xs2.max()}, n={dk[a:z+1].sum()}")

print("\n=== vertical profile: white panel left/right edges per row ===")
for yy in (462, 470, 480, 490, 500, 510, 520, 527):
    row = IM[yy]
    wl = None
    wr = None
    for x in range(660, 900):
        if row[x][0] > 240 and row[x][1] > 240 and row[x][2] > 238:
            if wl is None:
                wl = x
            wr = x
    tl = None
    tr = None
    for x in range(590, 700):
        if row[x][1] > 100 and row[x][2] > 100 and row[x][0] < 130:
            if tl is None:
                tl = x
            tr = x
    print(f"y={yy}: teal {tl}..{tr}, white {wl}..{wr}")
