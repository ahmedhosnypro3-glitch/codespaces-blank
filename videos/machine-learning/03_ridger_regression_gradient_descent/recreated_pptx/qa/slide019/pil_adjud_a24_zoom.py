#!/usr/bin/env python3
"""1px color-coded ASCII of original outlier groups 1 and 3 (+render_24)."""
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{V}/recreated_pptx/qa/slide019"

def cls(px):
    r, g, b = px
    if r > 200 and g > 200 and b < 190: return "y"          # yellow bg
    if b > r + 25 and b > g + 25 and b > 70: return "B"     # blue
    if r > g + 45 and r > b + 45 and r > 90: return "R"     # red
    if g > r + 30 and g > b + 30 and g > 90: return "G"     # green
    if r < 120 and g < 120 and b < 120: return "#"          # dark
    return "."

def dump(img, x0, x1, y0, y1, sx=1.0, sy=1.0, label=""):
    px = img.load()
    print(f"-- {label} frame x{x0}..{x1} y{y0}..{y1} (1 char = 1px) --")
    print("    " + "".join(str((x0 + i) % 10) for i in range(x1 - x0)))
    for fy in range(y0, y1):
        row = []
        for fx in range(x0, x1):
            cxx, cyy = int(fx * sx), int(fy * sy)
            if cxx >= img.size[0] or cyy >= img.size[1]:
                row.append("?"); continue
            row.append(cls(px[cxx, cyy]))
        print(f"y{fy:3d} " + "".join(row))

orig = Image.open(f"{V}/unique_slides/slide_019.jpg").convert("RGB")
rend = Image.open(f"{Q}/render_24.png").convert("RGB")
SX = rend.size[0] / orig.size[0]; SY = rend.size[1] / orig.size[1]

dump(orig, 74, 116, 190, 292, label="ORIG group1")
print()
dump(orig, 70, 116, 424, 500, label="ORIG group3")
print()
dump(rend, 74, 116, 190, 292, SX, SY, label="REND24 group1")
