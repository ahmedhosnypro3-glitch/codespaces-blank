#!/usr/bin/env python3
"""Slide 005 Procedure B crop pair, attempt 14 — render_14.png vs unique_slides/slide_005.jpg.
Only the lower_eqs region is re-cut: the remember2 equation asset was regenerated
(X-terminal), and that box (x656..873, y372..423) lives inside lower_eqs.
Law (judge_protocol_03.md §Procedure B): same slide-space bbox both sides, original
crop LANCZOS-upscaled to the render crop's exact pixel size."""
from PIL import Image

SCALE = 1125 / 540.0
D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = D + "/recreated_pptx/qa/slide005"

REGIONS = {"lower_eqs": (64, 350, 900, 530)}

r = Image.open(Q + "/render_14.png")
o = Image.open(D + "/unique_slides/slide_005.jpg")
for name, (x0, y0, x1, y1) in REGIONS.items():
    rc = r.crop((int(x0 * SCALE), int(y0 * SCALE), int(x1 * SCALE), int(y1 * SCALE)))
    oc = o.crop((x0, y0, x1, y1))
    oc2 = oc.resize(rc.size, Image.LANCZOS)
    rc.save("%s/crop_14_%s_render.png" % (Q, name))
    oc2.save("%s/crop_14_%s_orig.png" % (Q, name))
    print("%s region x%d..%d y%d..%d -> %s (render) / %s (orig)"
          % (name, x0, x1, y0, y1, rc.size, oc2.size))
