#!/usr/bin/env python3
"""Table grid + arrow geometry for slide 34; panel borders for 33."""
import numpy as np
from PIL import Image

base = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "10_nn_training_and_example")
a = np.asarray(Image.open(f"{base}/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 120) & ((r - g) > 45) & ((r - b) > 35)

print("=== slide 34: horizontal red lines (rows with >200 red px in x=40..660) ===")
for y in range(195, 540):
    c = red[y, 40:660].sum()
    if c > 200:
        xs = np.where(red[y, 40:660])[0] + 40
        print(f"  y={y}: count={c} x={xs.min()}-{xs.max()}")

print("=== vertical red lines (cols with >150 red px in y=195..540) ===")
for x in range(40, 700):
    c = red[195:540, x].sum()
    if c > 150:
        ys = np.where(red[195:540, x])[0] + 195
        print(f"  x={x}: count={c} y={ys.min()}-{ys.max()}")

print("=== red arrow blob (x>560, y>200) ===")
mask = red[:, 560:660]
ys, xs = np.where(mask)
if len(ys):
    print(f"  bbox x={xs.min()+560}-{xs.max()+560} y={ys.min()}-{ys.max()}")
# arrow profile per row
for y in range(260, 460, 10):
    c = red[y, 560:660].sum()
    if c:
        xs = np.where(red[y, 560:660])[0] + 560
        print(f"  y={y}: x={xs.min()}-{xs.max()} n={c}")

print("=== green title box (slide 34 top-left) ===")
green = (g > 100) & ((g - r) > 30) & ((g - b) > 30)
ys, xs = np.where(green[:200, :350])
if len(ys):
    print(f"  bbox x={xs.min()}-{xs.max()} y={ys.min()}-{ys.max()}")

# slide 33 panel borders
a3 = np.asarray(Image.open(f"{base}/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
r3, g3, b3 = a3[:, :, 0], a3[:, :, 1], a3[:, :, 2]
red3 = (r3 > 120) & ((r3 - g3) > 45) & ((r3 - b3) > 35)
print("=== slide 33: horizontal red lines ===")
for y in range(40, 540):
    c = red3[y, 30:930].sum()
    if c > 300:
        xs = np.where(red3[y, 30:930])[0] + 30
        print(f"  y={y}: count={c} x={xs.min()}-{xs.max()}")
print("=== slide 33: vertical red lines ===")
for x in range(30, 930):
    c = red3[40:540, x].sum()
    if c > 150:
        ys = np.where(red3[40:540, x])[0] + 40
        print(f"  x={x}: count={c} y={ys.min()}-{ys.max()}")
