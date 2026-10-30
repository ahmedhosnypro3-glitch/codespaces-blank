#!/usr/bin/env python3
"""measure_frame3.py — ASCII ink map (8px blocks) of slide_021.jpg + panel edges."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

blue = (b > 120) & (b - r > 60) & (b - g > 60)
red = (r > 100) & (r - g > 60) & (r - b > 60)
green = (g > 100) & (g - r > 50) & (g - b > 50)
yellow = (r > 180) & (g > 180) & (b < 140)
dark = (r < 110) & (g < 110) & (b < 110)
dark = dark & ~blue & ~red & ~green & ~yellow

BS = 8
print("ASCII ink map, 8px blocks: B=blue R=red G=green Y=yellow #=dark .=bg")
print("cols: 0..959 -> 120 chars; rows 0..539 -> 68 chars")
hdr = "    " + "".join(str((i // 8) % 10) for i in range(120))
print(hdr)
for by in range(0, H, BS):
    row = []
    for bx in range(0, W, BS):
        blk_d = dark[by:by+BS, bx:bx+BS].sum()
        blk_b = blue[by:by+BS, bx:bx+BS].sum()
        blk_r = red[by:by+BS, bx:bx+BS].sum()
        blk_g = green[by:by+BS, bx:bx+BS].sum()
        blk_y = yellow[by:by+BS, bx:bx+BS].sum()
        counts = {'#': blk_d, 'B': blk_b, 'R': blk_r, 'G': blk_g, 'Y': blk_y}
        mx = max(counts, key=counts.get)
        row.append(mx if counts[mx] >= 2 else ' ')
    print(f"{by:4d} " + "".join(row))
