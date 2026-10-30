#!/usr/bin/env python3
"""ASCII art of slide_044.jpg — classify each cell's dominant colour."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]

# downsample to 120x54 cells (8x10 px each), classify dominant colour
CW, CH = 8, 10
cols, rows = W // CW, H // CH

sample = np.median(IM[460:470, 300:330].reshape(-1, 3), axis=0)

def classify(px):
    r, g, b = px
    if abs(r - sample[0]) < 7 and abs(g - sample[1]) < 7 and abs(b - sample[2]) < 7:
        return "."
    if r > 230 and g > 230 and b > 230:
        return " "
    if r > 200 and g > 200 and b < 190:
        return "Y"   # yellow
    if b > 110 and b - r > 40:
        return "B"   # blue
    if r > 110 and r - g > 45 and r - b > 45:
        return "R"   # red
    if g > r + 20 and g > b + 20:
        return "G"   # green
    if r < 130 and g < 130 and b < 130:
        return "#"   # dark ink
    return ":"

print("    " + "".join(str((c * CW) // 100 % 10) for c in range(cols)))
print("    " + "".join(str((c * CW) // 10 % 10) for c in range(cols)))
for ry in range(rows):
    line = ""
    for cx in range(cols):
        blk = IM[ry*CH:(ry+1)*CH, cx*CW:(cx+1)*CW].reshape(-1, 3)
        # majority non-panel colour
        from collections import Counter
        cnt = Counter(classify(px) for px in blk)
        # drop '.' and ' ' majority if any strong ink present
        strong = {k: v for k, v in cnt.items() if k not in ". "}
        if strong and max(strong.values()) >= 3:
            line += max(strong, key=strong.get)
        else:
            line += max(cnt, key=cnt.get)
    print(f"{ry*CH:>3} {line}")
