#!/usr/bin/env python3
"""Slide 011 assets v3: exact-size 600dpi mathtext fractions + transparent plane crops."""
import json, subprocess, sys
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
A = NS + "/recreated_pptx/build/assets"
RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq.py"


def render_eq(latex, out, fs, color="000000"):
    res = subprocess.run([sys.executable, RENDER, latex, out, str(fs), color],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr)
    return json.loads(res.stdout.strip().splitlines()[-1])


def render_eq_to_width(latex, out, target_w_in, fs0=20.0, color="000000"):
    info = render_eq(latex, out, fs0, color)
    fs = fs0 * target_w_in / info["w_in"]
    info = render_eq(latex, out, round(fs, 2), color)
    return info


# fraction TP/(TP+FN): must fit inside red formula box (box x 0.97..4.40, frac starts ~3.00) -> target 1.32in
i1 = render_eq_to_width(r"\frac{TP}{TP + FN}", A + "/eq_011_v3_tpfn.png", 1.32, 20.0)
print("tpfn:", i1["w_px"], "x", i1["h_px"], "=", i1["w_in"], "x", i1["h_in"], "in")

# fraction 28/(28+2): target 0.73in
i2 = render_eq_to_width(r"\frac{28}{28+2}", A + "/eq_011_v3_frac28.png", 0.73, 14.0)
print("frac28:", i2["w_px"], "x", i2["h_px"], "=", i2["w_in"], "x", i2["h_in"], "in")

# airplane crops from the original frame, near-white -> transparent, 3x upscale
im = Image.open(NS + "/unique_slides/slide_011.jpg").convert("RGB")
a = np.array(im).astype(int)
mx = a.max(2); sat = mx - a.min(2)


def plane_crop(x0, y0, x1, y1, out):
    crop = im.crop((x0, y0, x1, y1))
    c = np.array(crop).astype(int)
    cmx = c.max(2); csat = cmx - c.min(2)
    alpha = np.where(cmx >= 238, 0, np.clip((238 - cmx) * 5, 0, 255)).astype(np.uint8)
    rgba = np.dstack([c.astype(np.uint8), alpha])
    img = Image.fromarray(rgba, "RGBA").resize(((x1 - x0) * 3, (y1 - y0) * 3), Image.LANCZOS)
    img.save(out)
    print("plane:", out, img.size, "-> slide in:", round((x1 - x0) / 72, 4), "x", round((y1 - y0) / 72, 4))


plane_crop(588, 343, 673, 373, A + "/plane_011_v3_pos.png")   # left plane  x=8.17 y=4.76 w=1.18 h=0.42
plane_crop(764, 343, 852, 367, A + "/plane_011_v3_neg.png")   # right plane x=10.61 y=4.76 w=1.22 h=0.33
