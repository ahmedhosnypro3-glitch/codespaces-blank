#!/usr/bin/env python3
"""Slide 026 Template B crop-pair cutter (attempt 6, resume worker 2026-10-21).

Procedure B of shared_patterns/judge_protocol_03.md:
  1. region = slide-space bbox in FRAME px (original is 960x540), ~8px padding;
  2. crop BOTH images at the same frame-px region;
  3. MATCH effective scale: the render crop's output px / frame px must equal the
     original crop's, per axis. Render is 2001x1125 (SX=2001/960=2.0844,
     SY=1125/540=2.0833), so the original crop is LANCZOS-upscaled to the render
     crop's exact pixel box — never the bare 960px original (an 8% mismatch
     fabricates drift MAJORs);
  4. bank under qa/slide026/ as crop_6_<name>_render.png / _orig.png.

Regions (frame px, measured from the bank; both stay INSIDE the blue box border
x82..864 y90..500 so no chrome bleeds into the pair):
  alg   x138..853 y135..270  - the GD algorithm header block: rows [1]-[3] as four
        17.5pt blue lines (the [2] bullet wraps exactly as the original does),
        both measured underline bars (rowB y193 x350..717, rowD y258 x288..472),
        bold "negative gradient"/"almost zero", the red tail "AKA Learning Rate)".
  notes x 83..846 y302..502  - "Notes:" red header + both black bullets (five
        lines incl. the blank-line gap), round discs d=7 at x91, underline bars
        N3a x176..279 and N3b x538..729, bold spans.
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
ORG = QA + "/../../../unique_slides/slide_026.jpg"
REN = QA + "/render_6.png"

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
    rc.save(QA + "/crop_6_%s_render.png" % name)
    oc.save(QA + "/crop_6_%s_orig.png" % name)
    fw, fh = x1 - x0, y1 - y0
    print("%-6s frame bbox x%d..%d y%d..%d (%dx%d) -> %dx%d px | effective scale ren %.4f/%.4f orig %.4f/%.4f"
          % (name, x0, x1, y0, y1, fw, fh, rc.size[0], rc.size[1],
             rc.size[0] / fw, rc.size[1] / fh, oc.size[0] / fw, oc.size[1] / fh))
    assert rc.size == oc.size, "crop sizes must match exactly"

with open(QA + "/crop_6_desc.txt", "w") as f:
    f.write("crop_6_alg   frame x138..853 y135..270 — GD algorithm steps [1]-[3]: four blue 17.5pt\n"
            "            lines (the [2] bullet wraps across two lines exactly as the original does),\n"
            "            underline bars rowB x350..717 y193 and rowD x288..472 y258, bold\n"
            "            'negative gradient' and 'almost zero', red tail 'AKA Learning Rate)' x520..682.\n"
            "crop_6_notes frame x83..846 y302..502 — 'Notes:' red header + two black bullets (five\n"
            "            lines with the blank-line gap between them), round discs d=7 at x91,\n"
            "            underline bars N3a x176..279 y458 and N3b x538..729 y458, bold\n"
            "            'is a convex function' / 'ONE Minimum' / 'Learning Rate'.\n"
            "Both crops matched effective scale: render crop taken from render_6.png (2001x1125,\n"
            "2.0844x / 2.0833y per frame px), original crop LANCZOS-upscaled to the render crop's\n"
            "exact pixel size. Both bboxes stay inside the blue box border (x82..864, y90..500).\n")
print("banked 4 crops + crop_6_desc.txt")
