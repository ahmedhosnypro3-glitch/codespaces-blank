#!/usr/bin/env python3
"""PIL measurement of unique_slides/slide_014.jpg (960x540, 1px=1pt)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
H, W = im.shape[:2]
print("image", W, "x", H)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def mask_ink(tol=25):
    return (np.abs(im - 255).max(axis=2) > tol)

ink = mask_ink()
rows = np.where(ink.sum(axis=1) > 0)[0]
cols = np.where(ink.sum(axis=0) > 0)[0]
print("full ink bbox x", cols.min(), cols.max(), "y", rows.min(), rows.max())

# Per-row ink profile to find band boundaries
prof = ink.sum(axis=1)
print("\n--- row ink profile (every 4 rows) ---")
for y in range(0, 540, 4):
    if prof[y] > 0:
        print(f"y={y:3d} ink={prof[y]:4d}")
