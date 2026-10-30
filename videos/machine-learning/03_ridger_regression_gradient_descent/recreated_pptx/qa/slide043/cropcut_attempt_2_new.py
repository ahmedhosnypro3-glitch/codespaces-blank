#!/usr/bin/env python3
"""Procedure B crop cutter — slide 043, attempt 2 (S25 worker; written fresh).

Cuts render_2 and the original at the SAME slide-space bbox, LANCZOS-upscaling
the original to the render's effective scale. Regions (frame px):
  topband  — data table, Initial W vector, Step eta, class-check matrix, legend
  midleft  — augmented-vector box + Iteration-2 callout
  eqstack  — the 6 stacked calculation rows (densest region)
"""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{V}/recreated_pptx/qa/slide043"
ORIG = Image.open(f"{V}/unique_slides/slide_043.jpg").convert("RGB")
R = Image.open(f"{Q}/render_2.png").convert("RGB")
SX, SY = R.size[0] / 960.0, R.size[1] / 540.0

REGIONS = {
    "topband": (70, 50, 675, 132),
    "eqstack": (268, 133, 859, 535),
    "midleft": (60, 130, 260, 320),
}

for nm, (x0, y0, x1, y1) in REGIONS.items():
    oc = ORIG.crop((x0, y0, x1, y1))
    rc = R.crop((int(round(x0 * SX)), int(round(y0 * SY)),
                 int(round(x1 * SX)), int(round(y1 * SY))))
    w, h = rc.size
    up = oc.resize((w, h), Image.LANCZOS)
    assert up.size == rc.size, (up.size, rc.size)
    rc.save(f"{Q}/crop_2_{nm}_render.png")
    up.save(f"{Q}/crop_2_{nm}_orig.png")
    ex, ey = w / (x1 - x0), h / (y1 - y0)
    print(f"{nm}: frame {x1-x0}x{y1-y0} -> render crop {w}x{h}, orig upscaled {up.size}; "
          f"effective px/frame x={ex:.4f} (render {SX:.4f}) y={ey:.4f} (render {SY:.4f}) "
          f"-> {'MATCHED' if abs(ex-SX)<0.005 and abs(ey-SY)<0.005 else 'MISMATCH'}")
