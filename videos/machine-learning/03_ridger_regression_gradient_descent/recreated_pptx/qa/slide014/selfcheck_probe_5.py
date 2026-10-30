#!/usr/bin/env python3
"""Sample exact colors along horizontal centerlines."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)

# y=250 (Ridge band + Objective band)
print("=== Horizontal scan at y=250 (Ridge/Objective bands) ===")
for x in range(50, 960, 20):
    px = im[250, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")

# y=270 (Define Loss band)
print("\n=== Horizontal scan at y=270 (Define Loss band) ===")
for x in range(50, 960, 20):
    px = im[270, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")

# y=470 (Loss Term / Reg Term boxes)
print("\n=== Horizontal scan at y=470 (Loss Term / Reg Term boxes) ===")
for x in range(50, 960, 20):
    px = im[470, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")

# y=515 (Final objective band)
print("\n=== Horizontal scan at y=515 (Final objective band) ===")
for x in range(50, 960, 20):
    px = im[515, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")

# y=80 (vector boxes)
print("\n=== Horizontal scan at y=80 (vector boxes) ===")
for x in range(50, 960, 20):
    px = im[80, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")