#!/usr/bin/env python3
"""Slide 020 cream-panel per-line ink extents, borders excluded (region inset
0.06in inside the panel edges). Thresholds 128 and 220."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
S = 960 / 13.3333
IN = 2001 / 13.3333
O = np.array(Image.open(f"{NS}/unique_slides/slide_020.jpg").convert("L")).astype(int)
R = np.array(Image.open(f"{NS}/qa/slide020/b10wave2/render-1.png").convert("L")).astype(int)

BANDS = [(3.42, 3.88), (4.32, 4.78), (5.14, 5.60), (6.00, 6.46)]
for i, (y0, y1) in enumerate(BANDS, 1):
    print(f"\n--- cream line {i}  (y {y0}-{y1} in) ---")
    for tag, a, sc in (("ORIG", O, S), ("REND", R, IN)):
        X0, X1, Y0, Y1 = (int(v * sc) for v in (9.10, 12.62, y0, y1))
        for thr in (128, 220):
            sub = a[Y0:Y1, X0:X1] < thr
            if not sub.any():
                print(f"  {tag} thr{thr}: no ink")
                continue
            ys, xs = np.where(sub)
            print(f"  {tag} thr{thr}: x {(xs.min()+X0)/sc:.3f}-{(xs.max()+X0)/sc:.3f} "
                  f"w={(xs.max()-xs.min())/sc:.3f}  n={sub.sum()}")
