#!/usr/bin/env python3
"""Crop-pair preparation for slide 048, render_10 (150dpi) — same regions as the
banked crop_9 pairs (frame px), re-cut from the current render after the
initial-W asset fix. Orig upscaled LANCZOS to the render crop's exact size."""
import os, sys
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent")
QA = os.path.join(NS, "recreated_pptx/qa/slide048")
ORIG = os.path.join(NS, "unique_slides/slide_048.jpg")

REGIONS = [
    ("top_band", 60, 46, 730, 138),
    ("aug_iter", 78, 141, 332, 311),
    ("calc_panel", 486, 140, 800, 532),
]

K = sys.argv[1] if len(sys.argv) > 1 else "10"
render_png = os.path.join(QA, "render_%s.png" % K)

r = Image.open(render_png).convert("RGB")
o = Image.open(ORIG).convert("RGB")
SC = r.size[1] / 540.0
print("render %dx%d  scale=%.4f" % (r.size[0], r.size[1], SC))

for name, x0, y0, x1, y1 in REGIONS:
    rc = r.crop((int(x0 * SC), int(y0 * SC), int(np.ceil(x1 * SC)), int(np.ceil(y1 * SC))))
    oc = o.crop((x0, y0, x1, y1))
    oc = oc.resize(rc.size, Image.LANCZOS)
    rc.save(os.path.join(QA, "crop_%s_%s_render.png" % (K, name)))
    oc.save(os.path.join(QA, "crop_%s_%s_orig.png" % (K, name)))
    print("%-10s render %s  orig %s  eff=%.2f/%.2f" %
          (name, rc.size, oc.size, rc.size[0] / (x1 - x0), oc.size[0] / (x1 - x0)))
