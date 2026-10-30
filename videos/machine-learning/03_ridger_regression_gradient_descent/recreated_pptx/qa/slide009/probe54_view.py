#!/usr/bin/env python3
"""Probe 54: coarse colour-classified ASCII view of the whole slide (96x54)."""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
im = Image.open(FRAME).convert("RGB").resize((96, 54), Image.LANCZOS)
a = np.asarray(im).astype(int)


def cls(p):
    r, g, b = p
    mx, mn = max(r, g, b), min(r, g, b)
    sat = mx - mn
    if sat < 18:
        if mx > 248: return "."
        if mx > 235: return ","
        if mx > 210: return "-"
        if mx > 170: return "="
        return "#"
    # saturated
    if r >= g and r >= b:
        if g > 90 and b < 100 and r > 180: return "O"      # orange
        if g < 70 and b < 90: return "R"                    # pure red
        return "r"                                           # pale red
    if b >= g and b >= r:
        if b - r > 60: return "B"                            # blue / navy
        return "b"                                           # pale blue
    if g >= r and g >= b:
        if g - r > 25: return "C"                            # cyan/green
        return "c"
    return "?"


hdr = "    " + "".join(str((x // 10) % 10) for x in range(0, 96, 1))
print("     0123456789" * 9 + "012345")
for y in range(54):
    row = "".join(cls(a[y, x]) for x in range(96))
    print(f"  {y*10:3d} {row}")
print("\nlegend: . near-white  , v.light  - light  = mid  # dark")
print("        O orange   R pure red   r pale red   B blue/navy   b pale blue   C cyan   c pale cyan")
