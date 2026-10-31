#!/usr/bin/env python3
"""ASCII map of the four formula boxes on slide_021 (text layout)."""
from PIL import Image
import numpy as np

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

BOXES = {
    "TL": (108, 50, 418, 110),
    "TR": (545, 50, 856, 110),
    "BL": (90, 281, 435, 344),
    "BR": (578, 285, 820, 342),
}
STEP = 4

for name, (x0, y0, x1, y1) in BOXES.items():
    print(f"\n=== {name} === x {x0}..{x1} y {y0}..{y1}  (each char = {STEP}px)")
    hdr = "     " + "".join(str(((x0 + c * STEP) // 10) % 10) for c in range((x1 - x0) // STEP))
    print(hdr)
    for y in range(y0, y1, STEP):
        row = ""
        for x in range(x0, x1, STEP):
            blk = a[y:y + STEP, x:x + STEP]
            r, g, b = blk[:, :, 0].mean(), blk[:, :, 1].mean(), blk[:, :, 2].mean()
            if r < 95 and g < 95 and b < 95:
                ch = "#"
            elif r > 120 and r - g > 45 and r - b > 45:
                ch = "R"
            elif g > 90 and g - r > 40 and g - b > 40:
                ch = "G"
            elif b - r > 45 and b - g > 35:
                ch = "B"
            elif r > 235 and 215 < g < 243:
                ch = "."
            elif r > 235 and g > 235 and b > 235:
                ch = " "
            else:
                ch = "o"
            row += ch
        print(f"{y:4d} {row}")
