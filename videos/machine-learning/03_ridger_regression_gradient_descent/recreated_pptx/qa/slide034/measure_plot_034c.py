#!/usr/bin/env python3
"""Find slide_034's y-axis position and tick labels."""
import numpy as np
from PIL import Image

ROOT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
im = np.asarray(Image.open(ROOT + "/unique_slides/slide_034.jpg").convert("RGB")).astype(int)

X0, X1, Y0, Y1 = 608, 847, 60, 312
box = im[Y0:Y1, X0:X1]
r, g, b = box[:, :, 0], box[:, :, 1], box[:, :, 2]

# y-axis should be a dark vertical line on the left side of the plot box
# Look for dark pixels in left region of box
left = box[:, :50]
rd, gd, bd = left[:, :, 0], left[:, :, 1], left[:, :, 2]
dark = (rd + gd + bd) < 200
colcnt = dark.sum(axis=0)
print("left dark cols (rel 0..49):", [(i, int(c)) for i, c in enumerate(colcnt) if c > 50])

# Check entire left edge for the y-axis line
# Also check for the x-axis tick labels: "-10", "-6", "-2", "2", "6", "10" 
# These would be below the x-axis at y~172

# Let's also find the "y" label (vertical) above the y-axis
# and "x" label at right of x-axis
# Search for dark vertical text at left edge of box
for y_off in range(0, Y1 - Y0, 20):
    patch = box[y_off:y_off+20, :30]
    rd, gd, bd = patch[:, :, 0], patch[:, :, 1], patch[:, :, 2]
    dark = (rd + gd + bd) < 180
    if dark.sum() > 30:
        print(f"y={Y0+y_off}: left edge has {dark.sum()} dark px")

# The x-axis is at y=172 (frame). Let's scan below it for tick labels
print("\n--- below x-axis (y=172..312) ---")
bottom = box[112:, :]  # below y=172
rb, gb, bb = bottom[:, :, 0], bottom[:, :, 1], bottom[:, :, 2]
darkb = (rb + gb + bb) < 180
rowcnt = darkb.sum(axis=1)
print("dark rows below x-axis:", [(172+i, int(c)) for i, c in enumerate(rowcnt) if c > 100][:15])

# And check the left of box for y-axis tick labels
print("\n--- left of box (x=608..640) ---")
leftfull = im[60:312, 590:620]
rl, gl, bl = leftfull[:, :, 0], leftfull[:, :, 1], leftfull[:, :, 2]
darkl = (rl + gl + bl) < 180
colcnt = darkl.sum(axis=0)
print("dark cols left of box:", [(590+i, int(c)) for i, c in enumerate(colcnt) if c > 100])
rowcnt = darkl.sum(axis=1)
print("dark rows left of box:", [(60+i, int(c)) for i, c in enumerate(rowcnt) if c > 80][:20])