#!/usr/bin/env python3
"""Precise geometry of slide_028: frame, boxes, and text bands."""
from PIL import Image
import numpy as np

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_028.jpg").convert("RGB")
a = np.asarray(img).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
H, W = a.shape[:2]

red = (r > 140) & (r - g > 50) & (r - b > 50)

# 1. Which COLUMNS have long vertical red lines (frame / box borders)?
colsum = red.sum(axis=0)
print("cols with >50 red px:")
for x in range(W):
    if colsum[x] > 60:
        print(f"  col {x} ({x/72:.2f}in): {colsum[x]} px")

rowsum = red.sum(axis=1)
print("\nrows with >50 red px:")
for y in range(H):
    if rowsum[y] > 60:
        print(f"  row {y} ({y/72:.2f}in): {rowsum[y]} px")