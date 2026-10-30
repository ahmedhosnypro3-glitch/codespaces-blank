#!/usr/bin/env python3
"""Cut matched-scale crop pairs for the S23 paren-sweep vision legs.

Frame-space bbox in; render crop from the certified render at native 150dpi
scale (2.0843 render-px per frame-px), original crop LANCZOS-upscaled from the
960x540 frame to the same effective scale. Pair sizes equal per axis.
"""
import sys

import numpy as np
from PIL import Image

DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
SX = SY = 1125 / 540.0  # 2.0833; render is 2001x1125 (sx=2001/960=2.0844)


def cut(nnn, render, name, fx0, fy0, fx1, fy1):
    rx0, ry0 = int(round(fx0 * SX)), int(round(fy0 * SY))
    rx1, ry1 = int(round(fx1 * SX)), int(round(fy1 * SY))
    r = Image.open(f"{DECK}/recreated_pptx/qa/slide{nnn}/{render}").convert("RGB")
    rc = r.crop((rx0, ry0, rx1, ry1))
    o = Image.open(f"{DECK}/unique_slides/slide_{nnn}.jpg").convert("RGB")
    oc = o.crop((int(fx0), int(fy0), int(fx1), int(fy1)))
    oc = oc.resize(rc.size, Image.LANCZOS)
    base = f"{DECK}/recreated_pptx/qa/slide{nnn}/crop_ps_{name}"
    rc.save(f"{base}_render.png")
    oc.save(f"{base}_orig.png")
    print(f"slide{nnn} {name}: render {rc.size} orig {oc.size} from frame "
          f"({fx0},{fy0},{fx1},{fy1}) render-px ({rx0},{ry0},{rx1},{ry1})")


if __name__ == "__main__":
    nnn, render, name = sys.argv[1], sys.argv[2], sys.argv[3]
    fx0, fy0, fx1, fy1 = map(int, sys.argv[4:8])
    cut(nnn, render, name, fx0, fy0, fx1, fy1)
