#!/usr/bin/env python3
"""Slide 025 Procedure B: cut render/original crop pairs at matched effective
scale for the zoomed judge (deck 03 shared_patterns/judge_protocol_03.md).

 scale S = H_render/540 (1125/540 = 2.083333... render-px per frame-px)
 render crop = render[y0*S:y1*S, x0*S:x1*S]
 orig  crop = LANCZOS-upscale of orig[y0:y1, x0:x1] by S  -> same effective scale
Writes qa/slide025/crop_11_<name>_render.png / crop_11_<name>_orig.png and prints
the verified output_px/frame_px ratio per axis (must be equal for both).
"""
import os
import numpy as np
from PIL import Image

DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide_025"
RENDER = QA + "/render_11.png"
ORIG = DECK + "/unique_slides/slide_025.jpg"

rend = Image.open(RENDER).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
S = rend.size[1] / 540.0
print("render %s  scale S=%.6f" % (rend.size, S))

# (name, x0, y0, x1, y1) in frame px, ~8px padding around each dense region
REGIONS = {
    "title":     (250,  55, 600,  95),
    "lbl_upper": (260, 130, 620, 232),
    "lbl_lower": (372, 346, 620, 497),
    "tl":        ( 78, 108, 290, 295),
    "tr":        (608, 108, 886, 324),
    "bl":        ( 78, 284, 383, 533),
    "br":        (606, 338, 886, 538),
}

for name, (x0, y0, x1, y1) in REGIONS.items():
    rc = rend.crop((round(x0 * S), round(y0 * S), round(x1 * S), round(y1 * S)))
    ow, oh = x1 - x0, y1 - y0
    oc = orig.crop((x0, y0, x1, y1)).resize(
        (round(ow * S), round(oh * S)), Image.LANCZOS)
    rx = rc.size[0] / ow
    ry = rc.size[1] / oh
    ox = oc.size[0] / ow
    oy = oc.size[1] / oh
    ok = abs(rx - ox) < 0.01 and abs(ry - oy) < 0.01
    rc.save("%s/crop_11_%s_render.png" % (QA, name))
    oc.save("%s/crop_11_%s_orig.png" % (QA, name))
    print("  %-10s frame %4dx%-4d  render %dx%d (%.4f,%.4f)  orig %dx%d (%.4f,%.4f)  MATCHED=%s"
          % (name, ow, oh, rc.size[0], rc.size[1], rx, ry,
             oc.size[0], oc.size[1], ox, oy, ok))
