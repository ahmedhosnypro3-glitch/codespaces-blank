#!/usr/bin/env python3
"""Tight zoom pairs for slide 036 attempt 8 — adjudication evidence for crop-leg
findings (equation glyph/subscript detail and the two class-token case checks).

Same Procedure B method as cut_crops_7.py (rendered from the CURRENT render_8.png,
original LANCZOS-upscaled to the render crop's exact size). No pixels are edited.
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


def cut(name, fx0, fy0, fx1, fy1):
    b = (int(round(fx0)), int(round(fy0)), int(round(fx1)), int(round(fy1)))
    co = o.crop(b)
    cr = r.crop((int(round(fx0 * sx)), int(round(fy0 * sy)),
                 int(round(fx1 * sx)), int(round(fy1 * sy))))
    co = co.resize(cr.size, Image.LANCZOS)
    co.save(f"{OUT}/zoom_8_{name}_orig.png")
    cr.save(f"{OUT}/zoom_8_{name}_render.png")
    print(f"  {name}: frame bbox {b} -> {cr.size} px each side")


print(f"orig {o.size}  render {r.size}  per-axis scale x={sx:.6f} y={sy:.6f}")
cut("eq_head", 70, 330, 200, 422)        # "Define Error function as:" + "Error ="
cut("eq_sigma", 150, 355, 320, 422)      # Sigma display glyph + its subscript limit
cut("eq_term1", 295, 358, 400, 400)      # first W^T X_i group (paren? underline?)
cut("eq_term2", 430, 358, 620, 400)      # second (W^T X_i) group + " take ..."
cut("eq_tail", 600, 355, 800, 400)       # phrase tail + red X mark
cut("b2_class", 295, 275, 560, 318)      # box2 line3 "as Class I ..." token case
cut("b4_class", 295, 488, 560, 534)      # box4 line2 "as Class I ..." token case
cut("b1_line2", 70, 118, 470, 152)       # "let d(X) ... = W^T X" (superscript/underline)
