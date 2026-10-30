#!/usr/bin/env python3
"""ASCII color maps: outlier column + table block 1, orig vs render_20.
3px cells; classes: K black, N navy(35,30,86), P purple(115,106,184),
B brightblue(89,89,255), R red, M maroon(139,58,58), Y yellow, G gray,
E panel E9E9E7, W white/bg."""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019/render_20.png"
O = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"
ri = Image.open(R).convert("RGB"); oi = Image.open(O).convert("RGB")
ra = np.asarray(ri).astype(int); oa = np.asarray(oi).astype(int)
RS = ri.size[0] / 960.0

def cls(v):
    r, g, b = v
    s = r + g + b
    if s > 720: return "W"
    if abs(r - 233) < 14 and abs(g - 233) < 14 and abs(b - 231) < 14: return "E"
    if r > 170 and g > 170 and b < 160: return "Y"
    if r > 150 and r - g > 70 and r - b > 70: return "R"
    if 90 < r < 180 and 40 < g < 110 and 40 < b < 110 and r - g > 45: return "M"
    if b - r > 60 and b > 150: return "B"
    if 60 < r < 150 and b > 140 and b - g > 40 and abs(int(r) - int(g)) < 35: return "P"
    if b - r > 25 and s < 330: return "N"
    if abs(int(r) - int(g)) < 30 and abs(int(g) - int(b)) < 30 and s < 420: return "K"
    if abs(int(r) - int(g)) < 25 and abs(int(g) - int(b)) < 25 and s < 600: return "G"
    return "."

def amap(tag, a, s, x0, y0, x1, y1, cell):
    c = a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    h, w = c.shape[:2]
    rows = []
    hdr = "     " + "".join(str((x0 + i * cell) // 100 % 10) for i in range(0, w // cell, 10))
    print(tag)
    print(hdr)
    for cy in range(0, h - cell + 1, cell):
        line = []
        for cx in range(0, w - cell + 1, cell):
            blk = c[cy:cy + cell, cx:cx + cell].reshape(-1, 3)
            # dominant non-bg class, else bg
            best, bn = ".", 0
            counts = {}
            for v in blk:
                k = cls(v)
                counts[k] = counts.get(k, 0) + 1
            for k, n in counts.items():
                if k in "KNRMBP" and n > bn:
                    best, bn = k, n
            if best == ".":
                best = counts.get("Y", 0) > cell * cell * 0.4 and "Y" or (counts.get("E", 0) > cell * cell * 0.5 and "E" or (counts.get("G", 0) > cell * cell * 0.4 and "G" or "W"))
            line.append(best)
        print(f"{y0 + cy:4d} " + "".join(line))

# outlier column full height, 3px cells
amap("=== ORIG outlier col x60..125 y160..530 ===", oa, 1.0, 60, 160, 125, 530, 3)
amap("=== REND20 outlier col x60..125 y160..530 ===", ra, RS, 60, 160, 125, 530, 3)
