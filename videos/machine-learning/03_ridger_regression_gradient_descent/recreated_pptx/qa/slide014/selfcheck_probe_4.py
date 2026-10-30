#!/usr/bin/env python3
"""Sample exact colors along vertical and horizontal centerlines."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)

# Vertical scan down x=480 (center)
print("=== Vertical scan at x=480 ===")
for y in range(40, 545, 5):
    px = im[y, 480]
    print(f"y={y:3d}  rgb={tuple(int(v) for v in px)}")

# Horizontal scan at y=470 (loss/reg term boxes)
print("\n=== Horizontal scan at y=250 ===")
for x in range(50, 960, 20):
    px = im[250, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")

print("\n=== Horizontal scan at y=470 ===")
for x in range(50, 960, 20):
    px = im[470, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")
