#!/usr/bin/env python3
"""Column ink-profile of a region: shows where glyphs start/end and their colour."""
import sys
import numpy as np
from PIL import Image

path = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_023.jpg"
a = np.asarray(Image.open(path).convert("RGB")).astype(int)

x0, y0, x1, y1 = (int(v) for v in sys.argv[1:5])
reg = a[y0:y1, x0:x1]
r, g, b = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
mx = reg.max(axis=2)

ink = mx < 210
red = ink & (r - g > 40) & (r - b > 40)
green = ink & (g - r > 30) & (g - b > 30)
blue = ink & (b - r > 55) & (b - g > 55)
black = ink & ~red & ~green & ~blue

print(f"region x{x0}-{x1} y{y0}-{y1}")
cols = np.where(ink.any(axis=0))[0]
if len(cols) == 0:
    print("  (no ink)")
    sys.exit()

runs = []
start = cols[0]
prev = cols[0]
for c in cols[1:]:
    if c - prev > 3:
        runs.append((start, prev))
        start = c
    prev = c
runs.append((start, prev))

for s, e in runs:
    seg = slice(s, e + 1)
    tags = []
    for name, m in (("R", red), ("G", green), ("B", blue), ("K", black)):
        n = int(m[:, seg].sum())
        if n:
            tags.append(f"{name}:{n}")
    ys = np.where(ink[:, seg].any(axis=1))[0]
    print(f"  x {x0+s:4d}-{x0+e:4d} (w={e-s+1:3d})  y {y0+ys[0]:3d}-{y0+ys[-1]:3d}  {' '.join(tags)}")
