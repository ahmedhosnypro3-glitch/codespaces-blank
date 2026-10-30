#!/usr/bin/env python3
"""Fine ASCII map of slide_025 left column + diagram regions (text-readable)."""
from PIL import Image
import numpy as np

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_025.jpg").convert("RGB")


def cls(px):
    r, g, b = px
    if r > 200 and g > 200 and b < 175:
        return "Y"
    if r > 140 and r - g > 45 and r - b > 45:
        return "R"
    if b > 140 and b - r > 45 and b - g > 35:
        return "B"
    if r > 90 and b > 90 and r - g > 25 and b - g > 25:
        return "P"
    if g > 110 and g - r > 35 and g - b > 35:
        return "G"
    if r > 200 and 120 < g < 200 and b < 110:
        return "O"
    if (r + g + b) / 3 < 110:
        return "#"
    if (r + g + b) / 3 > 235:
        return "."
    if 175 < (r + g + b) / 3 < 235:
        return "-"
    return " "


def dump(name, x0, y0, x1, y1, cw=4, ch=4):
    crop = img.crop((x0, y0, x1, y1))
    w, h = crop.size
    sw, sh = w // cw, h // ch
    small = crop.resize((sw, sh), Image.LANCZOS)
    a = np.asarray(small).astype(int)
    print(f"\n=== {name}  px x{x0}-{x1} y{y0}-{y1}  ({cw}px/char) ===")
    print("      " + "".join(str(((x0 + c * cw) // 10) % 10) if c % 10 == 0 else " "
                            for c in range(sw)))
    for row in range(sh):
        line = "".join(cls(a[row, c]) for c in range(sw))
        py = y0 + row * ch
        print(f"{py:4d}  {line}  y={py/72:.2f}in")


dump("LEFT COLUMN", 40, 115, 310, 310, 3, 4)
dump("CENTER DIAGRAM", 300, 120, 660, 310, 4, 5)
dump("DIAGRAM RIGHT", 600, 120, 960, 310, 4, 5)
