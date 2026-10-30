#!/usr/bin/env python3
"""Find pink band (Define Loss) and light blue bands."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# Pink band (FFEBEE) - light pink #FFEBEE = (255, 235, 238)
pink = (r > 240) & (r < 255) & (g > 220) & (g < 250) & (b > 225) & (b < 255) & (r - g > 5) & (g - b > -30)
rowc = pink.sum(axis=1)
print("Pink band matching px per row:")
for y in range(280, 400, 2):
    if rowc[y] > 50:
        print(f"  y={y:3d}: {rowc[y]}")

# Light blue band (E1F5FE) - (225, 245, 254)
lblue = (r > 215) & (r < 240) & (g > 235) & (g < 255) & (b > 240) & (b < 255)
rowc = lblue.sum(axis=1)
print("\nLight blue band matching px per row:")
for y in range(400, 540, 2):
    if rowc[y] > 50:
        print(f"  y={y:3d}: {rowc[y]}")

# Vector boxes top area
print("\n=== Vector boxes y-range ===")
for y in range(60, 240, 4):
    # look for white background with black text
    pix = im[y, 200]
    if pix[0] > 245 and pix[1] > 245 and pix[2] > 245:
        print(f"  y={y:3d} white at x=200")

# Right vector box x-range at y=100
print("\n=== Right vector box x at y=100 ===")
for x in range(500, 960, 20):
    pix = im[100, x]
    print(f"  x={x:3d} rgb={tuple(int(v) for v in pix)}")