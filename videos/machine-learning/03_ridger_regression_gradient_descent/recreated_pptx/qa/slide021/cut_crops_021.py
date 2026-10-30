#!/usr/bin/env python3
"""Procedure B: cut matched-scale crop pairs for slide 021 (attempt 10, render_10.png).

Regions chosen from the ORIGINAL frame (960x540) per the frozen protocol
(judge_protocol_03.md Procedure B): every dense region, ~8px padding.
Render: 150dpi (2001x1125) -> multiply frame coords by H_render/540.
Original: LANCZOS-upscaled by the same factor so output_px/frame_px is EQUAL.
"""
from PIL import Image

ROOT = "/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{ROOT}/unique_slides/slide_021.jpg"
REND = f"{ROOT}/recreated_pptx/qa/slide021/render_10.png"
QADIR = f"{ROOT}/recreated_pptx/qa/slide021"

# (slug, x0, y0, x1, y1, description)  frame px, ~8px padding
REGIONS = [
    ("top_table_eq",   88, 126, 322, 232,
     "top-left of the first block: the red X^T X label equation and the full 3x3 singular matrix table with its gridlines"),
    ("top_chain",      332, 182, 802, 218,
     "first block's determinant chain: |X^T X| = 0, two blue arrows, 'Singular Matrix', red italic 'No Inverse'"),
    ("mid_table_eq",   80, 290, 322, 402,
     "second block's left side: the (X^T X + lambda I) label, green lambda=3, the full 3x3 regularized matrix, and the three FDFD96 highlight bands on the 17/43/95 diagonal"),
    ("mid_chain",      332, 348, 892, 382,
     "second block's determinant chain: |X^T X| = 5685, two blue arrows, 'Non-Singular Matrix', red italic 'Inverse Exists'"),
    ("bot_eq_table",   148, 450, 642, 519,
     "bottom block: the (X^T X + lambda I)^-1 expression, the long blue arrow, and the 3x3 inverse matrix table of decimals"),
]

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")
SC = r.size[1] / 540.0
print(f"scale = H_render/540 = {SC:.6f}")

for slug, x0, y0, x1, y1, desc in REGIONS:
    # exact render-px box first (ground truth), then derive the original crop from it
    # so the two crops have IDENTICAL pixel dimensions and identical effective scale
    rx0, ry0 = int(round(x0 * SC)), int(round(y0 * SC))
    rx1, ry1 = int(round((x1 + 1) * SC)), int(round((y1 + 1) * SC))
    rc = r.crop((rx0, ry0, rx1, ry1))
    w, h = rc.size
    oc = o.crop((x0, y0, x1 + 1, y1 + 1)).resize((w, h), Image.LANCZOS)
    po = f"{QADIR}/crop_10_{slug}_orig.png"
    pr = f"{QADIR}/crop_10_{slug}_render.png"
    oc.save(po); rc.save(pr)
    print(f"{slug:16s} region x{x0}..{x1} y{y0}..{y1}  orig {oc.size}  render {rc.size}  "
          f"match={oc.size == rc.size}")
    with open(f"{QADIR}/crop_10_{slug}_desc.txt", "w") as f:
        f.write(desc + "\n")
