#!/usr/bin/env python3
"""High-res ASCII of diagram right labels + eq boxes + red curve geometry."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_025.jpg").convert("RGB")
a = np.asarray(img).astype(int)


def cls(px):
    r, g, b = px
    if r > 140 and r - g > 45 and r - b > 45:
        return "R"
    if g > 110 and g - r > 35 and g - b > 35:
        return "G"
    if b > 130 and b - r > 40 and b - g > 25:
        return "B"
    if r > 90 and b > 90 and r - g > 25 and b - g > 25:
        return "P"
    if (r + g + b) / 3 < 140:
        return "#"
    if (r + g + b) / 3 > 245:
        return "."
    return "-"


def dump(name, x0, y0, x1, y1, cw=1, ch=2):
    crop = img.crop((x0, y0, x1, y1))
    sw, sh = crop.size[0] // cw, crop.size[1] // ch
    aa = np.asarray(crop.resize((sw, sh), Image.LANCZOS)).astype(int)
    print(f"\n=== {name} x{x0}-{x1} y{y0}-{y1} cw={cw} ===")
    print("     " + "".join(str(((x0 + c * cw) // 10) % 10) if c % 10 == 0 else " "
                           for c in range(sw)))
    for row in range(sh):
        print(f"{y0+row*ch:4d} " + "".join(cls(aa[row, c]) for c in range(sw)))


dump("DIAG ROW1 RIGHT", 655, 138, 830, 170, 1, 2)
dump("EQ1 INNER", 150, 172, 300, 232, 1, 2)

print("\n=== LEFT CHART red curve per column ===")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 140) & (r - g > 45) & (r - b > 45)
for x in range(110, 310, 10):
    ys = np.where(red[340:520, x])[0]
    print(f"  x={x}: rows {[int(v)+340 for v in ys]}")
