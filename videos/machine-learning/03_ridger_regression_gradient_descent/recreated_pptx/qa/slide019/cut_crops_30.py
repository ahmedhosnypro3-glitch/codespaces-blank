#!/usr/bin/env python3
"""Attempt 30 crop pairs from render_28 (post-a29-fix bytes) at matched scale.

Regions re-certified after the a29 adjudication fixes: y170 top-rule colour
segments + header fs16/indent + continuous λ3/λ10 rect edges + w3 0.99.
noreg_rows re-cut (the x130 RULE vline was removed; crop_23 PASS no longer
covers it). title_bar covers the y170/header band only.
"""
from PIL import Image
import os

os.chdir("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent")
Q = "recreated_pptx/qa/slide019"
ORIG = "unique_slides/slide_019.jpg"
REND = f"{Q}/render_28.png"

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")
OW, OH = o.size
RW, RH = r.size
SX, SY = RW / OW, RH / OH
print(f"original {o.size} render {r.size} scaleX={SX:.6f} scaleY={SY:.6f}")

REGIONS = [
    ("title_bar",   58, 157, 480, 203,
     "top rule y170 + the four column headers (fs16, indented): navy/red/green segments"),
    ("table_left",  58, 157, 480, 360,
     "outlier column + NO Regularizer column: headers, row groups 1-2, highlight band A"),
    ("table_right", 400, 157, 904, 530,
     "Ridge lambda=3 + Ridge lambda=10 columns: continuous red/green rect edges, all three row groups, bottom tint strip"),
    ("noreg_rows",  124, 199, 380, 485,
     "NO REG W-vectors + test grids for all three row groups (x130 rule removed)"),
]

for name, x0, y0, x1, y1, desc in REGIONS:
    rx0, ry0 = int(x0 * SX + 0.5), int(y0 * SY + 0.5)
    rx1, ry1 = int(x1 * SX + 0.5), int(y1 * SY + 0.5)
    rc = r.crop((rx0, ry0, rx1, ry1))
    oc = o.crop((x0, y0, x1, y1))
    oc = oc.resize(rc.size, Image.LANCZOS)
    assert rc.size == oc.size, (rc.size, oc.size)
    assert abs(rc.size[0] / (x1 - x0) - SX) < 0.01 and abs(rc.size[1] / (y1 - y0) - SY) < 0.01
    rc.save(f"{Q}/crop_30_{name}_render.png")
    oc.save(f"{Q}/crop_30_{name}_orig.png")
    print(f"  {name:12s} frame x{x0}..{x1} y{y0}..{y1} -> {rc.size}  eff-scale "
          f"{rc.size[0]/(x1-x0):.4f}/{rc.size[1]/(y1-y0):.4f}  OK")
    print(f"      {desc}")
