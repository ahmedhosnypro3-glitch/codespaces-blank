#!/usr/bin/env python3
"""Coarse ASCII color map for a given slide (scope_a18: slides 31, 32)."""
import sys
from PIL import Image
import numpy as np

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
n = int(sys.argv[1])
img = Image.open(f"{BASE}/slide_{n:03d}.jpg").convert("RGB")

small = img.resize((96, 27), Image.LANCZOS)
a = np.asarray(small).astype(int)

def cls(px):
    r, g, b = px
    if r > 230 and g > 225 and b < 175: return "Y"
    if r > 140 and r - g > 55 and r - b > 55: return "R"
    if b > 135 and b - r > 45 and b - g > 25: return "B"
    if r > 190 and 70 < g < 175 and b < 120: return "O"
    if g > 130 and r < 150 and b < 150 and g - r > 30: return "G"
    if (r+g+b)/3 < 95: return "#"
    if abs(r-g) < 14 and abs(g-b) < 14 and 175 < (r+g+b)/3 < 205: return "g"
    if r > 225 and g < 200 and b > 210: return "p"
    if (r+g+b)/3 > 222: return "."
    return " "

print("Legend: #=dark ink R=red B=blue Y=yellow O=orange G=green g=graybox .=white <sp>=bg")
hdr = "     " + "".join(str((i//10) % 10) if i % 10 == 0 else " " for i in range(96))
print(hdr)
for row in range(27):
    line = "".join(cls(a[row, col]) for col in range(96))
    print(f"{row:3d}  {line}   y={row*20}px={row*20/72:.2f}in")
