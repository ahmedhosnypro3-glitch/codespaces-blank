#!/usr/bin/env python3
"""Slide 009 — Template B crop-pair cutter (Procedure B, judge_protocol_03.md).

Frozen-law implementation, verbatim steps 1-4 of Procedure B:

  1. Regions picked from the ORIGINAL frame (960x540) — every dense region:
        eq_left / eq_right      equation stacks (the pale-cyan annotation boxes)
        cap_left / cap_right    small-text clusters (the two 2-line captions)
        chart_left / chart_right  graph annotations (the two scatter charts)
     Each region carries ~8px of padding.
  2. Render crop: from render_1.png (150dpi), frame coords x H_render/540.
     Original crop: the same frame-px bbox from the 960x540 original.
  3. Effective scale matched PER AXIS BY CONSTRUCTION: the original crop is
     LANCZOS-upscaled to EXACTLY the render crop's pixel size, so
     output_px/frame_px is identical for both images on both axes (the law's
     "8% mismatch fabricates drift MAJORs" hazard is structurally impossible
     here, not merely small). The upscale factor is H_render/540 = 1125/540
     = 2.0833 (y) / 2.0844 (x) as prescribed.
  4. Banked as crop_1_<name>_render.png + crop_1_<name>_orig.png.

This run is attempt K=1 (build unchanged since the certified selfcheck pass).
The dead predecessor's crop_*.png files (Oct-21 04:41) are NEVER deleted —
HARD RULE — they are simply superseded by these crop_1_* files.

Run: python3 probe59_crops.py     (writes probe59_crops.txt)
"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))   # lecture root
ORIG = os.path.join(DECK, "unique_slides", "slide_009.jpg")
REND = os.path.join(HERE, "render_1.png")

# ── dense regions, frame px, ~8px padding (measured; see measurements_summary) ─
REGIONS = [
    # name        x0     y0     x1     y1     description
    ("eq_left",    208,   140,   325,   183,  "LEFT chart annotation box holding the black equation 50.85^2 = 2585"),
    ("eq_right",   625,   140,   742,   183,  "RIGHT chart annotation box holding the black equation 63.64^2 = 4050"),
    ("cap_left",   100,   480,   427,   527,  "LEFT chart's two caption lines: red 'Overfit' keyword + '(try to minimize the residuals ONLY)' over 'Fails to detect the Pattern'"),
    ("cap_right",  515,   480,   827,   527,  "RIGHT chart's two caption lines: red 'Generalized' keyword + '(Residuals are not minimized)' over 'Successes to detect the Pattern'"),
    ("chart_left",  87,   102,   473,   480,  "LEFT scatter chart: navy border, 16x16 grid, red axes + arrowheads, blue fitted line, 12 orange points, red diagonal stroke, solid red discs incl. the large one"),
    ("chart_right", 478,  102,   878,   480,  "RIGHT scatter chart: navy border, 16x16 grid, red axes + arrowheads, blue fitted line, 12 orange points, red diagonal stroke, two solid red discs"),
]

ren = Image.open(REND).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
RW, RH = ren.size
SY = RH / 540.0
SX = RW / 960.0

print("render %dx%d  scale x %.5f y %.5f   original %dx%d"
      % (RW, RH, SX, SY, orig.size[0], orig.size[1]))
print("prescribed original upscale H_render/540 = %.5f" % SY)
print()

rows = []
for name, x0, y0, x1, y1, desc in REGIONS:
    # render crop: native 150dpi pixels, no rescale
    rb = (int(round(x0 * SX)), int(round(y0 * SY)),
          int(round(x1 * SX)), int(round(y1 * SY)))
    rc = ren.crop(rb)
    # original crop: same frame-px bbox, then LANCZOS to EXACTLY the render
    # crop's size -> identical output_px/frame_px on both axes by construction
    ob = (int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))
    oc = orig.crop(ob).resize(rc.size, Image.LANCZOS)
    assert oc.size == rc.size, (name, rc.size, oc.size)
    cp_r = os.path.join(HERE, "crop_1_%s_render.png" % name)
    cp_o = os.path.join(HERE, "crop_1_%s_orig.png" % name)
    rc.save(cp_r)
    oc.save(cp_o)
    w_f, h_f = x1 - x0, y1 - y0
    rows.append((name, w_f, h_f, rc.size))
    print("%-12s region %4dx%-4d frame px -> %dx%d crop px  (scale x %.4f y %.4f)"
          % (name, w_f, h_f, rc.size[0], rc.size[1],
             rc.size[0] / w_f, rc.size[1] / h_f))
    print("             %s" % desc)
    print("             banked crop_1_%s_render.png / crop_1_%s_orig.png" % (name, name))

print()
print("== matched-scale audit ==")
print("Law: output_px/frame_px must be EQUAL for both images, per axis. Both")
print("members of a pair are resized to the SAME pixel box, so this holds by")
print("construction; the audit re-opens the saved PNGs and proves it from disk")
print("rather than trusting the in-memory objects. The x/y scale columns are the")
print("crop's own per-axis scales — they differ slightly only from integer")
print("rounding of the region box, which is NOT a mismatch (the law constrains")
print("render-vs-orig, not x-vs-y).")
bad = []
for name, x0, y0, x1, y1, desc in REGIONS:
    r = Image.open(os.path.join(HERE, "crop_1_%s_render.png" % name))
    o = Image.open(os.path.join(HERE, "crop_1_%s_orig.png" % name))
    w_f, h_f = x1 - x0, y1 - y0
    same = (r.size == o.size)
    near = (abs(r.size[0] / w_f - SX) < 0.03 and abs(r.size[1] / h_f - SY) < 0.03)
    ok = same and near
    print("  %-12s %dx%d vs %dx%d  identical=%-5s  per-axis x %.4f y %.4f"
          " (target %.4f/%.4f)  %s"
          % (name, r.size[0], r.size[1], o.size[0], o.size[1], same,
             r.size[0] / w_f, r.size[1] / h_f, SX, SY, "OK" if ok else "MISMATCH"))
    if not ok:
        bad.append(name)
print()
print("crops cut: %d   scale mismatches: %d" % (len(REGIONS), len(bad)))
print("VERDICT:", "PASS" if not bad else "FAIL")

with open(os.path.join(HERE, "probe59_crops.txt"), "w") as fh:
    fh.write("Template B crop pairs, attempt K=1, slide 009\n")
    fh.write("render %dx%d scale x %.5f y %.5f; original %dx%d\n"
             % (RW, RH, SX, SY, orig.size[0], orig.size[1]))
    fh.write("original crop LANCZOS-upscaled to the render crop's EXACT pixel size"
             " -> output_px/frame_px equal per axis by construction\n\n")
    for name, x0, y0, x1, y1, desc in REGIONS:
        r = Image.open(os.path.join(HERE, "crop_1_%s_render.png" % name))
        o = Image.open(os.path.join(HERE, "crop_1_%s_orig.png" % name))
        assert r.size == o.size, (name, r.size, o.size)
        fh.write("%-12s region x%d..%d y%d..%d (%dx%d frame px) -> %dx%d px"
                 "   crop_1_%s_{render,orig}.png\n"
                 % (name, x0, x1, y0, y1, x1 - x0, y1 - y0, r.size[0], r.size[1], name))
    fh.write("\nVERDICT: %s\n" % ("PASS" if not bad else "FAIL"))
