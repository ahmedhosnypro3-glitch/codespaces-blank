#!/usr/bin/env python3
"""Crop original frame regions for slide_031 and verify against judge findings."""
from PIL import Image
import numpy as np, os

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
OUT = "/tmp/031_crops"
os.makedirs(OUT, exist_ok=True)
orig = Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")
O = np.array(orig)

# Original frame regions (fractions of 960x540)
# Diagram: original says approx 20%-90% width, 10%-45% height
# Blue box1: 5%-45% w, 50%-75% h  -> but actual rendering: boxes at
# Let's find actual ink bounding boxes by color channel to be precise.

print("=== find non-background regions ===")
bg = O[5,5]
print("bg pixel", bg)
# Estimate background color from corners
print("corner colors", O[0,0], O[0,-1], O[-1,0], O[-1,-1])

# Find red frame
r,g,b = O[...,0].astype(int), O[...,1].astype(int), O[...,2].astype(int)
reddish = (r>150)&(g<80)&(b<80)
ys,xs = np.where(reddish)
print("red frame ink bbox", xs.min() if len(xs) else None, ys.min() if len(ys) else None,
      xs.max() if len(xs) else None, ys.max() if len(ys) else None, "count", len(xs))

# diagram region: from 20% to 90% w = 192..864, 10%-45% h = 54..243
d = orig.crop((192, 40, 880, 250))
d.save(f"{OUT}/orig_diagram.png")
print("orig diagram crop", d.size)

# blue boxes region: 5%-45% w = 48..432; 50%-75% h = 270..405
b1 = orig.crop((40, 250, 460, 420))
b1.save(f"{OUT}/orig_boxes.png")
print("orig boxes crop", b1.size)
