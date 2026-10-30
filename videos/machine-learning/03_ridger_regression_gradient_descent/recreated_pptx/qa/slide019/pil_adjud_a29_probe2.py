#!/usr/bin/env python3
"""Probe 2: label-column zone, RIDGE10 top rule, W-box borders, y-band z-order."""
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
        return "Y"          # yellow band
    if b > r + 30 and b > g + 20:
        return "B"
    if r > g + 40 and r > b + 40:
        return "R"
    if g > r + 30 and g > b + 30:
        return "G"
    if abs(r - g) < 35 and abs(g - b) < 35:
        return "k"
    return "?"

def vprofile(img, scale, xf, y0, y1, tol=1, minlen=8):
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
                if cur not in (None, ".") and n >= minlen:
                    runs.append((cur, n, i - n))
                cur, n = c, 1
        if cur not in (None, ".") and n >= minlen:
            runs.append((cur, n, len(col) - n))
        if runs:
            out.append((x / scale[0], runs))
    return out

def show(img, scale, tag, xf, y0, y1, minlen=8):
    print(f"--- {tag} x~{xf} y{y0}..{y1}")
    for x, runs in vprofile(img, scale, xf, y0, y1, minlen=minlen):
        s = "  ".join(f"{c} y{y0 + a / scale[1]:.0f}..{y0 + (a + n) / scale[1]:.0f}({n / scale[1]:.0f})" for c, n, a in runs)
        print(f"    x={x:6.1f} {s}")

def hprofile(img, scale, yf, x0, x1, tol=1, minlen=8):
    Y0 = int(round(yf * scale[1]))
    print(f"--- {tag_h(img)} y~{yf} x{x0}..{x1}")
    for y in range(int((yf - tol) * scale[1]), int((yf + tol) * scale[1]) + 1):
        row = img[y, int(x0 * scale[0]):int(x1 * scale[0])]
        runs = []
        cur, n = None, 0
        for i, px in enumerate(row):
            c = cls(px)
            if c == cur:
                n += 1
            else:
                if cur not in (None, ".") and n >= minlen:
                    runs.append((cur, n, i - n))
                cur, n = c, 1
        if cur not in (None, ".") and n >= minlen:
            runs.append((cur, n, len(row) - n))
        if runs:
            s = "  ".join(f"{c} x{x0 + a / scale[0]:.0f}..{x0 + (a + n) / scale[0]:.0f}({n / scale[0]:.0f})" for c, n, a in runs)
            print(f"    y={y / scale[1]:6.1f} {s}")

def tag_h(img):
    return "ORIG" if img is orig else "REND"

# 1) RIDGE 10 top rule? scan horizontal at y166..176 x640..900
for yf in [168, 169, 170, 171]:
    hprofile(orig, (1.0, 1.0), yf, 600, 910)
print()
# 2) test-grid left edges + label zone (finding b): NO REG x0=124
for xf in [204, 205, 206, 207]:
    show(orig, (1.0, 1.0), "ORIG", xf, 195, 540)
print()
for xf in [205, 206]:
    show(rend, (SX, SY), "REND", xf, 195, 540)
print()
# 3) RIDGE 3 x0=384: grid left edge candidates x464..467
for xf in [464, 465, 466]:
    show(orig, (1.0, 1.0), "ORIG", xf, 195, 540)
print()
# 4) RIDGE 10 x0=644: grid left edge candidates x722..725
for xf in [722, 723, 724]:
    show(orig, (1.0, 1.0), "ORIG", xf, 195, 540)
print()
# 5) x640/641 in orig (lambda3 right / test grid right)
for xf in [640, 641]:
    show(orig, (1.0, 1.0), "ORIG", xf, 160, 540)
