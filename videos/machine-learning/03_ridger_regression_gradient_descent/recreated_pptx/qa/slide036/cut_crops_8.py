#!/usr/bin/env python3
"""Procedure B crop pairs for slide 036 attempt 8 (run 859463, worker w036).

Cut FRESH pairs from the CURRENT render (render_8.png, md5 checked in the driver)
so both legs are judged on the same bytes as the banked full-slide transcript.

Method (mission protocol §7 / judge_protocol_03.md Procedure B):
  * region = slide-space bbox in FRAME px (960x540, +8 px padding around the ink)
  * render crop: the same frame bbox scaled by the render's per-axis scale
  * original crop: the frame bbox LANCZOS-upscaled to the render crop's exact size
    => output_px/frame_px is identical on both sides (matched effective scale)

Regions (dense clusters chosen from the ORIGINAL frame):
  eq_stack     box 3: the composite Error equation (Sigma display glyph + limits,
               two W^T X_i groups, trailing phrase) and the red X mark
  delta_lines  box 4: the two delta_i conditional lines with sub/superscripts
  class_lines  boxes 1+2: the small-text clusters (colored class tokens,
               W^T superscript, membership signs, inequality results)
"""
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{V}/unique_slides/slide_036.jpg"
REND = f"{V}/recreated_pptx/qa/slide036/render_8.png"
OUT = f"{V}/recreated_pptx/qa/slide036"

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")
sx = r.size[0] / 960.0
sy = r.size[1] / 540.0
print(f"orig {o.size}  render {r.size}  per-axis scale x={sx:.6f} y={sy:.6f}")


def cut(name, fx0, fy0, fx1, fy1):
    b = (int(round(fx0)), int(round(fy0)), int(round(fx1)), int(round(fy1)))
    co = o.crop(b)
    cr = r.crop((int(round(fx0 * sx)), int(round(fy0 * sy)),
                 int(round(fx1 * sx)), int(round(fy1 * sy))))
    co = co.resize(cr.size, Image.LANCZOS)   # match effective scale exactly
    co.save(f"{OUT}/crop_8_{name}_orig.png")
    cr.save(f"{OUT}/crop_8_{name}_render.png")
    print(f"  {name}: frame bbox {b}  crop size {cr.size}  "
          f"eff px/frame-px render=({cr.size[0]/(fx1-fx0):.4f},{cr.size[1]/(fy1-fy0):.4f}) "
          f"orig=({co.size[0]/(fx1-fx0):.4f},{co.size[1]/(fy1-fy0):.4f})")


cut("eq_stack", 60, 320, 890, 430)      # box 3 equation + Sigma limits + red X
cut("delta_lines", 60, 433, 880, 539)   # box 4 (delta_i lines)
cut("class_lines", 60, 90, 880, 318)    # boxes 1+2 small-text clusters
