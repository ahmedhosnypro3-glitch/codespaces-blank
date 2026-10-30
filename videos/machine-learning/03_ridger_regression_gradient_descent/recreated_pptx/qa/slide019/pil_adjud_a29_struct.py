#!/usr/bin/env python3
"""PIL adjudication of Template A attempt-29 MAJOR findings on slide 019.

Finding (a): original encloses each column in a separate closed colored
rectangle (dark-blue NO REG, red Ridge-3, green Ridge-10, blue rounded Outlier)
with visible gaps; recreation renders a continuous line grid.
Finding (b): original x1/x2/y labels sit OUTSIDE the ruled cell grid (no
bordered label column); recreation adds a bordered first column.

Method: color-classified stroke census of the ORIGINAL frame (960x540) vs the
banked render_27 (2001x1125, S=2001/960), long-run detection per column/row.
"""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(ROOT + "/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(ROOT + "/recreated_pptx/qa/slide019/render_27.png").convert("RGB")).astype(int)
SX, SY = rend.shape[1] / orig.shape[1], rend.shape[0] / orig.shape[0]
print(f"orig {orig.shape[1]}x{orig.shape[0]}  render {rend.shape[1]}x{rend.shape[0]}  S={SX:.4f},{SY:.4f}")

def classify(px):
    r, g, b = px
    if r < 120 and g < 120 and b < 120:
        return "dark"
    if b > r + 30 and b > g + 20 and b > 90:
        return "blue"
    if r > g + 40 and r > b + 40 and r > 110:
        return "red"
    if g > r + 30 and g > b + 30 and g > 90:
        return "green"
    return None

def stroke_census(img, scale, name, y0f, y1f, x0f, x1f, min_run):
    """Report vertical strokes: per x, longest run of same-class pixels."""
    Y0, Y1, X0, X1 = int(y0f * scale[1]), int(y1f * scale[1]), int(x0f * scale[0]), int(x1f * scale[0])
    region = img[Y0:Y1, X0:X1]
    H = region.shape[0]
    print(f"\n== {name} vertical strokes in frame x[{x0f},{x1f}] y[{y0f},{y1f}] (min run {min_run} frame px) ==")
    found = {}
    for x in range(region.shape[1]):
        best = None
        run_cls, run_len, run_start = None, 0, 0
        for y in range(H):
            c = classify(region[y, x])
            if c == run_cls and c is not None:
                run_len += 1
            else:
                if run_cls is not None and run_len >= min_run * scale[1] and (best is None or run_len > best[1]):
                    best = (run_cls, run_len, run_start)
                run_cls, run_len, run_start = c, 1, y
        if run_cls is not None and run_len >= min_run * scale[1] and (best is None or run_len > best[1]):
            best = (run_cls, run_len, run_start)
        if best:
            xf = X0 / scale[0] + x / scale[0]
            y0 = Y0 / scale[1] + best[2] / scale[1]
            y1 = Y0 / scale[1] + (best[2] + best[1]) / scale[1]
            found[round(xf)] = (best[0], round(y0), round(y1), round(best[1] / scale[1]))
    # merge adjacent x columns of same class
    merged = []
    for xf in sorted(found):
        cls, y0, y1, ln = found[xf]
        if merged and abs(xf - merged[-1][0]) <= 2 and merged[-1][1] == cls:
            px0, c_, a, b_, ln0 = merged[-1]
            merged[-1] = (px0, c_, min(a, y0), max(b_, y1), max(ln, ln0))
        else:
            merged.append((xf, cls, y0, y1, ln))
    for xf, cls, y0, y1, ln in merged:
        print(f"  x~{xf} {cls:5s} y{y0}..{y1} (len {ln})")

def hstroke_census(img, scale, name, y0f, y1f, x0f, x1f, min_run):
    Y0, Y1, X0, X1 = int(y0f * scale[1]), int(y1f * scale[1]), int(x0f * scale[0]), int(x1f * scale[0])
    region = img[Y0:Y1, X0:X1]
    W = region.shape[1]
    print(f"\n== {name} horizontal strokes in frame y[{y0f},{y1f}] x[{x0f},{x1f}] ==")
    found = {}
    for y in range(region.shape[0]):
        best = None
        run_cls, run_len, run_start = None, 0, 0
        for x in range(W):
            c = classify(region[y, x])
            if c == run_cls and c is not None:
                run_len += 1
            else:
                if run_cls is not None and run_len >= min_run * scale[0] and (best is None or run_len > best[1]):
                    best = (run_cls, run_len, run_start)
                run_cls, run_len, run_start = c, 1, x
        if run_cls is not None and run_len >= min_run * scale[0] and (best is None or run_len > best[1]):
            best = (run_cls, run_len, run_start)
        if best:
            yf = Y0 / scale[1] + y / scale[1]
            x0 = X0 / scale[0] + best[2] / scale[0]
            x1 = X0 / scale[0] + (best[2] + best[1]) / scale[0]
            found[round(yf)] = (best[0], round(x0), round(x1), round(best[1] / scale[0]))
    merged = []
    for yf in sorted(found):
        cls, x0, x1, ln = found[yf]
        if merged and abs(yf - merged[-1][0]) <= 2 and merged[-1][1] == cls:
            py, c_, a, b_, ln0 = merged[-1]
            merged[-1] = (py, c_, min(a, x0), max(b_, x1), max(ln, ln0))
        else:
            merged.append((yf, cls, x0, x1, ln))
    for yf, cls, x0, x1, ln in merged:
        print(f"  y~{yf} {cls:5s} x{x0}..{x1} (len {ln})")

# Table region: x56..904, y157..540
for img, scale, nm in [(orig, (1.0, 1.0), "ORIG"), (rend, (SX, SY), "RENDER27")]:
    stroke_census(img, scale, nm, 157, 540, 56, 904, 25)
    hstroke_census(img, scale, nm, 157, 540, 56, 904, 25)
