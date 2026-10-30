#!/usr/bin/env python3
"""Slide 005 Procedure B crop pairs, attempt 15 — render_15.png vs original.
Attempt-15 fixes: eq2/eq4/eq5 assets untrimmed (left-edge clips) + remember1
Y-terminal. Regions as in crops_005_attempt13.py.
Law (judge_protocol_03.md §Procedure B): same slide-space bbox both sides,
original crop LANCZOS-upscaled to the render crop's exact pixel size."""
from PIL import Image

SCALE = 1125 / 540.0
D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = D + "/recreated_pptx/qa/slide005"

REGIONS = [
    ("eq_stack", "the three stacked Loss equations in the cream upper box", 88, 100, 650, 285),
    ("blue_upper", "upper-right blue Remember box: Remember label, X is a matrix/W is a vector, XW is a vector, and the transposed identity equation", 660, 128, 890, 245),
    ("pink_band", "the full-width pink band: the partial-Loss-fraction = 0 equation at the left and the 'Get Best W that minimizes the loss' text at the right", 65, 280, 515, 350),
    ("lower_eqs", "the two derivative equation chains in the cream lower box, the lower-right blue Remember box, and the green-outlined final W formula", 64, 350, 900, 530),
]

r = Image.open(Q + "/render_15.png")
o = Image.open(D + "/unique_slides/slide_005.jpg")
for name, desc, x0, y0, x1, y1 in REGIONS:
    rc = r.crop((int(x0 * SCALE), int(y0 * SCALE), int(x1 * SCALE), int(y1 * SCALE)))
    oc = o.crop((x0, y0, x1, y1))
    oc2 = oc.resize(rc.size, Image.LANCZOS)
    rc.save("%s/crop_15_%s_render.png" % (Q, name))
    oc2.save("%s/crop_15_%s_orig.png" % (Q, name))
    with open("%s/crop_15_%s_desc.txt" % (Q, name), "w") as f:
        f.write(desc + "\n")
    print("%-10s region x%d..%d y%d..%d -> %s (render) / %s (orig)"
          % (name, x0, x1, y0, y1, rc.size, oc2.size))
