#!/usr/bin/env python3
"""Fine blob census: purple blobs in input column + ring colors by row, 960-space."""
import sys
from PIL import Image

im = Image.open(sys.argv[1]).convert("RGB")
W, H = im.size
px = im.load()
sc = W / 960.0

def pred_purple(c):
    r, g, b = c
    return r > 100 and b > 100 and g < r - 35 and g < b - 35

# 1) purple blobs in x[60,145], y[140,360] (960-space), min 12px
seen = set()
out = []
for y in range(int(140 * H / 540), int(360 * H / 540)):
    for x in range(int(60 * sc), int(145 * sc)):
        if (x, y) in seen:
            continue
        if not pred_purple(px[x, y]):
            continue
        stack = [(x, y)]; seen.add((x, y)); comp = []
        while stack:
            a, b = stack.pop(); comp.append((a, b))
            for da, db in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                na, nb = a+da, b+db
                if (na, nb) in seen or na < 0 or nb < 0 or na >= W or nb >= H:
                    continue
                if pred_purple(px[na, nb]):
                    seen.add((na, nb)); stack.append((na, nb))
        if len(comp) >= 12:
            xs = [p[0] for p in comp]; ys = [p[1] for p in comp]
            out.append((len(comp), round(min(xs)/sc), round(max(xs)/sc),
                        round(min(ys)/sc*540/H*540), round(max(ys)/sc*540/H*540)))
print("purple blobs x[60,145] y[140,360]:", sorted(out, key=lambda t: t[3]))

# 2) row profile of colored ring ink across diagram x[150,760]
def ring_pred(c, kind):
    r, g, b = c
    if kind == "red":   return r > 120 and g < 90 and b < 90
    if kind == "blue":  return b > 120 and g < 100 and r < 120
    if kind == "green": return g > 100 and r < 130 and b < 130
for kind in ("red", "blue", "green"):
    rows = []
    for y in range(int(90 * H / 540), int(400 * H / 540)):
        n = sum(1 for x in range(int(150 * sc), int(760 * sc))
                if ring_pred(px[x, y], kind))
        rows.append((round(y * 540 / H), n))
    bands = []
    cur = None
    for yy, n in rows:
        if n >= 4:
            if cur is None:
                cur = [yy, yy, n]
            else:
                cur[1] = yy; cur[2] = max(cur[2], n)
        else:
            if cur:
                bands.append(tuple(cur)); cur = None
    if cur:
        bands.append(tuple(cur))
    print(f"{kind} ring row-bands y[90,400]:", bands)
