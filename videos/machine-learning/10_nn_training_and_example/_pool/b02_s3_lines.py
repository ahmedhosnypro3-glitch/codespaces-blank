#!/usr/bin/env python3
"""Line-ink profile between input dots and first Sigma column, slide 3 original."""
import sys
from PIL import Image

im = Image.open(sys.argv[1]).convert("RGB")
W, H = im.size
px = im.load()
sc = W / 960.0

def dark(c):
    return max(c) < 225

# For each row y in [140,360], count ink pixels in x[90,190] (between dots and col1)
print("row : inkcount in x[90,190]")
rows = []
for y in range(int(140 * H / 540), int(360 * H / 540)):
    n = sum(1 for x in range(int(90 * sc), int(190 * sc)) if dark(px[x, y]))
    rows.append((round(y * 540 / H), n))
for yy, n in rows:
    if n >= 2:
        print(f"  y={yy:3d} n={n}")
