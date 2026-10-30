#!/usr/bin/env python3
"""Slide 049 — ASCII dumps of parenthesis regions, ORIG vs RENDER_13 (PIL-only).

Renders each region at 1 char per frame-px: original directly, render_13
downsampled to frame scale (block-mean). Two thresholds: any-ink (.) and
dark-ink (#) so thin strokes survive.
"""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.array(Image.open(BASE + "/unique_slides/slide_049.jpg").convert("L"), dtype=np.float32)
rend = Image.open(BASE + "/recreated_pptx/qa/slide049/render_13.png").convert("L")
S = rend.size[1] / orig.shape[0]

REGIONS = [
    ( 83,  66, 222, 132, "A top-table 2-stacks"),
    (320,  44, 436,  98, "B initial-W vector"),
    (630,  60, 710, 128, "C Z-block parens"),
    ( 84, 170, 228, 232, "D aug-table parens"),
    (368, 140, 404, 194, "E calc-row left delim row1"),
    (706, 140, 774, 194, "F calc-row right delim row1"),
]

def ascii_art(a):
    out = []
    for row in a:
        line = []
        for v in row:
            line.append("#" if v < 100 else ("." if v < 150 else " "))
        out.append("".join(line).rstrip())
    return "\n".join(out)

for (x0, y0, x1, y1, name) in REGIONS:
    o = orig[y0:y1 + 1, x0:x1 + 1]
    r = np.array(rend.crop((int(x0 * S), int(y0 * S), int((x1 + 1) * S), int((y1 + 1) * S))),
                 dtype=np.float32)
    h, w = r.shape
    r_small = r[: (h // 2) * 2, : (w // 2) * 2].reshape(h // 2, 2, w // 2, 2).mean(axis=(1, 3))
    # pad orig to same frame size as render crop (should match already)
    oh, ow = o.shape
    print(f"\n===== {name}  frame box ({x0},{y0})-({x1},{y1}) =====")
    print("--- ORIG ---")
    print(ascii_art(o))
    print("--- RENDER (downsampled to frame scale) ---")
    print(ascii_art(r_small))
