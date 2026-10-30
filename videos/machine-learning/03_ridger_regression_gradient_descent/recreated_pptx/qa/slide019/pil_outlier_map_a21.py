#!/usr/bin/env python3
"""Faint-rule check at build hline positions + ASCII color map of outlier column."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
oi = Image.open(f"{V}/unique_slides/slide_019.jpg").convert("RGB")
oa = np.asarray(oi).astype(int)

print("=== 1. FAINT-RULE CHECK: row means across grid interior (x215..370) ===")
print("orig row-mean rgb (background is panel gray E9E9E7=233 or white 255):")
for y in [224, 225, 226, 227, 228, 246, 247, 248, 249, 250, 251, 252, 253, 268, 269, 270]:
    row = oa[y, 215:370]
    print(f"  y{y}: rgb ({int(row[:,0].mean())},{int(row[:,1].mean())},{int(row[:,2].mean())})  min-sum {int(row.sum(axis=1).min())}")

print("=== 2. ASCII MAP orig outlier col x80..120, y195..300 (2px cols, 1px rows) ===")
# classify each 1x2 cell: Y=yellow B=blue R=red G=green D=dark .=bg
for y in range(195, 300):
    line = ""
    for x in range(80, 120, 2):
        c = oa[y, x]
        r, g, b = int(c[0]), int(c[1]), int(c[2])
        if r > 200 and g > 200 and b < 170: ch = "Y"
        elif b > 120 and b - r > 50 and b - g > 40: ch = "B"
        elif r > 110 and r - g > 55 and r - b > 55: ch = "R"
        elif g > 80 and g - r > 30 and g - b > 30: ch = "G"
        elif r + g + b < 330: ch = "D"
        elif r + g + b < 520: ch = "+"
        else: ch = "."
        line += ch
    print(f"{y:3d} {line}")
