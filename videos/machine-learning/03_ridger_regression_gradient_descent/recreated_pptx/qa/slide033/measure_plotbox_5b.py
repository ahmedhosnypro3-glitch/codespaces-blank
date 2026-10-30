#!/usr/bin/env python3
"""Measure the white plot background box in the original frame (slide 033).

The build paints the house panel (E9E9E7, x54..903 y45..540) but never paints a
white box for the plot, so the render shows panel gray where the original shows
white. Find the box's exact x/y extent so the fix is measured, not guessed.

Method: in the plot's x-range (x590..915) walk rows top-to-bottom and find, for
each row, the contiguous run of WHITE/near-white pixels that is NOT broken by the
curve/gridlines/text. The box is the region where white dominates.
"""
from PIL import Image
import numpy as np, collections

ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg")
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)

W = (o[:, :, 0] >= 240) & (o[:, :, 1] >= 240) & (o[:, :, 2] >= 240)

print("=== per-row white fraction in x600..905 (plot x-range) ===")
for y in range(46, 332):
    frac = W[y, 600:906].mean()
    print(f"  y{y:4d} white_frac {frac:.3f}")
