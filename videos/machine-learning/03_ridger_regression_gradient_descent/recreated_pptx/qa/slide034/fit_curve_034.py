#!/usr/bin/env python3
"""Fit slide_034 plot's coordinate transform from curve pixels + markers."""
import numpy as np
from PIL import Image

ROOT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
im = np.asarray(Image.open(ROOT + "/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
X0, X1, Y0, Y1 = 608, 847, 60, 312
box = im[Y0:Y1, X0:X1]
r, g, b = box[:, :, 0], box[:, :, 1], box[:, :, 2]

# cyan curve mask
cyan = (b - r > 55) & (g - r > 30) & (b > 140)
ys, xs = np.where(cyan)

def f(xd):
    return (xd**2 * np.cos(xd) - xd) / 10.0

# grid search affine maps: frame_x = a*d + bx ; frame_y = ay_f + by_f
# domain assumed [-12, 12]
best = None
for xd_min in np.arange(-13, -9, 0.5):
    for xd_max in np.arange(9, 14, 0.5):
        for yd_min in np.arange(-14, -8, 0.5):
            for yd_max in np.arange(6, 14, 0.5):
                a = (X1 - X0) / (xd_max - xd_min)
                bx = X0 - a * xd_min
                ay = (Y1 - Y0) / (yd_max - yd_min)
                by_f = Y0 - ay * yd_max
                # check every curve pixel
                d = (X0 + xs) - bx
                xd = (X0 + xs - bx) / a
                yexp = Y0 + ((Y1 - Y0) * (yd_min - f(xd)) / (yd_min - yd_max))
                # residual in frame px
                res = np.abs((Y0 + ys) - yexp)
                med = np.median(res)
                if best is None or med < best[0]:
                    best = (med, xd_min, xd_max, yd_min, yd_max)
print("best median residual %.1f px: x ∈[%.1f,%.1f] y∈[%.1f,%.1f]" % best)

_, xd_min, xd_max, yd_min, yd_max = best
a = (X1 - X0) / (xd_max - xd_min)
bx = X0 - a * xd_min
ay = (Y1 - Y0) / (yd_max - yd_min)
by_f = Y0 - ay * yd_max
print("frame_x = %.3f*domain_x + %.1f" % (a, bx))
print("frame_y = %.3f*domain_y + %.1f" % (ay, by_f))
print("x=0 axis at frame x %.0f ; y=0 axis at frame y %.0f"
      % (bx, by_f))
for fx in [617, 640, 660, 700, 740, 760, 780, 800, 820, 829]:
    dx = (fx - bx) / a
    print("frame x=%d -> domain %.2f, f=%.2f" % (fx, dx, f(dx)))
print()
for mk in [(741, 150), (771, 126), (783, 148)]:
    dx = (mk[0] - bx) / a
    dy = (mk[1] - by_f) / ay
    print("marker frame %s -> domain (%.2f, %.2f); f(%.2f)=%.2f"
          % (mk, dx, dy, dx, f(dx)))