#!/usr/bin/env python3
"""Precise text ink measurement for slide 5 and 6."""
from PIL import Image
import numpy as np

def load(path):
    return Image.open(path).convert("RGB")

def find_text_bands(img, color_mask, label):
    a = np.asarray(img)
    mask = color_mask(a)
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    if len(rows) == 0:
        print(f"{label}: no ink")
        return
    runs = []
    start = None
    for r in range(int(rows[0]), int(rows[-1]) + 2):
        on = r < mask.shape[0] and mask[r].any()
        if on and start is None:
            start = r
        elif not on and start is not None:
            if r - start >= 2:
                runs.append((start, r - 1))
            start = None
    print(f"{label}: rows {rows[0]}..{rows[-1]} cols {cols[0]}..{cols[-1]}")
    for (r0, r1) in runs:
        c = mask[r0:r1+1]
        cc = np.where(c.any(axis=0))[0]
        print(f"   band rows {r0}-{r1} (h={r1-r0+1}) cols {cc[0].astype(int)}-{cc[-1].astype(int)}")

def red_text_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (r > 180) & (r - g > 50) & (r - b > 50) & (g < 100) & (b < 100)

def blue_text_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (b > 180) & (b - r > 50) & (b - g > 50) & (r < 100) & (g < 100)

def black_text_mask(a):
    return a.mean(axis=2) < 80

def slide5_red_text_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (r > 180) & (r - g > 50) & (r - b > 50) & (g < 100) & (b < 100) & (a[:,:,0] > a[:,:,1] + 50)

img5 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_005.jpg")
img6 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_006.jpg")

print("=== SLIDE 5 TEXT ===")
find_text_bands(img5, red_text_mask, "slide5 RED text")
find_text_bands(img5, blue_text_mask, "slide5 BLUE text")
find_text_bands(img5, black_text_mask, "slide5 BLACK text")

print("\n=== SLIDE 6 TEXT ===")
find_text_bands(img6, red_text_mask, "slide6 RED text")
find_text_bands(img6, blue_text_mask, "slide6 BLUE text")
find_text_bands(img6, black_text_mask, "slide6 BLACK text")