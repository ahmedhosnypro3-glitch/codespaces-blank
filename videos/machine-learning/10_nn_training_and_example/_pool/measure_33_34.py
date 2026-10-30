#!/usr/bin/env python3
"""Measure slide 33/34 originals: color families, blob bboxes, and grid structure."""
from PIL import Image
import numpy as np
from scipy import ndimage
import sys

n = sys.argv[1]
img = Image.open(f"/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_0{n}.jpg").convert("RGB")
arr = np.asarray(img).astype(int)
H, W = arr.shape[:2]
r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
print(f"=== slide {n}: {arr.shape} ===")

def blobs(mask, name, min_size=300):
    lab, cnt = ndimage.label(mask)
    print(f"\n-- {name} --")
    for i in range(1, cnt+1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_size:
            continue
        print(f"  x={xs.min()}-{xs.max()} y={ys.min()}-{ys.max()} "
              f"(w={xs.max()-xs.min()+1}, h={ys.max()-ys.min()+1}, area={len(ys)})")

blobs((r > 140) & (r < 235) & (g < 90) & (b < 95), "DARK RED", 200)
blobs((r > 235) & (g > 195) & (b < 100) & (r - b > 140), "YELLOW", 150)
blobs((r > 220) & (g > 120) & (g < 205) & (b < 120) & (r - b > 110), "ORANGE", 150)
blobs((b > 140) & (b - r > 50) & (b - g > 40), "BLUE", 150)
blobs((g > 90) & (g < 175) & (r < 100) & (b < 100), "DARK GREEN", 150)
blobs((r > 220) & (g > 180) & (g < 240) & (b > 180) & (b < 245) & (g - b > 15), "LIGHT GREEN", 200)

# non-white (content) extents
nw = (r < 245) | (g < 245) | (b < 245)
ys, xs = np.where(nw)
print(f"\nnon-white bbox: x={xs.min()}-{xs.max()} y={ys.min()}-{ys.max()}")

# Row profile of content
print("\nrow profile:")
for y in range(0, H, 15):
    c = np.sum(nw[y])
    if c:
        print(f"  y={y:3d}: {c}")
