#!/usr/bin/env python3
"""probe73 — Template B crop-pair cutter for attempt 7 (K=6), slide 009.

Derived from probe59_crops.py (frozen-law implementation of Procedure B in
shared_patterns/judge_protocol_03.md). Only two things changed:
  - REND = render_7.png  (attempt 7: founder-annotation fix + restored chrome)
  - two extra dense regions for the annotation corridors themselves, which are
    the subject of the founder's 2026-10-25 directive (graph annotations).

Every region's ORIGINAL crop is LANCZOS-upscaled to EXACTLY the render crop's
pixel size, so output_px/frame_px is equal per axis by construction.

Run: python3 probe73_crops_6.py   (writes probe73_crops_6.txt)
"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ORIG = os.path.join(DECK, "unique_slides", "slide_009.jpg")
REND = os.path.join(HERE, "render_7.png")
K = 6

REGIONS = [
    ("eq_left",    208,   140,   325,   183,
     "LEFT chart annotation box holding the black equation 50.85^2 = 2585; the founder-corrected red dimension shaft clips this box's lower-left corner"),
    ("eq_right",   625,   140,   742,   183,
     "RIGHT chart annotation box holding the black equation 63.64^2 = 4050; the founder-corrected red dimension shaft clips this box's lower-left corner"),
    ("cap_left",   100,   480,   427,   527,
     "LEFT chart's two caption lines: red 'Overfit' keyword + '(try to minimize the residuals ONLY)' over 'Fails to detect the Pattern'"),
    ("cap_right",  515,   480,   827,   527,
     "RIGHT chart's two caption lines: red 'Generalized' keyword + '(Residuals are not minimized)' over 'Successes to detect the Pattern'"),
    ("chart_left",  87,   102,   473,   480,
     "LEFT scatter chart: navy border, 16x16 grid, red axes + arrowheads, blue fitted line, orange points, and the rebuilt red mm-annotation (double-headed arrow orthogonal to the blue line, label along the arrow, plain parallel leader beside the outlier)"),
    ("chart_right", 478,  102,   878,   480,
     "RIGHT scatter chart: navy border, 16x16 grid, red axes + arrowheads, blue fitted line, orange points, and the rebuilt red mm-annotation (double-headed arrow orthogonal to the blue line, label along the arrow, plain parallel leader beside the outlier)"),
    ("annotation_left", 150, 125, 340, 330,
     "LEFT chart mm-annotation corridor: the red dimension arrow (orthogonal to the blue fitted line, foot ON the line, arrowheads at BOTH ends), the '50.85 mm' label running ALONG that arrow, the plain parallel red leader through the outlier (NO arrowhead), and the orange outlier point"),
    ("annotation_right", 555, 125, 765, 390,
     "RIGHT chart mm-annotation corridor: the red dimension arrow (orthogonal to the blue fitted line, foot ON the line, arrowheads at BOTH ends), the '63.64 mm' label running ALONG that arrow, the plain parallel red leader through the outlier (NO arrowhead), and the orange outlier point"),
]

ren = Image.open(REND).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
RW, RH = ren.size
SY = RH / 540.0
SX = RW / 960.0

print("render %dx%d  scale x %.5f y %.5f   original %dx%d  (K=%d)"
      % (RW, RH, SX, SY, orig.size[0], orig.size[1], K))
print("prescribed original upscale H_render/540 = %.5f" % SY)
print()

for name, x0, y0, x1, y1, desc in REGIONS:
    rb = (int(round(x0 * SX)), int(round(y0 * SY)),
          int(round(x1 * SX)), int(round(y1 * SY)))
    rc = ren.crop(rb)
    ob = (int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))
    oc = orig.crop(ob).resize(rc.size, Image.LANCZOS)
    assert oc.size == rc.size, (name, rc.size, oc.size)
    rc.save(os.path.join(HERE, "crop_%d_%s_render.png" % (K, name)))
    oc.save(os.path.join(HERE, "crop_%d_%s_orig.png" % (K, name)))
    print("%-16s region %4dx%-4d frame px -> %dx%d crop px"
          % (name, x1 - x0, y1 - y0, rc.size[0], rc.size[1]))
    print("                 %s" % desc)

print()
print("== matched-scale audit (re-opened from disk) ==")
bad = []
for name, x0, y0, x1, y1, desc in REGIONS:
    r = Image.open(os.path.join(HERE, "crop_%d_%s_render.png" % (K, name)))
    o = Image.open(os.path.join(HERE, "crop_%d_%s_orig.png" % (K, name)))
    w_f, h_f = x1 - x0, y1 - y0
    same = (r.size == o.size)
    near = (abs(r.size[0] / w_f - SX) < 0.03 and abs(r.size[1] / h_f - SY) < 0.03)
    ok = same and near
    print("  %-16s %dx%d vs %dx%d  identical=%-5s  x %.4f y %.4f (target %.4f/%.4f)  %s"
          % (name, r.size[0], r.size[1], o.size[0], o.size[1], same,
             r.size[0] / w_f, r.size[1] / h_f, SX, SY, "OK" if ok else "MISMATCH"))
    if not ok:
        bad.append(name)
print()
print("crops cut: %d   scale mismatches: %d" % (len(REGIONS), len(bad)))
print("VERDICT:", "PASS" if not bad else "FAIL")
