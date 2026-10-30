#!/usr/bin/env python3
"""1:1 ASCII ink maps of logo sub-regions to read glyph structure."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)


def pxmap(x0, x1, y0, y1, mode="logo"):
    print(f"--- 1:1 map x{x0}..{x1}, y{y0}..{y1} (T=teal, c=cyan-wash, .=white, #=dark, g=gray-ink, m=mauve, space=panel) ---")
    hdr1 = "    " + "".join(str((x0 + i) // 100 % 10) for i in range(x1 - x0))
    hdr2 = "    " + "".join(str((x0 + i) // 10 % 10) for i in range(x1 - x0))
    print(hdr1)
    print(hdr2)
    for y in range(y0, y1):
        line = []
        for x in range(x0, x1):
            r, g, b = IM[y, x]
            if g > 100 and b > 100 and r < 130 and abs(g - b) < 60:
                ch = "T"
            elif r > 240 and g > 240 and b > 238:
                ch = "."
            elif r < 100 and g < 100 and b < 115:
                ch = "#"
            elif abs(r - 231) < 12 and abs(g - 233) < 12 and abs(b - 230) < 14:
                ch = " "
            elif r > 110 and g > 190 and b > 190:
                ch = "c"  # cyan wash (white text on teal)
            elif abs(r - g) < 22 and abs(g - b) < 22 and r < 210:
                ch = "g"  # neutral gray ink
            else:
                ch = "m"  # mauve/pink
            line.append(ch)
        print(f"{y:3d} " + "".join(line))


print("=== TEAL PANEL full interior ===")
pxmap(592, 678, 458, 532)

print("\n=== WHITE PANEL band A (Arabic?) y478..500 ===")
pxmap(676, 890, 478, 500)

print("\n=== WHITE PANEL band B (English?) y502..520 ===")
pxmap(676, 890, 502, 520)
