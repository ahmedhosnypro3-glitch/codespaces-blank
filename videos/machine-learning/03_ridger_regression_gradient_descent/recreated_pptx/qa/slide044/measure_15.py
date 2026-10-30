#!/usr/bin/env python3
"""Clean approach: interior = strictly inside blue box (x74..714, y58..126).
Print row-by-row ink counts so I can see the actual text lines."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf
satred = (rf - gf > 45) & (rf - bf > 45) & (rf > 110)
satblue = (bf - rf > 40) & (bf - gf > 25) & (bf > 110)
ink = (LUM < 205) | satred | satblue
X0, X1, Y0, Y1 = 74, 714, 58, 126   # strictly inside the blue box

print("row: inkpx  inkcols")
for y in range(48, 140):
    row = ink[y, :]
    n = int(row[Y0:Y1].sum() if X0 <= 0 else row[X0:X1+1].sum())
    cols = np.where(ink[y, X0:X1+1])[0] + X0
    if n:
        print(f"  y{y:>3}: {n:>4}  x {cols.min()}..{cols.max()}")
    else:
        print(f"  y{y:>3}:   0")
