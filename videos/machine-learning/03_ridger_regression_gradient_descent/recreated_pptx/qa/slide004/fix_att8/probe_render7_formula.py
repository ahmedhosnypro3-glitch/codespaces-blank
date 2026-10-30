#!/usr/bin/env python3
"""Sanity: measure render_7's actual formula ink extent vs the eqImage call
(171.54, 481.92, 3.682, 0.336) and vs the original's measured ink (x93..392, y470..502).
Mapping: render px -> slide px via /2.084375 (x) and /2.083333 (y)."""
import numpy as np
from PIL import Image

Q = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide004"
D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
SRX, SRY = 2001 / 960.0, 1125 / 540.0

r7 = np.asarray(Image.open(Q + "/render_7.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(D + "/unique_slides/slide_004.jpg").convert("RGB")).astype(int)

def ink_extent(img, x0, y0, x1, y1, tag, isrender):
    if isrender:
        im = img[int(y0 * SRY):int(y1 * SRY), int(x0 * SRX):int(x1 * SRX)]
        fx = lambda v: (v + int(x0 * SRX)) / SRX
        fy = lambda v: (v + int(y0 * SRY)) / SRY
    else:
        im = img[y0:y1, x0:x1]
        fx = lambda v: v + x0
        fy = lambda v: v + y0
    mx = im.max(axis=2)
    ink = mx < 160
    ys, xs = np.where(ink)
    if not len(ys):
        print(f"  {tag}: EMPTY")
        return
    print(f"  {tag}: ink n={len(ys)} slide-x {fx(xs.min()):.1f}..{fx(xs.max()):.1f} slide-y {fy(ys.min()):.1f}..{fy(ys.max()):.1f}")
    red = (im[:, :, 0] > im[:, :, 1] + 40) & (im[:, :, 0] > im[:, :, 2] + 40)
    ys2, xs2 = np.where(red)
    if len(ys2):
        print(f"    red n={len(ys2)} slide-x {fx(xs2.min()):.1f}..{fx(xs2.max()):.1f} slide-y {fy(ys2.min()):.1f}..{fy(ys2.max()):.1f}")

print("=== ORIGINAL formula band x60..420 y455..520 ===")
ink_extent(o, 60, 455, 420, 520, "ORIG", False)
print("=== RENDER_7 formula band x60..460 y455..535 ===")
ink_extent(r7, 60, 455, 460, 535, "REND7", True)
