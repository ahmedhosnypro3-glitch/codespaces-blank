#!/usr/bin/env python3
"""ASCII colour map of slide_011 regions for precise reconstruction."""
import numpy as np
from PIL import Image

IMG = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "09_introduction_to_neural_networks/unique_slides/slide_011.jpg")

a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W, _ = a.shape


def classify(px):
    r, g, b = px
    mx, mn = max(px), min(px)
    sat = mx - mn
    if r > 110 and r - g > 45 and r - b > 45:
        return "R" if sat > 70 else "r"
    if b - r > 45 and b > 100:
        return "B"
    if g - r > 25 and b - r > 25:
        return "C"
    if g - r > 40 and g - b > 25:
        return "G"
    if mx - mn < 18:
        if mx < 90:
            return "#"
        if mx < 190:
            return "+"
        return "."
    return "?"


def ascii_map(x0, y0, x1, y1, sx=2, sy=4, title=""):
    print(f"--- {title}  x{x0}-{x1} y{y0}-{y1} (scale {sx}x{sy}) ---")
    for y in range(y0, y1, sy):
        row = []
        for x in range(x0, x1, sx):
            counts = {}
            for dy in range(sy):
                for dx in range(sx):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < H and 0 <= xx < W:
                        c = classify(a[yy, xx])
                        counts[c] = counts.get(c, 0) + 1
            row.append(max(counts, key=counts.get) if counts else " ")
        print(f"{y:4d} " + "".join(row))
    print()


ascii_map(590, 115, 850, 365, 2, 4, "PLOT")
ascii_map(90, 125, 320, 315, 2, 4, "TABLE")
ascii_map(150, 380, 490, 500, 2, 4, "NN DIAGRAM")
ascii_map(590, 405, 830, 475, 2, 4, "EQUATION BOX")
ascii_map(0, 0, 960, 540, 6, 8, "WHOLE SLIDE (coarse)")
