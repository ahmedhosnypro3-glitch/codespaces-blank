#!/usr/bin/env python3
"""Procedure B crop-pair prep, slide 029 attempt 1 (judge_protocol_03.md §B).

Region: the title block — the slide's single dense content region (the three
bold-red title lines, incl. the '(GD)' parens + colon + descenders).
Frame-px bbox (960x540): x 125..840, y 180..403 (title ink x 137-824, y 191-392,
with ~8-12px padding).

Matched effective scale law (§B.3): output_px/frame_px EQUAL per axis.
  render_2.png: 2001x1125 (150dpi) -> scale = H/540 = 2.0833 (protocol formula);
    crop by frame coords x scale, no rescale.
  original 960x540: same frame-px bbox, LANCZOS-upscale by H/540 = 2.0833.
Both crops: ~1490x465 px, effective scale 2.0833 px/frame-px per axis.
"""
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide029"
REND = f"{QA}/render_2.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_029.jpg"

X0, Y0, X1, Y1 = 125, 180, 840, 403  # frame px

rend = Image.open(REND)
sc = rend.size[1] / 540.0  # H_render/540
rx0, ry0, rx1, ry1 = (int(round(X0 * sc)), int(round(Y0 * sc)),
                      int(round(X1 * sc)), int(round(Y1 * sc)))
rc = rend.crop((rx0, ry0, rx1, ry1))
rc.save(f"{QA}/crop_1_title_render.png")
print(f"render crop: frame ({X0},{Y0})-({X1},{Y1}) -> render px ({rx0},{ry0})-({rx1},{ry1}) "
      f"size {rc.size}  effective scale {rc.size[0] / (X1 - X0):.4f} x {rc.size[1] / (Y1 - Y0):.4f}")

orig = Image.open(ORIG)
oc = orig.crop((X0, Y0, X1, Y1))  # 715 x 223
tw, th = int(round((X1 - X0) * sc)), int(round((Y1 - Y0) * sc))
oc = oc.resize((tw, th), Image.LANCZOS)
oc.save(f"{QA}/crop_1_title_orig.png")
print(f"orig crop: 715x223 -> LANCZOS x{sc:.4f} -> {oc.size}  "
      f"effective scale {oc.size[0] / (X1 - X0):.4f} x {oc.size[1] / (Y1 - Y0):.4f}")

# assert matched effective scale per axis
rsc_x, rsc_y = rc.size[0] / (X1 - X0), rc.size[1] / (Y1 - Y0)
osc_x, osc_y = oc.size[0] / (X1 - X0), oc.size[1] / (Y1 - Y0)
ok = abs(rsc_x - osc_x) < 0.02 and abs(rsc_y - osc_y) < 0.02
print(f"scale match: dx={abs(rsc_x - osc_x):.5f} dy={abs(rsc_y - osc_y):.5f} -> "
      + ("MATCHED" if ok else "MISMATCH — FIX BEFORE JUDGING"))
