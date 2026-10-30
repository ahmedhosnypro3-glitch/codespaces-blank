#!/usr/bin/env python3
"""Cut crop pairs for slide 034's dense regions (matched effective scale).

Regions (frame px, 960x540 original; 150dpi render = 2001x1125, scale 2.083):
  table    — the big 8x19 numeric table (densest ink)
  plot     — the function plot + annotations (top-right)
  leftblk  — title/param-box/equation/callout cluster (top-left)
"""
import json
from PIL import Image

ROOT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
QA = ROOT + "/recreated_pptx/qa/slide034"
ORIG = ROOT + "/unique_slides/slide_034.jpg"
RENDER = QA + "/render_1.png"

orig = Image.open(ORIG).convert("RGB")
rend = Image.open(RENDER).convert("RGB")
ORIG_W, ORIG_H = orig.size        # 960x540
REND_W, REND_H = rend.size        # 2001x1125
SR = REND_H / ORIG_H              # ~2.083

REGIONS = {
    "table":   (60, 315, 890, 525),
    "plot":    (600, 55, 850, 315),
    "leftblk": (65, 55, 610, 310),
}

for name, (x0, y0, x1, y1) in REGIONS.items():
    # original crop upscaled to match the render's effective scale
    oc = orig.crop((x0, y0, x1, y1)).resize(
        (int(round((x1 - x0) * SR)), int(round((y1 - y0) * SR))), Image.LANCZOS)
    cv = (int(round(x0 * SR)), int(round(y0 * SR)),
          int(round(x1 * SR)), int(round(y1 * SR)))
    rc = rend.crop(cv)
    oc.save(f"{QA}/crop_1_{name}_orig.png")
    rc.save(f"{QA}/crop_1_{name}_render.png")
    print(f"{name}: orig_crop={oc.size} render_crop={rc.size} "
          f"scale_orig={oc.size[0]/(x1-x0):.3f} scale_rend={rc.size[0]/(cv[2]-cv[0]):.3f}")
