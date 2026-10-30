#!/usr/bin/env python3
"""ASCII maps of the NO REG and RIDGE 3 test grids, orig vs render_27."""
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
        return "y"          # yellow
    if b > r + 30 and b > g + 20:
        return "B"
    if r > g + 40 and r > b + 40:
        return "R"
    if g > r + 30 and g > b + 30:
        return "G"
    if abs(r - g) < 35 and abs(g - b) < 35:
        return "#"
    return "+"

def amap(img, scale, x0, x1, y0, y1, tag, ds=2):
    print(f"===== {tag} frame x{x0}..{x1} y{y0}..{y1} (downsample {ds}) =====")
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(x0, x1, ds))
    print(hdr)
    for yf in range(y0, y1, ds):
        row = []
        for xf in range(x0, x1, ds):
            # sample the ds x ds block, pick the darkest/most saturated class
            block = img[int(yf * scale[1]):int((yf + ds) * scale[1]), int(xf * scale[0]):int((xf + ds) * scale[0])]
            classes = [cls(px) for px in block.reshape(-1, 3)]
            order = {"#": 0, "B": 1, "R": 2, "G": 3, "+": 4, "y": 5, ".": 6}
            best = min(classes, key=lambda c: order[c])
            row.append(best if best != "." else ("y" if all(c in ".y" for c in classes) else "."))
        print(f"{yf:4d} " + "".join(row))

# NO REG grid + borders, row group 1
amap(orig, (1.0, 1.0), 200, 385, 200, 302, "ORIG NO REG g1")
amap(rend, (SX, SY), 200, 385, 200, 302, "REND NO REG g1")
