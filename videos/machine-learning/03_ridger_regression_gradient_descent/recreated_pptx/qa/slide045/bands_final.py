#!/usr/bin/env python3
"""Slide 045: precise per-row y bands for the top table, Z table, and stop box."""
import numpy as np
from PIL import Image

F = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_045.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
lum = a.mean(axis=2)


def bands(x0, x1, y0, y1, thr=205, label="", minrun=1):
    sub = lum[y0:y1 + 1, x0:x1 + 1]
    prof = (sub < thr).sum(axis=1)
    out, cur = [], None
    for i, v in enumerate(prof):
        if v > 0 and cur is None:
            cur = [y0 + i, y0 + i]
        elif v > 0:
            cur[1] = y0 + i
        else:
            if cur:
                out.append((cur[0], cur[1])); cur = None
    if cur:
        out.append((cur[0], cur[1]))
    print("%-28s %s" % (label, " ".join("y%d..%d(h=%d)" % (b[0], b[1], b[1]-b[0]+1) for b in out)))
    return out


print("=== TOP data table, one column (x89..103) — rows x header/data/class ===")
bands(89, 104, 60, 130, 205, "col1 x89..104")

print("=== TOP data table, col2 (x111..125) ===")
bands(111, 126, 60, 130, 205, "col2 x111..126")

print("=== Z table header (x600..656) ===")
bands(597, 658, 60, 116, 205, "Z region")

print("=== Z table cols separately ===")
bands(597, 614, 60, 116, 205, "Z col1")
bands(621, 636, 60, 116, 205, "Z col2")
bands(642, 658, 60, 116, 205, "Z col3")

print("=== Aug table rows ===")
bands(95, 105, 160, 250, 205, "aug col1 values")
bands(93, 107, 176, 228, 205, "aug col1 data rows")

print("=== Stop box lines (x64..246) ===")
bands(66, 244, 330, 418, 210, "stop box all ink")

print("=== Iteration badge text (x84..214) ===")
bands(85, 213, 276, 306, 210, "badge text")

print("=== Legend line, full x range ===")
bands(238, 512, 104, 128, 210, "legend")

print("=== Calc panel text-line y bands per row (left label col) ===")
for i, (y0, y1) in enumerate([(140, 200), (205, 265), (270, 332), (336, 397), (402, 463), (468, 530)]):
    bands(282, 325, y0, y1, 205, "calc row%d label" % (i + 1))
print()
print("=== Calc panel: 'Keep same Weight' y bands per row (x525..619) ===")
for i, (y0, y1) in enumerate([(140, 200), (205, 265), (270, 332), (336, 397), (402, 463), (468, 530)]):
    bands(524, 620, y0, y1, 205, "calc row%d keep" % (i + 1))
print()
print("=== Calc panel: W label + bracket y bands per row (x698..760) ===")
for i, (y0, y1) in enumerate([(140, 200), (205, 265), (270, 332), (336, 397), (402, 463), (468, 530)]):
    bands(698, 760, y0, y1, 205, "calc row%d W" % (i + 1))
