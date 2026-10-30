#!/usr/bin/env python3
"""Procedure B crop-pair cutter for slide 003's densest region (the matrix /
equation stack). Crops both images at the SAME slide-space bbox and matches
effective scale (output_px / frame_px) per axis."""
import numpy as np
from PIL import Image

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003"
RENDER = f"{QA}/render_5.png"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_003.jpg"

# densest region: the whole matrix/equation stack, frame px (x0,y0,x1,y1)
REGIONS = {
    "matrix_stack": (265, 100, 600, 305),
    "eq_remember":   (645, 148, 880, 300),
}

def main():
    r = Image.open(RENDER).convert("RGB")
    o = Image.open(ORIG).convert("RGB")
    Hr = r.height
    scale = Hr / 540.0
    print(f"render {r.size}  scale {scale:.4f}")
    for name, (x0, y0, x1, y1) in REGIONS.items():
        # render crop: frame px -> render px
        rc = r.crop((int(x0 * scale), int(y0 * scale), int(x1 * scale), int(y1 * scale)))
        # original crop: same frame-px bbox, then LANCZOS-upscaled to match
        oc = o.crop((x0, y0, x1, y1))
        target_w = int(oc.width * scale)
        target_h = int(oc.height * scale)
        # match effective scale per axis exactly
        oc2 = oc.resize((int(round(oc.width * (rc.width / oc.width))),
                         int(round(oc.height * (rc.height / oc.height)))),
                        Image.LANCZOS)
        rc.save(f"{QA}/crop_5_{name}_render.png")
        oc2.save(f"{QA}/crop_5_{name}_orig.png")
        print(f"{name}: render {rc.size} eff {rc.width/(x1-x0):.4f} | "
              f"orig {oc2.size} eff {oc2.width/oc.width:.4f} (upscaled x{scale:.4f})")

main()
