#!/usr/bin/env python3
"""Row-by-row layout dump for slide 037 — render vs original side by side."""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide037"
ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_037.jpg"
import sys
REN = sys.argv[1] if len(sys.argv) > 1 else f"{QA}/render_3.png"
R = np.asarray(Image.open(REN).convert("RGB")).astype(int)
O = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
s = R.shape[0] / 540.0


def dark(a):
    return (a.sum(axis=2) < 430)


def runs_for_row(mask, row, x0, x1, scale):
    r = int(round(row * scale))
    line = mask[r, int(x0 * scale):int(x1 * scale)]
    idx = np.where(line)[0]
    if not len(idx):
        return []
    out, start, prev = [], idx[0], idx[0]
    for i in idx[1:]:
        if i > prev + 6:
            out.append((round((start + x0 * scale) / scale, 1), round((prev + x0 * scale) / scale, 1)))
            start = i
        prev = i
    out.append((round((start + x0 * scale) / scale, 1), round((prev + x0 * scale) / scale, 1)))
    return out


def dump(mask, label, y0, y1, scale, x0=40, x1=920):
    print(f"\n=== {label} (rows {y0}..{y1}) ===")
    for row in range(y0, y1):
        rr = runs_for_row(mask, row, x0, x1, scale)
        txt = "  ".join(f"{a:.0f}-{b:.0f}" for a, b in rr) if rr else "-"
        print(f"  r{row:3d}: {txt}")


DR, DO = dark(R), dark(O)
A, B = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (60, 90)
dump(DO, "ORIGINAL", A, B, 1.0)
dump(DR, "RENDER", A, B, s)
dump(DO, "ORIGINAL", B, B + 60, 1.0)
dump(DR, "RENDER", B, B + 60, s)
