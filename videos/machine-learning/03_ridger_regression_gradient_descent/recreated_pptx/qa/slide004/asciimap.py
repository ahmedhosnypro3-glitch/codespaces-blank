#!/usr/bin/env python3
"""ASCII ink map of a region, for structural identification without vision."""
import sys
from PIL import Image

IMGPATH = sys.argv[1]
X0, X1 = int(sys.argv[2]), int(sys.argv[3])
Y0, Y1 = int(sys.argv[4]), int(sys.argv[5])
STEP = int(sys.argv[6]) if len(sys.argv) > 6 else 2

img = Image.open(IMGPATH).convert("RGB")
if img.size != (960, 540):
    img = img.resize((960, 540), Image.LANCZOS)
p = img.load()


def ch(p):
    r, g, b = p
    if r > 235 and g > 235 and b > 235:
        return "."
    if r > 150 and g < 120 and b < 120:
        return "R"
    if r > 205 and g > 155 and b > 155:
        return "p"
    if r < 120 and g < 120 and b < 120:
        return "#"
    if b > 150 and r < 130:
        return "B"
    return "+"


hdr = "     " + "".join(str((x // 10) % 10) if (x // STEP) % 5 == 0 else " " for x in range(X0, X1, STEP))
print(f"{IMGPATH}  x{X0}..{X1} y{Y0}..{Y1}")
print(hdr)
for y in range(Y0, Y1, STEP):
    row = "".join(ch(p[x, y]) for x in range(X0, X1, STEP))
    print(f"y{y:3d} {row}")
