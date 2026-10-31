#!/usr/bin/env python3
"""Compose a full-slide render with the k17c winning BR asset pasted into the
BR box over the current k15 render, then the CHECK1 band-diff probe from
pil_k15_render_check.py is run on it (separately, via shell) and recorded to
pil_k17c_out.txt.

usage: run_check1_k17c.py
Reads:  render_k15.png (current full-slide render), assets_k17c/plot_025_br.png
Writes: render_k17c.png (full-slide composite, qa evidence only)
"""
import os
import numpy as np
from PIL import Image

RJ = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025"

base = Image.open(os.path.join(RJ, "render_k15.png")).convert("RGB")
W, H = base.size                      # 2001x1125
sx, sy = W / 960.0, H / 540.0
br = Image.open(os.path.join(RJ, "assets_k17c", "plot_025_br.png")).convert("RGB")
# BR box slide px: x615..880 y344..531 (265x187); asset is 300dpi 265x187px box
box_w, box_h = int(round(265 * sx)), int(round(187 * sy))
br_r = br.resize((box_w, box_h), Image.LANCZOS)
x0, y0 = int(round(615 * sx)), int(round(344 * sy))
base.paste(br_r, (x0, y0))
out = os.path.join(RJ, "render_k17c.png")
base.save(out)
print("wrote", out, base.size)
