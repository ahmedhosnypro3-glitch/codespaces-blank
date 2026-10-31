#!/usr/bin/env python3
"""PIL measurement of unique_slides/slide_019.jpg (960x540, 1px = 1pt).

Measures: crimson frame, blue panel boxes, plot interior axes/tick ink,
caption boxes, connector arrow, in-panel titles, legend swatch.
"""
import os
from collections import defaultdict

from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
V = os.path.join(ROOT, "videos/machine-learning/09_introduction_to_neural_networks")
IMG = os.path.join(V, "unique_slides/slide_019.jpg")

im = Image.open(IMG).convert("RGB")
W, H = im.size
px = im.load()
print(f"image {W}x{H}")


def close(a, b, tol=18):
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol and abs(a[2] - b[2]) <= tol


def near(c, hexs, tol=18):
    r = int(hexs[0:2], 16); g = int(hexs[2:4], 16); b = int(hexs[4:6], 16)
    return close(c, (r, g, b), tol)


# ---- 1. crimson frame ----
crim = []
for y in range(H):
    for x in range(W):
        c = px[x, y]
        if c[0] > 120 and c[0] < 215 and c[1] < 110 and c[2] < 120 and c[0] - c[1] > 45:
            crim.append((x, y))
if crim:
    xs = [p[0] for p in crim]; ys = [p[1] for p in crim]
    print(f"crimson frame bbox: x {min(xs)}..{max(xs)}  y {min(ys)}..{max(ys)}")

# ---- 2. blue panel borders ----
def blue_hit(c):
    return c[2] > 120 and c[2] - c[0] > 55 and c[2] - c[1] > 55 and c[0] < 120


blue = defaultdict(list)
for y in range(H):
    for x in range(W):
        if blue_hit(px[x, y]):
            blue[y].append(x)

rows = sorted(blue)
# group contiguous y bands with blue pixels
bands = []
cur = [rows[0]]
for y in rows[1:]:
    if y - cur[-1] <= 2:
        cur.append(y)
    else:
        bands.append(cur); cur = [y]
bands.append(cur)
panels = []
for b in bands:
    xs = [x for y in b for x in blue[y]]
    panels.append((min(xs), b[0], max(xs), b[-1]))
    print(f"blue band y {b[0]}..{b[-1]}  x {min(xs)}..{max(xs)}")

# ---- 3. classify blue runs into columns (vertical borders) ----
print("\n-- vertical blue border columns (top band) --")
for pi, (x0, y0, x1, y1) in enumerate(panels):
    cols = defaultdict(int)
    for y in range(y0, y1 + 1):
        for x in (x0, x1):
            if blue_hit(px[x, y]):
                cols[x] += 1
    print(f"panel#{pi} y{y0}-{y1}: strong cols {[(x, n) for x, n in cols.items() if n > (y1-y0)*0.5]}")

# ---- 4. peach / gray caption boxes ----
print("\n-- peach boxes --")
peach = []
for y in range(H):
    for x in range(W):
        if near(px[x, y], "FCE4D6", 14) or near(px[x, y], "FDE8E2", 14):
            peach.append((x, y))
if peach:
    ys = defaultdict(list)
    for x, y in peach:
        ys[y].append(x)
    yy = sorted(ys)
    grp = [yy[0]]
    for y in yy[1:]:
        if y - grp[-1] <= 3:
            grp.append(y)
        else:
            xs = [x for t in grp for x in ys[t]]
            print(f"  peach band y {grp[0]}..{grp[-1]} x {min(xs)}..{max(xs)}")
            grp = [y]
    xs = [x for t in grp for x in ys[t]]
    print(f"  peach band y {grp[0]}..{grp[-1]} x {min(xs)}..{max(xs)}")

print("-- gray caption boxes (light gray fill) --")
grayfill = []
for y in range(H):
    for x in range(W):
        if near(px[x, y], "DCDCDC", 10):
            grayfill.append((x, y))
if grayfill:
    ys = defaultdict(list)
    for x, y in grayfill:
        ys[y].append(x)
    yy = sorted(ys)
    grp = [yy[0]]
    for y in yy[1:]:
        if y - grp[-1] <= 3:
            grp.append(y)
        else:
            xs = [x for t in grp for x in ys[t]]
            if len(xs) > 400:
                print(f"  gray band y {grp[0]}..{grp[-1]} x {min(xs)}..{max(xs)}")
            grp = [y]
    xs = [x for t in grp for x in ys[t]]
    if len(xs) > 400:
        print(f"  gray band y {grp[0]}..{grp[-1]} x {min(xs)}..{max(xs)}")

# ---- 5. red arrow in the gutter between bottom panels ----
print("\n-- red arrow ink (gutter x 386..470) --")
reds = []
for y in range(H):
    for x in range(380, 475):
        c = px[x, y]
        if c[0] > 150 and c[1] < 110 and c[2] < 110 and c[0] - c[1] > 70:
            reds.append((x, y, c))
if reds:
    xs = [p[0] for p in reds]; ys = [p[1] for p in reds]
    print(f"  red ink bbox x {min(xs)}..{max(xs)} y {min(ys)}..{max(ys)}  n={len(reds)}")
    # row histogram
    rh = defaultdict(int)
    for x, y, c in reds:
        rh[y] += 1
    for y in sorted(rh):
        if rh[y] >= 2:
            row = [x for x, yy, c in reds if yy == y]
            print(f"   y={y}: n={rh[y]} x {min(row)}..{max(row)}")

print("\n-- all red-ish ink in whole frame (arrow + frame) --")
print("done")
