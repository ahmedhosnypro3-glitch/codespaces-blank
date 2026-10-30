#!/usr/bin/env python3
"""2px ASCII zoom of BOX1/BOX2/Remember interiors, R/B/K ink separated.

Lets me read the exact glyph layout of the tall column-vector equations and
their side captions (which ink color sits where). 1px=1pt.
"""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 100) & ((r - g) > 50) & ((r - b) > 30)
blue = (b > 90) & ((b - r) > 50) & ((b - g) > 30)
dark = (r + g + b) < 330


def zoom(name, x0, x1, y0, y1, cell=2):
    print(f"\n--- {name}: x{x0}..{x1} y{y0}..{y1} (cell {cell}px) --- top header = tens digit of abs x")
    hdr = "     " + "".join(str(((x0 + i * cell) // 10) % 10) for i in range((x1 - x0) // cell))
    print(hdr)
    for cy in range(y0, y1, cell):
        line = []
        for cx in range(x0, x1, cell):
            block = im[cy:cy + cell, cx:cx + cell].reshape(-1, 3)
            rr, gg, bb = block[:, 0], block[:, 1], block[:, 2]
            R = int((((rr > 100) & ((rr - gg) > 50) & ((rr - bb) > 30))).sum())
            B = int((((bb > 90) & ((bb - rr) > 50) & ((bb - gg) > 30))).sum())
            K = int((((rr + gg + bb) < 330)).sum())
            line.append("R" if R >= B and R >= K and R > 0 else ("B" if B >= K and B > 0 else ("K" if K > 0 else ".")))
        print(f"{cy:4d} " + "".join(line))


zoom("BOX1 OriginalLabels", 82, 392, 104, 216, cell=2)
zoom("BOX2 PredLabels", 428, 742, 104, 216, cell=2)
zoom("Remember", 788, 874, 104, 148, cell=2)
