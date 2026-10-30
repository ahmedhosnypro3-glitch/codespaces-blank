#!/usr/bin/env python3
"""Fine ASCII ink maps of specific regions of slide_016 original + color samples."""
from PIL import Image
import numpy as np

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_016.jpg"


def amap(a, label, x0, x1, y0, y1, sx=4, sy=4):
    sub = a[y0:y1, x0:x1]
    h, w = sub.shape[:2]
    bg = (abs(sub[..., 0] - 234) < 10) & (abs(sub[..., 1] - 234) < 10) & (abs(sub[..., 2] - 234) < 10)
    s_red = (sub[..., 0] > 165) & (sub[..., 1] < 90) & (sub[..., 2] < 90)
    f_red = (~bg) & (sub[..., 0] >= 100) & (sub[..., 0] <= 165) & (sub[..., 1] < 80) & (sub[..., 2] < 80)
    blue = (sub[..., 2] > 90) & (sub[..., 2] - sub[..., 0] > 60) & (sub[..., 2] - sub[..., 1] > 60)
    black = (sub.max(axis=2) < 110) & (~bg)
    yellow = (sub[..., 0] > 190) & (sub[..., 1] > 165) & (sub[..., 2] < 160) & (sub[..., 0] - sub[..., 2] > 55)
    white = (sub.min(axis=2) > 240)
    print(f"\n===== {label}  x[{x0},{x1}] y[{y0},{y1}] step {sx}x{sy} =====")
    for y in range(0, h, sy):
        row = ""
        for x in range(0, w, sx):
            blk = (slice(y, min(y + sy, h)), slice(x, min(x + sx, w)))
            if black[blk].any():
                row += "#"
            elif yellow[blk].any():
                row += "Y"
            elif blue[blk].any():
                row += "B"
            elif s_red[blk].any():
                row += "R"
            elif f_red[blk].any():
                row += "r"
            elif white[blk].any():
                row += " "
            elif bg[blk].any():
                row += "."
            else:
                row += "o"
        print(f"{y0+y:4d} {row}")


a = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
print("background samples:")
for (y, x) in [(3, 3), (20, 480), (30, 100), (40, 480), (45, 480), (100, 30), (100, 480),
               (150, 100), (300, 40), (400, 480), (500, 480), (530, 480), (480, 960),
               (60, 500), (300, 930), (300, 950), (200, 880)]:
    print(f"  (x={x},y={y}) -> {a[y, x].tolist()}")

# left edge structure
amap(a, "LEFT EDGE x[40,100] y[40,120]", 40, 100, 40, 120, sx=2, sy=2)
amap(a, "LEFT EDGE mid y[250,320]", 40, 100, 250, 320, sx=2, sy=2)
# badge
amap(a, "BADGE x[840,930] y[40,100]", 840, 930, 40, 100, sx=2, sy=2)
# title band
amap(a, "TITLE x[160,840] y[210,255]", 160, 840, 210, 255, sx=3, sy=2)
# subtitle band
amap(a, "SUBTITLE x[295,705] y[272,320]", 295, 705, 272, 320, sx=3, sy=2)
# bottom
amap(a, "BOTTOM x[30,960] y[505,540]", 30, 960, 505, 540, sx=8, sy=2)
