#!/usr/bin/env python3
"""Fit the three decision-boundary lines inside the slide_008 plot panel."""
import numpy as np
from PIL import Image

P = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
a = np.asarray(Image.open(P).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

PX0, PX1, PY0, PY1 = 167, 798, 120, 505

red = (R > 135) & (R - G > 55) & (R - B > 55)
blue = (B > 140) & (B - R > 75) & (B - G > 55)
green = (G > 110) & (G - R > 40) & (G - B > 28)

print("=== RED x positions per row (panel interior) ===")
for y in range(150, 500, 20):
    xs = np.where(red[y, PX0 + 4:PX1 - 3])[0] + PX0 + 4
    print(f" y{y:3d}: {list(xs)}")

print()
print("=== BLUE x positions per row ===")
for y in range(140, 490, 20):
    xs = np.where(blue[y, PX0 + 4:PX1 - 3])[0] + PX0 + 4
    print(f" y{y:3d}: {list(xs)}")

print()
print("=== GREEN x positions per row ===")
for y in range(150, 480, 20):
    xs = np.where(green[y, PX0 + 4:PX1 - 3])[0] + PX0 + 4
    print(f" y{y:3d}: {list(xs)}")
