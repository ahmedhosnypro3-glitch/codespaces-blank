#!/usr/bin/env python3
"""Measure precise geometry for slide_005 and slide_006 boxes and text."""
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
    # find connected row runs
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

def dark_mask(a):
    return a.mean(axis=2) < 100

def blue_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (b > 120) & (b - r > 30) & (b - g > 20)

def yellow_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (r > 200) & (g > 200) & (b < 180) & (b < r - 30)

def green_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (g > 120) & (g - r > 20) & (g - b > 20)

def red_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (r > 150) & (r - g > 30) & (r - b > 30)

# Slide 5 detailed
img5 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_005.jpg")
print("=== SLIDE 5 DETAILED ===")
ink_bands(img5, red_mask, "slide5 RED (title)")
ink_bands(img5, yellow_mask, "slide5 YELLOW (badge)")

# Also find the three colored boxes by their background colors
# Light blue: high B, moderate R,G
def light_blue_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (b > 200) & (b - r > 30) & (b - g > 30) & (r > 150) & (g > 150)

# Light yellow: high R,G, low B
def light_yellow_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (r > 230) & (g > 230) & (b > 200) & (b < 230) & (abs(r-g) < 30)

# Light green: high G
def light_green_mask(a):
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    return (g > 200) & (g - r > 30) & (g - b > 30) & (r > 150) & (b > 150)

ink_bands(img5, light_blue_mask, "slide5 LIGHT BLUE box bg")
ink_bands(img5, light_yellow_mask, "slide5 LIGHT YELLOW box bg")
ink_bands(img5, light_green_mask, "slide5 LIGHT GREEN box bg")

# Slide 6 detailed
img6 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_006.jpg")
print("\n=== SLIDE 6 DETAILED ===")
ink_bands(img6, red_mask, "slide6 RED (title)")
ink_bands(img6, blue_mask, "slide6 BLUE (subtitle)")
ink_bands(img6, yellow_mask, "slide6 YELLOW (badge)")