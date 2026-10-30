#!/usr/bin/env python3
"""Probe 2 — color-specific extraction on a unique-slide frame.

Usage: probe2_colors.py <frame.jpg> <label>
Reports: orange data-point blobs, blue fitted-line pixels, red-pixel
row/col profiles + clusters, green markers, dark-ink row profile
(text lines), yellow badge region.
"""
from PIL import Image
import sys, collections

img_path, label = sys.argv[1], sys.argv[2]
im = Image.open(img_path).convert("RGB")
W, H = im.size
px = im.load()
print(f"== {label}: {img_path} {im.size}")

# ---------- ORANGE data points ----------
orange = []
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if r > 200 and 90 < g < 190 and b < 90:
            orange.append((x, y))
print(f"orange px: {len(orange)}")
# cluster orange pixels into blobs (grid hashing, 8px cells)
cells = collections.defaultdict(list)
for x, y in orange:
    cells[(x // 8, y // 8)].append((x, y))
blobs = []
for key, pts in cells.items():
    if len(pts) < 6:
        continue
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    blobs.append((min(xs), min(ys), max(xs), max(ys), len(pts)))
# merge blobs whose boxes are within 6px
merged = True
while merged:
    merged = False
    for i in range(len(blobs)):
        for j in range(i + 1, len(blobs)):
            a, b = blobs[i], blobs[j]
            if (a[0] - 6 < b[2] and b[0] - 6 < a[2] and a[1] - 6 < a[3] and b[1] - 6 < a[3]):
                blobs[i] = (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]), a[4] + b[4])
                del blobs[j]; merged = True; break
        if merged:
            break
blobs.sort(key=lambda b: (b[0]))
print("orange blobs (x0,y0,x1,y1,n) -> centroid (cx,cy) size dx dy:")
for b in blobs:
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    print(f"   {b}  c=({cx:.1f},{cy:.1f}) dx={b[2]-b[0]} dy={b[3]-b[1]}")

# ---------- BLUE fitted line ----------
blue = []
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if b > 120 and b - r > 60 and b - g > 60:
            blue.append((x, y))
print(f"blue px: {len(blue)}")
if blue:
    # cluster blue into left/right groups by x<480
    for name, pts in (("left", [p for p in blue if p[0] < 480]), ("right", [p for p in blue if p[0] >= 480])):
        if not pts:
            continue
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        print(f"  {name}: n={len(pts)} xrange={min(xs)}..{max(xs)} yrange={min(ys)}..{max(ys)}")
        # per-column mean to see the line slope
        colx = collections.defaultdict(list)
        for x, y in pts:
            colx[x].append(y)
        ks = sorted(colx)
        sample = ks[::max(1, len(ks) // 12)]
        print("    slope samples:", [(x, round(sum(colx[x]) / len(colx[x]), 1)) for x in sample])

# ---------- RED pixels ----------
red = []
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if r > 120 and r - g > 60 and r - b > 60:
            red.append((x, y))
print(f"red px: {len(red)}")
col = collections.Counter(x for x, y in red)
row = collections.Counter(y for x, y in red)
print("red x-profile peaks (x: n) n>=15:")
for x in sorted(col):
    if col[x] >= 15:
        print(f"   x={x}: {col[x]}")
print("red y-profile peaks (y: n) n>=15:")
for y in sorted(row):
    if row[y] >= 15:
        print(f"   y={y}: {row[y]}")
# red clusters (vertical bands)
print("red x-clusters (contiguous x with >=3 red px):")
xs_sorted = sorted(col)
clusters = []
cur = None
for x in xs_sorted:
    if cur and x - cur[1] <= 3:
        cur[1] = x
    else:
        if cur:
            clusters.append(cur)
        cur = [x, x]
if cur:
    clusters.append(cur)
for a, b in clusters:
    n = sum(col[x] for x in range(a, b + 1))
    if n >= 20:
        print(f"   x {a}..{b}: n={n}")
# horizontal red bands
print("red y-clusters (contiguous y with >=3 red px):")
clusters = []
cur = None
for y in sorted(row):
    if cur and y - cur[1] <= 3:
        cur[1] = y
    else:
        if cur:
            clusters.append(cur)
        cur = [y, y]
if cur:
    clusters.append(cur)
for a, b in clusters:
    n = sum(row[y] for y in range(a, b + 1))
    if n >= 20:
        print(f"   y {a}..{b}: n={n}")

# ---------- GREEN markers ----------
green = []
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if g > 140 and g - r > 60 and g - b > 60:
            green.append((x, y))
print(f"green px: {len(green)}")
if green:
    cells = collections.defaultdict(list)
    for x, y in green:
        cells[(x // 6, y // 6)].append((x, y))
    seen = set()
    for key, pts in sorted(cells.items()):
        if len(pts) < 4:
            continue
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        print(f"   green blob x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} n={len(pts)} c=({sum(xs)/len(xs):.0f},{sum(ys)/len(ys):.0f})")

# ---------- DARK ink (text/borders) ----------
dark = []
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if r < 110 and g < 110 and b < 110:
            dark.append((x, y))
print(f"dark px: {len(dark)}")
drow = collections.Counter(y for x, y in dark)
print("dark y-profile (text lines; y: n) n>=25:")
for y in sorted(drow):
    if drow[y] >= 25:
        print(f"   y={y}: {drow[y]}")
dcol = collections.Counter(x for x, y in dark)
print("dark x-profile peaks (x: n) n>=25:")
for x in sorted(dcol):
    if dcol[x] >= 25:
        print(f"   x={x}: {dcol[x]}")

# ---------- YELLOW badge ----------
yellow = []
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if r > 220 and g > 220 and b < 170:
            yellow.append((x, y))
print(f"yellow px: {len(yellow)}")
if yellow:
    xs = [p[0] for p in yellow]; ys = [p[1] for p in yellow]
    print(f"   yellow bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
