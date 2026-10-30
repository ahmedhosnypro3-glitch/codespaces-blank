#!/usr/bin/env python3
"""Coarse ASCII structure map of a slide original: cell -> dominant color class."""
from PIL import Image
import numpy as np
import sys

n = sys.argv[1]
img = Image.open(
    f"/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"
    f"unique_slides/slide_0{n}.jpg").convert("RGB")
a = np.asarray(img).astype(int)
H, W = a.shape[:2]
COLS, ROWS = 96, 45

def classify(c):
    r, g, b = c
    mx, mn = max(c), min(c)
    if mx - mn < 14:                      # gray / near-white
        if r > 246: return "."
        if r > 231: return "-"            # light gray fill
        return "#" if r < 150 else "+"    # dark gray / mid gray
    if r > g > b:
        if r - b > 120: return "R"        # strong red
        if r - b > 45: return "r"         # pale red/pink
        if r > 215 and g > 170: return "Y"  # yellow
        return "o"                        # orange
    if g > r and g > b:
        if g - b > 40: return "G"         # green
        return "y"                        # pale yellow-green
    if b > r and b > g:
        return "B"                        # blue
    return "?"

print(f"=== slide {n}  ({W}x{H})  legend: . white  - lightgray  + midgray  # dark")
print("    R red  r pink  Y yellow  o orange  G green  y paleyellow  B blue")
for ry in range(ROWS):
    y0, y1 = ry * H // ROWS, (ry + 1) * H // ROWS
    line = []
    for rx in range(COLS):
        x0, x1 = rx * W // COLS, (rx + 1) * W // COLS
        cell = a[y0:y1, x0:x1].reshape(-1, 3)
        q = (cell // 24 * 24)
        vals, counts = np.unique(q, axis=0, return_counts=True)
        order = counts.argsort()[::-1]
        pick = None
        for i in order:
            frac = counts[i] / len(cell)
            if frac < 0.12: continue
            cls = classify(vals[i])
            if cls != ".":
                pick = cls
                break
        line.append(pick or " ")
    print(f"{ry*12:3d} {''.join(line)}")
