#!/usr/bin/env python3
"""Probe 53: raw pixels of the two red diagonal strokes (width + colour)."""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)

print("=== RIGHT diagonal: raw pixels, y210..268, x620..656 ===")
print("     " + "".join(f"{x%100:4d}" for x in range(620, 657)))
for y in range(210, 269, 2):
    print(f"  {y:4d} " + "".join(f"{a[y,x,0]:3d},{a[y,x,1]:3d},{a[y,x,2]:3d} " for x in range(620, 657, 3)))

print("\n=== LEFT diagonal: raw pixels, y196..232, x195..220 ===")
print("     " + "".join(f"{x%100:4d}" for x in range(195, 221)))
for y in range(196, 233, 2):
    print(f"  {y:4d} " + "".join(f"{a[y,x,0]:3d},{a[y,x,1]:3d},{a[y,x,2]:3d} " for x in range(195, 221, 1)))

print("\n=== LEFT big disc: raw x219..248 y228..256 (every 3rd row) ===")
for y in range(228, 257, 2):
    print(f"  {y:4d} " + "".join(f"{a[y,x,0]:3d},{a[y,x,1]:3d},{a[y,x,2]:3d} " for x in range(219, 249, 3)))
