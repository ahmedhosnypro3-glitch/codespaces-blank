#!/usr/bin/env python3
"""Fine-grained logo census for slide_001.jpg — settle the logo's true structure:
teal panel contents, white panel edges, text lines, pink/purple elements."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)

print("=== 1. TEAL panel interior (x596..673, y461..529) ===")
seg = IM[461:530, 596:674]
sr, sg, sb = seg[:, :, 0], seg[:, :, 1], seg[:, :, 2]
teal = (sg > 100) & (sb > 100) & (sr < 130) & (abs(sg - sb) < 60)
nont = ~teal
print(f"non-teal px: {nont.sum()} / {seg.shape[0]*seg.shape[1]}")
if nont.sum():
    cnt = Counter(map(tuple, seg[nont] // 16 * 16))
    print("non-teal colors:", cnt.most_common(8))
    ys, xs = np.where(nont)
    print(f"non-teal bbox: x {596+xs.min()}..{596+xs.max()}, y {461+ys.min()}..{461+ys.max()}")
    # rows with non-teal
    rr = np.where(nont.any(axis=1))[0]
    if len(rr):
        bands = []
        s = p = rr[0]
        for y in rr[1:]:
            if y - p > 2:
                bands.append((s, p)); s = y
            p = y
        bands.append((s, p))
        for a, z in bands:
            xs2 = np.where(nont[a:z + 1].any(axis=0))[0]
            print(f"  non-teal band y {461+a}..{461+z}, x {596+xs2.min()}..{596+xs2.max()}, n={nont[a:z+1].sum()}")
    # LIGHT pixels (white-ish text would be >200)
    light = (sr > 200) & (sg > 200) & (sb > 200)
    print(f"light(>200) px inside teal: {light.sum()}")
    if light.sum():
        ys, xs = np.where(light)
        print(f"  light bbox x {596+xs.min()}..{596+xs.max()} y {461+ys.min()}..{461+ys.max()}")
        pxs = seg[light]
        print(f"  light colors: {Counter(map(tuple, pxs//16*16)).most_common(5)}")

print("\n=== 2. WHITE panel edges (rows y462..528) ===")
# scan columns x600..902 at mid-row y495: where does white start/end?
row = IM[495]
for x in range(670, 905):
    if x in (670, 674, 675, 676, 677, 678, 679, 685, 880, 885, 890, 893, 895, 898, 899, 900, 901, 902, 903, 904):
        print(f"  ({x},495) = {tuple(row[x])}")
# vertical profile at x750: where white starts/ends vertically
col = IM[:, 750]
trans = [y for y in range(440, 545) if abs(int(col[y][0]) - 231) + abs(int(col[y][1]) - 233) + abs(int(col[y][2]) - 230) > 60]
print(f"x750 non-panel rows y440..545: {trans[:5]} ... {trans[-5:]}" if trans else "x750 all panel-color")

print("\n=== 3. WHITE panel ALL ink lines (x678..900, y455..535, non-white non-panel) ===")
seg2 = IM[455:536, 678:901]
bgd = np.minimum(np.abs(seg2 - np.array([231, 233, 230])).sum(axis=2),
                 np.abs(seg2 - np.array([255, 255, 255])).sum(axis=2))
ink2 = bgd > 60
rows = np.where(ink2.any(axis=1))[0]
if len(rows):
    bands = []
    s = p = rows[0]
    for y in rows[1:]:
        if y - p > 2:
            bands.append((s, p)); s = y
        p = y
    bands.append((s, p))
    for a, z in bands:
        xs2 = np.where(ink2[a:z + 1].any(axis=0))[0]
        pxs = seg2[a:z + 1][ink2[a:z + 1]]
        cnt = Counter(map(tuple, pxs // 24 * 24))
        print(f"ink line y {455+a}..{455+z} (h={z-a+1}), x {678+xs2.min()}..{678+xs2.max()}: n={ink2[a:z+1].sum()} colors {cnt.most_common(4)}")

print("\n=== 4. PINK/MAUVE clusters 2D (30px grid, logo region x570..910 y425..540) ===")
seg3 = IM[425:541, 570:911]
pink = (seg3[:, :, 0] > 140) & (seg3[:, :, 0] < 235) & (seg3[:, :, 1] > 80) & (seg3[:, :, 1] < 185) & (seg3[:, :, 2] > 110) & (seg3[:, :, 2] < 205) & (seg3[:, :, 0] > seg3[:, :, 2])
ys, xs = np.where(pink)
print(f"pink px: {len(ys)}")
if len(ys):
    grid = Counter(((y // 15) * 15, (x // 20) * 20) for y, x in zip(ys, xs))
    for (gy, gx), n in sorted(grid.items()):
        if n > 30:
            print(f"  y {425+gy}..{425+gy+15}, x {570+gx}..{570+gx+20}: {n}")
    print("top pink colors:", Counter(map(tuple, seg3[pink] // 24 * 24)).most_common(6))

print("\n=== 5. FULL logo color census (x590..905, y455..535, exclude panel/white) ===")
seg4 = IM[455:536, 590:906]
bgd4 = np.minimum(np.abs(seg4 - np.array([231, 233, 230])).sum(axis=2),
                  np.abs(seg4 - np.array([255, 255, 255])).sum(axis=2))
ink4 = bgd4 > 60
pxs = seg4[ink4]
print("ALL non-bg colors in logo:", Counter(map(tuple, pxs // 32 * 32)).most_common(12))

print("\n=== 6. White panel: left/right edge precise scan (row y495, y465, y520) ===")
for yy in (465, 495, 520):
    row = IM[yy]
    edges = []
    prev_white = False
    for x in range(660, 906):
        is_white = row[x][0] > 244 and row[x][1] > 244 and row[x][2] > 244
        if is_white != prev_white:
            edges.append(x)
            prev_white = is_white
    print(f"y={yy}: white<->nonwhite transitions at x {edges}")
