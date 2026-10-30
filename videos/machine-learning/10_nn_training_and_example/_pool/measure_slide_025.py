#!/usr/bin/env python3
"""Measure slide_025 ink bands for build geometry."""
import sys
from PIL import Image
import numpy as np

def load(path):
    return Image.open(path).convert("RGB")

def ink_bands(img, mask_fn, label):
    a = np.asarray(img)
    mask = mask_fn(a)
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
    print(f"{label}: rows {rows[0]}..{rows[-1]} cols {cols[0]}..{cols[-1]} size {img.size}")
    for (r0, r1) in runs:
        c = mask[r0:r1+1]
        cc = np.where(c.any(axis=0))[0]
        print(f"   band rows {r0}-{r1} (h={r1-r0+1}) cols {cc[0].astype(int)}-{cc[-1].astype(int)}")

def red_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (r > 150) & (r - g > 30) & (r - b > 30)

def blue_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (b > 150) & (b - r > 30) & (b - g > 20)

def yellow_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (r > 200) & (g > 200) & (b < 200) & (b < r - 40)

def dark_mask(a):
    return a.mean(axis=2) < 100

def gray_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (abs(r - g) < 20) & (abs(g - b) < 20) & (r > 150) & (r < 220)

if __name__ == "__main__":
    base = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
    img = load(f"{base}/slide_025.jpg")
    print(f"=== slide_025.jpg size={img.size} ===")
    ink_bands(img, dark_mask, "slide28 dark")
    ink_bands(img, red_mask, "slide28 red")
    ink_bands(img, blue_mask, "slide28 blue")
    ink_bands(img, yellow_mask, "slide28 yellow")
    ink_bands(img, gray_mask, "slide28 gray")