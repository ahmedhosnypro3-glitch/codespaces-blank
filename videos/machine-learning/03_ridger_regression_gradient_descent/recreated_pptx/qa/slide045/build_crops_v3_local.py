#!/usr/bin/env python3
"""Slide 045: re-cut zoomed crop pairs from the CURRENT render_2.png (Procedure B).

The 01:27 crop pairs were cut from the superseded build_attempt_1 render; the
lane shipped build_attempt_2 at 02:49 and re-rendered render_2.png at 02:50.
The old crops are left banked untouched; the fresh pairs get suffix _r2.

Rule followed: crop-vs-crop ONLY, matched effective scale. Render crop is taken
at frame coords x (H_render/540) from render_2.png; the original crop is the same
frame-px bbox LANCZOS-upscaled by the SAME factor so output_px/frame_px is
equal on both axes.
"""
import os
from PIL import Image

NS = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide045"
RENDER = QA + "/render_2.png"
ORIG = NS + "/unique_slides/slide_045.jpg"

SUFFIX = "_r2"

# dense regions, frame px, ~8px padding (unchanged region definitions from
# build_crops.py / build_attempt_2.js measured geometry)
REGIONS = [
    ("calcs", 266, 131, 861, 536, "calculation panel: six ruled rows of dotted-product arithmetic with two bracket column vectors per row"),
    ("toppanel", 60, 46, 727, 137, "top worked-example panel: data table x1..x6, Initial W bracket vector, Step eta, check-classes matrix and pointer arrow"),
    ("augtable", 62, 132, 254, 263, "augmented vectors table with class row"),
]

rim = Image.open(RENDER).convert("RGB")
oim = Image.open(ORIG).convert("RGB")
RW, RH = rim.size
S = RH / 540.0
print("render %dx%d  scale=%.6f" % (RW, RH, S))

for name, x0, y0, x1, y1, desc in REGIONS:
    rx0, ry0 = int(round(x0 * S)), int(round(y0 * S))
    rx1, ry1 = int(round(x1 * S)), int(round(y1 * S))
    rc = rim.crop((rx0, ry0, rx1, ry1))
    oc = oim.crop((x0, y0, x1, y1))
    fw, fh = x1 - x0, y1 - y0
    oc2 = oc.resize((rc.width, rc.height), Image.LANCZOS)
    rp = QA + ("/crop_1%s_%s_render.png" % (SUFFIX, name))
    op = QA + ("/crop_1%s_%s_orig.png" % (SUFFIX, name))
    rc.save(rp)
    oc2.save(op)
    print("%-9s frame x%d..%d y%d..%d (%dx%d) -> render %dx%d, orig %dx%d (LANCZOS %.4fx)" %
          (name, x0, x1, y0, y1, fw, fh, rc.width, rc.height, oc2.width, oc2.height, oc2.width / fw))
    print("           effective scale render=%.5f orig=%.5f match=%s" %
          (rc.width / fw, oc2.width / fw, abs(rc.width / fw - oc2.width / fw) < 0.001))
    print("           region: %s" % desc)
