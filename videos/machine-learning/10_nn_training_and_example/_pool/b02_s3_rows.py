#!/usr/bin/env python3
"""Row-profile of purple ink in the input column (x 60..140) of a 960x540 frame."""
import sys
from PIL import Image

im = Image.open(sys.argv[1]).convert("RGB")
W, H = im.size
px = im.load()
x0, x1 = int(60 * W / 960), int(140 * W / 960)
counts = []
for y in range(H):
    n = 0
    for x in range(x0, x1):
        r, g, b = px[x, y]
        if r > 110 and b > 110 and g < r - 40 and g < b - 40:
            n += 1
    counts.append(n)
# group contiguous rows with n>=3 into bands
bands = []
y = 0
while y < H:
    if counts[y] >= 3:
        y2 = y
        while y2 < H and counts[y2] >= 3:
            y2 += 1
        peak = max(counts[y:y2])
        bands.append((y, y2 - 1, peak))
        y = y2
    else:
        y += 1
print("purple bands in x[60,140]:", bands)
