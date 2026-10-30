#!/usr/bin/env python3
"""Slide 025 attempt-12 crop pairs: cut render/original crops at matched
effective scale from the CURRENT render (render_3 = render of the current
slide_025_recreated.pptx, assets md5-verified) vs unique_slides/slide_025.jpg.

 scale S = H_render/540; render crop = render[y0*S:y1*S, x0*S:x1*S];
 orig crop = LANCZOS-upscale of orig[y0:y1, x0:x1] by S.
Regions = same frame-px boxes as cut_crops_14.py (title/tl/tr/bl/br).
"""
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide025"
RENDER = QA + "/render_3.png"
ORIG = NS + "/unique_slides/slide_025.jpg"

rend = Image.open(RENDER).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
S = rend.size[1] / 540.0
print("render %s  scale S=%.6f" % (rend.size, S))

REGIONS = {
    "title": (250,  55, 600,  95),
    "tl":    ( 78, 108, 290, 295),
    "tr":    (608, 108, 886, 324),
    "bl":    ( 78, 284, 383, 533),
    "br":    (606, 338, 886, 538),
}

for name, (x0, y0, x1, y1) in REGIONS.items():
    rc = rend.crop((round(x0 * S), round(y0 * S), round(x1 * S), round(y1 * S)))
    ow, oh = x1 - x0, y1 - y0
    oc = orig.crop((x0, y0, x1, y1)).resize(
        (round(ow * S), round(oh * S)), Image.LANCZOS)
    ok = abs(rc.size[0] / ow - oc.size[0] / ow) < 0.01 and \
         abs(rc.size[1] / oh - oc.size[1] / oh) < 0.01
    rc.save("%s/crop_12_%s_render.png" % (QA, name))
    oc.save("%s/crop_12_%s_orig.png" % (QA, name))
    print("  %-6s frame %4dx%-4d render %dx%d orig %dx%d MATCHED=%s"
          % (name, ow, oh, rc.size[0], rc.size[1], oc.size[0], oc.size[1], ok))
