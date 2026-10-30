#!/usr/bin/env python3
"""Fine 2px/char ASCII map of slide_025 left equation column to read glyphs."""
from PIL import Image
import numpy as np

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_025.jpg").convert("RGB")


def cls(px):
    r, g, b = px
    if r > 140 and r - g > 45 and r - b > 45:
        return "R"
    if g > 110 and g - r > 35 and g - b > 35:
        return "G"
    if b > 140 and b - r > 45 and b - g > 35:
        return "B"
    if r > 90 and b > 90 and r - g > 25 and b - g > 25:
        return "P"
    if (r + g + b) / 3 < 120:
        return "#"
    if (r + g + b) / 3 > 240:
        return "."
    return " "


def dump(name, x0, y0, x1, y1, cw=2, ch=3):
    crop = img.crop((x0, y0, x1, y1))
    w, h = crop.size
    sw, sh = w // cw, h // ch
    small = crop.resize((sw, sh), Image.LANCZOS)
    a = np.asarray(small).astype(int)
    print(f"\n=== {name} px x{x0}-{x1} y{y0}-{y1} ({cw}px/char,{ch}px/row) ===")
    print("      " + "".join(str(((x0 + c * cw) // 10) % 10) if c % 10 == 0 else " "
                            for c in range(sw)))
    for row in range(sh):
        line = "".join(cls(a[row, c]) for c in range(sw))
        py = y0 + row * ch
        print(f"{py:4d} {line}")


dump("EQ COLUMN", 52, 168, 300, 236, 2, 3)
dump("EQ COLUMN 2", 52, 236, 300, 302, 2, 3)
