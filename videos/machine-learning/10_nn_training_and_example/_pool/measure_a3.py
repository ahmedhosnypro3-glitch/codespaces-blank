#!/usr/bin/env python3
"""Measure slide_005 and slide_006 ink bands for build geometry."""
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
    # row runs
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

def blue_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (b > 150) & (b - r > 30) & (b - g > 20)

def yellow_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (r > 200) & (g > 200) & (b < 200) & (b < r - 40)

def green_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (g > 150) & (g - r > 25) & (g - b > 25)

def dark_mask(a):
    return a.mean(axis=2) < 100

if __name__ == "__main__":
    base = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
    for n in (5, 6):
        img = load(f"{base}/slide_{n:03d}.jpg")
        print(f"=== slide_{n:03d}.jpg size={img.size} ===")
        ink_bands(img, dark_mask, f"slide{n} dark")
        ink_bands(img, blue_mask, f"slide{n} blue")
        ink_bands(img, yellow_mask, f"slide{n} yellow")
        ink_bands(img, green_mask, f"slide{n} green")
