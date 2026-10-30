#!/usr/bin/env python3
"""Cut Procedure-B crop pairs from render_2.png at matched effective scale.

Per judge_protocol_03.md Procedure B step 2-4:
  * region = slide-space bbox (x0,y0,x1,y1) in ORIGINAL frame px (960x540)
  * render crop : bbox scaled by H_render/540
  * orig crop   : same frame-px bbox, LANCZOS-upscaled by H_render/540
  * both sides therefore have identical output_px/frame_px
"""
import os
import sys
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{NS}/recreated_pptx/qa/slide019"
K = sys.argv[1] if len(sys.argv) > 1 else "2"

RENDER = f"{QA}/render_{K}.png"
ORIG = f"{NS}/unique_slides/slide_019.jpg"

# region slug -> (x0, y0, x1, y1) in original frame px
REGIONS = {
    # title bar + the three stacked test-point vectors (z1/z2/z3 + y=NN)
    "header_strip": (60, 58, 440, 165),
    # outlier column + NO Regularizer column, row groups 1-2 (incl. yellow band A)
    "table_left": (56, 160, 390, 360),
    # RIDGE lambda=3 + lambda=10 columns, all three row groups + bands A/B/C
    "table_right": (378, 160, 902, 530),
    # all three NO Regularizer row groups (the previously disputed y-value cells)
    "noreg_rows": (122, 198, 382, 520),
}

r = Image.open(RENDER).convert("RGB")
o = Image.open(ORIG).convert("RGB")
SX = r.width / o.width
SY = r.height / o.height
print(f"render {r.size}, orig {o.size} -> scale X {SX:.4f} Y {SY:.4f}")

for slug, (x0, y0, x1, y1) in REGIONS.items():
    # render crop
    rc = r.crop((round(x0 * SX), round(y0 * SY), round(x1 * SX), round(y1 * SY)))
    # orig crop, upscaled to the SAME effective scale
    oc = o.crop((x0, y0, x1, y1)).resize(
        (round((x1 - x0) * SX), round((y1 - y0) * SY)), Image.LANCZOS
    )
    rp = f"{QA}/crop_{K}_{slug}_render.png"
    op = f"{QA}/crop_{K}_{slug}_orig.png"
    rc.save(rp)
    oc.save(op)
    print(f"{slug}: frame ({x0},{y0})-({x1},{y1}) -> render {rc.size} / orig {oc.size}")
