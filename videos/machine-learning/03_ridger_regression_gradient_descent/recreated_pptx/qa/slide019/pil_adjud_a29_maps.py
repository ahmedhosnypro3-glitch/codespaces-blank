#!/usr/bin/env python3
# pil_adjud_a29_maps.py — grayscale+ramp ASCII maps of the two decisive regions.
# ORIG frame px == pt. Saturated pixels tagged R/B/G/y/#; else luminance ramp.
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
oi = Image.open(ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg").convert("RGB")
op = oi.load()
RAMP = " .:-=+*#%@"

def ch(x, y):
    r, g, b = op[x, y]
    if r > 180 and g < 110 and b < 110: return "R"
    if b > 140 and r < 110 and g < 110: return "B"
    if g > 110 and r < 110 and b < 110: return "G"
    if r > 225 and g > 225 and b < 165: return "y"
    lum = (r * 299 + g * 587 + b * 114) // 1000
    return RAMP[min(9, (255 - lum) * 10 // 256)]

def map_region(x0, x1, y0, y1, title, half=None):
    cols = list(range(x0, x1))
    seg = cols[: len(cols) // 2] if half == 1 else (cols[len(cols) // 2:] if half == 2 else cols)
    print(f"== {title} x{x0}..{x1-1} y{y0}..{y1-1} (part {half or 'all'}) ==")
    print("      " + "".join(str((x // 100) % 10) for x in seg))
    print("      " + "".join(str((x // 10) % 10) for x in seg))
    print("      " + "".join(str(x % 10) for x in seg))
    for y in range(y0, y1):
        print(f"y{y:<4}" + "".join(ch(x, y) for x in seg))

import sys
which = sys.argv[1] if len(sys.argv) > 1 else "all"
if which in ("noreg", "all"):
    map_region(204, 382, 200, 302, "ORIG NO REG g1", 1)
    map_region(204, 382, 200, 302, "ORIG NO REG g1", 2)
if which in ("ridge3", "all"):
    map_region(460, 645, 415, 520, "ORIG RIDGE3 g3", 1)
    map_region(460, 645, 415, 520, "ORIG RIDGE3 g3", 2)
