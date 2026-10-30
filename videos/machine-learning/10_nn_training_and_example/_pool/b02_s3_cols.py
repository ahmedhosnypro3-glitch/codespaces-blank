#!/usr/bin/env python3
"""Column profile of saturated ink (ring pixels) in slide-3 diagram band."""
import sys
from PIL import Image

im = Image.open(sys.argv[1]).convert("RGB")
W, H = im.size
px = im.load()
sc = W / 960.0

def sat(c):
    r, g, b = c
    mx, mn = max(c), min(c)
    return mx - mn > 60 and mx > 100

cols = []
for x in range(int(90 * sc), int(820 * sc)):
    n = sum(1 for y in range(int(140 * H / 540), int(360 * H / 540)) if sat(px[x, y]))
    cols.append((round(x / sc), n))
# print peaks
bands = []
cur = None
for xx, n in cols:
    if n >= 6:
        if cur is None:
            cur = [xx, xx, n]
        else:
            cur[1] = xx; cur[2] = max(cur[2], n)
    else:
        if cur:
            bands.append(tuple(cur)); cur = None
if cur:
    bands.append(tuple(cur))
print("saturated column bands x[90,820] y[140,360] (x0,x1,peak):")
for b in bands:
    print("  ", b)
