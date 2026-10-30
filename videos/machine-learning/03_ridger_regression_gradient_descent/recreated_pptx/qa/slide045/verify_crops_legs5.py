#!/usr/bin/env python3
"""Slide 045: independent re-derivation of the Procedure B crop-pair effective scale.

Re-cuts every _r2 crop pair into a scratch dir from render_1.png + slide_045.jpg
and (a) compares bytes against the banked pair, (b) re-derives and prints the
effective scale (output_px / frame_px) on BOTH axes for render and original.
"""
import hashlib
import os
import sys
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = os.path.join(DECK, "recreated_pptx", "qa", "slide045")
RENDER = os.path.join(QA, "render_1.png")
ORIG = os.path.join(DECK, "unique_slides", "slide_045.jpg")
SCRATCH = os.path.join(DECK, "scratch", "045legs5_crops")
os.makedirs(SCRATCH, exist_ok=True)

REGIONS = [
    ("calcs", 266, 131, 861, 536),
    ("toppanel", 60, 46, 727, 137),
    ("augtable", 62, 132, 254, 263),
]

def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

rim = Image.open(RENDER).convert("RGB")
oim = Image.open(ORIG).convert("RGB")
RW, RH = rim.size
S = RH / 540.0
print("render=%dx%d  scale H_render/540=%.6f" % (RW, RH, S))
print("original=%dx%d" % oim.size)
print()

all_ok = True
for name, x0, y0, x1, y1 in REGIONS:
    rx0, ry0 = int(round(x0 * S)), int(round(y0 * S))
    rx1, ry1 = int(round(x1 * S)), int(round(y1 * S))
    rc = rim.crop((rx0, ry0, rx1, ry1))
    oc = oim.crop((x0, y0, x1, y1))
    fw, fh = x1 - x0, y1 - y0
    oc2 = oc.resize((rc.width, rc.height), Image.LANCZOS)
    rp = os.path.join(SCRATCH, "crop_1_r2_%s_render.png" % name)
    op = os.path.join(SCRATCH, "crop_1_r2_%s_orig.png" % name)
    rc.save(rp)
    oc2.save(op)

    brp = os.path.join(QA, "crop_1_r2_%s_render.png" % name)
    bop = os.path.join(QA, "crop_1_r2_%s_orig.png" % name)

    r_bytes = open(rp, "rb").read() == open(brp, "rb").read()
    o_bytes = open(op, "rb").read() == open(bop, "rb").read()

    es_r_x = rc.width / fw
    es_r_y = rc.height / fh
    es_o_x = oc2.width / fw
    es_o_y = oc2.height / fh
    x_match = abs(es_r_x - es_o_x) < 1e-9
    y_match = abs(es_r_y - es_o_y) < 1e-9

    ok = r_bytes and o_bytes and x_match and y_match
    all_ok = all_ok and ok
    print("%-9s frame=(%d,%d)-(%d,%d) %dx%d" % (name, x0, y0, x1, y1, fw, fh))
    print("           render crop %dx%d  orig crop(upscaled) %dx%d  LANCZOS factor=%.6f"
          % (rc.width, rc.height, oc2.width, oc2.height, oc2.width / fw))
    print("           effective scale render=(%.5f, %.5f) orig=(%.5f, %.5f)  per-axis match=%s"
          % (es_r_x, es_r_y, es_o_x, es_o_y, x_match and y_match))
    print("           byte-identical: render=%s (%s)  orig=%s (%s)"
          % (r_bytes, md5(brp), o_bytes, md5(bop)))
    print("           RESULT: %s" % ("OK" if ok else "MISMATCH"))
    print()

print("OVERALL: %s" % ("ALL 3 CROP PAIRS BYTE-IDENTICAL AT MATCHED EFFECTIVE SCALE" if all_ok else "FAIL"))
sys.exit(0 if all_ok else 1)
