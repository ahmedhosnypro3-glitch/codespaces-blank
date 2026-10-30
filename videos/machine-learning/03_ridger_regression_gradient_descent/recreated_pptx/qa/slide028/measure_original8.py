#!/usr/bin/env python3
"""Pass 8: 1px-resolution ASCII zooms to settle the left-panel dot inventory."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
# blue-ness score: how far toward curve blue
score = (b - r) - 0.5 * (255 - b)  # high when blue & saturated


def zoom(x0, x1, y0, y1, label):
    print(f"\n== ZOOM {label}: x {x0}-{x1}, y {y0}-{y1} (1px/char; #=strong, +=mid, .=faint) ==")
    hdr1 = "".join(str((x0 + i) // 100 % 10) for i in range(x1 - x0))
    hdr2 = "".join(str((x0 + i) // 10 % 10) for i in range(x1 - x0))
    hdr3 = "".join(str((x0 + i) % 10) for i in range(x1 - x0))
    print("     " + hdr1)
    print("     " + hdr2)
    print("     " + hdr3)
    for yy in range(y0, y1):
        row = ""
        for xx in range(x0, x1):
            s = score[yy, xx]
            bl = b[yy, xx]
            if bl > 150 and s > 80:
                row += "#"
            elif bl > 120 and s > 40:
                row += "+"
            elif s > 15:
                row += "."
            else:
                row += " "
        print(f"{yy:4d} {row}")


zoom(234, 274, 394, 446, "LEFT arm terminal cluster")
zoom(170, 208, 236, 266, "left arm top: candidate dot (178,245)")
zoom(190, 212, 284, 312, "left arm dot at (198,294)")
zoom(214, 240, 348, 376, "left arm dot at (223,360)")
zoom(580, 610, 382, 412, "RIGHT panel dot at (593,396) reference shape")
