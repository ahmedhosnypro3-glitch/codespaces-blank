#!/usr/bin/env python3
"""Row-by-row band profile (left/right extents + fill color) for render_2 and
the original, so band geometry and fills can be compared directly."""
import numpy as np
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
QA = NS + "recreated_pptx/qa/slide014/"

def profile(img, scale, label, y0=40, y1=540):
    print(f"--- {label} ---")
    nz = (np.abs(img - 255).max(axis=2) > 12)
    rowcount = nz.sum(axis=1)
    state = None
    for y in range(y0, y1):
        c = rowcount[y] if y < len(rowcount) else 0
        s = "BAND" if c > 400 else ("ink" if c > 15 else "empty")
        if s != state:
            cols = np.where(nz[y, :])[0] if c else []
            ext = f"x {cols.min()}..{cols.max()}" if len(cols) else "-"
            print(f"  y={y:4d} {s:5s} count={c:4d} {ext}")
            state = s

RV = np.asarray(Image.open(QA + "render_2.png").convert("RGB")).astype(int)
OG = np.asarray(Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")).astype(int)
profile(OG, 1.0, "ORIGINAL (960x540)")
profile(RV, 2001 / 960.0, "RENDER_2 (2001x1125)")
