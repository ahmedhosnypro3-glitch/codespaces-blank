#!/usr/bin/env python3
"""ASCII-art dump of text regions so glyph shapes/colors are legible without vision."""
from PIL import Image
import numpy as np
import sys

def classify(px):
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    s = r + g + b
    if s < 330:
        if r > g + 40 and r > b + 40: return "R"
        if b > r + 40: return "B"
        if g > r + 25 and g > b + 25: return "G"
        return "K"
    if r > g + 45 and r > b + 45 and s < 620: return "r"
    if b > r + 35 and b > g + 20 and s < 720: return "b"
    if g > r + 20 and g > b + 20 and s < 720: return "g"
    return "."

def art(a, x0, x1, y0, y1, label, step=1):
    print(f"\n=== {label}  x{x0}..{x1} y{y0}..{y1} (step {step}) ===")
    hdr = "     " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x0, x1 + 1, step))
    print(hdr)
    for y in range(y0, y1 + 1):
        row = "".join(classify(a[y, x]) for x in range(x0, x1 + 1, step))
        print(f"{y:4d} {row}")

im = Image.open("unique_slides/slide_014.jpg").convert("RGB")
a = np.asarray(im).astype(int)
which = sys.argv[1] if len(sys.argv) > 1 else "all"

if which in ("all", "mb1"):
    art(a, 88, 668, 348, 392, "MIDBAND1 peach (red border + text)", step=2)
if which in ("all", "mb2"):
    art(a, 88, 472, 402, 446, "MIDBAND2 peach", step=2)
if which in ("all", "mb3"):
    art(a, 532, 882, 402, 446, "MIDBAND3 yellow", step=2)
if which in ("all", "mb1x"):
    art(a, 550, 668, 348, 392, "MIDBAND1 right part detail", step=1)
if which in ("all", "lb"):
    art(a, 170, 800, 468, 530, "LOWER BLUE band text", step=2)
