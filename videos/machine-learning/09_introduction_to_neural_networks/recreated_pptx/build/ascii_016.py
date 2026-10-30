#!/usr/bin/env python3
"""Coarse ASCII ink map of slide_016 original (and optionally a render).

Classes: '#' black, 'R' strong red, 'r' frame red, 'B' blue, 'Y' yellow, '.' bg
"""
import sys
from PIL import Image
import numpy as np

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_016.jpg"
REND = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_016_rendered-1.png"


def amap(path, label, step_x=8, step_y=6):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    h, w = a.shape[:2]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(axis=2)
    bg = (abs(r - 234) < 10) & (abs(g - 234) < 10) & (abs(b - 234) < 10)
    strong_red = (r > 165) & (g < 90) & (b < 90)
    frame_red = (~bg) & (r >= 100) & (r <= 165) & (g < 80) & (b < 80)
    blue = (b > 90) & (b - r > 60) & (b - g > 60)
    black = (mx < 110) & (~bg)
    yellow = (r > 190) & (g > 165) & (b < 160) & (r - b > 55)
    print(f"\n===== {label} ({w}x{h}) step {step_x}x{step_y} =====")
    print("     " + "".join(str((c * step_x // 10) % 10) for c in range(w // step_x)))
    for y in range(0, h, step_y):
        row = ""
        for x in range(0, w, step_x):
            blk = slice(y, min(y + step_y, h)), slice(x, min(x + step_x, w))
            if black[blk].any():
                row += "#"
            elif yellow[blk].any():
                row += "Y"
            elif blue[blk].any():
                row += "B"
            elif strong_red[blk].any():
                row += "R"
            elif frame_red[blk].any():
                row += "r"
            elif bg[blk].any():
                row += "."
            else:
                row += "o"
        print(f"{y:4d} {row}")


amap(ORIG, "ORIGINAL slide_016.jpg")
if len(sys.argv) > 1 and sys.argv[1] == "both":
    amap(REND, "FRESH RENDER", step_x=16, step_y=10)
