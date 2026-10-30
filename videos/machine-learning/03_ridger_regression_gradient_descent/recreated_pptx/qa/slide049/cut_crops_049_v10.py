#!/usr/bin/env python3
"""Crop-pair preparation for slide 049, render_10 (150dpi).

Regions (frame px) chosen from the ORIGINAL frame for the densest content regions:
  top_band  x60..740  y50..135   (top box: x1..x6 table + Initial W + REPEAT + Check classes + Z-grid)
  aug_box   x60..255  y132..260  (augmented vectors box + C1/C2 tags)
  legend    x230..522 y98..134   (C1 positive C2 negative Zero is unaccepted)
  calc_rows x270..860 y140..528  (six d(x) rows: digits, bracket column, results, arrows, W columns)
  iter_stop x60..260  y265..405  (Iteration 2 box, No change in W, Stop Iterations)

Original crop source: unique_slides/slide_049.jpg, LANCZOS-upscaled to the render
crop's exact size so effective scales match (Procedure B).
"""
import os
import sys

import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent")
QA = os.path.join(NS, "recreated_pptx/qa/slide049")
ORIG = os.path.join(NS, "unique_slides/slide_049.jpg")

REGIONS = [
    ("top_band", 60, 50, 740, 135),
    ("aug_box", 60, 132, 255, 260),
    ("legend", 230, 98, 522, 134),
    ("calc_rows", 270, 140, 860, 528),
    ("iter_stop", 60, 265, 260, 405),
]

K = sys.argv[1] if len(sys.argv) > 1 else "10"
render_png = os.path.join(QA, "render_%s.png" % K)

r = Image.open(render_png).convert("RGB")
o = Image.open(ORIG).convert("RGB")
H_render = r.size[1]
SC = H_render / 540.0
print("render %dx%d  scale=%.4f" % (r.size[0], H_render, SC))

for name, x0, y0, x1, y1 in REGIONS:
    rc = r.crop((int(x0 * SC), int(y0 * SC), int(np.ceil(x1 * SC)), int(np.ceil(y1 * SC))))
    oc = o.crop((x0, y0, x1, y1))
    oc = oc.resize(rc.size, Image.LANCZOS)
    rp = os.path.join(QA, "crop_%s_%s_render.png" % (K, name))
    op = os.path.join(QA, "crop_%s_%s_orig.png" % (K, name))
    rc.save(rp)
    oc.save(op)
    print("%-9s render %s  orig %s  eff=%.2f/%.2f matched=%s"
          % (name, rc.size, oc.size, rc.size[0] / (x1 - x0), oc.size[0] / (x1 - x0),
             "YES" if abs(rc.size[0] / (x1 - x0) - oc.size[0] / (x1 - x0)) < 0.02 else "NO"))
