#!/usr/bin/env python3
"""Glyph-level forensics for slide_002.jpg title + plus-sign artifact."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_002.jpg"
).convert("RGB")).astype(int)
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
tit = (r > 150) & (g < 110) & (b < 110)

def ascii_art(mask, y0, y1, x0, x1, step=1):
    print(f"--- band y{y0}..{y1} x{x0}..{x1} ---")
    for y in range(y0, y1 + 1, step):
        row = "".join("#" if mask[y, x] else "." for x in range(x0, x1 + 1))
        print(f"{y:3d} {row}")

# Line 1: y 199..230. Show "Revision" start (x 197..280)
print("=== LINE 1 first letters (R e v i ...) ===")
ascii_art(tit, 197, 232, 195, 285)

# row profile of line 1 (ink count per row) to pin cap top / baseline
print("\n=== line 1 row profile (y190..235) ===")
for y in range(190, 236):
    n = tit[y, 150:800].sum()
    print(f"y={y}: {'#' * min(n, 60)} {n}")
