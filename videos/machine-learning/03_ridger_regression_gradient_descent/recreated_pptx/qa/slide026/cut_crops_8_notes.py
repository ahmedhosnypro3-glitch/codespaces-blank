#!/usr/bin/env python3
"""Slide 026 Template B NOTES crop-pair cutter (attempt 8, resume worker 2026-10-21).

render_8 differs from render_7 ONLY in the N3 line (pixel diff: changed rows frame
y440..457 x139..837 = the N3 band; diff_render7_render8.out), so only the NOTES crop is
re-cut. The ALG crop (frame y135..270) is untouched by the change and its render_7 crops
stay valid evidence. Same REGION, same matched effective scale as cut_crops_6/7.
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
ORG = QA + "/../../../unique_slides/slide_026.jpg"
REN = QA + "/render_8.png"
ren = Image.open(REN).convert("RGB"); org = Image.open(ORG).convert("RGB")
WR, HR = ren.size
SX, SY = WR/960.0, HR/540.0
print("render %dx%d  SX %.4f SY %.4f | original %dx%d" % (WR, HR, SX, SY, org.size[0], org.size[1]))
x0, y0, x1, y1 = 83, 302, 846, 502   # notes region
rx0, ry0, rx1, ry1 = int(round(x0*SX)), int(round(y0*SY)), int(round(x1*SX)), int(round(y1*SY))
rc = ren.crop((rx0, ry0, rx1, ry1))
oc = org.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(QA + "/crop_8_notes_render.png"); oc.save(QA + "/crop_8_notes_orig.png")
print("notes frame bbox x%d..%d y%d..%d -> %dx%d px" % (x0, x1, y0, y1, rc.size[0], rc.size[1]))
assert rc.size == oc.size
# confirm the render's N3 word now carries 12 glyphs (no 'e') in the crop
a = np.asarray(rc).astype(int); s = rc.size[0]/(x1-x0)
print("crop effective scale %.4f; N3 word band (frame y441..456) shift check:" % s)
for i, row in enumerate(range(441, 457)):
    fr = a[int(round((row-y0)*s)):int(round((row+1-y0)*s)), int(round((170-x0)*s)):int(round((285-x0)*s))]
    ink = (fr.sum(axis=2) < 520).sum()
    print("   y%d ink cols in x170..285: %d" % (row, ink))
