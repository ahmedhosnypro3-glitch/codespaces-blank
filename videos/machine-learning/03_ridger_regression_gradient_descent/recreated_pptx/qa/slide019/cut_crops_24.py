#!/usr/bin/env python3
"""Cut Procedure B crop pairs from render_23 at MATCHED effective scale (x2.0843).

Same validated regions as cut_crops_10v2 / crop_18/19 rounds; render_24 = post-fix
bytes (outlierRow single-line digit boxes 9/9 colored, W-enclosure + grid outer
rects maroon).
"""
from PIL import Image
import os

os.chdir("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent")
Q = "recreated_pptx/qa/slide019"
ORIG = "unique_slides/slide_019.jpg"
REND = f"{Q}/render_24.png"

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")
OW, OH = o.size
RW, RH = r.size
SX, SY = RW / OW, RH / OH
print(f"original {o.size} render {r.size} scaleX={SX:.6f} scaleY={SY:.6f}")

REGIONS = [
    ("table_left",  58, 157, 480, 360,
     "outlier column + NO Regularizer column: headers, row groups 1-2, highlight band A"),
    ("table_right", 400, 157, 904, 530,
     "Ridge lambda=3 + Ridge lambda=10 columns: headers, all three row groups, bands A/B/C, bottom tint strip"),
    ("noreg_rows",  124, 199, 380, 485,
     "NO Regularizer column: all three row groups (the disputed y-value cells)"),
    ("header_strip", 58, 60, 904, 200,
     "title box + reference line + four column headers + outlier header"),
]

for name, x0, y0, x1, y1, desc in REGIONS:
    rx0, ry0 = int(x0 * SX + 0.5), int(y0 * SY + 0.5)
    rx1, ry1 = int(x1 * SX + 0.5), int(y1 * SY + 0.5)
    rc = r.crop((rx0, ry0, rx1, ry1))
    oc = o.crop((x0, y0, x1, y1))
    oc = oc.resize(rc.size, Image.LANCZOS)
    assert rc.size == oc.size, (rc.size, oc.size)
    assert abs(rc.size[0] / (x1 - x0) - SX) < 0.01 and abs(rc.size[1] / (y1 - y0) - SY) < 0.01
    rc.save(f"{Q}/crop_24_{name}_render.png")
    oc.save(f"{Q}/crop_24_{name}_orig.png")
    print(f"  {name:12s} frame x{x0}..{x1} y{y0}..{y1} -> {rc.size}  eff-scale "
          f"{rc.size[0]/(x1-x0):.4f}/{rc.size[1]/(y1-y0):.4f}  OK")
    print(f"      {desc}")
