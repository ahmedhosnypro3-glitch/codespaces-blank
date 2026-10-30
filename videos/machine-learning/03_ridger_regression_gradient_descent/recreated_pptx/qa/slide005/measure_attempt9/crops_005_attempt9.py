#!/usr/bin/env python3
"""Slide 005 Procedure B crop pairs, attempt 9 — render_9.png vs unique_slides/slide_005.jpg.
Law (judge_protocol_03.md §Procedure B): crop BOTH images at the SAME slide-space bbox
(~8px padding), LANCZOS-upscale the ORIGINAL crop so output_px/frame_px is EQUAL per axis
(render is 2001x1125 @150dpi -> sx = 2001/960 = 2.084375, sy = 1125/540 = 2.083333)."""
import numpy as np
from PIL import Image

D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = D + "/recreated_pptx/qa/slide005"
SX, SY = 2001/960.0, 1125/540.0

o = Image.open(D + "/unique_slides/slide_005.jpg").convert("RGB")
r = Image.open(Q + "/render_9.png").convert("RGB")

# (name, description, x0, y0, x1, y1) slide-space frame px, ~8px padding
REGIONS = [
 ("eq_stack",  "the three stacked Loss equations in the cream upper box", 88, 100, 650, 285),
 ("blue_upper", "upper-right blue Remember box: Remember label, X is a matrix/W is a vector, XW is a vector, and the transposed identity equation", 660, 128, 890, 245),
 ("pink_band", "the full-width pink band: the partial-Loss-fraction = 0 equation at the left and the 'Get Best W that minimizes the loss' text at the right", 65, 280, 515, 350),
 ("lower_eqs", "the two derivative equation chains in the cream lower box, the lower-right blue Remember box, and the green-outlined final W formula", 64, 350, 900, 530),
]

for name, desc, x0, y0, x1, y1 in REGIONS:
    rx = r.crop((int(round(x0*SX)), int(round(y0*SY)), int(round(x1*SX)), int(round(y1*SY))))
    oc = o.crop((x0, y0, x1, y1))
    tw, th = rx.size
    oc2 = oc.resize((tw, th), Image.LANCZOS)
    assert rx.size == oc2.size, (name, rx.size, oc2.size)
    rp = "%s/crop_9_%s_render.png" % (Q, name)
    op = "%s/crop_9_%s_orig.png" % (Q, name)
    rx.save(rp); oc2.save(op)
    print("crop_9_%-10s region x%d..%d y%d..%d (%dx%d frame px) -> %dx%d px  eff-scale %.4f/%.4f"
          % (name, x0, x1, y0, y1, x1-x0, y1-y0, tw, th, tw/(x1-x0), th/(y1-y0)))
    print("    desc: %s" % desc)
