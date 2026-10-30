#!/usr/bin/env python3
"""Detect colored box borders in original slide_031 to get true geometry."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
orig = Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")
O = np.array(orig).astype(int)
H, W = O.shape[:2]
r, g, b = O[...,0], O[...,1], O[...,2]

def bbox(mask, name):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(name, "NONE"); return None
    print(f"{name:16s} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] count={len(xs)}")
    return (xs.min(), ys.min(), xs.max(), ys.max())

# strong blue (000080-ish)
blue = (b > 90) & (b - r > 50) & (b - g > 50)
bbox(blue, "blue-ish")
# navy specifically
navy = (r < 100) & (g < 100) & (b > 80) & (b < 180)
bbox(navy, "navy")
# strong green (008000)
green = (g > 70) & (g - r > 40) & (g - b > 40)
bbox(green, "green-ish")
# strong red
red = (r > 130) & (g < 90) & (b < 90)
bbox(red, "red-ish")

# Row profile of navy to find the two blue box bands
for name, mask in [("navy", navy), ("green", green)]:
    rows = mask.sum(axis=1)
    runs, inrun = [], False
    for y, c in enumerate(rows):
        if c > 3 and not inrun: s=y; inrun=True
        elif c <= 3 and inrun: runs.append((s, y-1)); inrun=False
    if inrun: runs.append((s, H-1))
    print(f"{name} row runs (>3 px):", runs)
    for (y0,y1) in runs:
        sub = mask[y0:y1+1]
        xs = np.where(sub.any(axis=0))[0]
        if len(xs): print(f"   band y[{y0},{y1}] x[{xs.min()},{xs.max()}]")

# Column profile of navy/green for vertical box edges
for name, mask in [("navy", navy), ("green", green)]:
    cols = mask.sum(axis=0)
    runs, inrun = [], False
    for x, c in enumerate(cols):
        if c > 3 and not inrun: s=x; inrun=True
        elif c <= 3 and inrun: runs.append((s, x-1)); inrun=False
    if inrun: runs.append((s, W-1))
    print(f"{name} col runs (>3 px):", runs)
