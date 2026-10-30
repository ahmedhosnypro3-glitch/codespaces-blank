#!/usr/bin/env python3
"""Verify both sides of each crop pair carry ink (crop sanity pre-flight)."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{NS}/recreated_pptx/qa/slide019"

for slug in ["header_strip", "table_left", "table_right", "noreg_rows"]:
    rc = np.asarray(Image.open(f"{QA}/crop_2_{slug}_render.png").convert("RGB")).astype(int)
    oc = np.asarray(Image.open(f"{QA}/crop_2_{slug}_orig.png").convert("RGB")).astype(int)
    print(f"--- {slug}  render {rc.shape[:2]}  orig {oc.shape[:2]}")
    for nm, img in (("render", rc), ("orig", oc)):
        lum = img.sum(axis=2) / 3.0
        for t, lab in ((120, "dark(<120)"), (170, "ink(<170)")):
            print(f"    {nm} {lab}: {(lum < t).sum()} px")
    # colour presence per side
    for nm, img in (("render", rc), ("orig", oc)):
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        red = ((r > 120) & (g < 105) & (b < 105) & (r - g > 45)).sum()
        grn = ((g > 105) & (r < 120) & (b < 100) & (g - b > 35)).sum()
        blu = ((b > 120) & (r < 110) & (b - r > 35)).sum()
        yel = ((r > 215) & (g > 215) & (b < 175)).sum()
        print(f"    {nm} colours: red {red} green {grn} blue {blu} yellow {yel}")
