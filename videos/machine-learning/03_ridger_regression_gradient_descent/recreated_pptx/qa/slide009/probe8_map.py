#!/usr/bin/env python3
"""Probe 8: fine ASCII class map of the left/right chart regions."""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def cls(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R > 248 and G > 248 and B > 248:
        return " "                      # pure white
    if B - R > 45 and B < 200:
        return "N"                      # navy border
    if B - R > 12 and B > 200:
        return "b"                      # pale blue
    if abs(R - 233) < 9 and abs(G - 231) < 11 and abs(B - 230) < 13:
        return "."                      # panel gray
    if R - G > 40 and R - B > 10 and R > 90:
        return "R"                      # red
    if B - R > 40 and B - G > 30 and B > 120:
        return "B"                      # blue line
    if R > 200 and G > 100 and G < 210 and B < 130 and R - G > 40:
        return "O"                      # orange
    if R < 95 and G < 95 and B < 95:
        return "k"                      # dark text
    if abs(R - G) < 14 and abs(G - B) < 14 and R > 225:
        return "g"                      # light gray (grid)
    if R > 235 and G > 230 and B < 200:
        return "Y"                      # yellow badge
    return "?"                          # other

def dump(x0, x1, y0, y1, step=4):
    print(f"\n=== x {x0}..{x1}  y {y0}..{y1}  (step {step}px) ===")
    hdr = "      "
    for x in range(x0, x1, step):
        hdr += str((x // 10) % 10) if x % 20 < step else " "
    print(hdr)
    for y in range(y0, y1, step):
        row = ""
        for x in range(x0, x1, step):
            row += cls(a[y, x])
        print(f"{y:5d} {row}")

dump(85, 480, 95, 545)      # LEFT panel
dump(475, 910, 95, 545)     # RIGHT panel
