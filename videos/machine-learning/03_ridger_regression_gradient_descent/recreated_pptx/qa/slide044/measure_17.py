#!/usr/bin/env python3
"""Measure subscript glyph boxes: header row vs class row, both tables."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf
dark = LUM < 175
satred = (rf - gf > 45) & (rf - bf > 45) & (rf > 110)
satblue = (bf - rf > 40) & (bf - gf > 25) & (bf > 110)
ink = dark | satred | satblue

COLS = [99, 121, 143, 167, 190, 213]


def box(y0, y1, cx0, pad=3):
    reg = ink[y0:y1, cx0 - pad:cx0 + 7]
    ys, xs = np.where(reg)
    if not len(ys):
        return None
    return (cx0 - pad + int(xs.min()), cx0 - pad + int(xs.max()),
            y0 + int(ys.min()), y0 + int(ys.max()))


def report(label, y0, y1):
    print(f"--- {label} (y{y0}..{y1}) ---")
    for i, cx in enumerate(COLS):
        b = box(y0, y1, cx)
        if b:
            print(f"  col{i+1}: x{b[0]}..{b[1]} w{b[1]-b[0]+1}  y{b[2]}..{b[3]} h{b[3]-b[2]+1}")


report("T1 header subscripts", 63, 77)
report("T1 class-row subscripts", 117, 127)
report("T2 header subscripts", 146, 160)
report("T2 class-row subscripts", 236, 247)
