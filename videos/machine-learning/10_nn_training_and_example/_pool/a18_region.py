#!/usr/bin/env python3
"""ASCII color map of an arbitrary crop region of a slide frame.

Usage: python3 a18_region.py <slide#> <x0> <y0> <x1> <y1> [cellpx]
"""
import sys
from PIL import Image
import numpy as np

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
n = int(sys.argv[1])
x0, y0, x1, y1 = [int(v) for v in sys.argv[2:6]]
cell = int(sys.argv[6]) if len(sys.argv) > 6 else 10
img = Image.open(f"{BASE}/slide_{n:03d}.jpg").convert("RGB").crop((x0, y0, x1, y1))
w, h = img.size
cols = max(1, w // cell)
rows = max(1, h // cell)
small = img.resize((cols, rows), Image.LANCZOS)
a = np.asarray(small).astype(int)


def cls(px):
    r, g, b = px
    if r > 230 and g > 225 and b < 175: return "Y"
    if r > 140 and r - g > 55 and r - b > 55: return "R"
    if b > 135 and b - r > 45 and b - g > 25: return "B"
    if r > 190 and 70 < g < 175 and b < 120: return "O"
    if g > 130 and r < 150 and b < 150 and g - r > 30: return "G"
    if (r + g + b) / 3 < 95: return "#"
    if abs(r - g) < 14 and abs(g - b) < 14 and 175 < (r + g + b) / 3 < 205: return "g"
    if (r + g + b) / 3 > 222: return "."
    return " "


print(f"slide {n} region x {x0}..{x1} y {y0}..{y1}  cell={cell}px  cols={cols} rows={rows}")
print("     " + "".join(str(((x0 + c * cell) // 10) % 10) if (x0 + c * cell) % 10 < cell else " "
                       for c in range(cols)))
for row in range(rows):
    line = "".join(cls(a[row, c]) for c in range(cols))
    print(f"{y0 + row * cell:4d}  {line}")
