#!/usr/bin/env python3
"""ASCII color map of slide_004.jpg at 8x8px cells — layout comprehension pass."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = im.shape[:2]

CELL = 8  # 960/8=120 cols, 540/8=67.5 -> 68 rows

def classify(rgb):
    r, g, b = rgb
    if r > 245 and g > 245 and b > 245:
        return "."   # white
    # gray panel E9E9E7
    if abs(r - 233) < 12 and abs(g - 233) < 12 and abs(b - 231) < 14:
        return "g"
    if r > 100 and (r - g) > 50 and (r - b) > 30:
        return "R"   # red ink
    if b > 90 and (b - r) > 50 and (b - g) > 30:
        return "B"   # blue ink
    if r > 180 and g > 170 and b < 130:
        return "Y"   # yellow
    if r + g + b < 330:
        return "K"   # dark text
    # warm pale pink/salmon fill
    if (r - b) > 15 and r > 240 and g > 210:
        return "P"
    # pale blue fill
    if (b - r) > 6 and b > 245 - 20:
        return "p"
    return "?" if (r + g + b < 720) else " "

rows = []
for cy in range(0, H, CELL):
    line = []
    for cx in range(0, W, CELL):
        block = im[cy:cy + CELL, cx:cx + CELL].reshape(-1, 3)
        # dominant non-white class by count
        classes = {}
        for px in block[::2]:
            c = classify(px)
            classes[c] = classes.get(c, 0) + 1
        # prefer ink classes over background if present
        for pref in ("K", "R", "B", "Y", "P", "p", "?", " ", "g", "."):
            if classes.get(pref, 0) >= 3:
                line.append(pref)
                break
        else:
            line.append(".")
    rows.append("".join(line))

print("cols: 1 char = 8 px; 60 cols of 8 = x 480")
for i, rtext in enumerate(rows):
    y = i * CELL
    print(f"{y:3d} {rtext}")
