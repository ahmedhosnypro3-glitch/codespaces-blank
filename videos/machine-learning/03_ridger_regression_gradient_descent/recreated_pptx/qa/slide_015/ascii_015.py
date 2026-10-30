#!/usr/bin/env python3
r"""ASCII ink-map dump for slide 015 forensics (deck 03).

Prints a downsampled ink mask of a frame-px crop of the original so structure
(stacked fractions, underline bars, delimiters) can be read without a vision
model. Each char = `sx` x `sy` frame px; '#' = ink present in that block.

Usage: python3 ascii_015.py x0 y0 x1 y1 [sx] [sy]
"""
import sys
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_015.jpg"
LUM_THR = 190

rgb = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
lum = rgb.mean(axis=2)
ink = lum < LUM_THR

x0, y0, x1, y1 = (int(v) for v in sys.argv[1:5])
sx = int(sys.argv[5]) if len(sys.argv) > 5 else 2
sy = int(sys.argv[6]) if len(sys.argv) > 6 else 2

sub = ink[y0:y1, x0:x1]
h, w = sub.shape
print(f"crop x{x0}..{x1} y{y0}..{y1} ({w}x{h}px)  block {sx}x{sy}px  '#'=ink")
hdr = "".join(str((x0 + i * sx) // 100 % 10) for i in range(w // sx))
print("     " + hdr)
for by in range(0, h - sy + 1, sy):
    row = []
    for bx in range(0, w - sx + 1, sx):
        blk = sub[by:by + sy, bx:bx + sx]
        row.append("#" if blk.mean() > 0.30 else ("+" if blk.any() else "."))
    print(f"{y0 + by:4d} " + "".join(row))
