#!/usr/bin/env python3
"""Slide 045: bank zoomed crop pairs at MATCHED effective scale (Procedure B).

Render crop: frame coords x (H_render/540) from render_K.png.
Original crop: same frame bbox from the 960x540 original, LANCZOS-upscaled by the
same factor so output_px/frame_px is equal on both axes.
"""
import os
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide045"
RENDER = os.path.join(QA, "render_1.png")
ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_045.jpg"

# dense regions, frame px, ~8px padding
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
    # render crop (nearest-exact: multiply then box-round)
    rx0, ry0 = int(round(x0 * S)), int(round(y0 * S))
    rx1, ry1 = int(round(x1 * S)), int(round(y1 * S))
    rc = rim.crop((rx0, ry0, rx1, ry1))
    # original crop at frame px, upscaled to the SAME output size (matched scale)
    oc = oim.crop((x0, y0, x1, y1))
    fw, fh = x1 - x0, y1 - y0
    oc2 = oc.resize((rc.width, rc.height), Image.LANCZOS)
    rp = os.path.join(QA, "crop_1_%s_render.png" % name)
    op = os.path.join(QA, "crop_1_%s_orig.png" % name)
    rc.save(rp)
    oc2.save(op)
    print("%-9s frame x%d..%d y%d..%d (%dx%d)  -> render crop %dx%d, orig crop %dx%d (LANCZOS %.4fx)" %
          (name, x0, x1, y0, y1, fw, fh, rc.width, rc.height, oc2.width, oc2.height, oc2.width / fw))
    print("           effective scale render=%.4f orig=%.4f (must match)" %
          (rc.width / fw, oc2.width / fw))
    print("           region: %s" % desc)
