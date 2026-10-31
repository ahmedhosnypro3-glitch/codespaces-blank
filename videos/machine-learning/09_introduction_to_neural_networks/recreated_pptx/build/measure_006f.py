#!/usr/bin/env python3
"""ASCII-render regions of the original so glyph colours can be read numerically."""
from PIL import Image
import numpy as np
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
a = np.array(Image.open(V / "unique_slides/slide_006.jpg").convert("RGB")).astype(int)


def art(x0, x1, y0, y1, label, step=1):
    print(f"\n=== {label}  x{x0}-{x1} y{y0}-{y1} ===")
    hdr = "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x0, x1, step))
    print("      " + hdr)
    for y in range(y0, y1):
        row = ""
        for x in range(x0, x1, step):
            r, g, b = a[y, x]
            lum = (r + g + b) / 3
            if lum > 215:
                row += "."
            elif r > 130 and g < 120 and b < 120:
                row += "R"
            elif b > 120 and r < 150:
                row += "B"
            elif g > 90 and r < 140 and b < 140:
                row += "G"
            elif lum < 90:
                row += "#"
            elif lum < 150:
                row += "+"
            else:
                row += "-"
        print(f"  y{y:3d} {row}")


art(76, 240, 106, 128, "equation line 1 head")
art(380, 445, 106, 128, "equation line 1 tail")
art(76, 240, 155, 175, "equation line 2 head")
art(390, 435, 200, 222, "equation line 3 tail")
art(130, 330, 360, 400, "callout box")
art(390, 450, 155, 230, "input column upper")
art(390, 450, 275, 340, "input column mid")
art(390, 450, 390, 430, "input column lower")
art(650, 710, 165, 210, "sigma 1 circle")
art(715, 775, 165, 205, "activation box 1")
art(795, 880, 172, 202, "class label 1")
