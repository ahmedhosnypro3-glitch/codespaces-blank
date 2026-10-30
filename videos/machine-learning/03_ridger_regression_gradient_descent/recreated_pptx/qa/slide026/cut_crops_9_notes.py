#!/usr/bin/env python3
"""Slide 026 Template B NOTES crop-pair cutter (attempt 9, resume worker 2026-10-21).

render_9 differs from render_8 ONLY in the N1 line (pixel diff probe_a9_verify.out: 20,190
changed px, bbox frame x 109.9..769.1 y 341.6..357.9 = the "Least Squares" bold fix), so
only the NOTES crop is re-cut. The ALG crop (frame y135..270) is untouched by the change and its render_7 crops
stay valid evidence. Same REGION, same matched effective scale as cut_crops_6/7.
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
ORG = QA + "/../../../unique_slides/slide_026.jpg"
REN = QA + "/render_9.png"
ren = Image.open(REN).convert("RGB"); org = Image.open(ORG).convert("RGB")
WR, HR = ren.size
SX, SY = WR/960.0, HR/540.0
print("render %dx%d  SX %.4f SY %.4f | original %dx%d" % (WR, HR, SX, SY, org.size[0], org.size[1]))
x0, y0, x1, y1 = 83, 302, 846, 502   # notes region
rx0, ry0, rx1, ry1 = int(round(x0*SX)), int(round(y0*SY)), int(round(x1*SX)), int(round(y1*SY))
rc = ren.crop((rx0, ry0, rx1, ry1))
oc = org.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(QA + "/crop_9_notes_render.png"); oc.save(QA + "/crop_9_notes_orig.png")
print("notes frame bbox x%d..%d y%d..%d -> %dx%d px" % (x0, x1, y0, y1, rc.size[0], rc.size[1]))
assert rc.size == oc.size
# confirm BOTH attempt-9 markers: N3 'approximatly' (12 glyphs) and the bold N1 stem
a = np.asarray(rc).astype(int); s = rc.size[0]/(x1-x0)
print("crop effective scale %.4f" % s)
print("N3 'approximatly' band (frame y441..456), ink px in x170..285:")
for row in range(441, 457):
    fr = a[int(round((row-y0)*s)):int(round((row+1-y0)*s)), int(round((170-x0)*s)):int(round((285-x0)*s))]
    print("   y%d ink=%d" % (row, (fr.sum(axis=2) < 520).sum()))
print("N1 'Least Squares' cap-zone stem ink (frame y342..354, x108..120):")
fr = a[int(round((342-y0)*s)):int(round((355-y0)*s)), int(round((108-x0)*s)):int(round((120-x0)*s))]
prof = fr.sum(axis=2)
print("   stem col ink:", [int((prof[:, i] < 430).sum()) for i in range(prof.shape[1])])
