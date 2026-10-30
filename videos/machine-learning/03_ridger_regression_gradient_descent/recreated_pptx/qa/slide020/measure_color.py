#!/usr/bin/env python3
"""Title core color decision: C00000 vs 8B0000, from darkest red pixels."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_020.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
# title pixels only (exclude strokes + badge area)
mask = red.copy()
mask[:, :62] = False; mask[:, 898:] = False; mask[533:, :] = False; mask[:52, :] = False
ys, xs = np.where(mask)
px = im[ys, xs]
lum = px.sum(axis=1)
order = np.argsort(lum)
dark = px[order[:400]]  # darkest 400 title pixels
print("darkest 400 title px mean:", dark.mean(axis=0).round(1))
print("darkest 50 px mean:", px[order[:50]].mean(axis=0).round(1))
print("min px:", px[order[0]])
# modal color among pixels with R-G>100 (stroke-core-like)
core = px[(px[:,0] - px[:,1] > 100)]
print("px with R-G>100: n=", len(core), " mean:", core.mean(axis=0).round(1) if len(core) else "-")
# stroke color cores for comparison
for (x, y) in ((58, 300), (901, 300)):
    print(f"stroke px ({x},{y}):", tuple(im[y, x]))
