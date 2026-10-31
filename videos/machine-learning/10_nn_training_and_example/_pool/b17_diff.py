#!/usr/bin/env python3
"""Compare b17 render (150dpi) vs original frame: downscale render to 960x540, diff map."""
import sys
import numpy as np
from PIL import Image

n = sys.argv[1]
base = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "10_nn_training_and_example")
orig = Image.open(f"{base}/unique_slides/slide_0{n}.jpg").convert("RGB")
ren = Image.open(f"{base}/qa/slide0{n}/rejudge/render-1.png").convert("RGB")
ren2 = ren.resize(orig.size, Image.LANCZOS)
a = np.asarray(orig).astype(int)
b = np.asarray(ren2).astype(int)
diff = np.abs(a - b).sum(axis=2)
print(f"slide {n}: mean abs diff = {diff.mean():.1f}  frac>60: {(diff > 60).mean():.4f}")
# ascii diff map: 4px blocks, '#'=big diff
H, W = diff.shape
for y0 in range(0, H, 9):
    row = []
    for x0 in range(0, W, 4):
        d = diff[y0:y0+9, x0:x0+4].mean()
        row.append('#' if d > 90 else ('+' if d > 40 else ('.' if d > 15 else ' ')))
    print(f"{y0:3d}|" + "".join(row))
