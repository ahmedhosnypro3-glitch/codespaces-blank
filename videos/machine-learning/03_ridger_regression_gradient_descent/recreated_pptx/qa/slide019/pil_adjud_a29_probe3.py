#!/usr/bin/env python3
"""Probe 3: NO REG test-grid interior (finding b) — vertical rules between
labels and value cells; row-separator extents; label glyph positions."""
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
    if r > 200 and g > 200 and b <= 200:
        return "Y"
    if b > r + 30 and b > g + 20:
        return "B"
    if r > g + 40 and r > b + 40:
        return "R"
    if g > r + 30 and g > b + 30:
        return "G"
    if abs(r - g) < 35 and abs(g - b) < 35:
        return "k"
    return "?"

def inkcol(img, scale, xf, y0, y1):
    """any non-background ink runs down frame column xf"""
    col = img[int(y0 * scale[1]):int(y1 * scale[1]), int(round(xf * scale[0]))]
    runs, cur, n = [], None, 0
    for i, px in enumerate(col):
        c = cls(px)
        if c == cur:
            n += 1
        else:
            if cur not in (None, "."):
                runs.append((cur, n, i - n))
            cur, n = c, 1
    if cur not in (None, "."):
        runs.append((cur, n, len(col) - n))
    return runs

# Vertical-rule scan across the whole NO REG test grid for both images
for tag, img, scale in [("ORIG", orig, (1.0, 1.0)), ("REND", rend, (SX, SY))]:
    print(f"===== {tag}: columns x208..378 with ink runs >=25 rows in y205..300 (NO REG row 1 grid) =====")
    for xf in range(208, 379):
        runs = inkcol(img, scale, xf, 205, 300)
        tot = sum(n for _, n, _ in runs)
        if tot >= 25 * scale[1]:
            s = "  ".join(f"{c} y{205 + a / scale[1]:.0f}..{205 + (a + n) / scale[1]:.0f}({n / scale[1]:.0f})" for c, n, a in runs if n >= 8)
            if s:
                print(f"  x={xf}: {s}")

print()
# Same for RIDGE 3 (x386..638) row 1
for tag, img, scale in [("ORIG", orig, (1.0, 1.0)), ("REND", rend, (SX, SY))]:
    print(f"===== {tag}: columns x386..638 with ink runs >=25 rows in y205..300 (RIDGE 3 row 1 grid) =====")
    for xf in range(386, 639):
        runs = inkcol(img, scale, xf, 205, 300)
        tot = sum(n for _, n, _ in runs)
        if tot >= 25 * scale[1]:
            s = "  ".join(f"{c} y{205 + a / scale[1]:.0f}..{205 + (a + n) / scale[1]:.0f}({n / scale[1]:.0f})" for c, n, a in runs if n >= 8)
            if s:
                print(f"  x={xf}: {s}")

print()
# Horizontal-row-separator extents inside NO REG grid, orig vs rend: y220..260
def hscan(img, scale, tag, y0, y1, x0, x1):
    print(f"===== {tag}: horizontal ink rows y{y0}..{y1} x{x0}..{x1} (runs >=60) =====")
    for yf in np.arange(y0, y1, 1.0):
        row = img[int(round(yf * scale[1])), int(x0 * scale[0]):int(x1 * scale[0])]
        runs, cur, n = [], None, 0
        for i, px in enumerate(row):
            c = cls(px)
            if c == cur:
                n += 1
            else:
                if cur not in (None, ".") and n >= 60 * scale[0]:
                    runs.append((cur, n, i - n))
                cur, n = c, 1
        if cur not in (None, ".") and n >= 60 * scale[0]:
            runs.append((cur, n, len(row) - n))
        if runs:
            s = "  ".join(f"{c} x{x0 + a / scale[0]:.0f}..{x0 + (a + n) / scale[0]:.0f}({n / scale[0]:.0f})" for c, n, a in runs)
            print(f"  y={yf:.0f}: {s}")

hscan(orig, (1.0, 1.0), "ORIG", 218, 262, 208, 380)
hscan(rend, (SX, SY), "REND", 218, 262, 208, 380)
