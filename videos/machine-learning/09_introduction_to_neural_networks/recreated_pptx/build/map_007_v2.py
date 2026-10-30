#!/usr/bin/env python3
"""Classify the slide 007 plot panel into a coarse ASCII map by pixel color."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)

X0, X1, Y0, Y1 = 150, 765, 108, 484
STEP = 6


def classify(px):
    r, g, b = px
    if r > 195 and g > 185 and b < 150:
        return "Y"  # yellow box
    if r > 150 and g < 90 and b < 90:
        return "R"  # strong red (line, axis, red dots)
    if r > 110 and 150 < g < 205 and 140 < b < 205 and g - r > 20:
        return "g"  # light green hatch
    if r > 120 and r < 205 and g > 120 and b - r > 45:
        return "b"  # light blue hatch
    if r > 180 and g < 195 and 120 < g < 200 and r - g > 40 and r - b > 40:
        return "p"  # light pink hatch
    if b > 140 and r < 120:
        return "B"  # strong blue
    if g > 110 and r < 120 and b < 120:
        return "G"  # strong green
    if r < 95 and g < 95 and b < 95:
        return "k"  # black
    if r > 205 and g > 205 and b > 205:
        return "."
    return "-"


print("cols:", " ".join(f"{x}" for x in range(X0, X1, STEP * 2)))
for y in range(Y0, Y1, STEP):
    row = "".join(classify(a[y, x]) for x in range(X0, X1, STEP))
    print(f"{y:3d} {row}")
