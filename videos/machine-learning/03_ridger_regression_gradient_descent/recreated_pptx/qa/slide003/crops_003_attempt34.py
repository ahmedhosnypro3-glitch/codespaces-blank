#!/usr/bin/env python3
"""Slide 003 Procedure B crop pairs, attempt 34 — render_34.png vs unique_slides/slide_003.jpg.
Law (judge_protocol_03.md §Procedure B): crop BOTH images at the SAME slide-space bbox
(~8px padding), LANCZOS-upscale the ORIGINAL crop so output_px/frame_px is EQUAL per axis
(render is 2001x1125 @150dpi -> sx = 2001/960 = 2.084375, sy = 1125/540 = 2.083333).
Regions from cut_attempt_19.sh (the standing slide-003 crop set)."""
import numpy as np
from PIL import Image

D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = D + "/recreated_pptx/qa/slide003"
SX, SY = 2001/960.0, 1125/540.0

o = Image.open(D + "/unique_slides/slide_003.jpg").convert("RGB")
r = Image.open(Q + "/render_34.png").convert("RGB")

# (name, description, x0, y0, x1, y1) slide-space frame px, ~8px padding
REGIONS = [
 ("matrix",      "the bottom-left expanded-equation box: y-vector, '=', the 4-row colored matrix with nested parentheses, w-vector with b, and the three dimension labels", 74, 320, 538, 520),
 ("topbox",      "the top matrix-notation box: three colored column bands with entries, column parentheses, header dots column, red y-labels, and the separator line", 266, 105, 600, 305),
 ("sideboxes",   "the right-side Remember box (y = W^T X = X^T W) and the In General: N >>> d box", 640, 140, 903, 310),
 ("bottomright", "the bottom-right box: Y = XW heading, Where: X is a matrix, Y is labels vector", 538, 380, 903, 520),
]

for name, desc, x0, y0, x1, y1 in REGIONS:
    rx = r.crop((int(round(x0*SX)), int(round(y0*SY)), int(round(x1*SX)), int(round(y1*SY))))
    oc = o.crop((x0, y0, x1, y1))
    tw, th = rx.size
    oc2 = oc.resize((tw, th), Image.LANCZOS)
    assert rx.size == oc2.size, (name, rx.size, oc2.size)
    rp = "%s/crop_34_%s_render.png" % (Q, name)
    op = "%s/crop_34_%s_orig.png" % (Q, name)
    rx.save(rp); oc2.save(op)
    print("crop_34_%-10s region x%d..%d y%d..%d (%dx%d frame px) -> %dx%d px  eff-scale %.4f/%.4f"
          % (name, x0, x1, y0, y1, x1-x0, y1-y0, tw, th, tw/(x1-x0), th/(y1-y0)))
    print("    desc: %s" % desc)
