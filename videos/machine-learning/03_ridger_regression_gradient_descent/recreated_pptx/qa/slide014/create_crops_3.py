#!/usr/bin/env python3
"""Procedure B crop pairs for slide014 (attempt K) at MATCHED EFFECTIVE SCALE.

Regions chosen from the ORIGINAL frame (unique_slides/slide_014.jpg, 960x540):
  1. title_boxes   — title + both vector boxes            x 48..910, y  50..240
  2. upper_bands   — ridge + objective yellow bands        x 48..910, y 242..340
  3. middle_bands  — peach/yellow/gutter region            x 48..910, y 345..452
  4. lower_region  — loss/reg term boxes + final band      x 48..910, y 462..532

Render crop: same frame-px bbox from render_K.png (150dpi), so render-px =
  frame-px * H_render/540 (exact).
Original crop: the same bbox, LANCZOS-upscaled by H_render/540 so both crops have
  IDENTICAL effective scale (px per frame-px) — never pair different scales.
"""
import sys

from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{DECK}/unique_slides/slide_014.jpg"
REND = f"{DECK}/recreated_pptx/qa/slide014/render_2.png"
OUT = f"{DECK}/recreated_pptx/qa/slide014"

K = sys.argv[1] if len(sys.argv) > 1 else "2"

REGIONS = {
    "title_boxes": (48, 50, 910, 240),
    "upper_bands": (48, 242, 910, 340),
    "middle_bands": (48, 345, 910, 452),
    "lower_region": (48, 462, 910, 532),
}

ro = Image.open(ORIG).convert("RGB")
rr = Image.open(REND).convert("RGB")
RH, RW = rr.size[1], rr.size[0]
OH, OW = ro.size[1], ro.size[0]
SCALE = RH / OH          # render px per frame px
# exact horizontal render px per frame px for the render crop
SCALE_X = RW / OW
print(f"orig {ro.size}  render {rr.size}  SCALE_Y={SCALE:.4f} SCALE_X={SCALE_X:.4f}")

for name, (x0, y0, x1, y1) in REGIONS.items():
    # render crop (exact pixel mapping)
    rx0, ry0 = int(round(x0 * SCALE_X)), int(round(y0 * SCALE))
    rx1, ry1 = int(round(x1 * SCALE_X)), int(round(y1 * SCALE))
    crop_r = rr.crop((rx0, ry0, rx1, ry1))
    # original crop at the same frame-px bbox, then upscaled to the SAME output
    # size so both crops have identical effective scale
    crop_o = ro.crop((x0, y0, x1, y1))
    crop_o_up = crop_o.resize(crop_r.size, Image.LANCZOS)
    pr = f"{OUT}/crop_{K}_{name}_render.png"
    po = f"{OUT}/crop_{K}_{name}_orig.png"
    crop_r.save(pr)
    crop_o_up.save(po)
    # verify effective scales match
    eff_r = crop_r.size[0] / (x1 - x0)
    eff_o = crop_o.size[0] / (x1 - x0)
    up = crop_o_up.size[0] / crop_o.size[0]
    print(f"  {name:14s} frame bbox x{x0}..{x1} y{y0}..{y1}  "
          f"render {crop_r.size} eff_x={eff_r:.4f}  "
          f"orig {crop_o.size} -> upscaled x{up:.4f} -> {crop_o_up.size} eff_x={eff_o:.4f}  "
          f"MATCH={'YES' if abs(eff_r-eff_o)<1e-6 else 'NO'}")
