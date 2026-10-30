#!/usr/bin/env python3
"""ASCII color maps of orig outlier column groups 2 and 3."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
oa = np.asarray(Image.open(f"{V}/unique_slides/slide_019.jpg").convert("RGB")).astype(int)

def amap(y0, y1, x0=80, x1=122):
    for y in range(y0, y1):
        line = ""
        for x in range(x0, x1, 2):
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

print("=== GROUP 2: y320..400 ===")
amap(320, 400)
print("=== GROUP 3: y424..502 ===")
amap(424, 502)
