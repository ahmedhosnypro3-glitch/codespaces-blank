#!/usr/bin/env python3
"""Probe 4 — full-resolution classified map of each panel interior.

Char per 2x2 px cell:  R strict red  o orange  B navy/blue  G green
d dark-green #008000-family  # dark ink  . light  : mid-gray
Also: exact run-length structure of the green horizontal line, and a
dark-green census (the analysis claims #008000 projection lines that the
bright-green test misses).
"""
from PIL import Image
import sys, collections

img_path, label = sys.argv[1], sys.argv[2]
im = Image.open(img_path).convert("RGB")
W, H = im.size
px = im.load()
print(f"== {label}: {img_path} {im.size}")

def classify(c):
    r, g, b = c
    if r > 150 and r - g > 70 and r - b > 70 and g < 110:
        return "R"          # strict red (excludes orange: g<110)
    if r > 200 and 90 < g < 190 and b < 90:
        return "o"          # orange
    if b > 110 and b - r > 50 and b - g > 50:
        return "B"          # navy / blue
    if g > 130 and g - r > 60 and g - b > 60:
        return "G"          # bright green
    if g > 80 and g - r > 35 and g - b > 35 and r < 150:
        return "d"          # dark green (#008000 family)
    if r < 100 and g < 100 and b < 100:
        return "#"          # dark ink
    if r < 215 and g < 215 and b < 215:
        return ":"          # mid gray (grid/panel)
    return "."

def panel_map(x0, x1, y0, y1, name):
    print(f"\n-- {name} classified map (x{x0}..{x1} y{y0}..{y1}, 2x2 cells) --")
    hdr1 = "".join(str((x0 + 2 * c) // 100 % 10) for c in range((x1 - x0) // 2))
    hdr2 = "".join(str((x0 + 2 * c) // 10 % 10) for c in range((x1 - x0) // 2))
    print("     " + hdr1)
    print("     " + hdr2)
    for cy in range(0, y1 - y0, 2):
        row = []
        for cx in range(0, x1 - x0, 2):
            # sample the darkest/most-saturated of the 4 px
            best = "."
            for yy in range(y0 + cy, y0 + cy + 2):
                for xx in range(x0 + cx, x0 + cx + 2):
                    ch = classify(px[xx, yy])
                    if ch != ".":
                        best = ch
            row.append(best)
        ylabel = f"{y0 + cy:4d} "
        print(ylabel + "".join(row))

panel_map(99, 462, 112, 470, "LEFT interior")
panel_map(491, 866, 112, 470, "RIGHT interior")

# ---- dark-green census & components ----
def is_dg(c):
    r, g, b = c
    return g > 80 and g - r > 35 and g - b > 35 and r < 150

dg = [(x, y) for y in range(H) for x in range(W) if is_dg(px[x, y])]
print(f"\ndark-green px: {len(dg)}")
if dg:
    rowc = collections.Counter(y for x, y in dg)
    print("dark-green y-profile (y: n) n>=8:")
    for y in sorted(rowc):
        if rowc[y] >= 8:
            print(f"   y={y}: {rowc[y]}")
    colc = collections.Counter(x for x, y in dg)
    print("dark-green x-profile (x: n) n>=8:")
    for x in sorted(colc):
        if colc[x] >= 8:
            print(f"   x={x}: {colc[x]}")

# ---- strict red census (g<110) ----
def is_sr(c):
    r, g, b = c
    return r > 150 and r - g > 70 and r - b > 70 and g < 110
sr = [(x, y) for y in range(H) for x in range(W) if is_sr(px[x, y])]
print(f"\nstrict-red px: {len(sr)}")
if sr:
    rowc = collections.Counter(y for x, y in sr)
    print("strict-red y-profile (y: n) n>=8:")
    for y in sorted(rowc):
        if rowc[y] >= 8:
            print(f"   y={y}: {rowc[y]}")
    colc = collections.Counter(x for x, y in sr)
    print("strict-red x-profile (x: n) n>=8:")
    for x in sorted(colc):
        if colc[x] >= 8:
            print(f"   x={x}: {colc[x]}")

# ---- exact green horizontal line profile (LEFT panel, y230..246) ----
print("\n-- LEFT green line exact profile (x120..350): for each x, green ys --")
for x in range(120, 350, 2):
    ys = [y for y in range(225, 250) if (px[x, y][1] > 80 and px[x, y][1] - px[x, y][0] > 35 and px[x, y][1] - px[x, y][2] > 35 and px[x, y][0] < 150)]
    if ys:
        print(f"   x={x}: y{min(ys)}..{max(ys)} n={len(ys)}")

# ---- core colors of the green pieces ----
print("\n-- green core colors --")
for desc, pts in (
    ("L hline mid (250,238)", [(250, 238), (250, 239), (200, 238), (320, 238)]),
    ("L marker (354,434)", [(354, 434), (353, 433), (356, 435)]),
    ("L bit (352,245)", [(352, 245), (353, 246)]),
    ("L bit (352,389)", [(352, 389), (351, 397)]),
    ("R bit (546,286)", [(546, 286), (547, 287)]),
    ("R bit (766,292)", [(766, 292), (767, 293)]),
    ("R bit (544,209)", [(544, 209), (545, 210)]),
    ("R marker (766,434)", [(766, 434), (765, 433), (769, 435)]),
):
    print(f"   {desc}: " + ", ".join(f"{p}={px[p[0], p[1]]}" for p in pts))
