#!/usr/bin/env python3
"""Slide 049 — per-row ink runs for each paren region, ORIG vs RENDER_13.

Threshold <215 catches light-gray JPEG strokes. Render block-downsampled to
frame scale. Output: one line per row with ink runs as x-ranges.
"""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.array(Image.open(BASE + "/unique_slides/slide_049.jpg").convert("L"), dtype=np.float32)
rend_img = Image.open(BASE + "/recreated_pptx/qa/slide049/render_13.png").convert("L")
S = rend_img.size[1] / orig.shape[0]

REGIONS = [
    ( 84,  74, 110, 112, "A col1 pair"),
    (314,  58, 360, 100, "B initial-W"),
    (634,  84, 664, 124, "C pair1"),
    ( 86, 176, 112, 228, "D pair1"),
    (372, 142, 410, 196, "E high-bracket col"),
    (714, 142, 752, 196, "F W-col row1"),
]

def runs_line(row, thr=215):
    out, cur = [], None
    for i, v in enumerate(row):
        on = v < thr
        if on and cur is None:
            cur = i
        elif not on and cur is not None:
            out.append((cur, i - 1)); cur = None
    if cur is not None:
        out.append((cur, len(row) - 1))
    return out

for (x0, y0, x1, y1, name) in REGIONS:
    o = orig[y0:y1 + 1, x0:x1 + 1]
    r = np.array(rend_img.crop((int(x0 * S), int(y0 * S), int((x1 + 1) * S), int((y1 + 1) * S))),
                 dtype=np.float32)
    h, w = r.shape
    r_small = r[: (h // 2) * 2, : (w // 2) * 2].reshape(h // 2, 2, w // 2, 2).mean(axis=(1, 3))
    print(f"\n===== {name} ({x0},{y0})-({x1},{y1}) =====")
    print("-- ORIG runs (x offset {}) --".format(x0))
    for i, row in enumerate(o):
        rr = runs_line(row)
        if rr:
            print(f"y{y0 + i}: " + " ".join(f"{x0 + a}-{x0 + b}" for a, b in rr))
    print("-- RENDER runs (x offset {}) --".format(x0))
    for i, row in enumerate(r_small):
        rr = runs_line(row)
        if rr:
            print(f"y~{y0 + i}: " + " ".join(f"{x0 + a}-{x0 + b}" for a, b in rr))
