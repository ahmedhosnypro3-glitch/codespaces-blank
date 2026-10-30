#!/usr/bin/env python3
"""Probe 7: vertical/horizontal color profiles through the annotation boxes."""
import numpy as np
from PIL import Image
from collections import Counter

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = a.shape[:2]

def prof_col(x, y0=95, y1=200):
    print(f"\n=== COLUMN x={x}, y{y0}..{y1} ===")
    prev = None
    for y in range(y0, y1):
        c = tuple(int(v) for v in a[y, x])
        if c != prev:
            print(f"  y={y:4d}  {c}")
            prev = c

def prof_row(y, x0=85, x1=490):
    print(f"\n=== ROW y={y}, x{x0}..{x1} ===")
    prev = None
    for x in range(x0, x1):
        c = tuple(int(v) for v in a[y, x])
        if c != prev:
            print(f"  x={x:4d}  {c}")
            prev = c

for x in (100, 150, 200, 250, 300, 350, 400, 440, 466, 700, 750, 800):
    prof_col(x)

for y in (104, 106, 107, 108, 109, 112, 120, 140, 145, 150, 160, 170, 176,
          178, 180, 182, 185, 190, 460, 465, 468, 470, 472, 475):
    prof_row(y)

print("\n=== histogram of colors in left box interior (x 130..440, y 120..175) ===")
sub = a[120:175, 130:440].reshape(-1, 3)
for c, n in Counter(map(tuple, sub)).most_common(20):
    print(f"  {c} n={n}")

print("\n=== histogram of colors in right box interior (x 500..850, y 120..175) ===")
sub = a[120:175, 500:850].reshape(-1, 3)
for c, n in Counter(map(tuple, sub)).most_common(20):
    print(f"  {c} n={n}")

print("\n=== histogram: left chart panel interior away from box (x 150..430, y 200..420) ===")
sub = a[200:420, 150:430].reshape(-1, 3)
for c, n in Counter(map(tuple, sub)).most_common(12):
    print(f"  {c} n={n}")
