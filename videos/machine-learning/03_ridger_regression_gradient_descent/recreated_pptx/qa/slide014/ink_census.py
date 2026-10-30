#!/usr/bin/env python3
"""Ink census + vertical balance for slide014 attempt 3, measured on BOTH images.
Penalty-free measurement only: counts dark-ink pixels inside identical frame-px
bboxes and reports the first/last inked row (top-heavy text = lines hugging the
band top).
"""
import json

import numpy as np
from PIL import Image

Q = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014"
o = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{Q}/render_3.png").convert("RGB")).astype(int)
SC = r.shape[0] / 540.0

io = o.sum(axis=2) < 660
ir = r.sum(axis=2) < 660

REGIONS = {
    "title": (48, 55, 880, 108),
    "left_vector_box": (80, 105, 450, 232),
    "right_vector_box": (500, 105, 899, 232),
    "ridge_band": (60, 250, 903, 279),
    "objective_band": (60, 308, 903, 336),
    "mid_zone_peach": (80, 405, 471, 444),
    "mid_zone_yellow": (533, 405, 882, 444),
    "loss_term": (80, 468, 450, 523),
    "reg_term": (500, 468, 899, 523),
    "final_band": (60, 504, 903, 524),
}

print(f"{'region':18s} {'orig_ink':>9s} {'rend_ink':>9s} {'ratio':>6s}   {'o_y':>12s} {'r_y':>12s}")
res = {}
for k, (x0, y0, x1, y1) in REGIONS.items():
    ao = io[y0:y1, x0:x1]
    ar = ir[int(y0 * SC):int(y1 * SC), int(x0 * SC):int(x1 * SC)]
    a, b = int(ao.sum()), int(ar.sum())
    oy = oyr = "-"
    if ao.any():
        ry = np.where(ao.any(axis=1))[0]
        oy = f"{y0 + ry.min()}..{y0 + ry.max()}"
    if ar.any():
        rr = np.where(ar.any(axis=1))[0]
        oyr = f"{y0 + rr.min()/SC:.0f}..{y0 + rr.max()/SC:.0f}"
    res[k] = {"orig_ink": a, "rend_ink": b, "orig_y": oy, "rend_y": oyr}
    print(f"{k:18s} {a:9d} {b:9d} {(b / a if a else float('inf')):6.2f}   {oy:>12s} {oyr:>12s}")

with open(f"{Q}/ink_census_attempt3.json", "w") as f:
    json.dump(res, f, indent=1)

# title region: does the text overflow past its band / collide with the badge?
print()
tb = io[55:108, 48:880]
tbr = ir[int(55 * SC):int(108 * SC), int(48 * SC):int(880 * SC)]
print("title ink rows orig:", np.where(tb.any(axis=1))[0].min() + 55,
      np.where(tb.any(axis=1))[0].max() + 55,
      "| render:", int((np.where(tbr.any(axis=1))[0].min()/SC + 55)),
      int((np.where(tbr.any(axis=1))[0].max()/SC + 55)))
# badge collision check: any title ink under/over the badge bbox?
bx0, by0, bx1, by1 = 858, 55, 895, 92
print("ink in badge overlap orig:", int(io[by0:by1, bx0:bx1].sum()),
      "| render:", int(ir[int(by0 * SC):int(by1 * SC), int(bx0 * SC):int(bx1 * SC)].sum()))
