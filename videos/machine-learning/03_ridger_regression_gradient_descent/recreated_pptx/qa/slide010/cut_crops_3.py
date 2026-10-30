#!/usr/bin/env python3
"""Slide 010 — Template B crop-pair cutter, child-lane attempt K=3 (Procedure B).
Cuts the densest regions of slide 010 from render_3.png (150dpi) and the
960x540 original at MATCHED effective scale (LANCZOS-upscale the original crop
to the render crop's exact pixel size → output_px/frame_px equal per axis by
construction; judge_protocol_03.md Procedure B step 3). Portable paths.

Dense regions (frame px, slide space, ~8px padding):
  chart_left  — LEFT scatter chart (grid, axes, blue fitted line, 12 points,
                periwinkle residual connectors, green cross + axis dot, two
                pale-rose projection pairs, red arrowheads/triangles)
  chart_right — RIGHT scatter chart (same family; 12 points; same delta marks)
  cap_left    — LEFT caption band (cream box + red bold 'Overfit', two serif lines)
  cap_right   — RIGHT caption band (cream box + red bold 'Generalized', two lines)
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ORIG = os.path.join(DECK, "unique_slides", "slide_010.jpg")
RENDER = os.path.join(HERE, "render_3.png")

REGIONS = [
    ("chart_left", 87, 102, 473, 480,
     "LEFT scatter chart: navy-bordered white panel, 16x16 gray grid, red axes with triangular heads, blue fitted line, 12 orange points, light-periwinkle dashed residual connectors, a green dashed cross (horizontal line + vertical line) ending in a solid bright-green dot on the x-axis, two pale-rose projection pairs with red arrowheads/triangles"),
    ("chart_right", 478, 102, 878, 480,
     "RIGHT scatter chart: same family (navy panel, grid, red axes, blue fitted line, 12 orange points, periwinkle residual connectors); green dashed cross + bright-green x-axis dot; two pale-rose projection pairs; no equation box"),
    ("cap_left", 87, 476, 441, 534,
     "LEFT caption block: red bold 'Overfit' + '(try to minimize the residuals ONLY)' over 'Fails to detect the Pattern', serif, inside the cream-filled rose-outlined open-top box"),
    ("cap_right", 494, 476, 850, 534,
     "RIGHT caption block: red bold 'Generalized' + '(Residuals are not minimized)' over 'Successes to detect the Pattern', serif, inside the cream-filled rose-outlined open-top box"),
]

ren = Image.open(RENDER).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
RW, RH = ren.size
SX, SY = RW / 960.0, RH / 540.0
print("render_3 %dx%d   scale x %.5f y %.5f   original %s" % (RW, RH, SX, SY, orig.size))
print("prescribed original upscale H_render/540 = %.5f" % SY)
print()

rows = []
for name, x0, y0, x1, y1, desc in REGIONS:
    rb = (int(round(x0 * SX)), int(round(y0 * SY)), int(round(x1 * SX)), int(round(y1 * SY)))
    rc = ren.crop(rb)
    oc = orig.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    assert oc.size == rc.size, (name, rc.size, oc.size)
    rc.save(os.path.join(HERE, "crop_3_%s_render.png" % name))
    oc.save(os.path.join(HERE, "crop_3_%s_orig.png" % name))
    w_f, h_f = x1 - x0, y1 - y0
    rows.append((name, w_f, h_f, rc.size, desc))
    print("%-12s region %4dx%-4d frame px -> %dx%d crop px (scale x %.4f y %.4f)"
          % (name, w_f, h_f, rc.size[0], rc.size[1], rc.size[0] / w_f, rc.size[1] / h_f))

print()
print("== matched-scale audit (re-opened from disk) ==")
bad = []
for name, x0, y0, x1, y1, desc in REGIONS:
    r = Image.open(os.path.join(HERE, "crop_3_%s_render.png" % name))
    o = Image.open(os.path.join(HERE, "crop_3_%s_orig.png" % name))
    w_f, h_f = x1 - x0, y1 - y0
    same = r.size == o.size
    near = abs(r.size[0] / w_f - SX) < 0.03 and abs(r.size[1] / h_f - SY) < 0.03
    print("  %-12s %dx%d vs %dx%d identical=%-5s x %.4f y %.4f (target %.4f/%.4f) %s"
          % (name, r.size[0], r.size[1], o.size[0], o.size[1], same,
             r.size[0] / w_f, r.size[1] / h_f, SX, SY, "OK" if (same and near) else "MISMATCH"))
    if not (same and near):
        bad.append(name)
print()
print("crops cut: %d   scale mismatches: %d" % (len(REGIONS), len(bad)))
print("VERDICT:", "PASS" if not bad else "FAIL")
with open(os.path.join(HERE, "cut_crops_3.txt"), "w") as fh:
    fh.write("Template B crop pairs, child-lane attempt K=3, slide 010 (worker w010-child-20261024b)\n")
    fh.write("render_3 %dx%d scale x %.5f y %.5f; original %s\n" % (RW, RH, SX, SY, orig.size))
    fh.write("original crop LANCZOS-upscaled to the render crop's EXACT pixel size -> output_px/frame_px equal per axis by construction\n\n")
    for name, w_f, h_f, sz, desc in rows:
        fh.write("%-12s %dx%d frame px -> %dx%d px   crop_3_%s_{render,orig}.png\n     region: %s\n"
                 % (name, w_f, h_f, sz[0], sz[1], name, desc))
    fh.write("\nVERDICT: %s\n" % ("PASS" if not bad else "FAIL"))
