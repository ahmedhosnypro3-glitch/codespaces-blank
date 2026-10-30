#!/usr/bin/env python3
"""Fit slide_034 plot scales once the axis positions are pinned."""
import numpy as np
from PIL import Image

ROOT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
im = np.asarray(Image.open(ROOT + "/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
X0, X1, Y0, Y1 = 608, 847, 60, 312
box = im[Y0:Y1, X0:X1]
r, g, b = box[:, :, 0], box[:, :, 1], box[:, :, 2]
cyan = (b - r > 55) & (g - r > 30) & (b > 140)

def f(xd):
    return (xd**2 * np.cos(xd) - xd) / 10.0

AX_X0 = 721.5   # y-axis (domain x=0) in frame px
AX_Y0 = 172      # x-axis (domain y=0) in frame px

best = None
for px_per_unit in np.arange(8.0, 12.0, 0.05):
    for ax0 in np.arange(715.0, 728.0, 0.5):
        xs, ys = [], []
        for fx in range(610, 845):
            xd = (fx - ax0) / px_per_unit
            col = np.where(cyan[:, fx - X0])[0]
            if len(col) >= 4:
                xs.append(xd); ys.append(np.median(col) + Y0)
        if len(xs) < 50:
            continue
        xs = np.array(xs); ys = np.array(ys)
        dy = f(xs)
        A = np.vstack([dy, np.ones_like(dy)]).T
        (a, b0), res, *_ = np.linalg.lstsq(A, ys, rcond=None)
        pred = A @ [a, b0]
        med = np.median(np.abs(pred - ys))
        if best is None or med < best[0]:
            best = (med, px_per_unit, ax0, a, b0, len(xs))

med, ppu, ax0, a, b0, n = best
print("n=%d  median residual %.2f px" % (n, med))
print("x: %.3f px/unit, y-axis at frame x %.1f" % (ppu, ax0))
print("y: frame_y = %.3f * domain_y + %.1f" % (a, b0))
print("domain y=0 -> frame y %.1f (axis measured 172)" % b0)
print("domain y scale: %.3f px/unit" % -a)
print("x tick -10 -> frame %.0f ; +10 -> frame %.0f"
      % (ax0 - 10 * ppu, ax0 + 10 * ppu))
print("x tick -6 -> %.0f ; -2 -> %.0f ; 2 -> %.0f ; 6 -> %.0f"
      % (ax0 - 6 * ppu, ax0 - 2 * ppu, ax0 + 2 * ppu, ax0 + 6 * ppu))
for yv in [12, 11, 10, 8, 6, 4, 2, 0, -2, -4, -6, -8, -10, -12]:
    print("  y=%4d -> frame y %.0f" % (yv, a * yv + b0))
