#!/usr/bin/env python3
"""Full-res ASCII of class labels and activation boxes."""
from PIL import Image
import numpy as np
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
a = np.array(Image.open(V / "unique_slides/slide_006.jpg").convert("RGB")).astype(int)


def art(x0, x1, y0, y1, label):
    print(f"\n=== {label} x{x0}-{x1} y{y0}-{y1} ===")
    print("      " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x0, x1)))
    for y in range(y0, y1):
        row = ""
        for x in range(x0, x1):
            r, g, b = a[y, x]
            lum = (r + g + b) / 3
            if lum > 230:
                row += "."
            elif r - g > 20 and r - b > 20:
                row += "R"
            elif b - r > 20 and b - g > 15:
                row += "B"
            elif g - r > 15 and g - b > 15:
                row += "G"
            elif lum < 110:
                row += "#"
            elif lum < 175:
                row += "+"
            else:
                row += "-"
        print(f"  y{y:3d} {row}")


art(800, 885, 174, 201, "class label pair 1")
art(800, 885, 306, 332, "class label pair 2")
art(718, 770, 168, 205, "activation box 1")
art(655, 706, 165, 210, "sigma circle 1")
art(415, 450, 278, 295, "input label row (x?)")
art(415, 450, 300, 315, "input label row 2")
art(415, 450, 325, 340, "input label row 3")
art(415, 450, 392, 430, "input label xn + bias 1")
