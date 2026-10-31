#!/usr/bin/env python3
"""Full dark-ink band map of original slide_031: text/label regions in inches."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
O = np.array(Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
H, W = O.shape[:2]
PPI = W / 13.33
def inch(v): return round(v / PPI, 3)

G = O.mean(axis=2)
ink = G < 100  # dark ink

# Column profile of the whole slide, to find the diagram panel borders
cols = ink.sum(axis=0)
print("=== dark-ink column runs with >=8 px (slide-wide) ===")
runs, inrun = [], False
for x, c in enumerate(cols):
    if c >= 8 and not inrun: s = x; inrun = True
    elif c < 8 and inrun:
        runs.append((s, x - 1)); inrun = False
if inrun: runs.append((s, len(cols) - 1))
for a, b in runs: print(f"  x {a}-{b}  ({inch(a)}-{inch(b)}in)  n={int(cols[a:b+1].sum())}")

print("\n=== dark-ink row runs with >=8 px ===")
rows = ink.sum(axis=1)
runs, inrun = [], False
for y, c in enumerate(rows):
    if c >= 8 and not inrun: s = y; inrun = True
    elif c < 8 and inrun:
        runs.append((s, y - 1)); inrun = False
if inrun: runs.append((s, len(rows) - 1))
for a, b in runs: print(f"  y {a}-{b}  ({inch(a)}-{inch(b)}in)  n={int(rows[a:b+1].sum())}")

print("\n=== ink bbox per row-band, 12-px granularity (regions) ===")
step = 8
y = 0
while y < H:
    band = ink[y:y + step]
    n = band.sum()
    if n > 0:
        xs = np.where(band.any(axis=0))[0]
        print(f"  y {y:3d}-{y+step:3d} ({inch(y)}-{inch(y+step)}in)  x {xs.min():3d}-{xs.max():3d}"
              f" ({inch(xs.min())}-{inch(xs.max())}in)  n={n}")
    y += step
