#!/usr/bin/env python3
"""Slide 030 Procedure B crop cutter (w030-finish-20261024).

Crops BOTH images at the same slide-space bbox (frame px) and LANCZOS-upscales
the original crop by H_render/540 so both crops have the SAME effective scale
(judge_protocol_03.md procedure B). Banks crop_6_<name>_{render,orig}.png and a
scale audit JSON.
"""
import json

import numpy as np
from PIL import Image

V = "videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{V}/recreated_pptx/qa/slide030"
REND = f"{Q}/render_6.png"
ORIG = f"{V}/unique_slides/slide_030.jpg"

rend = Image.open(REND).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
RW, RH = rend.size          # 2001x1125
OW, OH = orig.size          # 960x540
SXR = RW / 960.0            # render px per frame px
SYR = RH / 540.0
UP = SYR                    # original upscale factor (isotropic effective scale)

# dense regions from the ORIGINAL frame (frame px, ~8px padding)
REGIONS = {
    "iter_left":  (72, 318, 400, 538, "iteration table left half: x/f(x)/x-delta/f(x-delta) label + value cells"),
    "iter_right": (370, 318, 662, 538, "iteration table right half: x+delta/f(x+delta)/slope/next x value cells"),
    "formula":    (340, 178, 562, 288, "red equation box f(x)=(x-5)^2+1 + green box X=5 / f(x) Minimum value is 1.0"),
    "plot":       (565, 58, 818, 318, "graph: parabola, red dashed x=5, secant + dots, point labels, tick labels"),
    "param":      (95, 190, 245, 292, "small parameter table: step/0.2, initial X/3, delta/0.1"),
    "callout":    (325, 282, 580, 330, "purple callout: Reach Minimum after 11 Steps"),
    "arrow":      (160, 294, 208, 348, "red block arrow pointing down toward the iteration table"),
}

audit = {}
for name, (x0, y0, x1, y1, desc) in REGIONS.items():
    # render crop (render px)
    rb = (int(round(x0 * SXR)), int(round(y0 * SYR)),
          int(round(x1 * SXR)), int(round(y1 * SYR)))
    rc = rend.crop(rb)
    # original crop (frame px) upscaled to the same effective scale
    op = orig.crop((x0, y0, x1, y1))
    ow, oh = op.size
    owu, ohu = int(round(ow * UP)), int(round(oh * UP))
    oc = op.resize((owu, ohu), Image.LANCZOS)
    rp, op_ = f"{Q}/crop_6_{name}_render.png", f"{Q}/crop_6_{name}_orig.png"
    rc.save(rp)
    oc.save(op_)
    sx = rc.size[0] / (x1 - x0)
    sy = rc.size[1] / (y1 - y0)
    osx = oc.size[0] / (x1 - x0)
    osy = oc.size[1] / (y1 - y0)
    audit[name] = {
        "region_frame_px": [x0, y0, x1, y1],
        "render_box_px": rb,
        "render_px": list(rc.size),
        "orig_px_after_upscale": list(oc.size),
        "scale_render": [round(sx, 4), round(sy, 4)],
        "scale_orig": [round(osx, 4), round(osy, 4)],
        "scale_mismatch_pct": [round(abs(sx - osx) / sx * 100, 3), round(abs(sy - osy) / sy * 100, 3)],
        "desc": desc,
    }
    print(f"{name:11s} region={x0,y0,x1,y1} render={rc.size} orig={oc.size} "
          f"scale r={sx:.3f}/{sy:.3f} o={osx:.3f}/{osy:.3f} mismatch={audit[name]['scale_mismatch_pct']}%")

with open(f"{Q}/crop_6_scale_audit.json", "w") as f:
    json.dump(audit, f, indent=1)
print("\nbanked", len(audit), "crop pairs ->", Q)
