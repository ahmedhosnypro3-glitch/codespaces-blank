#!/usr/bin/env python3
"""ASCII map of an RGBA equation asset (alpha-aware)."""
import sys
from PIL import Image

path = sys.argv[1]
step = int(sys.argv[2]) if len(sys.argv) > 2 else 8
im = Image.open(path).convert("RGBA")
w, h = im.size
im2 = im.resize((max(1, w // step), max(1, h // step)), Image.LANCZOS)
px = im2.load()
W, H = im2.size
print(f"{path} ({w}x{h}) -> {W}x{H} ascii, step={step}")
for y in range(H):
    row = ""
    for x in range(W):
        r, g, b, a = px[x, y]
        if a < 60:
            ch = "."
        elif r > 150 and g < 120:
            ch = "R"
        elif r < 120 and g < 120 and b < 120:
            ch = "#"
        else:
            ch = "+"
        row += ch
    print(f"{y:3d} {row}")
