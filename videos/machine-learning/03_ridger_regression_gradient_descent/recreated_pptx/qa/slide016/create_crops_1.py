#!/usr/bin/env python3
"""Procedure B crop-pair cutter for slide 016, attempt 1.

Frame-space bbox -> same bbox cropped from BOTH the 150dpi render (scale s=1125/540)
and the 960x540 original; the original crop is LANCZOS-upscaled by the same s so
output_px/frame_px is EQUAL on both axes (protocol 03 step 3: an ~8% mismatch
fabricates drift MAJORs).

Dense regions of slide 016 (from the frame measurement):
  missing_band  y330..450 — the L2/L1 bullet continuations + red/blue key terms
                 (the render's empty region: BLOCKER-level evidence)
  full_body     y100..530 — the whole 12-line text block inside the white box
"""
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016"
RENDER = f"{QA}/render_1.png"
ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg"

r_im = Image.open(RENDER).convert("RGB")
o_im = Image.open(ORIG).convert("RGB")
W_f, H_f = o_im.size                      # 960 x 540 frame px
s = r_im.size[1] / H_f                    # render px per frame px (~2.0833)
print(f"render {r_im.size}  frame {o_im.size}  scale s={s:.4f}")

# (name, x0, y0, x1, y1) in frame px, ~8px padding around each dense region
REGIONS = [
    ("missing_band", 80, 325, 815, 455),
    ("full_body",    80,  98, 815, 532),
]

for name, x0, y0, x1, y1 in REGIONS:
    r_box = (round(x0 * s), round(y0 * s), round(x1 * s), round(y1 * s))
    r_crop = r_im.crop(r_box)
    o_crop = o_im.crop((x0, y0, x1, y1))
    o_up = o_crop.resize((r_crop.size[0], r_crop.size[1]), Image.LANCZOS)
    # equal effective scale check (per axis)
    fr = (r_crop.size[0] / (x1 - x0), r_crop.size[1] / (y1 - y0))
    fo = (o_up.size[0] / (x1 - x0), o_up.size[1] / (y1 - y0))
    assert abs(fr[0] - fo[0]) < 0.01 and abs(fr[1] - fo[1]) < 0.01, (fr, fo)
    rp, op = f"{QA}/crop_1_{name}_render.png", f"{QA}/crop_1_{name}_orig.png"
    r_crop.save(rp)
    o_up.save(op)
    print(f"{name}: render {r_crop.size} orig-upscaled {o_up.size} "
          f"eff scale x={fr[0]:.4f}/{fo[0]:.4f} y={fr[1]:.4f}/{fo[1]:.4f} -> {rp}")
