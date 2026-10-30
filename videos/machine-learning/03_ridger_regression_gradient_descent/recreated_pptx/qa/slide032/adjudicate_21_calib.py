#!/usr/bin/env python3
"""Slide 032 — ink-bbox calibration of every graph label, original vs render.

Known-good labels ("(2, 10)", "(5, 1)", tick numbers, the two segment "3"
marks) calibrate the render's type size against the frame; the right
chord-endpoint label is then judged on the same yardstick.
"""
import os
from PIL import Image

DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_032.jpg"
REND = DECK + "/recreated_pptx/qa/slide032/render_10.png"
SC = 2001.0 / 540.0

REGIONS = [
    ("y-tick 15", 600, 74, 630, 96),
    ("y-tick 10", 600, 134, 630, 156),
    ("y-tick 5", 600, 194, 630, 216),
    ("x-tick -5", 560, 256, 590, 280),
    ("x-tick 0", 612, 256, 645, 280),
    ("x-tick 5", 670, 256, 700, 280),
    ("x-tick 10", 728, 256, 760, 280),
    ("x-tick 15", 785, 256, 815, 280),
    ("label (2, 10)", 612, 138, 668, 162),
    ("label (5, 1)", 682, 240, 722, 262),
    ("RIGHT label", 712, 132, 762, 158),
    ("segment 3 L", 655, 122, 690, 148),
    ("segment 3 R", 688, 122, 722, 148),
]

def inkbox(im, x0, y0, x1, y1, thr):
    px = im.load()
    xs, ys, n = [], [], 0
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            v = px[x, y]
            if v < thr:
                xs.append(x); ys.append(y); n += 1
    if not n:
        return None
    return min(xs), min(ys), max(xs), max(ys), n

o = Image.open(ORIG).convert("L")
r = Image.open(REND).convert("L")
print(f"original {o.size}  render {r.size}  scale {r.size[1]/540.0:.4f}\n")
print(f"{'region':<15} {'orig ink bbox (frame px)':<30} {'render ink bbox (frame px)':<32} "
      f"{'dW':>5} {'dH':>5} {'dxL':>5} {'dxT':>5}")
for name, x0, y0, x1, y1 in REGIONS:
    a = inkbox(o, x0, y0, x1, y1, 190)
    rx0, ry0 = round(x0 * SC), round(y0 * SC)
    rx1, ry1 = round(x1 * SC), round(y1 * SC)
    b = inkbox(r, rx0, ry0, rx1, ry1, 190)
    if a and b:
        aw = a[2] - a[0] + 1
        ah = a[3] - a[1] + 1
        bw = (b[2] - b[0] + 1) / SC
        bh = (b[3] - b[1] + 1) / SC
        print(f"{name:<15} x{a[0]}..{a[2]} y{a[1]}..{a[3]} ({aw}x{ah})   "
              f"x{a[0]}..{a[2]} (render {b[0]}..{b[2]}, {bw:.1f}x{bh:.1f})   "
              f"{bw-aw:5.1f} {bh-ah:5.1f} { (b[0]/SC) - a[0]:5.1f} {(b[1]/SC) - a[1]:5.1f}")
    else:
        print(f"{name:<15} orig={a} render={b}")
