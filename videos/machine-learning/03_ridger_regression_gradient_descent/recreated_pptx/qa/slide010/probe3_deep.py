#!/usr/bin/env python3
"""Probe 3 — 2D structure: red/green ASCII maps, connected components,
fitted-line endpoints, targeted color samples, grid/cursor checks.

Usage: probe3_deep.py <frame.jpg> <label>
"""
from PIL import Image
import sys, collections

img_path, label = sys.argv[1], sys.argv[2]
im = Image.open(img_path).convert("RGB")
W, H = im.size
px = im.load()
print(f"== {label}: {img_path} {im.size}")

def is_red(c):
    r, g, b = c
    return r > 120 and r - g > 60 and r - b > 60
def is_green(c):
    r, g, b = c
    return g > 140 and g - r > 60 and g - b > 60
def is_orange(c):
    r, g, b = c
    return r > 200 and 90 < g < 190 and b < 90
def is_navyish(c):
    r, g, b = c
    return b > 120 and b - r > 60 and b - g > 60
def is_dark(c):
    r, g, b = c
    return r < 110 and g < 110 and b < 110
def is_white(c):
    r, g, b = c
    return r > 235 and g > 235 and b > 235

# ---------- targeted color samples ----------
print("\n-- color samples --")
samples = [
    ("left stroke x58-60 @y300", [(58, 300), (59, 300), (60, 300)]),
    ("right stroke x900-903 @y300", [(900, 300), (901, 300), (902, 300), (903, 300)]),
    ("bottom stroke y536-539 @x300", [(300, 536), (300, 537), (300, 538), (300, 539)]),
    ("L panel border x95 @y300", [(94, 300), (95, 300), (96, 300)]),
    ("L panel border x465 @y300", [(464, 300), (465, 300), (466, 300)]),
    ("R panel border x486 @y300", [(485, 300), (486, 300), (487, 300)]),
    ("R panel border x870 @y300", [(869, 300), (870, 300), (871, 300)]),
    ("L panel border y108 @x300", [(300, 107), (300, 108), (300, 109)]),
    ("L panel border y473 @x300", [(300, 472), (300, 473), (300, 474)]),
    ("L interior @ (300,300)", [(300, 300)]),
    ("L eq-box fill (266,161)?", [(266, 161), (260, 150), (270, 170)]),
    ("R eq-box fill (682,161)?", [(682, 161), (676, 150), (686, 170)]),
    ("L band-box fill (264,505)?", [(264, 505), (150, 505), (400, 505)]),
    ("R band-box fill (671,505)?", [(671, 505), (560, 505), (800, 505)]),
    ("bg @ (30,30), (500,520)", [(30, 30), (500, 520)]),
    ("badge center (876,73)", [(876, 73)]),
    ("badge ring (858,73)", [(858, 73), (861, 66)]),
    ("cursor? L bottom center (264,420)", [(264, 420), (270, 415), (258, 425)]),
]
for name, pts in samples:
    vals = [f"{p}={px[p[0], p[1]]}" for p in pts]
    print(f"   {name}: " + ", ".join(vals))

# ---------- red/green ASCII maps (4x4 px cells) over the two panels ----------
def ascii_map(x0, x1, y0, y1, test, ch, title):
    print(f"\n-- {title} (x{x0}..{x1}, y{y0}..{y1}, 4x4 cells) --")
    for cy in range(y0, y1, 4):
        row = []
        for cx in range(x0, x1, 4):
            hit = 0
            for yy in range(cy, cy + 4):
                for xx in range(cx, cx + 4):
                    if test(px[xx, yy]):
                        hit += 1
            row.append(ch if hit else ".")
        print("".join(row))

ascii_map(95, 466, 108, 474, is_red, "R", "LEFT panel RED map")
ascii_map(486, 871, 108, 474, is_red, "R", "RIGHT panel RED map")
ascii_map(95, 466, 108, 474, is_green, "G", "LEFT panel GREEN map")
ascii_map(486, 871, 108, 474, is_green, "G", "RIGHT panel GREEN map")

# ---------- connected components (red, green, navy) ----------
def components(test, min_size=4):
    pix = set()
    for y in range(H):
        for x in range(W):
            if test(px[x, y]):
                pix.add((x, y))
    comps = []
    while pix:
        seed = pix.pop()
        stack = [seed]
        comp = [seed]
        while stack:
            x, y = stack.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n in pix:
                    pix.discard(n)
                    stack.append(n)
                    comp.append(n)
        if len(comp) >= min_size:
            xs = [p[0] for p in comp]; ys = [p[1] for p in comp]
            comps.append((min(xs), min(ys), max(xs), max(ys), len(comp)))
    comps.sort()
    return comps

