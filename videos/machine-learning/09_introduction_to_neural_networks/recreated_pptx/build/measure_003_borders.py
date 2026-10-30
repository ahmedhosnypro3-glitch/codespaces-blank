#!/usr/bin/env python3
"""Detect panel border rectangles + text-line segmentation for slide_003.jpg."""
from PIL import Image
import collections

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_003.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
px = im.load()

def is_red(c):
    r, g, b = c
    return r > 110 and r - g > 45 and r - b > 35

# ---- long horizontal red runs (candidate panel top/bottom borders) ----
print("=== HORIZONTAL RED RUNS (len>=300) ===")
hlines = []
for y in range(H):
    x = 0
    while x < W:
        if is_red(px[x, y]):
            sx = x
            while x < W and is_red(px[x, y]):
                x += 1
            if x - sx >= 300:
                hlines.append((y, sx, x - 1, x - sx))
        else:
            x += 1
for h in hlines:
    print(f"  y={h[0]:4d} x={h[1]:4d}..{h[2]:4d} len={h[3]}")

print("\n=== VERTICAL RED RUNS (len>=100) ===")
vlines = []
for x in range(W):
    y = 0
    while y < H:
        if is_red(px[x, y]):
            sy = y
            while y < H and is_red(px[x, y]):
                y += 1
            if y - sy >= 100:
                vlines.append((x, sy, y - 1, y - sy))
        else:
            y += 1
for v in vlines:
    print(f"  x={v[0]:4d} y={v[1]:4d}..{v[2]:4d} len={v[3]}")

# ---- yellow badge detection ----
print("\n=== YELLOW PIXEL CLUSTERS (r>200,g>200,b<200) ===")
yel = collections.Counter()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if r > 200 and g > 190 and b < 210 and r - b > 25:
            yel[(x, y)] += 1
if yel:
    xs = [p[0] for p in yel]; ys = [p[1] for p in yel]
    print(f"  count={len(yel)} bbox x={min(xs)}..{max(xs)} y={min(ys)}..{max(ys)}")
    xh = collections.Counter(p[0] for p in yel)
    print("  densest x:", sorted(xh.items(), key=lambda kv: -kv[1])[:6])
    yh = collections.Counter(p[1] for p in yel)
    print("  densest y:", sorted(yh.items(), key=lambda kv: -kv[1])[:6])
else:
    print("  none")

# ---- title ink bbox (red text, top region) ----
print("\n=== TITLE REGION (y<95) ink bbox + red bbox ===")
minx=miny=None; maxx=maxy=None
for y in range(0, 95):
    for x in range(W):
        c = px[x, y]
        if c[0]+c[1]+c[2] < 620 and not is_red(c):
            if minx is None or x<minx: minx=x
            if maxx is None or x>maxx: maxx=x
            if miny is None or y<miny: miny=y
            if maxy is None or y>maxy: maxy=y
print(f"  non-red ink bbox: x={minx}..{maxx} y={miny}..{maxy}")
minx=miny=None; maxx=maxy=None
for y in range(0, 95):
    for x in range(W):
        if is_red(px[x, y]):
            if minx is None or x<minx: minx=x
            if maxx is None or x>maxx: maxx=x
            if miny is None or y<miny: miny=y
            if maxy is None or y>maxy: maxy=y
print(f"  red ink bbox: x={minx}..{maxx} y={miny}..{maxy}")
