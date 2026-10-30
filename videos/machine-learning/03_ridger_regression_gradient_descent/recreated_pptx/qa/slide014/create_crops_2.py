#!/usr/bin/env python3
"""Cut Procedure-B crop pairs for slide 014 (attempt 2) from render_2.png.

Regions chosen from the ORIGINAL's dense ink (measure_orig / measure_bands2):
  rect of columns -> the two side-by-side vector-definition boxes
  lower bands    -> loss-term / reg-term boxes + final objective band
Original crop is LANCZOS-upscaled by H_render/540 so both sides of every pair
share one effective scale.
"""
import numpy as np
from PIL import Image

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/")
NS = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/")

render = Image.open(QA + "render_2.png")
orig = Image.open(NS + "unique_slides/slide_014.jpg")
H = render.height
scale = H / 540.0
print(f"render {render.size} orig {orig.size} scale {scale:.4f}")

# name, x0, y0, x1, y1 (frame px, ~8px padding)
regions = [
    ("column_of_columns", 48, 96, 906, 240),
    ("lower_bands", 48, 336, 906, 528),
]

for name, x0, y0, x1, y1 in regions:
    rx0, ry0 = int(round(x0 * scale)), int(round(y0 * scale))
    rx1, ry1 = int(round(x1 * scale)), int(round(y1 * scale))
    rc = render.crop((rx0, ry0, rx1, ry1))
    oc = orig.crop((x0, y0, x1, y1)).resize((rx1 - rx0, ry1 - ry0), Image.LANCZOS)
    rc.save(f"{QA}crop_2_{name}_render.png")
    oc.save(f"{QA}crop_2_{name}_orig.png")
    print(f"{name}: render crop {rc.size}, orig upscaled {oc.size} "
          f"(effective scale {rc.size[0]/(x1-x0):.4f} vs {oc.size[0]/(x1-x0):.4f})")
print("crop pairs created")