for name, test in (("RED", is_red), ("GREEN", is_green)):
    comps = components(test)
    print(f"\n-- {name} connected components (n>={4}) : {len(comps)} --")
    for c in comps:
        cx, cy = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2
        print(f"   x{c[0]}..{c[2]} y{c[1]}..{c[3]} n={c[4]} c=({cx:.1f},{cy:.1f}) w={c[2]-c[0]} h={c[3]-c[1]}")

# ---------- fitted blue lines: interior only ----------
print("\n-- blue fitted line (interior, excluding 8px border band) --")
for name, (ix0, ix1) in (("LEFT", (104, 457)), ("RIGHT", (495, 862))):
    pts = []
    for y in range(116, 466):
        for x in range(ix0, ix1):
            if is_navyish(px[x, y]):
                pts.append((x, y))
    if not pts:
        print(f"   {name}: none")
        continue
    # exclude the left/right panel borders: x within ix0..ix1 already; but panel
    # top/bottom borders y108/y473 excluded by range. Cluster columns:
    colx = collections.defaultdict(list)
    for x, y in pts:
        colx[x].append(y)
    xs = sorted(colx)
    print(f"   {name}: n={len(pts)} xrange={xs[0]}..{xs[-1]}")
    # column with most blue = fitted line center; report per-column min/max y
    # for columns where blue count is small (line only, 2pt) vs huge (border)
    linecols = [x for x in xs if 3 <= len(colx[x]) <= 12]
    if linecols:
        print(f"   line-ish columns x{linecols[0]}..{linecols[-1]}")
        for x in linecols[::max(1, len(linecols)//20)]:
            ys = sorted(colx[x])
            print(f"      x={x}: y {ys[0]}..{ys[-1]} n={len(ys)}")
    thick = [x for x in xs if len(colx[x]) > 12]
    if thick:
        print(f"   thick/vertical columns (borders): {thick[:6]}...{thick[-6:] if len(thick)>6 else ''}")

# ---------- grid check (expected 009 grid: col0 103.5 pitch 23; row0 120.5 pitch 22.4) ----------
print("\n-- grid check: sample row y=250 across x for gray-ish vertical lines --")
y = 250
runs = []
cur = None
for x in range(99, 461):
    c = px[x, y]
    gray_line = (abs(c[0] - c[1]) < 12 and abs(c[1] - c[2]) < 12 and 190 < c[0] < 235)
    if gray_line:
        if cur:
            cur[1] = x
        else:
            cur = [x, x]
    else:
        if cur:
            runs.append(tuple(cur))
            cur = None
if cur:
    runs.append(tuple(cur))
print("   gray runs at y=250 (LEFT):", runs)
print("   expected cols:", [round(103.5 + 23 * k) for k in range(16)])

print("\n-- grid check: sample col x=300 across y for gray-ish horizontal lines --")
x = 300
runs = []
cur = None
for y in range(114, 468):
    c = px[x, y]
    gray_line = (abs(c[0] - c[1]) < 12 and abs(c[1] - c[2]) < 12 and 190 < c[0] < 235)
    if gray_line:
        if cur:
            cur[1] = y
        else:
            cur = [y, y]
    else:
        if cur:
            runs.append(tuple(cur))
            cur = None
if cur:
    runs.append(tuple(cur))
print("   gray runs at x=300 (LEFT):", runs)
print("   expected rows:", [round(120.5 + 22.4 * k, 1) for k in range(16)])

# ---------- dark text in captions: x-extent per line ----------
print("\n-- caption text bands --")
for ylo, yhi, name in ((488, 502, "line1 y488-502"), (509, 521, "line2 y509-521")):
    for panel, (xa, xb) in (("L", (60, 470)), ("R", (480, 900))):
        xs = [x for x in range(xa, xb) if any(is_dark(px[x, y]) for y in range(ylo, yhi))]
        reds = [x for x in range(xa, xb) if any(is_red(px[x, y]) for y in range(ylo, yhi))]
        if xs:
            print(f"   {name} {panel}: dark x {min(xs)}..{max(xs)} (n={len(xs)})")
        if reds:
            print(f"   {name} {panel}: RED  x {min(reds)}..{max(reds)} (n={len(reds)})")

# ---------- white cursor check in left panel ----------
print("\n-- white px count in LEFT panel interior (possible cursor) --")
wcnt = 0
wpts = []
for y in range(112, 470):
    for x in range(99, 462):
        if is_white(px[x, y]):
            wcnt += 1
            if len(wpts) < 4000:
                wpts.append((x, y))
print(f"   white px in L interior: {wcnt}")
if wpts:
    xs = [p[0] for p in wpts]; ys = [p[1] for p in wpts]
    print(f"   white bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
    # cluster
    comps = components(is_white, min_size=20)
    for c in comps[:12]:
        print(f"      white comp x{c[0]}..{c[2]} y{c[1]}..{c[3]} n={c[4]}")
