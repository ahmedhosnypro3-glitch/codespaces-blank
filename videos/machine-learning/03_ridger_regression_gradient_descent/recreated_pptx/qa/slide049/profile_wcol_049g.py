#!/usr/bin/env python3
"""Column ink profile of the bracket region, original vs render (frame px)."""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide049"
SX = 68.0 / 142.0
SY = 395.0 / 823.0


def prof(name, thr, fy0, fy1, label):
    a = np.asarray(Image.open(f"{QA}/{name}").convert("L"))
    cy0 = int(round((fy0 - 135) / SY))
    cy1 = int(round((fy1 - 135) / SY))
    band = a[cy0:cy1]
    print(f"\n--- {label} {name} thr{thr} band y{fy0}..{fy1} ---")
    # for each frame x in 715..752, count ink rows and print min/max row
    for fxv in np.arange(715.0, 753.0, 0.5):
        cx = int(round((fxv - 692) / SX))
        col = band[:, cx - 1:cx + 2]
        ys = np.where((col < thr).any(axis=1))[0]
        if len(ys) == 0:
            continue
        y0 = 135 + (cy0 + ys[0]) * SY
        y1 = 135 + (cy0 + ys[-1]) * SY
        print(f"  x={fxv:6.1f} n={len(ys):3d} y={y0:7.2f}..{y1:7.2f}")


prof("crop_9_wstack_orig.png", 205, 140, 205, "ORIG row1")
prof("crop_9_wstack_render.png", 150, 140, 205, "RENDER row1")
