#!/usr/bin/env python3
"""Procedure B crop-pair preparation for slide 050.

Regions (frame px, ~8px padding) chosen from the ORIGINAL frame for the densest
content regions:
  chart   — x310..826, y171..483  (scatter + decision line + annotations + ticks)
  tableeq — x60..722, y50..250    (navy box: data table + math zone + vectors)
  pinkbox — x735..836, y52..178   (pink W-vector box)
  redstop — x60..240, y270..400   (red iteration badge + stop text)

Render crop source: qa/slide050/render_K.png (150dpi).
Original crop source: unique_slides/slide_050.jpg, LANCZOS-upscaled by
H_render/540 so the effective scales match (output_px / frame_px equal per axis).
"""
import os
import sys

import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
NS = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent")
QA = os.path.join(NS, "recreated_pptx/qa/slide050")
ORIG = os.path.join(NS, "unique_slides/slide_050.jpg")

REGIONS = [
    ("chart", 310, 171, 826, 483),
    ("tableeq", 60, 50, 722, 250),
    ("pinkbox", 735, 52, 836, 178),
    ("redstop", 60, 270, 240, 400),
]

K = sys.argv[1] if len(sys.argv) > 1 else "2"
render_png = os.path.join(QA, "render_%s.png" % K)

r = Image.open(render_png).convert("RGB")
o = Image.open(ORIG).convert("RGB")
H_render = r.size[1]
SC = H_render / 540.0
print("render %dx%d  scale=%.4f" % (r.size[0], H_render, SC))

for name, x0, y0, x1, y1 in REGIONS:
    # render crop: multiply frame coords by SC
    rc = r.crop((int(x0 * SC), int(y0 * SC), int(np.ceil(x1 * SC)), int(np.ceil(y1 * SC))))
    # original crop at the same frame-px box, then upscale to the same output size
    oc = o.crop((x0, y0, x1, y1))
    oc = oc.resize(rc.size, Image.LANCZOS)
    rp = os.path.join(QA, "crop_%s_%s_render.png" % (K, name))
    op = os.path.join(QA, "crop_%s_%s_orig.png" % (K, name))
    rc.save(rp)
    oc.save(op)
    eff_r = rc.size[0] / (x1 - x0)
    eff_o = oc.size[0] / (x1 - x0)
    print("%-8s render %s  orig %s  effective scale render=%.2f orig=%.2f  (matched=%s)"
          % (name, rc.size, oc.size, eff_r, eff_o, "YES" if abs(eff_r - eff_o) < 0.02 else "NO"))
