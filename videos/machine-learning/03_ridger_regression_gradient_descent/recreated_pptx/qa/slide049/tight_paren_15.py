#!/usr/bin/env python3
"""Slide 049 — tight per-paren crops, ORIG vs RENDER_13 at 1 char = 1 frame px."""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.array(Image.open(BASE + "/unique_slides/slide_049.jpg").convert("L"), dtype=np.float32)
rend_img = Image.open(BASE + "/recreated_pptx/qa/slide049/render_13.png").convert("L")
S = rend_img.size[1] / orig.shape[0]

CROPS = [
    ( 84,  73, 108, 112, "A col1 pair (font parens)"),
    (322,  50, 340,  98, "B initial-W left delim"),
    (636,  84, 662, 122, "C pair1 (z49 bezier)"),
    ( 88, 176, 114, 226, "D pair1 (aug bezier)"),
    (374, 142, 404, 195, "E wcol_1 tall col"),
    (716, 142, 748, 195, "F wcol_2 W-col row1"),
]

def art(a):
    out = []
    for row in a:
        out.append("".join("#" if v < 110 else ("+" if v < 170 else " ") for v in row).rstrip())
    return "\n".join(out)

for (x0, y0, x1, y1, name) in CROPS:
    o = orig[y0:y1 + 1, x0:x1 + 1]
    r = np.array(rend_img.crop((int(x0 * S), int(y0 * S), int((x1 + 1) * S), int((y1 + 1) * S))),
                 dtype=np.float32)
    h, w = r.shape
    r_small = r[: (h // 2) * 2, : (w // 2) * 2].reshape(h // 2, 2, w // 2, 2).mean(axis=(1, 3))
    oh, ow = o.shape
    print(f"\n===== {name}  ({x0},{y0})-({x1},{y1}) =====")
    print("--- ORIG ---")
    print(art(o))
    print("--- RENDER ---")
    print(art(r_small))
