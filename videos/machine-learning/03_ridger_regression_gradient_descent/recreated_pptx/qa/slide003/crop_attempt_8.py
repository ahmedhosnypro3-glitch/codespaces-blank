#!/usr/bin/env python3
"""Procedure B crop-pair cutter for slide 003 attempt 8 (fresh from render_8).

Cuts both images at the SAME slide-space bbox and matches effective scale
(output_px / frame_px) per axis, LANCZOS, per judge_protocol_03.md Procedure B.
"""
import numpy as np
from PIL import Image

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003")
RENDER = f"{QA}/render_8.png"
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_003.jpg")

# densest regions (frame px, ~8px padding), from the take-6 census
REGIONS = {
    "matrix_stack": (265, 100, 600, 305),
    "eq_bl":        (72, 320, 540, 520),
    "eq_br":        (565, 318, 758, 520),
    "side_boxes":   (640, 145, 880, 300),
}

r = Image.open(RENDER).convert("RGB")
o = Image.open(ORIG).convert("RGB")
Hr = r.height
scale = Hr / 540.0
print(f"render {r.size}  orig {o.size}  scale {scale:.4f}")
for name, (x0, y0, x1, y1) in REGIONS.items():
    rc = r.crop((int(x0 * scale), int(y0 * scale), int(x1 * scale), int(y1 * scale)))
    oc = o.crop((x0, y0, x1, y1))
    oc2 = oc.resize((int(round(oc.width * (rc.width / oc.width))),
                     int(round(oc.height * (rc.height / oc.height)))),
                    Image.LANCZOS)
    rc.save(f"{QA}/crop_8_{name}_render.png")
    oc2.save(f"{QA}/crop_8_{name}_orig.png")
    print(f"{name}: render {rc.size} eff {rc.width/(x1-x0):.4f} | "
          f"orig {oc2.size} eff {oc2.width/oc.width:.4f}")
