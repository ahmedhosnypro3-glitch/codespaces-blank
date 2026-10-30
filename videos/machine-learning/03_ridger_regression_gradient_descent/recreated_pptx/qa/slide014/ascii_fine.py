#!/usr/bin/env python3
"""1px-per-char ASCII dump of a window, so glyph level structure reads."""
import sys
import numpy as np
from PIL import Image

NS = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/")
og = np.asarray(Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")).astype(int)


def cls(R, G, B):
    if R > 242 and G > 242 and B > 242:
        return " "
    if abs(R - 233) < 14 and abs(G - 233) < 14 and abs(B - 231) < 14:
        return " "
    if R > 150 and G < 115 and B < 115:
        return "R"
    if B > 145 and R < 95 and G < 95:
        return "B"
    if G > 115 and R < 155 and B < 155:
        return "G"
    if R < 135 and G < 135 and B < 135:
        return "#"
    return "."


def dump(x0, x1, y0, y1, title):
    print(f"\n=== {title} x {x0}..{x1} y {y0}..{y1} (1 char = 1px) ===")
    for y in range(y0, y1):
        print(f"y={y:3d} " + "".join(cls(*og[y, x]) for x in range(x0, x1)))


x0, x1, y0, y1 = (int(a) for a in sys.argv[1:5])
title = sys.argv[5] if len(sys.argv) > 5 else "window"
dump(x0, x1, y0, y1, title)
