#!/usr/bin/env python3
"""Fine probes for A29 findings (a) column rectangles and (b) labels outside grid.
Targeted ink profiles + ASCII maps of the boundary zones, orig vs render_27."""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(ROOT + "/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(ROOT + "/recreated_pptx/qa/slide019/render_27.png").convert("RGB")).astype(int)
SX, SY = rend.shape[1] / orig.shape[1], rend.shape[0] / orig.shape[0]

def cls(px):
    r, g, b = px
    if r > 200 and g > 200 and b > 200:
        return "."
    if b > r + 30 and b > g + 20:
        return "B"          # blue/navy
    if r > g + 40 and r > b + 40:
        return "R"          # red/maroon
    if g > r + 30 and g > b + 30:
        return "G"          # green
    if abs(r - g) < 35 and abs(g - b) < 35:
        return "k"          # dark/neutral
    return "?"

def vprofile(img, scale, xf, y0, y1, tol=1):
    """Ink class runs down the column at frame x=xf (+-tol), frame y range."""
    X0 = int(round(xf * scale[0]))
    out = []
    for x in range(int((xf - tol) * scale[0]), int((xf + tol) * scale[0]) + 1):
        col = img[int(y0 * scale[1]):int(y1 * scale[1]), x]
        runs = []
        cur, n = None, 0
        for i, px in enumerate(col):
            c = cls(px)
            if c == cur:
                n += 1
            else:
                if cur not in (None, ".") and n >= 8:
                    runs.append((cur, n, i - n))
                cur, n = c, 1
        if cur not in (None, ".") and n >= 8:
            runs.append((cur, n, len(col) - n))
        if runs:
            out.append((x / scale[0], runs))
    return out

def show(img, scale, tag, xf, y0, y1):
    print(f"--- {tag} x~{xf} y{y0}..{y1}")
    for x, runs in vprofile(img, scale, xf, y0, y1):
        for c, n, start in runs:
            print(f"    x={x:6.1f} {c} y{y0 + start / scale[1]:.0f}..{y0 + (start + n) / scale[1]:.0f} (len {n / scale[1]:.0f})")

# Boundary zones: every candidate rule x, full table height
for xf in [376, 377, 378, 379, 382, 383, 384, 636, 637, 638, 642, 643, 644]:
    show(orig, (1.0, 1.0), "ORIG", xf, 160, 540)
print()
for xf in [376, 378, 383, 637, 643]:
    show(rend, (SX, SY), "REND", xf, 160, 540)
