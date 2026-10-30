#!/usr/bin/env python3
"""Attempt-27 crop pairs for slide 034 zoomed judging (protocol_03 procedure B).

Cuts each pinned slide-space region from render_27.png (per-axis render scale)
and from the 960x540 original (LANCZOS upscale by H_render/540), banks
crop_27_<name>_{render,orig}.png, and asserts matched effective scale.
"""
import sys
from PIL import Image

D = "videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{D}/recreated_pptx/qa/slide034"
RENDER = f"{QA}/render_27.png"
ORIG = f"{D}/unique_slides/slide_034.jpg"

# slide-space bboxes (frame px, ~8px pad) pinned by the attempt-27 fix list
REGIONS = [
    ("table",     (74, 313, 887, 525)),
    ("plot",      (599, 50, 853, 321)),
    ("leftblock", (60, 50, 610, 330)),
]

r = Image.open(RENDER).convert("RGB")
o = Image.open(ORIG).convert("RGB")
if r.size != (2001, 1125):
    sys.exit(f"render size {r.size} != (2001,1125)")
if o.size != (960, 540):
    sys.exit(f"orig size {o.size} != (960,540)")
sxr, syr = r.width / 960.0, r.height / 540.0
f = 1125 / 540.0

for name, (x0, y0, x1, y1) in REGIONS:
    rc = r.crop((round(x0 * sxr), round(y0 * syr), round(x1 * sxr), round(y1 * syr)))
    oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    s_r = rc.width / (x1 - x0), rc.height / (y1 - y0)
    if abs(s_r[0] - 2.0833) > 0.01 or abs(s_r[1] - 2.0833) > 0.01:
        sys.exit(f"{name}: render crop scale {s_r} off nominal 150dpi")
    rc.save(f"{QA}/crop_27_{name}_render.png")
    oc.save(f"{QA}/crop_27_{name}_orig.png")
    print(f"{name}: render {rc.size} (scale {s_r[0]:.4f}/{s_r[1]:.4f})  "
          f"orig resized to {oc.size}  -> crop_27_{name}_*.png")
print("crop pairs banked; effective scales identical by construction")
