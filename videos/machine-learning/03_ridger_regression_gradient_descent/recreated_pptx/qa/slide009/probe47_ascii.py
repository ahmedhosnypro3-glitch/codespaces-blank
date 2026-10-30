#!/usr/bin/env python3
"""Probe 47: full-panel ASCII maps of true-red, orange, blue."""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
TRED = (r > 90) & (g < 75) & (b < 75) & ((r - g) > 60) & ((r - b) > 60)
ORANGE = (r > 180) & (g > 70) & (g < 175) & (b < 90) & ((r - g) > 60)
BLUE = (b > 90) & ((b - r) > 40) & ((b - g) > 30) & (r < 90)

def show(mask, x0, x1, y0, y1, sx=1, sy=1, title=""):
    print(f"\n=== {title} x{x0}..{x1} y{y0}..{y1} (step {sx},{sy}) ===")
    hdr = "     " + "".join(str((x // 10) % 10) if (x % 10 == 0) else " " for x in range(x0, x1, sx))
    print(hdr)
    for y in range(y0, y1, sy):
        cells = []
        for x in range(x0, x1, sx):
            block = mask[y:y + sy, x:x + sx]
            cells.append("#" if bool(np.any(block)) else ".")
        print(f"  {y:4d} " + "".join(cells))

# LEFT panel: red only, 2x1 downsample in x to keep width manageable
show(TRED, 118, 455, 138, 445, 2, 2, "LEFT TRUE RED")
show(ORANGE, 118, 455, 138, 445, 2, 2, "LEFT ORANGE")
show(BLUE, 118, 455, 138, 445, 2, 2, "LEFT BLUE")
show(TRED, 532, 860, 138, 445, 2, 2, "RIGHT TRUE RED")
