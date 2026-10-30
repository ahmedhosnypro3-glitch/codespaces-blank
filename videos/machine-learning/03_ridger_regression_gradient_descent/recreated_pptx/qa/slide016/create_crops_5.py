#!/usr/bin/env python3
"""Procedure B crop-pair cutter for slide 016, attempt 5 (worker-016-finish-20261024).

Frame-space bbox -> same bbox cropped from BOTH render_5.png (150dpi, s=1125/540=2.0833
render px per frame px) and the 960x540 original; the original crop is LANCZOS-upscaled
by the same s so output_px/frame_px is EQUAL on both axes (protocol 03 step 3).

Regions (from the measured line inventory + the attempt-4 disputed region):
  missing_band  y330..450 — L2/L1 bullet continuations + blue key terms + red runs
                          (the band that was BLANK in render_1; must be re-certified)
  bullet2       y225..300 — bullet 2 (b2a/b2b/b2c): the region the attempt-4 judge
                          flagged (wording MAJOR) + yellow highlight + red underline
  last_bullet   y478..532 — small-text cluster: red (N)/(d) + dark underline under "Length"
"""
from PIL import Image

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
RENDER = f"{QA}/render_5.png"
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")

r_im = Image.open(RENDER).convert("RGB")
o_im = Image.open(ORIG).convert("RGB")
H_f = o_im.size[1]
s = r_im.size[1] / H_f
print(f"render {r_im.size}  original {o_im.size}  scale s={s:.4f}")

REGIONS = [
    ("missing_band", 80, 325, 815, 455),
    ("bullet2",      80, 222, 820, 302),
    ("last_bullet",  80, 475, 820, 532),
]

for name, x0, y0, x1, y1 in REGIONS:
    r_box = (round(x0 * s), round(y0 * s), round(x1 * s), round(y1 * s))
    r_crop = r_im.crop(r_box)
    o_crop = o_im.crop((x0, y0, x1, y1))
    o_up = o_crop.resize((r_crop.size[0], r_crop.size[1]), Image.LANCZOS)
    er = (r_crop.size[0] / (x1 - x0), r_crop.size[1] / (y1 - y0))
    eo = (o_up.size[0] / (x1 - x0), o_up.size[1] / (y1 - y0))
    assert abs(er[0] - eo[0]) < 0.01 and abs(er[1] - eo[1]) < 0.01, (er, eo)
    rp, op = f"{QA}/crop_5_{name}_render.png", f"{QA}/crop_5_{name}_orig.png"
    r_crop.save(rp)
    o_up.save(op)
    print(f"{name}: render {r_crop.size} orig-upscaled {o_up.size} "
          f"eff scale x={er[0]:.4f}/{eo[0]:.4f} y={er[1]:.4f}/{eo[1]:.4f}")
    print(f"  -> {rp}")
    print(f"  -> {op}")
