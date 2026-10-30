#!/usr/bin/env python3
"""Finer analysis: sample pixel values, find blue-box extents, red/blue/text bands."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]

print("=== SAMPLES ===")
for (y, x) in [(155, 355), (155, 402), (65, 66), (65, 300), (130, 200),
               (162, 655), (235, 655), (65, 750), (110, 700), (275, 110),
               (60, 100), (100, 100)]:
    print(f"  IM[{y},{x}] = {IM[y, x]}  #%02X%02X%02X" % tuple(IM[y, x]))

# --- blue box at top: find its exact frame ---
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
blue = (b > 110) & (b - r > 40) & (b - g > 25)
# top band only
sub = blue[48:135]
print("\n=== BLUE in rows 48..134: col profile ===")
cc = sub.sum(axis=0)
for x in range(60, 730):
    if cc[x] > 3:
        print(f"  x{x}: {cc[x]} blue px", end="")
        ys = np.where(sub[:, x])[0]
        if len(ys): print(f"  y{ys.min()+48}..{ys.max()+48}")
        else: print()
