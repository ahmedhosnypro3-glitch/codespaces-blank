#!/usr/bin/env python3
"""Overview map of the diagram panel: classify each sampled pixel."""
from PIL import Image
import numpy as np
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
a = np.array(Image.open(V / "unique_slides/slide_006.jpg").convert("RGB")).astype(int)

X0, X1, Y0, Y1, S = 415, 700, 150, 470, 4
print(f"overview x{X0}-{X1} y{Y0}-{Y1} step {S} (each cell = pixel at that coordinate)")
print("      " + "".join(str((x // 100) % 10) if x % 20 == 0 else " " for x in range(X0, X1, S)))
for y in range(Y0, Y1, S):
    row = ""
    for x in range(X0, X1, S):
        r, g, b = a[y, x]
        lum = (int(r) + int(g) + int(b)) / 3
        if r - g > 22 and r - b > 22:
            row += "R"
        elif b - r > 25 and b - g > 22:
            row += "B"
        elif g - r > 20 and g - b > 20:
            row += "G"
        elif lum > 245:
            row += " "
        elif lum > 225:
            row += "."
        elif lum > 175:
            row += "-"
        elif lum > 110:
            row += "+"
        else:
            row += "#"
    print(f"  y{y:3d} {row}")
print("      " + "".join(str((x // 100) % 10) if x % 20 == 0 else " " for x in range(X0, X1, S)))
