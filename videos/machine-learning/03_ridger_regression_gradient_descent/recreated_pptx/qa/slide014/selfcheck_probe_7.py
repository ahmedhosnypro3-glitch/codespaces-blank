#!/usr/bin/env python3
"""Measure each content band's extent precisely."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# Yellow band (FFF9C4 approx ~249,253,218). Scan at columns that are text-free
print("=== YELLOW band: vertical scan at x=150 (text-free left area) ===")
for y in range(230, 460, 4):
    print(f"  y={y:3d} rgb={tuple(int(v) for v in im[y,150])}")

# Determine the yellow band y-extent by counting matching pixels per row
yel = (r > 240) & (g > 240) & (b > 200) & (b < 240) & (r - b > 15)
rowc = yel.sum(axis=1)
print("\nYellow matching px per row:")
for y in range(230, 460, 4):
    print(f"  y={y:3d}: {rowc[y]}")
