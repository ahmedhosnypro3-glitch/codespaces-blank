#!/usr/bin/env python3
"""Measure slide 23 original node positions via color-blob connected components."""
from PIL import Image
import numpy as np
from scipy import ndimage

img = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_023.jpg").convert("RGB")
arr = np.asarray(img).astype(int)
H, W = arr.shape[:2]

r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

# Categorize pixels into families
purple = (r > 225) & (b > 225) & (g < 215) & (b - g > 20)
green_lt = (g > 200) & (g - r > 20) & (g - b > 15) & (r > 150) & (b < 235)
green_br = (g > 200) & (g - r > 60) & (g - b > 60)
pink = (r > 235) & (b > 200) & (g < 215) & (r - g > 25)
orange = (r > 225) & (g > 140) & (g < 205) & (b < 175) & (r - g > 25)
cream = (r > 242) & (g > 242) & (b > 205) & (b < 250) & (g - b < 15)

def blobs(mask, name, min_size=400):
    lab, n = ndimage.label(mask)
    print(f"\n=== {name} (blobs>= {min_size}px) ===")
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_size:
            continue
        print(f"  bbox x={xs.min()}-{xs.max()} y={ys.min()}-{ys.max()} "
              f"(w={xs.max()-xs.min()+1}, h={ys.max()-ys.min()+1}, area={len(ys)})")

blobs(purple, "PURPLE")
blobs(green_lt, "LIGHT GREEN")
blobs(green_br, "BRIGHT GREEN")
blobs(pink, "PINK")
blobs(orange, "ORANGE")
blobs(cream, "CREAM")

# Also: all "light fill" pixels (any pastel, not white, not dark) to catch shapes
light = (r > 235) & (g > 230) & (b > 200) & (np.abs(arr - arr.mean(axis=2, keepdims=True)).max(axis=2) < 40)
blobs(light, "ALL LIGHT FILL", 600)

# Dark red text/arrows pixels
darkred = (r > 80) & (r < 180) & (g < 90) & (b < 95)
blobs(darkred, "DARK RED (text/arrows)", 250)
