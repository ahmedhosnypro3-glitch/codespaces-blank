#!/usr/bin/env python3
"""Probe 14: save PNG crops of the ambiguous regions so they can be viewed
directly (caption bands, 'mm' label bands, equation box interiors).
Frame px coordinates are drawn into the crop titles via filename only.
"""
import os
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009"
im = Image.open(SRC).convert("RGB")

CROPS = {
    "crop_LEQ": (85, 100, 480, 195),      # LEFT annotation box + top of chart
    "crop_REQ": (478, 100, 880, 195),     # RIGHT annotation box
    "crop_LMM": (90, 478, 160, 535),      # LEFT 'mm' label
    "crop_RMM": (485, 478, 555, 535),     # RIGHT 'mm' label
    "crop_LCAP": (95, 480, 470, 535),     # LEFT caption band
    "crop_RCAP": (475, 480, 880, 535),    # RIGHT caption band
    "crop_LAXIS": (90, 100, 480, 480),    # LEFT chart panel
    "crop_RAXIS": (480, 100, 880, 480),   # RIGHT chart panel
}
for name, box in CROPS.items():
    c = im.crop(box)
    c = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
    p = os.path.join(OUT, name + ".png")
    c.save(p)
    print(f"{name}: src box {box} -> {c.size}  {p}")
