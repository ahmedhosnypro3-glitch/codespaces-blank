#!/usr/bin/env python3
"""Count ink glyph clusters in a row band of the frame."""
from PIL import Image
import numpy as np
import sys

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
im = Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")
a = np.asarray(im).astype(int)

def classify(px):
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    s = r + g + b
    if s < 480:
        if r > g + 35 and r > b + 35: return "R"
        if b > r + 35 and b > g + 15: return "B"
        if g > r + 20 and g > b + 20: return "G"
        return "K"
    return "."

for spec in sys.argv[1:]:
    x0, x1, y0, y1, hue = spec.split(",")
    x0, x1, y0, y1 = int(x0), int(x1), int(y0), int(y1)
    def ink(x, y):
        c = classify(a[y, x])
        if hue == "K": return c == "K"
        if hue == "R": return c in ("R",)
        if hue == "B": return c in ("B",)
        if hue == "G": return c in ("G",)
        return c != "."
    cols = [sum(1 for y in range(y0, y1) if ink(x, y)) for x in range(x0, x1)]
    groups = []
    cur = None
    gap = 0
    for i, n in enumerate(cols):
        if n:
            if cur is None:
                cur = [x0 + i, x0 + i]
            else:
                cur[1] = x0 + i
            gap = 0
        elif cur is not None:
            gap += 1
            if gap > 2:
                groups.append(tuple(cur)); cur = None
    if cur is not None: groups.append(tuple(cur))
    widths = [g[1] - g[0] + 1 for g in groups]
    print(f"x{x0}..{x1} y{y0}..{y1} hue={hue}: clusters={len(groups)} widths={widths}")
    print("   spans:", groups)
