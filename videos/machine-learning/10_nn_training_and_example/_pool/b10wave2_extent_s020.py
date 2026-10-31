#!/usr/bin/env python3
"""Slide 020: measure ink extent/centroid where strip + delta box + deriv panel.
Region declared in build/slide_020.js vs ink actually measured in render."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
R = np.array(Image.open(f"{NS}/qa/slide020/b10wave2/render-1.png").convert("L")).astype(int)
O = np.array(Image.open(f"{NS}/unique_slides/slide_020.jpg").convert("L")).astype(int)
RI = R < 128
OI = O < 128
IN = 2001 / 13.3333  # render px per in
S = 960 / 13.3333    # orig px per in


def report(nm, x0, y0, x1, y1):
    print(f"\n--- {nm} (region x {x0}-{x1} in, y {y0}-{y1} in) ---")
    for tag, ink, sc in (("ORIG", OI, S), ("REND", RI, IN)):
        X0, Y0, X1, Y1 = (int(v * sc) for v in (x0, y0, x1, y1))
        sub = ink[Y0:Y1, X0:X1]
        if not sub.any():
            print(f"  {tag}: NO INK")
            continue
        ys, xs = np.where(sub)
        lx, rx, ty, by = xs.min(), xs.max(), ys.min(), ys.max()
        print(f"  {tag}: ink px={sub.sum()} bbox x {lx/sc:.3f}-{rx/sc:.3f} in "
              f"(w={ (rx-lx)/sc:.3f})  y {ty/sc:.3f}-{by/sc:.3f} in (h={(by-ty)/sc:.3f})")
        # column histogram in 0.25in bins to see where ink distributes
        cols = sub.sum(axis=0)
        w = X1 - X0
        step = max(1, int(0.25 * sc))
        parts = [f"{int((i*step)/sc):.2f}in:{cols[i*step:(i+1)*step].sum()}"
                 for i in range(0, w // step)]
        print("        cols:", " ".join(parts))


# The whole where strip: box x 0.67-8.93, y 6.70-7.42
report("where strip (declared box)", 0.60, 6.60, 9.10, 7.50)
report("delta box (declared)", 0.80, 5.85, 6.13, 6.77)
report("cream deriv panel", 9.07, 3.30, 12.67, 6.75)
report("eq_mid1 row", 0.67, 3.42, 7.34, 3.86)
report("eq_mid2 row", 0.67, 4.32, 7.48, 5.00)
