#!/usr/bin/env python3
"""Slide 009 — Template B crop-pair cutter, attempt K=2 (Procedure B).

Re-cuts the regions whose pixels CHANGED in attempt 2 (the two equation-box
fills and the caption band incl. the restored rose marks) from render_2.png,
and re-banks the two chart crops verbatim from render_1.png — proven
pixel-identical across the rebuild by the diff in adjudication_attempt_2.py
(0 px changed outside the fix regions), so per judge_protocol_03.md those two
crop transcripts may be kept. Effective scale is matched PER AXIS BY
CONSTRUCTION: the original crop is LANCZOS-upscaled to EXACTLY the render
crop's pixel size, so output_px/frame_px is identical for both images.
"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ORIG = os.path.join(DECK, "unique_slides", "slide_009.jpg")
R2 = os.path.join(HERE, "render_2.png")
R1 = os.path.join(HERE, "render_1.png")

# name, x0, y0, x1, y1, source render, description
# Caption regions are widened from attempt 1 (y480..527) to include the full
# restored mark geometry: LEFT x95..433 y502..530, RIGHT x502..842 y480..530.
REGIONS = [
    ("eq_left",    208, 140, 325, 183, R2,
     "LEFT chart annotation box holding the black equation 50.85^2 = 2585 (fill corrected to pale cyan in attempt 2)"),
    ("eq_right",   625, 140, 742, 183, R2,
     "RIGHT chart annotation box holding the black equation 63.64^2 = 4050 (fill corrected to pale cyan in attempt 2)"),
    ("cap_left",    87, 476, 441, 534, R2,
     "LEFT caption block: red 'Overfit' keyword + '(try to minimize the residuals ONLY)' over 'Fails to detect the Pattern', plus the restored rose vertical + underline marks"),
    ("cap_right",  494, 476, 850, 534, R2,
     "RIGHT caption block: red 'Generalized' keyword + '(Residuals are not minimized)' over 'Successes to detect the Pattern', plus the restored rose verticals + underline"),
    ("chart_left",  87, 102, 473, 480, R1,
     "LEFT scatter chart — UNCHANGED across the rebuild (0 px changed outside fix regions); re-banked verbatim from render_1"),
    ("chart_right",478, 102, 878, 480, R1,
     "RIGHT scatter chart — UNCHANGED across the rebuild (0 px changed outside fix regions); re-banked verbatim from render_1"),
]

ren2 = Image.open(R2).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
RW, RH = ren2.size
SX, SY = RW / 960.0, RH / 540.0
print("render_2 %dx%d  scale x %.5f y %.5f   original %s"
      % (RW, RH, SX, SY, orig.size))
print("prescribed original upscale H_render/540 = %.5f" % SY)
print()

rows = []
for name, x0, y0, x1, y1, rpath, desc in REGIONS:
    ren = ren2 if rpath == R2 else Image.open(rpath).convert("RGB")
    rb = (int(round(x0 * SX)), int(round(y0 * SY)), int(round(x1 * SX)), int(round(y1 * SY)))
    rc = ren.crop(rb)
    ob = (int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))
    oc = orig.crop(ob).resize(rc.size, Image.LANCZOS)
    assert oc.size == rc.size, (name, rc.size, oc.size)
    cp_r = os.path.join(HERE, "crop_2_%s_render.png" % name)
    cp_o = os.path.join(HERE, "crop_2_%s_orig.png" % name)
    rc.save(cp_r)
    oc.save(cp_o)
    w_f, h_f = x1 - x0, y1 - y0
    rows.append((name, w_f, h_f, rc.size))
    print("%-12s region %4dx%-4d frame px -> %dx%d crop px  (scale x %.4f y %.4f)"
          % (name, w_f, h_f, rc.size[0], rc.size[1],
             rc.size[0] / w_f, rc.size[1] / h_f))
    print("             %s" % desc)
    print("             banked crop_2_%s_render.png / crop_2_%s_orig.png" % (name, name))

print()
print("== matched-scale audit (re-opened from disk) ==")
bad = []
for name, x0, y0, x1, y1, rpath, desc in REGIONS:
    r = Image.open(os.path.join(HERE, "crop_2_%s_render.png" % name))
    o = Image.open(os.path.join(HERE, "crop_2_%s_orig.png" % name))
    w_f, h_f = x1 - x0, y1 - y0
    same = (r.size == o.size)
    near = (abs(r.size[0] / w_f - SX) < 0.03 and abs(r.size[1] / h_f - SY) < 0.03)
    print("  %-12s %dx%d vs %dx%d  identical=%-5s  x %.4f y %.4f (target %.4f/%.4f)  %s"
          % (name, r.size[0], r.size[1], o.size[0], o.size[1], same,
             r.size[0] / w_f, r.size[1] / h_f, SX, SY, "OK" if (same and near) else "MISMATCH"))
    if not (same and near):
        bad.append(name)
print()
print("crops cut: %d   scale mismatches: %d" % (len(REGIONS), len(bad)))
print("VERDICT:", "PASS" if not bad else "FAIL")
with open(os.path.join(HERE, "cut_crops_2.txt"), "w") as fh:
    fh.write("Template B crop pairs, attempt K=2, slide 009\n")
    fh.write("render_2 %dx%d scale x %.5f y %.5f; original %s\n" % (RW, RH, SX, SY, orig.size))
    fh.write("original crop LANCZOS-upscaled to the render crop's EXACT pixel size"
             " -> output_px/frame_px equal per axis by construction\n\n")
    for name, w_f, h_f, sz in rows:
        fh.write("%-12s %dx%d frame px -> %dx%d px   crop_2_%s_{render,orig}.png\n"
                 % (name, w_f, h_f, sz[0], sz[1], name))
    fh.write("\nVERDICT: %s\n" % ("PASS" if not bad else "FAIL"))
