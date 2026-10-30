#!/usr/bin/env python3
"""Attempt-5 Procedure B crop pairs at matched effective scale (from render_5)."""
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{DECK}/unique_slides/slide_014.jpg"
REND = f"{DECK}/recreated_pptx/qa/slide014/render_6.png"
OUT = f"{DECK}/recreated_pptx/qa/slide014"
K = "6"

REGIONS = {
    "bands":   (48, 242, 910, 347),  # ridge + objective navy-ruled bands
    "vectors": (48, 50, 910, 240),   # y / y-hat vector-definition boxes
    "final":   (48, 462, 910, 532),  # final pale-cyan objective band
}

ro = Image.open(ORIG).convert("RGB")
rr = Image.open(REND).convert("RGB")
SCALE_Y = rr.size[1] / ro.size[1]
SCALE_X = rr.size[0] / ro.size[0]
print(f"orig {ro.size} render {rr.size} SCALE {SCALE_X:.4f}/{SCALE_Y:.4f}")

for name, (x0, y0, x1, y1) in REGIONS.items():
    rx0, ry0 = round(x0 * SCALE_X), round(y0 * SCALE_Y)
    rx1, ry1 = round(x1 * SCALE_X), round(y1 * SCALE_Y)
    crop_r = rr.crop((rx0, ry0, rx1, ry1))
    crop_o = ro.crop((x0, y0, x1, y1)).resize(crop_r.size, Image.LANCZOS)
    crop_r.save(f"{OUT}/crop_{K}_{name}_render.png")
    crop_o.save(f"{OUT}/crop_{K}_{name}_orig.png")
    print(f"  {name}: frame x{x0}..{x1} y{y0}..{y1} -> {crop_r.size}")
