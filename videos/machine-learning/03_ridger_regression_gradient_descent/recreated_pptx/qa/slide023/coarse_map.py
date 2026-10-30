#!/usr/bin/env python3
"""Coarse ASCII classification map of slide_023.jpg + border line detection."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)
H, W = a.shape[:2]

def classify(px):
    r, g, b = px
    mx, mn = max(px), min(px)
    if mx > 247 and mx - mn < 9: return 'W'   # white / near-white pale fills
    if abs(r-g) < 10 and abs(g-b) < 12 and 220 <= r <= 246: return '.'  # gray panel
    if g > r and g >= b and g > 230 and r > 200: return 'G'   # green fill
    if r > g and g > b and r > 240 and b < 235: return 'Y'    # yellow fill
    if b > r and b > g: return 'B'    # blueish
    if r > 120 and r - g > 80 and r - b > 80: return 'R'  # red ink
    if mx < 120: return '#'  # dark ink
    if mx - mn > 25 and r > g and g > b: return 'y'
    return '?'

# sample every 6px, majority class in 6x6 cell
rows = []
for y in range(0, H, 6):
    line = []
    for x in range(0, W, 6):
        cell = a[y:y+6, x:x+6].reshape(-1, 3)
        c = Counter(classify(p) for p in cell).most_common(1)[0][0]
        line.append(c)
    rows.append(''.join(line))
print("ASCII map (6px/cell; W=white . =gray G=green Y=yellow B=blue R=red #=dark ?=other y=lt-yellow):")
for i, r in enumerate(rows):
    print(f"{i*6:3d} {r}")

# Row-wise: exact dominant colors every 8 rows to find box fill boundaries
print("\nRow dominant colors (x sampled 100..850):")
for y in range(45, 540, 8):
    strip = a[y, 100:850]
    c = Counter(tuple(p) for p in strip).most_common(3)
    print(f"y={y:3d}: " + "  ".join(f"{col}x{n}" for col, n in c))
