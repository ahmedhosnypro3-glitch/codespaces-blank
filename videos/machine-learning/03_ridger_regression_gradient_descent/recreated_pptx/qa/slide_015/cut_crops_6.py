#!/usr/bin/env python3
r"""Cut Procedure B crop pairs for slide 015, attempt 6 (render_6), at MATCHED
effective scale. Regions identical to the banked attempt-4 cutter (cut_crops_4.py)
— the slide's five dense regions. No payloads are emitted here; the crop judges
source the frozen Template B payload directly from shared_patterns/judge_protocol_03.md.

No vision call is made here.  Usage: cut_crops_6.py
"""
import json
import os

import numpy as np
from PIL import Image

REPO = "/home/ahmed/Projects/ai_llm_slides"
DECK = f"{REPO}/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{DECK}/recreated_pptx/qa/slide_015"
RENDER = f"{QA}/render_6.png"
ORIG = f"{DECK}/unique_slides/slide_015.jpg"
OUT = f"{QA}/crops_6.json"

ATTEMPT = 6
# (slug, region description, frame bbox x0,x1,y0,y1) — same as attempt 4
REGIONS = [
    ("eq_stack", "three-line J(W) objective-function expansion stack", 89, 799, 100, 271),
    ("pinkbox", "the ∂J/∂W = 0 identity and the 'Get Best W ... J(W)' "
                "sentence inside the red-bordered callout box", 73, 710, 268, 325),
    ("peachbox", "the Remember label and the ∂W^TW/∂W = 2W matrix-derivative "
                 "identity inside the peach box", 783, 898, 271, 337),
    ("deriv_stack", "the two ∂J/∂W simplification lines (gradient steps)", 71, 518, 343, 475),
    ("solution", "the closed-form W = (X^TX + λI)^-1 X^TY "
                 "normal-equation solution in the green box", 545, 893, 466, 523),
]

SCALE = 1125 / 540.0   # render px per frame px (150dpi fleet convention)


def crop_pair(x0, x1, y0, y1):
    """Return (render_crop, orig_crop) as equal-size PIL images."""
    tw = int(round((x1 - x0 + 1) * SCALE))
    th = int(round((y1 - y0 + 1) * SCALE))
    r = Image.open(RENDER).convert("RGB")
    rx0, ry0 = int(round(x0 * r.width / 960.0)), int(round(y0 * r.height / 540.0))
    rx1 = int(round((x1 + 1) * r.width / 960.0))
    ry1 = int(round((y1 + 1) * r.height / 540.0))
    rc = r.crop((rx0, ry0, rx1, ry1)).resize((tw, th), Image.LANCZOS)
    o = Image.open(ORIG).convert("RGB")
    oc = o.crop((x0, y0, x1 + 1, y1 + 1)).resize((tw, th), Image.LANCZOS)
    return rc, oc


def main():
    os.makedirs(QA, exist_ok=True)
    r = Image.open(RENDER)
    o = Image.open(ORIG)
    print(f"render {r.size}  orig {o.size}  scale {SCALE:.6f} render-px/frame-px")
    made = []
    for slug, desc, x0, x1, y0, y1 in REGIONS:
        rc, oc = crop_pair(x0, x1, y0, y1)
        assert rc.size == oc.size, (slug, rc.size, oc.size)
        eff = rc.size[0] / (x1 - x0 + 1)
        rp = f"{QA}/crop_{ATTEMPT}_{slug}_render.png"
        op = f"{QA}/crop_{ATTEMPT}_{slug}_orig.png"
        rc.save(rp)
        oc.save(op)
        a = np.asarray(rc.convert("L"))
        b = np.asarray(oc.convert("L"))
        made.append({
            "slug": slug, "desc": desc,
            "bbox_frame": [x0, x1, y0, y1], "frame_wh": [x1 - x0 + 1, y1 - y0 + 1],
            "out_px": list(rc.size), "effective_scale": round(eff, 5),
            "render_png": rp, "orig_png": op,
            "ink_lt150_render": int((a < 150).sum()), "ink_lt150_orig": int((b < 150).sum()),
        })
        print(f"  {slug:12s} frame x{x0}..{x1} y{y0}..{y1} "
              f"({x1 - x0 + 1}x{y1 - y0 + 1}px) -> {rc.size}px "
              f"eff {eff:.4f}  ink r/o {int((a < 150).sum())}/{int((b < 150).sum())}")
    json.dump({"attempt": ATTEMPT, "render": RENDER, "orig": ORIG,
               "scale": SCALE, "crops": made},
              open(OUT, "w"), indent=1)
    print(f"\nbanked {OUT} with {len(made)} crop pairs")


if __name__ == "__main__":
    main()
