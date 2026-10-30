#!/usr/bin/env python3
"""Row-by-row ink layout dump for slide 037: render vs original frame.
Dark ink = luminance-based so red/brown/blue all count."""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide037"
ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_037.jpg"
R = np.asarray(Image.open(f"{QA}/render_3.png").convert("RGB")).astype(int)
O = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
s = R.shape[0] / 540.0
print(f"render {R.shape[1]}x{R.shape[0]} scale {s:.4f}")


def dark(a):
    return (a.sum(axis=2) < 430)  # catches C00000 (192) and darker


def runs_for_row(mask, row, x0=0, x1=None, scale=1.0):
    r = int(round(row * scale))
    if x1 is None:
        x1 = mask.shape[1]
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


def dump(mask, label, y0, y1, scale):
    print(f"\n=== {label} (rows {y0}..{y1}) ===")
    for row in range(y0, y1):
        rr = runs_for_row(mask, row, 40, 920, scale)
        if rr:
            txt = "  ".join(f"{a:.0f}-{b:.0f}" for a, b in rr)
            print(f"  r{row:3d}: {txt}")
        else:
            print(f"  r{row:3d}: -")


DR, DO = dark(R), dark(O)
dump(DO, "ORIGINAL", 60, 90, 1.0)
