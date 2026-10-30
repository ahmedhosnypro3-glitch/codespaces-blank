#!/usr/bin/env python3
"""Detailed measure of slide_028 specific elements."""
import sys
from PIL import Image
import numpy as np

def load(path):
    return Image.open(path).convert("RGB")

def find_color_region(a, r_min, r_max, g_min, g_max, b_min, b_max):
    """Find connected regions matching color bounds."""
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    mask = (r >= r_min) & (r <= r_max) & (g >= g_min) & (g <= g_max) & (b >= b_min) & (b <= b_max)
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    if len(rows) == 0:
        return None
    return (rows[0], rows[-1], cols[0], cols[-1])

def measure_boxes(img, color_name, r_min, r_max, g_min, g_max, b_min, b_max):
    a = np.asarray(img)
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    mask = (r >= r_min) & (r <= r_max) & (g >= g_min) & (g <= g_max) & (b >= b_min) & (b <= b_max)
    # Find connected components by row runs
    rows = np.where(mask.any(axis=1))[0]
    if len(rows) == 0:
        return
    print(f"\n{color_name} boxes:")
    runs = []
    start = None
    for ri in range(int(rows[0]), int(rows[-1]) + 2):
        on = ri < mask.shape[0] and mask[ri].any()
        if on and start is None:
            start = ri
        elif not on and start is not None:
            if ri - start >= 2:
                runs.append((start, ri - 1))
            start = None
    for (r0, r1) in runs:
        c = mask[r0:r1+1]
        cc = np.where(c.any(axis=0))[0]
        if len(cc) > 0:
            print(f"  rows {r0}-{r1} (h={r1-r0+1}) cols {cc[0].astype(int)}-{cc[-1].astype(int)} (w={cc[-1]-cc[0]+1})")

if __name__ == "__main__":
    base = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
    img = load(f"{base}/slide_028.jpg")
    a = np.asarray(img)
    print(f"=== slide_028.jpg size={img.size} ===")
    
    # Badge - yellow circle (top right)
    print("\n=== YELLOW BADGE ===")
    measure_boxes(img, "yellow", 200, 255, 200, 255, 0, 180)
    
    # Red frame elements
    print("\n=== RED FRAMES / BOXES ===")
    measure_boxes(img, "red", 180, 255, 0, 100, 0, 100)
    
    # Blue header text region
    print("\n=== BLUE HEADER ===")
    measure_boxes(img, "blue", 0, 100, 0, 150, 180, 255)
    
    # Gray output boxes
    print("\n=== GRAY BOXES ===")
    measure_boxes(img, "gray", 160, 210, 160, 210, 160, 210)
    
    # Red arrow
    print("\n=== RED ARROW ===")
    measure_boxes(img, "arrow", 200, 255, 0, 50, 0, 50)
    
    # Convert px to inches (960px = 13.33in slide width per house chrome)
    # 1px = 13.33/960 = 0.013885 in
    # 1pt = 1/72 in = 0.013889 in
    # So 1px ≈ 1pt exactly for this resolution
    print("\n=== CONVERSION ===")
    print(f"960px = 13.33in => 1px = {13.33/960:.5f} in ≈ 1pt ({1/72:.5f} in)")
    print(f"540px = 7.5in => 1px = {7.5/540:.5f} in ≈ 1pt ({1/72:.5f} in)")