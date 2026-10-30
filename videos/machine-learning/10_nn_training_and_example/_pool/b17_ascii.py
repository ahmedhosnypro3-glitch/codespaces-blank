#!/usr/bin/env python3
"""Color-classified ASCII map of an original frame (b17 slides 33/34)."""
import sys
import numpy as np
from PIL import Image

n = sys.argv[1]
base = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "10_nn_training_and_example")
img = Image.open(f"{base}/unique_slides/slide_0{n}.jpg").convert("RGB")
a = np.asarray(img).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (r > 110) & ((r - g) > 45) & ((r - b) > 35)
yellow = (r > 195) & (g > 160) & ((r - b) > 60) & (g > b)
orange = (r > 195) & (g > 100) & (g < 195) & ((r - b) > 80) & (g > b)
blue = (b > 110) & ((b - r) > 45) & ((b - g) > 25)
green = (g > 95) & ((g - r) > 25) & ((g - b) > 25)
dark = (r < 110) & (g < 110) & (b < 110)

cw = 4
for y0 in range(0, H, 8):
    row = []
    for x0 in range(0, W, cw):
        blk_r = r[y0:y0+8, x0:x0+cw]
        blk_g = g[y0:y0+8, x0:x0+cw]
        blk_b = b[y0:y0+8, x0:x0+cw]
        counts = {
            'R': int(red[y0:y0+8, x0:x0+cw].sum()),
            'Y': int(yellow[y0:y0+8, x0:x0+cw].sum()),
            'O': int(orange[y0:y0+8, x0:x0+cw].sum()),
            'B': int(blue[y0:y0+8, x0:x0+cw].sum()),
            'G': int(green[y0:y0+8, x0:x0+cw].sum()),
            '#': int(dark[y0:y0+8, x0:x0+cw].sum()),
        }
        best = max(counts, key=counts.get)
        row.append(best if counts[best] >= 4 else ('#' if counts['#'] >= 2 else '.'))
    print(f"{y0:3d}|" + "".join(row))
