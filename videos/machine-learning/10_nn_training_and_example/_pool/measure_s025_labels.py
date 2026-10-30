#!/usr/bin/env python3
"""Decide diagram right-side labels + chart interiors."""
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
    if (r + g + b) / 3 < 130:
        return "#"
    if (r + g + b) / 3 > 245:
        return "."
    return "-"


def dump(name, x0, y0, x1, y1, cw=2, ch=3):
    crop = img.crop((x0, y0, x1, y1))
    w, h = crop.size
    sw, sh = w // cw, h // ch
    small = crop.resize((sw, sh), Image.LANCZOS)
    aa = np.asarray(small).astype(int)
    print(f"\n=== {name} px x{x0}-{x1} y{y0}-{y1} ===")
    print("      " + "".join(str(((x0 + c * cw) // 10) % 10) if c % 10 == 0 else " "
                            for c in range(sw)))
    for row in range(sh):
        print(f"{y0+row*ch:4d} " + "".join(cls(aa[row, c]) for c in range(sw)))


dump("RIGHT LABELS", 640, 128, 830, 290, 2, 4)
dump("NODE BIAS", 310, 275, 400, 310, 2, 3)

print("\n=== chart interiors ===")
print("left chart (200,300):", tuple(a[300, 200]), " (200,500):", tuple(a[500, 200]),
      " (300,430):", tuple(a[430, 300]))
print("right chart (500,450):", tuple(a[450, 500]), " (800,500):", tuple(a[500, 800]),
      " (600,300):", tuple(a[300, 600]))
print("left chart grid y=430 x=100..340:", [tuple(a[430, x]) for x in (100, 150, 200, 250, 300)])
print("left chart y-axis x=56 vs x=57:", tuple(a[400, 56]), tuple(a[400, 57]))
print("right chart interior row 450 x 400..880 step 60:",
      [tuple(a[450, x]) for x in range(400, 881, 60)])
print("right chart col scan x=600 y 380..510 step 20:",
      [tuple(a[y, 600]) for y in range(380, 511, 20)])
