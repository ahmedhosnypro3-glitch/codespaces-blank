#!/usr/bin/env python3
"""Baseline-structure probe, slide 029 attempt 1: per-row ink profiles of each
title line, ORIGINAL vs RENDER, same sensitive predicate + same x-window per
line, to adjudicate the y0 band-top delta (+4.4px) seen in selfcheck_attempt_1.

Hypothesis to test: the original's band TOP is inflated by JPEG halo above thin
ascender tips (rows 191-192 carry only 12-44 px), while the render's clean AA
shows the true ascender tip. If so, the render's ASCENDER rows should align with
the original's rows 193-194 and the x-height core + baseline rows must match.
"""
import numpy as np
from PIL import Image

REND = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide029/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_029.jpg"

LINES = [
    ("L1", (185, 245), (130, 830)),
    ("L2", (263, 323), (260, 675)),
    ("L3", (341, 400), (228, 718)),
]


def rows(path, wy, wx, label):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    H = im.shape[0]
    sc = H / 540.0
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    dist = np.sqrt((r - 231) ** 2 + (g - 233) ** 2 + (b - 230) ** 2)
    ink = dist > 40
    y0, y1 = int(wy[0] * sc), int(wy[1] * sc)
    x0, x1 = int(wx[0] * sc), int(wx[1] * sc)
    seg = ink[y0:y1, x0:x1]
    p = seg.sum(axis=1)
    mx = p.max()
    print(f"  [{label}] rows {wy[0]}..{wy[1]} frame px (x {wx[0]}..{wx[1]}):")
    line = []
    for i, c in enumerate(p):
        mark = "#" if c > mx * 0.55 else ("+" if c > mx * 0.2 else ".")
        line.append(f"{wy[0] + i / sc:5.1f}:{c:4d}{mark}")
    for j in range(0, len(line), 6):
        print("    " + "  ".join(line[j:j + 6]))
    core = [i for i, c in enumerate(p) if c > mx * 0.2]
    faint_top = [i for i, c in enumerate(p) if 0 < c <= mx * 0.2]
    print(f"    core(>20%) rows: {wy[0] + core[0] / sc:.1f}..{wy[0] + core[-1] / sc:.1f}"
          f"  | faint tail rows below core end: "
          f"{[f'{wy[0] + i / sc:.1f}' for i in faint_top if i > core[-1]][:12]}")


for name, wy, wx in LINES:
    print(f"================ {name} ================")
    rows(ORIG, wy, wx, "ORIG")
    rows(REND, wy, wx, "REND")
