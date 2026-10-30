#!/usr/bin/env python3
"""Cut Procedure B crop pairs from render_8 at MATCHED effective scale (x2.0833).

Protocol: crop BOTH images at the same slide-space region; LANCZOS-upscale the
original crop by H_render/540 so output_px/frame_px is EQUAL for both images.
"""
from PIL import Image
import os

Q = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"
REND = f"{Q}/render_9.png"

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")
OW, OH = o.size
RW, RH = r.size
SX, SY = RW / OW, RH / OH
print(f"original {o.size} render {r.size} scaleX={SX:.6f} scaleY={SY:.6f}")

# slide-space regions (frame px, ~8px padding), from the prior lane's validated picks
REGIONS = [
    ("table_left",  58, 157, 480, 360,
     "outlier column + NO Regularizer column: headers, row groups 1-2, highlight band A"),
    ("table_right", 400, 157, 904, 530,
     "Ridge lambda=3 + Ridge lambda=10 columns: headers, all three row groups, bands A/B/C"),
    ("noreg_rows",  124, 199, 380, 485,
     "NO Regularizer column: all three row groups (the disputed y-value cells)"),
    ("header_strip", 58, 60, 904, 200,
     "title box + reference line + four column headers + outlier header"),
]

for name, x0, y0, x1, y1, desc in REGIONS:
    # render crop: exact integer render px
    rx0, ry0 = int(x0 * SX + 0.5), int(y0 * SY + 0.5)
    rx1, ry1 = int(x1 * SX + 0.5), int(y1 * SY + 0.5)
    rc = r.crop((rx0, ry0, rx1, ry1))
    # original crop: same frame px, then upscale to the SAME output size
    oc = o.crop((x0, y0, x1, y1))
    oc = oc.resize(rc.size, Image.LANCZOS)
    assert rc.size == oc.size, (rc.size, oc.size)
    assert abs(rc.size[0] / (x1 - x0) - SX) < 0.01 and abs(rc.size[1] / (y1 - y0) - SY) < 0.01
    rp, op = f"{Q}/crop_9_{name}_render.png", f"{Q}/crop_9_{name}_orig.png"
    rc.save(rp); oc.save(op)
    print(f"  {name:12s} frame x{x0}..{x1} y{y0}..{y1} -> {rc.size}  "
          f"eff-scale {rc.size[0]/(x1-x0):.4f}/{rc.size[1]/(y1-y0):.4f}  OK")
    print(f"      {desc}")
