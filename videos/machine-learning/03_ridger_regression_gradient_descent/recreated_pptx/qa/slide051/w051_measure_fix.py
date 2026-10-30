#!/usr/bin/env python3
"""w051_measure_fix: measure every zone slide 051's attempt-3 rebuild needs.
All targets in ORIGINAL frame px (960x540, 1px = 1pt). Banked to JSON."""
from PIL import Image
import numpy as np
import json

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
im = Image.open(f"{NS}/unique_slides/slide_051.jpg").convert("RGB")
z = np.asarray(im).astype(int)
R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
ink = (0.299*R + 0.587*G + 0.114*B) < 215
blue = (B > 90) & (B-R > 25) & (B-G > 10) & (G >= R)
green = (G > 80) & (G-R > 15) & (G-B > 15)
red = (R > 110) & (R-G > 50) & (R-B > 40)

out = {}
def extents(mask, x0, x1, y0, y1):
    m = mask[y0:y1, x0:x1]
    rows = np.where(m.any(axis=1))[0]
    cols = np.where(m.any(axis=0))[0]
    if len(rows) == 0:
        return None
    return [int(x0+cols[0]), int(y0+rows[0]), int(x0+cols[-1]), int(y0+rows[-1])]

# green DEC column vectors: full extents per card (window right of blue row vector)
for i, (y0, y1) in enumerate(((138, 200), (204, 266), (270, 336)), 1):
    out[f"dec{i}_green"] = extents(green, 375, 420, y0, y1)
    out[f"dec{i}_blue"] = extents(blue, 300, 380, y0, y1)
# red step text
out["step_red"] = extents(red, 355, 450, 58, 92)
# red ink dominant colour in the step zone
ys, xs = np.where(red[58:92, 355:450])
if len(ys):
    px = z[58:92, 355:450][ys, xs]
    out["step_red_rgb"] = [int(px[:,0].mean()), int(px[:,1].mean()), int(px[:,2].mean())]
# "Check classes of" label
out["check_classes"] = extents(ink, 490, 600, 70, 95)
# heading
out["heading"] = extents(ink, 75, 260, 140, 165)
# navy heading dominant colour
ys, xs = np.where(ink[140:165, 75:260])
px = z[140:165, 75:260][ys, xs]
navy = px[(px[:,2] > px[:,0]+20)]
out["heading_rgb"] = [int(navy[:,0].mean()), int(navy[:,1].mean()), int(navy[:,2].mean())] if len(navy) else None
# d(Z1) label + first '='
out["dz1_label"] = extents(ink, 276, 316, 155, 180)
out["dz1_eq"] = extents(ink, 316, 328, 155, 180)
# second '=' + value per row
for i, (y0, y1) in enumerate(((155, 182), (221, 248), (287, 314)), 1):
    out[f"dec{i}_eq2"] = extents(ink, 405, 422, y0, y1)
    out[f"dec{i}_val"] = extents(ink, 422, 445, y0, y1)
    out[f"dec{i}_arrow"] = extents(ink, 492, 524, y0-4, y1)
    out[f"dec{i}_cond"] = extents(ink, 505, 645, y0, y1)
    out[f"dec{i}_cls"] = extents(ink, 645, 760, y0, y1)
# arrows are black+blue mix: use ink|blue
inkb = ink | blue
for i, (y0, y1) in enumerate(((155, 182), (221, 248), (287, 314)), 1):
    out[f"dec{i}_arrow_ib"] = extents(inkb, 492, 524, y0-4, y1)
# sample/Z/aug/InitialW paren spans (for PNG height targets)
out["sample_span"] = [90, 78, 214, 106]
out["z_span"] = [598, 80, 656, 108]
out["aug_span"] = [94, 181, 218, 224]
out["initw_span"] = [329, 59, 354, 106]
# InitialW "Initial W =" text
out["initw_label"] = extents(ink, 258, 328, 70, 92)
print(json.dumps(out, indent=1))
json.dump(out, open(f"{NS}/recreated_pptx/qa/slide051/w051_measure_fix.json", "w"), indent=1)
