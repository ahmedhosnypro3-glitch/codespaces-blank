#!/usr/bin/env python3
"""ASCII-art region reader: print a source region as a character map."""
import sys
import numpy as np
from PIL import Image

base = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "10_nn_training_and_example")
n, x0, y0, x1, y1 = sys.argv[1], *map(int, sys.argv[2:6])
thresh = int(sys.argv[6]) if len(sys.argv) > 6 else 660
a = np.asarray(Image.open(f"{base}/unique_slides/slide_0{n}.jpg").convert("RGB")).astype(int)
reg = a[y0:y1 + 1, x0:x1 + 1]
lum = reg.sum(axis=2)
mx = lum.max()
for ry in range(reg.shape[0]):
    print("".join("#" if lum[ry, cx] < thresh else ("+" if lum[ry, cx] < mx - 30 else ".")
                  for cx in range(reg.shape[1])))
