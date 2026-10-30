#!/usr/bin/env python3
"""Coarse density map of a frame region, 2x2 px per char, with dominant color class."""
from PIL import Image
import numpy as np
import sys

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
im = Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")
a = np.asarray(im).astype(int)

x0, x1, y0, y1 = (int(v) for v in sys.argv[1:5])
step = int(sys.argv[5]) if len(sys.argv) > 5 else 2

def classify(px):
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    s = r + g + b
    if s < 480:
        if r > g + 35 and r > b + 35: return "R"
        if b > r + 35 and b > g + 15: return "B"
        if g > r + 20 and g > b + 20: return "G"
        return "K"
    return "."

print(f"region x{x0}..{x1} y{y0}..{y1} step={step}")
for y in range(y0, y1, step):
    row = ""
    for x in range(x0, x1, step):
        counts = {}
        for yy in range(y, min(y + step, y1)):
            for xx in range(x, min(x + step, x1)):
                c = classify(a[yy, xx])
                if c != ".":
                    counts[c] = counts.get(c, 0) + 1
        if not counts:
            row += " "
        else:
            c = max(counts, key=counts.get)
            row += c if counts[c] >= 2 else c.lower()
    print(f"{y:4d} {row}")
