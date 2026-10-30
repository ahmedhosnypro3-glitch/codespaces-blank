#!/usr/bin/env python3
"""ASCII-render the slide 017 original's bottom equation boxes so the exact
glyph layout (label text, brace, value column, condition column) is readable
without a vision call."""
import sys
import numpy as np
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "unique_slides/slide_017.jpg"
X0, X1, Y0, Y1 = (int(v) for v in (sys.argv[2:6] if len(sys.argv) > 6 else (110, 420, 450, 515)))

a = np.array(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (R > 120) & (G < 95) & (B < 95) & (R - G > 65)
green = (G > 80) & (G - R > 20) & (G - B > 20)
black = (R < 90) & (G < 90) & (B < 90)

CH = {True: "#"}
print(f"### {SRC} region x{X0}-{X1} y{Y0}-{Y1}  (R=red G=green K=black .=none)")
hdr = "".join(str((X0 + i) // 10 % 10) for i in range(X1 - X0 + 1))
hdr2 = "".join(str((X0 + i) % 10) for i in range(X1 - X0 + 1))
print("     " + hdr)
print("     " + hdr2)
for y in range(Y0, Y1 + 1):
    row = []
    for x in range(X0, X1 + 1):
        if red[y, x]:
            row.append("R")
        elif green[y, x]:
            row.append("G")
        elif black[y, x]:
            row.append("K")
        else:
            row.append(".")
    print(f"{y:4d} " + "".join(row))
