#!/usr/bin/env python3
"""PIL measurement of specific content regions in slide_014.jpg."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def mask_color(target_r, target_g, target_b, tol=30):
    return (np.abs(r - target_r) < tol) & (np.abs(g - target_g) < tol) & (np.abs(b - target_b) < tol)

def mask_ink(tol=30):
    return (np.abs(im - 255).max(axis=2) > tol)

ink = mask_ink()

# Measure yellow badge
yel = mask_color(255, 235, 59, tol=40)  # ~FFEB3B
ys = np.where(yel)
if len(ys[0]) > 0:
    print(f"Yellow badge: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}, center=({(ys[1].min()+ys[1].max())/2:.1f}, {(ys[0].min()+ys[0].max())/2:.1f})")

# Measure purple ring
pur = mask_color(106, 90, 205, tol=50)  # ~6A5ACD
ys = np.where(pur)
if len(ys[0]) > 0:
    print(f"Purple ring: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Red strokes
red = (r > 80) & ((r - g) > 30) & ((r - b) > 30)
ys = np.where(red)
print(f"Red strokes: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Panel gray E9E9E7 ~ (233,233,231)
gray = mask_color(233, 233, 231, tol=20)
ys = np.where(gray)
print(f"Panel gray: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Title region - look for blue text (0000FF)
blue = mask_color(0, 0, 255, tol=60)
ys = np.where(blue)
if len(ys[0]) > 0:
    print(f"Blue text: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Light yellow band (FFF9C4)
yel_band = mask_color(255, 249, 196, tol=40)
ys = np.where(yel_band)
if len(ys[0]) > 0:
    print(f"Light yellow band: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Light pink band (FFEBEE)
pink = mask_color(255, 235, 238, tol=40)
ys = np.where(pink)
if len(ys[0]) > 0:
    print(f"Light pink band: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Light blue band (E1F5FE)
lblue = mask_color(225, 245, 254, tol=40)
ys = np.where(lblue)
if len(ys[0]) > 0:
    print(f"Light blue band: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Vertical ink profile for left/right columns
print("\n--- col ink profile (every 20 cols) ---")
prof = ink.sum(axis=0)
for x in range(0, 960, 20):
    if prof[x] > 0:
        print(f"x={x:3d} ink={prof[x]:4d}")