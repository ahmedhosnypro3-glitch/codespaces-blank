#!/usr/bin/env python3
"""Ground-truth probe for slide014 mid/lower regions: border detection + step-1 ASCII."""
from PIL import Image
import numpy as np
import sys

im = Image.open("unique_slides/slide_014.jpg").convert("RGB")
a = np.asarray(im).astype(int)


def cls(px):
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


def art(x0, x1, y0, y1, step=1):
    for y in range(y0, y1 + 1):
        print(f"{y:4d} " + "".join(cls(a[y, x]) for x in range(x0, x1 + 1, step)))


def raw(x0, x1, y0, y1, tag):
    print(f"\n-- raw {tag} x{x0}..{x1} y{y0}..{y1}")
    for y in range(y0, y1 + 1):
        vals = []
        for x in range(x0, x1 + 1):
            r, g, b = a[y, x]
            if r > 120 and g < 90 and b < 100:
                vals.append(f"{x}:({r},{g},{b})")
        if vals:
            print(f" y={y} " + " ".join(vals[:14]) + (" ..." if len(vals) > 14 else ""))


which = sys.argv[1] if len(sys.argv) > 1 else "all"

if which in ("all", "mb1"):
    print("=== MB1 borders (red-ish) ===")
    raw(60, 690, 344, 396, "mb1")
if which in ("all", "mb2"):
    print("=== MB2 borders (red-ish) ===")
    raw(80, 480, 398, 450, "mb2")
if which in ("all", "mb3"):
    print("=== MB3 borders (blue-ish) ===")
    for y in range(398, 452):
        vals = []
        for x in range(525, 890):
            r, g, b = a[y, x]
            if b > 100 and b - r > 30 and b - g > 30:
                vals.append(x)
        if len(vals) > 50:
            print(f" y={y} blue x{min(vals)}..{max(vals)} n={len(vals)}")
if which in ("all", "lb"):
    print("=== LOWER band borders ===")
    for y in range(462, 536):
        vals = []
        for x in range(60, 905):
            r, g, b = a[y, x]
            if b > 90 and b - r > 25 and b - g > 25:
                vals.append(x)
        if len(vals) > 40:
            print(f" y={y} blue x{min(vals)}..{max(vals)} n={len(vals)}")
    print("=== LOWER band vertical dark columns ===")
    for x in range(85, 890):
        cnt = 0
        for y in range(468, 530):
            r, g, b = a[y, x]
            if r + g + b < 400:
                cnt += 1
        if cnt > 25:
            print(f" x={x} dark rows={cnt}")
