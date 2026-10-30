#!/usr/bin/env python3
"""probe69 — what ink actually lies in the perpendicular corridor (outlier -> blue line)?

Classifies every non-background pixel within +-6px of the perpendicular path for
both charts and prints it per scanline, so the shaft question is answered from
the pixels rather than from 1px point samples.
"""
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
A = np.asarray(Image.open(f"{ROOT}/unique_slides/slide_009.jpg").convert("RGB")).astype(int)
H, W, _ = A.shape

CHARTS = {
    "LEFT": dict(outlier=(197.5, 145.0), blue=((141, 351), (433, 201))),
    "RIGHT": dict(outlier=(611.0, 145.0), blue=((555, 387), (849, 247))),
}


def klass(rgb):
    r, g, b = rgb
    if r > 235 and g > 235 and b > 235:
        return "."           # white / near-white background
    if r > 200 and g < 160 and b < 90 and r - b > 120:
        return "O"           # orange data point
    if b > 120 and r < 120 and g < 120:
        return "B"           # blue fitted line
    if r > 110 and g < 85 and b < 95:
        return "R"           # strong red
    if r > 170 and g < 130 and b < 150 and r > g > b:
        return "p"           # rose / pink ink (label glyphs, pale leader)
    if b - r > 8:
        return "v"           # periwinkle / cool ink (dashed connector)
    if r > 215 and g > 215 and b > 215:
        return "-"
    return "?"


for name, cfg in CHARTS.items():
    ox, oy = cfg["outlier"]
    (bx0, by0), (bx1, by1) = cfg["blue"]
    dx, dy = bx1 - bx0, by1 - by0
    l2 = dx * dx + dy * dy
    t = ((ox - bx0) * dx + (oy - by0) * dy) / l2
    fx, fy = bx0 + t * dx, by0 + t * dy
    ux, uy = fx - ox, fy - oy
    L = np.hypot(ux, uy)
    ux, uy = ux / L, uy / L

    print(f"\n===== {name}: corridor outlier({ox},{oy}) -> foot({fx:.1f},{fy:.1f}) "
          f"len={L:.1f} ang={np.degrees(np.arctan2(uy, ux)):.2f} =====")
    print("scanline map: each row = one y; chars span x within corridor+-7, left->right")
    for y in range(int(oy) - 6, int(fy) + 8):
        row = []
        for x in range(int(ox) - 10, int(fx) + 12):
            if 0 <= x < W and 0 <= y < H:
                row.append(klass(A[y, x]))
            else:
                row.append(" ")
        s = "".join(row)
        if s.strip(" .-") != "":
            print(f"  y={y:4d} |{s}|")
    print("  legend: . white  - near-white  O orange  B blue  R strong-red  p rose/pink  v periwinkle  ? other")
