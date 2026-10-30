#!/usr/bin/env python3
"""Slide 045: text metrics — glyph heights and ink widths, render vs frame (same frame coords)."""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide045"
r = np.asarray(Image.open(QA + "/render_1.png").convert("RGB")).astype(int)
f = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
S = r.shape[0] / 540.0
rl, fl = r.mean(axis=2), f.mean(axis=2)


def box(arr, x0, y0, x1, y1, thr, label):
    """Ink extent in frame coords; for the render the box is scaled by S first."""
    if arr is rl:
        X0, Y0, X1, Y1 = int(round(x0 * S)), int(round(y0 * S)), int(round(x1 * S)), int(round(y1 * S))
        # report in frame units
        def fx(v): return v / S
        def fy(v): return v / S
    else:
        X0, Y0, X1, Y1 = x0, y0, x1, y1
        fx = fy = lambda v: v
    sub = arr[Y0:Y1 + 1, X0:X1 + 1]
    ink = sub < thr
    rows = np.where(ink.sum(axis=1) > 0)[0]
    cols = np.where(ink.sum(axis=0) > 0)[0]
    if len(rows) == 0 or len(cols) == 0:
        print("  %-32s NO INK" % label)
        return
    print("  %-32s y%.0f..%.0f h=%.1f   x%.0f..%.0f w=%.1f" %
          (label, y0 + fy(rows.min()), y0 + fy(rows.max()), fy(rows.max() - rows.min() + 1),
           x0 + fx(cols.min()), x0 + fx(cols.max()), fx(cols.max() - cols.min() + 1)))


print("=== CALC PANEL row1 ===")
for src, thr in ((fl, 200), (rl, 190)):
    print("%s:" % ("frame" if src is fl else "render"))
    box(src, 382, 145, 401, 195, thr, "d-vec digit rows")
    box(src, 732, 145, 752, 195, thr, "W-vec digit rows")
    box(src, 283, 145, 325, 195, thr, "label d(x1) =")
    box(src, 505, 145, 620, 195, thr, "arrow + Keep same Weight")
    box(src, 386, 176, 398, 194, thr, "d-vec '0' (row3)")
    box(src, 528, 158, 542, 178, thr, "'K' in Keep")

print()
print("=== TOP PANEL ===")
for src, thr in ((fl, 200), (rl, 190)):
    print("%s:" % ("frame" if src is fl else "render"))
    box(src, 90, 62, 102, 76, thr, "header x1")
    box(src, 89, 76, 103, 88, thr, "data cell (1)")
    box(src, 266, 74, 328, 88, thr, "Initial W =")
    box(src, 365, 64, 437, 82, thr, "Step eta = 2")
    box(src, 499, 78, 584, 90, thr, "Check classes of")
    box(src, 600, 62, 656, 78, thr, "Z header Z1")
    box(src, 600, 80, 656, 110, thr, "Z data rows")

print()
print("=== AUG TABLE ===")
for src, thr in ((fl, 200), (rl, 190)):
    print("%s:" % ("frame" if src is fl else "render"))
    box(src, 81, 145, 237, 161, thr, "title 'Ugmented Vectors'")
    box(src, 95, 164, 104, 178, thr, "row1 cell")
    box(src, 94, 229, 105, 245, thr, "class row C1")
    box(src, 206, 229, 219, 245, thr, "class row C2")

print()
print("=== STOP BOX ===")
for src, thr in ((fl, 200), (rl, 190)):
    print("%s:" % ("frame" if src is fl else "render"))
    box(src, 68, 348, 130, 370, thr, "'No change in W'")
    box(src, 68, 372, 160, 394, thr, "'Stop Iterations'")

print()
print("=== LEGEND ===")
for src, thr in ((fl, 200), (rl, 190)):
    print("%s:" % ("frame" if src is fl else "render"))
    box(src, 240, 108, 510, 126, thr, "legend line")
