#!/usr/bin/env python3
"""Procedure B crop-pair generator for slide 002, attempt 1 (render_1.png).

Cuts BOTH images at the same slide-space region and matches effective scale
per axis (output_px/frame_px equal for render crop and original crop):
  - render crop: native pixels at (frame_px * Sx, frame_px * Sy)
  - original crop: LANCZOS upscale of the same frame-px bbox to the render
    crop's exact pixel size.
Regions (frame px, 960x540, ~8px padding):
  title     x 189..764, y 191..322  (two-line red title = densest content)
  badgeplus x 747..908, y 47..103   (badge numeral 2 + plus-sign small-text cluster)
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide002/"
RE = Image.open(QA + "render_1.png").convert("RGB")
OR = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_002.jpg").convert("RGB")
W, H = RE.size
Sx, Sy = W / 960.0, H / 540.0
print(f"render {W}x{H}  Sx={Sx:.6f} Sy={Sy:.6f}")

REGIONS = {"title": (189, 764, 191, 322), "badgeplus": (747, 908, 47, 103)}

for name, (x0, x1, y0, y1) in REGIONS.items():
    rx0, rx1 = round(x0 * Sx), round(x1 * Sx)
    ry0, ry1 = round(y0 * Sy), round(y1 * Sy)
    rc = RE.crop((rx0, ry0, rx1 + 1, ry1 + 1))           # inclusive bbox
    fw, fh = x1 - x0 + 1, y1 - y0 + 1
    oc = OR.crop((x0, y0, x1 + 1, y1 + 1)).resize(rc.size, Image.LANCZOS)
    rp = f"{QA}crop_1_{name}_render.png"
    op = f"{QA}crop_1_{name}_orig.png"
    rc.save(rp); oc.save(op)
    esx, esy = rc.size[0] / fw, rc.size[1] / fh
    osx, osy = oc.size[0] / fw, oc.size[1] / fh
    assert (esx, esy) == (osx, osy), "effective scale mismatch"
    # sanity: ink present in both crops (non-background pixels)
    ra = np.asarray(rc).astype(int); oa = np.asarray(oc).astype(int)
    rink = int((np.abs(ra - np.array([231, 233, 230])).max(axis=2) > 40).sum())
    oink = int((np.abs(oa - np.array([231, 233, 230])).max(axis=2) > 40).sum())
    print(f"{name}: pair {rc.size}  frame {fw}x{fh}  effScale ({esx:.4f},{esy:.4f})  "
          f"ink render={rink} orig={oink}  -> {rp} + {op}")
    assert rink > 50 and oink > 50, f"{name}: crop appears empty"
print("CROP PAIRS OK")
