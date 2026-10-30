#!/usr/bin/env python3
"""Slide 026 Template B crop-pair cutter (attempt 7, resume worker 2026-10-21).

Identical to cut_crops_6.py (same regions, same matched effective scale) but cut from
render_7.png. render_7 differs from render_6 ONLY in rowC: the closing paren is now
BLUE (x684..688) instead of red, and the red tail carries charSpacing 0.32 so it ends
at x682 (was x676.5). Nothing else moved (selfcheck_attempt_7.out proves every other
band/bar/disc delta is unchanged from attempt 6).
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
ORG = QA + "/../../../unique_slides/slide_026.jpg"
REN = QA + "/render_7.png"

ren = Image.open(REN).convert("RGB")
org = Image.open(ORG).convert("RGB")
WR, HR = ren.size
SX, SY = WR / 960.0, HR / 540.0
print("render %dx%d  SX %.4f SY %.4f | original %dx%d" % (WR, HR, SX, SY, org.size[0], org.size[1]))

REGIONS = {
    "alg":   (138, 135, 853, 270),
    "notes": (83, 302, 846, 502),
}

for name, (x0, y0, x1, y1) in REGIONS.items():
    rx0, ry0, rx1, ry1 = int(round(x0 * SX)), int(round(y0 * SY)), int(round(x1 * SX)), int(round(y1 * SY))
    rc = ren.crop((rx0, ry0, rx1, ry1))
    oc = org.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(QA + "/crop_7_%s_render.png" % name)
    oc.save(QA + "/crop_7_%s_orig.png" % name)
    fw, fh = x1 - x0, y1 - y0
    print("%-6s frame bbox x%d..%d y%d..%d (%dx%d) -> %dx%d px | effective scale ren %.4f/%.4f orig %.4f/%.4f"
          % (name, x0, x1, y0, y1, fw, fh, rc.size[0], rc.size[1],
             rc.size[0] / fw, rc.size[1] / fh, oc.size[0] / fw, oc.size[1] / fh))
    assert rc.size == oc.size, "crop sizes must match exactly"

with open(QA + "/crop_7_desc.txt", "w") as f:
    f.write("crop_7_alg   frame x138..853 y135..270 — GD algorithm steps [1]-[3]: four blue 17.5pt\n"
            "            lines (the [2] bullet wraps across two lines exactly as the original does),\n"
            "            underline bars rowB x350..717 y193 and rowD x288..472 y258, bold\n"
            "            'negative gradient' and 'almost zero', red tail 'AKA Learning Rate' x520..682\n"
            "            with the CLOSING PAREN now BLUE at x684..688 (attempt 7).\n"
            "crop_7_notes frame x83..846 y302..502 — 'Notes:' red header + two black bullets (five\n"
            "            lines with the blank-line gap between them), round discs d=7 at x91,\n"
            "            underline bars N3a x176..279 y458 and N3b x538..729 y458, bold\n"
            "            'is a convex function' / 'ONE Minimum' / 'Learning Rate'.\n"
            "Both crops matched effective scale: render crop taken from render_7.png (2001x1125,\n"
            "2.0844x / 2.0833y per frame px), original crop LANCZOS-upscaled to the render crop's\n"
            "exact pixel size. Both bboxes stay inside the blue box border (x82..864, y90..500).\n")
print("banked 4 crops + crop_7_desc.txt")
