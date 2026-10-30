#!/usr/bin/env python3
"""Slide 032 — exact ink runs (x, y, RGB, class) for the original's right-label area.

Distinguishes RED plot-border ink from BLACK glyph ink, so the label glyphs can
be isolated from the plot frame and from the chord.
"""
import os
from PIL import Image

ROOT = "/worksp""aces/codespaces-blank/ai_llm_slides"
DECK = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent")
ORIG = os.path.join(DECK, "unique_slides/slide_032.jpg")
REND = os.path.join(DECK, "recreated_pptx/qa/slide032/render_10.png")

def cls(r, g, b):
    if r > 200 and g > 200 and b > 200:
        return "."
    if r > 110 and g < 120 and b < 120 and r - g > 45:
        return "R"      # dark red
    if r < 110 and g < 110 and b < 110:
        return "K"      # black
    if r < 180 and g < 180 and b < 180:
        return "g"      # gray
    return "+"

def runs(path, label, x0, x1, y0, y1, thr=205, scale=1.0, xoff=0.0, yoff=0.0):
    im = Image.open(path).convert("RGB")
    px = im.load()
    print(f"===== {label} :: {path}")
    print(f"      frame x = (render_x - {xoff}) / {scale}")
    for y in range(y0, y1):
        fy = (y - yoff) / scale
        row = []
        x = x0
        while x < x1:
            r, g, b = px[x, y]
            if r < thr or g < thr or b < thr:
                c = cls(r, g, b)
                x2 = x
                while x2 < x1:
                    r2, g2, b2 = px[x2, y]
                    if r2 < thr or g2 < thr or b2 < thr:
                        x2 += 1
                    else:
                        break
                row.append((x, x2 - 1, c, (r, g, b)))
                x = x2
            else:
                x += 1
        if row:
            parts = []
            for a, b2, c, rgb in row:
                fx = (a - xoff) / scale
                parts.append(f"x{(a-xoff)/scale:6.1f}..{(b2+1-xoff)/scale:6.1f} {c} {rgb}")
            print(f"  y={(y-yoff)/scale:6.1f}  " + " | ".join(parts))
    print()

runs(ORIG, "ORIGINAL right-label area", 700, 770, 130, 162)
runs(REND, "RENDER_10 right-label area", 1458, 1604, 271, 337, thr=205, scale=2.0833, xoff=0.0, yoff=0.0)
